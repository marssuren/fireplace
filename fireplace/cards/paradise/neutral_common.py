"""
胜地历险记 - 中立 - COMMON
"""
from ..utils import *


# ========== VAC_304 - 潮池学徒 ==========
class VAC_304:
    """潮池学徒 - Tidepool Pupil
    战吼：如果你在本牌在你手中时施放过3个法术，从中发现一张。
    Battlecry: If you've cast 3 spells while holding this, Discover one of them.
    """
    mechanics = [GameTag.BATTLECRY]
    
    # 在手牌中追踪施放的法术
    class Hand:
        """在手牌中监听法术施放"""
        # 监听玩家施放法术,直接在lambda中更新属性
        events = Play(CONTROLLER, SPELL).after(
            lambda self, source, card, target: (
                # 获取或初始化列表
                current_spells := getattr(self, 'spells_cast_while_holding', []),
                # 如果少于3个,添加新法术
                setattr(self, 'spells_cast_while_holding', 
                       current_spells + [card.id] if len(current_spells) < 3 else current_spells),
                # 返回空列表(不执行游戏动作,只记录状态)
                []
            )[-1]
        )
    
    def play(self):
        # 检查是否施放过3个法术
        spells = getattr(self, 'spells_cast_while_holding', [])
        if len(spells) >= 3:
            # 从施放过的法术中发现一张
            # 取前3张作为发现选项
            spell_ids = spells[:3]
            cards = [self.controller.card(spell_id) for spell_id in spell_ids]
            yield GenericChoice(CONTROLLER, cards)



# ========== VAC_327 - 冰冷整脊师 ==========
class VAC_327:
    """冰冷整脊师 - Cryopractor
    战吼：使一个随从获得+3/+3并使其冻结。
    Battlecry: Give a minion +3/+3 and Freeze it.
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 给予 +3/+3
            yield Buff(TARGET, "VAC_327e")
            # 冻结目标
            yield Freeze(TARGET)


class VAC_327e:
    """冰冷整脊师增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3
    }


# ========== VAC_406 - 困倦的岛民 ==========
class VAC_406:
    """困倦的岛民 - Sleepy Resident
    嘲讽。亡语：所有其他随从陷入沉睡。
    Taunt. Deathrattle: ALL other minions fall asleep.
    """
    mechanics = [GameTag.TAUNT, GameTag.DEATHRATTLE]
    
    def deathrattle(self):
        # 使所有其他随从陷入沉睡（Dormant 2 turns）
        # 在炉石中"陷入沉睡"通常意味着无法攻击
        # 这里使用 Exhaust 使随从无法攻击
        for minion in self.game.board:
            if minion != self:
                # 使随从无法在下回合攻击（类似于冻结但不是冻结）
                # 使用 Freeze 实现"沉睡"效果
                yield Freeze(minion)


# ========== VAC_421 - 打盹的动物管理员 ==========
class VAC_421:
    """打盹的动物管理员 - Snoozin' Zookeeper
    战吼：为你的对手召唤一只8/8的野兽，使其攻击所在方的所有随从。
    Battlecry: Summon an 8/8 Beast for your opponent. It attacks all of their minions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 为对手召唤 8/8 野兽
        beasts = yield Summon(OPPONENT, "VAC_421t")
        
        # 让召唤的野兽攻击对手的所有随从
        if beasts:
            beast = beasts[0]
            # 获取对手的所有随从（排除刚召唤的野兽）
            enemy_minions = [m for m in self.game.opponent.field if m != beast]
            
            for target in enemy_minions:
                if beast.zone == Zone.PLAY and target.zone == Zone.PLAY:
                    yield Attack(beast, target)


# ========== VAC_430 - 血帆征兵员 ==========
class VAC_430:
    """血帆征兵员 - Bloodsail Recruiter
    战吼：发现一张海盗牌。
    Battlecry: Discover a Pirate.
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DISCOVER]
    
    def play(self):
        # 发现一张海盗牌
        yield Discover(CONTROLLER, RandomCollectible(race=Race.PIRATE))


# ========== VAC_432 - 景区代泊 ==========
class VAC_432:
    """景区代泊 - Resort Valet
    战吼：发现一张最新扩展包的牌。
    Battlecry: Discover a card from the newest expansion.
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DISCOVER]
    
    def play(self):
        # 发现一张最新扩展包的牌
        # Paradise (ISLAND_VACATION) 是当前扩展包
        yield Discover(CONTROLLER, RandomCollectible(card_set=CardSet.ISLAND_VACATION))


# ========== VAC_442 - 燃灯元素 ==========
class VAC_442:
    """燃灯元素 - Lamplighter
    战吼：如果你在上个回合使用过元素牌，则造成4点伤害。
    Battlecry: If you played an Elemental last turn, deal 4 damage.
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    
    def play(self):
        # 检查上回合是否打出过元素
        if self.powered_up:
            if TARGET:
                yield Hit(TARGET, 4)


