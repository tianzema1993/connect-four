# Course: CS5001
# Laboratory: Hw12
# Username: tma64
# Author: Tianze Ma
# Date: 03/30/2020
# Description: This program creates a 6 x 7 connect_4 game
from game_controller import GameController

# the number of rows and columns within the game
GAMESIZE = {'r': 6, 'c': 7}
# the diameter of the disk, also the length of each grid
DIAM = 100
game_controller = GameController(GAMESIZE, DIAM)


def setup():
    size(GAMESIZE['c'] * DIAM, (GAMESIZE['r']+1) * DIAM)
    answer = input('enter your name')
    if answer:
        print('hi ' + answer)
        game_controller.player_name = answer
    elif answer == '':
        print('[empty string]')
    else:
        print(answer)  # Canceled dialog will print None


def input(self, message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)


def draw():
    background(180)
    game_controller.update()
    if game_controller.is_player_turn is False:
        # let the computer think a little time
        game_controller.countdown -= 1
        if game_controller.countdown == 0:
            game_controller.computermove()


# all mouse related function can only be performed in player turn
def mousePressed():
    if game_controller.is_player_turn and \
            game_controller.game_is_over is False:
        game_controller.press()


def mouseDragged():
    if game_controller.is_player_turn and \
            game_controller.game_is_over is False:
        game_controller.drag()


def mouseReleased():
    if game_controller.is_player_turn and \
            game_controller.game_is_over is False:
        game_controller.release()
