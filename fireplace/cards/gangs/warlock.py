from ..utils import *


##
# Minions


class CFM_610:
    """Crystalweaver / 魔瘾结晶者
    战吼：使你的所有恶魔获得+1/+1。"""

    play = Buff(FRIENDLY_MINIONS + DEMON, "CFM_610e")


CFM_610e = buff(+1, +1)


class CFM_663:
    """Kabal Trafficker / 暗金教恶魔商贩
    在你的回合结束时，随机将一张恶魔牌置入你的手牌。"""

    events = OWN_TURN_END.on(Give(CONTROLLER, RandomDemon()))


class CFM_699:
    """Seadevil Stinger / 海魔钉刺者
    战吼：在本回合中，你使用的下一张鱼人牌不再消耗法力值，转而消耗生命值。"""

    play = Buff(CONTROLLER, "CFM_699e")


class CFM_699e:
    events = Play(CONTROLLER, MURLOC).on(Destroy(SELF))
    update = Refresh(CONTROLLER, {enums.MURLOCS_COST_HEALTH: True})


class CFM_750:
    """Krul the Unshackled / 唤魔者克鲁尔
    战吼：如果你的牌库里没有相同的牌，则召唤你手牌中的所有 恶魔。"""

    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & Summon(CONTROLLER, FRIENDLY_HAND + DEMON)


class CFM_751:
    """Abyssal Enforcer / 渊狱惩击者
    战吼：对所有其他角色造成3点伤害。"""

    play = Hit(ALL_CHARACTERS - SELF, 3)


class CFM_900:
    """Unlicensed Apothecary / 无证药剂师
    在你召唤一个随从后，对你的英雄造成5点伤害。"""

    events = Summon(CONTROLLER, MINION).after(Hit(FRIENDLY_HERO, 5))


##
# Spells


class CFM_094:
    """Felfire Potion / 邪火药水
    对所有角色造成$5点伤害。"""

    play = Hit(ALL_CHARACTERS, 5)


class CFM_608:
    """Blastcrystal Potion / 爆晶药水
    消灭一个随从，和你的一个法力水晶。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), GainMana(CONTROLLER, -1), SpendMana(CONTROLLER, -1)


class CFM_611:
    """Bloodfury Potion / 血怒药水
    使一个随从获得+3攻击力。如果该随从是恶魔，还会获得+3生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = (Find(TARGET + DEMON), Buff(TARGET, "CFM_611e2")) | Buff(TARGET, "CFM_611e")


CFM_611e = buff(+3)
CFM_611e2 = buff(+3, +3)
