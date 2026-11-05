# Pikafish 选步原理与代码核对

## 四层职责

```text
视觉模型：照片 → 棋子表
数据接口：棋子表 → FEN
Pikafish：FEN → 合法着法生成 → 搜索 → bestmove
交互层：UCI → 项目坐标 → 中文棋谱
```

“某枚棋子按规则能走到那里”不等于当前局面允许这么走。引擎必须继续检查走完后己方将帅是否仍被攻击，再在合法分支里向后搜索。

## 本课真实样例

```text
21 条按棋子规则展开的候选
→ 删除 19 条走后仍被将军的非法候选
→ 两条合法着法：e1d0、e2c0
→ 搜索后 bestmove e2c0
→ 相五退七
```

视频里的逐枚扫描是机制可视化，不声明 Pikafish 内部存在固定的逐枚遍历顺序。候选数量、合法着法和最终 bestmove 来自同一个真实局面。

## 视频与代码一致性

| 视频表达 | 代码位置 |
| --- | --- |
| 棋子表先转成 FEN | `board_to_fen()` |
| Python 通过 UCI 与引擎通信 | `PikafishSession` 发送 `position fen` 与 `go movetime` |
| 引擎返回 bestmove | `bestmove()` 读取 `bestmove` 行 |
| 无合法着法不是程序崩溃 | `(none)`、`none`、`0000` 返回 `None` |
| UCI 还原为项目坐标 | `uci_square_to_detector()` |
| 最后生成中文棋谱 | `move_to_notation()` |

每次命令独占一个 Pikafish 进程，避免上一次超时后的旧输出污染下一题。
