# "持有期间"（While Holding）机制实现说明

## 问题描述

**卡牌**：TID_706 - 混乱使徒（Herald of Chaos）
**效果**：战吼：如果你在**持有本牌期间**施放过邪能法术，获得突袭。

## 实现方案对比

### ❌ 简化实现（错误）

```python
def play(self):
    # 检查整局游戏是否打出过邪能法术
    fel_spells_played = any(
        card.type == CardType.SPELL and SpellSchool.FEL in getattr(card, 'spell_schools', [])
        for card in self.controller.cards_played_this_game
    )

    if fel_spells_played:
        yield SetAttr(SELF, GameTag.RUSH, True)
```

**问题**：

-   检查的是整局游戏的历史
-   无法区分卡牌在手牌中前后发生的事件
-   不符合官方行为

### ✅ 完整实现（正确）

```python
class TID_706:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.LIFESTEAL: True,
    }

    # 在手牌中时监听邪能法术施放
    events = Play(CONTROLLER, SPELL + FEL).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TID_706_tracker")
    )

    def play(self):
        # 检查是否有追踪标记
        has_tracker = any(
            buff.id == "TID_706_tracker"
            for buff in self.buffs
        )

        if has_tracker:
            yield SetAttr(SELF, GameTag.RUSH, True)


class TID_706_tracker:
    """追踪标记"""
    pass
```

## 工作原理

### 1. 事件监听

```python
events = Play(CONTROLLER, SPELL + FEL).on(
    Find(SELF + IN_HAND) & Buff(SELF, "TID_706_tracker")
)
```

**说明**：

-   监听玩家施放邪能法术的事件
-   当事件触发时，检查自己是否在手牌中（`Find(SELF + IN_HAND)`）
-   如果在手牌中，给自己添加追踪标记 buff

### 2. 战吼检查

```python
def play(self):
    has_tracker = any(
        buff.id == "TID_706_tracker"
        for buff in self.buffs
    )

    if has_tracker:
        yield SetAttr(SELF, GameTag.RUSH, True)
```

**说明**：

-   打出时检查是否有追踪标记
-   如果有，说明在手牌中期间施放过邪能法术
-   触发效果：获得突袭

## 为什么不需要扩展核心？

### 已有的机制足够

1. **事件系统**：fireplace 已有完整的事件监听系统
2. **条件检查**：`Find(SELF + IN_HAND)`可以检查卡牌是否在手牌中
3. **Buff 系统**：可以用 buff 作为标记来追踪状态

### 实现模式

这个模式可以用于所有"while holding"卡牌：

```python
# 通用模式
class CardWithWhileHolding:
    # 监听特定事件，在手牌中时添加标记
    events = EventTrigger(CONDITION).on(
        Find(SELF + IN_HAND) & Buff(SELF, "tracker")
    )

    def play(self):
        # 检查标记
        if has_tracker:
            # 触发效果
            pass
```

## 其他"持有期间"卡牌

### 沉没之城中的类似卡牌

1. **TID_085** - 圣光使徒（牧师）

    - 如果持有期间施放过神圣法术，恢复 6 点生命值

2. **TSC_212** - 侍女（牧师）

    - 如果持有期间施放过三个法术，抽三张牌

3. **TSC_215** - 蛇发（牧师）

    - 如果持有期间打出过娜迦牌，再给一张蛇发

4. **TSC_058** - 捕食（恶魔猎手）

    - 如果持有期间打出过娜迦牌，费用为 0

5. **TSC_609** - 盘蛇指挥官（恶魔猎手）
    - 如果持有期间施放过三个法术，召唤两个复制

### 建议

所有这些卡牌都应该使用相同的模式实现：

-   使用事件监听 + 标记 buff
-   不要使用简化实现（检查整局历史）

## 总结

**结论**：

-   ✅ **不需要扩展核心**
-   ✅ 使用事件监听 + buff 标记即可完整实现
-   ✅ 符合官方行为
-   ✅ 代码清晰易维护

**优势**：

1. 精确追踪"持有期间"的事件
2. 不依赖全局历史记录
3. 性能更好（只在手牌中时监听）
4. 可复用的实现模式

---

**实现完成时间**：2025-12-31
**状态**：✅ 完整实现，无需扩展核心
