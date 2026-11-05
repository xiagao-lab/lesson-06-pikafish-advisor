from __future__ import annotations


def parse_bestmove(line: str) -> str | None:
    """解析 `bestmove e2c0`；无合法着法时返回 None。"""
    raise NotImplementedError("TODO: 校验前缀、长度，并处理 none/(none)/0000")


def uci_square_to_detector(square: str, rotated: bool = False) -> dict[str, int]:
    """把 a0..i9 映射到 row=1..10、col=1..9；必要时旋转 180°。"""
    raise NotImplementedError("TODO: 字母转列、数字转行，再处理 rotated")
