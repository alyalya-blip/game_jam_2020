import Metal
import random

MAX_LUCK = 100
DICE_SIZE = 20


class Player:
    def __init__(self):
        self.__luck = MAX_LUCK // 2
        self.__dice_size = DICE_SIZE
        self.actions = ["Paper", "Scissors", "Rock"]

    def dice_throw(self, luck):
        choices_array = []
        weights = []
        for index in range(self.__dice_size):
            choices_array.append(index + 1)
            weights.append(1)

        if luck != 0:
            for index in range(self.__dice_size):
                weights[index] += (luck / 100) * (index + 1)

        return random.choices(choices_array, weights=weights)

    def get_luck_max_six(self):
        return self.__luck // 20 + 1

    def set_luck(self, new_luck):
        self.__luck = new_luck


class HumanPlayer(Player):
    def __init__(self):
        Player.__init__(self)


class ComputerPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def take_action(self, enemy_player):
        pass


def main():
    p = HumanPlayer()
    Metal.screen_function(p.get_luck_max_six())


if __name__ == '__main__':
    main()
