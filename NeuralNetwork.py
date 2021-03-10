import numpy as np
from scipy import special
from Constants import *


class NeuralNetwork:

    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):

        # Initialize nodes
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # Initialize learning rate
        self.lr = learningrate

        # Initialize weights
        self.wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # Set activation function
        self.activation_function = lambda x: special.expit(x)

    def train(self, input_list, target_list):

        inputs = np.array(input_list, ndmin=2).T
        targets = np.array(target_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        output_errors = targets - final_outputs
        hidden_errors = np.dot(self.who.T, output_errors)

        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), hidden_outputs.T)
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1 - hidden_outputs)), inputs.T)

    def query(self, input_list):

        inputs = np.array(input_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

    @staticmethod
    def pass_mutate(x, rate):
        probability = np.random.rand()
        if probability < rate:
            return np.random.rand()
        else:
            return x

    def mutate(self):
        # print(self.wih)
        # myfunc = np.vectorize(self.pass_mutate)
        # myfunc(self.wih, 0.4)
        # myfunc(self.who, 0.4)
        # print(self.wih)
        # self.wih[self.wih > 0.1] = np.random.rand()
        # self.who[self.wih > 0.1] = np.random.rand()

        for i in range(self.hnodes):
            for j in range(self.inodes):
                probability = np.random.rand()
                if probability < MUTATION_PROBABILITY:
                    self.wih[i][j] = np.random.normal(0, 1)

        for i in range(self.onodes):
            for j in range(self.hnodes):
                probability = np.random.rand()
                if probability < MUTATION_PROBABILITY:
                    self.who[i][j] = np.random.normal(0, 1)


pass






