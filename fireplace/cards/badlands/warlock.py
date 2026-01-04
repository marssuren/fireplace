"""
决战荒芜之地 - WARLOCK
"""
from ..utils import *


# COMMON

class DEEP_031:
    """混乱化形 - Chaos Creation
    Deal $6 damage. Summon a random 6-Cost minion. Destroy the bottom 6 cards of your deck.
    """
    # TODO: 实现卡牌效果
    pass


class WW_041:
    """排污助理 - Disposal Assistant
    [x]Battlecry and Deathrattle: Put a Barrel of Sludge on the bottom of your deck.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class WW_042:
    """废物清理工 - Waste Remover
    [x]At the end of your turn, destroy the bottom 3 cards of your deck.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class WW_441:
    """锅炉燃料 - Furnace Fuel
    When this is played, discarded, or destroyed, draw 2 cards.
    """
    # Mechanics: InvisibleDeathrattle
    # TODO: 实现卡牌效果
    pass


# RARE

class DEEP_030:
    """源质晶簇 - Elementium Geode
    Battlecry and Deathrattle: Draw a card. Deal 2 damage to your hero.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class DEEP_032:
    """灵魂冻结 - Soulfreeze
    Freeze a minion and its neighbors. Deal damage to your hero equal to the number Frozen.
    """
    # Mechanics: FREEZE
    # TODO: 实现卡牌效果
    pass


class WW_043:
    """轮式淤泥怪 - Sludge on Wheels
    [x]Rush. Whenever this takes damage, get a Barrel of Sludge and add one to the bottom of your deck.
    """
    # Mechanics: RUSH, TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class WW_092:
    """液力压裂 - Fracking
    [x]Look at the bottom 3 cards of your deck. Draw one and destroy the others.
    """
    # TODO: 实现卡牌效果
    pass


class WW_442:
    """钻拳莫尔葛 - Mo'arg Drillfist
    Taunt  Deathrattle: Excavate a treasure.
    """
    # Mechanics: DEATHRATTLE, EXCAVATE, TAUNT
    # TODO: 实现卡牌效果
    pass


# EPIC

class WW_378:
    """列车烟囱 - Smokestack
    Deal $1 damage to a minion. If it dies, Excavate a treasure.
    """
    # Mechanics: EXCAVATE
    # TODO: 实现卡牌效果
    pass


class WW_436:
    """列车难题 - Trolley Problem
    Discard your lowest Cost spell. Summon two 3/3 Tram Cars with Rush. Quickdraw: Don't discard.
    """
    # Mechanics: QUICKDRAW
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class WW_091:
    """腐臭淤泥波普加 - Pop'gar the Putrid
    Your Fel spells cost (2) less and have Lifesteal. Battlecry: Get two Barrels of Sludge.
    """
    # Mechanics: AURA, BATTLECRY
    # TODO: 实现卡牌效果
    pass


class WW_437:
    """列车司机杰里 - Tram Conductor Gerry
    Battlecry: If you've Excavated twice, summon six 3/3 Tram Cars with Rush.
    """
    # Mechanics: BATTLECRY, EXCAVATE
    # TODO: 实现卡牌效果
    pass


