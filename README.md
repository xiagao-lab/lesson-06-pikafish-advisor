# 虾搞象棋第 6 课：Pikafish 选步

本课只解决一件事：把棋子位置表变成一步合法的走法建议和中文棋谱。

```text
board.json → FEN → Pikafish 合法着法与搜索 → bestmove → 项目坐标 → 中文棋谱
```

当前链路没有大模型点评。大模型可以解释或说段子，但不负责保证走法合法，也不参与本课的推荐结果。

## 准备 Pikafish

从 Pikafish 官方项目下载与你的操作系统匹配的引擎和所需网络文件：

- <https://github.com/official-pikafish/Pikafish>

按下面的结构放置，二进制和网络文件不要提交到 Git：

```text
engines/pikafish/
├── macos/pikafish-apple-silicon
├── linux/pikafish
├── windows/pikafish.exe
└── pikafish.nnue
```

实际只需保留当前平台对应的一个可执行文件；文件名也可以使用 `engine.py` 中列出的兼容名称。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python lesson/run.py --board /path/to/board.json --side red --movetime 1000
```

输出 `outputs/lesson06/advice.json`，包括：

- 发送给引擎的 FEN。
- Pikafish 返回的四字符 UCI 走法。
- 项目的起点、终点和棋子名称。
- 中文棋谱，例如“相五退七”。

引擎如何从候选中筛掉非法走法、再搜索最佳走法，见 [docs/ENGINE_FLOW.md](docs/ENGINE_FLOW.md)。

## 课后练习

仓库不提供标准答案。完成 `exercises/starter.py` 后运行：

```bash
python exercises/check.py
```

需要 AI 陪练时使用 [exercises/AI_PRACTICE.md](exercises/AI_PRACTICE.md)。

## 课程材料

- `courseware/`：带逐页提词器备注和内嵌视频的 PPT。
- `visual-demos/lesson06-advise/`：每枚棋子的候选走法、合法性过滤和最终 bestmove。
- `src/xiagao_chess/`：FEN、UCI 会话、坐标转换和中文棋谱实现。
