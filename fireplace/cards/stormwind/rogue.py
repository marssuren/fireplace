# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 潜行者
"""

from ..utils import *

class DED_004:
    """黑水弯刀 / Blackwater Cutlass
    可交易 在你交易此牌后，使你手牌中一张法术牌的费用减少（1）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 2,
        GameTag.COST: 2,
    }
    
    # 交易后减费
    trade = Find(FRIENDLY_HAND + SPELL) & Buff(RANDOM(FRIENDLY_HAND + SPELL), "DED_004e")


class DED_004e:
    """黑水弯刀减费"""
    cost = -1


class DED_005:
    """海盗谈判 / Parrrley
    将此牌与你对手牌库中的一张牌交换。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """与对手牌库中的一张牌交换"""
        # 从对手牌库中随机抽一张牌给自己
        if self.controller.opponent.deck:
            yield Give(CONTROLLER, Random(OPPONENT_DECK))
            # 将此牌洗入对手牌库
            yield Shuffle(OPPONENT, Copy(SELF))


class DED_510:
    """艾德温，迪菲亚首脑 / Edwin, Defias Kingpin
    战吼：抽一张牌。如果你在本回合打出它，获得+2/+2并重复此效果。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    def play(self):
        """抽牌，如果本回合打出则获得+2/+2并重复"""
        # 抽一张牌
        drawn_cards = yield Draw(CONTROLLER)
        
        # 给自己添加buff，监听打出刚抽的牌
        if drawn_cards:
            # Draw可能返回单张牌或列表
            drawn_card = drawn_cards[0] if isinstance(drawn_cards, list) else drawn_cards
            yield Buff(SELF, "DED_510e", tracked_card_id=drawn_card.id)


class DED_510e:
    """艾德温追踪器"""
    def __init__(self, tracked_card_id):
        self.tracked_card_id = tracked_card_id
    
    def apply(self, target):
        """保存追踪的卡牌ID"""
        if not hasattr(target, 'edwin_tracked_cards'):
            target.edwin_tracked_cards = set()
        target.edwin_tracked_cards.add(self.tracked_card_id)
    
    # 监听打出卡牌
    events = Play(CONTROLLER).after(
        lambda self: self._on_card_played()
    )
    
    def _on_card_played(self):
        """当打出卡牌时检查是否是追踪的牌"""
        played_card = Play.CARD
        
        # 检查是否是追踪的牌
        if (hasattr(self.owner, 'edwin_tracked_cards') and 
            played_card.id in self.owner.edwin_tracked_cards):
            
            # 移除已打出的牌的追踪
            self.owner.edwin_tracked_cards.remove(played_card.id)
            
            # 获得+2/+2
            yield Buff(self.owner, "DED_510_buff")
            
            # 重复效果：抽一张牌
            drawn_cards = yield Draw(CONTROLLER)
            
            # 继续追踪新抽的牌
            if drawn_cards:
                drawn_card = drawn_cards[0] if isinstance(drawn_cards, list) else drawn_cards
                # 添加新的追踪
                self.owner.edwin_tracked_cards.add(drawn_card.id)


class DED_510_buff:
    """艾德温增益"""
    atk = 2
    max_health = 2

