from ..utils import *


##
# Minions


class AT_011:
    """Holy Champion / 神圣勇士
    过量治疗：获得+2攻击力。"""

    events = Heal().on(Buff(SELF, "AT_011e"))


AT_011e = buff(atk=2)


class AT_012:
    """Spawn of Shadows / 暗影子嗣
    战吼，激励：对每个英雄造成4点伤害。"""

    inspire = Hit(ALL_HEROES, 4)


class AT_014:
    """Shadowfiend / 暗影魔
    每当你抽一张牌时，使其法力值消耗减少（1）点。"""

    events = Draw(CONTROLLER).on(Buff(Draw.CARD, "AT_014e"))


class AT_014e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class AT_018:
    """Confessor Paletress / 银色神官帕尔崔丝
    战吼，激励：随机召唤一个传说随从。"""

    inspire = Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))


class AT_116:
    """Wyrmrest Agent / 龙眠教官
    战吼：如果你的手牌中有龙牌，便获得+1攻击力和嘲讽。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "AT_116e")


AT_116e = buff(atk=1, taunt=True)


##
# Spells


class AT_013:
    """Power Word: Glory / 真言术：耀
    选择一个随从。每当其进行攻击，为你的英雄恢复 4点生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "AT_013e")


class AT_013e:
    events = Attack(OWNER).on(Heal(FRIENDLY_HERO, 4))


class AT_015:
    """Convert / 策反
    将一个敌方随从的一张复制置入你的手牌。其法力值消耗为（1）点。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Give(CONTROLLER, Copy(TARGET))


class AT_016:
    """Confuse / 迷乱
    将所有随从的攻击力和生命值 互换。"""

    play = Buff(ALL_MINIONS, "AT_016e")


AT_016e = AttackHealthSwapBuff()


class AT_055:
    """Flash Heal / 快速治疗
    恢复#5点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 5)
