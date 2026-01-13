"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_910:
    """Grimoire of Sacrifice - 牺牲魔典
    Destroy a friendly minion. Deal $2 damage to all enemy minions.
    摧毁一个友方随从。对所有敌方随从造成$2点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Destroy(TARGET), Hit(ENEMY_MINIONS, 2)


class BAR_911:
    """Soul Rend - 灵魂撕裂
    Deal $5 damage to all minions. Destroy a card in your deck for each killed.
    对所有随从造成$5点伤害。每有一个随从死亡,便摧毁你牌库中的一张牌。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        # 记录造成伤害前场上的随从
        minions_before = list(self.game.board)
        yield Hit(ALL_MINIONS, 5)
        # 计算死亡的随从数量
        minions_after = list(self.game.board)
        killed_count = len(minions_before) - len(minions_after)
        # 摧毁相应数量的牌库卡牌
        for _ in range(killed_count):
            if self.controller.deck:
                yield Destroy(RANDOM(FRIENDLY_DECK))


class BAR_912:
    """Apothecary's Caravan - 药剂师车队
    At the start of your turn, summon a 1-Cost minion from your deck.
    在你的回合开始时，从你的牌库中召唤一个法力值消耗为1点的随从。
    """
    events = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == 1)))
    )


class BAR_913:
    """Altar of Fire - 火焰祭坛
    Destroy the top 3 cards of each deck.
    摧毁双方牌库顶的3张牌。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Destroy(TOP(FRIENDLY_DECK, 3)),
        Destroy(TOP(ENEMY_DECK, 3)),
    )


class BAR_914:
    """Imp Swarm (Rank 1) - 小鬼集群（等级1）
    Summon a 3/2 Imp. (Upgrades when you have 5 Mana.)
    召唤一个3/2的小鬼。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_914t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_914t")


class BAR_914t:
    """Imp Swarm (Rank 2) - 小鬼集群（等级2）
    Summon two 3/2 Imps. (Upgrades when you have 10 Mana.)
    召唤两个3/2的小鬼。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_914t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_914t3") * 2


class BAR_914t2:
    """Imp Swarm (Rank 3) - 小鬼集群（等级3）
    Summon three 3/2 Imps.
    召唤三个3/2的小鬼。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_914t4") * 3


class BAR_915:
    """Kabal Outfitter - 暗金教物资官
    Battlecry and Deathrattle: Give another random friendly minion +1/+1.
    战吼和亡语：随机使另一个友方随从获得+1/+1。
    """
    play = Buff(RANDOM(FRIENDLY_MINIONS - SELF), "BAR_915e")
    deathrattle = Buff(RANDOM_FRIENDLY_MINION, "BAR_915e")


class BAR_915e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_916:
    """Blood Shard Bristleback - 血岩碎片刺背野猪人
    Lifesteal. Battlecry: If your deck contains 10 or fewer cards, deal 6 damage to a minion.
    吸血。战吼：如果你的牌库中有10张或更少的牌，对一个随从造成6点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = Count(FRIENDLY_DECK) <= 10
    play = powered_up & Hit(TARGET, 6)


class BAR_917:
    """Barrens Scavenger - 贫瘠之地拾荒者
    Taunt. Costs (1) while your deck has 10 or fewer cards.
    嘲讽。当你的牌库中有10张或更少的牌时，法力值消耗为（1）点。
    """
    cost_mod = (Count(FRIENDLY_DECK) <= 10) & SET(1)


class BAR_918:
    """Tamsin Roame - 塔姆辛·罗姆
    Whenever you cast a Shadow spell that costs (1) or more, add a copy to your hand that costs (0).
    每当你施放一个法力值消耗大于或等于（1）点的暗影法术时，将一张法力值消耗为（0）点的复制置入你的手牌。
    """
    events = Play(CONTROLLER, SPELL + SHADOW + (COST >= 1)).after(
        Give(CONTROLLER, Copy(Play.CARD)).then(
            Buff(Give.CARD, "BAR_918e")
        )
    )


class BAR_918e:
    tags = {
        GameTag.COST: SET(0),
    }


class BAR_919:
    """Neeru Fireblade - 尼尔鲁·火刃
    Battlecry: If your deck is empty, open a portal that fills your board with 3/2 Imps each turn.
    战吼：如果你的牌库为空，开启一个传送门，每回合用3/2的小鬼填满你的战场。
    """
    powered_up = Count(FRIENDLY_DECK) == 0
    play = powered_up & Summon(CONTROLLER, "BAR_919t")


class BAR_919t:
    """Nether Portal"""
    tags = {
        GameTag.DORMANT: True,
    }
    events = OWN_TURN_BEGIN.on(
        lambda self, player: [Summon(CONTROLLER, "BAR_919t2") for _ in range(7 - len(self.controller.field))]
    )


class WC_021:
    """Unstable Shadow Blast - 不稳定的暗影震爆
    Deal $6 damage to a minion. Excess damage hits your hero.
    对一个随从造成$6点伤害。超量伤害会对你的英雄造成伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 6), Hit(FRIENDLY_HERO, Excess(TARGET, 6))


class WC_022:
    """Final Gasp - 临终之息
    Deal $1 damage to a minion. If it dies, summon a 2/2 Adventurer with a random bonus effect.
    对一个随从造成$1点伤害。如果其死亡，召唤一个2/2并具有随机奖励效果的冒险者。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1).then(
        Dead(Hit.TARGET) & Summon(CONTROLLER, RandomID(
            "WC_034t", "WC_034t2", "WC_034t3", "WC_034t4",
            "WC_034t5", "WC_034t6", "WC_034t7", "WC_034t8"
        ))
    )


class WC_023:
    """Stealer of Souls - 灵魂窃贼
    The first card you draw each turn costs Health instead of Mana.
    你每回合抽的第一张牌用生命值而非法力值来支付其费用。
    """
    events = (
        OWN_TURN_BEGIN.on(SetTags(SELF, {enums.ACTIVATIONS_THIS_TURN: 0})),
        Draw(CONTROLLER).after(
            Find(SELF + (ACTIVATIONS_THIS_TURN == 0)) & (
                Buff(Draw.CARD, "WC_023e"),
                AddProgress(SELF, SELF, 1, "activations_this_turn"),
            )
        ),
    )


class WC_023e:
    """Costs Health"""
    tags = {
        enums.HEALTH_COST: True,
    }


