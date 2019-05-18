import os, argparse, sys
from network.network import CNN



class Trainer(object):
    """docstring for Trainer."""

    def __init__(self):
        super(Trainer, self).__init__()


    def run_neural_network(self):
        cnn = CNN(set=2, network_type="VGG")
        cnn.start()






if __name__ == '__main__':
    args = None
    Trainer().run_neural_network()
