"""
失落之城 - ROGUE (潜行者)
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from .map_helpers import mark_map_discovered_card, check_is_map_discovered_card


# ========================================
# COMMON (普通)
# ========================================

class DINO_427:
    """装扮商贩 - Costume Merchant
    2费 2/4 随从
    战吼:随机获取一张另一职业的面具牌。连击:其法力值消耗减少(2)点。
    
    Battlecry: Get a random Mask from another class. Combo: It costs (2) less.
    
    实现说明:
    - 随机获取一张其他职业的面具牌
    - 如果是连击,减少2费
    - 面具牌包括: DINO_403(魔暴龙面具), DINO_402(蝙蝠面具), DINO_428(巨鳗面具), 
      DINO_429(绵羊面具), DINO_432(奔行豹面具) 等
    """
    def play(self):
        # 定义所有面具牌ID (来自其他职业)
        mask_cards = [
            "DINO_403",  # 魔暴龙面具 (Hunter)
            "DINO_402",  # 蝙蝠面具 (Warlock)
            "DINO_428",  # 巨鳗面具 (Priest)
            "DINO_429",  # 绵羊面具 (Mage)
            "DINO_432",  # 奔行豹面具 (Druid)
        ]
        
        # 随机选择一张面具牌
        import random
        mask_id = random.choice(mask_cards)
        
        # 给予面具牌
        yield Give(CONTROLLER, mask_id)
        
        # 如果是连击,减少2费
        if self.controller.combo:
            # 获取刚刚给予的牌 (手牌最后一张)
            if self.controller.hand:
                last_card = self.controller.hand[-1]
                yield Buff(last_card, "DINO_427e")


class DINO_427e:
    """减少2费"""
    tags = {GameTag.COST: -2}


class TLC_514:
    """传奇商贩 - Legendary Merchant
    1费 1/2 随从
    战吼:发现一张传说随从牌。将其余两张洗入你的牌库。
    
    Battlecry: Discover a Legendary minion. Shuffle the other 2 into your deck.
    
    实现说明:
    - 发现一张传说随从牌
    - 将未选择的两张洗入牌库
    """
    def play(self):
        # 发现一张传说随从牌
        # 注意: 发现机制会自动将选中的牌加入手牌
        # 我们需要手动将未选择的牌洗入牌库
        
        # 生成3张随机传说随从
        from ..db import cardlist
        legendary_minions = [
            c for c in cardlist.values() 
            if c.type == CardType.MINION and c.rarity == Rarity.LEGENDARY and c.collectible
        ]
        
        import random
        choices = random.sample(legendary_minions, min(3, len(legendary_minions)))
        choice_ids = [c.id for c in choices]
        
        # 发现效果
        discovered = yield GenericChoice(CONTROLLER, choice_ids)
        
        # 将未选择的牌洗入牌库
        if discovered:
            for card_id in choice_ids:
                if card_id != discovered[0]:
                    yield Shuffle(CONTROLLER, card_id)


class TLC_516:
    """尼斐塞特武器匠 - Nerubian Weaponsmith
    4费 5/4 随从
    战吼:随机获取一张另一职业的武器牌。连击:使其获得+2攻击力。
    
    Battlecry: Get a random Weapon from another class. Combo: Give it +2 Attack.
    
    实现说明:
    - 随机获取一张其他职业的武器牌
    - 如果是连击,给予+2攻击力
    """
    def play(self):
        # 从其他职业中随机获取一张武器牌
        from ..db import cardlist
        other_class_weapons = [
            c for c in cardlist.values()
            if c.type == CardType.WEAPON 
            and c.card_class != CardClass.ROGUE 
            and c.card_class != CardClass.NEUTRAL
            and c.collectible
        ]
        
        if other_class_weapons:
            import random
            weapon = random.choice(other_class_weapons)
            
            # 给予武器牌
            yield Give(CONTROLLER, weapon.id)
            
            # 如果是连击,给予+2攻击力
            if self.controller.combo:
                # 获取刚刚给予的牌 (手牌最后一张)
                if self.controller.hand:
                    last_card = self.controller.hand[-1]
                    yield Buff(last_card, "TLC_516e")


class TLC_516e:
    """武器+2攻击力"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }


