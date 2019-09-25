import random as random
import util.aux_funcs as aux


class Dice:
    """
    Dice should always be rollable
    """
    def __init__(self):
        self.val = random.randint(1, 6)
        # self.rollable = True

    def get_val(self):
        return self.val

    def roll(self):
        self.val = random.randint(1, 6)


class Field:

    def __init__(self):
        self.unlocked = False
        self.val = None

    def unlock(self):
        self.unlocked = True

    def lock(self):
        self.unlocked = False

    def is_unlocked(self):
        return self.unlocked

    def get_val(self):
        if self.val is None:
            return 0
        else:
            return self.val

    def write(self, val):
        self.val = val
        self.lock()


class Column:
    """
    Notice: upper section is calculated with 6 dices !!!
    Column contains list of fields and proprietary methods
    """
    def __init__(self, type):
        self.fields = [Field() for _ in range(13)]
        self.type = type
        if type == 0:  # top2bottom
            self.fields[0].unlock()
        elif type == 1:  # free
            for field in self.fields:
                field.unlock()
        elif type == 2:  # bottom2top
            self.fields[12].unlock()
        elif type == 3:  # first throw only
            for field in self.fields:
                field.unlock()
        elif type == 4:  # top and bottom
            self.fields[0].unlock()
            self.fields[12].unlock()
        elif type == 5:  # middle
            self.fields[6].unlock()
            self.fields[7].unlock()
        else:
            print("Unsupported type")

    def unlock_next_field(self, index):
        if self.type == 0 and index != 12:
            self.fields[index + 1].unlock()
        #  type == 1 is unlocked by default
        if self.type == 2 and index != 0:
            self.fields[index - 1].unlock()
        #  type == 3 is unlocked only on 1st throw
        if self.type == 4:
            # unlocking only fields that are locked and empty and in range
            if index + 1 < 12 and not self.fields[index + 1].is_unlocked() and self.fields[index + 1].get_val() is None:
                self.fields[index + 1].unlock()
            if index - 1 > 0 and not self.fields[index - 1].is_unlocked() and self.fields[index - 1].get_val() is None:
                self.fields[index - 1].unlock()
        if self.type == 5:
            # if index is in upper section, unlock only upper field
            if index <= 6 and index != 0:
                self.fields[index - 1].unlock()
            # analog for lower section
            if index >= 7 and index != 12:
                self.fields[index + 1].unlock()

    def write_result(self, index, dices, throws):
        """
        :returns True if writing is successful
        """
        if 0 <= index <= 12:
            if self.fields[index].is_unlocked():  # nested ifs just to be sure "self.fields[index]" indexing is valid
                self.fields[index].write(aux.calc_val(dices, index, throws))
                self.unlock_next_field(index)
                return True
        self.write_first(dices, throws)

    def write_first(self, dices, throws):
        for index in range(len(self.fields)):
            if self.fields[index].is_unlocked():
                self.fields[index].write(aux.calc_val(dices, index, throws))
                self.unlock_next_field(index)
                return True
        return False


class Yamb:

    def __init__(self, table=None):
        #  table is list of columns
        self.table = table
        self.dices = [Dice() for _ in range(6)]
        self.throws = 0
        self.done = False
        self.fields_filled = 0

    def is_done(self):
        return self.done

    def get_throws(self):
        return aux.sigmoid(self.throws)

    def get_all_fields(self):
        ret = []
        for column in self.table:
            for field in column.fields:
                ret.append(aux.sigmoid(field.get_val()))
                if field.is_unlocked():
                    ret.append(1)
                else:
                    ret.append(0)
        return ret

    def get_dices(self):
        ret = []
        for dice in self.dices:
            ret.append(aux.sigmoid(dice.get_val()))
        return ret

    def roll_dices(self, dice_index=None):
        """
        by default rolls all 6 dices
        :param  dice_index: set that indicates which dices to roll,
                since user can't roll same dice multiple times in one turn
        """
        if dice_index is None:
            for dice in self.dices:
                dice.roll()
        else:
            for index in dice_index:
                if 0 <= index <= 5:
                    self.dices[index].roll()
                else:
                    self.invalid_action()
        self.throws += 1

    # def keep_dices(self, dice_index):
    #     for index in dice_index:
    #         if 1 <= index <= 6 and self.throws < 2:
    #             self.dices[index].save()
    #         else:
    #             self.invalid_action()

    def invalid_action(self):
        wrote = False
        for column in self.table:
            if column.write_first(self.dices, self.throws):
                wrote = True
                break
        if not wrote:  # table is full, game is done
            self.done = True
        self.throws = 0

    def make_decision(self, decoded):
        """
        Next action depends on output of NN which means
        next invoked function(and their parameters) depends on decoded value
        decoded = [0, dice index] or
        decoded = [1, column index, row index]
        """
        if self.throws <= 3:
            if decoded[0] == 0:
                self.roll_dices(decoded[1])
                return False
            else:
                self.write_result(decoded[1], decoded[2])
                return True
        else:
            self.invalid_action()
            return True

    def write_result(self, column_index, field_index):

        self.throws = 0
        if 0 <= column_index <= 5:
            self.table[column_index].write_result(field_index, self.dices, self.throws)
        else:
            self.invalid_action()

    def get_table_sum(self):
        """
        if upper section has more than 60 points, current column gets bonus 30 points
        """
        if self.done:
            sum1 = 0
            sum2 = 0
            sum3 = 0
            for column in self.table:
                upper_sum = 0
                for index in range(6):  # upper section
                    upper_sum += column.fields[index].get_val()
                if upper_sum > 60:  # upper sum is necessary because of bonus, both are tied to current column
                    sum1 += upper_sum + 30
                else:
                    sum1 += upper_sum
                sum2 += column.fields[0].get_val()*(column.fields[6].get_val() - column.fields[7].get_val()) # ones*(max-min)
                for index in range(8, 13):  # lower section
                    sum3 += column.fields[index].get_val()
            if sum2 < 0:
                sum2 = 0
            return sum1+sum2+sum3
        else:
            print("summing table while game is still playing")
            return 0

    def print_table(self):
        print("top2bot\t", "free\t", "bot2top\t", "first-only\t", "top&bot\t", "middle\t")
        for i in range(13):
            if i == 6 or i == 8:
                print("\n")
            print(self.table[0].fields[i].get_val(), "\t\t",
                  self.table[1].fields[i].get_val(), "\t\t",
                  self.table[2].fields[i].get_val(), "\t\t\t",
                  self.table[3].fields[i].get_val(), "\t\t\t",
                  self.table[4].fields[i].get_val(), "\t\t\t",
                  self.table[5].fields[i].get_val()
                  )
