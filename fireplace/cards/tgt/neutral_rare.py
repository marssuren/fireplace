from ..utils import *


##
# Minions


class AT_086:
    """Saboteur / 破坏者
    战吼：下个回合敌方英雄技能的法力值消耗增加（5）点。"""

    play = Buff(OPPONENT, "AT_086e")


class AT_086e:
    update = CurrentPlayer(OWNER) & Refresh(ENEMY_HERO_POWER, {GameTag.COST: +5})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class AT_088:
    """Mogor's Champion / 穆戈尔的勇士
    50%几率攻击错误的敌人。"""

    events = FORGETFUL


class AT_105:
    """Injured Kvaldir / 受伤的克瓦迪尔
    战吼：对自身造成3点伤害。"""

    play = Hit(SELF, 3)


class AT_106:
    """Light's Champion / 圣光勇士
    战吼： 沉默一个恶魔。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 15,
    }
    play = Silence(TARGET)


class AT_108:
    """Armored Warhorse / 重甲战马
    战吼：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，则获得冲锋。"""

    play = JOUST & GiveCharge(SELF)


class AT_109:
    """Argent Watchman / 银色警卫
    无法攻击。 激励：在本回合中可正常进行攻击。"""

    inspire = Buff(SELF, "AT_109e")


AT_109e = buff(cant_attack=False)


class AT_110:
    """Coliseum Manager / 角斗场主管
    激励：将本随从移回你的手牌。"""

    inspire = Bounce(SELF)


class AT_112:
    """Master Jouster / 大师级枪骑士
    战吼：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，则获得嘲讽和圣盾。"""

    play = JOUST & SetTags(SELF, (GameTag.TAUNT, GameTag.DIVINE_SHIELD))


class AT_115:
    """Fencing Coach / 击剑教头
    战吼：你的下一个英雄技能的法力值消耗减少（2）点。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(CONTROLLER, "AT_115e")


class AT_115e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: -2})
    events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))
