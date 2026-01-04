"""
深暗领域 - DEATHKNIGHT
"""
from ..utils import *


# COMMON

class GDB_475:
    """近轨血月 - Orbital Moon
    Give a minion Taunt and Lifesteal. If you played an adjacent card this turn, also give it Reborn.
    """
    # TODO: 实现卡牌效果
    pass


class GDB_476:
    """难以喘息 - Suffocate
    Destroy a minion. If you're building a Starship, also destroy a random neighbor.
    """
    # TODO: 实现卡牌效果
    pass


class GDB_478:
    """凋零同化 - Assimilating Blight
    Discover a 3-Cost Deathrattle minion. Summon it with Reborn.
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class SC_001:
    """爆虫冲锋 - Baneling Barrage
    [x]Get a 1/1 Baneling that explodes. If you control a Zerg minion, get another Baneling.
    """
    # TODO: 实现卡牌效果
    pass


# RARE

class GDB_112:
    """魂缚尖塔 - Soulbound Spire
    [x]Deathrattle: Summon a minion with Cost equal to this minion's Attack <i>(up to 10)</i>. Starship Piece
    """
    # Mechanics: DEATHRATTLE, STARSHIP_PIECE
    # TODO: 实现卡牌效果
    pass


class GDB_113:
    """气闸破损 - Airlock Breach
    [x]Summon a 5/5 Undead with Taunt and give your hero +5 Health. Spend 5 Corpses to do it again.
    """
    # TODO: 实现卡牌效果
    pass


class GDB_468:
    """灵魂唤醒者 - Wakener of Souls
    Taunt, Reborn Deathrattle: Resurrect a different friendly Deathrattle minion.
    """
    # Mechanics: DEATHRATTLE, REBORN, TAUNT
    # TODO: 实现卡牌效果
    pass


class SC_002:
    """感染者 - Infestor
    [x]Deathrattle: Your Zerg minions have +1 Attack for the rest of the game.
    """
    # Mechanics: DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class SC_018:
    """飞蛇 - Viper
    [x]Battlecry: Summon a minion from your opponent's hand. Your other Zerg minions gain Reborn and attack it.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


# EPIC

class GDB_106:
    """引航舰首像 - Guiding Figure
    [x]Spellburst: Trigger a random friendly minion's Deathrattle. Starship Piece
    """
    # Mechanics: SPELLBURST, STARSHIP_PIECE
    # TODO: 实现卡牌效果
    pass


class GDB_469:
    """奥金尼亡语者 - Auchenai Death-Speaker
    [x]After another friendly minion is Reborn, summon a copy of it.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class GDB_470:
    """大主教玛拉达尔 - Exarch Maladaar
    Battlecry: The next card you play this turn costs Corpses instead of Mana.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class GDB_477:
    """深暗八爪怪 - The 8 Hands From Beyond
    Battlecry: Destroy both players' decks EXCEPT the 8 highest Cost cards in each.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


