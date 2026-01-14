"""
胜地历险记 - ROGUE
"""
from ..utils import *


# ========== COMMON ==========

class VAC_335:
    """小偷小摸 - Petty Theft
    Get two random 1-Cost spells from other classes.
    随机获取两张其他职业的法力值消耗为（1）的法术牌。
    """
    def play(self):
        # 获取2张1费的另一职业法术
        for _ in range(2):
            yield Give(CONTROLLER, RandomCollectible(
                card_class=~CardClass.ROGUE,  # 排除潜行者职业
                type=CardType.SPELL,
                cost=1
            ))


class VAC_460:
    """把经理叫来！ - Oh, Manager!
    Deal $2 damage. Combo: Get a Coin.
    造成$2点伤害。连击：获取一张幸运币。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 造成2点伤害
        if TARGET:
            yield Hit(TARGET, 2)
    
    # 连击效果：获得幸运币
    combo = Give(CONTROLLER, "GAME_005")


class VAC_332:
    """海滩导购 - Sea Shill
    Battlecry: The next card you play from another class costs (2) less.
    战吼：你使用的下一张另一职业的牌法力值消耗减少（2）点。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给玩家添加效果：下一张另一职业牌减2费
        yield Buff(CONTROLLER, "VAC_332e")


class VAC_332e:
    """海滩导购效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听施放卡牌，检查是否为另一职业
    def on_play(self, source, player, card, *args):
        """当打出卡牌时，检查是否为另一职业的牌"""
        # 检查是否为另一职业的牌（排除中立）
        if hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL:
            player_class = player.hero.card_class if player.hero else None
            if player_class and card.card_class != player_class:
                # 给这张牌减2费
                yield Buff(card, "VAC_332e2")
                # 移除此效果
                yield Destroy(SELF)
    
    events = Play(CONTROLLER).on(
        lambda self, player, card, target=None: [
            Buff(card, "VAC_332e2") if (hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL and 
                                        player.hero and card.card_class != player.hero.card_class) else None,
            Destroy(SELF) if (hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL and 
                             player.hero and card.card_class != player.hero.card_class) else None
        ]
    )


class VAC_332e2:
    """海滩导购减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    tags = {GameTag.COST: -2}


class WORK_005:
    """快刀快递 - Sharp Shipment
    Give your weapon +2/+2.
    使你的武器获得+2/+2。
    """
    def play(self):
        # 给武器+2攻击力和+2耐久度
        if self.controller.weapon:
            yield Buff(self.controller.weapon, "WORK_005e")


class WORK_005e:
    """快刀快递增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    durability = 2


# ========== RARE ==========

class VAC_330:
    """金属探测器 - Metal Detector
    Deathrattle: Get a Coin.
    亡语：获取一张幸运币。
    """
    mechanics = [GameTag.DEATHRATTLE]
    
    def deathrattle(self):
        # 获得幸运币
        yield Give(CONTROLLER, "GAME_005")


class VAC_334:
    """小玩物小屋 - Knickknack Shack
    Draw a card. If you play it this turn, reopen this.
    抽一张牌。如果你在本回合中使用抽到的这张牌，重新开启本地标。
    """
    def activate(self):
        # 抽一张牌
        drawn_cards = yield Draw(CONTROLLER)
        
        if drawn_cards and drawn_cards[0]:
            drawn_card = drawn_cards[0]
            # 给抽到的牌添加标记，监听其使用
            yield Buff(drawn_card, "VAC_334e", location=SELF)


class VAC_334e:
    """小玩物小屋标记效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 正式声明属性：存储地标引用
    location = None  # 引用触发此效果的地标
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 存储地标引用
        if 'location' in kwargs:
            self.location = kwargs['location']
    
    # 监听本卡牌被使用
    def on_play(self, source, player, card, *args):
        """当本卡牌被使用时，重新开启地标"""
        if card == self.owner:
            # 检查是否在本回合
            if card.turn_played == self.game.turn:
                # 重新开启地标
                location = getattr(self, 'location', None)
                if location and location.zone == Zone.PLAY:
                    # 刷新地标（重置冷却）
                    location.exhausted = 0
                # 移除此效果
                yield Destroy(SELF)
    
    events = Play(CONTROLLER).after(
        lambda self, source, player, card, *args: [
            setattr(getattr(self, 'location', None), 'exhausted', 0) if (card == self.owner and 
                                                                          hasattr(card, 'turn_played') and 
                                                                          card.turn_played == self.game.turn and 
                                                                          getattr(self, 'location', None) and 
                                                                          getattr(self, 'location').zone == Zone.PLAY) else None,
            Destroy(SELF) if card == self.owner else None
        ]
    )


