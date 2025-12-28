from ..utils import *


##
# Minions


class AT_017:
    """Twilight Guardian / 暮光守护者
    战吼：如果你的手牌中有龙牌，便获得+1攻击力和嘲讽。"""

    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "AT_017e")


AT_017e = buff(atk=1, taunt=True)


class AT_080:
    """Garrison Commander / 要塞指挥官
    每个回合你可以使用两次英雄技能。"""

    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: 1})


class AT_098:
    """Sideshow Spelleater / 杂耍吞法者
    战吼：复制对手的英雄技能。"""

    play = Summon(CONTROLLER, Copy(ENEMY_HERO_POWER))


class AT_099:
    """Kodorider / 科多兽骑手
    激励：召唤一个3/5的作战科多兽。"""

    inspire = Summon(CONTROLLER, "AT_099t")


class AT_113:
    """Recruiter / 征募官
    激励：将一个2/2的侍从置入你的手牌。"""

    inspire = Give(CONTROLLER, "CS2_152")


class AT_117:
    """Master of Ceremonies / 庆典司仪
    战吼：如果你控制任何具有法术伤害的随从，便获得+2/+2。"""

    powered_up = Find(FRIENDLY_MINIONS + SPELLPOWER)
    play = powered_up & Buff(SELF, "AT_117e")


AT_117e = buff(+2, +2)


class AT_118:
    """Grand Crusader / 十字军统领
    战吼： 随机将一张圣骑士牌置入你的手牌。"""

    play = Give(CONTROLLER, RandomCollectible(card_class=CardClass.PALADIN))


class AT_120:
    """Frost Giant / 冰霜巨人
    在本局对战中，你每使用一次英雄技能，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Attr(CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME)


class AT_121:
    """Crowd Favorite / 人气选手
    每当你使用一张具有战吼的牌，便获得+1/+1。"""

    events = Play(CONTROLLER, BATTLECRY).on(Buff(SELF, "AT_121e"))


AT_121e = buff(+1, +1)