class TLC_518:
    """审讯 - Interrogation
    2费 暗影法术
    将三张3/3并具有潜行和抽到时召唤的忍者洗入你的牌库。
    
    Shuffle three 3/3 Ninjas with Stealth and Cast When Drawn into your deck.
    
    实现说明:
    - 洗入3张忍者Token (TLC_518t)
    - Token具有潜行和抽到时召唤
    """
    def play(self):
        # 洗入3张忍者Token
        for _ in range(3):
            yield Shuffle(CONTROLLER, "TLC_518t")


# ========================================
# RARE (稀有)
# ========================================

class DINO_408:
    """棱晶獠牙 - Prismatic Fang
    2费 2/2 武器
    战吼:将你最左边的手牌洗入你的牌库。亡语:抽两张牌。
    
    Battlecry: Shuffle the leftmost card in your hand into your deck. Deathrattle: Draw 2 cards.
    
    实现说明:
    - 战吼:将手牌最左边的牌洗入牌库
    - 亡语:抽两张牌
    """
    def play(self):
        # 将最左边的手牌洗入牌库
        if self.controller.hand:
            leftmost_card = self.controller.hand[0]
            yield Shuffle(CONTROLLER, leftmost_card)
    
    deathrattle = Draw(CONTROLLER) * 2


class TLC_515:
    """异教地图 - Heretic's Map
    2费 暗影法术 - 地图卡牌
    从你的牌库中发现一张牌,如果你在本回合中使用该牌,再从其余选项中选择一张。
    
    Discover a card from your deck. If you play it this turn, Discover again from the other options.
    
    实现说明:
    - 从牌库中发现一张牌
    - 标记该牌为地图发现的牌
    - 监听该牌被打出,触发第二次发现
    - 使用 map_helpers 追踪地图发现的牌
    """
    def play(self):
        # 从牌库中随机选择3张牌
        if self.controller.deck:
            import random
            choices = random.sample(self.controller.deck, min(3, len(self.controller.deck)))
            choice_ids = [c.id for c in choices]
            
            # 发现效果
            discovered = yield GenericChoice(CONTROLLER, choice_ids)
            
            # 标记该牌为地图发现的牌并存储剩余选项
            if discovered and self.controller.hand:
                discovered_card = self.controller.hand[-1]
                mark_map_discovered_card(self.controller, discovered_card.id)
                
                # 存储未选择的选项,以便后续再次发现
                remaining_choices = [cid for cid in choice_ids if cid != discovered[0]]
                if not hasattr(self.controller, 'map_remaining_choices'):
                    self.controller.map_remaining_choices = {}
                self.controller.map_remaining_choices[discovered_card.id] = remaining_choices
                
                # 创建一个临时的事件监听器,监听该牌被打出
                # 使用 Buff 来附加事件监听
                yield Buff(discovered_card, "TLC_515e")


class TLC_519:
    """潜踪掠食 - Stalking Predation
    3费 暗影法术
    召唤一只1/1并具有潜行和剧毒的喷毒龙。延系:重复一次。
    
    Summon a 1/1 Venomspitter with Stealth and Poisonous. Kindred: Do it twice.
    
    实现说明:
    - 召唤1/1潜行+剧毒的喷毒龙Token
    - 如果延系激活,召唤2次
    """
    def play(self):
        # 检查延系是否激活 (暗影法术学派)
        kindred_count = check_kindred_active(
            self.controller, 
            card_type=CardType.SPELL,
            spell_school=SpellSchool.SHADOW
        )
        
        # 基础召唤1次
        summon_count = 1
        
        # 如果延系激活,额外召唤1次
        if kindred_count:
            summon_count = 2
        
        # 召唤喷毒龙
        for _ in range(summon_count):
            yield Summon(CONTROLLER, "TLC_519t")


