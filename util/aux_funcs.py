import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def calc_val(dices, i, throws):
    if 0 <= i <= 5:
        sum = 0
        for dice in dices:
            sum = sum+dice.get_val() if dice.get_val() == i + 1 else sum
        return sum
    elif i == 6 or i == 7:
        sum = 0
        for dice in dices:
            sum = dice.get_val()
        return sum
    elif i == 8:
        if has_straight(dices):
            if throws == 1:
                return 66
            if throws == 2:
                return 56
            if throws == 3:
                return 46
        else:
            return 0
    elif i == 9:
        return get_three(dices)
    elif i == 10:
        return get_full(dices)
    elif i == 11:
        return get_four(dices)
    elif i == 12:
        return get_yamb(dices)
    else:
        print("Unexpected error! Row index is", i, "expected values range from 0 to 12")


def has_straight(dices):
    found = {
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False
    }
    for dice in dices:
        found.update({dice.get_val(): True})
    if not found[1] and found[2] and found[3] and found[4] and found[5] and found[6] or found[1] and found[2] and found[
        3] and found[4] and found[5] and not found[6]:
        return True
    else:
        return False


def get_three(dices):
    found = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for dice in dices:
        found.update({dice.get_val(): found[dice.get_val()]+1})
    for i in reversed(range(6)):
        if found[i + 1] >= 3:
            return 3 * (i + 1)+20
    return 0


def get_four(dices):
    found = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for dice in dices:
        found.update({dice.get_val(): found[dice.get_val()]+1})
    for i in reversed(range(6)):
        if found[i + 1] >= 4:
            return 4 * (i + 1)+40
    return 0


def get_yamb(dices):
    found = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for dice in dices:
        found.update({dice.get_val(): found[dice.get_val()]+1})
    for i in reversed(range(6)):
        if found[i + 1] >= 5:
            return 5 * (i + 1)+50
    return 0


def get_full(dices):
    found = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for dice in dices:
        found.update({dice.get_val(): found[dice.get_val()]+1})
    for i in reversed(range(6)):
        for j in reversed(range(i)):
            if found[j + 1] >= 3 and found[i + 1] >= 2:
                return 3 * (j + 1) + 2 * (i + 1)+30
            elif found[j + 1] >= 2 and found[i + 1] >= 3:
                return 2 * (j + 1) + 3 * (i + 1)+30
    return 0


if __name__ == '__main__':
    import game.Yamb as yamb
    dices = [yamb.Dice() for _ in range(6)]
    while True:
        for dice in dices:
            dice.roll()

        # elif get_full(dices) != 0:
            # print("Full")
        # elif get_three(dices) != 0:
            # print("Three of a kind")
        if get_yamb(dices) != 0:
            print("YAMB!!!!")
        elif get_four(dices) != 0:
            print("Four of a kind")
        # elif has_straight(dices):
        #     print("Straight")
        #     for dice in dices:
        #         print(dice.get_val())
