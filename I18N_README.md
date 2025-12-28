# Fireplace 国际化 (i18n) 功能说明

## 功能概述

为 Fireplace 项目添加了完整的国际化支持，现在可以输出中文或英文的游戏日志。

## 已完成的工作

### 1. 核心模块
- ✅ 创建了 `fireplace/i18n.py` - 国际化核心模块
- ✅ 修改了 `fireplace/logging.py` - 集成 i18n 支持
- ✅ 添加了 `log_info()` 函数用于翻译日志

### 2. 语言包
- ✅ 创建了 `fireplace/locales/en.json` - 英文翻译（55+ 条消息）
- ✅ 创建了 `fireplace/locales/zh_CN.json` - 中文翻译（55+ 条消息）

### 3. 工具和示例
- ✅ `i18n_example.py` - 使用示例
- ✅ `convert_logs_to_i18n.py` - 批量转换脚本
- ✅ `I18N_GUIDE.md` - 使用指南

## 快速使用

### 方式一：在代码中设置语言

```python
from fireplace.i18n import set_language

# 设置为中文
set_language("zh_CN")

# 现在所有日志都会输出中文
```

### 方式二：使用环境变量

```bash
# Linux/Mac
export FIREPLACE_LANG=zh_CN

# Windows
set FIREPLACE_LANG=zh_CN
```
