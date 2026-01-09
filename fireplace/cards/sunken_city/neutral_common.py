# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立普通
"""

from ..utils import *

class TID_713:
    """泡泡元素 - 1费 2/4
    在本随从受到刚好一点伤害后，消灭本随从"""
    events = Damage(SELF).on(
        ((Damage.AMOUNT == 1) & Destroy(SELF))
    )


class TSC_001:
    """海军水雷 - 2费 0/2
    亡语：对敌方英雄造成4点伤害"""
    deathrattle = Hit(ENEMY_HERO, 4)


class TSC_002:
    """刺豚拳手 - 3费 3/4
    在你的英雄攻击后，对所有敌人造成1点伤害"""
    events = Attack(FRIENDLY_HERO).after(
        Hit(ALL_ENEMIES, 1)
    )


class TSC_007:
    """潜水跳板船员 - 5费 6/4
    休眠1回合。突袭。攻击时具有免疫"""
    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    tags = {GameTag.RUSH: True}
    events = Attack(SELF).on(Buff(SELF, "TSC_007e"))


class TSC_007e:
    """攻击时免疫"""
    tags = {GameTag.IMMUNE: True}
    events = Attack(OWNER).after(Destroy(SELF))


class TSC_013:
    """潜水泥鳞鱼人 - 3费 2/4
    休眠1回合。突袭，剧毒"""
    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    tags = {GameTag.RUSH: True, GameTag.POISONOUS: True}

class TSC_017:
    """巫婆纳迦 - 4费 4/4
    战吼：如果你在本牌在你手中时施放过法术，造成3点伤害"""
    powered_up = Find(FRIENDLY_HAND + SPELL) & Buff(SELF, "TSC_017e")
    play = (Find(SELF + POWERED_UP), Hit(TARGET, 3))


class TSC_017e:
    """已施放法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_020:
    """野蛮的女巫 - 6费 3/7
    嘲讽。战吼：交换每个玩家手牌中各一张随机法术牌的法力值消耗"""
    tags = {GameTag.TAUNT: True}
    play = (
        SwapCost(RANDOM(FRIENDLY_HAND + SPELL), RANDOM(ENEMY_HAND + SPELL))
    )



class TSC_034:
    """鳄鱼人掠夺者 - 5费 4/3
    战吼：抽三张鱼人牌"""
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC)) * 3


class TSC_053:
    """虹彩闪鳞纳迦 - 2费 2/3
    法术伤害+1"""
    tags = {GameTag.SPELLPOWER: 1}

class TSC_632:
    """械钳虾 - 1费 1/1
    圣盾。战吼：随机使你手牌中的一张机械牌获得+1/+1"""
    tags = {GameTag.DIVINE_SHIELD: True}
    play = Buff(RANDOM(FRIENDLY_HAND + MECH), "TSC_632e")


class TSC_632e:
    """机械增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_638:
    """食人鱼集群 - 1费 1/1
    突袭。在你召唤一个食人鱼集群后，获得+1攻击力"""
    tags = {GameTag.RUSH: True}
    events = Summon(CONTROLLER, SELF).after(
        Buff(SELF, "TSC_638e")
    )


class TSC_638e:
    """食人鱼集群增益"""
    tags = {GameTag.ATK: 1}


class TSC_640:
    """堡礁行者 - 3费 3/2
    战吼和亡语：召唤一个1/1的食人鱼集群"""
    play = Summon(CONTROLLER, "TSC_638")
    deathrattle = Summon(CONTROLLER, "TSC_638")


class TSC_646:
    """海底侦察兵 - 3费 2/4
    战吼：如果你控制任何机械，则召唤两条2/1的机械鱼"""
    play = Find(FRIENDLY_MINIONS + MECH) & (
        Summon(CONTROLLER, "TSC_646t") * 2
    )

class TSC_647:
    """潜水俯冲鹈鹕 - 1费 4/1
    休眠1回合。突袭"""
    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    tags = {GameTag.RUSH: True}


class TSC_823:
    """暗水记录员 - 2费 3/2
    战吼：你使用的下一张法术牌法力值消耗减少（1）点"""
    play = Buff(CONTROLLER, "TSC_823e")


class TSC_823e:
    """下一个法术减费"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class TSC_909:
    """拖网海象人 - 2费 2/3
    战吼：探底"""
    play = Dredge(CONTROLLER)

class TSC_911:
    """挖掘专家 - 4费 3/6
    战吼：探底。选中的牌法力值消耗减少（1）点"""
    play = (Dredge(CONTROLLER), Buff(DREDGED_CARD, "TSC_911e"))


class TSC_911e:
    """探底减费"""
    tags = {GameTag.COST: -1}


class TSC_919:
    """艾萨拉的哨兵 - 5费 5/6
    嘲讽。亡语：将一张\"沉没的哨兵\"置于你的牌库底"""
    tags = {GameTag.TAUNT: True}
    deathrattle = ShuffleIntoDeck(CONTROLLER, "TSC_919t", position='bottom')


class TSC_928:
    """安保自动机 - 2费 1/3
    在你召唤一个机械后，获得+1/+1"""
    events = Summon(CONTROLLER, MECH).after(
        Buff(SELF, "TSC_928e")
    )


class TSC_928e:
    """机械增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_935:
    """自私的扇贝 - 4费 7/7
    亡语：你的对手抽两张牌"""
    deathrattle = Draw(OPPONENT) * 2


class TSC_938:
    """宝藏守卫 - 3费 1/5
    嘲讽。亡语：抽一张牌"""
    tags = {GameTag.TAUNT: True}
    deathrattle = Draw(CONTROLLER)

