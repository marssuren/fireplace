from ..utils import *


##
# Minions


class UNG_078:
    """Tortollan Forager / 始祖龟劫掠者
    战吼：随机将一张攻击力大于或等于5的随从牌置入你的手牌。"""

    play = Give(CONTROLLER, RandomMinion(atk=range(5, 100)))


class UNG_086:
    """Giant Anaconda / 巨型蟒蛇
    嘲讽。亡语：从你手牌中召唤一个攻击力大于或等于5的随从。"""

    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + (ATK >= 5)))


class UNG_100:
    """Verdant Longneck / 苍绿长颈龙
    战吼：进化。"""

    play = Adapt(SELF)


class UNG_101:
    """Shellshifter / 变形神龟
    抉择：变形成为5/3并具有潜行；或者变形成为3/5并具有嘲讽。"""

    choose = ("UNG_101a", "UNG_101b")
    play = ChooseBoth(CONTROLLER) & Morph(SELF, "UNG_101t3")


class UNG_101a:
    play = Morph(SELF, "UNG_101t")


class UNG_101b:
    play = Morph(SELF, "UNG_101t2")


class UNG_109:
    """Elder Longneck / 年迈的长颈龙
    战吼： 如果你的手牌中有攻击力大于或等于5的随从牌，便获得进化。"""

    play = Find(FRIENDLY_MINIONS + (ATK >= 5)) & Adapt(SELF)


##
# Spells


class UNG_103:
    """Evolving Spores / 生长孢子
    进化你所有的随从。"""

    play = Adapt(FRIENDLY_MINIONS)


class UNG_108:
    """Earthen Scales / 大地之鳞
    使一个友方随从获得+1/+1，然后获得等同于其攻击力的 护甲值。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "UNG_108e").then(GainArmor(FRIENDLY_HERO, ATK(Buff.TARGET)))


UNG_108e = buff(+1, +1)


class UNG_111:
    """Living Mana / 活体法力
    将你所有的法力水晶变成2/2的树人，当它们死亡时恢复你的法力值。"""

    play = (MANA(CONTROLLER) > 0) & (
        FULL_BOARD
        | (
            GainEmptyMana(CONTROLLER, -1),
            Summon(CONTROLLER, "UNG_111t1"),
            Battlecry(SELF, None),
        )
    )


class UNG_111t1:
    deathrattle = GainEmptyMana(CONTROLLER, 1)


class UNG_116:
    """Jungle Giants / 丛林巨兽
    任务：召唤4个攻击力大于或等于5的随从。 奖励：班纳布斯。"""

    progress_total = 5
    quest = Summon(CONTROLLER, MINION + (ATK >= 5)).after(
        AddProgress(SELF, Summon.CARD)
    )
    reward = Give(CONTROLLER, "UNG_116t")


class UNG_116t:
    play = Buff(FRIENDLY_DECK + MINION, "UNG_116te")


class UNG_116te:
    cost = SET(0)
    events = REMOVED_IN_PLAY
