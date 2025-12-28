from ..utils import *


##
# Minions


class OG_051:
    """Forbidden Ancient / 禁忌古树
    战吼：消耗你所有的法力值，每消耗一点法力值，便获得+1/+1。"""

    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
        Buff(SELF, "OG_051e") * SpendMana.AMOUNT
    )


OG_051e = buff(+1, +1)


class OG_044:
    """Fandral Staghelm / 范达尔·鹿盔
    你的抉择牌和英雄技能可以同时拥有两种效果。"""

    update = Refresh(
        CONTROLLER,
        {
            GameTag.CHOOSE_BOTH: True,
        },
    )


class OG_202:
    """Mire Keeper / 泥潭守护者
    抉择：召唤一个2/2的泥浆怪；或者获得一个空的法力水晶。"""

    choose = ("OG_202a", "OG_202b")
    play = ChooseBoth(CONTROLLER) & (
        Summon(CONTROLLER, "OG_202c"),
        AT_MAX_MANA(CONTROLLER) | GainEmptyMana(CONTROLLER, 1),
    )


class OG_202a:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 2,
    }
    play = Summon(CONTROLLER, "OG_202c")


class OG_202b:
    play = AT_MAX_MANA(CONTROLLER) | GainEmptyMana(CONTROLLER, 1)


class OG_313:
    """Addled Grizzly / 腐化灰熊
    在你召唤一只野兽后，使其获得+1/+1。"""

    events = Summon(CONTROLLER, MINION).after(Buff(Summon.CARD, "OG_313e"))


OG_313e = buff(+1, +1)


class OG_188:
    """Klaxxi Amber-Weaver / 卡拉克西织珀者
    嘲讽。战吼： 如果你的克苏恩至少有10点攻击力，便获得+5生命值。"""

    play = CHECK_CTHUN & Buff(SELF, "OG_188e")


OG_188e = buff(health=4)


class OG_293:
    """Dark Arakkoa / 黑暗鸦人
    嘲讽，战吼：使你的克苏恩获得+4/+4（无论它在哪里）。"""

    play = Buff(CTHUN, "OG_281e", atk=3, max_health=3)


##
# Spells


class OG_047:
    """Feral Rage / 野性之怒
    抉择：使你的英雄在本回合中获得+4攻击力；或者获得8点护甲值。"""

    choose = ("OG_047a", "OG_047b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(FRIENDLY_HERO, "OG_047e"),
        GainArmor(FRIENDLY_HERO, 8),
    )


class OG_047a:
    play = Buff(FRIENDLY_HERO, "OG_047e")


OG_047e = buff(atk=4)


class OG_047b:
    play = GainArmor(FRIENDLY_HERO, 8)


class OG_048:
    """Mark of Y'Shaarj / 亚煞极印记
    使一个随从获得+2/+2。 如果该随从是野兽，抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "OG_048e").then(Find(Buff.TARGET + BEAST) & Draw(CONTROLLER))


OG_048e = buff(+2, +2)


class OG_195:
    """Wisps of the Old Gods / 上古之神的小精灵
    抉择：召唤七个1/1的小精灵；或者使你的所有随从获得+2/+2。"""

    choose = ("OG_195a", "OG_195b")
    play = ChooseBoth(CONTROLLER) & (
        Summon(CONTROLLER, "OG_195c") * 7,
        Buff(FRIENDLY_MINIONS, "OG_195e"),
    )


class OG_195a:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "OG_195c") * 7


class OG_195b:
    play = Buff(FRIENDLY_MINIONS, "OG_195e")


OG_195e = buff(+2, +2)
