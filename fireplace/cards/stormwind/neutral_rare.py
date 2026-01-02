# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立稀有
"""

from ..utils import *


class DED_524:
    """多系施法者 / Multicaster
    战吼：在本局对战中，你每施放过一个不同派系的法术，抽一张牌。"""
    
    def play(self):
        """
        抽取等于本局游戏施放过的不同法术学派数量的卡牌
        
        使用 player.spell_schools_played_this_game 集合
        set 数据结构自动去重，len() 即为不同学派的数量
        """
        school_count = len(self.controller.spell_schools_played_this_game)
        if school_count > 0:
            yield Draw(CONTROLLER) * school_count



class SW_036:
    """双面投资者 / Two-Faced Investor
    在你的回合结束时，使你的一张手牌法力值消耗减少（1）点。（50%的几率改为消耗增加。）"""
    events = OwnTurnEnds(CONTROLLER).on(
        Find(FRIENDLY_HAND) & (
            Buff(RANDOM(FRIENDLY_HAND), "SW_036e_reduce") |
            Buff(RANDOM(FRIENDLY_HAND), "SW_036e_increase")
        )
    )


class SW_036e_reduce:
    """双面投资者减费"""
    cost = -1


class SW_036e_increase:
    """双面投资者增费"""
    cost = 1


class SW_062:
    """闪金镇豺狼人 / Goldshire Gnoll
    突袭 你的手牌中每有一张其他牌，本牌的法力值消耗便减少（1）点。"""
    cost_mod = -Count(FRIENDLY_HAND - SELF)


class SW_070:
    """邮箱舞者 / Mailbox Dancer
    战吼：将一个幸运币置入你的手牌。亡语：将一个幸运币置入你对手的手牌。"""
    play = Give(CONTROLLER, "GAME_005")  # The Coin
    deathrattle = Give(OPPONENT, "GAME_005")


class SW_306:
    """劳累的驮骡 / Encumbered Pack Mule
    嘲讽 当你抽到本牌时，将一张本牌的复制置入你的手牌。"""
    events = Draw(CONTROLLER, SELF).on(Give(CONTROLLER, Copy(SELF)))


class SW_400:
    """被困的女巫 / Entrapped Sorceress
    战吼：如果你控制一个任务，发现一张法术牌。"""
    play = Find(FRIENDLY_SECRETS + QUEST) & GenericChoice(
        CONTROLLER, Discover(CONTROLLER, RandomSpell())
    )
