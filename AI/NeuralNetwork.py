import numpy as np
import util.aux_funcs as aux
import game.Yamb as yamb


class NeuralNetwork:

    def __init__(self, neuron_list, bias_list=None, weight_list=None):
        """
        neuron_list = [15, 10 5]
        3 layers; input has 15 neurons, hidden 10, output 5
        """
        self.game = None
        self.layer_num = len(neuron_list)
        self.neuron_list = neuron_list
        self.score = 0
        if bias_list is not None and weight_list is not None:
            self.bias_list = bias_list
            self.weight_list = weight_list
        else:
            self.biases = [np.random.randn(y, 1) for y in neuron_list[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(neuron_list[:-1], neuron_list[1:])]

    def feed_forward(self, input):
        output = None
        for bias, weight in zip(self.bias_list, self.weight_list):
            input = aux.sigmoid(np.dot(weight, input) + bias)
            output = self.decode_output(input)
            # TODO continue work
        return output

    def decode_output(self, input):
        # TODO design decoding
        return input

    def set_genes(self, *bias_and_weights):
        self.bias_list, self.weight_list = bias_and_weights

    def get_genes(self):
        return self.bias_list, self.weight_list

    def mutate_genes(self):
        """
        for every bias and weight
            chance to mutate, chance initialy large, reducing with "time"
        """

    def reproduce_with_mutation(self):
        offspring = NeuralNetwork(self.neuron_list)
        offspring.set_genes(self.get_genes())
        offspring.mutate_genes()
        return offspring

    def play_game(self):
        table = [yamb.Column(i) for i in range(6)]
        self.game = yamb.Yamb(table)
        while not self.game.is_done:
            self.game.roll_dices()
            self.game.make_decision(self.feed_forward(self.prepare_input()))
        #  TODO
        #   some sort of flag to indicate if turn is ending prematurely
        #   if it is, continue to next iteration
        #   if not, 3 more dice rolling

    def prepare_input(self):
        """
        :return: list of:
                    field values
                    field is_unlocked flag
                    dice values
                    number of throws in current turn
        """
        # TODO ****************** TEST IF ret LIST CONTAINS ONLY INTEGERS
        ret = self.game.get_all_fields()
        ret.append(self.game.get_dices())
        ret.append(self.game.get_throws())
        return ret

    def evaluate_fitness(self):
        self.score = self.game.get_table_sum()
