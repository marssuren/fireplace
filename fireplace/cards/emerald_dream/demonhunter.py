"""
漫游翡翠梦境 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class EDR_840:
    """恐怖收割 - Grim Harvest
    Draw a card. Summon a random Dormant Dreadseed.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_842:
    """亵渎之矛 - Defiled Spear
    [x]After your hero attacks an  enemy, deal your hero's Attack damage to another random enemy.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class EDR_890:
    """梦魇龙裔 - Nightmare Dragonkin
    Deathrattle: Reduce the Cost of the right-most card in your hand by (2).
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class FIR_952:
    """灼热掠夺者 - Scorchreaver
    [x]Battlecry: Discover a Fel spell. Reduce the Cost of Fel spells in your hand by (1).
    """
    # Mechanics: BATTLECRY, DISCOVER
    # TODO: 实现卡牌效果
    pass


# RARE

class EDR_841:
    """恐魂腐蚀者 - Dreadsoul Corrupter
    [x]Battlecry and Deathrattle: Summon a random Dormant Dreadseed.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class EDR_882:
    """跳脸惊吓 - Jumpscare!
    Discover a Demon that costs (5) or more with a Dark Gift. Shuffle the other two into your deck.
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class EDR_891:
    """贪婪的地狱猎犬 - Ravenous Felhunter
    Deathrattle: Resurrect a friendly Deathrattle minion that costs (4) or less. Summon a copy of it.
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class FIR_904:
    """邪火爆焰 - Felfire Blaze
    [x]After you cast a Fel spell, destroy this and deal 2 damage to all enemies.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


# EPIC

class EDR_820:
    """飞龙之眠 - Wyvern's Slumber
    Choose One - Summon two Dormant Dreadseeds; or Deal $2 damage to all minions.
    """
    # Mechanics: CHOOSE_ONE
    # TODO: 实现卡牌效果
    pass


class EDR_892:
    """残暴的魔蝠 - Ferocious Felbat
    [x]Deathrattle: Resurrect a different friendly Deathrattle minion that costs (5) or more. Summon a copy of it.
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class FIR_902:
    """燃薪咒符 - Sigil of Cinder
    [x]At the start of your next turn, deal $6 damage randomly split among all enemies.
    """
    # Mechanics: ImmuneToSpellpower
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class EDR_421:
    """年兽 - Omen
    [x]Rush, Windfury Deathrattle: Deal 1 damage to all enemies. <i>(Improves after this attacks!)</i>
    """
    # Mechanics: DEATHRATTLE, RUSH, WINDFURY
    # TODO: 实现卡牌效果
    pass


class EDR_493:
    """阿莱纳希 - Alara'shi
    [x]Battlecry: Transform minions in your hand into random Demons. <i>(They keep their   original stats and Cost.)</I>
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


