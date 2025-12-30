"""
暗月马戏团 - 战士
"""
from ..utils import *


##
# Minions

class DMF_521:
    """吞剑艺人 - Sword Eater
    嘲讽。战吼：装备一把3/2的剑。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
        GameTag.TAUNT: True,
    }
    play = Summon(CONTROLLER, "DMF_521t")


class DMF_521t:
    """剑 - Sword"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 2,
        GameTag.COST: 1,
    }


class DMF_523:
    """碰碰车 - Bumper Car
    突袭。亡语：将两张1/1并具有突袭的骑手牌置入你的手牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.RUSH: True,
    }
    deathrattle = Give(CONTROLLER, "DMF_523t") * 2


class DMF_523t:
    """骑手 - Rider"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.RUSH: True,
    }


class DMF_525:
    """马戏领班威特利 - Ringmaster Whatley
    战吼：抽一张机械牌、一张龙牌和一张海盗牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
    }
    play = (
        ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + MECH),
        ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + DRAGON),
        ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + PIRATE),
    )


class DMF_528:
    """帐篷摧毁者 - Tent Trasher
    突袭。你每控制一个种族唯一的友方随从，本牌的法力值消耗便减少(1)点。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.RUSH: True,
    }
    # TODO: 实现种族唯一计数的减费
    # 这需要复杂的逻辑，暂时简化为固定减费
    cost_mod = -COUNT(FRIENDLY_MINIONS)


class DMF_529:
    """精英牛头人酋长，金属之神 - E.T.C., God of Metal
    在一个友方突袭随从攻击后，对敌方英雄造成2点伤害。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 8,
    }
    events = Attack(FRIENDLY + MINION + RUSH).after(
        Hit(ENEMY_HERO, 2)
    )


class DMF_531:
    """置景工 - Stage Hand
    战吼：随机使你手牌中的一张随从牌获得+1/+1。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
    }
    play = Buff(RANDOM(FRIENDLY_HAND + MINION), "DMF_531e")


class DMF_531e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class YOP_014:
    """铁甲战车 - Ironclad
    战吼：如果你的英雄拥有护甲值，便获得+2/+2。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    play = Find(FRIENDLY_HERO + (ARMOR > 0)) & Buff(SELF, "YOP_014e")


class YOP_014e:
    """+2/+2"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


##
# Spells

class DMF_522:
    """雷区挑战 - Minefield
    随机对所有随从造成共5点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = Hit(RANDOM(ALL_MINIONS), 1) * 5


class DMF_526:
    """舞台跳水 - Stage Dive
    抽一张突袭随从牌。腐蚀：使其获得+2/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + RUSH)
    corrupt = Buff(FRIENDLY_HAND + MINION + RUSH, "DMF_526e")


class DMF_526e:
    """+2/+1"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }


class DMF_530:
    """实力担当 - Feat of Strength
    随机使你手牌中的一张嘲讽随从牌获得+5/+5。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    play = Buff(RANDOM(FRIENDLY_HAND + MINION + TAUNT), "DMF_530e")


class DMF_530e:
    """+5/+5"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }


##
# Weapons

class DMF_524:
    """马戏领班的节杖 - Ringmaster's Baton
    在你的英雄攻击后，使你手牌中的一张机械牌、一张龙牌和一张海盗牌获得+1/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 1,
        GameTag.DURABILITY: 3,
        GameTag.COST: 3,
    }
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + MINION + MECH), "DMF_524e"),
        Buff(RANDOM(FRIENDLY_HAND + MINION + DRAGON), "DMF_524e"),
        Buff(RANDOM(FRIENDLY_HAND + MINION + PIRATE), "DMF_524e"),
    )


class DMF_524e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class YOP_013:
    """尖刺轮盘 - Spiked Wheel
    当你的英雄拥有护甲值时，本武器具有+3攻击力。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 1,
        GameTag.DURABILITY: 4,
        GameTag.COST: 2,
    }
    update = Find(FRIENDLY_HERO + (ARMOR > 0)) & Refresh(SELF, {GameTag.ATK: 3})
