from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("exercise06", HERE / "starter.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def main() -> int:
    assert module.parse_bestmove("bestmove e2c0") == "e2c0"
    assert module.parse_bestmove("bestmove (none)") is None
    assert module.parse_bestmove("bestmove 0000") is None
    assert module.uci_square_to_detector("e2") == {"row": 3, "col": 5}
    assert module.uci_square_to_detector("c0") == {"row": 1, "col": 3}
    assert module.uci_square_to_detector("e2", rotated=True) == {"row": 8, "col": 5}
    print("练习 06 通过：UCI bestmove 与项目坐标已经正确衔接。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
