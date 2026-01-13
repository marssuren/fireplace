"""
穿越时间流 - DRUID
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_023:
    """后备预案 - Contingency
    Draw the bottom two cards from your deck.
    
    3费 法术
    抽取你牌库底的两张牌。
    """
    requirements = {}
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 抽取牌库底的两张牌
            # 牌库底的牌是 deck[-1] 和 deck[-2]
            if len(self.controller.deck) > 0:
                # 先抽倒数第一张
                yield Draw(self.controller, self.controller.deck[-1])
            if len(self.controller.deck) > 0:
                # 再抽倒数第一张（原来的倒数第二张）
                yield Draw(self.controller, self.controller.deck[-1])

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_033:
    """再生德鲁伊 - Druid of Regrowth
    Rewind Battlecry: Cast 2 random Nature spells.
    
    6费 3/5 随从
    回溯。战吼：随机施放2个自然法术。
    """
    requirements = {}
    
    def play(self):
        
        # 随机施放2个自然法术
        # 参考 whizbang/mage.py 的 CastSpell(RandomSpell()) 实现
        for _ in range(2):
            yield CastSpell(RandomSpell(spell_school=SpellSchool.NATURE))


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_702:
    """潮起潮落 - Ebb and Flow
    Deal $3 damage. If you played a minion while holding this, gain 5 Armor.
    
    2费 自然法术
    造成$3点伤害。如果你在本牌在你手中时使用过随从牌，获得5点护甲值。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)
        
        # 检查是否在手牌中时使用过随从牌
        # 使用 Hand 类追踪
        if getattr(self, '_played_minion_while_holding', False):
            yield GainArmor(FRIENDLY_HERO, 5)
    
    class Hand:
        # 监听随从打出事件
        events = OWN_MINION_PLAY.on(
            lambda self, player, played_card, target: setattr(self.owner, '_played_minion_while_holding', True)
        )


# RARE

class TIME_701:
    """波涛形塑 - Waveshaping
    Discover a card from your deck. The others get put on the bottom.
    
    1费 自然法术
    从你的牌库中发现一张牌。将其余选项置于牌库底。
    
    完整实现：
    1. 从牌库中随机选择3张牌
    2. 玩家选择其中一张
    3. 选中的牌加入手牌
    4. 未选中的牌放回牌库底
    """
    requirements = {}
    
    def play(self):
        # 从牌库中随机选择3张牌进行发现
        if len(self.controller.deck) == 0:
            return
        
        # 随机选择最多3张牌
        num_cards = min(3, len(self.controller.deck))
        cards_to_discover = []
        
        # 从牌库中随机选择牌（不移除）
        import random
        available_cards = list(self.controller.deck)
        selected_cards = random.sample(available_cards, num_cards)
        
        # 使用 GenericChoice 让玩家选择
        choice = yield GenericChoice(self.controller, selected_cards)
        
        if choice and len(choice) > 0:
            chosen_card = choice[0]
            
            # 将选中的牌加入手牌（从牌库移除）
            yield Give(self.controller, chosen_card)
            
            # 将未选中的牌移到牌库底
            for card in selected_cards:
                if card != chosen_card and card in self.controller.deck:
                    # 移除卡牌
                    card.zone = Zone.SETASIDE
                    # 放回牌库底（插入到索引0）
                    self.controller.deck.insert(0, card)
                    card.zone = Zone.DECK


class TIME_703:
    """濒危的渡渡鸟 - Endangered Dodo
    [x]Taunt Battlecry: If you have 10 or less Health, gain +5/+5 and summon a copy of this.
    
    5费 5/5 野兽
    嘲讽。战吼：如果你的生命值小于或等于10点，获得+5/+5并召唤一个本随从的复制。
    """
    requirements = {}
    
    def play(self):
        # 检查英雄生命值
        if self.controller.hero.health <= 10:
            # 获得 +5/+5
            yield Buff(SELF, "TIME_703e")
            # 召唤一个本随从的复制
            yield Summon(self.controller, self.id)


class TIME_703e:
    """濒危的渡渡鸟 - +5/+5"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }


class TIME_730:
    """卡多雷培育师 - Kaldorei Cultivator
    [x]Battlecry: Discover 2 Beasts. Put them on the bottom of your deck with +5/+5.
    
    2费 2/3 随从
    战吼：发现2张野兽牌，将它们置于你的牌库底并具有+5/+5。
    
    完整实现：
    1. 发现2张野兽牌
    2. 给它们施加 +5/+5 buff
    3. 将它们放到牌库底
    """
    requirements = {}
    
    def play(self):
        # 发现两次野兽牌
        for _ in range(2):
            # 发现一张野兽牌
            choice = yield GenericChoice(
                self.controller, RandomCollectible(race=Race.BEAST)
            )
            
            if choice and len(choice) > 0:
                beast_card = choice[0]
                
                # 给发现的牌施加 +5/+5 buff
                yield Buff(beast_card, "TIME_730e")
                
                # 将牌放到牌库底（插入到索引0）
                # 注意：GenericChoice 会自动将牌加入手牌，我们需要将其移到牌库底
                if beast_card.zone == Zone.HAND:
                    beast_card.zone = Zone.SETASIDE
                    self.controller.deck.insert(0, beast_card)
                    beast_card.zone = Zone.DECK


class TIME_730e:
    """卡多雷培育师 - +5/+5"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }


