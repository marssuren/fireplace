# 通灵学园（Scholomance Academy）质量审查报告

## 审查时间

2025-12-31

## 审查范围

-   14 个 Python 文件
-   135 张卡牌
-   总代码行数：约 1,914 行

## 发现的问题

### 🔴 优先级 1 - 简化实现（需要修复）

#### 1. SCH_162 - Vectus（维克图斯）

**文件**：`neutral_legendary.py:69-92`
**问题**：

```python
# 复制亡语效果（简化实现：添加相同的亡语）
if hasattr(source, 'deathrattle'):
    whelp.deathrattle = source.deathrattle
```

**影响**：直接赋值 deathrattle 可能不正确，应该使用 CopyDeathrattleBuff
**修复方案**：使用 fireplace 的 CopyDeathrattleBuff 机制

#### 2. SCH_259 - Sphere of Sapience（睿智法球）

**文件**：`neutral_legendary.py:112-118`
**问题**：

```python
# 注：原版需要玩家交互选择是否置底，AI训练中简化为仅显示
events = OWN_TURN_BEGIN.on(Reveal(TOP(FRIENDLY_DECK)))
```

**影响**：缺少"置底"功能，只是显示卡牌
**修复方案**：

-   方案 1：实现完整的玩家选择机制
-   方案 2：AI 训练中使用随机选择（更合理）

### 🟡 优先级 2 - 需要验证的实现

#### 3. SCH_351 - Jandice Barov（詹迪斯·巴罗夫）

**文件**：`neutral_legendary.py:37-58`
**状态**：✅ 实现看起来正确
**说明**：使用随机选择代替玩家秘密选择，对 AI 训练是合理的

#### 4. 所有 `pass` 语句

**文件**：多个文件
**数量**：16 个
**说明**：这些都是 Token 卡牌或纯属性卡牌，`pass` 是正确的

### 🟢 优先级 3 - 需要检查的细节

#### 5. 检查所有 Spellburst 实现

**需要验证**：

-   Spellburst 触发逻辑是否正确
-   SPELLBURST_SPELL 选择器是否可用
-   一次性触发是否正确实现

#### 6. 检查所有自定义 play 方法

**需要验证**：

-   是否正确使用 yield
-   是否正确处理边界情况
-   是否与 DSL 一致

## 详细问题列表

### 简化实现（2 个）

| 卡牌 ID | 卡牌名             | 文件                 | 行数 | 问题描述                                         |
| ------- | ------------------ | -------------------- | ---- | ------------------------------------------------ |
| SCH_162 | Vectus             | neutral_legendary.py | 89   | 直接赋值 deathrattle，应使用 CopyDeathrattleBuff |
| SCH_259 | Sphere of Sapience | neutral_legendary.py | 117  | 缺少置底功能，只是显示卡牌                       |

### 需要深入检查的文件

1. **neutral_legendary.py** - 2 个简化实现
2. **paladin.py** - 需要检查 Spellburst 实现
3. **priest.py** - 需要检查复杂效果
4. **demonhunter.py** - 需要检查自定义逻辑

## 下一步行动

### 立即修复

1. ✅ SCH_162 - 使用 CopyDeathrattleBuff
2. ✅ SCH_259 - 实现完整的置底逻辑（或合理简化）

### 深入审查

3. 检查所有 Spellburst 实现
4. 检查所有自定义 play 方法
5. 验证所有复杂效果

### 测试验证

6. 创建测试用例
7. 验证核心机制
8. 确保无运行时错误

## 总体评估

**代码质量**：⭐⭐⭐⭐☆ (4/5)

-   ✅ 大部分实现正确
-   ✅ 使用了 fireplace DSL
-   ⚠️ 存在 2 个简化实现
-   ✅ 代码结构清晰

**完成度**：95%

-   需要修复 2 个简化实现
-   需要深入验证复杂效果

**预计修复时间**：1-2 小时
