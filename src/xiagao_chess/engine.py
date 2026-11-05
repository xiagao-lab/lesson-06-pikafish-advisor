from __future__ import annotations

import os
import platform
import queue
import subprocess
import threading
import time
from pathlib import Path

from .board import board_to_fen, piece_at, uci_square_to_detector


class EngineError(RuntimeError):
    pass


def detect_engine(engine_root: str | Path) -> Path:
    root = Path(engine_root)
    if os.name == "nt":
        names = ("windows/pikafish.exe", "windows/pikafish-bmi2.exe")
    elif platform.system() == "Darwin":
        names = ("macos/pikafish-apple-silicon", "macos/Pikafish-MacOS-universal", "macos/pikafish")
    else:
        names = ("linux/pikafish", "linux/pikafish-bmi2", "linux/pikafish-sse41-popcnt")
    for relative in names:
        candidate = root / relative
        if candidate.is_file():
            if os.name != "nt":
                candidate.chmod(candidate.stat().st_mode | 0o111)
            return candidate
    raise FileNotFoundError(f"在 {root} 下找不到当前平台可用的 Pikafish")


class PikafishSession:
    """每次教学命令独占一个进程，避免超时后的旧输出污染下一题。"""

    def __init__(self, engine_root: str | Path, hash_mb: int = 32, threads: int = 1):
        self.root = Path(engine_root)
        self.executable = detect_engine(self.root)
        self.hash_mb = hash_mb
        self.threads = threads
        self.process: subprocess.Popen[bytes] | None = None
        self.lines: queue.Queue[str] = queue.Queue()

    def __enter__(self) -> "PikafishSession":
        try:
            self.process = subprocess.Popen(
                [str(self.executable)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self.root,
                bufsize=0,
            )
            threading.Thread(target=self._reader, daemon=True).start()
            self._send("uci")
            self._read_until("uciok", 30)
            self._send(f"setoption name Hash value {self.hash_mb}")
            self._send(f"setoption name Threads value {self.threads}")
            self._send("isready")
            self._read_until("readyok", 30)
            return self
        except Exception:
            self.close()
            raise

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def _reader(self) -> None:
        assert self.process is not None and self.process.stdout is not None
        for raw in iter(self.process.stdout.readline, b""):
            text = raw.decode("utf-8", errors="replace").strip()
            if text:
                self.lines.put(text)
        self.lines.put("")

    def _send(self, command: str) -> None:
        if self.process is None or self.process.stdin is None:
            raise EngineError("Pikafish 尚未启动")
        self.process.stdin.write((command + "\n").encode("utf-8"))
        self.process.stdin.flush()

    def _read_until(self, prefix: str, timeout: float) -> str:
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise EngineError(f"等待 {prefix} 超时")
            try:
                line = self.lines.get(timeout=remaining)
            except queue.Empty as error:
                raise EngineError(f"等待 {prefix} 超时") from error
            if not line:
                raise EngineError("Pikafish 意外退出")
            if line.startswith(prefix):
                return line

    def bestmove(self, fen: str, movetime_ms: int = 1000) -> str | None:
        self._send(f"position fen {fen}")
        self._send(f"go movetime {movetime_ms}")
        line = self._read_until("bestmove", movetime_ms / 1000 + 10)
        parts = line.split()
        if len(parts) < 2 or parts[1] in {"none", "(none)", "0000"}:
            return None
        if len(parts[1]) != 4:
            raise EngineError(f"无法解析引擎输出: {line}")
        return parts[1]

    def close(self) -> None:
        if self.process is None:
            return
        try:
            if self.process.poll() is None:
                self._send("quit")
                self.process.wait(timeout=2)
        except Exception:
            self.process.kill()
            self.process.wait(timeout=2)
        finally:
            self.process = None


def advise(
    board: list[dict],
    engine_root: str | Path,
    side: str = "red",
    movetime_ms: int = 1000,
) -> dict:
    fen, rotated = board_to_fen(board, side)
    with PikafishSession(engine_root) as engine:
        uci = engine.bestmove(fen, movetime_ms)
    if uci is None:
        return {"status": "no_legal_move", "fen": fen, "uci": None, "move": None}
    start = uci_square_to_detector(uci[:2], rotated)
    end = uci_square_to_detector(uci[2:], rotated)
    move = {"piece": piece_at(board, start), "f": start, "t": end}
    return {"status": "ok", "fen": fen, "uci": uci, "move": move}