class TLC_521:
    """高空眼线 - High-Altitude Scout
    2费 2/3 随从
    战吼:检视敌方牌库中的三张牌,选择一张置于其牌库顶。
    
    Battlecry: Look at 3 cards in your opponent's deck. Choose one to put on top.
    
    实现说明:
    - 查看对手牌库中的3张牌
    - 选择一张置于牌库顶
    - 使用 ShuffleIntoDeck 指定位置
    """
    def play(self):
        # 查看对手牌库中的3张牌
        opponent_deck = self.controller.opponent.deck
        if opponent_deck:
            import random
            # 随机选择3张牌
            cards_to_view = random.sample(opponent_deck, min(3, len(opponent_deck)))
            card_ids = [c.id for c in cards_to_view]
            
            # 让玩家选择一张
            chosen = yield GenericChoice(CONTROLLER, card_ids)
            
            # 将选中的牌置于牌库顶
            if chosen:
                for card in cards_to_view:
                    if card.id == chosen[0]:
                        # 先从牌库移除该牌
                        opponent_deck.remove(card)
                        # 使用 ShuffleIntoDeck 将其放到牌库顶部
                        yield ShuffleIntoDeck(OPPONENT, card, position='top')
                        break


# ========================================
# EPIC (史诗)
# ========================================

class TLC_517:
    """一脚踢飞 - Kick 'Em While They're Down
    1费 法术
    对一个随从造成$1点伤害(你每将卡牌洗入牌库一次都会提升)。
    
    Deal $1 damage to a minion. (Improves each time you shuffle a card into your deck.)
    
    实现说明:
    - 造成伤害,伤害值基于洗入牌库的次数
    - 需要追踪 cards_shuffled_into_deck 计数
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 获取洗入牌库的次数
        shuffle_count = getattr(self.controller, 'cards_shuffled_into_deck', 0)
        
        # 基础伤害1点 + 洗入次数
        damage = 1 + shuffle_count
        
        # 造成伤害
        yield Hit(TARGET, damage)


class TLC_520:
    """灌林追踪者 - Thicket Tracker
    6费 5/5 随从
    突袭。你每将牌洗入你的牌库一次,本牌的法力值消耗便减少(1)点。
    
    Rush. Costs (1) less for each card you've shuffled into your deck.
    
    实现说明:
    - 具有突袭
    - 费用减少,基于洗入牌库的次数
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    @property
    def cost(self):
        base_cost = self.tags.get(GameTag.COST, 6)
        # 获取洗入牌库的次数
        shuffle_count = getattr(self.controller, 'cards_shuffled_into_deck', 0)
        return max(0, base_cost - shuffle_count)


# ========================================
# LEGENDARY (传说)
# ========================================

class DINO_407:
    """米尔雷斯,晶化镜甲龙 - Mirrex, the Crystalline
    3费 3/4 元素+野兽 传说
    此牌在你的手牌中时,会变成你的对手使用的上一张随从牌的3/4的复制。
    
    While in your hand, this transforms into a 3/4 copy of the last minion your opponent played.
    
    实现说明:
    - 在手牌中时,监听对手打出随从
    - 变形为对手打出的随从的3/4版本
    - 使用 Morph 变形机制
    """
    class Hand:
        # 监听对手打出随从
        events = Play(OPPONENT, MINION).after(
            Morph(SELF, Play.CARD),
            Buff(SELF, "DINO_407e")
        )


class DINO_407e:
    """设置属性为3/4"""
    atk = SET(3)
    max_health = SET(4)


class TLC_513:
    """暗中设伏 - Ambush in the Shadows
    1费 法术 - 任务
    任务:将卡牌洗入你的牌库,总计5次。奖励:暮影大师。
    
    Quest: Shuffle cards into your deck 5 times. Reward: Shadowmaster.
    
    实现说明:
    - 任务:洗入牌库5次
    - 奖励:暮影大师 (TLC_513t)
    - 监听 Shuffle action 的 AFTER 事件
    """
    progress_total = 5
    
    # 监听洗牌事件 - 每次成功洗入牌库时增加进度
    # 监听 Shuffle action 的 AFTER 事件
    quest = Shuffle(CONTROLLER, CONTROLLER).after(AddProgress(SELF, Shuffle.CARD))
    
    reward = Give(CONTROLLER, "TLC_513t")


