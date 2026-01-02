# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立稀有
"""

from ..utils import *

class TID_710:
    """毒鳍龙 - 3费 3/3
    战吼：使你牌库中的所有战吼随从获得+1/+1"""
    play = Buff(FRIENDLY_DECK + MINION + BATTLECRY, "TID_710e")


class TID_710e:
    """战吼增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TID_744:
    """盘牙蟠蟒 - 4费 5/4
    战吼：检视你对手的3张手牌并选择一张，使其无法在下回合中使用"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    # 从对手手牌中随机选择3张（去重），让玩家选择一张，然后对其施加 buff
    play = GenericChoice(CONTROLLER, RANDOM(DeDuplicate(ENEMY_HAND)) * 3).then(
        Buff(GenericChoice.CARD, "TID_744e")
    )



class TID_744e:
    """无法打出"""
    tags = {GameTag.CANT_PLAY: True}
    events = OwnTurnBegin(CONTROLLER).on(Destroy(SELF))


class TSC_065:
    """盔中寄居蟹 - 1费 4/3
    无法攻击"""
    tags = {GameTag.CANT_ATTACK: True}

class TSC_645:
    """积雷母舰 - 6费 5/4
    突袭。亡语：随机召唤两个法力值消耗小于或等于（3）点的机械"""
    tags = {GameTag.RUSH: True}
    deathrattle = (
        Summon(CONTROLLER, RandomMinion(cost=3, race=Race.MECHANICAL)) * 2
    )


class TSC_826:
    """重钳执行者 - 3费 3/4
    战吼：如果你在本牌在你手中时施放过法术，抽一张纳迦牌"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_826e")
    play = Find(SELF + POWERED_UP) & ForceDraw(RANDOM(FRIENDLY_DECK + NAGA))


class TSC_826e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}

class TSC_827:
    """凶恶的滑矛纳迦 - 1费 1/3
    在你施放一个法术后，直到你的下个回合，获得+1攻击力"""
    events = Play(CONTROLLER, SPELL).after(
        Buff(SELF, "TSC_827e")
    )


class TSC_827e:
    """临时攻击力增益"""
    tags = {GameTag.ATK: 1}
    events = OwnTurnBegin(CONTROLLER).on(Destroy(SELF))


class TSC_960:
    """并鳍奇兵 - 3费 2/1
    突袭。战吼：召唤一个本随从的复制"""
    tags = {GameTag.RUSH: True}
    play = Summon(CONTROLLER, ExactCopy(SELF))

