class Grid:
    def __init__(self, GAMESIZE, DIAM):
        self.GAMESIZE = GAMESIZE
        self.m = self.GAMESIZE['c']
        self.n = self.GAMESIZE['r'] + 1
        self.table = [[0] * self.m for i in range(self.n)]
        self.player_win = False
        self.computer_win = False
        self.player_dir_list = []
        self.ai_dir_list = []

    # fill the grid with the color_value, check four direction everytime
    # and check if there is a winner
    def fillgrid(self, x, y, color):
        if color == 'RED':
            self.table[y][x] = 1
            self.dir_check(x, y, 1)
            self.checkwin(1)
        elif color == 'YELLOW':
            self.table[y][x] = -1
            self.dir_check(x, y, -1)
            self.checkwin(-1)

    # check four directions based on input color value, fill the corresponding
    #  list, the list shows the maximum connected disks in each direction
    def dir_check(self, x, y, color_value):
        if color_value == 1:
            self.player_dir_list = []
            self.player_dir_list.append(
                self.check_vertical(x, y, color_value))
            self.player_dir_list.append(
                self.check_horizontal(x, y, color_value))
            self.player_dir_list.append(
                self.check_diagonal_1(x, y, color_value))
            self.player_dir_list.append(
                self.check_diagonal_2(x, y, color_value))
            return self.player_dir_list
        if color_value == -1:
            self.ai_dir_list = []
            self.ai_dir_list.append(
                self.check_horizontal(x, y, color_value))
            self.ai_dir_list.append(
                self.check_vertical(x, y, color_value))
            self.ai_dir_list.append(
                self.check_diagonal_1(x, y, color_value))
            self.ai_dir_list.append(
                self.check_diagonal_2(x, y, color_value))
            return self.ai_dir_list

    def check_vertical(self, x, y, color_value):
        count = 0
        max_count = 0
        for i in range(1, self.GAMESIZE['r']+1):
            if self.table[i][x] == color_value:
                count += 1
            else:
                count = 0
            if count > max_count:
                max_count = count
        return max_count

    def check_horizontal(self, x, y, color_value):
        count = 0
        max_count = 0
        for i in range(0, self.GAMESIZE['c']):
            if self.table[y][i] == color_value:
                count += 1
            else:
                count = 0
            if count > max_count:
                max_count = count
        return max_count

    # left bottom to right top
    def check_diagonal_1(self, x, y, color_value):
        count = 0
        max_count = 0
        # x + y less or equal to 6, start from x = 0, y = y+x
        if x + y <= self.GAMESIZE['r']:
            for i in range(x+y, 0, -1):
                if self.table[i][x+y-i] == color_value:
                    count += 1
                else:
                    count = 0
                if count > max_count:
                    max_count = count
            return max_count
        # x + y greater than 6, start from y = 6, x = x+y - 6
        if x + y > self.GAMESIZE['r']:
            for i in range(
                    self.GAMESIZE['r'], x+y-(self.GAMESIZE['c']-1)-1, -1):
                if self.table[i][x+y-i] == color_value:
                    count += 1
                else:
                    count = 0
                if count > max_count:
                    max_count = count
            return max_count

    # left top to right bottom
    def check_diagonal_2(self, x, y, color_value):
        count = 0
        max_count = 0
        # y - x >= 1, start from x = 0, y = y-x
        if y - x >= 1:
            for i in range(y-x, self.GAMESIZE['r']+1):
                if self.table[i][i-y+x] == color_value:
                    count += 1
                else:
                    count = 0
                if count > max_count:
                    max_count = count
            return max_count
        # y - x < 1, start from y = 1, x = x - (y-1)
        if y - x < 1:
            for i in range(1, self.GAMESIZE['c']-1-(x-y)+1):
                if self.table[i][i+x-y] == color_value:
                    count += 1
                else:
                    count = 0
                if count > max_count:
                    max_count = count
            return max_count

    # if any direction has equal or more than 4 connect disks, winner shows up!
    def checkwin(self, color_value):
        if color_value == 1:
            for item in self.player_dir_list:
                if item >= 4:
                    self.player_win = True
                    return
        if color_value == -1:
            for item in self.ai_dir_list:
                if item >= 4:
                    self.computer_win = True
                    return
