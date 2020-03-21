"""
Filename: main.py
Author: D.C
Purpose: Main file for the *insert game name* game.
"""

from time import sleep
import random
import pygame
import pygame_functions

TYPES_ENUM = {'rock': 0, 'paper': 1, 'scissor': 2}

SCREEN_SIZE_X = 1280
SCREEN_SIZE_Y = 720



class Card:
    def __init__(self, card_sprite, card_type, card_factor):
        """
        Initiate a card object.
        :param card_sprite: The path to the image file of the card. (str)
        :param card_type: The type of the card, rock, paper, scissor. (str)
        :param card_factor: The "level" of the card, between 1 and 20. (int)
        """

        self.card_sprite = card_sprite
        self.card_type = card_type
        self.card_factor = card_factor


def init_cards():
    """
    Initiate all the card objects.
    :return: A tuple containing all the cards in the enum order.
    """

    rock_types = {1: 'rock.png', 2: 'rock.png', 3: 'rock.png', 4: 'rock.png', 5: 'rock.png', 6: 'the_rock.png'}
    paper_types = {1: 'rock.png', 2: 'rock.png', 3: 'rock.png', 4: 'rock.png', 5: 'rock.png', 6: 'toilet_paper.png'}
    scissor_types = {1: 'rock.png', 2: 'rock.png', 3: 'chainsaw.png', 4: 'rock.png', 5: 'rock.png', 6: 'chainsaw.png'}

    #Initiate the card objects according to the given lists.
    rock_cards = [Card(pygame_functions.newSprite('assets\\pictures\\cards\\' + rock_types[key])\
                        , 'rock', key) for key in rock_types]
    paper_cards = [Card(pygame_functions.newSprite('assets\\pictures\\cards\\' + paper_types[key]) \
                         , 'paper', key) for key in paper_types]
    scissor_cards = [Card(pygame_functions.newSprite('assets\\pictures\\cards\\' + scissor_types[key]) \
                           , 'scissor', key) for key in scissor_types]

    return rock_cards, paper_cards, scissor_cards


def show_cards(current_luck, cards):
    """
    Show the option cards according to the dice roll.
    :param current_luck: The current roll outcome. (int)
    :param cards: The tuple containing the card objects. (tuple)

    :return: a tuple containing the sprites of the option cards.
    """

    OPTION_CARD_Y = SCREEN_SIZE_Y - 100
    OPTION_CARD_MIDDLE_X = SCREEN_SIZE_X // 2
    OPTIONS_CARD_SPACING = SCREEN_SIZE_X // 3

    rock_card = cards[TYPES_ENUM['rock']][current_luck - 1]
    paper_card = cards[TYPES_ENUM['paper']][current_luck - 1]
    scissor_card = cards[TYPES_ENUM['scissor']][current_luck - 1]

    pygame_functions.moveSprite(rock_card.card_sprite, OPTION_CARD_MIDDLE_X - OPTIONS_CARD_SPACING, OPTION_CARD_Y)
    pygame_functions.moveSprite(paper_card.card_sprite, OPTION_CARD_MIDDLE_X, OPTION_CARD_Y)
    pygame_functions.moveSprite(scissor_card.card_sprite, OPTION_CARD_MIDDLE_X + OPTIONS_CARD_SPACING, OPTION_CARD_Y)

    pygame_functions.showSprite(rock_card.card_sprite)
    pygame_functions.showSprite(paper_card.card_sprite)
    pygame_functions.showSprite(scissor_card.card_sprite)

    return rock_card, paper_card, scissor_card


def detect_choice(option_cards):
    """
    Detect which card was clicked and make the choice.
    :param option_cards: The options for the player to choose from. (tuple)
    """

    while not pygame_functions.keyPressed('esc'):
        if pygame_functions.spriteClicked(option_cards[TYPES_ENUM['rock']].card_sprite):
            return make_choice(option_cards[TYPES_ENUM['rock']])

        elif pygame_functions.spriteClicked(option_cards[TYPES_ENUM['paper']].card_sprite):
            return make_choice(option_cards[TYPES_ENUM['paper']])

        elif pygame_functions.spriteClicked(option_cards[TYPES_ENUM['scissor']].card_sprite):
            return make_choice(option_cards[TYPES_ENUM['scissor']])


def make_choice(chosen_card):
    """
    Show the chosen card and return its details details.
    :param chosen_card: The card object that was chosen. (Card)
    :return: The stats of the card
    """

    pygame_functions.hideAll()
    pygame_functions.moveSprite(chosen_card.card_sprite, SCREEN_SIZE_X // 2, SCREEN_SIZE_Y // 2)
    pygame_functions.showSprite(chosen_card.card_sprite)

    return chosen_card.card_type, chosen_card.card_factor


def throw_dice():
    """
    Display the dice throwing animation and return the result.
    :return: The result of the dice roll. (int)
    """
    DICE_IMAGE_SIZE = 128

    dice_path = 'assets\\pictures\\dice\\dice_'
    dice_sprite = pygame_functions.newSprite(dice_path + '1.png')
    pygame_functions.moveSprite(dice_sprite, SCREEN_SIZE_X // 2, SCREEN_SIZE_Y // 2)

    # Animation of the dice roll.
    for runs in range(3):
        for index in range(1, 7):
            pygame_functions.setSpriteImage(dice_sprite, pygame_functions.loadImage(dice_path+str(index)+'.png'))
            pygame_functions.showSprite(dice_sprite)
            sleep(0.05)
    # Actually generate the cards luck.
    luck_choice = random.randrange(1, 7)

    pygame_functions.setSpriteImage(dice_sprite, pygame_functions.loadImage(dice_path+str(luck_choice)+'.png'))
    pygame_functions.showSprite(dice_sprite)

    sleep(2)
    # Move the dice to the side.
    pygame_functions.moveSprite(dice_sprite, SCREEN_SIZE_X - (DICE_IMAGE_SIZE // 2), SCREEN_SIZE_Y // 2)

    return luck_choice


def main():

    pygame_functions.screenSize(SCREEN_SIZE_X, SCREEN_SIZE_Y, fullscreen=False)
    pygame_functions.setBackgroundColour('black')

    current_luck = throw_dice()

    cards = init_cards()

    card_sprites = show_cards(current_luck, cards)
    print(detect_choice(card_sprites))

    pygame_functions.endWait()


if __name__ == '__main__':
    main()

