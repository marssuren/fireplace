"""
胜地历险记 - PRIEST
"""
from ..utils import *


# ========== COMMON ==========

class VAC_419:
    """针灸 - Acupuncture
    Deal $4 damage to both heroes.
    对双方英雄造成$4点伤害。
    """
    def play(self):
        # 对双方英雄各造成4点伤害
        yield Hit(FRIENDLY_HERO, 4)
        yield Hit(ENEMY_HERO, 4)


class VAC_512:
    """心灵按摩师 - Brain Masseuse
    Whenever this minion takes damage, also deal that amount to your hero.
    每当本随从受到伤害，对你的英雄造成等量的伤害。
    """
    # 监听本随从受到伤害
    events = Damage(SELF).on(
        lambda self, source, target, amount, *args: Hit(FRIENDLY_HERO, amount) if amount > 0 else []
    )


class VAC_414:
    """炽热火炭 - Hot Coals
    Deal $2 damage to all enemies. If your hero took damage this turn, deal $1 more.
    对所有敌人造成$2点伤害。如果你的英雄在本回合受到过伤害，再造成$1点。
    """
    def play(self):
        # 检查英雄本回合是否受到过伤害
        # 直接访问 hero 的 damaged_this_turn 属性
        hero_damaged = self.controller.hero.damaged_this_turn > 0
        
        # 基础伤害2点
        base_damage = 2
        # 如果英雄受到过伤害，额外1点
        total_damage = base_damage + (1 if hero_damaged else 0)
        
        # 对所有敌人造成伤害
        yield Hit(ENEMY_CHARACTERS, total_damage)


class WORK_032:
    """影随员工 - Job Shadower
    Battlecry: If your hero took damage this turn, summon a copy of this.
    战吼：如果你的英雄在本回合受到过伤害，召唤一个本随从的复制。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 检查英雄本回合是否受到过伤害
        # 直接访问 hero 的 damaged_this_turn 属性
        hero_damaged = self.controller.hero.damaged_this_turn > 0
        
        if hero_damaged:
            # 召唤一个本随从的复制
            yield Summon(CONTROLLER, self.id)


# ========== RARE ==========

class VAC_404:
    """夜影花茶 - Nightshade Tea
    Deal $2 damage to a minion. Deal $2 damage to your hero. (3 Drinks left!)
    对一个随从造成$2点伤害。对你的英雄造成$2点伤害。（还剩3杯！）
    """
    # Drink Spell: 使用后返回手牌，最多使用3次
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 对目标随从造成2点伤害
        if TARGET:
            yield Hit(TARGET, 2)
        
        # 对友方英雄造成2点伤害
        yield Hit(FRIENDLY_HERO, 2)
        
        # Drink Spell机制：返回2杯版本
        yield Give(CONTROLLER, "VAC_404t")


class WORK_017:
    """银月城宣传单 - Silvermoon Brochure
    Give a minion Immune this turn and +2/+2. (Flips each turn.)
    使一个随从获得在本回合中免疫和+2/+2。（每回合翻面。）
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 给予+2/+2（永久）
            yield Buff(TARGET, "WORK_017e")
            # 给予本回合免疫（临时）
            yield Buff(TARGET, "WORK_017e2")
    
    # 翻面机制：在手牌中每回合翻转为 Gilneas Brochure
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "WORK_017t"))


class WORK_017e:
    """银月城宣传单 - 永久属性增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class WORK_017e2:
    """银月城宣传单 - 本回合免疫"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    # 回合结束时移除免疫效果
    events = OWN_TURN_END.on(Destroy(SELF))


