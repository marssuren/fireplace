from ..utils import *


##
# Minions


class GVG_051:
    """Warbot / 战斗机器人
    受伤时拥有+1攻 击力。"""

    enrage = Refresh(SELF, buff="GVG_051e")


GVG_051e = buff(atk=1)


class GVG_053:
    """Shieldmaiden / 盾甲侍女
    战吼： 获得5点护甲值。"""

    play = GainArmor(FRIENDLY_HERO, 5)


class GVG_055:
    """Screwjank Clunker / 废旧螺栓机甲
    战吼：使一个友方机械获得+2/+2。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
    }
    powered_up = Find(FRIENDLY_MINIONS + MECH)
    play = Buff(TARGET, "GVG_055e")


GVG_055e = buff(+2, +2)


class GVG_056:
    """Iron Juggernaut / 钢铁战蝎
    战吼，亡语：将一张“地雷” 牌洗入你对手的牌库。当抽到“地雷”时，便会受到10点伤害。"""

    play = Shuffle(OPPONENT, "GVG_056t")


class GVG_056t:
    """Burrowing Mine"""

    play = Hit(FRIENDLY_HERO, 10)
    draw = CAST_WHEN_DRAWN


class GVG_086:
    """Siege Engine / 重型攻城战车
    每当你获得 护甲值，使本随从获得+1攻击力。"""

    events = GainArmor(FRIENDLY_HERO).on(Buff(SELF, "GVG_086e"))


GVG_086e = buff(atk=1)


##
# Spells


class GVG_050:
    """Bouncing Blade / 弹射之刃
    随机对一个随从造成$1点伤害。重复此效果，直到某个随从死亡。"""

    requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1}
    play = Hit(RANDOM(ALL_MINIONS - IMMUNE - (CURRENT_HEALTH == MIN_HEALTH)), 1).then(
        Dead(Hit.TARGET) | CastSpell("GVG_050")
    )


class GVG_052:
    """Crush / 重碾
    消灭一个随从。如果你控制任何受伤的随从，该法术的法力值消耗减少（4）点。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET)
    cost_mod = Find(FRIENDLY_MINIONS + DAMAGED) & -4


##
# Weapons


class GVG_054:
    """Ogre Warmaul / 食人魔战槌
    50%几率攻击错误的敌人。"""

    events = FORGETFUL
