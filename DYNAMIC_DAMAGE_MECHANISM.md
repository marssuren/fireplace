# 动态伤害机制实现说明

## 卡牌信息

**TSC_219 - 渊狱魔犬希拉格（Xhilag of the Abyss）**

-   7 费 3/6
-   巨型+4
-   效果：在你的回合开始时，希拉格的蔓足造成的伤害提高 1 点

**TSC_219t - 希拉格之茎（Xhilag's Stalk）**

-   1 费 0/2
-   效果：在你的回合结束时，对一个随机敌人造成 1 点伤害

## 问题分析

### ❌ 简化实现（错误）

```python
class TSC_219e:
    """+1伤害"""
    # 简化实现：增加攻击力
    tags = {
        GameTag.ATK: 1,
    }

class TSC_219t:
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 1))
```

**问题**：

1. 增加攻击力不等于增加技能伤害
2. 技能伤害始终是 1 点，不会随着 buff 增加
3. 攻击力增加会影响随从的攻击，但不影响技能

### ✅ 完整实现（正确）

```python
class TSC_219:
    # 回合开始时，给所有茎添加伤害增加标记
    events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_MINIONS + ID("TSC_219t"), "TSC_219e"))


class TSC_219t:
    def trigger_end_of_turn_damage(self):
        # 统计TSC_219e buff的数量
        damage_bonus = sum(
            1 for buff in self.buffs
            if buff.id == "TSC_219e"
        )

        # 基础伤害1点 + 额外伤害
        total_damage = 1 + damage_bonus

        yield Hit(RANDOM_ENEMY_CHARACTER, total_damage)

    events = OWN_TURN_END.on(trigger_end_of_turn_damage)


class TSC_219e:
    """+1伤害增加标记"""
    # 只是一个计数标记，不增加攻击力
    pass
```

## 工作原理

### 1. 回合开始（TSC_219）

```python
events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_MINIONS + ID("TSC_219t"), "TSC_219e"))
```

**流程**：

-   每个回合开始时触发
-   给所有场上的"希拉格之茎"添加一个`TSC_219e` buff
-   这个 buff 只是一个计数标记

### 2. 回合结束（TSC_219t）

```python
def trigger_end_of_turn_damage(self):
    # 统计buff数量
    damage_bonus = sum(
        1 for buff in self.buffs
        if buff.id == "TSC_219e"
    )

    # 计算总伤害
    total_damage = 1 + damage_bonus

    yield Hit(RANDOM_ENEMY_CHARACTER, total_damage)
```

**流程**：

1. 回合结束时触发
2. 统计自己身上有多少个`TSC_219e` buff
3. 计算总伤害 = 1（基础）+ buff 数量
4. 造成伤害

### 3. 伤害增长示例

| 回合 | 回合开始添加 buff | buff 总数 | 回合结束伤害 |
| ---- | ----------------- | --------- | ------------ |
| 1    | +1                | 1         | 1 + 1 = 2    |
| 2    | +1                | 2         | 1 + 2 = 3    |
| 3    | +1                | 3         | 1 + 3 = 4    |
| 4    | +1                | 4         | 1 + 4 = 5    |

## 为什么不需要扩展核心？

### 已有的机制足够

1. **Buff 系统**：可以添加任意数量的相同 buff
2. **动态计算**：可以在运行时统计 buff 数量
3. **自定义方法**：可以在事件触发时执行自定义逻辑

### 实现模式

这个模式可以用于所有"累积增强"的效果：

```python
# 通用模式：累积增强
class MainCard:
    # 定期添加增强标记
    events = TRIGGER.on(Buff(TARGET, "enhancement_marker"))


class EnhancedCard:
    def trigger_effect(self):
        # 统计增强标记数量
        enhancement_count = sum(
            1 for buff in self.buffs
            if buff.id == "enhancement_marker"
        )

        # 使用增强值
        enhanced_value = base_value + enhancement_count

        yield Effect(enhanced_value)

    events = TRIGGER.on(trigger_effect)


class enhancement_marker:
    """只是一个计数标记"""
    pass
```

## 与攻击力增加的区别

### 攻击力增加

```python
class Buff:
    tags = {
        GameTag.ATK: 1,  # 增加攻击力
    }
```

**效果**：

-   影响随从的攻击伤害
-   影响随从的属性显示
-   **不影响**技能造成的伤害

### 技能伤害增加

```python
def trigger_damage(self):
    damage_bonus = sum(1 for buff in self.buffs if buff.id == "marker")
    total_damage = base_damage + damage_bonus
    yield Hit(TARGET, total_damage)
```

**效果**：

-   只影响技能造成的伤害
-   **不影响**随从的攻击伤害
-   **不影响**随从的属性显示

## 其他类似卡牌

### 可能需要类似实现的卡牌

1. **技能伤害随时间增加**

    - 每回合技能伤害+1
    - 每次触发后伤害+1

2. **累积效果**

    - 每回合效果增强
    - 每次触发后效果增强

3. **动态数值**
    - 基于 buff 数量计算
    - 基于游戏状态计算

## 总结

**结论**：

-   ✅ **不需要扩展核心**
-   ✅ 使用 buff 计数 + 动态计算即可完整实现
-   ✅ 符合官方行为
-   ✅ 代码清晰易维护

**关键点**：

1. 区分攻击力增加和技能伤害增加
2. 使用 buff 作为计数标记
3. 在触发时动态计算伤害值
4. 不要混淆属性增加和效果增强

**优势**：

1. 精确控制技能伤害
2. 不影响其他属性
3. 易于扩展和维护
4. 性能良好

---

**实现完成时间**：2025-12-31
**状态**：✅ 完整实现，无需扩展核心