class SW_050:
    """变装大师 / Maestra of the Masquerade
    游戏开始时以不同职业的身份开始，直到你打出一张盗贼牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    def play(self):
        """打出变装大师，如果还在伪装中则揭示身份"""
        # 如果还在伪装中，恢复真实身份
        if hasattr(self.controller, 'maestra_disguise_active'):
            yield from self._reveal_identity()
    
    def _reveal_identity(self):
        """揭示真实身份"""
        controller = self.controller
        
        # 恢复原始英雄
        if hasattr(controller, 'maestra_original_hero_id'):
            from ..actions import ReplaceHero
            
            # 使用ReplaceHero动作恢复原始英雄
            yield ReplaceHero(controller, controller.maestra_original_hero_id)
            delattr(controller, 'maestra_original_hero_id')
        
        # 标记伪装已结束
        if hasattr(controller, 'maestra_disguise_active'):
            delattr(controller, 'maestra_disguise_active')
        
        # 移除监听器
        if hasattr(controller, 'maestra_reveal_listener'):
            delattr(controller, 'maestra_reveal_listener')
    
    @staticmethod
    def apply_disguise(player):
        """
        应用职业伪装（在游戏开始时调用）
        完整替换英雄，包括英雄肖像和英雄技能
        """
        from ..actions import ReplaceHero
        
        # 随机选择一个其他职业
        other_classes = [
            CardClass.DRUID, CardClass.HUNTER, CardClass.MAGE,
            CardClass.PALADIN, CardClass.PRIEST, CardClass.SHAMAN,
            CardClass.WARLOCK, CardClass.WARRIOR, CardClass.DEMONHUNTER
        ]
        
        import random
        disguise_class = random.choice(other_classes)
        
        # 保存原始英雄ID（用于恢复）
        player.maestra_original_hero_id = player.hero.id
        
        # 根据职业选择对应的英雄
        disguise_hero_id = {
            CardClass.DRUID: "HERO_06",  # 玛法里奥·怒风
            CardClass.HUNTER: "HERO_05",  # 雷克萨
            CardClass.MAGE: "HERO_08",  # 吉安娜·普罗德摩尔
            CardClass.PALADIN: "HERO_04",  # 乌瑟尔·光明使者
            CardClass.PRIEST: "HERO_09",  # 安度因·乌瑞恩
            CardClass.SHAMAN: "HERO_02",  # 萨尔
            CardClass.WARLOCK: "HERO_07",  # 古尔丹
            CardClass.WARRIOR: "HERO_01",  # 加尔鲁什·地狱咆哮
            CardClass.DEMONHUNTER: "HERO_10",  # 伊利丹·怒风
        }.get(disguise_class)
        
        if disguise_hero_id:
            # 使用ReplaceHero动作替换整个英雄
            # 这会保留生命值、护甲等状态
            player.game.queue_actions(player.hero, [ReplaceHero(player, disguise_hero_id)])
        
        # 标记伪装激活
        player.maestra_disguise_active = True
        player.maestra_disguise_class = disguise_class
        
        # 添加监听器：打出盗贼牌时揭示身份
        player.maestra_reveal_listener = SW_050e(player)


class SW_050e:
    """变装大师揭示监听器"""
    def __init__(self, player):
        self.controller = player
    
    # 监听打出盗贼牌
    events = Play(CONTROLLER).after(
        lambda self: self._check_reveal()
    )
    
    def _check_reveal(self):
        """检查是否打出盗贼牌"""
        played_card = Play.CARD
        
        # 检查是否是盗贼牌
        if (hasattr(played_card, 'card_class') and 
            played_card.card_class == CardClass.ROGUE):
            
            # 揭示身份
            controller = self.controller
            
            # 恢复原始英雄
            if hasattr(controller, 'maestra_original_hero_id'):
                from ..actions import ReplaceHero
                
                # 使用ReplaceHero动作恢复原始英雄
                yield ReplaceHero(controller, controller.maestra_original_hero_id)
                delattr(controller, 'maestra_original_hero_id')
            
            # 移除监听器
            if hasattr(controller, 'maestra_reveal_listener'):
                delattr(controller, 'maestra_reveal_listener')
            
            # 标记伪装已结束
            if hasattr(controller, 'maestra_disguise_active'):
                delattr(controller, 'maestra_disguise_active')
            
            if hasattr(controller, 'maestra_disguise_class'):
                delattr(controller, 'maestra_disguise_class')


class SW_052:
    """探查内鬼 / Find the Imposter
    任务线：打出2张SI:7牌。奖励：将一个间谍装置置入你的手牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段打出2张SI:7牌
    questline_requirements = [2, 2, 2]
    
    def play(self):
        """打出任务线"""
        from ..enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_052e")
    
    def questline_reward_1(self):
        """阶段1奖励：间谍装置"""
        return [Give(CONTROLLER, "SW_052t")]
    
    def questline_reward_2(self):
        """阶段2奖励：间谍装置"""
        return [Give(CONTROLLER, "SW_052t2")]
    
    def questline_reward_3(self):
        """阶段3奖励：间谍装置"""
        return [Give(CONTROLLER, "SW_052t3")]


class SW_052e:
    """探查内鬼追踪器"""
    # 监听打出SI:7牌（卡牌名称包含"SI:7"）
    events = Play(CONTROLLER).after(
        lambda self: [
            Find(FRIENDLY_SECRETS + ID("SW_052")) &
            QuestlineProgress(FRIENDLY_SECRETS + ID("SW_052"), 2)
        ] if "SI:7" in Play.CARD.name or "军情七处" in Play.CARD.name else None
    )


