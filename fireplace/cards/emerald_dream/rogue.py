"""
漫游翡翠梦境 - ROGUE
"""
from ..utils import *


# COMMON

class EDR_521:
    """狡猾的萨特 - Tricky Satyr
    Battlecry: Get a copy of the lowest Cost card in your opponent's hand.
    
    2费 2/2 恶魔
    战吼:获取你对手手牌中法力值消耗最低的牌的一张复制。
    """
    def play(self):
        # 获取对手手牌中费用最低的牌
        opponent_hand = self.controller.opponent.hand
        if opponent_hand:
            # 找到费用最低的牌
            lowest_cost_card = min(opponent_hand, key=lambda c: c.cost)
            # 给自己一张复制
            yield Give(CONTROLLER, lowest_cost_card.id)


class EDR_522:
    """拟态 - Mimicry
    Your opponent draws 2 cards. You get copies of them.
    
    1费 法术
    你的对手抽两张牌,你获取其复制。
    
    实现说明:
    - 让对手抽2张牌
    - 获取对手手牌中最后抽到的2张牌的复制
    """
    requirements = {}
    
    def play(self):
        # 记录对手当前手牌数
        initial_hand_size = len(self.controller.opponent.hand)
        
        # 对手抽2张牌
        for _ in range(2):
            yield Draw(OPPONENT)
        
        # 获取对手新抽到的牌(手牌末尾的牌)
        # 从initial_hand_size位置开始到末尾的牌就是新抽到的牌
        if len(self.controller.opponent.hand) > initial_hand_size:
            newly_drawn = self.controller.opponent.hand[initial_hand_size:]
            # 给自己这些牌的复制
            for card in newly_drawn:
                yield Give(CONTROLLER, card.id)


class EDR_528:
    """梦魇供能 - Nightmare Fuel
    Discover a copy of a minion in your opponent's deck. Combo: With a Dark Gift.
    
    1费 法术
    从你对手的牌库中发现一张随从牌的复制。连击:并使其具有黑暗之赐。
    """
    requirements = {}
    
    def play(self):
        from .dark_gift_helpers import apply_dark_gift
        
        # 从对手牌库中发现一张随从牌
        opponent_minions = [c for c in self.controller.opponent.deck if c.type == CardType.MINION]
        
        if opponent_minions:
            # 随机选择3张不同的随从
            choices = self.game.random.sample(opponent_minions, min(3, len(opponent_minions)))
            
            # 发现效果
            yield GenericChoice(CONTROLLER, [c.id for c in choices])
            
            # 如果是连击,给予黑暗之赐
            if self.controller.combo:
                # 获取刚刚发现的牌
                discovered_card = self.controller.hand[-1] if self.controller.hand else None
                if discovered_card:
                    yield apply_dark_gift(discovered_card)


class FIR_922:
    """燃薪之剑 - Cindersword
    Battlecry: If you're holding a minion with a Dark Gift, gain +3 Attack.
    
    1费 1/2 武器
    战吼:如果你的手牌中有具有黑暗之赐的随从牌,获得+3攻击力。
    """
    def play(self):
        from .dark_gift_helpers import has_dark_gift
        
        # 检查手牌中是否有具有黑暗之赐的随从
        has_dark_gift_minion = any(
            has_dark_gift(c) and c.type == CardType.MINION 
            for c in self.controller.hand
        )
        
        if has_dark_gift_minion:
            # 给予武器+3攻击力
            yield Buff(SELF, "FIR_922e")


# RARE

