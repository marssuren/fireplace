from ..utils import *


##
# Minions


class CFM_643:
    """Hobart Grapplehammer / 霍巴特·钩锤
    战吼：如果你装备着武器，使你的手牌和牌库里的所有随从牌获得+2/+2。"""

    play = Buff(FRIENDLY + WEAPON + (IN_HAND | IN_DECK), "CFM_643e")


CFM_643e = buff(atk=1)


class CFM_754:
    """Grimy Gadgeteer / 污手玩具商
    在你的回合结束时，随机使你手牌中的一张随从牌获得+2/+2。"""

    events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_754e"))


CFM_754e = buff(+2, +2)


class CFM_755:
    """Grimestreet Pawnbroker / 污手街典当师
    战吼：随机使你手牌中的一张武器牌获得+1/+1。"""

    play = Buff(RANDOM(FRIENDLY_HAND + WEAPON), "CFM_755e")


CFM_755e = buff(+1, +1)


class CFM_756:
    """Alley Armorsmith / 兽人铸甲师
    嘲讽 每当本随从造成伤害时，获得等量的护甲值。"""

    events = Damage(CHARACTER, None, SELF).on(GainArmor(FRIENDLY_HERO, Damage.AMOUNT))


##
# Spells


class CFM_716:
    """Sleep with the Fishes / 鱼死网破
    对所有受伤的随从造成$3点 伤害。"""

    play = Hit(ALL_MINIONS + DAMAGED, 3)


class CFM_752:
    """Stolen Goods / 失窃物资
    抽一张嘲讽随从牌，使其获得+2/+2。"""

    play = Buff(RANDOM(FRIENDLY_HAND + MINION + TAUNT), "CFM_752e")


CFM_752e = buff(+3, +3)


class CFM_940:
    """I Know a Guy / 盛气凌人
    发现一张嘲讽随从牌。使其获得+1/+2。"""

    play = DISCOVER(RandomMinion(taunt=True))


##
# Weapons


class CFM_631:
    """Brass Knuckles / 黄铜指虎
    在你的英雄攻击后，随机使你手牌中的一张随从牌获得+1/+1。"""

    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_631e")
    )


CFM_631e = buff(+1, +1)
