# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立稀有
"""

from ..utils import *

class TID_710:
    """Snapdragon - 3费 3/3
    战吼：使你牌库中所有战吼随从获得+1/+1"""
    play = Buff(FRIENDLY_DECK + MINION + BATTLECRY, "TID_710e")


class TID_710e:
    """战吼增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TID_744:
    """Coilfang Constrictor - 4费 5/4
    战吼：查看对手手牌中的3张牌，选择一张。该牌在下回合无法打出"""
    # 简化实现：随机选择对手手牌中的一张牌，使其下回合无法打出
    play = Buff(RANDOM(ENEMY_HAND), "TID_744e")


class TID_744e:
    """无法打出"""
    tags = {GameTag.CANT_PLAY: True}
    events = OwnTurnBegin(CONTROLLER).on(Destroy(SELF))


class TSC_065:
    """Helmet Hermit - 1费 4/3
    无法攻击"""
    tags = {GameTag.CANT_ATTACK: True}

class TSC_645:
    """Stormcoil Mothership - 6费 5/4
    突袭。亡语：召唤两个随机的费用不超过(3)的机械"""
    tags = {GameTag.RUSH: True}
    deathrattle = (
        Summon(CONTROLLER, RandomMinion(cost=3, race=Race.MECHANICAL)) * 2
    )


class TSC_826:
    """Crushclaw Enforcer - 3费 3/4
    战吼：如果你在持有该牌时施放过法术，抽一张娜迦牌"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_826e")
    play = Find(SELF + POWERED_UP) & ForceDraw(RANDOM(FRIENDLY_DECK + NAGA))


class TSC_826e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}

class TSC_827:
    """Vicious Slitherspear - 1费 1/3
    在你施放一个法术后，获得+1攻击力，直到你的下个回合"""
    events = Play(CONTROLLER, SPELL).after(
        Buff(SELF, "TSC_827e")
    )


class TSC_827e:
    """临时攻击力增益"""
    tags = {GameTag.ATK: 1}
    events = OwnTurnBegin(CONTROLLER).on(Destroy(SELF))


class TSC_960:
    """Twin-fin Fin Twin - 3费 2/1
    突袭。战吼：召唤一个该随从的复制"""
    tags = {GameTag.RUSH: True}
    play = Summon(CONTROLLER, ExactCopy(SELF))

