import util.aux_funcs as aux
import game.Yamb as yamb
import numpy as np
from threading import Thread
from keras import *
from keras.layers import Dense, Activation


class CSP(Thread):

    def __init__(self, hidden_neurons, game_iterations):
        super().__init__()
        self.hidden_neurons = hidden_neurons
        table = [yamb.Column(i) for i in range(6)]
        self.best_game = yamb.Yamb(table)
        self.game = None
        self.game_iterations = game_iterations
        self.model = Sequential()

        self.model.add(Dense(hidden_neurons[0], input_shape=(163, )))
        for index in range(len(hidden_neurons)):
            self.model.add(Dense(hidden_neurons[index]))
            self.model.add(Activation('sigmoid'))
        self.model.add(Dense(9))
        self.model.add(Activation('sigmoid'))

        self.model.compile(optimizer='sgd',
                      loss='mean_squared_error',
                      metrics=['accuracy'])

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
        np.reshape(ret, (-1, 1))
        return ret

    def new_game(self):
        table = [yamb.Column(i) for i in range(6)]
        # set weights
        for column_index in range(len(table)):
            for field_index in range(len(table[column_index].fields)):
                if column_index == 0:  # top2bot
                    table[column_index].fields[field_index].set_weight(12-field_index)
                if column_index == 2:  # bot2top
                    table[column_index].fields[field_index].set_weight(field_index+1)
                if column_index == 3:  # first
                    table[column_index].fields[field_index].set_weight(2)
                if column_index == 4 and field_index < 7:  # middle upper half
                    table[column_index].fields[field_index].set_weight(12 - field_index)
                if column_index == 4 and field_index > 6:  # middle lower half
                    table[column_index].fields[field_index].set_weight(field_index+1)
                if column_index == 5 and field_index < 7:  # top&bot upper half
                    table[column_index].fields[field_index].set_weight(field_index+1)
                if column_index == 5 and field_index > 6:  # top&bot lower half
                    table[column_index].fields[field_index].set_weight(12 - field_index)
        # set max values
        for column_index in range(len(table)):
            for field_index in range(len(table[column_index].fields)):
                if 0 <= field_index <= 5:
                    table[column_index].fields[field_index].max = 5 * (field_index+1)
                elif field_index == 6:  # min
                    table[column_index].fields[field_index].ax = 5
                elif field_index == 7:  # max
                    table[column_index].fields[field_index].ax = 30
                elif field_index == 8:  # straight
                    table[column_index].fields[field_index].ax = 66
                elif field_index == 9:  # three
                    table[column_index].fields[field_index].ax = 38
                elif field_index == 10: # full
                    table[column_index].fields[field_index].ax = 58
                elif field_index == 11: # four
                    table[column_index].fields[field_index].ax = 64
                elif field_index == 12: # yamb
                    table[column_index].fields[field_index].ax = 80
        self.game = yamb.Yamb(table)

    def generate_label(self, dices, throws):
        # insert into list weighted current values and indexes
        constraints = []
        for column_index in range(len(self.game.table)):
            for field_index in range(len(self.game.table[column_index].fields)):
                if self.game.table[column_index].fields[field_index].is_unlocked():
                    # appending tuple (val, col, row)
                    constraints.append((self.game.table[column_index].fields[field_index].weight * aux.calc_val(dices, field_index, throws) - self.game.table[column_index].fields[field_index].max, column_index, field_index))

        # sort constraints asc
        constraints.sort(key=lambda x: x[0], reverse=True)

        # constraints[0] makes the most sense to play (hopefully)
        if constraints[0][0] < 0:
            # if weighted value is less than max value, roll again
            label = [0]
            for i in range(6):
                label.append(1)
            label.append(0)
            label.append(0)
        else:
            label = [1]
            # good enough, write res
            # converting to binary
            # !!!! time pressure, can't trust libraries
            mask = 8
            for _ in range(4):
                if constraints[0][1] & mask:
                    label.append(1)
                else:
                    label.append(0)
                mask = mask >> 1  # 8, 4, 2, 1
            mask = 8
            for _ in range(4):
                if constraints[0][2] & mask:
                    label.append(1)
                else:
                    label.append(0)
                mask = mask >> 1  # 8, 4, 2, 1
            if len(label) != 9:
                print("Error in converting to binary, column is", constraints[0][1], constraints[0][2], "label is", label)
        label = np.reshape(label, (1, 9))
        return label

    def train(self):
        self.new_game()
        for _ in range(self.game_iterations):
            self.new_game()
            while not self.game.is_done() and self.game.fields_filled < 78:
                self.game.roll_dices()
                data = np.array(self.prepare_input())
                data = data.reshape(1, (data.shape[0]))
                # print(self.generate_label(self.game.dices, self.game.throws))
                self.model.train_on_batch(data, self.generate_label(self.game.dices, self.game.throws))
                # while not self.game.make_decision(self.decode_output(self.model.layers[-1:].output)):
                while not self.game.make_decision(self.decode_output(self.generate_label(self.game.dices, self.game.throws))):
                    pass
                # wrote
                self.game.fields_filled += 1
            self.game.done = True
            # game is finished
            print("score is", self.game.get_table_sum())
            if self.game.get_table_sum() > self.best_game.get_table_sum():
                self.best_game = self.game
            self.game.print_table()
            self.new_game()

    def run(self):
        self.train()


if __name__ == '__main__':
    # hidden_neurons, game_iterations
    csp = CSP([500, 200, 100], 50)
    csp.train()
