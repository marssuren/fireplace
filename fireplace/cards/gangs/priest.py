from ..utils import *


##
# Minions


class CFM_020:
    """Raza the Chained / 缚链者拉兹
    战吼：如果你的牌库里没有相同的牌，则在本局对战中，你的英雄技能的法力值消耗为（0）点。"""

    play = Buff(CONTROLLER, "CFM_020e")


class CFM_020e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})


class CFM_605:
    """Drakonid Operative / 龙人侦测者
    战吼： 如果你的手牌中有龙牌，便发现你对手牌库中一张牌的复制。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & GenericChoice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(ENEMY_DECK)) * 3)
    )


class CFM_606:
    """Mana Geode / 法力晶簇
    过量治疗：召唤一个2/2的水晶。"""

    events = Heal(SELF).on(Summon(CONTROLLER, "CFM_606t"))


class CFM_626:
    """Kabal Talonpriest / 暗金教鸦人祭司
    战吼：使一个友方随从获得+3生命值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "CFM_626e")


CFM_626e = buff(health=3)


class CFM_657:
    """Kabal Songstealer / 暗金教窃歌者
    战吼： 沉默一个随从。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Silence(TARGET)


##
# Spells


class CFM_603:
    """Potion of Madness / 疯狂药水
    直到回合结束，获得一个攻击力小于或等于2的敌方随从的控制权。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_TARGET_MAX_ATTACK: 2,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Steal(TARGET), Buff(TARGET, "CFM_603e")


class CFM_603e:
    events = [
        TURN_END.on(Destroy(SELF), Steal(OWNER, OPPONENT)),
        Silence(OWNER).on(Steal(OWNER, OPPONENT)),
    ]
    tags = {GameTag.CHARGE: True}


class CFM_604:
    """Greater Healing Potion / 强效治疗药水
    为一个友方角色恢复#12点生命值。抽一张牌。"""

    requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 12)


class CFM_661:
    """Pint-Size Potion / 缩小药水
    在本回合中，使所有敌方随从获得-3攻击力。"""

    play = Buff(ENEMY_MINIONS, "CFM_661e")


CFM_661e = buff(atk=-3)


class CFM_662:
    """Dragonfire Potion / 龙息药水
    对所有非龙随从造成$5点伤害。"""

    play = Hit(ALL_MINIONS - DRAGON, 5)