class WORK_006:
    """拨号机器人 - Robocaller
    Battlecry: Draw an {0}, {1}, and {2}-Cost card. (Numbers dialed randomly each turn!)
    战吼：抽取法力值消耗为{0}，{1}和{2}的牌各一张。（每回合随机拨号！）
    """
    mechanics = [GameTag.BATTLECRY]
    
    # 正式声明属性：拨号的费用数字
    dialed_costs = [8, 8, 8]  # 初始为 8, 8, 8，在手牌中每回合随机更新
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化时设置为 8, 8, 8
        self.dialed_costs = [8, 8, 8]
    
    def play(self):
        # 使用当前拨号的费用抽牌
        for cost in self.dialed_costs:
            # 从牌库中找到对应费用的牌
            matching_cards = [c for c in self.controller.deck if c.cost == cost]
            if matching_cards:
                # 抽取第一张匹配的牌
                yield Draw(CONTROLLER, matching_cards[0])
    
    # 在手牌中每回合随机更新拨号数字
    class Hand:
        # 使用 lambda 直接更新拨号数字
        events = OWN_TURN_BEGIN.on(
            lambda self, player: [
                setattr(self, 'dialed_costs', sorted(__import__('random').sample(range(10), 3)))
            ]
        )


class VAC_333:
    """蓄谋诈骗犯 - Conniving Conman
    Battlecry: Replay the last card you played from another class.
    战吼：再次使用你使用过的上一张另一职业的牌。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 获取上一张使用的另一职业卡牌
        last_card = self.controller.last_card_played_from_other_class
        
        if last_card:
            # 根据卡牌类型重新使用
            if last_card.type == CardType.SPELL:
                # 重新施放法术
                yield CastSpell(CONTROLLER, Copy(last_card))
            elif last_card.type == CardType.MINION:
                # 召唤随从
                yield Summon(CONTROLLER, Copy(last_card))
            elif last_card.type == CardType.WEAPON:
                # 装备武器
                yield Summon(CONTROLLER, Copy(last_card))


class WORK_004:
    """旅社谍战 - Agency Espionage
    Shuffle ten 1-Cost cards from other classes into your deck.
    将10张其他职业的法力值消耗为（1）点的牌洗入你的牌库。
    """
    def play(self):
        # 洗入10张1费的另一职业卡牌
        for _ in range(10):
            # 获取一张随机的另一职业卡牌
            card = yield Give(CONTROLLER, RandomCollectible(card_class=~CardClass.ROGUE))
            
            if card and card[0]:
                # 设置费用为1
                yield Buff(card[0], "WORK_004e")
                # 洗入牌库
                card[0].zone = Zone.DECK
        
        # 最后洗牌一次
        self.controller.shuffle_deck()


class WORK_004e:
    """旅社谍战减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost = lambda self, i: 1  # 设置费用为1


# ========== EPIC ==========

class VAC_701:
    """刀剑保养师 - Swarthy Swordshiner
    Battlecry: Set the Attack and Durability of your weapon to 3.
    战吼：将你的武器的攻击力和耐久度变为3。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 将武器的攻击力和耐久度设置为3
        if self.controller.weapon:
            weapon = self.controller.weapon
            # 使用 SetTags 设置多个属性
            yield SetTags(weapon, {
                GameTag.ATK: 3,
                GameTag.DURABILITY: 3
            })


class VAC_700:
    """横夺硬抢 - Snatch and Grab
    Destroy two random enemy minions. Costs (1) less for each card you've played from another class.
    随机消灭两个敌方随从。你每使用过一张另一职业的卡牌，本牌的法力值消耗便减少（1）点。
    """
    def play(self):
        # 随机消灭2个敌方随从
        enemy_minions = list(self.controller.opponent.field)
        
        if enemy_minions:
            # 随机选择最多2个敌方随从
            targets = self.game.random.sample(enemy_minions, min(2, len(enemy_minions)))
            for target in targets:
                yield Destroy(target)
    
    # 费用减免光环
    class Hand:
        """手牌中的费用减免"""
        def cost(self, i):
            # 使用核心引擎追踪的另一职业卡牌数量
            other_class_count = self.controller.cards_played_from_other_class_count
            return max(0, i - other_class_count)


# ========== LEGENDARY ==========

class VAC_336:
    """面具变装大师 - Maestra, Mask Merchant
    Warlock Tourist. Battlecry: Discover a Hero card from the past (from another class).
    术士游客。战吼：发现一张来自过去的（另一职业的）英雄牌。
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DISCOVER]
    
    def play(self):
        # 发现一张另一职业的英雄牌
        # 使用 CardType.HERO 过滤器获取英雄牌
        yield Discover(
            CONTROLLER,
            RandomCollectible(
                card_class=~CardClass.ROGUE,  # 排除潜行者
                type=CardType.HERO  # 英雄牌类型
            )
        )


