from ..utils import *


##
# Minions


class GVG_006:
    """Mechwarper / 机械跃迁者
    你的机械的法力值消耗减少（1）点。"""

    update = Refresh(FRIENDLY_HAND + MECH, {GameTag.COST: -1})


class GVG_013:
    """Cogmaster / 齿轮大师
    如果你控制任何机械，便拥有 +2攻击力。"""

    update = Find(FRIENDLY_MINIONS + MECH) & Refresh(SELF, {GameTag.ATK: +2})


class GVG_065:
    """Ogre Brute / 食人魔步兵
    50%几率攻击错误的敌人。"""

    events = FORGETFUL


class GVG_067:
    """Stonesplinter Trogg / 碎石穴居人
    每当你的对手施放一个法术，便获得+1攻击力。"""

    events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_067a"))


GVG_067a = buff(atk=1)


class GVG_068:
    """Burly Rockjaw Trogg / 石腭穴居人壮汉
    每当你的对手施放一个法术，获得 +2攻击力。"""

    events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_068a"))


GVG_068a = buff(atk=2)


class GVG_069:
    """Antique Healbot / 老式治疗机器人
    战吼：为你的英雄恢复#8点生命值。"""

    play = Heal(FRIENDLY_HERO, 8)


class GVG_075:
    """Ship's Cannon / 船载火炮
    在你召唤一个海盗后，随机对一个敌人造成2点伤害。"""

    events = Summon(CONTROLLER, PIRATE).on(Hit(RANDOM_ENEMY_CHARACTER, 2))


class GVG_076:
    """Explosive Sheep / 自爆绵羊
    亡语：对所有随从造成2点伤害。"""

    deathrattle = Hit(ALL_MINIONS, 2)


class GVG_078:
    """Mechanical Yeti / 机械雪人
    亡语：使每个玩家获得一张零件牌。"""

    deathrattle = Give(ALL_PLAYERS, RandomSparePart())


class GVG_082:
    """Clockwork Gnome / 发条侏儒
    亡语：将一张零件牌置入你的手牌。"""

    deathrattle = Give(CONTROLLER, RandomSparePart())


class GVG_090:
    """Madder Bomber / 疯狂爆破者
    战吼：造成6点伤害，随机分配到所有其他角色身上。"""

    play = Hit(RANDOM_OTHER_CHARACTER, 1) * 6


class GVG_096:
    """Piloted Shredder / 载人收割机
    亡语：随机召唤一个法力值消耗为（2）的随从。"""

    deathrattle = Summon(CONTROLLER, RandomMinion(cost=2))


class GVG_102:
    """Tinkertown Technician / 工匠镇技师
    战吼：如果你控制一个机械，便获得+1/+1并将一张零件牌置入你的手牌。"""

    powered_up = Find(FRIENDLY_MINIONS + MECH)
    play = powered_up & (Buff(SELF, "GVG_102e"), Give(CONTROLLER, RandomSparePart()))


GVG_102e = buff(+1, +1)


class GVG_103:
    """Micro Machine / 微型战斗机甲
    在每个回合开始时，获得+1攻击力。"""

    # That card ID is not a mistake
    events = TURN_BEGIN.on(Buff(SELF, "GVG_076a"))


GVG_076a = buff(atk=1)
