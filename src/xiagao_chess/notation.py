from __future__ import annotations


PIECE_CN = {
    "redGeneral": "帅",
    "redAdvisor": "士",
    "redElephant": "相",
    "redHorse": "马",
    "redChariot": "车",
    "redCannon": "炮",
    "redSoldier": "兵",
    "blackGeneral": "将",
    "blackAdvisor": "士",
    "blackElephant": "象",
    "blackHorse": "马",
    "blackChariot": "车",
    "blackCannon": "炮",
    "blackSoldier": "卒",
}
NUM_CN = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
STRAIGHT = {
    "redGeneral",
    "redChariot",
    "redCannon",
    "redSoldier",
    "blackGeneral",
    "blackChariot",
    "blackCannon",
    "blackSoldier",
}


def move_to_notation(move: dict, side: str = "red") -> str:
    if side not in {"red", "black"}:
        raise ValueError("side 只能是 red 或 black")
    piece = move.get("piece", "")
    from_row, from_col = int(move["f"]["row"]), int(move["f"]["col"])
    to_row, to_col = int(move["t"]["row"]), int(move["t"]["col"])
    if not piece or piece not in PIECE_CN:
        return ""

    red = side == "red"
    from_label = NUM_CN[10 - from_col] if red else str(from_col)
    if from_row == to_row:
        direction = "平"
    elif red:
        direction = "进" if to_row > from_row else "退"
    else:
        direction = "进" if to_row < from_row else "退"

    if direction == "平":
        target = NUM_CN[10 - to_col] if red else str(to_col)
    elif piece in STRAIGHT:
        steps = abs(to_row - from_row)
        target = NUM_CN[steps] if red else str(steps)
    else:
        target = NUM_CN[10 - to_col] if red else str(to_col)
    return f"{PIECE_CN[piece]}{from_label}{direction}{target}"
