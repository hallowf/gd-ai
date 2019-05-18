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
    parser = argparse.ArgumentParser(description='For training data')
    parser.add_argument("backend", help="Backend to use: (default/plaidml)", action="store", default="default")
    args = parser.parse_args()
    if args.backend == "plaidml":
        sys.stdout.write("Using plaidml\n")
        os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
    Trainer().run_neural_network()
