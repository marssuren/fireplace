# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 萨满
"""

from ..utils import *

class DED_509:
    """艳丽的金刚鹦鹉 / Brilliant Macaw
    Battlecry: Repeat the last Battlecry you played."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class DED_511:
    """吸盘钩手 / Suckerhook
    At the end of your turn, transform your weapon into one that costs (1) more."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class DED_522:
    """厨师曲奇 / Cookie the Cook
    Lifesteal Deathrattle: Equip a 2/3   Stirring Rod with Lifesteal. """
    # TODO: Implement mechanics: DEATHRATTLE, LIFESTEAL
    # deathrattle = ...

class SW_025:
    """拍卖行木槌 / Auctionhouse Gavel
    After your hero attacks, reduce the Cost of a Battlecry minion in your hand by (1)."""
    # TODO: Implement mechanics: TRIGGER_VISUAL
    # play = ...

class SW_026:
    """幽灵狼前锋 / Spirit Alpha
    After you play a card with Overload, summon a 2/3 Spirit Wolf with Taunt."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class SW_031:
    """号令元素 / Command the Elements
    Questline: Play 3 cards  with Overload. Reward: Unlock your Overloaded Mana Crystals."""
    # TODO: Implement Questline mechanic
    # play = ...

class SW_032:
    """花岗岩熔铸体 / Granite Forgeborn
    Battlecry: Reduce the Cost of Elementals in your hand and deck by (1)."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class SW_033:
    """运河慢步者 / Canal Slogger
    Rush, Lifesteal Overload: (1)"""
    pass

class SW_034:
    """小巧玩具 / Tiny Toys
    Summon four random 5-Cost minions. Make them 2/2."""
    # play = ...

class SW_035:
    """充能召唤 / Charged Call
    Discover a 1-Cost minion and summon it.  (Upgraded for each Overload  card you played this game!)"""
    # TODO: Implement mechanics: DISCOVER
    # play = ...

class SW_095:
    """投资良机 / Investment Opportunity
    Draw an Overload card."""
    # play = ...

class SW_114:
    """强行透支 / Overdraft
    Tradeable Unlock your Overloaded Mana Crystals to deal that much damage."""
    # TODO: Implement mechanics: AFFECTED_BY_SPELL_POWER, TRADEABLE
    # TODO: Implement Tradeable mechanic
    # play = ...

class SW_115:
    """伯尔纳·锤喙 / Bolner Hammerbeak
    After you play a Battlecry minion, repeat the first   Battlecry played this turn. """
    # TODO: Implement mechanics: TRIGGER_VISUAL
    # play = ...

