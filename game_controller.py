from disk import Disk
from grid import Grid
import random
import copy


class GameController:
    def __init__(self, GAMESIZE, DIAM):
        self.GAMESIZE = GAMESIZE
        self.DIAM = DIAM
        self.disks = []
        self.grids = Grid(self.GAMESIZE, self.DIAM)
        self.is_player_turn = True
        self.game_is_over = False
        # the fakegrid used to simulate what will happen next move
        self.fakegrids = Grid(self.GAMESIZE, self.DIAM)
        # the doublefakegrid used to simulate what happen next next
        self.doublefakegrids = Grid(self.GAMESIZE, self.DIAM)
        # computer think 30 frames, then select where to put the disk
        self.countdown = 30
        # used to read player name of the game
        self.player_name = ''
        # used to store the name and him/her score
        self.score = {}

    def update(self):
        for disk in self.disks:
            if disk.active:
                disk.display()
                stop_y = self.stopcheck(disk.x//self.DIAM, self.grids.table) \
                    * self.DIAM + self.DIAM/2
                if disk.fall:
                    disk.y = disk.y + disk.rate
                if disk.y >= stop_y:
                    disk.fall = False
                    disk.land = True
                    self.grids.fillgrid(
                        disk.x // self.DIAM, disk.y // self.DIAM, disk.color
                        )
                    # switch between player and computer
                    self.switch()
        self.drawlines()
        self.checkwin()
        self.gameover()
        # if player wins, process the file work
        if self.grids.player_win:
            self.fileprocessing()

    # create the new disk anytime, but only display them in the correct
    #  location, a new one can be created only if the last one landed
    def press(self):
        x = self.DIAM * (mouseX // self.DIAM) + self.DIAM/2
        index_x = x // self.DIAM
        if len(self.disks) == 0 or (self.disks[-1].land is True
                                    and self.disks[-1].color == "YELLOW"):
            self.disks.append(Disk(x, self.DIAM/2, self.DIAM, 'RED'))
            if mouseY > self.DIAM or self.grids.table[1][index_x] != 0:
                self.disks[-1].active = False

    # A disk can only be dragged when is not falling and not landing
    def drag(self):
        if self.disks[-1].fall is False \
                and self.disks[-1].land is False:
            x = self.DIAM * (mouseX // self.DIAM) + self.DIAM/2
            index_x = x // self.DIAM
            if index_x <= self.GAMESIZE['c']-1:
                if mouseY < self.DIAM and self.grids.table[1][index_x] == 0:
                    self.disks[-1].active = True
                    self.disks[-1].x = x
                else:
                    self.disks[-1].active = False
            else:
                self.disks[-1].active = False

    # A disk can only be released when is not falling and not landing
    # If the disk is inactive when releasing, delete it
    def release(self):
        if self.disks[-1].fall is False \
                and self.disks[-1].land is False:
            if mouseX < 0:
                # if the mouse is released less than zero, the disk should be
                #  put at the leftmost column which is not full
                index = 0
                for i in range(self.GAMESIZE['c']):
                    if self.grids.table[1][i] == 0:
                        index = i
                        break
                self.disks[-1].x = index * self.DIAM + self.DIAM/2
            # if the mouse is released bigger than 700, the disk should be
            #  put at the rightmost column which is not full
            if mouseX > self.GAMESIZE['c'] * self.DIAM:
                index = self.GAMESIZE['c'] - 1
                for i in range(self.GAMESIZE['c']-1, -1, -1):
                    if self.grids.table[1][i] == 0:
                        index = i
                        break
                self.disks[-1].active = True
                self.disks[-1].x = index * self.DIAM + self.DIAM/2
            if self.disks[-1].active is True:
                self.disks[-1].fall = True
            else:
                del self.disks[-1]

    # draw the blue lines
    def drawlines(self):
        for i in range(
            self.DIAM, (self.GAMESIZE['r']+1) * self.DIAM + 1, self.DIAM
                ):
            stroke(0, 0, 255)
            strokeWeight(15)
            line(0, i, (self.GAMESIZE['r']+1) * self.DIAM, i)
        for j in range(
            0, (self.GAMESIZE['c']+1) * self.DIAM + 1, self.DIAM
                ):
            stroke(0, 0, 255)
            strokeWeight(15)
            line(j, self.DIAM, j, (self.GAMESIZE['c']+1) * self.DIAM)

    # return the y index of where the disk should stop
    # the disk should stop one grid upper than a filled grid
    def stopcheck(self, x, table):
        stop_y = self.GAMESIZE['r']
        for i in range(1, self.GAMESIZE['r']+1):
            if table[i][x] != 0:
                stop_y = i - 1
                break
        return stop_y

    # if all grids in the first row are filled, game over
    def gameover(self):
        count = 0
        for i in range(self.GAMESIZE['c']):
            if self.grids.table[1][i] == 0:
                count += 1
        if count == 0:
            self.game_is_over = True
            fill(1)
            textSize(40)
            text(
                "Game Over!!!", self.GAMESIZE['r'] * self.DIAM/2 - self.DIAM/2,
                (self.GAMESIZE['c']) * self.DIAM/2
                )

    def checkwin(self):
        if self.grids.player_win:
            self.game_is_over = True
            fill(1)
            textSize(40)
            text(
                "Player Win!!!",
                self.GAMESIZE['r'] * self.DIAM/2 - self.DIAM/2,
                (self.GAMESIZE['c']) * self.DIAM/2
                )
        if self.grids.computer_win:
            self.game_is_over = True
            fill(1)
            textSize(40)
            text(
                "Computer Win!!!",
                self.GAMESIZE['r'] * self.DIAM/2 - self.DIAM/2,
                (self.GAMESIZE['c']) * self.DIAM/2
                )

    def switch(self):
        if self.is_player_turn:
            self.is_player_turn = False
        else:
            self.is_player_turn = True

    # after the player's disk has landed and countdown 30 frames, the computer
    # starts playing
    def computermove(self):
        if self.game_is_over is False:
            # first find out the columns has not been filled
            empty_column = []
            for i in range(self.GAMESIZE['c']):
                if self.grids.table[1][i] == 0:
                    empty_column.append(i)
            # the main AI part is to find the 'x'
            index = self.ai_strategy(empty_column)
            x = index * self.DIAM + self.DIAM/2
            if self.disks[-1].land is True:
                self.disks.append(Disk(x, self.DIAM/2, self.DIAM, 'YELLOW'))
                self.disks[-1].fall = True
            # redefine the counrdown value for next move
            self.countdown = 30

    def ai_strategy(self, empty_column):
        # if computer can win this turn, do it
        # check if AI put the disk in a specific x, it will win, so do it
        # using fakegrids so anything I do here won't affect real grids
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "YELLOW")
            fakelist = self.fakegrids.ai_dir_list
            for item in fakelist:
                if item >= 4:
                    index = x
                    return index
        # if the player can win next move, try to stop him
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "RED")
            fakelist = self.fakegrids.player_dir_list
            for item in fakelist:
                if item >= 4:
                    index = x
                    return index
        # try to delete the move which can let player win next time
        # try to avoid stupid moves by deleting x
        bad_x_list = self.checkbadx(empty_column)
        if len(bad_x_list) != 0:
            if len(empty_column) > len(bad_x_list):
                for bad_x in bad_x_list:
                    empty_column.remove(bad_x)
        # if the player can connect three disks, try to stop him
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "RED")
            fakelist = self.fakegrids.player_dir_list
            for item in fakelist:
                if item == 3:
                    index = x
                    return index
        # if computer can connect three disks, do it
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "YELLOW")
            fakelist = self.fakegrids.ai_dir_list
            for item in fakelist:
                if item == 3:
                    index = x
                    return index
        # if computer can connect two disks, do it
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "YELLOW")
            fakelist = self.fakegrids.ai_dir_list
            for item in fakelist:
                if item == 2:
                    index = x
                    return index
        # if the player can connect two disks, try to stop him
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "RED")
            fakelist = self.fakegrids.player_dir_list
            for item in fakelist:
                if item == 2:
                    index = x
                    return index
        # none above, choose a random place
        index = random.choice(empty_column)
        return index

    # try to find out a list of bad 'x'
    # first fill a yellow disk, and check out if player will win after the move
    # if so, it is a stupid movement, try to avoid that
    def checkbadx(self, empty_column):
        bad_x_list = []
        for x in empty_column:
            self.fakegrids.table = copy.deepcopy(self.grids.table)
            y = self.stopcheck(x, self.fakegrids.table)
            self.fakegrids.fillgrid(x, y, "YELLOW")
            new_empty_column = []
            for i in range(self.GAMESIZE['c']):
                if self.fakegrids.table[1][i] == 0:
                    new_empty_column.append(i)
            for m in new_empty_column:
                self.doublefakegrids.table = copy.deepcopy(
                    self.fakegrids.table)
                n = self.stopcheck(m, self.doublefakegrids.table)
                self.doublefakegrids.fillgrid(m, n, "RED")
                fakelist = self.doublefakegrids.player_dir_list
                for item in fakelist:
                    if item >= 4 and item not in bad_x_list:
                        bad_x_list.append(x)
        return bad_x_list

    def fileprocessing(self):
        try:
            f = open("scores.txt", "r")
            score_lines = f.readlines()
            for line in score_lines:
                item = line.split(' ')
                # here I need pay attention to long name
                # so I add a space to all names
                if len(item) <= 2:
                    longname = item[0] + ' '
                    if longname not in self.score:
                        self.score[longname] = int(item[1])
                else:
                    # add name parts to a string
                    longname = ''
                    for i in range(len(item)-1):
                        longname += item[i]
                        longname += ' '
                    if longname not in self.score:
                        self.score[longname] = int(item[-1])
        except Exception:
            pass
        the_player_name = self.player_name + ' '
        if the_player_name not in self.score:
            self.score[the_player_name] = 1
        else:
            self.score[the_player_name] += 1
        rank = sorted(
            self.score.items(),
            key=lambda x: x[1],
            reverse=True
        )
        w = open("scores.txt", "w")
        for item in rank:
            w.write('{0}{1}\n'.format(item[0], int(item[1])))
