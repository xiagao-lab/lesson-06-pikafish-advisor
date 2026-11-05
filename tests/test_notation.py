from xiagao_chess.notation import move_to_notation


def test_red_advisor_notation():
    move = {
        "piece": "redAdvisor",
        "f": {"row": 2, "col": 5},
        "t": {"row": 1, "col": 6},
    }
    assert move_to_notation(move, "red") == "士五退四"


def test_red_cannon_horizontal_notation():
    move = {
        "piece": "redCannon",
        "f": {"row": 3, "col": 8},
        "t": {"row": 3, "col": 5},
    }
    assert move_to_notation(move, "red") == "炮二平五"
