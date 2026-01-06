"""
胜地历险记 - SHAMAN
"""
from ..utils import *


# ========== COMMON ==========

class VAC_323:
    """麦芽岩浆 - Malted Magma
    Deal $1 damage to all enemies. (3 Drinks left!)
    对所有敌人造成$1点伤害。（还剩3杯！）
    
    Drink Spell 机制：使用后返回手牌，共可使用3次
    官方数据：对所有敌方角色（包括英雄）造成伤害
    """
    def play(self):
        # 对所有敌方角色造成1点伤害（包括英雄和随从）
        enemy_characters = self.game.board.get_enemies(self.controller)
        for character in enemy_characters:
            yield Hit(character, 1)
        
        # 返回2杯版本到手牌
        yield Give(CONTROLLER, "VAC_323t")


class VAC_324:
    """统一着装 - Matching Outfits
    Transform a minion into a random one that costs (1) more, then summon a copy of it.
    将一个随从随机变形成为一个法力值消耗增加（1）点的随从，然后召唤一个它的复制。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 获取目标随从的费用
            original_cost = TARGET.cost
            # 变形为费用+1的随从
            new_minion_id = RandomCollectible(type=CardType.MINION, cost=original_cost + 1)
            yield Morph(TARGET, new_minion_id)
            
            # 召唤变形后随从的复制
            # 注意：Morph后TARGET已经是新随从了
            if TARGET.zone == Zone.PLAY:
                yield Summon(CONTROLLER, Copy(TARGET))


class VAC_328:
    """消融元素 - Meltemental
    Taunt. This is permanently Frozen.
    嘲讽。本随从永久被冻结。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.FROZEN: True  # 永久冻结
    }
    
    # 确保冻结状态永久存在
    # 使用 Aura 防止解冻
    class Aura:
        """永久冻结光环"""
        def frozen(self, i):
            return True


class WORK_011:
    """饮水图腾 - Hydration Totem
    At the end of your turn, give adjacent minions +1/+1.
    在你的回合结束时，使相邻的随从获得+1/+1。
    """
    # 回合结束时触发
    events = OWN_TURN_END.on(
        lambda self, source: [
            Buff(adj, "WORK_011e") 
            for adj in source.adjacent_minions
        ]
    )


class WORK_011e:
    """饮水图腾增益效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    atk = 1
    max_health = 1


# ========== RARE ==========

class VAC_305:
    """冰霜摆件 - Frosty Décor
    Summon two 2/4 Elementals with Taunt and "Deathrattle: Gain 4 Armor".
    召唤两个2/4并具有嘲讽和"亡语：获得4点护甲值"的元素。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 召唤2个冰霜元素Token
        yield Summon(CONTROLLER, "VAC_305t") * 2


class VAC_308:
    """海妖之歌 - Siren Song
    Get two random spells from spell schools you haven't cast this game.
    随机获取两张你在本局对战中未施放过的派系的法术牌。
    """
    def play(self):
        # 获取所有派系
        all_schools = [
            SpellSchool.ARCANE,
            SpellSchool.FIRE,
            SpellSchool.FROST,
            SpellSchool.NATURE,
            SpellSchool.HOLY,
            SpellSchool.SHADOW,
            SpellSchool.FEL
        ]
        
        # 获取未施放过的派系
        played_schools = self.controller.spell_schools_played_this_game
        unplayed_schools = [s for s in all_schools if s not in played_schools]
        
        # 如果有未施放的派系，随机选择2个
        if unplayed_schools:
            # 随机选择最多2个未施放的派系
            selected_schools = self.game.random.sample(
                unplayed_schools, 
                min(2, len(unplayed_schools))
            )
            
            # 为每个派系获取一张随机法术
            for school in selected_schools:
                yield Give(CONTROLLER, RandomCollectible(
                    type=CardType.SPELL,
                    spell_school=school
                ))


class VAC_954:
    """顶流主唱 - Cabaret Headliner
    Battlecry: Reduce the Cost of a spell of each school in your hand by (2).
    战吼：使你手牌中每个派系的各一张法术牌的法力值消耗减少（2）点。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 收集手牌中每个派系的法术
        school_spells = {}  # {SpellSchool: [cards]}
        
        for card in self.controller.hand:
            if card.type == CardType.SPELL and hasattr(card, 'spell_school'):
                school = card.spell_school
                if school not in school_spells:
                    school_spells[school] = []
                school_spells[school].append(card)
        
        # 为每个派系随机选择一张法术减2费
        for school, cards in school_spells.items():
            if cards:
                # 随机选择该派系的一张法术
                target_card = self.game.random.choice(cards)
                yield Buff(target_card, "VAC_954e")


class VAC_954e:
    """顶流主唱减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost = -2


class WORK_030:
    """冰冠堡垒宣传单 - Icecrown Brochure
    Deal $3 damage to a minion and Freeze its neighbors. (Flips each turn.)
    对一个随从造成$3点伤害并冻结其相邻随从。（每回合翻面。）
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 对目标造成3点伤害
            yield Hit(TARGET, 3)
            
            # 冻结相邻随从
            if TARGET.zone == Zone.PLAY:
                for adj in TARGET.adjacent_minions:
                    yield Freeze(adj)
    
    # 翻面机制：在手牌中每回合翻转为另一张宣传单
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "WORK_030t"))


# ========== EPIC ==========

class VAC_301:
    """炫目演出者 - Razzle-Dazzler
    Battlecry: Summon a random 5-Cost minion. Repeat for each spell school you've cast this game.
    战吼：随机召唤一个法力值消耗为（5）的随从。在本局对战中你每施放过一个派系的法术，重复一次。
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 获取已施放的派系数量
        schools_count = len(self.controller.spell_schools_played_this_game)
        
        # 召唤 (1 + schools_count) 个5费随从
        # 基础召唤1个，每个派系额外召唤1个
        total_summons = 1 + schools_count
        
        for _ in range(total_summons):
            yield Summon(CONTROLLER, RandomCollectible(
                type=CardType.MINION,
                cost=5
            ))


