"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_077:
    """Kargal Battlescar - 卡加尔·战痕
    Battlecry: Summon a 5/5 Lookout for each Watch Post you've summoned this game.
    战吼：每有一个你在本局对战中召唤过的哨所，便召唤一个5/5的瞭望者。
    """
    play = Summon(CONTROLLER, "BAR_077t") * Count(FRIENDLY + SUMMONED + WATCHPOST)


class BAR_078:
    """Blademaster Samuro - 剑圣萨穆罗
    Rush. Frenzy: Deal damage equal to this minion's Attack to all enemy minions.
    突袭。暴怒：对所有敌方随从造成等同于该随从攻击力的伤害。
    """
    frenzy = Hit(ENEMY_MINIONS, ATK(SELF))


class BAR_079:
    """Kazakus, Golem Shaper - 魔像师卡扎库斯
    Battlecry: If your deck has no 4-Cost cards, build a custom Golem.
    战吼：如果你的牌库中没有法力值消耗为4点的牌，创造一个自定义魔像。
    
    简化实现：给予玩家一个随机 Golem 而不是复杂的选择过程
    """
    powered_up = -Find(FRIENDLY_DECK + (COST == 4))
    
    def play(self):
        # 检查是否符合条件
        has_4_cost = any(card.cost == 4 for card in self.controller.deck)
        if not has_4_cost:
            # 简化实现：随机召唤一个1/1, 5/5 或 10/10 的魔像
            golem_sizes = [
                ("BAR_079_Golem_1", 1, 1),  # 1费魔像
                ("BAR_079_Golem_5", 5, 5),  # 5费魔像
                ("BAR_079_Golem_10", 10, 10), # 10费魔像
            ]
            size = self.game.random.choice(golem_sizes)
            yield Summon(CONTROLLER, size[0])


# 魔像 Token 卡牌（简化版本）
@custom_card
class BAR_079_Golem_1:
    """1费魔像"""
    tags = {
        GameTag.CARDNAME: "Golem (1/1)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 1,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


@custom_card
class BAR_079_Golem_5:
    """5费魔像"""
    tags = {
        GameTag.CARDNAME: "Golem (5/5)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 5,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True,
    }


@custom_card
class BAR_079_Golem_10:
    """10费魔像"""
    tags = {
        GameTag.CARDNAME: "Golem (10/10)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 10,
        GameTag.ATK: 10,
        GameTag.HEALTH: 10,
        GameTag.TAUNT: True,
        GameTag.RUSH: True,
    }


class BAR_080:
    """Shadow Hunter Vol'jin - 暗影猎手沃金
    Battlecry: Choose a minion. Swap it with a random one in its owner's hand.
    战吼：选择一个随从。将其与其拥有者手牌中的一个随机随从交换。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        if self.target:
            # 将目标随从弹回手牌
            yield Bounce(self.target)
            # 从目标拥有者的手牌中召唤一个随机随从
            owner = self.target.controller
            hand_minions = [c for c in owner.hand if c.type == CardType.MINION]
            if hand_minions:
                minion = self.game.random.choice(hand_minions)
                yield Summon(owner, minion)


class BAR_721:
    """Mankrik - 曼科里克
    Battlecry: Help Mankrik find his wife! She was last seen somewhere in your deck.
    战吼：帮助曼科里克找到他的妻子！她最后一次被看到是在你的牌库中某处。
    """
    play = Shuffle(CONTROLLER, "BAR_721t")


class BAR_721t:
    """Olgra, Mankrik's Wife - 奥尔格拉，曼科里克的妻子
    Battlecry: Deal 3 damage to all enemies.
    战吼：对所有敌人造成3点伤害。
    """
    play = Hit(ENEMY_CHARACTERS, 3)


class WC_030:
    """Mutanus the Devourer - 吞噬者穆坦努斯
    Battlecry: Eat a minion in your opponent's hand. Gain its stats.
    战吼：吞噬你对手手牌中的一个随从。获得其属性值。
    """
    play = (
        Destroy(RANDOM(ENEMY_HAND + MINION)).then(
            Buff(SELF, "WC_030e", atk=ATK(Destroy.TARGET), max_health=HEALTH(Destroy.TARGET))
        )
    )


class WC_030e:
    """Mutanus buff"""
    pass


class WC_035:
    """Archdruid Naralex - 大德鲁伊纳拉雷克斯
    Dormant for 2 turns. While Dormant, add a Dream card to your hand at the end of your turn.
    休眠2回合。在休眠期间，在你的回合结束时，将一张梦境牌置入你的手牌。
    """
    tags = {
        GameTag.DORMANT: True,
    }
    progress_total = 2
    dormant_events = OWN_TURN_END.on(
        Give(CONTROLLER, RandomID("DREAM_01", "DREAM_02", "DREAM_03", "DREAM_04", "DREAM_05")),
        AddProgress(SELF, SELF, 1),
    )
    reward = SetTags(SELF, {GameTag.DORMANT: False})


