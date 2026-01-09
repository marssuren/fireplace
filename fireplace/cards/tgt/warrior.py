from ..utils import *


##
# Minions


class AT_066:
    """Orgrimmar Aspirant / 奥格瑞玛狼骑士
    激励：使你的武器获得+1攻击力。"""

    inspire = Buff(FRIENDLY_WEAPON, "AT_066e")


AT_066e = buff(atk=1)


class AT_067:
    """Magnataur Alpha / 猛犸人头领
    同时对其攻击目标相邻的随从造成伤害。"""

    events = Attack(SELF).on(CLEAVE)


class AT_069:
    """Sparring Partner / 格斗陪练师
    嘲讽 战吼：使一个随从获得嘲讽。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Taunt(TARGET)


class AT_071:
    """Alexstrasza's Champion / 阿莱克丝塔萨的勇士
    战吼：如果你的手牌中有龙牌，便获得+1攻击力和冲锋。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "AT_071e")


AT_071e = buff(atk=1, charge=True)


class AT_072:
    """Varian Wrynn / 瓦里安·乌瑞恩
    战吼：抽三张牌。将抽到的随从牌直接置入战场。"""

    play = (Draw(CONTROLLER) * 3).then(
        Find(MINION + Draw.CARD) & Summon(CONTROLLER, Draw.CARD)
    )


class AT_130:
    """Sea Reaver / 破海者
    当你抽到该牌时，对你的随从造成 1点伤害。"""

    draw = Hit(FRIENDLY_MINIONS, 1)


##
# Spells


class AT_064:
    """Bash / 怒袭
    造成$3点伤害。获得3点 护甲值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), GainArmor(FRIENDLY_HERO, 3)


class AT_068:
    """Bolster / 加固
    使你具有嘲讽的随从获得+2/+2。"""

    play = Buff(FRIENDLY_MINIONS + TAUNT, "AT_068e")


AT_068e = buff(+2, +2)


##
# Weapons


class AT_065:
    """King's Defender / 国王护卫者
    战吼：如果你控制任何具有嘲讽的随从，便获得+1耐久度。"""

    play = (Find(FRIENDLY_MINIONS + TAUNT), Buff(SELF, "AT_065e"))


AT_065e = buff(health=1)