class VAC_329:
    """自然天性 - Natural Talent
    Get a random Naga and a random spell. They cost (2) less.
    随机获取纳迦牌和法术牌各一张，其法力值消耗减少（2）点。
    """
    def play(self):
        # 获取一张随机纳迦
        naga = yield Give(CONTROLLER, RandomCollectible(race=Race.NAGA))
        if naga and naga[0]:
            yield Buff(naga[0], "VAC_329e")
        
        # 获取一张随机法术
        spell = yield Give(CONTROLLER, RandomCollectible(type=CardType.SPELL))
        if spell and spell[0]:
            yield Buff(spell[0], "VAC_329e")


class VAC_329e:
    """自然天性减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost = -2


# ========== LEGENDARY ==========

class VAC_449:
    """歌唱明星卡瑞斯 - Carress, Cabaret Star
    While in your hand, play two different spell schools to transform.
    此牌在你的手牌中时，使用两种不同派系的法术牌即可变形。
    
    官方机制：21种变形形态（7个派系选2的组合）
    每种形态具有不同的战吼效果组合
    
    派系效果：
    - Arcane: Draw 2 cards
    - Fel: Deal 2 damage to all enemy minions
    - Fire: Deal 6 damage to the enemy hero
    - Frost: Freeze three random enemy minions
    - Holy: Restore 6 Health to your hero
    - Nature: Gain +2/+2 and Taunt
    - Shadow: Destroy 2 random enemy minions
    """
    # 正式声明属性：追踪在手牌期间施放的派系
    schools_played_while_in_hand = None  # set()
    has_transformed = False  # 是否已经变形（防止重复变形）
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化派系追踪集合
        self.schools_played_while_in_hand = set()
        self.has_transformed = False
    
    class Hand:
        """手牌中的变形机制"""
        def on_spell_played(self, source, player, card, *args):
            """监听施放法术，追踪派系"""
            # 如果已经变形，不再处理
            if getattr(self, 'has_transformed', False):
                return
            
            if card.type == CardType.SPELL and hasattr(card, 'spell_school'):
                school = card.spell_school
                
                # 添加到追踪集合
                if not hasattr(self, 'schools_played_while_in_hand'):
                    self.schools_played_while_in_hand = set()
                
                self.schools_played_while_in_hand.add(school)
                
                # 检查是否达到2种不同派系
                if len(self.schools_played_while_in_hand) >= 2:
                    # 标记已变形
                    self.has_transformed = True
                    
                    # 获取前两个派系（按添加顺序）
                    schools_list = list(self.schools_played_while_in_hand)[:2]
                    school1, school2 = schools_list[0], schools_list[1]
                    
                    # 根据派系组合确定变形目标
                    # 使用映射表确定Token ID
                    from .carress_mapping import get_carress_token_id
                    token_id = get_carress_token_id(school1, school2)
                    
                    # 变形为对应形态
                    yield Morph(SELF, token_id)
        
        events = Play(CONTROLLER, SPELL).after(
            lambda self, source, player, card, *args: self.on_spell_played(source, player, card, *args)
        )


class VAC_450:
    """悠闲的曲奇 - Carefree Cookie
    Demon Hunter Tourist. After a friendly minion dies, summon a random minion that costs (1) more.
    恶魔猎手游客。在一个友方随从死亡后，随机召唤一个法力值消耗增加（1）点的随从。
    """
    # Tourist 标签在构筑验证中处理，这里只实现效果
    
    # 监听友方随从死亡
    events = Death(FRIENDLY_MINIONS).after(
        lambda self, source, target: [
            Summon(CONTROLLER, RandomCollectible(
                type=CardType.MINION,
                cost=target.cost + 1
            ))
        ]
    )


class WORK_013:
    """湍流元素特布勒斯 - Turbulus
    Hunter Tourist. Battlecry: Give +1/+1 to all other Battlecry minions in your hand, deck, and battlefield.
    猎人游客。战吼：使你手牌，牌库和战场上的所有其他战吼随从获得+1/+1。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给手牌中的战吼随从+1/+1
        for card in self.controller.hand:
            if card != self and card.type == CardType.MINION:
                if GameTag.BATTLECRY in card.tags or hasattr(card, 'battlecry'):
                    yield Buff(card, "WORK_013e")
        
        # 给牌库中的战吼随从+1/+1
        for card in self.controller.deck:
            if card.type == CardType.MINION:
                if GameTag.BATTLECRY in card.tags or hasattr(card, 'battlecry'):
                    yield Buff(card, "WORK_013e")
        
        # 给场上的其他战吼随从+1/+1
        for minion in self.controller.field:
            if minion != self:
                if GameTag.BATTLECRY in minion.tags or hasattr(minion, 'battlecry'):
                    yield Buff(minion, "WORK_013e")


class WORK_013e:
    """湍流元素特布勒斯增益效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    atk = 1
    max_health = 1
