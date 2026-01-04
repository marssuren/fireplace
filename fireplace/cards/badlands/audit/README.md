# TITANS Audit Tools

本目录包含用于验证泰坦诸神扩展包实现进度的工具。

## 包含文件

- `cards.json`: 从游戏数据中提取的泰坦诸神扩展包卡牌数据。
- `verify_titans.py`:检查卡牌是否已在代码中定义（通过 ID 匹配类名）。
- `check_placeholders.py`: 检查已定义的类是否仅包含 `pass`（即占位符）。
- `VALIDATION_REPORT.md` (自动生成): 验证报告。

## 使用方法

### 1. 检查实现进度

运行以下命令查看当前实现了多少张卡牌：

```bash
python verify_titans.py
```

### 2. 检查占位符

运行以下命令查看哪些卡牌只是占位符（未实现逻辑）：

```bash
python check_placeholders.py
```
