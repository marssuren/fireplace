"""
威兹班的工坊 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class MIS_102:
    """退货政策 - Return Policy
    Discover a friendly Deathrattle card you've played this game. Trigger its Deathrattle.
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class MIS_710:
    """滑矛布袋手偶 - Sock Puppet Slitherspear
    This minion's Attack is improved by your hero's.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_641:
    """裁判拳套 - Umpire's Grasp
    Deathrattle: Draw a Demon and reduce its Cost by (2).
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class TOY_642:
    """球霸野猪人 - Ball Hog
    [x]Lifesteal Battlecry and Deathrattle: Deal 2 damage to the lowest Health enemy.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE, LIFESTEAL
    # TODO: 实现卡牌效果
    pass


class TOY_643:
    """盲盒 - Blind Box
    Get 2 random Demons. Outcast: Discover them instead.
    """
    # Mechanics: DISCOVER, OUTCAST
    # TODO: 实现卡牌效果
    pass


# RARE

class MIS_911:
    """残次聒噪怪 - Gibbering Reject
    After your hero attacks, summon another Gibbering Reject.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class TOY_028:
    """团队之灵 - Spirit of the Team
    Stealth for 1 turn. Your hero has +2 Attack on your turn.
    """
    # Mechanics: AURA, STEALTH
    # TODO: 实现卡牌效果
    pass


class TOY_640:
    """工坊事故 - Workshop Mishap
    Deal $5 damage to a minion. Excess damages both neighbors. Outcast: Gain Lifesteal.
    """
    # Mechanics: OUTCAST, ImmuneToSpellpower
    # TODO: 实现卡牌效果
    pass


class TOY_645:
    """小型法术欧珀石 - Lesser Opal Spellstone
    Draw 1 card. <i>(Attack with your hero 2 times to upgrade.)</i>
    """
    # TODO: 实现卡牌效果
    pass


# EPIC

class TOY_644:
    """红牌 - Red Card
    Make a minion go Dormant for 2 turns.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_652:
    """橱窗看客 - Window Shopper
    [x]Miniaturize Battlecry: Discover a Demon. Set its stats and Cost to this minion's.
    """
    # Mechanics: BATTLECRY, DISCOVER, MINIATURIZE
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class TOY_647:
    """玛瑟里顿（未发售版） - Magtheridon, Unreleased
    [x]Dormant for 2 turns. While Dormant, deal 3 damage to all enemies at the end of your turn.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_913:
    """希希集 - Ci'Cigi
    [x]Battlecry, Outcast, and Deathrattle: Get a random   first-edition Demon Hunter   card <i>(in mint condition)</i>.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE, OUTCAST
    # TODO: 实现卡牌效果
    pass


