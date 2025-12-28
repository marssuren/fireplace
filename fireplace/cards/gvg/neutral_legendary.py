from ..utils import *


##
# Minions


class GVG_110:
    """Dr. Boom / 砰砰博士
    战吼： 召唤两个1/1的砰砰机器人。警告：该机器人随时可能爆炸。"""

    play = SummonBothSides(CONTROLLER, "GVG_110t") * 2


class GVG_110t:
    """Boom Bot"""

    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, RandomNumber(1, 2, 3, 4))


class GVG_111:
    """Mimiron's Head / 米米尔隆的头部
    在你的回合开始时，如果你控制至少三个机械，则消灭这些机械，并将其组合成V-07-TR-0N。"""

    events = OWN_TURN_BEGIN.on(
        (Count(FRIENDLY_MINIONS + MECH) >= 3)
        & (Destroy(FRIENDLY_MINIONS + MECH), Deaths(), Summon(CONTROLLER, "GVG_111t"))
    )


class GVG_111t:
    tags = {GameTag.MEGA_WINDFURY: True}


class GVG_112:
    """Mogor the Ogre / 食人魔勇士穆戈尔
    所有随从有50%几率攻击错误的敌人。"""

    events = Attack(MINION).on(
        COINFLIP
        & Retarget(
            Attack.ATTACKER,
            RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(Attack.ATTACKER)),
        )
    )


class GVG_113:
    """Foe Reaper 4000 / 死神4000型
    同时对其攻击目标相邻的随从造成伤害。"""

    events = Attack(SELF).on(CLEAVE)


class GVG_114:
    """Sneed's Old Shredder / 斯尼德的伐木机
    亡语：随机召唤一个传说随从。"""

    deathrattle = Summon(CONTROLLER, RandomLegendaryMinion())


class GVG_115:
    """Toshley / 托什雷
    战吼，亡语： 将一张零件牌置入你的手牌。"""

    play = deathrattle = Give(CONTROLLER, RandomSparePart())


class GVG_116:
    """Mekgineer Thermaplugg / 瑟玛普拉格
    每当一个敌方随从死亡，召唤一个 麻风侏儒。"""

    events = Death(ENEMY + MINION).on(Summon(CONTROLLER, "EX1_029"))


class GVG_117:
    """Gazlowe / 加兹鲁维
    每当你施放一个法力值消耗为（1）的法术，随机将一张机械牌置入你的手牌。"""

    events = Play(CONTROLLER, SPELL + (COST == 1)).on(Give(Play.PLAYER, RandomMech()))


class GVG_118:
    """Troggzor the Earthinator / 颤地者特罗格佐尔
    每当你的对手施放一个法术，召唤一个石腭穴居人壮汉。"""

    events = Play(OPPONENT, SPELL).on(Summon(CONTROLLER, "GVG_068"))


class GVG_119:
    """Blingtron 3000 / 布林顿3000型
    战吼：为每个玩家装备一把武器。"""

    play = Summon(ALL_PLAYERS, RandomWeapon())


class GVG_120:
    """Hemet Nesingwary / 赫米特·奈辛瓦里
    战吼： 消灭一个野兽。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Destroy(TARGET)