class SW_052t:
    """间谍装置 / Spy Gizmo
    发现一张牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    # 发现一张随机牌
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomCollectible()))


class SW_052t2:
    """间谍装置（强化）/ Spy Gizmo
    发现一张牌。其法力值消耗减少（1）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """发现一张牌并减费"""
        discovered = yield GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomCollectible()))
        if discovered:
            yield Buff(discovered, "SW_052t2e")


class SW_052t2e:
    """间谍装置减费"""
    cost = -1


class SW_052t3:
    """间谍装置（完全强化）/ Spy Gizmo
    发现一张牌。其法力值消耗减少（2）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """发现一张牌并减费2点"""
        discovered = yield GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomCollectible()))
        if discovered:
            yield Buff(discovered, "SW_052t3e")


class SW_052t3e:
    """间谍装置减费（强化）"""
    cost = -2


class SW_310:
    """伪造的匕首 / Counterfeit Blade
    战吼：获得本局游戏中死亡的一个随机友方亡语随从的复制。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    
    def play(self):
        """获得死亡的随机友方亡语随从的复制"""
        # 从墓地中找到亡语随从
        deathrattle_minions = [
            minion for minion in self.controller.graveyard
            if minion.type == CardType.MINION and hasattr(minion, 'deathrattle')
        ]
        
        if deathrattle_minions:
            # 随机选择一个
            target = self.game.random.choice(deathrattle_minions)
            yield Give(CONTROLLER, Copy(target))


class SW_311:
    """锁喉 / Garrote
    对敌方英雄造成$2点伤害。将3张流血洗入你的牌库，抽到时造成$2点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    play = Hit(ENEMY_HERO, 2) & Shuffle(CONTROLLER, "SW_311t") * 3


class SW_311t:
    """流血 / Bleed"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    # 抽到时触发：造成2点伤害
    draw = Hit(ENEMY_HERO, 2)


class SW_405:
    """简略情报 / Sketchy Information
    抽一张法力值消耗小于或等于（4）点的亡语牌。触发其亡语。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """抽取亡语牌并触发亡语"""
        # 抽一张费用<=4的亡语牌
        drawn = yield ForceDraw(CONTROLLER, 
                               FRIENDLY_DECK + DEATHRATTLE + (COST <= 4))
        
        if drawn and hasattr(drawn, 'deathrattle'):
            # 触发亡语
            yield drawn.deathrattle


class SW_411:
    """军情七处线人 / SI:7 Informant
    战吼：每有一张其他SI:7牌在本局游戏中被打出，便获得+1/+1。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    
    def play(self):
        """根据打出的SI:7牌数量获得buff"""
        # 统计打出的SI:7牌（不包括自己）
        si7_count = sum(
            1 for card in self.controller.cards_played_this_game
            if ("SI:7" in card.name or "军情七处" in card.name) and card != self
        )
        
        if si7_count > 0:
            # 每张SI:7牌给予+1/+1
            yield Buff(SELF, "SW_411e") * si7_count


class SW_411e:
    """军情七处线人增益"""
    atk = 1
    max_health = 1


class SW_412:
    """军情七处的要挟 / SI:7 Extortion
    可交易 对一个未受伤的角色造成$3点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Hit(TARGET, 3)


class SW_413:
    """军情七处探员 / SI:7 Operative
    突袭 在本随从攻击一个随从后，获得潜行。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.RUSH: True,
    }
    
    # 攻击随从后获得潜行
    events = Attack(SELF, MINION).after(
        SetTag(SELF, {GameTag.STEALTH: True})
    )


class SW_417:
    """军情七处刺客 / SI:7 Assassin
    你每在本局游戏中打出一张SI:7牌，本牌的法力值消耗便减少（1）点。连击：消灭一个敌方随从。"""
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
    }
    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    # 动态费用减少
    @property
    def cost(self):
        """根据打出的SI:7牌数量减费"""
        base_cost = 7
        if hasattr(self, 'controller'):
            si7_count = sum(
                1 for card in self.controller.cards_played_this_game
                if "SI:7" in card.name or "军情七处" in card.name
            )
            return max(0, base_cost - si7_count)
        return base_cost
    
    # 连击：消灭敌方随从
    combo = Destroy(TARGET)


class SW_434:
    """放贷的鲨鱼 / Loan Shark
    战吼：给你的对手一个幸运币。亡语：你获得两个幸运币。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    
    # 战吼：给对手一个幸运币
    play = Give(OPPONENT, "GAME_005")
    
    # 亡语：自己获得两个幸运币
    deathrattle = Give(CONTROLLER, "GAME_005") * 2
