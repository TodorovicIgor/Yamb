import numpy as np
from random import uniform, random
import util.aux_funcs as aux
import game.Yamb as yamb
from threading import Thread


class NeuralNetwork(Thread):

    def __init__(self, hidden_neurons, iterations,bias_list=None, weight_list=None):
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
                    next 4 bits represent binary value of row index - range from 0 to 12, others invoke invalid_action
            9 output neurons
            neuron_list[2] = 9

        Fitness is avg value of game score over lifetime
        """
        self.game = None
        self.iterations = iterations
        self.neuron_list = [163, hidden_neurons, 9]
        self.layer_num = len(self.neuron_list)
        self.score_sum = 0
        self.fitness = 0
        self.games_played = 0
        if bias_list is not None and weight_list is not None:
            self.bias_list = bias_list
            self.weight_list = weight_list
            self.age = 0
        else:
            self.bias_list = [np.random.randn(y, 1) for y in self.neuron_list[1:]]
            self.weight_list = [np.random.randn(y, x) for x, y in zip(self.neuron_list[:-1], self.neuron_list[1:])]
            self.age = -1

    def feed_forward(self, input):
        input = np.reshape(input, (163, 1)) # reshaping array to matrix for dot product
        if len(input) != self.neuron_list[0]:
            print("Unexpected error, found", len(input), "items feeding nn, expected 163")
        for bias, weight in zip(self.bias_list, self.weight_list):
            input = aux.sigmoid(np.dot(weight, input) + bias)
        output = self.decode_output(input)
        return output

    def decode_output(self, raw_nn_output):
        output = np.ndarray.flatten(raw_nn_output)
        if len(output) != 9:
            print("Output of nn is", len(raw_nn_output), "expected 9")
        if output[0] < 0.5:
            # roll again
            dices_set = set()
            for i in range(1, 7):
                if output[i] > 0.5:  # dice that should be rolled
                    dices_set.add(i-1)
            ret = [0, dices_set]
        else:
            column_index = 0
            row_index = 0
            if output[1] > 0.5: column_index += 8
            if output[2] > 0.5: column_index += 4
            if output[3] > 0.5: column_index += 2
            if output[4] > 0.5: column_index += 1
            if output[5] > 0.5: row_index += 8
            if output[6] > 0.5: row_index += 4
            if output[7] > 0.5: row_index += 2
            if output[8] > 0.5: row_index += 1
            ret = [1, column_index, row_index]
        return ret

    def set_genes(self, bias_and_weights):
        self.bias_list = bias_and_weights[0]
        self.weight_list = bias_and_weights[1]

    def get_genes(self):
        return [self.bias_list, self.weight_list]

    def mutate_genes(self):
        for i in range(len(self.weight_list)):
            for j in range(len(self.weight_list[i])):
                self.weight_list[i][j] *= uniform(0.9, 1.1)  # 10% mutation

        for i in range(len(self.bias_list)):
            for j in range(len(self.bias_list[i])):
                self.bias_list[i][j] *= uniform(0.9, 1.1)  # 10% mutation

    def reproduce_with_mutation(self):
        offspring = NeuralNetwork(self.neuron_list[1], self.iterations)
        offspring.set_genes(self.get_genes())
        offspring.mutate_genes()
        return offspring

    def reproduce_with_crossover_and_mutation(self, ind1, ind2):
        bias1 = ind1.get_genes()[0]
        bias2 = ind2.get_genes()[0]
        weight1 = ind1.get_genes()[1]
        weight2 = ind2.get_genes()[1]
        aux_bias = []
        new_bias = []
        aux_weight = []
        new_weight = []
        for row_index in range(len(bias1)):
            for elem_index in range(len(bias1[row_index])):
                if random() > 0.5:
                    aux_bias.append(bias1[row_index][elem_index])
                else:
                    aux_bias.append(bias2[row_index][elem_index])
            new_bias.append(aux_bias)
            aux_bias = []

        for row_index in range(len(weight1)):
            for elem_index in range(len(weight1[row_index])):
                if random() > 0.5:
                    aux_weight.append(weight1[row_index][elem_index])
                else:
                    aux_weight.append(weight2[row_index][elem_index])
            new_weight.append(aux_weight)
            aux_weight = []

        offspring = NeuralNetwork(self.neuron_list[1], self.iterations)
        offspring.set_genes([new_bias, new_weight])
        offspring.mutate_genes()
        return offspring

    def new_game(self):
        table = [yamb.Column(i) for i in range(6)]
        self.game = yamb.Yamb(table)

    def play_game(self, iterations=1):
        self.new_game()
        for _ in range(iterations):
            self.new_game()
            while not self.game.is_done() and self.game.fields_filled < 78:
                self.game.roll_dices()
                # while not writing result, keep making decisions
                # func game.make_decision provides maximum of 3 rolls in 1 turn
                while not self.game.make_decision(self.feed_forward(self.prepare_input())):
                    pass
                self.game.fields_filled += 1
                # either invalid action(more than 3 rolls), or premature writing
                # in both cases continue with new turn
            # game is finished
            self.game.done = True
            self.games_played += 1
            self.evaluate_fitness()

    def prepare_input(self):
        """
        :return: list of:
                    field values
                    field is_unlocked flag
                    dice values
        """
        ret = self.game.get_all_fields()
        ret.extend(self.game.get_dices())
        ret.append(self.game.get_throws())
        return ret

    def evaluate_fitness(self):
        self.score_sum += self.game.get_table_sum()
        self.fitness = float(self.score_sum) / self.games_played
        return self.fitness

    def run(self):
        self.play_game(self.iterations)


if __name__ == '__main__':
    nn1 = NeuralNetwork(500, 30)
    nn2 = NeuralNetwork(500, 30)
    new = nn1.reproduce_with_crossover_and_mutation(nn1, nn2)
    print("length of nn1 bias and weigth is", len(nn1.get_genes()[0][1]), len(nn1.get_genes()[1][1]))
    print("length of new bias and weigth is", len(new.get_genes()[0][1]), len(new.get_genes()[1][1]))
