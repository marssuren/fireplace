"""
威兹班的工坊 - Zilliax Deluxe 3000 模块组合变体
包含所有28种功能模块组合的完整实现
"""
from ..utils import *


# ========================================
# Zilliax Deluxe 3000 组合变体 (1-7)
# ========================================

class TOY_330_HaywirePower:
    """Zilliax Deluxe 3000 - Haywire + Power
    混乱模块 + 能量模块
    """
    # 组合属性：(2+2)费 (4+1)/(4+3) = 4费 5/7
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：回合开始时使本随从的攻击力翻倍

    events = [
        OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3)),
        OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))
    ]


class TOY_330_PowerBuff:
    """能量模块 - 攻击力翻倍"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    def apply(self, target):
        # 使攻击力翻倍
        target.atk = target.atk * 2


class TOY_330_HaywirePylon:
    """Zilliax Deluxe 3000 - Haywire + Pylon
    混乱模块 + 能量塔模块
    """
    # 组合属性：(2+3)费 (4+2)/(4+2) = 5费 6/6
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：你的其他随从获得+1攻击力

    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3))
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})


class TOY_330_HaywireRecursive:
    """Zilliax Deluxe 3000 - Haywire + Recursive
    混乱模块 + 递归模块
    """
    # 组合属性：(2+1)费 (4+1)/(4+1) = 3费 5/5
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：亡语：将本随从洗入你的牌库

    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3))
    deathrattle = Shuffle(CONTROLLER, SELF)


class TOY_330_HaywireTicking:
    """Zilliax Deluxe 3000 - Haywire + Ticking
    混乱模块 + 计时模块
    """
    # 组合属性：(2+4)费 (4+1)/(4+3) = 6费 5/7
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：你每有一个友方随从，本牌的法力值消耗减少（1）点

    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3))
    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)


class TOY_330_HaywireTwin:
    """Zilliax Deluxe 3000 - Haywire + Twin
    混乱模块 + 双生模块
    """
    # 组合属性：(2+4)费 (4+3)/(4+3) = 6费 7/7
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：战吼：召唤一个本随从的复制

    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3))

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_330_HaywirePerfect:
    """Zilliax Deluxe 3000 - Haywire + Perfect
    混乱模块 + 完美模块
    """
    # 组合属性：(2+5)费 (4+3)/(4+2) = 7费 7/6
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：圣盾，嘲讽，吸血，突袭

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True

    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3))


class TOY_330_HaywireVirus:
    """Zilliax Deluxe 3000 - Haywire + Virus
    混乱模块 + 病毒模块
    """
    # 组合属性：(2+4)费 (4+2)/(4+2) = 6费 6/6
    # 效果1：回合结束时对你的英雄造成3点伤害
    # 效果2：扰魔，剧毒

    elusive = True
    poisonous = True
    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 3))


# ========================================
# Power 模块组合 (8-13)
# ========================================

class TOY_330_PowerPylon:
    """Zilliax Deluxe 3000 - Power + Pylon
    能量模块 + 能量塔模块
    """
    # 组合属性：(2+3)费 (1+2)/(3+2) = 5费 3/5
    # 效果1：回合开始时使本随从的攻击力翻倍
    # 效果2：你的其他随从获得+1攻击力

    events = OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})


class TOY_330_PowerRecursive:
    """Zilliax Deluxe 3000 - Power + Recursive
    能量模块 + 递归模块
    """
    # 组合属性：(2+1)费 (1+1)/(3+1) = 3费 2/4
    # 效果1：回合开始时使本随从的攻击力翻倍
    # 效果2：亡语：将本随从洗入你的牌库

    events = OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))
    deathrattle = Shuffle(CONTROLLER, SELF)


class TOY_330_PowerTicking:
    """Zilliax Deluxe 3000 - Power + Ticking
    能量模块 + 计时模块
    """
    # 组合属性：(2+4)费 (1+1)/(3+3) = 6费 2/6
    # 效果1：回合开始时使本随从的攻击力翻倍
    # 效果2：你每有一个友方随从，本牌的法力值消耗减少（1）点

    events = OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))
    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)


class TOY_330_PowerTwin:
    """Zilliax Deluxe 3000 - Power + Twin
    能量模块 + 双生模块
    """
    # 组合属性：(2+4)费 (1+3)/(3+3) = 6费 4/6
    # 效果1：回合开始时使本随从的攻击力翻倍
    # 效果2：战吼：召唤一个本随从的复制

    events = OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_330_PowerPerfect:
    """Zilliax Deluxe 3000 - Power + Perfect
    能量模块 + 完美模块
    """
    # 组合属性：(2+5)费 (1+3)/(3+2) = 7费 4/5
    # 效果1：回合开始时使本随从的攻击力翻倍
    # 效果2：圣盾，嘲讽，吸血，突袭

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True
    events = OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))


class TOY_330_PowerVirus:
    """Zilliax Deluxe 3000 - Power + Virus
    能量模块 + 病毒模块
    """
    # 组合属性：(2+4)费 (1+2)/(3+2) = 6费 3/5
    # 效果1：回合开始时使本随从的攻击力翻倍
    # 效果2：扰魔，剧毒

    elusive = True
    poisonous = True
    events = OWN_TURN_BEGIN.on(lambda self: Buff(SELF, "TOY_330_PowerBuff"))


# ========================================
# Pylon 模块组合 (14-18)
# ========================================

class TOY_330_PylonRecursive:
    """Zilliax Deluxe 3000 - Pylon + Recursive
    能量塔模块 + 递归模块
    """
    # 组合属性：(3+1)费 (2+1)/(2+1) = 4费 3/3
    # 效果1：你的其他随从获得+1攻击力
    # 效果2：亡语：将本随从洗入你的牌库

    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})
    deathrattle = Shuffle(CONTROLLER, SELF)


class TOY_330_PylonTicking:
    """Zilliax Deluxe 3000 - Pylon + Ticking
    能量塔模块 + 计时模块
    """
    # 组合属性：(3+4)费 (2+1)/(2+3) = 7费 3/5
    # 效果1：你的其他随从获得+1攻击力
    # 效果2：你每有一个友方随从，本牌的法力值消耗减少（1）点

    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})
    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)


class TOY_330_PylonTwin:
    """Zilliax Deluxe 3000 - Pylon + Twin
    能量塔模块 + 双生模块
    """
    # 组合属性：(3+4)费 (2+3)/(2+3) = 7费 5/5
    # 效果1：你的其他随从获得+1攻击力
    # 效果2：战吼：召唤一个本随从的复制

    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_330_PylonPerfect:
    """Zilliax Deluxe 3000 - Pylon + Perfect
    能量塔模块 + 完美模块
    """
    # 组合属性：(3+5)费 (2+3)/(2+2) = 8费 5/4
    # 效果1：你的其他随从获得+1攻击力
    # 效果2：圣盾，嘲讽，吸血，突袭

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})


class TOY_330_PylonVirus:
    """Zilliax Deluxe 3000 - Pylon + Virus
    能量塔模块 + 病毒模块
    """
    # 组合属性：(3+4)费 (2+2)/(2+2) = 7费 4/4
    # 效果1：你的其他随从获得+1攻击力
    # 效果2：扰魔，剧毒

    elusive = True
    poisonous = True
    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})


# ========================================
# Recursive 模块组合 (19-22)
# ========================================

class TOY_330_RecursiveTicking:
    """Zilliax Deluxe 3000 - Recursive + Ticking
    递归模块 + 计时模块
    """
    # 组合属性：(1+4)费 (1+1)/(1+3) = 5费 2/4
    # 效果1：亡语：将本随从洗入你的牌库
    # 效果2：你每有一个友方随从，本牌的法力值消耗减少（1）点

    deathrattle = Shuffle(CONTROLLER, SELF)
    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)


class TOY_330_RecursiveTwin:
    """Zilliax Deluxe 3000 - Recursive + Twin
    递归模块 + 双生模块
    """
    # 组合属性：(1+4)费 (1+3)/(1+3) = 5费 4/4
    # 效果1：亡语：将本随从洗入你的牌库
    # 效果2：战吼：召唤一个本随从的复制

    deathrattle = Shuffle(CONTROLLER, SELF)

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_330_RecursivePerfect:
    """Zilliax Deluxe 3000 - Recursive + Perfect
    递归模块 + 完美模块
    """
    # 组合属性：(1+5)费 (1+3)/(1+2) = 6费 4/3
    # 效果1：亡语：将本随从洗入你的牌库
    # 效果2：圣盾，嘲讽，吸血，突袭

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True
    deathrattle = Shuffle(CONTROLLER, SELF)


class TOY_330_RecursiveVirus:
    """Zilliax Deluxe 3000 - Recursive + Virus
    递归模块 + 病毒模块
    """
    # 组合属性：(1+4)费 (1+2)/(1+2) = 5费 3/3
    # 效果1：亡语：将本随从洗入你的牌库
    # 效果2：扰魔，剧毒

    elusive = True
    poisonous = True
    deathrattle = Shuffle(CONTROLLER, SELF)


# ========================================
# Ticking 模块组合 (23-25)
# ========================================

class TOY_330_TickingTwin:
    """Zilliax Deluxe 3000 - Ticking + Twin
    计时模块 + 双生模块
    """
    # 组合属性：(4+4)费 (1+3)/(3+3) = 8费 4/6
    # 效果1：你每有一个友方随从，本牌的法力值消耗减少（1）点
    # 效果2：战吼：召唤一个本随从的复制

    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_330_TickingPerfect:
    """Zilliax Deluxe 3000 - Ticking + Perfect
    计时模块 + 完美模块
    """
    # 组合属性：(4+5)费 (1+3)/(3+2) = 9费 4/5
    # 效果1：你每有一个友方随从，本牌的法力值消耗减少（1）点
    # 效果2：圣盾，嘲讽，吸血，突袭

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True
    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)


class TOY_330_TickingVirus:
    """Zilliax Deluxe 3000 - Ticking + Virus
    计时模块 + 病毒模块
    """
    # 组合属性：(4+4)费 (1+2)/(3+2) = 8费 3/5
    # 效果1：你每有一个友方随从，本牌的法力值消耗减少（1）点
    # 效果2：扰魔，剧毒

    elusive = True
    poisonous = True
    cost_mod = lambda self, i: -Count(FRIENDLY_MINIONS)


# ========================================
# Twin 模块组合 (26-27)
# ========================================

class TOY_330_TwinPerfect:
    """Zilliax Deluxe 3000 - Twin + Perfect
    双生模块 + 完美模块
    """
    # 组合属性：(4+5)费 (3+3)/(3+2) = 9费 6/5
    # 效果1：战吼：召唤一个本随从的复制
    # 效果2：圣盾，嘲讽，吸血，突袭

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_330_TwinVirus:
    """Zilliax Deluxe 3000 - Twin + Virus
    双生模块 + 病毒模块
    """
    # 组合属性：(4+4)费 (3+2)/(3+2) = 8费 5/5
    # 效果1：战吼：召唤一个本随从的复制
    # 效果2：扰魔，剧毒

    elusive = True
    poisonous = True

    def play(self):
        yield Summon(CONTROLLER, ExactCopy(SELF))


# ========================================
# Perfect 模块组合 (28)
# ========================================

class TOY_330_PerfectVirus:
    """Zilliax Deluxe 3000 - Perfect + Virus
    完美模块 + 病毒模块
    """
    # 组合属性：(5+4)费 (3+2)/(2+2) = 9费 5/4
    # 效果1：圣盾，嘲讽，吸血，突袭
    # 效果2：扰魔，剧毒

    divine_shield = True
    taunt = True
    lifesteal = True
    rush = True
    elusive = True
    poisonous = True


# ========================================
# 总结
# ========================================
#
# 已完成所有28种 Zilliax Deluxe 3000 模块组合变体的实现
#
# 组合列表：
# 1-7:   Haywire + (Power, Pylon, Recursive, Ticking, Twin, Perfect, Virus)
# 8-13:  Power + (Pylon, Recursive, Ticking, Twin, Perfect, Virus)
# 14-18: Pylon + (Recursive, Ticking, Twin, Perfect, Virus)
# 19-22: Recursive + (Ticking, Twin, Perfect, Virus)
# 23-25: Ticking + (Twin, Perfect, Virus)
# 26-27: Twin + (Perfect, Virus)
# 28:    Perfect + Virus
#
# 使用说明：
# - 在实际游戏中，玩家在构筑套牌时选择2个功能模块
# - 系统会将 TOY_330 替换为对应的组合变体卡牌
# - 每个变体的费用、属性和效果都是两个模块的叠加
