from ..utils import *


##
# Minions


class AT_038:
    """Darnassus Aspirant / 达纳苏斯豹骑士
    战吼：获得一个空的法力水晶。 亡语：失去一个法力水晶。"""

    play = GainEmptyMana(CONTROLLER, 1)
    deathrattle = GainMana(CONTROLLER, -1)


class AT_039:
    """Savage Combatant / 狂野争斗者
    激励：在本回合中，使你的英雄获得+2攻击力。"""

    inspire = Buff(FRIENDLY_HERO, "AT_039e")


AT_039e = buff(atk=2)


class AT_040:
    """Wildwalker / 荒野行者
    战吼：使一个友方野兽获得+3生命值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Buff(TARGET, "AT_040e")


AT_040e = buff(health=3)


class AT_041:
    """Knight of the Wild / 荒野骑士
    在本局对战中，你每召唤过一只野兽，本牌的法力值消耗便减少（1）点。"""

    class Hand:
        events = Summon(CONTROLLER, BEAST).on(Buff(SELF, "AT_041e"))


class AT_041e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class AT_042:
    """Druid of the Saber / 刃牙德鲁伊
    抉择：变形成为2/1并具有冲锋；或者变形成为3/2并具有潜行。"""

    choose = ("AT_042a", "AT_042b")
    play = ChooseBoth(CONTROLLER) & Morph(SELF, "OG_044c")


class AT_042a:
    play = Morph(SELF, "AT_042t")


class AT_042b:
    play = Morph(SELF, "AT_042t2")


class AT_045:
    """Aviana / 艾维娜
    你的随从牌的法力值消耗为（1）点。"""

    update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: SET(1)})


##
# Spells


class AT_037:
    """Living Roots / 活体根须
    抉择：造成$2点伤害；或者召唤两个1/1的树苗。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    choose = ("AT_037a", "AT_037b")
    play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Summon(CONTROLLER, "AT_037t") * 2)


class AT_037a:
    play = Hit(TARGET, 2)
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}


class AT_037b:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "AT_037t") * 2


class AT_043:
    """Astral Communion / 星界沟通
    获得十个法力水晶。弃掉 你的手牌。"""

    play = Discard(FRIENDLY_HAND), (
        AT_MAX_MANA(CONTROLLER) & Give(CONTROLLER, "CS2_013t")
        | GainMana(CONTROLLER, 10)
    )


class AT_044:
    """Mulch / 腐根
    消灭一个随从。随机将一张随从牌置入对手的手牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), Give(OPPONENT, RandomMinion())
