"""
漫游翡翠梦境 - WARLOCK
"""
from ..utils import *


# COMMON

class EDR_482:
    """烂苹果 - Rotten Apple
    Restore #12 Health to your hero. For the next 2 turns, deal $3 damage to your hero.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_488:
    """前卫园艺 - Avant-Gardening
    [x]Discover a Deathrattle minion with a Dark Gift.
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class EDR_494:
    """饥饿古树 - Hungering Ancient
    [x]At the end of your turn, eat a minion in your deck and gain its stats. Deathrattle:       Add them to your hand.     
    """
    # Mechanics: DEATHRATTLE, TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class FIR_924:
    """影焰猎豹 - Shadowflame Stalker
    Battlecry: Discover a Demon with a Dark Gift. Get a copy of it.
    """
    # Mechanics: BATTLECRY, DISCOVER
    # TODO: 实现卡牌效果
    pass


class FIR_955:
    """烬根毁灭者 - Emberroot Destroyer
    [x]Whenever your hero takes damage on your turn, deal 3 damage to a random enemy minion.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


# RARE

class EDR_485:
    """腐心树妖 - Rotheart Dryad
    Deathrattle: Draw a minion that costs (7) or more.
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class EDR_490:
    """麻痹睡眠 - Sleep Paralysis
    [x]Choose One - Summon two 3/6 Demons with Taunt that can't attack; or Destroy an enemy minion.
    """
    # Mechanics: CHOOSE_ONE
    # TODO: 实现卡牌效果
    pass


class EDR_654:
    """疯长的恐魔 - Overgrown Horror
    [x]Taunt Battlecry: Reduce the Cost of minions in your hand with Dark Gifts by (2).
    """
    # Mechanics: BATTLECRY, TAUNT
    # TODO: 实现卡牌效果
    pass


class FIR_954:
    """焚烧 - Conflagrate
    Deal $5 damage to a minion. Its owner draws a card.
    """
    # TODO: 实现卡牌效果
    pass


# EPIC

class EDR_483:
    """破碎之力 - Fractured Power
    Destroy one of your Mana Crystals. In 2 turns, gain two.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_491:
    """荆棘大德鲁伊 - Archdruid of Thorns
    Battlecry: Gain the Deathrattles of your minions that died this turn.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class EDR_487:
    """瓦洛，污邪古树 - Wallow, the Wretched
    While this is in your hand or deck, it gains a copy of every Dark Gift given to your minions.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_489:
    """阿迦玛甘 - Agamaggan
    [x]Battlecry: The next card you play costs your OPPONENT'S Health instead of Mana <i>(up to 10)</i>.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


