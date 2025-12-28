from ..utils import *


##
# Minions


class OG_149:
    """Ravaging Ghoul / 暴虐食尸鬼
    战吼：对所有其他随从造成1点伤害。"""

    play = Hit(ALL_MINIONS, 1)


class OG_218:
    """Bloodhoof Brave / 血蹄勇士
    嘲讽 受伤时拥有+3攻 击力。"""

    enrage = Refresh(SELF, buff="OG_218e")


OG_218e = buff(atk=3)


class OG_220:
    """Malkorok / 马尔考罗克
    战吼：随机装备一把武器。"""

    play = Summon(CONTROLLER, RandomWeapon())


class OG_312:
    """N'Zoth's First Mate / 恩佐斯的副官
    战吼：装备一把1/3的锈蚀铁钩。"""

    play = Summon(CONTROLLER, "OG_058")


class OG_315:
    """Bloodsail Cultist / 血帆教徒
    战吼：如果你控制着其他海盗，使你的武器获得+1/+1。"""

    play = Find(FRIENDLY_MINIONS + PIRATE - SELF) & Buff(FRIENDLY_WEAPON, "OG_315e")


OG_315e = buff(+1, +1)


class OG_301:
    """Ancient Shieldbearer / 上古之神护卫
    战吼： 如果你的克苏恩至少有10点攻击力，则获得10点护甲值。"""

    play = CHECK_CTHUN & GainArmor(FRIENDLY_HERO, 10)


##
# Spells


class OG_276:
    """Blood Warriors / 苦战傀儡
    将每个受伤的友方随从的各一张复制置入你的手牌。"""

    play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS + DAMAGED))


class OG_314:
    """Blood To Ichor / 化血为脓
    对一个随从造成$1点伤害，如果它依然存活，则召唤一个2/2的泥浆怪。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1), Dead(TARGET) | Summon(CONTROLLER, "OG_314b")


##
# Weapons


class OG_033:
    """Tentacles for Arms / 钢铁触须
    亡语：将这把武器移回你的手牌。"""

    deathrattle = Bounce(SELF)
