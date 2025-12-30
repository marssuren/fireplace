"""
暗月马戏团 - 牧师
"""
from ..utils import *


##
# Minions

class DMF_053:
    """幸运灵魂 - Fortune Teller
    战吼：如果你在本回合中抽过至少3张牌，便发现一张法术牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    # 简化实现：直接发现
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, cards=SPELL + PRIEST_CLASS))


class DMF_056:
    """纳鲁之光 - Nazmani Bloodweaver
    战吼：如果你在本回合中受到过伤害，便发现一张法术牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    # 简化实现：直接发现
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, cards=SPELL + PRIEST_CLASS))


class DMF_116:
    """血色魔术师 - Blood of G'huun
    嘲讽。战吼：抽一张牌。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 9,
        GameTag.TAUNT: True,
    }
    play = Draw(CONTROLLER)


class DMF_120:
    """暗月兔 - Idol of Y'Shaarj
    战吼：选择一个友方随从。每当你抽一张牌，便召唤一个该随从的复制。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 8,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    # TODO: 实现复杂的抽牌触发召唤机制
    play = Buff(CONTROLLER, "DMF_120e")


class DMF_120e:
    """伊瑟拉的祝福"""
    # 简化实现
    events = Draw(CONTROLLER).after(Summon(CONTROLLER, "DMF_120t"))


class DMF_120t:
    """复制的随从"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


class DMF_121:
    """暗月兔 - The Nameless One
    战吼：选择一个友方随从。每当你抽一张牌，便召唤一个该随从的复制。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Morph(TARGET, RandomMinion(cost=COST(TARGET) - 1))


class DMF_184:
    """暗月兔 - Lightsteed
    战吼：如果你在本回合中恢复过生命值，便获得+2/+2。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    # 简化实现：直接获得buff
    play = Buff(SELF, "DMF_184e")


class DMF_184e:
    """+2/+2"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


##
# Spells

class DMF_054:
    """暗月兔 - Insight
    抽一张牌。如果它的法力值消耗为(3)或更少，则再抽一张。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = Draw(CONTROLLER) * 2  # 简化实现


class DMF_055:
    """暗月兔 - Auspicious Spirits
    召唤一个随机的法力值消耗为(4)的随从。腐蚀：改为(8)。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    play = Summon(CONTROLLER, RandomMinion(cost=4))
    corrupt = Summon(CONTROLLER, RandomMinion(cost=8))


class DMF_186:
    """暗月兔 - Palm Reading
    发现一张法术牌。你手牌中的法术牌在本回合中法力值消耗减少(1)点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = (
        GenericChoice(CONTROLLER, Discover(CONTROLLER, cards=SPELL + PRIEST_CLASS)),
        Buff(CONTROLLER, "DMF_186e"),
    )


class DMF_186e:
    """手牌法术减费"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))


class DMF_187:
    """暗月兔 - Sethekk Veilweaver
    造成2点伤害。如果目标是一个随从，则将一张随机牌置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = (
        Hit(TARGET, 2),
        Find(TARGET + MINION) & Give(CONTROLLER, RandomCollectible()),
    )
