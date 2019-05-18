import os, argparse, sys
from network.network import CNN



class Trainer(object):
    """docstring for Trainer."""

    def __init__(self,network_type="unknown", optimizer="Adam"):
        self.network = network_type
        self.optimizer = optimizer


    def run_neural_network(self):
        cnn = CNN(set=2, network_type=self.network)
        cnn.start()






if __name__ == '__main__':
    args = None
    Trainer("CIFAR10").run_neural_network()
