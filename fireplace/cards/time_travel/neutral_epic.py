"""
穿越时间流 - 中立 - EPIC
"""
from ..utils import *
from .rewind_helpers import create_rewind_point


class TIME_004:
    """时光流汇扫荡者 - Conflux Crasher
    回溯。战吼：随机对一个敌人造成7点伤害。
    
    Rewind. Battlecry: Deal 7 damage to a random enemy.
    """
    requirements = {}
    
    def play(self):
        # 1. 创建回溯点（快照）
        create_rewind_point(self.game)
        
        # 2. 随机对一个敌人造成7点伤害
        yield Hit(RANDOM(ENEMY_CHARACTERS), 7)


class TIME_041:
    """未来主义先祖 - Futuristic Forefather
    嘲讽。战吼：检视三张卡牌。猜中来自你对手手牌中的卡牌，则获得+4生命值。
    
    Taunt. Battlecry: Look at 3 cards. Guess which one is in your opponent's hand to gain +4 Health.
    
    官方机制：展示1张来自对手手牌的卡牌 + 2张来自对手牌库的卡牌
    """
    requirements = {}
    
    def play(self):
        # 检查对手是否有手牌
        if not self.controller.opponent.hand:
            # 如果对手没有手牌，无法进行猜测
            return
        
        # 从对手手牌中随机选择一张
        opponent_card = self.game.random.choice(self.controller.opponent.hand)
        
        # 从对手牌库中随机选择两张作为干扰项
        deck_cards = []
        if len(self.controller.opponent.deck) >= 2:
            # 有至少2张牌库卡牌
            deck_cards = self.game.random.sample(list(self.controller.opponent.deck), 2)
        elif len(self.controller.opponent.deck) == 1:
            # 只有1张牌库卡牌，补充一张随机卡牌
            deck_cards = [self.controller.opponent.deck[0]]
            deck_cards.append(RandomCard())
        else:
            # 没有牌库卡牌，使用两张随机卡牌
            deck_cards = [RandomCard(), RandomCard()]
        
        # 组合三张卡牌（1张手牌 + 2张牌库/随机）
        cards = [opponent_card.id] + [c.id if hasattr(c, 'id') else c for c in deck_cards]
        
        # 随机打乱顺序
        self.game.random.shuffle(cards)
        
        # 让玩家选择
        choice = yield GenericChoice(
            self.controller,
            cards=cards
        )
        
        # 检查是否猜中（选中的是对手手牌中的那张）
        if choice and choice[0] == opponent_card.id:
            # 猜中了，获得+4生命值
            yield Buff(self, "TIME_041e")


class TIME_041e:
    """未来主义先祖 - +4生命值"""
    max_health = 4



class TIME_052:
    """琥珀守卫 - Amber Warden
    嘲讽。亡语：召唤一个来自过去的随机随从。
    
    Taunt. Deathrattle: Summon a random minion from the past.
    """
    # 嘲讽在卡牌定义中通过标签实现
    # 亡语：召唤一个随机随从
    deathrattle = Summon(CONTROLLER, RandomMinion())


class TIME_061:
    """越时因果 - Timeless Causality
    战吼：反转你的牌库顺序。
    
    Battlecry: Reverse the order of your deck.
    """
    requirements = {}
    
    def play(self):
        # 反转牌库顺序
        # 获取当前牌库的所有卡牌
        deck_cards = list(self.controller.deck)
        
        # 如果牌库为空或只有一张牌，无需反转
        if len(deck_cards) <= 1:
            return
        
        # 反转顺序：将牌库中的卡牌按相反顺序重新排列
        # fireplace 的牌库是一个列表，我们需要反转它
        # 使用 Shuffle action 或直接操作列表
        # 由于 fireplace 没有直接的"反转牌库"action，我们手动操作
        
        # 清空牌库
        for card in deck_cards:
            card.zone = Zone.SETASIDE
        
        # 按反转顺序重新加入牌库
        for card in reversed(deck_cards):
            card.zone = Zone.DECK


class TIME_102:
    """昼夜节律术师 - Circadiamancer
    战吼：随机获取一张法力值消耗为（8）的随从牌。在你的回合开始时，使其法力值消耗减少（1）点。
    
    Battlecry: Add a random 8-Cost minion to your hand. At the start of your turns, reduce its Cost by (1).
    """
    requirements = {}
    
    def play(self):
        # 随机获取一张8费随从
        card = yield Give(self.controller, RandomMinion(cost=8))
        
        # 给这张卡添加标记buff，用于在回合开始时减费
        if card:
            yield Buff(card, "TIME_102e")


class TIME_102e:
    """昼夜节律术师 - 回合开始减1费"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 在己方回合开始时，减少1费
    events = [
        OWN_TURN_BEGIN.on(
            lambda self, entity: Buff(OWNER, "TIME_102e2")
        )
    ]


class TIME_102e2:
    """昼夜节律术师 - 减少1费"""
    cost = -1


