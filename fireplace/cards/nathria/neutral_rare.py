"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_031:
    """Afterlife Attendant - 冥界侍从
    Your <b>Infuse</b> cards also <b>Infuse</b> while in your deck.
    你的<b>注能</b>卡牌在牌库中也能<b>注能</b>。
    """
    # 核心已扩展支持牌库注能机制（actions.py:427-471）
    # 当友方随从死亡时：
    # 1. 检查控制者英雄是否有 MAW_031e buff
    # 2. 如果有，为牌库中的 Infuse 卡充能（与手牌相同）
    # 3. 牌库中的卡只累积充能计数，不触发效果
    # 4. 抽到手牌时已经是充能状态
    update = Buff(FRIENDLY_HERO, "MAW_031e")


class MAW_031e:
    """Afterlife Attendant Aura - 冥界侍从光环"""
    # 标记：牌库中的 Infuse 卡也能充能
    # 核心的 Death action 会检查此标记（已完全实现）
    tags = {enums.CUSTOM_CARDTEXT: 1}


class REV_016:
    """Crooked Cook - 邪恶的厨师
    [x]At the end of your turn, 
if you dealt 3 or more 
damage to the enemy 
hero, draw a card.
    在你的回合结束时，如果你对敌方英雄造成了3点或更多伤害，抽一张牌。
    """
    # 追踪本回合对敌方英雄造成的伤害
    # 使用 Predamage 事件监听伤害
    
    def _track_hero_damage(self, source, target, amount):
        # 累加对敌方英雄的伤害
        if not hasattr(self.controller, 'hero_damage_this_turn'):
            self.controller.hero_damage_this_turn = 0
        self.controller.hero_damage_this_turn += amount
    
    def _check_and_draw(self, source, player):
        # 检查本回合对敌方英雄造成的伤害
        damage_dealt = getattr(self.controller, 'hero_damage_this_turn', 0)
        
        if damage_dealt >= 3:
            yield Draw(CONTROLLER)
    
    def _reset_damage_counter(self, source, player):
        # 回合开始时重置计数器
        if player == self.controller:
            self.controller.hero_damage_this_turn = 0
    
    events = [
        # 监听对敌方英雄的伤害
        Predamage(ENEMY_HERO).on(_track_hero_damage),
        # 回合结束时检查并抽牌
        OWN_TURN_END.on(_check_and_draw),
        # 回合开始时重置计数器
        OWN_TURN_BEGIN.on(_reset_damage_counter),
    ]


class REV_019:
    """Famished Fool - 饥饿的愚人
    <b>Battlecry:</b> Draw a card.
<b>Infuse (4):</b> Draw 3 instead.
    <b>战吼：</b>抽一张牌。<b>注能(4)：</b>改为抽3张牌。
    """
    infuse = 4
    
    def play(self):
        if self.infused:
            # 注能后：抽3张牌
            yield Draw(CONTROLLER) * 3
        else:
            # 未注能：抽1张牌
            yield Draw(CONTROLLER)


class REV_377:
    """Invitation Courier - 邀请函信使
    After a card is added to your hand from another class, copy it.
    在一张其他职业的卡牌被置入你的手牌后，复制它。
    """
    # 这需要追踪卡牌来源和职业
    # 当卡牌被加入手牌时，检查：
    # 1. 卡牌是否来自其他职业
    # 2. 如果是，复制它
    
    def _copy_other_class_card(self, source, player, card):
        # 检查卡牌是否来自其他职业
        my_class = self.controller.hero.card_class
        card_class = card.card_class
        
        # 如果卡牌是其他职业的（非中立且非本职业）
        from hearthstone.enums import CardClass
        if card_class != CardClass.NEUTRAL and card_class != my_class:
            # 复制这张卡
            yield Give(CONTROLLER, Copy(card))
    
    # 监听卡牌被加入手牌的事件
    # 使用 Give action 的 AFTER 事件
    events = Give(CONTROLLER).after(_copy_other_class_card)


class REV_901:
    """Dispossessed Soul - 离躯之魂
    <b>Battlecry:</b> If you control a location, <b>Discover</b> a copy of a card in your deck.
    <b>战吼：</b>如果你控制一个地标，从你的牌库中<b>发现</b>一张卡牌的复制。
    """
    def play(self):
        # 检查是否控制地标
        has_location = any(card.type == CardType.LOCATION for card in self.controller.field)
        
        if has_location and self.controller.deck:
            # 从牌库中发现一张卡的复制
            # 使用 GenericChoice 从牌库中选择
            yield GenericChoice(CONTROLLER, FRIENDLY_DECK, Count(3))


class REV_946:
    """Steamcleaner - 蒸汽清洁器
    <b>Battlecry:</b> Destroy ALL cards in both players' decks that didn't start there.
    <b>战吼：</b>消灭双方牌库中所有不是初始卡组的卡牌。
    """
    def play(self):
        # 消灭所有"不是初始套牌"的卡牌
        # 这包括：
        # - 洗入牌库的卡牌（如发现的卡、复制的卡等）
        # - 由其他效果生成的卡牌
        #
        # 在 fireplace 中，我们检查卡牌的 creator 属性
        # creator 不为 None 表示卡牌是由其他卡牌创建的
        
        # 遍历双方牌库
        for player in [self.controller, self.controller.opponent]:
            cards_to_destroy = []
            for card in player.deck:
                # 检查卡牌是否是"生成的"（不是初始套牌的）
                # 标准检测：检查 creator 属性
                # creator 不为 None 表示这张卡是由其他卡牌/效果创建的
                if hasattr(card, 'creator') and card.creator is not None:
                    cards_to_destroy.append(card)
            
            # 消灭这些卡牌
            for card in cards_to_destroy:
                yield Destroy(card)


