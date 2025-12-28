# Fireplace 国际化 (i18n) 使用指南

## 概述

Fireplace 现在支持国际化（i18n），可以输出中文或英文的游戏日志。

## 快速开始

### 1. 设置语言

```python
from fireplace.i18n import set_language

# 设置为中文
set_language("zh_CN")

# 设置为英文
set_language("en")
```

### 2. 使用翻译日志

```python
from fireplace.logging import log_info

# 这会根据当前语言输出对应的日志
log_info("game_start")
log_info("attacks", attacker="随从A", defender="随从B")
log_info("draws", target="玩家1", card="火球术")
```

## 支持的语言

- `en` - English (英文)
- `zh_CN` - 简体中文

## 文件结构

```
fireplace/
├── fireplace/
│   ├── i18n.py              # 国际化核心模块
│   ├── logging.py           # 日志模块（已集成 i18n）
│   └── locales/             # 语言包目录
│       ├── en.json          # 英文翻译
│       └── zh_CN.json       # 中文翻译
```
