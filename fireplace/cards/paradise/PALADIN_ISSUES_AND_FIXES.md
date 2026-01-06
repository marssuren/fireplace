# 圣骑士实现问题修复方案

## 问题1: VAC_507 (阳光汲取者莱妮莎)

### 当前问题
- 使用未声明的临时属性 `_lynessa_cast`
- 使用 `Play()` action 重新施放可能导致费用重复扣除
- 不符合官方"施放两次"的机制

### 修复方案

参考官方"施放两次"的实现，应该在法术效果触发时重复触发，而不是重新施放整张牌。

```python
class VAC_507:
    """阳光汲取者莱妮莎 - Sunsapper Lynessa
    Rogue Tourist. Your spells that cost (2) or less cast twice.
    潜行者游客。你的法力值消耗小于或等于(2)点的法术会施放两次。
    """
    # 监听施放法术后，如果费用<=2，重复触发效果
    def on_spell_cast(self, source, card, target):
        """当施放法术后，如果费用<=2，重复触发其效果"""
        if card.cost <= 2:
            # 重复触发法术的 play() 效果
            # 使用相同的目标
            if hasattr(card, 'play') and callable(card.play):
                # 设置临时标记防止无限循环
                if not getattr(self, '_processing_lynessa', False):
                    self._processing_lynessa = True
                    # 重复触发法术效果（不重新扣费）
                    actions = card.get_actions("play")
                    if actions:
                        self.game.trigger(card, actions, event_args=None)
                    self._processing_lynessa = False
    
    events = Play(CONTROLLER, SPELL).after(
        lambda self, source, card, target: self.on_spell_cast(source, card, target)
    )
```

### 更好的方案（推荐）

使用光环效果，在法术施放时自动触发两次：

```python
class VAC_507:
    """阳光汲取者莱妮莎 - Sunsapper Lynessa
    Rogue Tourist. Your spells that cost (2) or less cast twice.
    潜行者游客。你的法力值消耗小于或等于(2)点的法术会施放两次。
    """
    # 给玩家添加光环效果
    def play(self):
        yield Buff(CONTROLLER, "VAC_507e")


class VAC_507e:
    """莱妮莎光环效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听施放法术
    def on_spell_played(self, source, card, target):
        """当施放法术时，如果费用<=2，重复触发"""
        if card.cost <= 2 and card.type == CardType.SPELL:
            # 标记防止无限循环
            if not getattr(card, '_lynessa_triggered', False):
                card._lynessa_triggered = True
                # 重复触发法术效果
                actions = card.get_actions("play")
                if actions:
                    self.game.trigger(card, actions, event_args=None)
                card._lynessa_triggered = False
    
    events = Play(CONTROLLER, SPELL).after(
        lambda self, source, card, target: self.on_spell_played(source, card, target)
    )
```

---

## 问题2: VAC_922e (救生光环)

### 当前问题
- 倒计时在回合结束时进行，应该在回合开始时
- 实例属性 `turns_remaining` 的管理方式可能不稳定

### 修复方案

参考 WORK_026e 的实现方式：

```python
class VAC_922e:
    """救生光环效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 持续3回合（在3个回合结束时触发）
        self.turns_remaining = 3
    
    # 回合结束时给予防晒霜
    def on_turn_end(self):
        """回合结束时触发"""
        yield Give(CONTROLLER, "VAC_921t")
        # 倒计时
        self.turns_remaining -= 1
        if self.turns_remaining <= 0:
            yield Destroy(SELF)
    
    events = OWN_TURN_END.on(
        lambda self, source: self.on_turn_end()
    )
```

**说明**: 当前实现其实是正确的，只是需要确保倒计时逻辑清晰。如果要改为回合开始时倒计时：

```python
class VAC_922e:
    """救生光环效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turns_remaining = 3
    
    # 回合开始时倒计时
    events = [
        # 回合结束时给予防晒霜
        OWN_TURN_END.on(
            lambda self, source: Give(CONTROLLER, "VAC_921t")
        ),
        # 回合开始时倒计时
        OWN_TURN_BEGIN.on(
            lambda self, source: (
                setattr(self, 'turns_remaining', self.turns_remaining - 1),
                Destroy(SELF) if self.turns_remaining <= 0 else None
            )
        )
    ]
```

---

## 建议

1. **立即修复**: VAC_507 的实现需要重写
2. **可选优化**: VAC_922e 的实现可以保持当前方式，但建议添加更清晰的注释
3. **测试验证**: 修复后需要进行充分测试

## 参考实现

可以参考以下卡牌的类似机制：
- **双生法术**: `twinspell` 机制
- **回响**: `echo` 机制  
- **持续回合效果**: `WORK_026e`, `VAC_524e`
