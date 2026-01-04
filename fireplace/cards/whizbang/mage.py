"""
威兹班的工坊 - MAGE
"""
from ..utils import *


# COMMON

class MIS_302:
    """买一冻一 - Buy One, Get One Freeze
    Freeze a minion. Summon a Frozen copy of it.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_037:
    """寻物解谜 - Hidden Objects
    Discover a Secret. Set its Cost to (1).
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class TOY_370:
    """三芯诡烛 - Triplewick Trickster
    Battlecry: Deal 2 damage to a random enemy, three times.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class TOY_374:
    """找不同 - Spot the Difference
    Discover a 3-Cost minion to summon. If your deck has no minions, repeat this.
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


# RARE

class MIS_107:
    """玩具故障 - Malfunction
    Deal $3 damage split among all enemy minions. If your deck has no minions, deal $3 more.
    """
    # Mechanics: ImmuneToSpellpower
    # TODO: 实现卡牌效果
    pass


class MIS_303:
    """暗月魔术师 - Darkmoon Magician
    [x]Elusive After you cast a spell, cast a random spell that costs (1) more.
    """
    # Mechanics: ELUSIVE, TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class TOY_371:
    """加工失误 - Manufacturing Error
    Draw 3 cards. If your deck has no minions, they cost (3) less.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_375:
    """滑冰元素 - Sleet Skater
    Miniaturize Battlecry: Freeze an enemy minion. Gain Armor equal to its Attack.
    """
    # Mechanics: BATTLECRY, MINIATURIZE
    # TODO: 实现卡牌效果
    pass


class TOY_377:
    """霜巫十字绣 - Frost Lich Cross-Stitch
    Deal $3 damage to a character. If it dies, summon a 3/6 Water Elemental that Freezes.
    """
    # TODO: 实现卡牌效果
    pass


# EPIC

class TOY_372:
    """匣中古神 - Yogg in the Box
    Cast 5 random spells. If your deck has no minions, the spells cast cost (5) or more.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_376:
    """水彩美术家 - Watercolor Artist
    Battlecry: Draw a Frost spell. At the start of your turns, reduce its Cost by (1).
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class TOY_373:
    """益智大师卡德加 - Puzzlemaster Khadgar
    [x]Battlecry: Equip a 0/6 Wisdomball that casts helpful Mage spells!
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class TOY_378:
    """星空投影球 - The Galactic Projection Orb
    Recast a random spell of each Cost you've cast this game <i>(targets enemies if possible)</i>.
    """
    # TODO: 实现卡牌效果
    pass


