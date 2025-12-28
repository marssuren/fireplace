from ..utils import *


class EX1_005:
    """Big Game Hunter / 王牌猎人
    可交易 战吼：消灭一个攻击力大于或等于7的随从。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_MIN_ATTACK: 7,
    }
    play = Destroy(TARGET)


class EX1_105:
    """Mountain Giant / 山岭巨人
    你每有一张其他手牌，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Count(FRIENDLY_HAND - SELF)


class EX1_507:
    """Murloc Warleader / 鱼人领军
    你的其他鱼人拥有+2攻击力。"""

    update = Refresh(FRIENDLY_MINIONS + MURLOC - SELF, buff="EX1_507e")


EX1_507e = buff(atk=2)


class EX1_564:
    """Faceless Manipulator / 无面操纵者
    战吼：选择一个随从，成为它的复制。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Morph(SELF, ExactCopy(TARGET))


class EX1_586:
    """Sea Giant / 海巨人
    战场上每有一个其他随从，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Count(ALL_MINIONS)


class EX1_590:
    """Blood Knight / 血骑士
    战吼：所有随从失去圣盾。每有一个随从失去圣盾，便获得+3/+3。"""

    play = (
        Buff(SELF, "EX1_590e") * Count(ALL_MINIONS + DIVINE_SHIELD),
        UnsetTags(ALL_MINIONS, (GameTag.DIVINE_SHIELD,)),
    )


EX1_590e = buff(+3, +3)


class EX1_620:
    """Molten Giant / 熔核巨人
    你的英雄每缺失一点生命值，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -DAMAGE(FRIENDLY_HERO)


class NEW1_016:
    """Captain's Parrot / 船长的鹦鹉
    战吼：从你的牌库中抽一张海盗牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE))


class NEW1_017:
    """Hungry Crab / 鱼人杀手蟹
    战吼：消灭一个鱼人，并获得+2/+2。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 14,
    }
    play = Destroy(TARGET), Buff(SELF, "NEW1_017e")


NEW1_017e = buff(+2, +2)


class NEW1_021:
    """Doomsayer / 末日预言者
    在你的回合开始时，消灭所有随从。"""

    events = OWN_TURN_BEGIN.on(Destroy(ALL_MINIONS))


class NEW1_027:
    """Southsea Captain / 南海船长
    你的其他海盗拥有+1/+1。"""

    update = Refresh(FRIENDLY_MINIONS + PIRATE - SELF, buff="NEW1_027e")


NEW1_027e = buff(+1, +1)


class EX1_188:
    """Barrens Stablehand / 贫瘠之地饲养员
    战吼：随机召唤一只野兽。"""

    # <b>Battlecry:</b> Summon a random Beast.
    play = Summon(CONTROLLER, RandomBeast())
