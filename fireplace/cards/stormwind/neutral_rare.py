# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立稀有
"""

from ..utils import *


class DED_524:
    """多系施法者 / Multicaster
    Battlecry: Draw a card for each different spell school you've cast this game."""
    # 需要追踪本局游戏中施放过的法术学派
    # 简化实现：抽取等于已施放不同学派数量的卡牌
    play = Draw(CONTROLLER) * Count(FRIENDLY_HERO + SPELLSCHOOLS_PLAYED)


class SW_036:
    """双面投资者 / Two-Faced Investor
    At the end of your turn, reduce the Cost of a card in your hand by (1). (50% chance to increase.)"""
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
    Rush Costs (1) less for each other card in your hand."""
    cost_mod = -Count(FRIENDLY_HAND - SELF)


class SW_070:
    """邮箱舞者 / Mailbox Dancer
    Battlecry: Add a Coin to your hand. Deathrattle: Give your opponent one."""
    play = Give(CONTROLLER, "GAME_005")  # The Coin
    deathrattle = Give(OPPONENT, "GAME_005")


class SW_306:
    """劳累的驮骡 / Encumbered Pack Mule
    Taunt When you draw this, add a copy of it to your hand."""
    events = Draw(CONTROLLER, SELF).on(Give(CONTROLLER, Copy(SELF)))


class SW_400:
    """被困的女巫 / Entrapped Sorceress
    Battlecry: If you control a Quest, Discover a spell."""
    play = Find(FRIENDLY_SECRETS + QUEST) & GenericChoice(
        CONTROLLER, Discover(CONTROLLER, RandomSpell())
    )
