"""
穿越时间流 - ROGUE
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_710:
    """暴徒双人组 - Troubled Double
    3/3 随从
    **潜行。连击：**召唤一个本随从的复制。
    
    Stealth. Combo: Summon a copy of this.
    """
    # Mechanics: COMBO, STEALTH
    # Stealth 由卡牌定义中的标签处理
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 连击效果：召唤自身的复制
            if self.controller.combo:
                yield Summon(self.controller, ExactCopy(SELF))
        
        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_712:
    """诛灭暴君 - Dethrone
    7费 暗影法术
    消灭一个随从。**连击：**随机召唤一个法力值消耗为（8）点的随从。
    
    Destroy a minion. Combo: Summon a random 8-Cost minion.
    """
    # Mechanics: COMBO
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 消灭目标随从
        yield Destroy(TARGET)
        
        # 连击效果：召唤随机8费随从
        if self.controller.combo:
            yield Summon(self.controller, RandomMinion(cost=8))


class TIME_770:
    """快进 - Fast Forward
    4费 法术
    抽两张牌。选择其中一张，使其法力值消耗减少（2）点。
    
    Draw 2 cards. Pick one to have its Cost reduced by (2).
    """
    def play(self):
        # 抽两张牌
        drawn_cards = []
        for _ in range(2):
            cards = yield Draw(self.controller)
            if cards:
                drawn_cards.extend(cards)
        
        # 如果抽到了牌，让玩家选择一张减费
        if drawn_cards:
            # 过滤出在手牌中的卡牌
            cards_in_hand = [card for card in drawn_cards if card.zone == Zone.HAND]
            
            if cards_in_hand:
                # 让玩家选择一张卡牌
                # 使用 GenericChoice 让玩家选择
                choice = yield GenericChoice(self.controller, cards=cards_in_hand)
                
                if choice:
                    # 给选中的卡牌减少2费
                    yield Buff(choice[0], "TIME_770e")


class TIME_770e:
    """快进 - 减少2费"""
    tags = {GameTag.COST: -2}


# RARE

class TIME_001:
    """时空飞刃 - Chrono Daggers
    3费 法术
    **回溯**。投掷3把飞刀，每把对随机敌人造成$2点伤害。
    
    Rewind. Throw 3 knives at random enemies that deal $2 damage each.
    """
    # Mechanics: REWIND
    def play(self):
        
        # 投掷3把飞刀，每把对随机敌人造成2点伤害
        for _ in range(3):
            yield Hit(RANDOM(ENEMY_CHARACTERS), 2)


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_039:
    """似曾相识 - Deja Vu
    1费 法术
    **发现**对手手牌中一张牌的复制。其法力值消耗减少（1）点。
    
    Discover a copy of a card in your opponent's hand. It costs (1) less.
    """
    # Mechanics: DISCOVER
    def play(self):
        # 发现对手手牌中的一张牌
        if self.controller.opponent.hand:
            # 从对手手牌中发现
            discovered = yield Discover(self.controller, RandomCard(ENEMY_HAND))
            
            # 给发现的牌减少1费
            if discovered:
                yield Buff(discovered, "TIME_039e")


class TIME_039e:
    """似曾相识 - 减少1费"""
    tags = {GameTag.COST: -1}


class TIME_711:
    """闪回 - Flashback
    2费 法术
    随机召唤两个来自过去的法力值消耗为（1）点的随从。**连击：**使其获得+1攻击力。
    
    Summon two random 1-Cost minions from the past. Combo: With +1 Attack.
    """
    # Mechanics: COMBO
    def play(self):
        # 召唤两个随机1费随从
        minions = []
        for _ in range(2):
            summoned = yield Summon(self.controller, RandomMinion(cost=1))
            if summoned:
                minions.extend(summoned)
        
        # 连击效果：给召唤的随从+1攻击力
        if self.controller.combo and minions:
            for minion in minions:
                yield Buff(minion, "TIME_711e")


class TIME_711e:
    """闪回 - +1攻击力"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


# EPIC

class TIME_036:
    """王室线人 - Royal Informant
    3费 2/4 随从
    **战吼：**查看对手手牌最右边的卡牌。获取其复制或使其法力值消耗增加（2）点。
    
    Battlecry: Look at the right-most card in your opponent's hand. Either get a copy of it or increase its Cost by (2).
    """
    # Mechanics: BATTLECRY
    def play(self):
        # 获取对手手牌最右边的卡牌
        if self.controller.opponent.hand:
            # 手牌最右边是索引 -1
            rightmost_card = self.controller.opponent.hand[-1]
            
            # 让玩家选择：获取复制 或 增加费用
            # 使用 GenericChoice 让玩家选择
            choice = yield GenericChoice(self.controller, cards=[
                "TIME_036t1",  # 获取复制
                "TIME_036t2",  # 增加费用
            ])
            
            if choice:
                if choice[0] == "TIME_036t1":
                    # 获取复制
                    yield Give(self.controller, ExactCopy(rightmost_card))
                elif choice[0] == "TIME_036t2":
                    # 增加费用
                    yield Buff(rightmost_card, "TIME_036e")


class TIME_036e:
    """王室线人 - 增加2费"""
    tags = {GameTag.COST: 2}


class TIME_876:
    """神秘变形者 - Shapeshifter
    1费 1/1 随从
    在你的手牌中时,每回合变形成对手手牌中的一个随机随从。
    
    Each turn this is in your hand, transform into a random minion in your opponent's hand.
    """
    # 在回合开始时触发变形
    # 需要在手牌中才会触发
    
    def _transform_to_opponent_minion(self):
        """变形成对手手牌中的随机随从"""
        # 获取对手手牌中的随从
        opponent_minions = [
            card for card in self.controller.opponent.hand
            if card.type == CardType.MINION
        ]
        
        if opponent_minions:
            # 随机选择一个随从并变形
            import random
            target = random.choice(opponent_minions)
            yield Morph(SELF, target.id)
    
    class Hand:
        """在手牌时的事件监听"""
        events = OWN_TURN_BEGIN.on(
            lambda self, player: self.owner._transform_to_opponent_minion()
        )



# LEGENDARY

class TIME_713:
    """时空上将钩尾 - Time Adm'ral Hooktail
    5费 4/6 龙/海盗
    **战吼：**为你的对手召唤一个0/8的宝箱。<i>里面装满了硬币！</i>
    
    Battlecry: Summon a 0/8 Chest for your opponent. <i>It's FULL of Coins!</i>
    """
    # Mechanics: BATTLECRY
    def play(self):
        # 为对手召唤一个宝箱
        yield Summon(self.controller.opponent, "TIME_713t")


class TIME_875:
    """半兽人迦罗娜 - Garona Halforcen
    4费 5/4 传说随从
    **奇闻。战吼：**如果你的对手持有莱恩国王，消灭他并使对手的生命值减半。
    
    Fabled. Battlecry: If your opponent is holding King Llane, destroy him and cut their Health in half.
    """
    # Mechanics: BATTLECRY, FABLED
    def play(self):
        # 检查对手是否持有莱恩国王（King Llane）
        # King Llane 的 ID 应该是 TIME_875t（Fabled 附带卡牌）
        king_llane = None
        for card in self.controller.opponent.hand:
            if card.id == "TIME_875t":
                king_llane = card
                break
        
        # 如果对手持有莱恩国王
        if king_llane:
            # 1. 消灭莱恩国王
            yield Destroy(king_llane)
            
            # 2. 使对手的生命值减半
            opponent_hero = self.controller.opponent.hero
            current_health = opponent_hero.health
            damage = current_health // 2
            yield Hit(opponent_hero, damage)


