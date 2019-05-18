import os, sys
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam, SGD, Adamax, Adadelta, Adagrad, RMSprop, Nadam
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import preprocessing
import cv2


class CNN(object):

    def __init__(self, set=1, network_type="unknown",optimizer="Adam", seed_weight=3):
        if not os.path.isfile("actions/set%s_actions.csv" % set) and not os.path.isdir("images/set%s" % set):
            if set == 10:
                sys.stdout.write("Didn't find training sets\n")
                sys.exit(1)
            set += 1
        self.models = {
            "unknown": self.build_unknown_model,
            "CIFAR10": self.build_CIFAR10,
            "MLP": self.build_MLP_unknown,
            "VGG": self.build_VGG
        }
        if network_type not in list(self.models.keys()):
            sys.stdout.write("Invalid network type: %s\n" % network_type)
        self.optimizers = {
            "Adam": Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
            "SGD": SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False),
            "RMSprop": RMSprop(lr=0.0001, rho=0.9, epsilon=None, decay=1e-6),
            "Adagrad": Adagrad(lr=0.01, epsilon=None, decay=0.0),
            "Adadelta": Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0),
            "Adamax": Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0),
            "Nadam": Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
        }
        if optimizer not in list(self.optimizers.keys()):
            sys.stdout.write("Invalid optimizer: %s\n" % optimizer)
        self.optimizer = optimizer
        self.set = set
        np.random.seed(seed_weight)
        self.x = []
        self.y = []
        self.network_type = network_type
        self.classifications = 3
        self.img_num = 0
        self.img_count = len(os.listdir("images/set%s" % set))
        self.actions_count = 0
        self.actions = {}
        # map trained data
        self.map_actions()
        self.map_images()

    def map_actions(self):
        with open ('actions/set%s_actions.csv' % self.set, 'r') as f:
            for line in f:
                self.y.append(line.rstrip())
        # 1 jump 0 nothing 2 duck
        up = len([x for x in self.y if x == "1"])
        front = len([x for x in self.y if x == "0"])
        down = len([x for x in self.y if x == "2"])
        self.actions["up"] = up
        self.actions["front"] = front
        self.actions["down"] = down
        self.actions_count = up + front + down
        sys.stdout.write("Actions: %s\n" % self.actions)

    def map_images(self):
        all_images = []
        while self.img_num < self.img_count:
            if os.path.isfile("images/set%s/frame_%s.jpg" % (self.set,self.img_num)):
                img = cv2.imread("images/set%s/frame_%s.jpg" % (self.set,self.img_num), cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
                img = img[:, :, np.newaxis]
                # check images for errors
                # cv2.imshow("image", img)
                # cv2.waitKey(0)
                h, w, c = img.shape
                all_images.append(img)
                self.img_num += 1
            else:
                sys.stdout.write("Failed to open image %s\n" % (self.img_num))


        self.x = np.array(all_images)

    def build_VGG(self, input_shape):
        model = Sequential()
        # input: input_shape images with 3 channels -> (x?, y?, z?) tensors.
        # this applies 32 convolution filters of size 3x3 each.
        model.add(Conv2D(32, (2, 2), activation='relu', input_shape=input_shape))
        model.add(Conv2D(32, (2, 2), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (2, 2), activation='relu'))
        model.add(Conv2D(64, (2, 2), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.classifications, activation='softmax'))
        return model

    def build_MLP_unknown(self, input_shape):
        model = Sequential()
        model.add(Conv2D(100, kernel_size=(2, 2), strides=(2, 2), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.classifications, activation='sigmoid'))
        return model

    # simple deep CNN
    def build_CIFAR10(self, input_shape):
        model = Sequential()
        model.add(Conv2D(32, (2, 2), padding='same',
                         input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (2, 2)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (2, 2), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (2, 2)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.classifications))
        model.add(Activation('softmax'))
        return model

    def build_unknown_model(self,input_shape):
        # CNN model
        model = Sequential()
        model.add(Conv2D(100, kernel_size=(2, 2), strides=(2, 2), activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(250, activation='relu'))
        model.add(Dense(self.classifications, activation='softmax'))
        return model



    def start(self):
        # split into test and train set
        x_train, x_test, y_train, y_test = train_test_split(self.x, self.y, test_size=.2, random_state=5)

        ## input image dimensions
        img_x, img_y = 80, 270
        input_shape = (img_x, img_y, 1)

        # convert class vectors to binary class matrices for use in categorical_crossentropy loss below
        # number of action classifications
        y_train = keras.utils.to_categorical(y_train, self.classifications)
        y_test = keras.utils.to_categorical(y_test, self.classifications)

        # Load model and optimizer based on user input
        model = self.models[self.network_type](input_shape)
        optzr = self.optimizers[self.optimizer]

        model.compile(loss="categorical_crossentropy", optimizer=optzr, metrics=['accuracy'])

        graph_dir = "./Graph/%s/%s" % (self.network_type,self.optimizer)
        if not os.path.isdir(graph_dir):
            os.makedirs(graph_dir, exist_ok=True)
        # tensorboard data callback
        tbCallBack = keras.callbacks.TensorBoard(log_dir=graph_dir, histogram_freq=0, write_graph=True, write_images=True)

        model.fit(x_train, y_train, batch_size=300, epochs=120, validation_data=(x_test, y_test), callbacks=[tbCallBack])
        if not os.path.isdir("trained_models"):
            os.mkdir("trained_models")
        # Build name: networkType_optimizer_set(X)_trainingData.h5
        model_name = "trained_models/%s_%s_set%s.h5" % (self.network_type, self.optimizer, self.set)

        # save weights post training
        model.save(model_name)
