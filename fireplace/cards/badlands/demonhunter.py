"""
决战荒芜之地 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class WW_403:
    """袋底藏沙 - Pocket Sand
    Deal $3 damage. Quickdraw: Your opponent's next card costs (1) more.
    """
    # Mechanics: QUICKDRAW
    # TODO: 实现卡牌效果
    pass


class WW_404:
    """绿洲歹徒 - Oasis Outlaws
    Discover a Naga. If you've played a Naga while holding this, reduce its Cost by (1).
    """
    # Mechanics: DISCOVER
    # TODO: 实现卡牌效果
    pass


class WW_406:
    """午夜啸狼 - Midnight Wolf
    Rush Outcast: Summon a copy of this.
    """
    # Mechanics: OUTCAST, RUSH
    # TODO: 实现卡牌效果
    pass


# RARE

class DEEP_012:
    """影石潜伏者 - Shadestone Skulker
    [x]Rush. Battlecry: Take your  weapon and gain its stats.  Deathrattle: Give it back.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE, RUSH
    # TODO: 实现卡牌效果
    pass


class DEEP_013:
    """邪能陷隙 - Fel Fissure
    Deal $2 damage to all minions. At the start of your next turn, deal $2 more damage to all minions.
    """
    # TODO: 实现卡牌效果
    pass


class WW_405:
    """迅疾连射 - Fan the Hammer
    Deal $6 damage split among the lowest Health enemies.
    """
    # Mechanics: ImmuneToSpellpower
    # TODO: 实现卡牌效果
    pass


class WW_407:
    """焦渴的亡命徒 - Parched Desperado
    Battlecry: If you've cast a spell while holding this, give your hero +3 Attack this turn.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


class WW_409:
    """装填弹膛 - Load the Chamber
    [x]Deal $2 damage. Your next Naga, Fel spell, and weapon cost (1) less.
    """
    # TODO: 实现卡牌效果
    pass


# EPIC

class WW_402:
    """盲眼神射手 - Blindeye Sharpshooter
    [x]After you play a Naga, deal 2 damage to a random enemy and draw a spell. <i>(Then switch!)</i>
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class WW_408:
    """机器调酒师 - Bartend-O-Bot
    Battlecry: Draw an Outcast card and slide it to the left side of your hand.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class WW_400:
    """蛇眼 - Snake Eyes
    [x]Battlecry: Roll two dice, then Discover two cards of those Costs. <i>(Doubles get an extra Discover!)</i>
    """
    # Mechanics: BATTLECRY, DISCOVER
    # TODO: 实现卡牌效果
    pass


class WW_401:
    """枪手库尔特鲁斯 - Gunslinger Kurtrus
    [x]Battlecry: If your deck started with no duplicates, fire six 2 damage shots at minions in the enemy's hand.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