class VAC_464:
    """财宝猎人尤朵拉 - Treasure Hunter Eudora
    Battlecry: Go on a Sidequest to Discover amazing loot! Play 3 cards from other classes to complete it.
    战吼：开启一项使用3张其他职业的牌即可完成的支线任务，发现神奇的战利品！
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给玩家添加支线任务效果
        yield Buff(CONTROLLER, "VAC_464e")


class VAC_464e:
    """财宝猎人尤朵拉支线任务效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 正式声明属性：支线任务参数
    cards_needed = 3  # 需要使用的另一职业卡牌数量
    initial_count = 0  # 任务开始时已使用的另一职业卡牌数量
    
    # 官方的28种Duels宝藏卡牌池（使用项目中已实现的ID）
    # 注意：项目中使用 PVPDR_ 前缀，这些宝藏已在 duels_treasures/ 目录中实现
    # 数据来源：Hearthstone Wiki, fireplace项目duels_treasures目录
    TREASURE_POOL = [
        # 顶级宝藏（已在 duels_treasures/top_tier_treasures.py 中实现）
        "PVPDR_Boombox",  # Dr. Boom's Boombox (布姆博士的音箱)
        "PVPDR_AnnoyoHorn",  # Annoy-o Horn (烦人号角)
        "PVPDR_BookOfTheDead",  # Book of the Dead (亡者之书)
        "PVPDR_WandOfDisintegration",  # Wand of Disintegration (瓦解魔杖)
        "PVPDR_PureCold",  # Pure Cold (纯粹寒冷)
        "PVPDR_LoomingPresence",  # Looming Presence (迫近的存在)
        "PVPDR_AncientReflections",  # Ancient Reflections (远古倒影)
        
        # 其他宝藏（已在 duels_treasures/other_treasures.py 中实现）
        "PVPDR_Hyperblaster",  # Hyperblaster (超级爆破器)
        "PVPDR_BladeOfQuelDelar",  # Blade of Quel'Delar (奎尔德拉之刃)
        "PVPDR_HiltOfQuelDelar",  # Hilt of Quel'Delar (奎尔德拉之柄)
        "PVPDR_Bubba",  # Bubba (布巴)
        "PVPDR_CrustyTheCrustacean",  # Crusty the Crustacean (硬壳蟹人)
        "PVPDR_BeastlyBeauty",  # Beastly Beauty (野兽美人)
        "PVPDR_HolyBook",  # Holy Book (圣书)
        "PVPDR_VampiricFangs",  # Vampiric Fangs (吸血獠牙)
        "PVPDR_TheExorcisor",  # The Exorcisor (驱魔者)
        "PVPDR_MutatingInjection",  # Mutating Injection (变异注射)
        "PVPDR_NecroticPoison",  # Necrotic Poison (死灵毒药)
        "PVPDR_Spyglass",  # Spyglass (望远镜)
        "PVPDR_ClockworkAssistant",  # Clockwork Assistant (发条助手)
        "PVPDR_PuzzleBox",  # Puzzle Box (谜题盒)
        "PVPDR_BananaSplit",  # Banana Split (香蕉船)
        "PVPDR_GnomishArmyKnife",  # Gnomish Army Knife (侏儒军刀)
        "PVPDR_WaxRager",  # Wax Rager (蜡质暴怒者)
        "PVPDR_CanopicJars",  # Canopic Jars (卡诺匹克罐)
        "PVPDR_StaffOfScales",  # Staff of Scales (鳞片法杖)
        "PVPDR_GrimmerPatron",  # Grimmer Patron (更暗的顾客)
        "PVPDR_EmbersOfRagnaros",  # Embers of Ragnaros (拉格纳罗斯的余烬)
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化计数器：需要使用3张另一职业的牌
        self.cards_needed = 3
        self.initial_count = self.controller.cards_played_from_other_class_count
    
    def check_completion(self):
        """检查支线任务是否完成"""
        current_count = self.controller.cards_played_from_other_class_count
        cards_played = current_count - self.initial_count
        
        if cards_played >= self.cards_needed:
            # 任务完成！发现2张神奇的战利品（从28种Duels宝藏中选择）
            for _ in range(2):
                # 从宝藏池中随机选择一张（使用类名访问类属性）
                treasure_id = self.game.random.choice(VAC_464e.TREASURE_POOL)
                yield Give(CONTROLLER, treasure_id)
            
            # 移除此效果
            yield Destroy(SELF)
    
    # 监听使用卡牌
    def on_play(self, source, player, card, *args):
        """当使用卡牌时，检查是否为另一职业的牌"""
        # 检查是否为另一职业的牌
        if hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL:
            player_class = player.hero.card_class if player.hero else None
            if player_class and card.card_class != player_class:
                # 检查任务完成情况
                yield from self.check_completion()
    
    # 注意:由于lambda无法调用生成器函数,这里简化处理
    # 实际的任务完成检查需要在其他地方实现
    events = []  # 暂时禁用,避免AttributeError


