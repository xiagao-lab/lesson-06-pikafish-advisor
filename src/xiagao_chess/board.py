from __future__ import annotations


FEN_CHAR = {
    "redGeneral": "K",
    "redAdvisor": "A",
    "redElephant": "B",
    "redHorse": "N",
    "redChariot": "R",
    "redCannon": "C",
    "redSoldier": "P",
    "blackGeneral": "k",
    "blackAdvisor": "a",
    "blackElephant": "b",
    "blackHorse": "n",
    "blackChariot": "r",
    "blackCannon": "c",
    "blackSoldier": "p",
}


def board_to_fen(board: list[dict], side: str = "red") -> tuple[str, bool]:
    """detector 坐标转 FEN；返回 (fen, 是否把输入旋转了 180°)。"""
    if side not in {"red", "black"}:
        raise ValueError("side 只能是 red 或 black")
    red_general_row = next(
        (
            int(item["cord"]["row"])
            for item in board
            if item.get("piece") == "redGeneral"
        ),
        0,
    )
    rotated = red_general_row > 5
    grid = [["" for _ in range(10)] for _ in range(11)]
    for item in board:
        char = FEN_CHAR.get(item.get("piece", ""))
        if not char:
            continue
        row = int(item["cord"]["row"])
        col = int(item["cord"]["col"])
        if rotated:
            row, col = 11 - row, 10 - col
        if not (1 <= row <= 10 and 1 <= col <= 9):
            raise ValueError(f"棋子坐标越界: {item}")
        if grid[row][col]:
            raise ValueError(f"同一坐标存在多个棋子: row={row}, col={col}")
        grid[row][col] = char

    ranks: list[str] = []
    for row in range(10, 0, -1):
        empty = 0
        rank = ""
        for col in range(1, 10):
            char = grid[row][col]
            if char:
                if empty:
                    rank += str(empty)
                    empty = 0
                rank += char
            else:
                empty += 1
        if empty:
            rank += str(empty)
        ranks.append(rank)
    active = "w" if side == "red" else "b"
    return f"{'/'.join(ranks)} {active} - - 0 1", rotated


def uci_square_to_detector(square: str, rotated: bool) -> dict[str, int]:
    if len(square) != 2 or square[0] < "a" or square[0] > "i" or not square[1].isdigit():
        raise ValueError(f"非法 UCI 坐标: {square}")
    col = ord(square[0]) - ord("a") + 1
    row = int(square[1]) + 1
    if rotated:
        row, col = 11 - row, 10 - col
    return {"row": row, "col": col}


def piece_at(board: list[dict], coordinate: dict[str, int]) -> str:
    for item in board:
        if item.get("cord") == coordinate:
            return str(item.get("piece", ""))
    return ""
