from xiagao_chess.board import board_to_fen, uci_square_to_detector


BOARD = [
    {"piece": "blackGeneral", "cord": {"row": 10, "col": 4}},
    {"piece": "blackSoldier", "cord": {"row": 5, "col": 3}},
    {"piece": "redElephant", "cord": {"row": 3, "col": 5}},
    {"piece": "redCannon", "cord": {"row": 3, "col": 7}},
    {"piece": "redAdvisor", "cord": {"row": 2, "col": 5}},
    {"piece": "blackChariot", "cord": {"row": 1, "col": 3}},
    {"piece": "redGeneral", "cord": {"row": 1, "col": 5}},
    {"piece": "redElephant", "cord": {"row": 1, "col": 7}},
]


def test_board_to_fen():
    fen, rotated = board_to_fen(BOARD, "red")
    assert not rotated
    assert fen == "3k5/9/9/9/9/2p6/9/4B1C2/4A4/2r1K1B2 w - - 0 1"


def test_uci_coordinate_mapping():
    assert uci_square_to_detector("e1", False) == {"row": 2, "col": 5}
    assert uci_square_to_detector("f0", False) == {"row": 1, "col": 6}
