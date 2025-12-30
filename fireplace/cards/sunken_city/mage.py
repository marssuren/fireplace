# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 法师
"""

from ..utils import *

class TID_707:
    """Submerged Spacerock - 2费 2/2
    亡语：将两张奥秘法师法术置入你的手牌。它们是临时的"""
    deathrattle = (
        Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE, spell_school=SpellSchool.ARCANE)) * 2 &
        Buff(LAST_GIVEN, "TID_707e")
    )


class TID_707e:
    """临时标记"""
    events = OwnTurnEnd(CONTROLLER).on(Discard(OWNER))


class TID_708:
    """Polymorph: Jellyfish - 3费法术
    将一个随从变形为一个4/1并具有法术伤害+2的水母"""
    play = Morph(TARGET, "TID_708t")


class TID_709:
    """Lady Naz'jar - 5费 5/5
    在你的手牌中时，在你施放一个火焰、冰霜或奥秘法术后变形"""
    events = Play(CONTROLLER, SPELL + (FIRE | FROST | ARCANE)).on(
        Morph(SELF, RandomMinion())
    )


class TSC_029:
    """Gaia, the Techtonic - 8费 5/7
    巨型+2。在一个友方机械攻击后，对所有敌人造成1点伤害"""
    colossal_appendages = ["TSC_029t", "TSC_029t2"]
    events = Attack(FRIENDLY_MINIONS + MECH).after(
        Hit(ALL_ENEMIES, 1)
    )


class TSC_054:
    """Mecha-Shark - 3费 4/3
    在你召唤一个机械后，造成3点伤害，随机分配到所有敌人身上"""
    events = Summon(CONTROLLER, MECH).after(
        Hit(RANDOM_ENEMY, 1) * 3
    )


class TSC_055:
    """Seafloor Gateway - 3费法术
    抽一张机械牌。使你手牌中的机械牌费用减少(1)点"""
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MECH)) & Buff(FRIENDLY_HAND + MECH, "TSC_055e")


class TSC_055e:
    """机械减费"""
    tags = {GameTag.COST: -1}


class TSC_056:
    """Volcanomancy - 2费法术
    选择一个随从。当它死亡时，对所有其他随从造成3点伤害"""
    play = Buff(TARGET, "TSC_056e")


class TSC_056e:
    """火山术标记"""
    deathrattle = Hit(ALL_MINIONS - SELF, 3)


class TSC_087:
    """Commander Sivara - 4费 3/5
    战吼：如果你在持有该牌时施放过3个法术，将这些法术加回你的手牌"""
    powered_up = Count(Play(CONTROLLER, SPELL)) >= 3 & Buff(SELF, "TSC_087e")
    play = Find(SELF + POWERED_UP) & Give(CONTROLLER, Copy(LAST_PLAYED_SPELL)) * 3


class TSC_087e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_620:
    """Spitelash Siren - 4费 2/5
    在你打出一张娜迦后，刷新两个法力水晶（然后切换到法术）"""
    events = Play(CONTROLLER, NAGA).after(
        GainMana(CONTROLLER, 2) & Morph(SELF, "TSC_620t")
    )


class TSC_642:
    """Trench Surveyor - 1费 2/1
    战吼：疏浚。如果是机械，抽出它"""
    play = Dredge(CONTROLLER) & Find(DREDGED_CARD + MECH) & ForceDraw(DREDGED_CARD)


class TSC_643:
    """Spellcoiler - 2费 2/3
    战吼：如果你在持有该牌时施放过法术，发现一个法术"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_643e")
    play = Find(SELF + POWERED_UP) & GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomSpell()))


class TSC_643e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_776:
    """Azsharan Sweeper - 3费 3/4
    战吼：将一张"沉没的清扫者"置入你的牌库底部"""
    play = ShuffleIntoDeck(CONTROLLER, "TSC_776t", position='bottom')


class TSC_948:
    """Gifts of Azshara - 2费法术
    抽一张牌。如果你在持有该牌时打出过娜迦，再抽一张"""
    powered_up = Find(FRIENDLY_HAND + NAGA) & Buff(SELF, "TSC_948e")
    play = Draw(CONTROLLER) & Find(SELF + POWERED_UP) & Draw(CONTROLLER)


class TSC_948e:
    """已打出娜迦标记"""
    tags = {GameTag.POWERED_UP: True}

