"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_306:
    """Sigil of Flame - 烈焰咒符
    At the start of your next turn, deal $3 damage to all minions.
    在你的下个回合开始时，对所有随从造成$3点伤害。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "BAR_306t")


class BAR_306t:
    """Sigil of Flame (dormant)"""
    tags = {
        GameTag.DORMANT: True,
    }
    events = OWN_TURN_BEGIN.on(
        Hit(ALL_MINIONS, 3),
        Destroy(SELF)
    )


class BAR_325:
    """Razorboar - 剃刀野猪
    <b>Deathrattle:</b> Summon a <b>Deathrattle</b> minion that costs (3) or less from your hand.
    亡语：从你的手牌中召唤一个法力值消耗小于或等于（3）点的亡语随从。
    """
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + DEATHRATTLE + (COST <= 3)))


class BAR_326:
    """Razorfen Beastmaster - 剃刀沼泽兽王
    <b>Deathrattle:</b> Summon a <b>Deathrattle</b> minion that costs (4) or less from your hand.
    亡语：从你的手牌中召唤一个法力值消耗小于或等于（4）点的亡语随从。
    """
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + DEATHRATTLE + (COST <= 4)))


class BAR_327:
    """Vile Call - 邪恶召唤
    Summon two 2/2 Demons with <b>Lifesteal</b>.
    召唤两个2/2并具有吸血的恶魔。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_327t") * 2


class BAR_328:
    """Vengeful Spirit - 复仇之魂
    <b>Outcast:</b> Draw 2 <b>Deathrattle</b> minions.
    流放：抽两张亡语随从牌。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    outcast = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE)),
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE)),
    )


class BAR_329:
    """Death Speaker Blackthorn - 亡语者布莱克松
    <b>Battlecry:</b> Summon 3 <b>Deathrattle</b> minions that cost (5) or less from your deck.
    战吼：从你的牌库中召唤三个法力值消耗小于或等于（5）点的亡语随从。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE + (COST <= 5))) * 3


class BAR_330:
    """Tuskpiercer - 獠牙锥刃
    [x]<b>Deathrattle:</b> Draw a <b>Deathrattle</b> minion.
    亡语：抽一张亡语随从牌。
    """
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE))


class BAR_333:
    """Kurtrus Ashfallen - 库尔特鲁斯·陨烬
    [x]<b>Battlecry:</b> Attack the left and right-most enemy minions.
    <b>Outcast:</b> <b>Immune</b> this turn.
    战吼：攻击最左边和最右边的敌方随从。流放：在本回合中获得免疫。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Find(ENEMY_MINIONS) & Attack(FRIENDLY_HERO, LEFTMOST(ENEMY_MINIONS)),
        Find(ENEMY_MINIONS) & Attack(FRIENDLY_HERO, RIGHTMOST(ENEMY_MINIONS)),
    )
    outcast = Buff(FRIENDLY_HERO, "BAR_333e")


class BAR_333e:
    """Kurtrus Immune buff"""
    tags = {
        GameTag.CANT_BE_DAMAGED: True,
        GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True,
    }
    events = OWN_TURN_END.on(Destroy(SELF))


class BAR_705:
    """Sigil of Silence - 沉默咒符
    At the start of your next turn, <b>Silence</b> all enemy minions.
    在你的下个回合开始时，沉默所有敌方随从。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "BAR_705t")


class BAR_705t:
    """Sigil of Silence (dormant)"""
    tags = {
        GameTag.DORMANT: True,
    }
    events = OWN_TURN_BEGIN.on(
        Silence(ENEMY_MINIONS),
        Destroy(SELF)
    )


class BAR_891:
    """Fury (Rank 1) - 怒火（等级1）
    Give your hero +2 Attack this turn. <i>(Upgrades when you have 5 Mana.)</i>
    使你的英雄在本回合中获得+2攻击力。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_891t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_HERO, "BAR_891e")


class BAR_891e:
    """Fury (Rank 1) buff"""
    tags = {
        GameTag.ATK: 2,
    }
    events = OWN_TURN_END.on(Destroy(SELF))


class BAR_891t:
    """Fury (Rank 2) - 怒火（等级2）
    Give your hero +3 Attack this turn. <i>(Upgrades when you have 10 Mana.)</i>
    使你的英雄在本回合中获得+3攻击力。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_891t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_HERO, "BAR_891t_e")


class BAR_891t_e:
    """Fury (Rank 2) buff"""
    tags = {
        GameTag.ATK: 3,
    }
    events = OWN_TURN_END.on(Destroy(SELF))


class BAR_891t2:
    """Fury (Rank 3) - 怒火（等级3）
    Give your hero +4 Attack this turn.
    使你的英雄在本回合中获得+4攻击力。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_HERO, "BAR_891t2_e")


class BAR_891t2_e:
    """Fury (Rank 3) buff"""
    tags = {
        GameTag.ATK: 4,
    }
    events = OWN_TURN_END.on(Destroy(SELF))


class WC_003:
    """Sigil of Summoning - 召唤咒符
    At the start of your next turn, summon two 2/2 Demons with <b>Taunt</b>.
    在你的下个回合开始时，召唤两个2/2并具有嘲讽的恶魔。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "WC_003t")


class WC_003t:
    """Sigil of Summoning (dormant)"""
    tags = {
        GameTag.DORMANT: True,
    }
    events = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, "WC_003t2") * 2,
        Destroy(SELF)
    )


class WC_040:
    """Taintheart Tormenter - 污心拷问者
    <b>Taunt</b>
    Your opponent's spells cost (2) more.
    嘲讽。你的对手的法术牌法力值消耗增加（2）点。
    """
    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +2})


class WC_701:
    """Felrattler - 邪能响尾蛇
    [x]<b>Rush</b>
    <b>Deathrattle:</b> Deal 1 damage to all enemy minions.
    突袭。亡语：对所有敌方随从造成1点伤害。
    """
    deathrattle = Hit(ENEMY_MINIONS, 1)