class EDR_523:
    """欺诈之网 - Web of Deception
    Return a friendly minion to your hand to summon a 4/4 Spider with Stealth.
    
    2费 法术
    将一个友方随从移回你的手牌以召唤一只4/4并具有潜行的蜘蛛。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        # 将目标随从移回手牌
        yield Bounce(TARGET)
        # 召唤4/4潜行蜘蛛
        yield Summon(CONTROLLER, "EDR_523t")


class EDR_540:
    """扭曲的织网蛛 - Twisted Webweaver
    [x]Whenever you play another minion you've already played, draw a card.
    
    2费 1/3 野兽
    每当你使用其他的你已经使用过的随从牌,抽一张牌。
    
    实现说明:
    - 使用 minions_played_this_game 追踪已打出的随从ID
    - 在 before 事件中检查,因为 after 时已经加入列表
    - 需要检查打出的随从是否在打出前就已经在列表中
    """
    # 监听随从打出事件 - 使用 before 检查是否已打过
    events = Play(CONTROLLER, MINION).before(
        lambda self, card: (
            source != self.owner and  # 不是自己
            source.id in self.owner.controller.minions_played_this_game  # 之前已经打过
        ),
        Draw(CONTROLLER)
    )



class EDR_781:
    """凋零先驱 - Harbinger of the Blighted
    [x]Whenever this enters your hand from the battlefield, summon two random 2-Cost minions.
    
    3费 2/3 随从
    每当本随从从战场进入你的手牌时,随机召唤两个法力值消耗为(2)的随从。
    """
    # 监听从战场回到手牌的事件
    # 使用 OWN_TURN_END 和 ZoneChange 事件
    class Hand:
        events = ZoneChange(SELF, PLAY, HAND).on(
            Summon(CONTROLLER, RandomMinion(cost=2)),
            Summon(CONTROLLER, RandomMinion(cost=2))
        )


class FIR_919:
    """永燃火凤 - Everburning Phoenix
    [x]Costs (1) less for each card you've played this turn. Deathrattle: At end of turn, get another Phoenix.
    
    5费 4/3 元素+野兽
    在本回合中你每使用过一张牌,本牌的法力值消耗便减少(1)点。亡语:在回合结束时,获取另一张永燃火凤。
    """
    # 动态费用计算
    @property
    def cost(self):
        base_cost = self.tags.get(GameTag.COST, 5)
        # 获取本回合打出的牌数
        cards_played_this_turn = getattr(self.controller, 'cards_played_this_turn', 0)
        return max(0, base_cost - cards_played_this_turn)
    
    # 亡语:回合结束时获取复制
    class Play:
        deathrattle = Buff(CONTROLLER, "FIR_919e")


class FIR_920:
    """烟雾弹 - Smoke Bomb
    Discover a Combo, Battlecry, or Stealth minion with a Dark Gift.
    
    2费 火焰法术
    发现一张具有黑暗之赐的连击,战吼或潜行随从牌。
    """
    requirements = {}
    
    def play(self):
        from .dark_gift_helpers import apply_dark_gift
        
        # 发现一张连击/战吼/潜行随从
        def card_filter(c):
            return (
                c.type == CardType.MINION and
                (
                    GameTag.COMBO in c.tags or
                    GameTag.BATTLECRY in c.tags or
                    GameTag.STEALTH in c.tags
                )
            )
        
        # 生成3个选项
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=card_filter,
            count=3
        ))
        
        # 给予黑暗之赐
        discovered_card = self.controller.hand[-1] if self.controller.hand else None
        if discovered_card:
            yield apply_dark_gift(discovered_card)


# EPIC

class EDR_524:
    """影蔽袭击者 - Shadowcloaked Assailant
    [x]Battlecry: If you're holding one of the same cards as your opponent, shuffle theirs into their deck.
    
    4费 3/5 恶魔
    战吼:如果你的手牌中有一张与对手相同的牌,将对手的该牌洗入其牌库。
    """
    def play(self):
        # 找到与对手手牌相同的牌
        my_hand_ids = set(c.id for c in self.controller.hand)
        opponent_hand = self.controller.opponent.hand
        
        # 找到对手手牌中与我手牌相同的牌
        matching_cards = [c for c in opponent_hand if c.id in my_hand_ids]
        
        if matching_cards:
            # 将对手的这些牌洗入其牌库
            for card in matching_cards:
                yield Shuffle(OPPONENT, card)


class EDR_525:
    """倒刺荆棘 - Barbed Thorn
    [x]Choose One - Gain Poisonous this turn; or Gain "Deathrattle: Deal 2 damage to all enemies."
    
    3费 1/3 武器
    抉择:获得在本回合中的剧毒;或者获得"亡语:对所有敌人造成2点伤害。"
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("EDR_525a", "EDR_525b")


class EDR_525a:
    """本回合剧毒"""
    play = Buff(FRIENDLY_WEAPON, "EDR_525e_poisonous")


class EDR_525b:
    """亡语:对所有敌人2伤"""
    play = Buff(FRIENDLY_WEAPON, "EDR_525e_deathrattle")


# LEGENDARY

class EDR_526:
    """雷弗拉尔,恶念巨蛛 - Renferal, the Malignant
    [x]Battlecry: Trap 1 random card in your opponent's hand for a turn. <i>(Improved for each time you've played this.)</i>
    
    3费 3/3 野兽
    战吼:随机使你对手手牌中的1张牌困住一回合。(你每使用过一次本随从都会提升。)
    
    实现说明:
    - 困住效果:使卡牌无法使用1回合
    - 每次打出后提升困住的牌数
    - 使用字典存储每张卡的打出次数,避免污染Player命名空间
    """
    def play(self):
        # 初始化追踪字典(如果不存在)
        if not hasattr(self.controller, 'card_play_counts'):
            self.controller.card_play_counts = {}
        
        # 获取本随从已打出的次数
        card_id = self.id
        times_played = self.controller.card_play_counts.get(card_id, 0)
        
        # 困住的牌数 = 当前次数 + 1
        trap_count = times_played + 1
        
        # 增加打出次数
        self.controller.card_play_counts[card_id] = times_played + 1
        
        # 随机选择对手手牌中的牌并困住
        opponent_hand = self.controller.opponent.hand
        if opponent_hand:
            cards_to_trap = self.game.random.sample(opponent_hand, min(trap_count, len(opponent_hand)))
            
            for card in cards_to_trap:
                # 给予"困住"效果:增加费用使其无法使用,1回合后恢复
                yield Buff(card, "EDR_526e")


class EDR_527:
    """阿莎曼 - Ashamane
    [x]Battlecry: Fill your hand with copies of cards from your opponent's deck. They cost (3) less.
    
    9费 7/7 野兽
    战吼:用你对手牌库中牌的复制填满你的手牌,其法力值消耗减少(3)点。
    """
    def play(self):
        # 计算手牌空位
        hand_space = 10 - len(self.controller.hand)
        
        if hand_space > 0 and self.controller.opponent.deck:
            # 从对手牌库中随机选择牌
            cards_to_copy = self.game.random.sample(
                self.controller.opponent.deck,
                min(hand_space, len(self.controller.opponent.deck))
            )
            
            # 给予复制并减少费用
            for card in cards_to_copy:
                yield Give(CONTROLLER, card.id)
                # 给予-3费buff
                if self.controller.hand:
                    yield Buff(self.controller.hand[-1], "EDR_527e")
