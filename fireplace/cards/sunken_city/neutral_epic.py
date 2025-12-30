# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立史诗
"""

from ..utils import *

class TSC_052:
    """School Teacher - 4费 5/4
    战吼：将一个1/1的娜迦幼体置入你的手牌。发现一个费用不超过(3)的法术来教导它"""
    play = Give(CONTROLLER, "TSC_052t") & GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomSpell(cost=3)))


class TSC_064:
    """Slithering Deathscale - 7费 5/9
    战吼：如果你在持有该牌时施放过3个法术，对所有敌人造成3点伤害"""
    powered_up = Count(Play(CONTROLLER, SPELL)) >= 3 & Buff(SELF, "TSC_064e")
    play = Find(SELF + POWERED_UP) & Hit(ALL_ENEMIES, 3)


class TSC_064e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}

class TSC_069:
    """Amalgam of the Deep - 2费 2/3
    战吼：选择一个友方随从。发现一个相同种族的随从"""
    # 简化实现：发现一个随机种族的随从
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion()))


class TSC_829:
    """Naga Giant - 20费 8/8
    你在本局对战中每在法术上花费1点法力值，该牌的费用便减少(1)点"""
    # 需要追踪本局对战中法术花费的法力值
    # 简化实现：每施放一个法术减少该牌费用
    events = Play(CONTROLLER, SPELL).after(
        Buff(FRIENDLY_HAND + ID("TSC_829"), "TSC_829e")
    )


class TSC_829e:
    """法术减费"""
    tags = {GameTag.COST: -1}


class TSC_926:
    """Smothering Starfish - 3费 2/4
    战吼：沉默所有其他随从"""
    play = Silence(ALL_MINIONS - SELF)

