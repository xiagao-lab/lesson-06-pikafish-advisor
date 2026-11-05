# 练习 06：读懂 UCI 的 bestmove

完成 `starter.py`：

- 从 Pikafish 输出行解析四字符 UCI 走法。
- 把 `(none)`、`none`、`0000` 识别为“没有合法着法”。
- 把 UCI 格子坐标映射成项目使用的 `row/col`。

验收：

```bash
python exercises/check.py
```

加分题：把解析出的走法交给 `xiagao_chess.notation.move_to_notation`，验证 `e2c0` 能在样例局面中显示为“相五退七”。
