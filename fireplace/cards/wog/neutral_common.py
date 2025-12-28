from ..utils import *


##
# Minions


class OG_281:
    """Beckoner of Evil / 邪灵召唤师
    战吼：使你的克苏恩获得+2/+2（无论它在哪里）。"""

    play = Buff(CTHUN, "OG_281e", atk=2, max_health=2)


class OG_283:
    """C'Thun's Chosen / 克苏恩的侍从
    圣盾，战吼：使你的克苏恩获得+3/+3（无论它在哪里）。"""

    play = Buff(CTHUN, "OG_281e", atk=2, max_health=2)


class OG_284:
    """Twilight Geomancer / 暮光地卜师
    嘲讽。战吼：使你的克苏恩获得+1/+1和嘲讽（无论它在哪里）。"""

    play = Buff(CTHUN, "OG_284e")


OG_284e = buff(taunt=True)


class OG_286:
    """Twilight Elder / 暮光尊者
    在你的回合结束时，使你的克苏恩 获得+1/+1（无论它在哪里）。"""

    events = OWN_TURN_END.on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


class OG_138:
    """Nerubian Prophet / 蛛魔先知
    在你的回合开始时，本牌的法力值消耗减少（1）点。"""

    class Hand:
        events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_138e"))


class OG_138e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class OG_150:
    """Aberrant Berserker / 畸变狂战士
    受伤时拥有+2攻 击力。"""

    enrage = Refresh(SELF, buff="OG_150e")


OG_150e = buff(atk=2)


class OG_151:
    """Tentacle of N'Zoth / 恩佐斯的触须
    亡语：对所有随从造成1点伤害。"""

    deathrattle = Hit(ALL_MINIONS, 1)


class OG_156:
    """Bilefin Tidehunter / 怒鳍猎潮者
    战吼：召唤一个1/1并具有嘲讽的软泥怪。"""

    play = Summon(CONTROLLER, "OG_156a")


class OG_158:
    """Zealous Initiate / 狂热的新兵
    亡语：随机使一个友方随从获得+1/+1。"""

    deathrattle = Buff(RANDOM_FRIENDLY_MINION, "OG_158e")


OG_158e = buff(+1, +1)


class OG_249:
    """Infested Tauren / 被感染的牛头人
    嘲讽 亡语：召唤一个2/2的泥浆怪。"""

    deathrattle = Summon(CONTROLLER, "OG_249a")


class OG_256:
    """Spawn of N'Zoth / 恩佐斯的子嗣
    亡语：使你的所有随从获得+1/+1。"""

    deathrattle = Buff(FRIENDLY_MINIONS, "OG_256e")


OG_256e = buff(+1, +1)


class OG_295:
    """Cult Apothecary / 异教药剂师
    战吼：每有一个敌方随从，便为你的英雄恢复#2点生命值。"""

    play = Heal(FRIENDLY_HERO, Count(ENEMY_MINIONS) * 2)


class OG_323:
    """Polluted Hoarder / 被感染的贮藏者
    亡语：抽一张牌。"""

    deathrattle = Draw(CONTROLLER)
