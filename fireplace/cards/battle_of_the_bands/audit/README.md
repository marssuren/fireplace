# -*- coding: utf-8 -*-
"""
传奇音乐节 - 测试套件说明
"""

# 测试工具集概览

## 1. verify_festival.py
**用途**: 完整性验证
- 检查所有可收集卡牌是否都有对应的类定义
- 对比 cards.json 与代码实现
- 输出缺失卡牌列表

**运行方式**:
```bash
cd fireplace/fireplace/cards/battle_of_the_bands/audit
python verify_festival.py
```

## 2. check_placeholders.py
**用途**: 占位符检查
- 扫描所有卡牌类，查找未实现的 `pass` 语句
- 识别需要补充逻辑的卡牌
- 输出占位符类列表及位置

**运行方式**:
```bash
python check_placeholders.py
```

## 3. test_mechanics.py
**用途**: 核心机制测试
- 测试 Finale（压轴）机制
- 测试 Overload（过载）机制
- 测试 Location（地标）机制
- 测试 Predamage（伤害预防）机制

**运行方式**:
```bash
python test_mechanics.py
```

**注意**: 此测试需要完整的 fireplace 环境

## 测试流程建议

### 阶段 1: 完整性检查
```bash
python verify_festival.py
```
确保所有卡牌都有类定义

### 阶段 2: 占位符检查
```bash
python check_placeholders.py
```
确认没有遗漏的 `pass` 占位符

### 阶段 3: 机制验证
```bash
python test_mechanics.py
```
验证核心机制是否正常工作

### 阶段 4: 实战测试
创建实际对局场景，测试复杂交互

## 已知限制

1. **verify_festival.py**: 仅检查类定义存在性，不验证逻辑正确性
2. **check_placeholders.py**: 使用启发式方法，可能有误报
3. **test_mechanics.py**: 需要完整的游戏环境，某些测试可能因环境问题失败

## 扩展建议

1. 添加单卡测试用例（针对复杂卡牌如 Symphony of Sins）
2. 添加职业特定测试（如萨满的 Overload 协同）
3. 添加边缘情况测试（如满手牌、空牌库等）
4. 集成到 CI/CD 流程

## 维护说明

- 当添加新卡牌时，运行 `verify_festival.py` 确认
- 当修改核心机制时，运行 `test_mechanics.py` 回归测试
- 定期运行 `check_placeholders.py` 确保代码质量
