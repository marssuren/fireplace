"""
暗月马戏团 - 萨满
"""
from ..utils import *


##
# Minions

class DMF_703:
    """大图腾埃索 - Grand Totem Eys'or
    在你的回合结束时，使你手牌、牌库和战场上的所有其他图腾获得+1/+1。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.TOTEM,
    }
    
    # 回合结束时，给所有其他图腾+1/+1
    events = OWN_TURN_END.on(
        Buff(FRIENDLY_MINIONS + TOTEM - SELF, "DMF_703e"),  # 战场上的其他图腾
        Buff(FRIENDLY_HAND + TOTEM, "DMF_703e"),             # 手牌中的图腾
        Buff(FRIENDLY_DECK + TOTEM, "DMF_703e"),             # 牌库中的图腾
    )


class DMF_703e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class DMF_704:
    """旋转木马狮鹫 - Cagematch Custodian
    战吼：抽一张武器牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)


class DMF_707:
    """投球游戏 - Dunk Tank
    造成4点伤害。腐蚀：然后对所有敌方随从造成2点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)
    corrupt = Hit(ENEMY_MINIONS, 2)


class DMF_708:
    """雷霆绽放图腾 - Totem Goliath
    过载：(1)。亡语：召唤所有四个基础图腾。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.OVERLOAD: 1,
    }
    deathrattle = (
        Summon(CONTROLLER, "CS2_050"),  # Stoneclaw Totem
        Summon(CONTROLLER, "CS2_051"),  # Wrath of Air Totem
        Summon(CONTROLLER, "CS2_052"),  # Searing Totem
        Summon(CONTROLLER, "NEW1_009"),  # Healing Totem
    )


class DMF_709:
    """竞技场主管 - Pit Master
    战吼：召唤一个3/2的决斗者。腐蚀：改为召唤两个。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    play = Summon(CONTROLLER, "DMF_709t")
    corrupt = Summon(CONTROLLER, "DMF_709t") * 2


class DMF_709t:
    """决斗者 - Duelist"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }


##
# Spells

class DMF_700:
    """雷霆打击 - Stormstrike
    造成3点伤害。使你的英雄在本回合中获得+3攻击力。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (Hit(TARGET, 3), Buff(FRIENDLY_HERO, "DMF_700e"))


class DMF_700e:
    """+3攻击力"""
    tags = {
        GameTag.ATK: 3,
        GameTag.ONE_TURN_EFFECT: True,
    }


class DMF_701:
    """打地鼠锤 - Whack-A-Gnoll Hammer
    在你的英雄攻击后，随机使一个友方随从获得+1/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 2,
        GameTag.COST: 2,
    }
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_MINIONS), "DMF_701e")
    )


class DMF_701e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


# DMF_702 已在前面实现为 DMF_707（投球游戏）


class DMF_706:
    """图腾召唤 - Grand Totem Eys'or
    召唤一个随机的基础图腾。过载：(1)。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.OVERLOAD: 1,
    }
    play = Summon(CONTROLLER, RandomTotem())


class DMF_705:
    """伊纳拉·风暴 - Inara Stormcrash
    过载：(10)。使你的所有随从获得+5/+5。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
        GameTag.OVERLOAD: 10,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    play = Buff(FRIENDLY_MINIONS, "DMF_705e")


class DMF_705e:
    """+5/+5"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }


##
# Weapons

class YOP_023:
    """打地鼠锤 - Whack-A-Gnoll-Hammer
    在你的英雄攻击后，对一个随机敌人造成2点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 2,
        GameTag.COST: 3,
    }
    events = Attack(FRIENDLY_HERO).after(
        Hit(RANDOM_ENEMY_CHARACTER, 2)
    )


class YOP_024:
    """决斗场馆 - Deathmatch Pavilion
    在你的英雄攻击后，召唤一个随机的基础图腾。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 3,
        GameTag.COST: 2,
    }
    events = Attack(FRIENDLY_HERO).after(
        Summon(CONTROLLER, RandomTotem())
    )
