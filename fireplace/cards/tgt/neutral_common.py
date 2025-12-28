from ..utils import *


##
# Minions


class AT_082:
    """Lowly Squire / 低阶侍从
    激励： 获得+1攻击力。"""

    inspire = Buff(SELF, "AT_082e")


AT_082e = buff(atk=1)


class AT_083:
    """Dragonhawk Rider / 龙鹰骑士
    激励：在本回合中，获得风怒。"""

    inspire = Buff(SELF, "AT_083e")


AT_083e = buff(windfury=True)


class AT_084:
    """Lance Carrier / 持枪侍从
    战吼：使一个友方随从获得+2攻击力。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "AT_084e")


AT_084e = buff(atk=2)


class AT_085:
    """Maiden of the Lake / 湖之仙女
    你的英雄技能的法力值消耗为（1）点。"""

    update = Refresh(FRIENDLY_HERO_POWER, buff="AT_085e")


class AT_085e:
    cost = SET(1)


class AT_089:
    """Boneguard Lieutenant / 白骨卫士军官
    激励： 获得+1生命值。"""

    inspire = Buff(SELF, "AT_089e")


AT_089e = buff(health=1)


class AT_090:
    """Mukla's Champion / 穆克拉的勇士
    激励：使你的其他随从获得+1/+1。"""

    inspire = Buff(FRIENDLY_MINIONS, "AT_090e")


AT_090e = buff(+1, +1)


class AT_091:
    """Tournament Medic / 赛场医师
    激励：为你的英雄恢复#2点生命值。"""

    inspire = Heal(FRIENDLY_HERO, 2)


class AT_094:
    """Flame Juggler / 火焰杂耍者
    战吼：随机对一个敌人造成1点伤害。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 1)


class AT_096:
    """Clockwork Knight / 发条骑士
    战吼：使一个友方机械获得+1/+1。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
    }
    play = Buff(TARGET, "AT_096e")


AT_096e = buff(+1, +1)


class AT_100:
    """Silver Hand Regent / 白银之手教官
    激励：召唤一个1/1的白银之手新兵。"""

    inspire = Summon(CONTROLLER, "CS2_101t")


class AT_103:
    """North Sea Kraken / 北海海怪
    战吼：造成4点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4)


class AT_111:
    """Refreshment Vendor / 零食商贩
    战吼：为每个英雄恢复#4点生命值。"""

    play = Heal(ALL_HEROES, 4)


class AT_119:
    """Kvaldir Raider / 克瓦迪尔劫掠者
    激励：获得+2/+2。"""

    inspire = Buff(SELF, "AT_119e")


AT_119e = buff(+2, +2)


class AT_133:
    """Gadgetzan Jouster / 加基森枪骑士
    战吼：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，则获得+1/+1。"""

    play = JOUST & Buff(SELF, "AT_133e")


AT_133e = buff(+1, +1)
