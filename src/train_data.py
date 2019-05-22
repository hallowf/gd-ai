import os, argparse, sys
from network.network import CNN



class Trainer(object):
    """docstring for Trainer."""
    def __init__(self, network_type="unknown",set=1):
        self.network = network_type
        self.set = set

    def recommended_optimizer(self):
        models = {
            "unknown": "Adam",
            "CIFAR10": "RMSprop",
            "MLP": "RMSprop",
            "VGG": "SGD"
        }
        return models[self.network]

    def run_neural_network(self, optimizer="recommended", sets=(False,0)):
        if optimizer == "recommended":
            optimizer = self.recommended_optimizer()
        multpl_sets,sets = sets
        if multpl_sets:
            if sets < 1:
                sys.stdout.write("Error: Trying to run multiple sets with low value: %s\n" % sets)
                sys.exit(1)
            sys.stdout.write("Running multiple sets\n")
            # HACK: this is just terrible
            while sets != 0:
                sys.stdout.write("Running %s on set %s with optimizer %s\n" % (self.network, self.set, optimizer))
                cnn = CNN(set=self.set, network_type=self.network, optimizer=optimizer)
                cnn.start()
                sets -= 1
                self.set += 1
        else:
            sys.stdout.write("Running %s on set %s with optimizer %s\n" % (self.network, self.set, optimizer))
            cnn = CNN(set=self.set, network_type=self.network, optimizer=optimizer)
            cnn.start()


def main():
    args = None
    Trainer("CIFAR10",1).run_neural_network("recommended")



if __name__ == '__main__':
    main()