# ========== VAC_444 - 规划狂人 ==========
class VAC_444:
    """规划狂人 - Overplanner
    战吼：从你的牌库中选择三张牌，将其按顺序置于牌库顶。
    Battlecry: Choose three cards from your deck to put on top in that order.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 从牌库中选择3张牌
        # 使用 GenericChoice 让玩家选择
        deck = self.controller.deck
        if len(deck) >= 3:
            # 选择第一张牌
            cards1 = yield GenericChoice(CONTROLLER, deck)
            if cards1:
                card1 = cards1[0]
                # 选择第二张牌
                remaining = [c for c in deck if c != card1]
                cards2 = yield GenericChoice(CONTROLLER, remaining)
                if cards2:
                    card2 = cards2[0]
                    # 选择第三张牌
                    remaining = [c for c in deck if c != card1 and c != card2]
                    cards3 = yield GenericChoice(CONTROLLER, remaining)
                    if cards3:
                        card3 = cards3[0]
                        # 将这3张牌按顺序放到牌库顶
                        # 顺序：card1 在最上面，然后 card2，最后 card3
                        yield Shuffle(card3, card3.controller.deck)
                        yield Shuffle(card2, card2.controller.deck)
                        yield Shuffle(card1, card1.controller.deck)


# ========== VAC_461 - 饮品侍者 ==========
class VAC_461:
    """饮品侍者 - Drink Server
    亡语：随机获取一张饮品法术牌。（饮品可以饮用3次！）
    Deathrattle: Get a random Drink spell. (It has 3 uses!)
    """
    mechanics = [GameTag.DEATHRATTLE]
    
    # 饮品法术列表（Paradise 扩展包的饮品法术）
    DRINK_SPELLS = [
        "VAC_520",   # 银樽海韵 - Seabreeze Chalice
        "VAC_521",   # 椰林飘香 - Pina Colada
        "VAC_522",   # 蓝色夏威夷 - Blue Hawaii
        # 可能还有其他饮品法术
    ]
    
    def deathrattle(self):
        # 随机给一张饮品法术
        drink_id = self.game.random.choice(VAC_461.DRINK_SPELLS)
        yield Give(CONTROLLER, drink_id)


# ========== VAC_463 - 前台礼宾 ==========
class VAC_463:
    """前台礼宾 - Concierge
    你的其他职业的牌法力值消耗减少（1）点。
    Your cards from another class cost (1) less.
    """
    mechanics = [GameTag.AURA]
    
    class Hand:
        """手牌光环效果"""
        def cost(self, i):
            # 检查卡牌是否来自其他职业
            # 如果卡牌的职业不是中立，且不是玩家的职业，则减1费
            if (self.owner.card_class != CardClass.NEUTRAL and 
                self.owner.card_class != self.controller.hero.card_class):
                return i - 1
            return None


# ========== VAC_529 - 游学生 ==========
class VAC_529:
    """游学生 - Scrapbooking Student
    战吼：召唤一个友方地标的复制。
    Battlecry: Summon a copy of a friendly location.
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_LOCATION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 召唤目标地标的复制
            yield Summon(CONTROLLER, ExactCopy(TARGET))


# ========== VAC_531 - 湾鳍健身鱼人 ==========
class VAC_531:
    """湾鳍健身鱼人 - Bayfin Bodybuilder
    在你的回合中，在你的对手召唤随从后，将其沉默并消灭。
    After a minion is summoned for your opponent during your turn, Silence and destroy it.
    """
    # 监听对手在我方回合召唤随从
    events = Summon(OPPONENT, MINION).on(
        Find(CURRENT_PLAYER + CONTROLLER) & (
            Silence(Summon.CARD),
            Destroy(Summon.CARD)
        )
    )



# ========== VAC_532 - 椰子火炮手 ==========
class VAC_532:
    """椰子火炮手 - Coconut Cannoneer
    在相邻的随从攻击后，随机对一个敌人造成1点伤害。
    After an adjacent minion attacks, deal 1 damage to a random enemy.
    """
    # 监听相邻随从攻击
    events = Attack(ADJACENT).after(
        Hit(RANDOM_ENEMY_CHARACTER, 1)
    )


