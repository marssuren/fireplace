# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 猎人
"""

from ..utils import *

class TID_074:
    """Ancient Krakenbane - 3费 3/3
    战吼：如果你在持有该牌时施放过3个法术，造成5点伤害"""
    powered_up = Count(Play(CONTROLLER, SPELL)) >= 3 & Buff(SELF, "TID_074e")
    play = Find(SELF + POWERED_UP) & Hit(TARGET, 5)


class TID_074e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TID_075:
    """Shellshot - 3费法术
    对一个随机敌方随从造成3点伤害。以少1点伤害重复此效果"""
    play = Hit(RANDOM(ENEMY_MINIONS), 3) & Hit(RANDOM(ENEMY_MINIONS), 2) & Hit(RANDOM(ENEMY_MINIONS), 1)


class TID_099:
    """K9-0tron - 2费 2/3
    战吼：疏浚。如果是1费随从，召唤它"""
    play = Dredge(CONTROLLER) & Find(DREDGED_CARD + MINION + (COST == 1)) & Summon(CONTROLLER, DREDGED_CARD)


class TSC_023:
    """Barbed Nets - 1费法术
    对一个敌人造成2点伤害。如果你在持有该牌时打出过娜迦，选择第二个目标"""
    powered_up = Find(FRIENDLY_HAND + NAGA) & Buff(SELF, "TSC_023e")
    play = Hit(TARGET, 2) & Find(SELF + POWERED_UP) & Hit(TARGET, 2)


class TSC_023e:
    """已打出娜迦标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_070:
    """Harpoon Gun - 3费 3/2武器
    在你的英雄攻击后，疏浚。如果是野兽，使其费用减少(2)点"""
    events = Attack(FRIENDLY_HERO).after(
        Dredge(CONTROLLER) &
        Find(DREDGED_CARD + BEAST) &
        Buff(DREDGED_CARD, "TSC_070e")
    )


class TSC_070e:
    """野兽减费"""
    tags = {GameTag.COST: -2}


class TSC_071:
    """Twinbow Terrorcoil - 4费 4/4
    战吼：如果你在持有该牌时施放过法术，你的下一个法术施放两次"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_071e")
    play = Find(SELF + POWERED_UP) & Buff(CONTROLLER, "TSC_071e2")


class TSC_071e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_071e2:
    """下一个法术施放两次"""
    events = Play(CONTROLLER, SPELL).after(
        CastSpell(Play.CARD) & Destroy(SELF)
    )


class TSC_072:
    """Conch's Call - 3费法术
    抽一张娜迦牌和一张法术牌"""
    play = ForceDraw(RANDOM(FRIENDLY_DECK + NAGA)) & ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))


class TSC_073:
    """Raj Naz'jan - 2费 2/3
    在你施放一个法术后，对敌方英雄造成等同于其费用的伤害"""
    events = Play(CONTROLLER, SPELL).after(
        Hit(ENEMY_HERO, COST(Play.CARD))
    )


class TSC_929:
    """Emergency Maneuvers - 2费法术
    奥秘：当一个友方随从死亡时，召唤它的一个复制。该复制休眠1回合"""
    secret = Death(FRIENDLY_MINIONS).on(
        Summon(CONTROLLER, ExactCopy(Death.ENTITY)) & Buff(LAST_SUMMONED, "TSC_929e")
    )


class TSC_929e:
    """休眠标记"""
    tags = {GameTag.DORMANT: True}


class TSC_945:
    """Azsharan Saber - 4费 4/3
    突袭。亡语：将一张"沉没的军刀"置入你的牌库底部"""
    tags = {GameTag.RUSH: True}
    deathrattle = ShuffleIntoDeck(CONTROLLER, "TSC_945t", position='bottom')


class TSC_946:
    """Urchin Spines - 1费法术
    你本回合的法术具有剧毒"""
    play = Buff(CONTROLLER, "TSC_946e")


class TSC_946e:
    """法术剧毒"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.POISONOUS: True})
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))


class TSC_947:
    """Naga's Pride - 3费法术
    召唤两个2/2的狮子鱼。如果你在持有该牌时打出过娜迦，使它们获得+1/+1"""
    powered_up = Find(FRIENDLY_HAND + NAGA) & Buff(SELF, "TSC_947e")
    play = (
        Summon(CONTROLLER, "TSC_947t") * 2 &
        Find(SELF + POWERED_UP) &
        Buff(FRIENDLY_MINIONS + ID("TSC_947t"), "TSC_947e2")
    )


class TSC_947e:
    """已打出娜迦标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_947e2:
    """狮子鱼增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_950:
    """Hydralodon - 7费 5/5
    巨型+2。战吼：使你的九头蛇龙头部获得突袭"""
    colossal_appendages = ["TSC_950t", "TSC_950t2"]
    play = Buff(FRIENDLY_MINIONS + ID("TSC_950t"), "TSC_950e")


class TSC_950e:
    """突袭"""
    tags = {GameTag.RUSH: True}

