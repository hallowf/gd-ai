import sys, os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D


class KModelBuilder(object):
    """docstring for KModelBuilder."""

    def __init__(self, input_shape, model):
        super(KModelBuilder, self).__init__()
        self.input_shape = input_shape
        self.classifications = 3
        self.models = {
            "unknown": self.build_unknown_model,
            "CIFAR10": self.build_CIFAR10,
            "MLP": self.build_MLP_unknown,
            "VGG": self.build_VGG
        }
        if model not in list(self.models.keys()):
            sys.stdout.write("Invalid network type: %s\n" % network_type)
        self.model = model

    def return_model(self):
        model = self.models[self.model]()
        if not os.path.isdir("trained_models"):
            os.mkdir("trained_models")
        model_summary = "trained_models/%s.txt" % (self.model)
        # with open(model_summary, "w") as f:
            # a = model.summary()
            # f.write(str(a))
        return model

    def build_unknown_model(self):
        # CNN model
        model = Sequential()
        model.add(Conv2D(100, kernel_size=(2, 2),
            strides=(2, 2), activation='relu', input_shape=self.input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(250, activation='relu'))
        model.add(Dense(self.classifications, activation='softmax'))
        return model

    def build_VGG(self):
        model = Sequential()
        # input: input_shape images with 3 channels -> (x?, y?, z?) tensors.
        # this applies 32 convolution filters of size 3x3 each.
        model.add(Conv2D(32, (2, 2), activation='relu',
            input_shape=self.input_shape))
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

    def build_MLP_unknown(self):
        model = Sequential()
        model.add(Conv2D(100, kernel_size=(2, 2),
            strides=(2, 2), activation='relu', input_shape=self.input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.classifications, activation='sigmoid'))
        return model

    # simple deep CNN
    def build_CIFAR10(self):
        model = Sequential()
        model.add(Conv2D(32, (2, 2), padding='same',
                         input_shape=self.input_shape))
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
