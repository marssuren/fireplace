from ..utils import *


##
# Minions


class GVG_039:
    """Vitality Totem / 活力图腾
    在你的回合结束时，为你的英雄恢复#4点生命值。"""

    events = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 4))


class GVG_040:
    """Siltfin Spiritwalker / 沙鳞灵魂行者
    每当有其他友方鱼人死亡，便抽一张牌。 过载：（1）"""

    events = Death(FRIENDLY + MURLOC).on(Draw(CONTROLLER))


class GVG_042:
    """Neptulon / 耐普图隆
    战吼：随机将四张鱼人牌置入你的手牌，过载：（3）"""

    play = Give(CONTROLLER, RandomMurloc()) * 4


class GVG_066:
    """Dunemaul Shaman / 砂槌萨满祭司
    风怒，过载：（1） 50%几率攻击错误的敌人。"""

    events = FORGETFUL


##
# Spells


class GVG_029:
    """Ancestor's Call / 先祖召唤
    每个玩家从手牌中随机将一个随从置入战场。"""

    play = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION)),
        Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION)),
    )


class GVG_038:
    """Crackle / 连环爆裂
    造成$3到$6点伤害，过载：（1）"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, RandomNumber(3, 4, 5, 6))


##
# Weapons


class GVG_036:
    """Powermace / 动力战锤
    亡语：随机使一个友方机械获得+2/+2。"""

    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS + MECH), "GVG_036e")


GVG_036e = buff(+2, +2)
