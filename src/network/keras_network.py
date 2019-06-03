import os, sys, time, threading
import keyboard
import keras
from sklearn.model_selection import train_test_split
import numpy as np
from keras.optimizers import Adam, SGD, Adamax, Adadelta, Adagrad, RMSprop, Nadam
# from sklearn import preprocessing
import cv2

from network.keras_models import KModelBuilder


class KMainframe(object):

    def __init__(self, identifier, model, optzr, seed_weight=3):
        self.identifier = identifier
        self.optimizers = {
            "Adam": Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
            "SGD": SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False),
            "RMSprop": RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0),
            "Adagrad": Adagrad(lr=0.01, epsilon=None, decay=0.0),
            "Adadelta": Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0),
            "Adamax": Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0),
            "Nadam": Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
        }
        if optzr not in list(self.optimizers.keys()):
            sys.stdout.write("Invalid optimizer: %s\n" % optimizer)
        self.optzr = optzr
        np.random.seed(seed_weight)
        self.file_name = "training/training_data_%s_balanced.npy" % identifier
        self.model = model
        self.classifications = 3
        self.actions = {}
        self.x = []
        self.y = []
        # map training data
        self.map_training_data()

    def map_training_data(self):
        # forward, jump, duck
        # [0,0,0]
        # 1 jump 0 nothing 2 duck
        if os.path.isfile(self.file_name):
            self.training_data = np.load(self.file_name)
            # imgs = np.array([i[0] for i in self.training_data]).reshape(-1,80,270,1)
            imgs = [i[0] for i in self.training_data]
            self.x = np.array(imgs)
            up = len([x[1] for x in self.training_data if x == [0,1,0]])
            front = len([x[1] for x in self.training_data if x == [1,0,0]])
            down = len([x[1] for x in self.training_data if x == [0,0,1]])
            self.actions["up"] = up
            self.actions["front"] = front
            self.actions["down"] = down
            sys.stdout.write("Actions: %s\n" % self.actions)
            self.y = np.array([i[1] for i in self.training_data])
            # print("len y:", len(self.y))
        else:
            raise IOError("Missing data set: %s" % self.file_name)



    # def map_images(self):
    #     all_images = []
    #     for item in self.training_data:
    #         if os.path.isfile("images/set%s/frame_%s.jpg" % (self.set,img_num)):
    #             img = cv2.imread("images/set%s/frame_%s.jpg" % (self.set,img_num), cv2.IMREAD_GRAYSCALE)
    #             img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    #             img = img[:, :, np.newaxis]
    #             # check images for errors
    #             # cv2.imshow("image", img)
    #             # cv2.waitKey(0)
    #             h, w, c = img.shape
    #             all_images.append(img)
    #             img_num += 1
    #             cv2.destroyAllWindows()
    #         else:
    #             sys.stdout.write("Failed to open image %s\n" % (img_num))
    #     self.mapping_images = False
    #     self.x = np.array(all_images)



    def start(self):
        ## input image dimensions
        img_x, img_y = 80, 270
        input_shape = (img_x, img_y, 1)
        # Load model and optimizer based on user input
        model = KModelBuilder(input_shape, self.model).return_model()
        optzr = self.optimizers[self.optzr]

        # split into test and train set
        X, test_x, Y, test_y = train_test_split(self.x, self.y, test_size=.2, random_state=5)
        print(X[0].shape)
        print(Y[0])
        # convert class vectors to binary class matrices for use in categorical_crossentropy loss below
        # number of action classifications
        # y_train = keras.utils.to_categorical(y_train, self.classifications)
        # y_test = keras.utils.to_categorical(y_test, self.classifications)
        # train and test data
        # self.training_data = np.load(self.file_name)
        # train = self.training_data[:-30]
        # test = self.training_data[-30:]
        # # Split data
        # X = np.array([i[0] for i in train]).reshape(-1, img_x, img_y, 1)
        # print(X.shape)
        # # print(X[0])
        # # print(X[0].shape)
        # Y = np.array([i[1] for i in train])
        # print(Y.shape)
        # # print(Y)
        # # print(Y[0].shape)
        # test_x = np.array([i[0] for i in test]).reshape(-1, img_x, img_y, 1)
        # test_y = np.array([i[1] for i in test])



        model.compile(loss="categorical_crossentropy", optimizer=optzr, metrics=['accuracy'])

        graph_dir = "./Graph/%s/%s" % (self.model,self.optzr)
        if not os.path.isdir(graph_dir):
            os.makedirs(graph_dir, exist_ok=True)
        # tensorboard data callback
        tbCallBack = keras.callbacks.TensorBoard(log_dir=graph_dir, histogram_freq=0, write_graph=True, write_images=True)

        model.fit(X, Y, batch_size=20, epochs=10, validation_data=(test_x, test_y), callbacks=[tbCallBack])
        if not os.path.isdir("trained_models"):
            os.mkdir("trained_models")

        model_name = "trained_models/%s_%s_%s.h5" % (self.identifier, self.model, self.optimizer)

        # save weights post training
        model.save(model_name)
