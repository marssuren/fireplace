# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立普通
"""

from ..utils import *

class TID_713:
    """Bubbler - 1费 2/4
    受到恰好1点伤害后，消灭该随从"""
    events = Damage(SELF).on(
        Find(SELF & (Damage.AMOUNT == 1)) & Destroy(SELF)
    )


class TSC_001:
    """Naval Mine - 2费 0/2
    亡语：对敌方英雄造成4点伤害"""
    deathrattle = Hit(ENEMY_HERO, 4)


class TSC_002:
    """Pufferfist - 3费 3/4
    在你的英雄攻击后，对所有敌人造成1点伤害"""
    events = Attack(FRIENDLY_HERO).after(
        Hit(ALL_ENEMIES, 1)
    )


class TSC_007:
    """Gangplank Diver - 5费 6/4
    休眠1回合。突袭。攻击时免疫"""
    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    tags = {GameTag.RUSH: True}
    events = Attack(SELF).on(Buff(SELF, "TSC_007e"))


class TSC_007e:
    """攻击时免疫"""
    tags = {GameTag.IMMUNE: True}
    events = Attack(OWNER).after(Destroy(SELF))


class TSC_013:
    """Slimescale Diver - 3费 2/4
    休眠1回合。突袭，剧毒"""
    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    tags = {GameTag.RUSH: True, GameTag.POISONOUS: True}

class TSC_017:
    """Baba Naga - 4费 4/4
    战吼：如果你在持有该牌时施放过法术，造成3点伤害"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_017e")
    play = Find(SELF + POWERED_UP) & Hit(TARGET, 3)


class TSC_017e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_020:
    """Barbaric Sorceress - 6费 3/7
    嘲讽。战吼：交换双方手牌中各一张随机法术的费用"""
    tags = {GameTag.TAUNT: True}
    play = (
        SwapCost(RANDOM(FRIENDLY_HAND + SPELL), RANDOM(ENEMY_HAND + SPELL))
    )


class TSC_034:
    """Gorloc Ravager - 5费 4/3
    战吼：抽3张鱼人牌"""
    play = Draw(CONTROLLER) * 3 & MURLOC


class TSC_053:
    """Rainbow Glowscale - 2费 2/3
    法术伤害+1"""
    tags = {GameTag.SPELLPOWER: 1}

class TSC_632:
    """Click-Clocker - 1费 1/1
    圣盾。战吼：随机使你手牌中的一张机械牌获得+1/+1"""
    tags = {GameTag.DIVINE_SHIELD: True}
    play = Buff(RANDOM(FRIENDLY_HAND + MECH), "TSC_632e")


class TSC_632e:
    """机械增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_638:
    """Piranha Swarmer - 1费 1/1
    突袭。在你召唤一个食人鱼群后，获得+1攻击力"""
    tags = {GameTag.RUSH: True}
    events = Summon(CONTROLLER, SELF).after(
        Buff(SELF, "TSC_638e")
    )


class TSC_638e:
    """食人鱼群增益"""
    tags = {GameTag.ATK: 1}


class TSC_640:
    """Reefwalker - 3费 3/2
    战吼和亡语：召唤一个1/1的食人鱼群"""
    play = Summon(CONTROLLER, "TSC_638")
    deathrattle = Summon(CONTROLLER, "TSC_638")


class TSC_646:
    """Seascout Operator - 3费 2/4
    战吼：如果你控制一个机械，召唤两个2/1的机械鱼"""
    play = Find(FRIENDLY_MINIONS + MECH) & (
        Summon(CONTROLLER, "TSC_646t") * 2
    )

class TSC_647:
    """Pelican Diver - 1费 4/1
    休眠1回合。突袭"""
    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    tags = {GameTag.RUSH: True}


class TSC_823:
    """Murkwater Scribe - 2费 3/2
    战吼：你的下一个法术费用减少(1)点"""
    play = Buff(CONTROLLER, "TSC_823e")


class TSC_823e:
    """下一个法术减费"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class TSC_909:
    """Tuskarrrr Trawler - 2费 2/3
    战吼：疏浚"""
    play = Dredge(CONTROLLER)

class TSC_911:
    """Excavation Specialist - 4费 3/6
    战吼：疏浚。使其费用减少(1)点"""
    play = Dredge(CONTROLLER) & Buff(DREDGED_CARD, "TSC_911e")


class TSC_911e:
    """疏浚减费"""
    tags = {GameTag.COST: -1}


class TSC_919:
    """Azsharan Sentinel - 5费 5/6
    嘲讽。亡语：将一张"沉没的哨兵"洗入你的牌库底部"""
    tags = {GameTag.TAUNT: True}
    deathrattle = ShuffleIntoDeck(CONTROLLER, "TSC_919t", position='bottom')


class TSC_928:
    """Security Automaton - 2费 1/3
    在你召唤一个机械后，获得+1/+1"""
    events = Summon(CONTROLLER, MECH).after(
        Buff(SELF, "TSC_928e")
    )


class TSC_928e:
    """机械增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_935:
    """Selfish Shellfish - 4费 7/7
    亡语：你的对手抽2张牌"""
    deathrattle = Draw(OPPONENT) * 2


class TSC_938:
    """Treasure Guard - 3费 1/5
    嘲讽。亡语：抽一张牌"""
    tags = {GameTag.TAUNT: True}
    deathrattle = Draw(CONTROLLER)

