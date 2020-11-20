from game_controller import GameController


GAMESIZE = {
    'c': 7,
    'r': 6
}
DIAM = 100


def test_constructor():
    # test the constructor
    gc = GameController(GAMESIZE, DIAM)
    assert gc.is_player_turn is True and \
        gc.countdown == 30


def test_stopcheck():
    # test if a disk will falls to the bottom
    gc = GameController(GAMESIZE, DIAM)
    assert gc.stopcheck(0, gc.grids.table) == 6


def test_switch():
    # test if player turn changes after switching
    gc = GameController(GAMESIZE, DIAM)
    gc.switch()
    assert gc.is_player_turn is False
