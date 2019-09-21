import numpy as np
import util.aux_funcs as aux
import game.Yamb as yamb


class NeuralNetwork:

    def __init__(self, hidden_neurons, bias_list=None, weight_list=None):
        """
        neuron_list = [15, 10 5] means nn has 3 layers; 15 neurons for input, 10 hidden, 5 output

        INPUT NEURONS (Hard coded!!!):
            input neurons accept values that correspond to 6(columns) times 13(rows) fields, each carrying 2 information
            6 values of rolled dices
            1 value of number of throws in current turn
            78*2+6+1 = 163 input neurons
            neuron_list[0] = 163

        HIDDEN NEURONS:
            Atm only 1 hidden layer
            num of neurons passed as parameter, default value to be discovered
            neuron_list[1]

        OUTPUT NEURONS (Hard coded!!!):
            1st neuron indicates decision - roll again (0) or write result (1)
                if rolling again,
                    next 6 neurons represent bit vector of rolling dices
                    next 2 neurons does not matter
                if writing result,
                    next 4 bits represent binary value of column index - range from 0 to 5, others invoke invalid_action
                    next 4 bits represent binary value of row index
            9 output neurons
            neuron_list[2] = 9

        Fitness is avg value of game score over lifetime
        """
        self.game = None
        self.neuron_list = [163, hidden_neurons, 9]
        self.layer_num = len(self.neuron_list)
        self.score_sum = 0
        self.fitness = 0
        self.games_played = 0
        if bias_list is not None and weight_list is not None:
            self.bias_list = bias_list
            self.weight_list = weight_list
        else:
            self.biases = [np.random.randn(y, 1) for y in self.neuron_list[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(self.neuron_list[:-1], self.neuron_list[1:])]

    def feed_forward(self, input):
        if len(input) != self.neuron_list[0]:
            print("Unexpected error, found", len(input), "items feeding nn, expected 163")

        for bias, weight in zip(self.bias_list, self.weight_list):
            # TEST if sigmoid is applied to every element in np matrix
            input = aux.sigmoid(np.dot(weight, input) + bias)
        output = self.decode_output(input)
        return output

    def decode_output(self, raw_nn_output):
        # raw_nn_output is np matrix, should be flattened to list
        flattened = raw_nn_output.tolist()  # double list
        output = flattened[0]  # list of output values
        if len(output) != 9:
            print("Output of nn is", len(raw_nn_output), "expected 9")
        if output[0] < 0.5:
            # roll again
            dices_set = set()
            for i in range(1, 7):
                if output[i] > 0.5:  # dice that should be rolled
                    dices_set.add(i)
            ret = [0, dices_set]
        else:
            # TODO convert binary values to indexes
            pass
        return ret

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

    def new_game(self):
        table = [yamb.Column(i) for i in range(6)]
        self.game = yamb.Yamb(table)

    def play_game(self):
        self.new_game()
        while not self.game.is_done:
            self.game.roll_dices()
            self.game.make_decision(self.feed_forward(self.prepare_input()))
            # TODO continue work
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
        """
        # TEST if ret does not contain lists
        ret = self.game.get_all_fields()
        ret.append(self.game.get_dices())
        ret.append(self.game.get_throws())
        return ret

    def evaluate_fitness(self):
        self.score_sum += self.game.get_table_sum()
        self.fitness = float(self.score_sum)/self.games_played
        return self.fitness
