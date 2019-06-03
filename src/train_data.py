import os, argparse, sys
from network.keras_network import KMainframe

class Trainer(object):
    """docstring for Trainer."""
    def __init__(self, model, identifier, optzr, *args, **kwargs):
        self.model = model
        self.identifier = identifier
        self.optzr = optzr

    def recommended_optimizer(self):
        models = {
            "unknown": "Adam",
            "CIFAR10": "RMSprop",
            "MLP": "RMSprop",
            "VGG": "SGD"
        }
        return models[self.model]

    def run_neural_network(self, optimizer="recommended"):
        if optimizer == "recommended":
            self.optzr = self.recommended_optimizer()
        sys.stdout.write("Running %s on id: %s with optimizer %s\n" % (self.model, self.identifier, self.optzr))
        cnn = KMainframe(self.identifier, self.model, self.optzr)
        try:
            cnn.start()
        except Exception as e:
            print(e)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Trains a model with the data provided")
    parser.add_argument("identifier", type=str, help="An identifier for training data file")
    parser.add_argument("model", type=str, help="Model to build check instructions.md for available modules")
    parser.add_argument("--optzr","--optimizer", type=str, help="Optimizer to user with keras models only")
    args = parser.parse_args()
    optzr = args.optzr or "Adam"
    Trainer(args.model,args.identifier, optzr).run_neural_network()