class WORK_031:
    """暴富特使 - Envoy of Prosperity
    Battlecry: Put the highest Cost card in your hand on top of your deck.
    战吼：将你手牌中法力值消耗最高的牌置于你的牌库顶。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 找到手牌中费用最高的牌（排除自己）
        hand_cards = [c for c in self.controller.hand if c != self]
        
        if hand_cards:
            highest_card = max(hand_cards, key=lambda c: c.cost)
            # 将该牌置于牌库顶
            yield Shuffle(CONTROLLER, highest_card, to_top=True)


class VAC_457:
    """安息 - Rest in Peace
    Each player summons their highest Cost minion that died this game.
    每个玩家分别召唤其在本局对战中死亡的法力值消耗最高的随从。
    """
    def play(self):
        # 为双方玩家各召唤其死亡的最高费随从
        for player in self.game.players:
            # 从墓地中找到所有死亡的随从
            dead_minions = [c for c in player.graveyard if c.type == CardType.MINION]
            
            if dead_minions:
                # 找到费用最高的随从
                highest_minion = max(dead_minions, key=lambda c: c.cost)
                # 为该玩家召唤
                yield Summon(player, highest_minion.id)


class VAC_418:
    """桑拿常客 - Sauna Regular
    Taunt. Costs (1) less for each time your hero has taken damage on your turn.
    嘲讽。你的英雄每在你的回合受到一次伤害，本牌的法力值消耗便减少（1）点。
    """
    mechanics = [GameTag.TAUNT]
    
    # 监听英雄受到伤害（仅在己方回合）
    def on_hero_damaged(self, source, target, amount):
        """当友方英雄受到伤害时，如果是己方回合，增加计数器"""
        # 检查是否是己方回合
        if self.controller.current_player:
            # 初始化计数器（如果不存在）
            if not hasattr(self.controller, 'hero_damage_count_on_own_turn'):
                self.controller.hero_damage_count_on_own_turn = 0
            # 增加计数
            self.controller.hero_damage_count_on_own_turn += 1
    
    def on_turn_begin(self, source, player):
        """回合开始时重置计数器"""
        if player == self.controller:
            self.controller.hero_damage_count_on_own_turn = 0
    
    # 事件监听
    events = [
        # 监听友方英雄受到伤害
        Damage(FRIENDLY_HERO).on(
            lambda self, source, target, amount, *args: self.on_hero_damaged(source, target, amount)
        ),
        # 回合开始时重置计数器
        OWN_TURN_BEGIN.on(
            lambda self, player: self.on_turn_begin(player)
        ),
    ]
    
    # 费用减免光环
    class Hand:
        """手牌中的费用减免"""
        def cost(self, i):
            # 计算英雄在己方回合受到伤害的次数
            damage_count = getattr(self.controller, 'hero_damage_count_on_own_turn', 0)
            return i - damage_count


# ========== EPIC ==========

class VAC_423:
    """暮光灵媒师 - Twilight Medium
    Taunt. Battlecry: Set the Cost of the top card of your deck to (1).
    嘲讽。战吼：将你牌库顶的一张牌的法力值消耗变为（1）点。
    """
    mechanics = [GameTag.BATTLECRY, GameTag.TAUNT]
    
    def play(self):
        # 获取牌库顶的牌
        if self.controller.deck:
            top_card = self.controller.deck[0]
            # 将其费用设置为1
            yield Buff(top_card, "VAC_423e")


class VAC_423e:
    """暮光灵媒师 - 费用设置为1"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 使用 lambda 将费用设置为固定值1
    cost = lambda self, i: 1


class VAC_417:
    """感官侵夺 - Sensory Deprivation
    Summon a copy of an enemy minion. If you have 20 or less Health, destroy the original.
    召唤一个敌方随从的一个复制。如果你的生命值小于或等于20点，消灭本体。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        target = self.target
        if target:
            # 召唤目标随从的复制
            yield Summon(CONTROLLER, target.id)
            
            # 如果生命值<=20,消灭本体
            if self.controller.hero.health <= 20:
                yield Destroy(target)


# ========== LEGENDARY ==========

class VAC_957:
    """惬意的沃金 - Chillin' Vol'jin
    Hunter Tourist. Battlecry: Choose 2 minions. Swap their stats.
    猎人游客。战吼：选择2个随从，交换其属性值。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 选择第一个随从
        first_target = yield GenericChoice(CONTROLLER, ALL_MINIONS)
        
        if first_target:
            first_minion = first_target[0]
            first_atk = first_minion.atk
            first_health = first_minion.health
            
            # 选择第二个随从
            second_target = yield GenericChoice(CONTROLLER, ALL_MINIONS)
            
            if second_target:
                second_minion = second_target[0]
                second_atk = second_minion.atk
                second_health = second_minion.health
                
                # 交换属性值
                # 第一个随从获得第二个随从的属性
                yield Buff(first_minion, "VAC_957e", new_atk=second_atk, new_health=second_health)
                # 第二个随从获得第一个随从的属性
                yield Buff(second_minion, "VAC_957e", new_atk=first_atk, new_health=first_health)


class VAC_957e:
    """惬意的沃金 - 属性交换效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 从参数中获取新的属性值并设置为 _atk 和 _max_health
        if 'new_atk' in kwargs:
            self._atk = kwargs['new_atk']
        if 'new_health' in kwargs:
            self._max_health = kwargs['new_health']
    



class VAC_420:
    """纳瑞安·柔想 - Narain Soothfancy
    Battlecry: Get two Fortunes that are copies of the top card of your deck.
    战吼：获取两张预知命运。预知命运为你牌库顶的牌的复制。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 获取牌库顶的牌
        if self.controller.deck:
            top_card = self.controller.deck[0]
            # 给予2张该牌的复制（作为"预知命运"）
            yield Give(CONTROLLER, top_card.id) * 2
