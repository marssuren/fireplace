# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 战士
"""

from ..utils import *

class TID_714:
    """Igneous Lavagorger - 4费 3/5
    嘲讽。战吼：疏浚。获得等同于其费用的护甲值"""
    tags = {GameTag.TAUNT: True}
    play = Dredge(CONTROLLER) & GainArmor(CONTROLLER, COST(DREDGED_CARD))


class TID_715:
    """Clash of the Colossals - 3费法术
    将一张随机巨型随从置入双方手牌。你的费用减少(2)点"""
    play = (
        Give(CONTROLLER, RandomMinion(tag=GameTag.COLOSSAL)) &
        Buff(LAST_GIVEN, "TID_715e") &
        Give(OPPONENT, RandomMinion(tag=GameTag.COLOSSAL))
    )


class TID_715e:
    """巨型减费"""
    tags = {GameTag.COST: -2}


class TID_716:
    """Tidal Revenant - 8费 5/8
    战吼：造成5点伤害。获得8点护甲值"""
    play = Hit(TARGET, 5) & GainArmor(CONTROLLER, 8)


class TSC_659:
    """Trenchstalker - 9费 8/9
    战吼：攻击三个不同的随机敌人"""
    play = (
        Attack(SELF, RANDOM(ALL_ENEMIES)) &
        Attack(SELF, RANDOM(ALL_ENEMIES)) &
        Attack(SELF, RANDOM(ALL_ENEMIES))
    )


class TSC_660:
    """Nellie, the Great Thresher - 7费 5/5
    巨型+1。战吼：发现3个海盗来组成奈莉的船员"""
    colossal_appendages = ["TSC_660t"]
    play = (
        GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion(race=Race.PIRATE))) * 3
    )


class TSC_913:
    """Azsharan Trident - 3费 3/2武器
    亡语：将一张"沉没的三叉戟"置入你的牌库底部"""
    deathrattle = ShuffleIntoDeck(CONTROLLER, "TSC_913t", position='bottom')


class TSC_917:
    """Blackscale Brute - 7费 5/6
    嘲讽。战吼：如果你装备了武器，召唤一个5/6并具有突袭的娜迦"""
    tags = {GameTag.TAUNT: True}
    play = Find(FRIENDLY_WEAPON) & Summon(CONTROLLER, "TSC_917t")


class TSC_939:
    """Forged in Flame - 2费法术
    摧毁你的武器，然后抽等同于其攻击力的牌"""
    play = (
        lambda self, target: [
            Draw(self.controller) * self.controller.weapon.atk,
            Destroy(self.controller.weapon)
        ] if self.controller.weapon else []
    )


class TSC_940:
    """From the Depths - 3费法术
    使你牌库底部的5张牌费用减少(3)点，然后疏浚"""
    play = (
        Buff(FRIENDLY_DECK[-5:], "TSC_940e") &
        Dredge(CONTROLLER)
    )


class TSC_940e:
    """深渊减费"""
    tags = {GameTag.COST: -3}


class TSC_941:
    """Guard the City - 2费法术
    获得3点护甲值。召唤一个2/3并具有嘲讽的娜迦"""
    play = GainArmor(CONTROLLER, 3) & Summon(CONTROLLER, "TSC_941t")


class TSC_942:
    """Obsidiansmith - 2费 3/2
    战吼：疏浚。如果是随从或武器，使其获得+1/+1"""
    play = (
        Dredge(CONTROLLER) &
        Find(DREDGED_CARD + (MINION | WEAPON)) &
        Buff(DREDGED_CARD, "TSC_942e")
    )


class TSC_942e:
    """黑曜石增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_943:
    """Lady Ashvane - 5费 5/5
    战吼：使你手牌、牌库和战场上的所有武器获得+1/+1"""
    play = Buff(FRIENDLY_HAND + WEAPON, "TSC_943e") & Buff(FRIENDLY_DECK + WEAPON, "TSC_943e") & Buff(FRIENDLY_WEAPON, "TSC_943e")


class TSC_943e:
    """武器增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_944:
    """The Fires of Zin-Azshari - 2费法术
    将你的牌库替换为费用不低于(5)的随从。它们的费用变为(5)点"""
    play = (
        lambda self, target: [
            Destroy(card) for card in list(self.controller.deck)
        ] + [
            Shuffle(self.controller, RandomMinion(cost_min=5)) for _ in range(30)
        ] + [
            Buff(FRIENDLY_DECK, "TSC_944e")
        ]
    )


class TSC_944e:
    """津艾萨里之火"""
    tags = {GameTag.COST: 5}
