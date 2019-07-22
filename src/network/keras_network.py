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
            # these images should have been reshaped already in balance_data
            imgs = [i[0] for i in self.training_data]
            self.x = np.array(imgs) / 255
            self.actions["up"] = len([x[1] for x in self.training_data if x[1] == [0,1,0]])
            self.actions["front"] = len([x[1] for x in self.training_data if x[1] == [1,0,0]])
            self.actions["down"] = len([x[1] for x in self.training_data if x[1] == [0,0,1]])
            sys.stdout.write("Actions: %s\n" % self.actions)
            self.y = np.array([i[1] for i in self.training_data])
            # print("len y:", len(self.y))
        else:
            raise IOError("Missing data set: %s" % self.file_name)

    def start(self):
        ## input image dimensions
        img_x, img_y = 80, 270
        input_shape = (img_x, img_y, 1)
        # Load model and optimizer based on user input
        model = KModelBuilder(input_shape, self.model).return_model(self.identifier)
        optzr = self.optimizers[self.optzr]

        # split into test and train set
        X, test_x, Y, test_y = train_test_split(self.x, self.y, test_size=.2, random_state=5)
        # print(X[0].shape)
        # print(Y[0])

        model.compile(loss="categorical_crossentropy", optimizer=optzr, metrics=['accuracy'])

        graph_dir = "./Graph/%s/%s" % (self.model,self.optzr)
        if not os.path.isdir(graph_dir):
            os.makedirs(graph_dir, exist_ok=True)
        # tensorboard data callback
        tbCallBack = keras.callbacks.TensorBoard(log_dir=graph_dir, histogram_freq=0, write_graph=True, write_images=True)

        model.fit(X, Y, batch_size=30, epochs=3, validation_data=(test_x, test_y), callbacks=[tbCallBack])
        if not os.path.isdir("trained_models"):
            os.mkdir("trained_models")

        model_name = "trained_models/%s_%s_%s.h5" % (self.identifier, self.model, self.optzr)

        # save weights post training
        model.save(model_name)