class TLC_522:
    """潜踪大师奥普 - Opp, Stealth Master
    6费 6/4 传说随从
    潜行。战吼,连击,亡语:施放刀扇。
    
    Stealth. Battlecry, Combo, and Deathrattle: Cast Fan of Knives.
    
    实现说明:
    - 具有潜行
    - 战吼:施放刀扇
    - 连击:施放刀扇
    - 亡语:施放刀扇
    - 刀扇效果:对所有敌方随从造成1点伤害,抽一张牌
    """
    tags = {
        GameTag.STEALTH: True,
    }
    
    def play(self):
        # 定义施放刀扇的辅助函数
        def cast_fan_of_knives():
            """施放刀扇效果"""
            # 对所有敌方随从造成1点伤害
            for minion in self.controller.opponent.field:
                yield Hit(minion, 1)
            
            # 抽一张牌
            yield Draw(CONTROLLER)
        
        # 战吼:施放刀扇
        yield from cast_fan_of_knives()
        
        # 连击:施放刀扇
        if self.controller.combo:
            yield from cast_fan_of_knives()
    
    def deathrattle(self):
        # 定义施放刀扇的辅助函数（deathrattle 也需要）
        def cast_fan_of_knives():
            """施放刀扇效果"""
            # 对所有敌方随从造成1点伤害
            for minion in self.controller.opponent.field:
                yield Hit(minion, 1)
            
            # 抽一张牌
            yield Draw(CONTROLLER)
        
        # 亡语:施放刀扇
        yield from cast_fan_of_knives()


# ========================================
# Tokens (衍生物)
# ========================================

class TLC_518t:
    """忍者 - Ninja
    3费 3/3 随从
    潜行。抽到时召唤。
    
    Stealth. Cast When Drawn.
    
    Token from TLC_518 (审讯)
    """
    tags = {
        GameTag.STEALTH: True,
        GameTag.CAST_WHEN_DRAWN: True,
    }
    
    # 抽到时召唤自己
    def drawn(self):
        yield Summon(CONTROLLER, SELF)


class TLC_519t:
    """喷毒龙 - Venomspitter
    1费 1/1 野兽
    潜行。剧毒。
    
    Stealth. Poisonous.
    
    Token from TLC_519 (潜踪掠食)
    """
    tags = {
        GameTag.STEALTH: True,
        GameTag.POISONOUS: True,
    }


class TLC_513t:
    """暮影大师 - Shadowmaster
    5费 5/5 随从
    战吼:你的随从获得+2/+2和潜行。
    
    Battlecry: Give your minions +2/+2 and Stealth.
    
    Quest reward from TLC_513 (暗中设伏)
    """
    def play(self):
        # 给予所有友方随从+2/+2和潜行
        for minion in self.controller.field:
            yield Buff(minion, "TLC_513te")


class TLC_513te:
    """+2/+2和潜行"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.STEALTH: True,
    }


# ========================================
# Enchantments (附魔)
# ========================================

class TLC_515e:
    """地图卡牌标记 - Map Card Marker
    
    标记从地图发现的卡牌,监听其被打出后触发第二次发现
    
    Enchantment from TLC_515 (异教地图)
    """
    # 监听该卡牌被打出 (从手牌到打出区域)
    # 当卡牌被打出时,从剩余选项中再次发现
    events = Play(CONTROLLER, SELF).on(
        lambda self, source, target: (
            # 检查是否有剩余选项
            GenericChoice(
                CONTROLLER, self.controller.map_remaining_choices.get(source.id, [])
            ) if (
                hasattr(self.controller, 'map_remaining_choices') and
                source.id in self.controller.map_remaining_choices and
                len(self.controller.map_remaining_choices[source.id]) > 0
            ) else None
        )
    )

