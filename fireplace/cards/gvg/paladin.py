from ..utils import *


##
# Minions


class GVG_060:
    """Quartermaster / 军需官
    战吼：使你的白银之手新兵获得+2/+2。"""

    play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "GVG_060e")


GVG_060e = buff(+2, +2)


class GVG_062:
    """Cobalt Guardian / 钴制卫士
    每当你召唤一个机械，便获得圣盾。"""

    events = Summon(CONTROLLER, MECH).on(GiveDivineShield(SELF))


class GVG_063:
    """Bolvar Fordragon / 伯瓦尔·弗塔根
    如果这张牌在你的手牌中，每当一个友方随从死亡，便获得+1攻击力。"""

    class Hand:
        events = Death(FRIENDLY + MINION).on(Buff(SELF, "GVG_063a"))


GVG_063a = buff(atk=1)


class GVG_101:
    """Scarlet Purifier / 血色净化者
    战吼： 对所有具有亡语的随从造成2点伤害。"""

    play = Hit(ALL_MINIONS + DEATHRATTLE, 2)


##
# Spells


class GVG_057:
    """Seal of Light / 光明圣印
    为你的英雄恢复#4点生命值，并在本回合中 获得+2攻击力。"""

    play = Heal(FRIENDLY_HERO, 4), Buff(FRIENDLY_HERO, "GVG_057a")


GVG_057a = buff(atk=2)


class GVG_061:
    """Muster for Battle / 作战动员
    召唤三个1/1的白银之手新兵，装备一把1/4的武器。"""

    play = Summon(CONTROLLER, "CS2_101t") * 3, Summon(CONTROLLER, "CS2_091")


##
# Weapons


class GVG_059:
    """Coghammer / 齿轮光锤
    战吼：随机使一个友方随从获得圣盾和嘲讽。"""

    play = SetTags(RANDOM_FRIENDLY_MINION, (GameTag.TAUNT, GameTag.DIVINE_SHIELD))
