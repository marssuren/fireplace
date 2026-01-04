"""
漫游翡翠梦境 - PALADIN
"""
from ..utils import *


# COMMON

class EDR_255:
    """复苏烈焰 - Renewing Flames
    Lifesteal. Deal $5 damage to the lowest Health enemy, twice.
    """
    # Mechanics: LIFESTEAL
    # TODO: 实现卡牌效果
    pass


class EDR_257:
    """圣光抚愈者 - Lightmender
    [x]Taunt. Choose One - +3 Attack and Divine Shield;  or +3 Health and Lifesteal.
    """
    # Mechanics: CHOOSE_ONE, TAUNT
    # TODO: 实现卡牌效果
    pass


class EDR_451:
    """金萼幼龙 - Goldpetal Drake
    [x]Battlecry and Deathrattle: Imbue your Hero Power.
    """
    # Mechanics: BATTLECRY, DEATHRATTLE
    # TODO: 实现卡牌效果
    pass


class FIR_914:
    """焚火之力 - Smoldering Strength
    Give a friendly minion +{0}/+{0}. <i>(Upgrades each turn, but discards after {1}!)</i>1Give a friendly minion +{0}/+{0}. <i>(Discards this turn!)</i>
    """
    # TODO: 实现卡牌效果
    pass


class FIR_941:
    """烧灼映像 - Searing Reflection
    Draw a minion. Summon an 8/8 copy of it with Divine Shield.
    """
    # TODO: 实现卡牌效果
    pass


# RARE

class EDR_251:
    """龙鳞军备 - Dragonscale Armaments
    Draw a spell that started in your deck and one that didn't.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_253:
    """巨熊之槌 - Ursine Maul
    After your hero attacks, draw your highest Cost card.
    """
    # Mechanics: TRIGGER_VISUAL
    # TODO: 实现卡牌效果
    pass


class EDR_264:
    """圣光护盾 - Aegis of Light
    Summon a random 2-Cost minion and give it Taunt. Imbue your Hero Power.
    """
    # TODO: 实现卡牌效果
    pass


class FIR_961:
    """灰叶树精 - Ashleaf Pixie
    Battlecry: If you're holding a spell that costs (5) or more, gain Divine Shield and Lifesteal.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


# EPIC

class EDR_252:
    """乌索尔印记 - Mark of Ursol
    [x]Choose a minion. If it's an enemy, set its stats to 1/1. If it's friendly, set its stats to 3/3 instead.
    """
    # TODO: 实现卡牌效果
    pass


class EDR_256:
    """梦境卫士 - Dreamwarden
    [x]Taunt. Battlecry: If there is a card in your deck that didn't start there, draw it and gain +2/+2.
    """
    # Mechanics: BATTLECRY, TAUNT
    # TODO: 实现卡牌效果
    pass


# LEGENDARY

class EDR_258:
    """坚韧的托雷斯 - Toreth the Unbreaking
    [x]Divine Shield, Taunt Your Divine Shields take three hits to break.
    """
    # Mechanics: AURA, DIVINE_SHIELD, TAUNT
    # TODO: 实现卡牌效果
    pass


class EDR_259:
    """乌索尔 - Ursol
    [x]Battlecry: Cast the highest Cost spell from your hand as  an Aura that lasts 3 turns.
    """
    # Mechanics: BATTLECRY
    # TODO: 实现卡牌效果
    pass