# EPIC

class TIME_704:
    """上层精灵教师 - Highborne Mentor
    [x]Battlecry: Get a 2/2 Pupil. Discover a spell that costs (7) or more from the past to teach it.
    
    7费 6/6 随从
    战吼：获取一张2/2的小学生。发现一个来自过去的法力值消耗大于或等于（7）点的法术，教会小学生。
    
    完整实现：
    1. 获取一张2/2的小学生Token
    2. 发现一个7费或以上的法术
    3. 将发现的法术"教会"小学生（存储到小学生的亡语中）
    """
    requirements = {}
    
    def play(self):
        # 1. 获取一张2/2的小学生
        pupil = yield Give(self.controller, "TIME_704t")
        
        # 2. 发现一个7费或以上的法术
        choice = yield GenericChoice(
            self.controller, RandomCollectible(card_type=CardType.SPELL, min_cost=7)
        )
        
        # 3. 将发现的法术"教会"小学生（存储到小学生的buff中）
        if choice and len(choice) > 0 and pupil and len(pupil) > 0:
            spell_id = choice[0].id
            # 给小学生添加一个buff，存储法术ID
            yield Buff(pupil[0], "TIME_704e", spell_id=spell_id)


class TIME_707:
    """平行现实 - Alternate Reality
    [x]Replace your hand and deck with random Choose One cards from the past. They cost (1) less.
    
    2费 法术
    将你的手牌和牌库里的牌替换为来自过去的随机抉择牌，其法力值消耗减少（1）点。
    
    完整实现：
    1. 记录当前手牌和牌库的数量
    2. 清空手牌和牌库
    3. 用随机的抉择牌填充，并减少1费
    """
    requirements = {}
    
    def play(self):
        # 1. 记录当前手牌和牌库的数量
        hand_size = len(self.controller.hand)
        deck_size = len(self.controller.deck)
        
        # 2. 清空手牌
        for card in list(self.controller.hand):
            yield Destroy(card)
        
        # 3. 清空牌库
        for card in list(self.controller.deck):
            yield Destroy(card)
        
        # 4. 用随机的抉择牌填充手牌
        for _ in range(hand_size):
            # 随机获取一张抉择牌
            card = yield Give(
                self.controller,
                RandomCollectible(card_filter=lambda c: GameTag.CHOOSE_ONE in c.tags)
            )
            # 减少1费
            if card and len(card) > 0:
                yield Buff(card[0], "TIME_707e")
        
        # 5. 用随机的抉择牌填充牌库
        for _ in range(deck_size):
            # 随机获取一张抉择牌并洗入牌库
            card = yield Shuffle(
                self.controller,
                RandomCollectible(card_filter=lambda c: GameTag.CHOOSE_ONE in c.tags)
            )
            # 减少1费
            if card and len(card) > 0:
                yield Buff(card[0], "TIME_707e")


class TIME_707e:
    """平行现实 - 减少1费"""
    tags = {GameTag.COST: -1}


# LEGENDARY

class TIME_211:
    """艾萨拉女士 - Lady Azshara
    [x]Fabled. Choose One - Empower Zin-Azshari; or The Well of Eternity. <i>(The other gets destroyed!)</i>
    
    5费 5/5 随从
    奇闻。抉择：强化辛艾萨莉；或者永恒之井。（未选择的选项会被摧毁！）
    
    完整实现：
    1. 使用标准的 Choose One 机制
    2. 两个选项分别对应不同的效果
    3. Fabled 机制：未选择的选项会被摧毁（由核心引擎处理）
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("TIME_211a", "TIME_211b")


class TIME_211a:
    """强化辛艾萨莉 - Empower Zin-Azshari
    
    选项1：强化辛艾萨莉（Fabled附带卡牌）
    效果：将辛艾萨莉洗入你的牌库
    """
    def play(self):
        # 将辛艾萨莉洗入牌库
        yield Shuffle(self.controller, "TIME_211t1")


class TIME_211b:
    """永恒之井 - The Well of Eternity
    
    选项2：永恒之井（Fabled附带卡牌）
    效果：将永恒之井加入手牌
    """
    def play(self):
        # 将永恒之井加入手牌
        yield Give(self.controller, "TIME_211t2")


class TIME_705:
    """纪元守护者克洛纳 - Krona, Keeper of Eons
    [x]Taunt Battlecry: Set the Costs of the bottom 5 cards of your deck to (1).
    
    6费 4/7 随从
    嘲讽。战吼：将你牌库底的五张牌的法力值消耗变为（1）点。
    
    完整实现：
    1. 获取牌库底的5张牌
    2. 将这些牌的费用设置为1（使用SET）
    """
    requirements = {}
    
    def play(self):
        # 获取牌库底的5张牌
        deck = self.controller.deck
        bottom_cards = deck[-5:] if len(deck) >= 5 else deck[:]
        
        # 将这些牌的费用设置为1
        for card in bottom_cards:
            yield Buff(card, "TIME_705e")


class TIME_705e:
    """纪元守护者克洛纳 - 费用变为1"""
    # 使用 cost 属性的 SET 函数来设置费用为1
    # 参考 the_lost_city/druid.py 的 DINO_432e
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    def cost(self, i):
        """将费用设置为1"""
        return 1
