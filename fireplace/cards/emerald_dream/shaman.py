"""
漫游翡翠梦境 - SHAMAN
"""
from ..utils import *


# COMMON

class EDR_231:
    """守护巨龙之拥 - Aspect's Embrace
    [x]Restore #4 Health. Draw a card. Imbue your Hero Power.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_233:
    """森林之灵 - Spirits of the Forest
    Choose One - Summon three 2/3 Wolves with Taunt; or Summon two 4/3 Falcons with Windfury.
    """
    # Mechanics: CHOOSE_ONE
    # TODO: 实现卡牌效果
    pass


class EDR_477:
    """明根捕食花 - Glowroot Lure
    [x]Taunt. Costs (1) less for each time you used your Hero Power this game.
    """
    # Mechanics: TAUNT
    # TODO: 实现卡牌效果
    pass


class FIR_778:
    """毁灭化身 - Avatar of Destruction
    [x]Taunt Deathrattle: Deal 9 damage to all enemy minions.
    """
    # Mechanics: DEATHRATTLE, TAUNT
    # TODO: 实现卡牌效果
    pass


# RARE

class EDR_232:
    """台风 - Typhoon
    Each minion gets shuffled into a random player's deck.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_234:
    """翡翠厚赠 - Emerald Bounty
    Draw 2 cards. You can't play them for 2 turns.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_518:
    """活体园林 - Living Garden
    [x]Battlecry: Imbue your Hero Power. Reduce the Cost of a  minion in your hand by (1).
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class FIR_923:
    """炎魔之火 - Flames of the Firelord
    [x]Deal $4 damage to a random enemy minion. If you're holding a card that costs (8) or more, deal $8 instead.
    """
    # TODO: 实现卡牌效果
    pass


class FIR_927:
    """烬鳞雏龙 - Emberscarred Whelp
    [x]Battlecry: Discover a 5-Cost card. Gain 1 Mana Crystal next turn only.
    """
    # Mechanics: BATTLECRY, DISCOVER
    # TODO: 实现卡牌效果
    pass


# EPIC

class EDR_230:
    """豆蔓蛮兵 - Beanstalk Brute
    Battlecry: Give +4/+4 to the top 3 minions in your deck.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class EDR_529:
    """胆大的魔荚人 - Plucky Podling
    [x]If this would transform into a minion, it transforms into one that costs (2) more.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class EDR_031:
    """欧恩哈拉 - Ohn'ahra
    At the end of your turn, play the top 3 cards from your deck.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class EDR_238:
    """麦琳瑟拉 - Merithra
    [x]Battlecry: Resurrect all different friendly minions that cost (8) or more.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


