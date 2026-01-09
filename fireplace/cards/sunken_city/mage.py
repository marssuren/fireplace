# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 法师
"""

from ..utils import *

class TID_707:
    """淹没的陨石 - 2费 2/2
    亡语：将两张法师奥术法术牌置入你的手牌。这些牌为临时牌"""
    deathrattle = (
        Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE, spell_school=SpellSchool.ARCANE)) * 2 &
        Buff(LAST_GIVEN, "TID_707e")
    )


class TID_707e:
    """临时标记"""
    events = OWN_TURN_END.on(Discard(OWNER))


class TID_708:
    """变形术：水母 - 3费法术
    将一个随从变形成为一只4/1并具有法术伤害+2的水母"""
    play = Morph(TARGET, "TID_708t")


class TID_709:
    """纳兹夏尔女士 - 5费 5/5
    此牌在你的手牌中时，会在你施放火焰、冰霜或奥术法术后变形"""
    events = Play(CONTROLLER, SPELL + (FIRE | FROST | ARCANE)).on(
        Morph(SELF, RandomMinion())
    )


class TSC_029:
    """盖亚，巨力机甲 - 8费 5/7
    巨型+2。在一个友方机械攻击后，对所有敌人造成1点伤害"""
    colossal_appendages = ["TSC_029t", "TSC_029t2"]
    events = Attack(FRIENDLY_MINIONS + MECH).after(
        Hit(ALL_ENEMIES, 1)
    )


class TSC_054:
    """机械鲨鱼 - 3费 4/3
    在你召唤一个机械后，造成3点伤害，随机分配到所有敌人身上"""
    events = Summon(CONTROLLER, MECH).after(
        Hit(RANDOM_ENEMY, 1) * 3
    )


class TSC_055:
    """海床传送口 - 3费法术
    抽一张机械牌。使你手牌中所有机械牌的法力值消耗减少（1）点"""
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MECH)) & Buff(FRIENDLY_HAND + MECH, "TSC_055e")


class TSC_055e:
    """机械减费"""
    tags = {GameTag.COST: -1}


class TSC_056:
    """火山术 - 2费法术
    选择一个随从。当其死亡时，对所有其他随从造成3点伤害"""
    play = Buff(TARGET, "TSC_056e")


class TSC_056e:
    """火山术标记"""
    deathrattle = Hit(ALL_MINIONS - SELF, 3)


class TSC_087:
    """指挥官西瓦拉 - 4费 3/5
    战吼：如果你在本牌在你手中时施放过三个法术，则将那些法术置回你的手牌"""
    powered_up = Count(Play(CONTROLLER, SPELL)) >= 3 & Buff(SELF, "TSC_087e")
    play = (Find(SELF + POWERED_UP), Give(CONTROLLER, Copy(LAST_PLAYED_SPELL))) * 3


class TSC_087e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_620:
    """恶鞭海妖 - 4费 2/5
    在你使用一张纳迦牌后，复原两个法力水晶（然后切换至法术牌）"""
    events = Play(CONTROLLER, NAGA).after(
        (GainMana(CONTROLLER, 2), Morph(SELF, "TSC_620t"))
    )


class TSC_642:
    """海沟勘测机 - 1费 2/1
    战吼：探底。如果选中的是机械牌，抽取这张牌"""
    play = (Dredge(CONTROLLER), Find(DREDGED_CARD + MECH)) & ForceDraw(DREDGED_CARD)


class TSC_643:
    """法术卷积者 - 2费 2/3
    战吼：如果你在本牌在你手中时施放过法术，发现一张法术牌"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_643e")
    play = (Find(SELF + POWERED_UP), GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomSpell())))


class TSC_643e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_776:
    """艾萨拉的清道夫 - 3费 3/4
    战吼：将一张"沉没的清道夫"置于你的牌库底"""
    play = ShuffleIntoDeck(CONTROLLER, "TSC_776t", position='bottom')


class TSC_948:
    """艾萨拉的恩赐 - 2费法术
    抽一张牌。如果你在本牌在你手中时使用过纳迦牌，再抽一张"""
    powered_up = Find(FRIENDLY_HAND + NAGA) & Buff(SELF, "TSC_948e")
    play = (Draw(CONTROLLER), Find(SELF + POWERED_UP)) & Draw(CONTROLLER)


class TSC_948e:
    """已使用纳迦牌标记"""
    tags = {GameTag.POWERED_UP: True}

