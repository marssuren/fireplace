"""
深暗领域 - DRUID
"""
from ..utils import *


# COMMON

class GDB_103:
    """沙塔尔力场 - Sha'tari Cloakfield
    Elusive. Your first spell each turn costs (1) less. Starship Piece
    """
    # Mechanics: AURA, STARSHIP_PIECE
    # TODO: 实现卡牌效果
    pass


class GDB_852:
    """阿肯尼特的启示 - Arkonite Revelation
    Draw a card. If it's a spell, it costs (1) less.
    """
    # TODO: 实现卡牌效果
    pass


class GDB_883:
    """求救信号 - Distress Signal
    [x]Summon two random 2-Cost minions. Refresh 2 Mana Crystals.
    """
    # TODO: 实现卡牌效果
    pass


class SC_755:
    """建造水晶塔 - Construct Pylons
    Your next Protoss card this turn costs (2) less.
    """
    # TODO: 实现卡牌效果
    pass


class SC_756:
    """航母 - Carrier
    [x]At the end of your turn, summon four 4/1 Interceptors that attack random enemies.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


# RARE

class GDB_108:
    """星光反应堆 - Starlight Reactor
    After you cast an Arcane spell, recast it <i>(targets chosen randomly)</i>. Starship Piece
    """
    # Mechanics: STARSHIP_PIECE, TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class GDB_851:
    """星域相变射线 - Astral Phaser
    Choose One - Deal $2 damage to two random enemy minions; or Make one Dormant for 2 turns.
    """
    # Mechanics: CHOOSE_ONE
    # TODO: 实现卡牌效果
    pass


class GDB_855:
    """吞星兽 - Star Grazer
    Elusive, Taunt Spellburst: Give your hero +8 Attack this turn and gain 8 Armor.
    """
    # Mechanics: ELUSIVE, SPELLBURST, TAUNT
    # TODO: 实现卡牌效果
    pass


class SC_763:
    """不朽者 - Immortal
    [x]Taunt, Divine Shield Battlecry: Spend 4 Mana to double this minion's stats.
    """
    # Mechanics: BATTLECRY, DIVINE_SHIELD, TAUNT
    # TODO: 实现卡牌效果
    pass


# EPIC

class GDB_857:
    """究极边境 - Final Frontier
    Discover a 10-Cost minion from the past. Set its Cost to (1).
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class GDB_882:
    """宇宙浑象 - Cosmic Phenomenon
    [x]Summon three 2/3 Elementals with Taunt. If your board is full, give your minions +1/+1.
    """
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class GDB_854:
    """乌鲁，泛天巨兽 - Uluu, the Everdrifter
    [x]Each turn this is in your hand, gain two random Choose One choices.
    """
    # TODO: 实现卡牌效果
    pass


class GDB_856:
    """大主教奥萨尔 - Exarch Othaar
    [x]Battlecry: If you're building a Starship, get 3 different Arcane spells and reduce their Costs by (2).
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


