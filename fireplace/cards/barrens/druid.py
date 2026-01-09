"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_533:
    """Thorngrowth Sentries - 荆棘护卫
    Summon two 1/2 Turtles with Taunt.
    召唤两个1/2并具有嘲讽的乌龟。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_533t") * 2


class BAR_534:
    """Pride's Fury - 狮群之怒
    Give your minions +1/+3.
    使你的所有随从获得+1/+3。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_MINIONS, "BAR_534e")


class BAR_534e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
    }


class BAR_535:
    """Thickhide Kodo - 厚皮科多兽
    Taunt. Deathrattle: Gain 5 Armor.
    嘲讽。亡语：获得5点护甲值。
    """
    deathrattle = GainArmor(FRIENDLY_HERO, 5)


class BAR_536:
    """Living Seed (Rank 1) - 生命之种（等级1）
    Draw a Beast. Reduce its Cost by (1). (Upgrades when you have 5 Mana.)
    抽一张野兽牌。使其法力值消耗减少（1）点。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_536t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + BEAST)
        if cards:
            for card in cards:
                if card:
                    yield Buff(card, "BAR_536e")


class BAR_536e:
    tags = {
        GameTag.COST: -1,
    }


class BAR_536t:
    """Living Seed (Rank 2) - 生命之种（等级2）
    Draw a Beast. Reduce its Cost by (2). (Upgrades when you have 10 Mana.)
    抽一张野兽牌。使其法力值消耗减少（2）点。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_536t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + BEAST)
        if cards:
            for card in cards:
                if card:
                    yield Buff(card, "BAR_536t_e")


class BAR_536t_e:
    tags = {
        GameTag.COST: -2,
    }


class BAR_536t2:
    """Living Seed (Rank 3) - 生命之种（等级3）
    Draw a Beast. Reduce its Cost by (3).
    抽一张野兽牌。使其法力值消耗减少（3）点。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + BEAST)
        if cards:
            for card in cards:
                if card:
                    yield Buff(card, "BAR_536t2_e")


class BAR_536t2_e:
    tags = {
        GameTag.COST: -3,
    }


class BAR_537:
    """Razormane Battleguard - 钢鬃卫兵
    The first Taunt minion you play each turn costs (2) less.
    你每回合打出的第一张嘲讽随从牌的法力值消耗减少（2）点。
    """
    events = OWN_TURN_BEGIN.on(SetTag(SELF, {enums.ACTIVATIONS_THIS_TURN: 0}))
    update = (
        Find(SELF + (ACTIVATIONS_THIS_TURN == 0))
        & Refresh(FRIENDLY_HAND + MINION + TAUNT, {GameTag.COST: -2})
    )


class BAR_538:
    """Druid of the Plains - 平原德鲁伊
    Rush. Frenzy: Transform into a 6/7 Kodo with Taunt.
    突袭。暴怒：变形成为一个6/7并具有嘲讽的科多兽。
    """
    frenzy = Morph(SELF, "BAR_538t")


class BAR_539:
    """Celestial Alignment - 超凡之盟
    Set your Mana Crystals to 0. Set the Cost of cards in your hand and deck to (1).
    将你的法力水晶设置为0。将你手牌和牌库中所有卡牌的法力值消耗设置为（1）点。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        SetMana(CONTROLLER, 0),
        Buff(FRIENDLY_HAND, "BAR_539e"),
        Buff(FRIENDLY_DECK, "BAR_539e"),
    )


class BAR_539e:
    tags = {
        GameTag.COST: SET(1),
    }


class BAR_540:
    """Plaguemaw the Rotting - 腐烂的普雷莫尔
    After a friendly minion with Taunt dies, summon a new copy of it without Taunt.
    在一个友方嘲讽随从死亡后，召唤一个它的新复制，且不具有嘲讽。
    """
    events = Death(FRIENDLY + MINION + TAUNT).on(
        Summon(CONTROLLER, Copy(Death.ENTITY)).then(
            SetTag(Summon.CARD, {GameTag.TAUNT: False})
        )
    )


class BAR_549:
    """Mark of the Spikeshell - 尖壳印记
    Give a minion +2/+2. If it has Taunt, add a copy of it to your hand.
    使一个随从获得+2/+2。如果它具有嘲讽，将它的一张复制置入你的手牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(TARGET, "BAR_549e"),
        Find(TARGET + TAUNT) & Give(CONTROLLER, Copy(TARGET)),
    )


class BAR_549e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class BAR_720:
    """Guff Runetotem - 古夫·符文图腾
    After you cast a Nature spell, give another friendly minion +2/+2.
    在你施放一个自然法术后，随机使另一个友方随从获得+2/+2。
    """
    events = Play(CONTROLLER, SPELL + NATURE).after(
        Buff(RANDOM(FRIENDLY_MINIONS - SELF), "BAR_720e")
    )


class BAR_720e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class WC_004:
    """Fangbound Druid - 牙缚德鲁伊
    Taunt. Deathrattle: Reduce the Cost of a Beast in your hand by (2).
    嘲讽。亡语：使你手牌中的一张野兽牌的法力值消耗减少（2）点。
    """
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "WC_004e")


class WC_004e:
    tags = {
        GameTag.COST: -2,
    }


class WC_006:
    """Lady Anacondra - 安娜科德拉
    Your Nature spells cost (2) less.
    你的自然法术牌的法力值消耗减少（2）点。
    """
    update = Refresh(FRIENDLY_HAND + SPELL + NATURE, {GameTag.COST: -2})


class WC_036:
    """Deviate Dreadfang - 变异尖牙风蛇
    After you cast a Nature spell, summon a 4/2 Viper with Rush.
    在你施放一个自然法术后，召唤一个4/2并具有突袭的毒蛇。
    """
    events = Play(CONTROLLER, SPELL + NATURE).after(
        Summon(CONTROLLER, "WC_036t")
    )


