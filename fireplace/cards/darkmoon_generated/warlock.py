"""
暗月马戏团 - 术士
"""
from ..utils import *


##
# Minions

class DMF_110:
    """自由飞翔 - Free Admission
    嘲讽。战吼：你每控制一个恶魔，便获得+1/+1。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.TAUNT: True,
    }
    play = Buff(SELF, "DMF_110e") * Count(FRIENDLY_MINIONS + DEMON)


class DMF_110e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class DMF_111:
    """自由飞翔 - Wriggling Horror
    战吼：抽一张牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
    }
    play = Draw(CONTROLLER)


class DMF_114:
    """自由飞翔 - Man'ari Mosher
    嘲讽。每当本随从受到伤害，便随机对一个敌方随从造成等量的伤害。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.TAUNT: True,
    }
    events = Damage(SELF).on(
        Hit(RANDOM(ENEMY_MINIONS), Count(EVENT_DAMAGE))
    )


class DMF_115:
    """自由飞翔 - Midway Maniac
    战吼：你每控制一个恶魔，便对你的英雄造成1点伤害。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 5,
        GameTag.COST: 2,
    }
    play = Hit(FRIENDLY_HERO, 1) * Count(FRIENDLY_MINIONS + DEMON)


class DMF_118:
    """自由飞翔 - Deck of Chaos
    战吼：摧毁一个法力水晶。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    play = DestroyManaCrystal(CONTROLLER)


class DMF_533:
    """自由飞翔 - Tickatus
    战吼：移除对手牌库顶的五张牌。腐蚀：改为十张。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 6,
    }
    play = Mill(OPPONENT) * 5
    corrupt = Mill(OPPONENT) * 10


##
# Spells

class DMF_113:
    """自由飞翔 - Cascading Disaster
    消灭一个随机敌方随从。重复，直到你的手牌中没有法术牌为止。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    # 简化实现：消灭1个随机敌方随从
    play = Destroy(RANDOM(ENEMY_MINIONS))


class DMF_117:
    """自由飞翔 - Revenant Rascal
    战吼：摧毁一个法力水晶。亡语：恢复一个法力水晶。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3)


class DMF_119:
    """自由飞翔 - Felosophy
    复制你手牌中的一张恶魔牌。腐蚀：改为复制所有恶魔牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY_HAND + MINION + DEMON)))
    corrupt = Give(CONTROLLER, Copy(FRIENDLY_HAND + MINION + DEMON))


class DMF_534:
    """自由飞翔 - Ring Matron
    嘲讽。战吼：召唤两个1/1的小鬼。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = (
        DestroyManaCrystal(CONTROLLER),
        Shuffle(FRIENDLY_DECK, RandomMinion()),
        Shuffle(FRIENDLY_DECK, RandomSpell()),
    )
