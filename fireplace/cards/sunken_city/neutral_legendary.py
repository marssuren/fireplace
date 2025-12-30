# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立传说
"""

from ..utils import *

class TID_711:
    """Ozumat - 8费 6/5
    巨型+6。亡语：奥祖玛特每有一个触须，便消灭一个随机敌方随从"""
    colossal_appendages = ["TID_711t"] * 6
    deathrattle = (
        Destroy(RANDOM(ENEMY_MINIONS)) * Count(FRIENDLY_MINIONS + ID("TID_711t"))
    )


class TID_712:
    """Neptulon the Tidehunter - 10费 7/7
    巨型+2，突袭，风怒。每当奈普图隆攻击时，如果你控制任何手部，改为由它们攻击"""
    colossal_appendages = ["TID_712t", "TID_712t2"]
    tags = {GameTag.RUSH: True, GameTag.WINDFURY: True}
    events = Attack(SELF).on(
        Find(FRIENDLY_MINIONS + ID("TID_712t")) & Attack(FRIENDLY_MINIONS + ID("TID_712t"), ATTACK_TARGET)
    )

class TSC_032:
    """Blademaster Okani - 4费 2/6
    战吼：秘密选择反制对手打出的下一张随从或法术"""
    # 简化实现：反制对手打出的下一张牌
    play = Buff(CONTROLLER, "TSC_032e")


class TSC_032e:
    """反制效果"""
    events = Play(OPPONENT).on(Counter(Play.CARD) & Destroy(SELF))


class TSC_067:
    """Ambassador Faelin - 4费 4/5
    战吼：将3张巨型随从置入你的牌库底部"""
    play = (
        ShuffleIntoDeck(CONTROLLER, RandomMinion(tag=GameTag.COLOSSAL), position='bottom') * 3
    )

class TSC_641:
    """Queen Azshara - 5费 5/5
    战吼：如果你在持有该牌时施放过3个法术，选择一个远古遗物"""
    powered_up = Count(Play(CONTROLLER, SPELL)) >= 3 & Buff(SELF, "TSC_641e")
    play = Find(SELF + POWERED_UP) & GenericChoice(CONTROLLER, Discover(CONTROLLER, ["TSC_641t1", "TSC_641t2", "TSC_641t3", "TSC_641t4"]))


class TSC_641e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_649:
    """Ini Stormcoil - 5费 4/4
    战吼：选择一个友方机械。召唤一个具有突袭、风怒和圣盾的该随从的复制"""
    play = Summon(CONTROLLER, ExactCopy(TARGET)) & Buff(LAST_SUMMONED, "TSC_649e")


class TSC_649e:
    """机械增强"""
    tags = {GameTag.RUSH: True, GameTag.WINDFURY: True, GameTag.DIVINE_SHIELD: True}


class TSC_908:
    """Sir Finley, Sea Guide - 1费 1/3
    战吼：将你的手牌与牌库底部的牌交换"""
    # 简化实现：将手牌移到牌库底部，然后从牌库底部抽相同数量的牌
    play = (
        lambda self, target: [
            ShuffleIntoDeck(self.controller, card, position='bottom')
            for card in list(self.controller.hand)
        ] + [Draw(self.controller) for _ in range(len(self.controller.hand))]
    )

