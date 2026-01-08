from ..utils import *


##
# Minions


class AT_028:
    """Shado-Pan Rider / 影踪骁骑兵
    连击： 获得+4攻击力。"""

    combo = Buff(SELF, "AT_028e")


AT_028e = buff(atk=4)


class AT_029:
    """Buccaneer / 锈水海盗
    每当你装备一把武器，使武器获得+1攻击力。"""

    events = Summon(CONTROLLER, FRIENDLY_WEAPON).on(Buff(Summon.CARD, "AT_029e"))


AT_029e = buff(atk=1)


class AT_030:
    """Undercity Valiant / 幽暗城勇士
    连击：造成1点伤害。"""

    requirements = {PlayReq.REQ_TARGET_FOR_COMBO: 0}
    combo = Hit(TARGET, 1)


class AT_031:
    """Cutpurse / 窃贼
    每当本随从攻击英雄时，将幸运币置入你的手牌。"""

    events = Attack(SELF, HERO).on(Give(CONTROLLER, "GAME_005"))


class AT_032:
    """Shady Dealer / 走私商贩
    战吼：如果你控制任何海盗，便获得+1/+1。"""

    powered_up = Find(FRIENDLY_MINIONS + PIRATE)
    play = powered_up & Buff(SELF, "AT_032e")


AT_032e = buff(+1, +1)


class AT_036:
    """Anub'arak / 阿努巴拉克
    亡语：召唤一个4/4并具有“亡语：召唤阿努巴拉克”的蛛魔。"""

    deathrattle = Bounce(SELF), Summon(CONTROLLER, "AT_036t")


##
# Spells


class AT_033:
    """Burgle / 剽窃
    随机获取3张（你对手职业的）卡牌。"""

    play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS)) * 3


class AT_035:
    """Beneath the Grounds / 危机四伏
    将三张伏击牌洗入你对手的牌库。当你的对手抽到该牌，便为你召唤一个4/4的蛛魔。"""

    play = Shuffle(OPPONENT, "AT_035t") * 3


class AT_035t:
    play = Summon(OPPONENT, "AT_036t")
    draw = CAST_WHEN_DRAWN


##
# Weapons


class AT_034:
    """Poisoned Blade / 淬毒利刃
    你的英雄技能不会取代该武器，改为+1攻击力。"""

    inspire = Buff(SELF, "AT_034e")


AT_034e = buff(atk=1)
