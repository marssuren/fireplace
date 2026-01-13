# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 中立传说
"""

from ..utils import *

class TID_711:
    """厄祖玛特 - 8费 6/5
    巨型+6。亡语：每有一条厄祖玛特的触须，随机消灭一个敌方随从"""
    colossal_appendages = ["TID_711t"] * 6
    deathrattle = (
        Destroy(RANDOM(ENEMY_MINIONS)) * Count(FRIENDLY_MINIONS + ID("TID_711t"))
    )


class TID_712:
    """猎潮者耐普图隆 - 10费 7/7
    巨型+2，突袭，风怒。每当耐普图隆攻击时，如果你控制着任意耐普图隆之手，改为由手攻击"""
    colossal_appendages = ["TID_712t", "TID_712t2"]
    tags = {GameTag.RUSH: True, GameTag.WINDFURY: True}
    events = Attack(SELF).on(
        Find(FRIENDLY_MINIONS + ID("TID_712t")) & Attack(FRIENDLY_MINIONS + ID("TID_712t"), ATTACK_TARGET)
    )

class TSC_032:
    """剑圣奥卡尼 - 4费 2/6
    战吼：秘密选择一项，当本随从存活时，反制你对手使用的下一张随从牌或法术牌"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 6,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 创建两个选项：反制随从 或 反制法术
        counter_minion = self.controller.card("TSC_032a", source=self)
        counter_spell = self.controller.card("TSC_032b", source=self)
        
        # 使用 SecretChoice 实现秘密选择（对手看不到）
        yield SecretChoice(CONTROLLER, [counter_minion, counter_spell])


class TSC_032a:
    """反制随从选项"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 0}
    
    def play(self):
        # 从场上找到奥卡尼(TSC_032)
        okani_list = [m for m in self.controller.field if m.id == "TSC_032"]
        if okani_list:
            okani = okani_list[0]
            yield Buff(okani, "TSC_032e_minion")


class TSC_032b:
    """反制法术选项"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 0}
    
    def play(self):
        # 从场上找到奥卡尼(TSC_032)
        okani_list = [m for m in self.controller.field if m.id == "TSC_032"]
        if okani_list:
            okani = okani_list[0]
            yield Buff(okani, "TSC_032e_spell")


class TSC_032e_minion:
    """反制随从效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 只有当奥卡尼还在场上时才触发反制
    # 反制对手的下一张随从牌
    events = Play(OPPONENT, MINION).on(
        Find(OWNER + IN_PLAY) & Counter(Play.CARD) & Destroy(SELF)
    )


class TSC_032e_spell:
    """反制法术效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 只有当奥卡尼还在场上时才触发反制
    # 反制对手的下一张法术牌
    events = Play(OPPONENT, SPELL).on(
        Find(OWNER + IN_PLAY) & Counter(Play.CARD) & Destroy(SELF)
    )


class TSC_067:
    """费林大使 - 4费 4/5
    战吼：将3张巨型随从牌置于你的牌库底"""
    play = (
        ShuffleIntoDeck(CONTROLLER, RandomMinion(tag=GameTag.COLOSSAL), position='bottom') * 3
    )

class TSC_641:
    """艾萨拉女王 - 5费 5/5
    战吼：如果你在本牌在你手中时施放过三个法术，选择一项远古圣物"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spells_cast_while_holding = 0
    
    class Hand:
        events = Play(CONTROLLER, SPELL).after(
            lambda self, player, played_card, target: setattr(self, 'spells_cast_while_holding', 
                                               getattr(self, 'spells_cast_while_holding', 0) + 1)
        )
    
    powered_up = lambda self: getattr(self, 'spells_cast_while_holding', 0) >= 3
    
    play = lambda self: (
        Discover(CONTROLLER, ["TSC_641t1", "TSC_641t2", "TSC_641t3", "TSC_641t4"])
        if self.powered_up else []
    )


class TSC_641e:
    """已施放3个法术标记"""
    tags = {GameTag.POWERED_UP: True}


class TSC_649:
    """伊妮·积雷 - 5费 4/4
    战吼：选择一个友方机械，召唤一个它的具有突袭、风怒和圣盾的复制"""
    play = (Summon(CONTROLLER, ExactCopy(TARGET)), Buff(LAST_SUMMONED, "TSC_649e"))


class TSC_649e:
    """机械增强"""
    tags = {GameTag.RUSH: True, GameTag.WINDFURY: True, GameTag.DIVINE_SHIELD: True}


class TSC_908:
    """海中向导芬利爵士 - 1费 1/3
    战吼：将你的手牌和牌库底的牌交换"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
    }
    
    def play(self):
        """
        交换手牌和牌库底部的牌
        
        实现逻辑：
        1. 保存当前手牌（排除芬利自己）
        2. 从牌库底部取出相同数量的牌
        3. 将手牌移到牌库底部
        4. 将取出的牌移到手牌
        
        注意：fireplace 中 deck[0] 是底部，deck[-1] 是顶部
        """
        controller = self.controller
        
        # 保存当前手牌（排除芬利自己，因为他刚被打出）
        hand_cards = [card for card in list(controller.hand) if card != self]
        hand_count = len(hand_cards)
        
        # 如果手牌为空，不需要交换
        if hand_count == 0:
            return
        
        # 从牌库底部取出与手牌数量相同的牌
        deck_bottom_cards = []
        for i in range(min(hand_count, len(controller.deck))):
            if controller.deck:
                # deck[0] 是牌库底部
                card = controller.deck[0]
                # 暂时移到 SETASIDE 区域
                card.zone = Zone.SETASIDE
                deck_bottom_cards.append(card)
        
        # 将手牌移到牌库底部
        for card in hand_cards:
            # 使用 ShuffleIntoDeck action 将卡牌放到牌库底部
            yield ShuffleIntoDeck(controller, card, position='bottom')
        
        # 将之前从牌库底部取出的牌移到手牌
        for card in deck_bottom_cards:
            if len(controller.hand) < controller.max_hand_size:
                yield Give(controller, card)
            else:
                # 如果手牌已满，烧掉这张牌
                card.discard()


