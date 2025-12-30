"""
威兹班的工坊 - WARRIOR
"""
from ..utils import *


# COMMON

class MIS_902:
    """零件破拆 - Part Scrapper
    Lose up to 5 Armor. Your next Mech costs that much less.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_605:
    """质量保证 - Quality Assurance
    Draw 2 Taunt minions.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_606:
    """测试假人 - Testing Dummy
    Taunt Deathrattle: Deal 8 damage randomly split among all enemy minions.
    """
    # Mechanics: DEATHRATTLE, TAUNT
    # TODO: 实现卡牌效果
    pass


class TOY_907:
    """安全护目镜 - Safety Goggles
    Gain 6 Armor. Costs (0) if you don't have any Armor.
    """
    # TODO: 实现卡牌效果
    pass


# RARE

class MIS_705:
    """标准的卡牌包 - Standardized Pack
    Add 5 random Taunt minions to your hand. They are Temporary.
    """
    # TODO: 实现卡牌效果
    pass


class MIS_711:
    """安全专家 - Safety Expert
    Rush. Deathrattle: Shuffle three Bombs into your opponent's deck.
    """
    # Mechanics: DEATHRATTLE, RUSH
    # TODO: 实现卡牌效果
    pass


class TOY_604:
    """砰砰扳手 - Boom Wrench
    [x]Miniaturize Deathrattle: Trigger the Deathrattle of a random friendly Mech.
    """
    # Mechanics: DEATHRATTLE, MINIATURIZE
    # TODO: 实现卡牌效果
    pass


class TOY_651:
    """实验室奴隶主 - Lab Patron
    [x]Whenever you gain Armor,  summon another Lab Patron <i>(once per turn)</i>.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class TOY_908:
    """焰火机师 - Fireworker
    Deathrattle: Summon two 1/1 Boom Bots. <i>WARNING: Bots may explode.</i>
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


# EPIC

class TOY_602:
    """化工泄漏 - Chemical Spill
    Summon the highest Cost minion from your hand, then deal $5 damage to it.
    """
    # TODO: 实现卡牌效果
    pass


class TOY_603:
    """炮灰出动 - Wreck'em and Deck'em
    [x]Choose a friendly Mech. Summon a copy of it that attacks a random enemy, then dies.
    """
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class TOY_607:
    """发明家砰砰 - Inventor Boom
    [x]Battlecry: Resurrect two different friendly Mechs that cost (5) or more. They attack random enemies.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class TOY_906:
    """机械腐面 - Botface
    [x]Taunt After this takes damage, get two random Minis.
    """
    # Mechanics: TAUNT, TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


