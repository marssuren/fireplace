from ..utils import *


##
# Minions


class UNG_002:
    """Volcanosaur / 火山龙
    战吼： 连续进化两次。"""

    play = Adapt(SELF) * 2


class UNG_070:
    """Tol'vir Stoneshaper / 托维尔塑石师
    战吼：如果你在上个回合使用过元素牌，则获得嘲讽和圣盾。"""

    play = ELEMENTAL_PLAYED_LAST_TURN & (Buff(SELF, "UNG_070e"), GiveDivineShield(SELF))


UNG_070e = buff(taunt=True)


class UNG_072:
    """Stonehill Defender / 石丘防御者
    嘲讽，战吼： 发现一张具有嘲讽的随从牌。"""

    play = DISCOVER(RandomMinion(taunt=True))


class UNG_075:
    """Vicious Fledgling / 凶恶的翼龙
    在本随从攻击英雄后，进化。"""

    events = Attack(SELF, ALL_HEROES).after(Adapt(SELF))


class UNG_079:
    """Frozen Crusher / 冰冻粉碎者
    在本随从攻击后，冻结本随从。"""

    events = Attack(SELF).after(Freeze(SELF))


class UNG_083:
    """Devilsaur Egg / 魔暴龙蛋
    亡语：召唤一个5/5的魔暴龙。"""

    deathrattle = Summon(CONTROLLER, "UNG_083t1")


class UNG_807:
    """Golakka Crawler / 葛拉卡爬行蟹
    战吼：消灭一个海盗，并获得+1/+1。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 23,
    }
    play = Destroy(TARGET), Buff(SELF, "UNG_807e")


UNG_807e = buff(+2, +2)


class UNG_816:
    """Servant of Kalimos / 卡利莫斯的仆从
    战吼：如果你在上个回合使用过元素牌，则发现一张元素牌。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    play = powered_up & DISCOVER(RandomElemental())