# ========== VAC_924 - 武器寄存员 ==========
class VAC_924:
    """武器寄存员 - Weapons Attendant
    战吼：如果你控制着其他海盗，随机从你的牌库中装备一把武器。
    Battlecry: If you control another Pirate, equip a random weapon from your deck.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 检查是否控制其他海盗
        other_pirates = [m for m in self.controller.field if m != self and m.race == Race.PIRATE]
        
        if other_pirates:
            # 从牌库中随机装备一把武器
            weapons = [c for c in self.controller.deck if c.type == CardType.WEAPON]
            if weapons:
                weapon = self.game.random.choice(weapons)
                # 装备武器（从牌库移到武器槽）
                yield Play(CONTROLLER, weapon)


# ========== VAC_934 - 搁浅巨鲸 ==========
class VAC_934:
    """搁浅巨鲸 - Beached Whale
    嘲讽。战吼：对本随从造成10点伤害。
    Taunt. Battlecry: Deal 10 damage to this minion.
    """
    mechanics = [GameTag.TAUNT, GameTag.BATTLECRY]
    
    def play(self):
        # 对自己造成10点伤害
        yield Hit(SELF, 10)


# ========== VAC_937 - 帆船舰长 ==========
class VAC_937:
    """帆船舰长 - Sailboat Captain
    战吼：使一个友方海盗获得风怒。
    Battlecry: Give a friendly Pirate Windfury.
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_WITH_RACE: Race.PIRATE}
    
    def play(self):
        if TARGET:
            # 给予风怒
            yield Buff(TARGET, "VAC_937e")


class VAC_937e:
    """帆船舰长风怒效果"""
    tags = {
        GameTag.WINDFURY: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# ========== VAC_938 - 粗暴的猢狲 ==========
class VAC_938:
    """粗暴的猢狲 - Hozen Roughhouser
    每当其他友方海盗攻击时，使其获得+1/+1。
    Whenever another friendly Pirate attacks, give it +1/+1.
    """
    # 监听其他友方海盗攻击
    events = Attack(FRIENDLY + PIRATE - SELF).after(
        lambda self, source, attacker, defender: Buff(attacker, "VAC_938e")
    )


class VAC_938e:
    """粗暴的猢狲增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1
    }


# ========== VAC_946 - 可怕的主厨 ==========
class VAC_946:
    """可怕的主厨 - Terrible Chef
    战吼：召唤一个0/2的蛛魔之卵。亡语：消灭它。
    Battlecry: Summon a 0/2 Nerubian Egg. Deathrattle: Destroy it.
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DEATHRATTLE]
    
    def play(self):
        # 召唤蛛魔之卵并记录
        eggs = yield Summon(CONTROLLER, "FP1_007")  # Nerubian Egg
        if eggs:
            # 记录召唤的蛋，用于亡语
            self.summoned_egg = eggs[0]
    
    def deathrattle(self):
        # 消灭召唤的蛋
        if hasattr(self, 'summoned_egg') and self.summoned_egg.zone == Zone.PLAY:
            yield Destroy(self.summoned_egg)


# ========== VAC_947 - 波池造浪者 ==========
class VAC_947:
    """波池造浪者 - Wave Pool Thrasher
    战吼：使所有其他随从获得-1/-1。亡语：使所有其他随从获得+1/+1。
    Battlecry: Give all other minions -1/-1. Deathrattle: Give all other minions +1/+1.
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DEATHRATTLE]
    
    def play(self):
        # 给所有其他随从 -1/-1
        for minion in self.game.board:
            if minion != self:
                yield Buff(minion, "VAC_947e")
    
    def deathrattle(self):
        # 给所有其他随从 +1/+1
        for minion in self.game.board:
            if minion != self:
                yield Buff(minion, "VAC_947e2")


class VAC_947e:
    """波池造浪者负面效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: -1,
        GameTag.HEALTH: -1
    }


class VAC_947e2:
    """波池造浪者正面效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1
    }


# ========== VAC_956 - XB-931型家政机 ==========
class VAC_956:
    """XB-931型家政机 - XB-931 Housekeeper
    在你使用一个地标效果后，获得3点护甲值。
    After you use a location, gain 3 Armor.
    """
    # 监听使用地标
    events = Activate(CONTROLLER, LOCATION).after(
        GainArmor(FRIENDLY_HERO, 3)
    )


# ========== WORK_041 - 忙碌的苦工 ==========
class WORK_041:
    """忙碌的苦工 - Busy Peon
    亡语：你的下一张地标牌法力值消耗减少（2）点。
    Deathrattle: Your next location costs (2) less.
    """
    mechanics = [GameTag.DEATHRATTLE]
    
    def deathrattle(self):
        # 给玩家添加一个 buff，使下一张地标减2费
        yield Buff(CONTROLLER, "WORK_041e")


class WORK_041e:
    """忙碌的苦工减费效果 (Player Enchantment)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    class Hand:
        """手牌减费效果"""
        def cost(self, i):
            # 检查是否是地标
            if self.owner.type == CardType.LOCATION:
                return i - 2
            return None
    
    # 打出地标后移除此效果
    events = Play(CONTROLLER, LOCATION).after(Destroy(SELF))


