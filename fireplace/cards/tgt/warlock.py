from ..utils import *


##
# Minions


class AT_019:
    """Dreadsteed / 恐惧战马
    亡语： 在回合结束时，召唤一匹恐惧战马。"""

    deathrattle = Buff(CONTROLLER, "AT_019e")


class AT_019e:
    events = OWN_TURN_END.on(Summon(CONTROLLER, "AT_019"), Destroy(SELF))


class AT_021:
    """Tiny Knight of Evil / 小鬼骑士
    每当你弃掉一张牌时，便获得+2/+1。"""

    events = Discard(FRIENDLY).on(Buff(SELF, "AT_021e"))


AT_021e = buff(atk=2, health=1)


class AT_023:
    """Void Crusher / 虚空碾压者
    激励：随机消灭每个玩家的一个随从。"""

    inspire = Destroy(RANDOM_ENEMY_MINION | RANDOM_FRIENDLY_MINION)


class AT_026:
    """Wrathguard / 愤怒卫士
    每当本随从受到伤害，对你的英雄造成等量的伤害。"""

    events = Damage(SELF).on(Hit(FRIENDLY_HERO, Damage.AMOUNT))


class AT_027:
    """Wilfred Fizzlebang / 威尔弗雷德·菲兹班
    你通过英雄技能抽到的卡牌，其法力值消耗为（0）点。"""

    events = Draw(CONTROLLER, None, FRIENDLY_HERO_POWER).on(Buff(Draw.CARD, "AT_027e"))


class AT_027e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


##
# Spells


class AT_022:
    """Fist of Jaraxxus / 加拉克苏斯之拳
    当你使用或弃掉这张牌时，随机对一个敌人造成$4点伤害。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 4)
    discard = Hit(RANDOM_ENEMY_CHARACTER, 4)


class AT_024:
    """Demonfuse / 恶魔融合
    使一个恶魔获得+3/+3。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 15,
    }
    play = Buff(TARGET, "AT_024e"), GainMana(OPPONENT, 1)


AT_024e = buff(+3, +3)


class AT_025:
    """Dark Bargain / 黑暗交易
    随机消灭两个敌方随从，随机弃两张牌。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Destroy(RANDOM_ENEMY_MINION * 2), Discard(RANDOM(FRIENDLY_HAND) * 2)
