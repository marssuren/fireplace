# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立史诗
"""

from ..utils import *

class TSC_052:
    """学校教师 - 4费 5/4
    战吼：将一张1/1的纳迦小学生置入你的手牌。发现一个法力值消耗小于或等于（3）点的法术，教会小学生"""
    play = (Give(CONTROLLER, "TSC_052t"), Discover(CONTROLLER, RandomSpell(cost=3)))


class TSC_064:
    """蛇行死鳞纳迦 - 7费 5/9
    战吼：如果你在本牌在你手中时施放过三个法术，则对所有敌人造成3点伤害"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spells_cast_while_holding = 0
    
    class Hand:
        events = Play(CONTROLLER, SPELL).after(
            lambda self, source, card: setattr(self, 'spells_cast_while_holding', 
                                               getattr(self, 'spells_cast_while_holding', 0) + 1)
        )
    
    powered_up = lambda self: self.spells_cast_while_holding >= 3
    
    play = lambda self: (
        Hit(ALL_ENEMIES, 3) if self.powered_up else []
    )


class TSC_064e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}

class TSC_069:
    """深海融合怪 - 2费 2/3
    战吼：选择一个友方随从，发现一张相同类型的随从牌"""
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    # 根据目标随从的种族发现相同种族的随从
    play = lambda self, target: (
        Discover(CONTROLLER, RandomMinion(race=target.race))
        if target and hasattr(target, 'race') and target.race
        else Discover(CONTROLLER, RandomMinion())
    )


class TSC_829:
    """纳迦巨人 - 20费 8/8
    在本局对战中，你每消耗1点法力值用于法术牌上，本牌的法力值消耗便减少（1）点"""
    # 使用 cost_mod 根据玩家在本局对战中施放法术消耗的总法力值来减费
    # Player 类中的 spent_mana_on_spells_this_game 属性会在每次施放法术时自动更新
    cost_mod = -AttrValue("spent_mana_on_spells_this_game")(CONTROLLER)


class TSC_926:
    """掩息海星 - 3费 2/4
    战吼：沉默所有其他随从"""
    play = Silence(ALL_MINIONS - SELF)

