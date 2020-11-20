from grid import Grid

GAMESIZE = {
    'c': 7,
    'r': 6
}
DIAM = 100


def test_constructor():
    the_grid = Grid(GAMESIZE, DIAM)
    # test the size of table, the initial content of the table
    assert len(the_grid.table) == 7 and \
        the_grid.table[0][0] == 0 and \
        the_grid.player_win is False


def test_fillgrid():
    the_grid = Grid(GAMESIZE, DIAM)
    the_grid.fillgrid(1, 2, "RED")
    # after fill the grid with a color, check if the value changes
    assert the_grid.table[2][1] == 1


def test_dir_check():
    the_grid = Grid(GAMESIZE, DIAM)
    # fill the grids, check if the number of maximum connected disks is correct
    the_grid.fillgrid(1, 1, "RED")
    the_grid.fillgrid(1, 2, "RED")
    the_grid.fillgrid(1, 3, "RED")
    the_grid.fillgrid(2, 2, "RED")
    the_grid.fillgrid(3, 3, "RED")
    the_grid.fillgrid(4, 4, "RED")
    the_grid.fillgrid(0, 5, "YELLOW")
    the_grid.fillgrid(1, 5, "YELLOW")
    the_grid.fillgrid(2, 5, "YELLOW")
    the_grid.fillgrid(3, 5, "YELLOW")
    the_grid.fillgrid(4, 5, "YELLOW")
    assert the_grid.check_vertical(1, 1, 1) == 3 and \
        the_grid.check_horizontal(0, 5, -1) == 5 and \
        the_grid.check_diagonal_2(1, 1, 1) == 4 and \
        the_grid.check_diagonal_1(1, 3, 1) == 2


def test_checkwin():
    the_grid = Grid(GAMESIZE, DIAM)
    # fill the grids, check if there is a winner
    the_grid.fillgrid(0, 5, "YELLOW")
    the_grid.fillgrid(1, 5, "YELLOW")
    the_grid.fillgrid(2, 5, "YELLOW")
    the_grid.fillgrid(3, 5, "YELLOW")
    the_grid.fillgrid(4, 5, "YELLOW")
    the_grid.fillgrid(1, 1, "RED")
    the_grid.fillgrid(1, 2, "RED")
    assert the_grid.player_win is False and \
        the_grid.computer_win is True
