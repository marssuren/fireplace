from ..utils import *


##
# Minions


class GVG_002:
    """Snowchugger / 碎雪机器人
    冻结任何受到本随从伤害的角色。"""

    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class GVG_004:
    """Goblin Blastmage / 地精炎术师
    战吼：如果你控制任何机械，则造成6点伤害，随机分配到所有敌人身上。"""

    powered_up = Find(FRIENDLY_MINIONS + MECH)
    play = powered_up & Hit(RANDOM_ENEMY_CHARACTER, 1) * 4


class GVG_007:
    """Flame Leviathan / 烈焰巨兽
    突袭。当你抽到该牌时，对所有除机械外的角色造成 2点伤害。"""

    draw = Hit(ALL_CHARACTERS, 2)


##
# Spells


class GVG_001:
    """Flamecannon / 烈焰轰击
    随机对一个敌方随从造成 $4点伤害。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION, 4)


class GVG_003:
    """Unstable Portal / 不稳定的传送门
    随机将一张随从牌置入你的手牌。该牌的法力值消耗减少（3）点。"""

    play = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


@custom_card
class GVG_003e:
    tags = {
        GameTag.CARDNAME: "Unstable Portal Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -3,
    }

    events = REMOVED_IN_PLAY


class GVG_005:
    """Echo of Medivh / 麦迪文的残影
    将每个友方随从的各一张复制置入你的手牌。"""

    play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS))
