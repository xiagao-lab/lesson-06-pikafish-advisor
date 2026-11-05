from __future__ import annotations

import argparse
import json
from pathlib import Path

from xiagao_chess.engine import advise
from xiagao_chess.image_io import save_json
from xiagao_chess.notation import move_to_notation


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="第 6 课：FEN、Pikafish 与中文记谱")
    parser.add_argument("--board", type=Path, required=True, help="第 5 课输出的 board.json")
    parser.add_argument("--side", choices=("red", "black"), default="red")
    parser.add_argument("--engine-root", type=Path, default=ROOT / "engines/pikafish")
    parser.add_argument("--movetime", type=int, default=1000, help="引擎思考毫秒数")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/lesson06")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    board = json.loads(args.board.read_text(encoding="utf-8"))
    result = advise(board, args.engine_root, args.side, args.movetime)
    if result["move"]:
        result["notation"] = move_to_notation(result["move"], args.side)
    else:
        result["notation"] = ""
    args.output.mkdir(parents=True, exist_ok=True)
    save_json(args.output / "advice.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"输出目录: {args.output}")
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
