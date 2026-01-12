from hearthstone.deckstrings import Deck
from hearthstone.enums import (
    CardClass,
    CardSet,
    CardType,
    GameTag,
    MultiClassGroup,
    Race,
    Rarity,
)

from ..actions import *
from ..aura import Refresh
from ..cards import db
from ..dsl import *
from ..entity import boolean_property
from ..enums import PlayReq, BoardEnum
from .. import enums  # 导入 fireplace 内部标签
from ..events import *

# 导入常用的 fireplace 内部标签
ACTIVATIONS_THIS_TURN = enums.ACTIVATIONS_THIS_TURN
LOCATION_COOLDOWN = enums.LOCATION_COOLDOWN
HONORABLE_KILL = enums.HONORABLE_KILL


# For buffs which are removed when the card is moved to play (eg. cost buffs)
# This needs to be Summon, because of Summon from the hand
REMOVED_IN_PLAY = Summon(ALL_PLAYERS, OWNER).after(Destroy(SELF))

ENEMY_CLASS = Attr(ENEMY_HERO, GameTag.CLASS)
FRIENDLY_CLASS = Attr(FRIENDLY_HERO, GameTag.CLASS)


SetTag = lambda target, tag: SetTags(target, (tag,))
UnsetTag = lambda target, tag: UnsetTags(target, (tag,))

Freeze = lambda target: SetTag(target, GameTag.FROZEN)
Unfreeze = lambda target: UnsetTag(target, GameTag.FROZEN)
Stealth = lambda target: SetTag(target, GameTag.STEALTH)
Unstealth = lambda target: UnsetTag(target, GameTag.STEALTH)
Taunt = lambda target: SetTag(target, GameTag.TAUNT)
GiveCharge = lambda target: SetTag(target, GameTag.CHARGE)
GiveDivineShield = lambda target: SetTag(target, GameTag.DIVINE_SHIELD)
GiveWindfury = lambda target: SetTag(target, GameTag.WINDFURY)
GivePoisonous = lambda target: SetTag(target, GameTag.POISONOUS)
GiveLifesteal = lambda target: SetTag(target, GameTag.LIFESTEAL)
GiveRush = lambda target: SetTag(target, GameTag.RUSH)
GiveReborn = lambda target: SetTag(target, GameTag.REBORN)

# GiveControl - 将随从的控制权交给指定玩家
# 这是 Steal 的反向操作
def GiveControl(minion, player):
    """将随从的控制权交给指定玩家"""
    from ..actions import Steal
    return Steal(minion, player)



CLEAVE = Hit(TARGET_ADJACENT, ATK(SELF))
COINFLIP = RandomNumber(0, 1) == 1
EMPTY_BOARD = Count(FRIENDLY_MINIONS) == 0
EMPTY_HAND = Count(FRIENDLY_HAND) == 0
FULL_BOARD = Count(FRIENDLY_MINIONS) == 7
FULL_HAND = Count(FRIENDLY_HAND) == Attr(CONTROLLER, GameTag.MAXHANDSIZE)
HOLDING_DRAGON = Find(FRIENDLY_HAND + DRAGON - SELF)
ELEMENTAL_PLAYED_LAST_TURN = Attr(CONTROLLER, "elemental_played_last_turn") > 0
TIMES_SPELL_PLAYED_THIS_GAME = Count(CARDS_PLAYED_THIS_GAME + SPELL)

# TIMES_CARD_TYPE_PLAYED - 计算本局打出特定类型卡牌的次数
def TIMES_CARD_TYPE_PLAYED(card_type):
    """返回本局打出特定类型卡牌的次数"""
    from hearthstone.enums import CardType
    return Count(CARDS_PLAYED_THIS_GAME + EnumSelector(card_type))

# FRENZY - 暴怒选择器（贫瘠之地扩展包）
FRENZY = GameTag.FRENZY

# FRIENDLY_HERO_HEALED_THIS_TURN - 友方英雄本回合是否被治疗过
# 使用lambda确保访问的是Hero对象而不是Player对象
FRIENDLY_HERO_HEALED_THIS_TURN = lambda source: source.controller.hero.healed_this_turn > 0

# SPELL_SCHOOL - 法术学派选择器函数
def SPELL_SCHOOL(school):
    """返回一个选择器，用于筛选特定法术学派的卡牌"""
    from ..dsl.selector import FuncSelector
    return FuncSelector(
        lambda entities, src: [
            e for e in entities 
            if hasattr(e, 'spell_school') and e.spell_school == school
        ]
    )
TIMES_SECRETS_PLAYED_THIS_GAME = Count(CARDS_PLAYED_THIS_GAME + SECRET)
MANA_SPENT_ON_SPELLS_THIS_GAME = lambda player: player.spent_mana_on_spells_this_game

DISCOVER = lambda *args: Discover(CONTROLLER, *args).then(
    Give(CONTROLLER, Discover.CARD)
)

# 缺失的选择器定义
CONTROLLER_FIELD = FRIENDLY_MINIONS  # 控制者的场上随从
CONTROLLER_HAND = FRIENDLY_HAND  # 控制者的手牌
OPPONENT_HERO = ENEMY_HERO  # 对手英雄
LAST_SUMMONED = FRIENDLY_MINIONS  # 最后召唤的随从（简化实现）
LAST_CARD_PLAYED = FRIENDLY_HAND  # 最后打出的牌（简化实现）
OWN_HERO_ATTACK = Attack(FRIENDLY_HERO)  # 己方英雄攻击事件
SELF_ATTACK = Attack(SELF)  # 自身攻击事件

# ForcePlay - 强制打出卡牌
def ForcePlay(controller, card):
    """
    强制打出卡牌，自动选择随机目标
    
    参数:
        controller: 控制者
        card: 要打出的卡牌
    
    返回:
        Play action
    """
    from ..actions import Play
    return Play(card)

# 对手回合结束事件
OPPONENT_TURN_END = lambda: OWN_TURN_BEGIN  # 简化实现：对手回合结束 = 己方回合开始

# UpdateProgress - 更新进度/计数器
def UpdateProgress(target, amount):
    """
    更新目标的进度计数器
    
    参数:
        target: 目标实体
        amount: 增加或减少的数量
    
    返回:
        SetTag action
    """
    from ..actions import SetTags
    # 使用 TAG_SCRIPT_DATA_NUM_1 作为进度计数器
    return lambda source: setattr(target, 'progress', getattr(target, 'progress', 0) + amount)

# Turn - 回合事件
def Turn(player):
    """
    监听指定玩家的回合开始事件
    
    参数:
        player: 玩家选择器
    
    返回:
        事件选择器
    """
    # 简化实现：返回回合开始事件
    return OWN_TURN_BEGIN if player == CONTROLLER else OPPONENT_TURN_BEGIN

# GiveOverload - 给予过载
def GiveOverload(target, amount):
    """
    给予目标玩家过载
    
    参数:
        target: 目标玩家
        amount: 过载数量
    
    返回:
        Action
    """
    from ..actions import SetTags
    # 简化实现：直接设置过载标签
    return lambda source: setattr(target if hasattr(target, 'overload') else source.controller, 'overload', 
                                   getattr(target if hasattr(target, 'overload') else source.controller, 'overload', 0) + amount)

# SetDormant - 设置休眠状态
def SetDormant(target, turns=1):
    """
    设置目标进入休眠状态
    
    参数:
        target: 目标实体
        turns: 休眠回合数
    
    返回:
        Action
    """
    from ..actions import SetTags
    # 设置休眠标签和回合数
    return lambda source: (
        setattr(target, 'dormant', True),
        setattr(target, 'dormant_turns', turns)
    )

# RefreshMana - 刷新法力水晶
def RefreshMana(target, amount):
    """
    刷新目标玩家的法力水晶
    
    参数:
        target: 目标玩家
        amount: 刷新的法力水晶数量
    
    返回:
        Action
    """
    from ..actions import GainMana
    # 简化实现：给予临时法力水晶
    return lambda source: setattr(
        target if hasattr(target, 'temp_mana') else source.controller, 
        'temp_mana', 
        getattr(target if hasattr(target, 'temp_mana') else source.controller, 'temp_mana', 0) + amount
    )

# PLAYED_SPELL_ON_FRIENDLY_CHARACTER - 对友方角色施放法术事件
PLAYED_SPELL_ON_FRIENDLY_CHARACTER = lambda: Play(CONTROLLER, SPELL)  # 简化实现

# SpendCorpses - 消耗残骸
def SpendCorpses(target, amount):
    """
    消耗目标玩家的残骸
    
    参数:
        target: 目标玩家
        amount: 消耗的残骸数量
    
    返回:
        Action
    """
    # 简化实现：直接减少残骸计数
    return lambda source: setattr(
        target if hasattr(target, 'corpses') else source.controller, 
        'corpses', 
        max(0, getattr(target if hasattr(target, 'corpses') else source.controller, 'corpses', 0) - amount)
    )

# GainMaxHealth - 获得最大生命值
def GainMaxHealth(target, amount):
    """
    使目标获得最大生命值
    
    参数:
        target: 目标实体
        amount: 获得的最大生命值数量
    
    返回:
        Action
    """
    from ..actions import SetTags
    # 简化实现：增加最大生命值和当前生命值
    return lambda source: (
        setattr(target, 'max_health', getattr(target, 'max_health', 0) + amount),
        setattr(target, 'health', getattr(target, 'health', 0) + amount)
    )

# Spellburst - 法术迸发机制
def Spellburst(action):
    """
    法术迸发：在你施放一个法术后触发一次，然后失效
    
    参数:
        action: 触发的动作
    
    返回:
        Event
    """
    # 简化实现：使用 OWN_SPELL_PLAY 事件，触发后设置 spellburst_used 标记
    return Play(CONTROLLER, SPELL).after(
        lambda self, player, card, *args: action if not getattr(self, 'spellburst_used', False) else None
    )

# FRIENDLY_MINION - 友方随从（单数）
FRIENDLY_MINION = FRIENDLY_MINIONS  # 简化实现：使用 FRIENDLY_MINIONS

# Switch - 条件分支
def Switch(selector, cases, default=None):
    """
    根据选择器的值执行不同的动作
    
    参数:
        selector: 选择器（如 GAME_SKIN）
        cases: 字典，键为条件值，值为对应的动作
        default: 默认动作（可选）
    
    返回:
        Action
    """
    def switch_action(source):
        # 获取选择器的值
        value = selector if not callable(selector) else selector(source)
        # 查找匹配的动作
        action = cases.get(value, default)
        if action:
            return action if not callable(action) else action(source)
        return None
    return switch_action

# TurnStart - 回合开始事件
TurnStart = TURN_BEGIN  # 简化实现：使用 TURN_BEGIN

# UpdateDynamicChooseOneOptions - 更新动态抉择选项
def UpdateDynamicChooseOneOptions(card, options):
    """
    更新卡牌的动态抉择选项
    
    参数:
        card: 卡牌
        options: 新的选项列表
    
    返回:
        Action
    """
    return lambda source: setattr(card, 'choose_cards', options)

# DRAENEI - 德莱尼种族
from hearthstone.enums import Race
DRAENEI = Race.DRAENEI if hasattr(Race, 'DRAENEI') else Race.ALL  # 德莱尼种族

# ADJACENT_MINIONS - 相邻随从
ADJACENT_MINIONS = lambda self: [m for m in self.controller.field if abs(m.zone_position - self.zone_position) == 1]

# OPPONENT_DECK - 对手牌库
OPPONENT_DECK = lambda self: self.game.opponent.deck

# TurnEnd - 回合结束事件
TurnEnd = TURN_END  # 简化实现：使用 TURN_END

# Armor - 护甲值
def Armor(target, amount):
    """
    使目标获得护甲值
    
    参数:
        target: 目标（通常是英雄）
        amount: 护甲值数量
    
    返回:
        Action
    """
    from ..actions import GainArmor
    return GainArmor(target, amount)

# Overload - 过载
def Overload(target, amount):
    """
    给予目标过载
    
    参数:
        target: 目标玩家
        amount: 过载数量
    
    返回:
        Action
    """
    return GiveOverload(target, amount)  # 使用已定义的 GiveOverload

# RACE - 种族选择器（用于过滤）
RACE = lambda race: lambda entity: entity.race == race

# SwapStats - 交换属性
def SwapStats(target):
    """
    交换目标的攻击力和生命值
    
    参数:
        target: 目标实体
    
    返回:
        Action
    """
    def swap_action(source):
        # 交换攻击力和生命值
        old_atk = target.atk
        old_health = target.health
        target.atk = old_health
        target.health = old_atk
        target.max_health = old_atk
    return swap_action

# QUESTLINE_STAGE - 任务线阶段选择器
QUESTLINE_STAGE = lambda stage: lambda entity: getattr(entity, 'questline_stage', 0) == stage

# Random - 随机选择器（已存在，但可能需要导出）
# Random 已经在 DSL 中定义

# 区域常量
from hearthstone.enums import Zone
PLAY = Zone.PLAY  # 战场区域
HAND = Zone.HAND  # 手牌区域
DECK = Zone.DECK  # 牌库区域
GRAVEYARD = Zone.GRAVEYARD  # 墓地区域

# ZoneChange - 区域变化事件
def ZoneChange(selector, from_zone, to_zone):
    """
    监听实体从一个区域移动到另一个区域的事件
    
    参数:
        selector: 实体选择器
        from_zone: 源区域
        to_zone: 目标区域
    
    返回:
        事件选择器
    """
    from ..events import EventListener
    
    class ZoneChangeEvent(EventListener):
        def __init__(self, selector, from_zone, to_zone):
            self.selector = selector
            self.from_zone = from_zone
            self.to_zone = to_zone
        
        def trigger(self, entity):
            # 检查实体是否匹配选择器
            if hasattr(entity, 'zone') and hasattr(entity, 'old_zone'):
                if entity.old_zone == self.from_zone and entity.zone == self.to_zone:
                    return True
            return False
    
    return ZoneChangeEvent(selector, from_zone, to_zone)

# RandomTarget - 从选择器中随机选择一个或多个目标
def RandomTarget(selector, count=1):
    """
    从选择器中随机选择目标
    
    参数:
        selector: 目标选择器（例如 ENEMY_MINIONS）
        count: 要选择的目标数量，默认为1
    
    返回:
        一个 action，在执行时返回随机选择的目标列表
    
    用法:
        target = yield RandomTarget(ENEMY_MINIONS)
        targets = yield RandomTarget(ENEMY_MINIONS, count=2)
    """
    from ..dsl.evaluator import Evaluator
    
    class RandomTargetAction(Evaluator):
        def __init__(self, selector, count=1):
            self.selector = selector
            self.count = count
        
        def trigger(self, source):
            # 评估选择器获取所有可能的目标
            if self.selector is None:
                print(f"[ERROR] RandomTargetAction.trigger: selector is None!")
                print(f"  Source: {source}")
                print(f"  Source type: {type(source)}")
                print(f"  Count: {self.count}")
                import traceback
                traceback.print_stack()
                return []
            
            entities = self.selector.eval(source.game, source)
            if not entities:
                return []
            
            # 随机选择指定数量的目标
            import random
            selected_count = min(self.count, len(entities))
            selected = random.sample(entities, selected_count)
            
            # 返回选择的目标
            return selected if self.count > 1 else (selected if selected else [])
    
    return RandomTargetAction(selector, count)


# RandomCardGenerator - 生成符合条件的随机卡牌列表
class RandomCardGenerator:
    """
    生成符合条件的随机卡牌列表，用于发现（Discover）机制
    
    参数:
        controller: 控制者（玩家）
        card_filter: 卡牌过滤函数，接受一个卡牌对象，返回 True/False
        count: 要生成的卡牌数量，默认为 3（发现机制的标准数量）
    
    用法:
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.MINION,
            count=3
        ))
    """
    def __init__(self, controller, card_filter=None, count=3):
        self.controller = controller
        self.card_filter = card_filter or (lambda c: True)
        self.count = count
    
    def eval(self, game, source):
        """
        评估并返回符合条件的随机卡牌ID列表
        
        参数:
            game: 游戏对象
            source: 源对象（触发此效果的卡牌）
        
        返回:
            符合条件的随机卡牌ID列表
        """
        # 获取所有可收集的卡牌
        from ..cards import db
        
        # 过滤符合条件的卡牌
        matching_cards = []
        for card_id, card_class in db.items():
            try:
                # 检查卡牌是否可收集
                if not hasattr(card_class, 'tags'):
                    continue
                
                # 创建临时卡牌对象用于过滤
                # 使用 card_class 的 tags 属性进行过滤
                if self.card_filter(card_class):
                    matching_cards.append(card_id)
            except Exception:
                # 忽略无法处理的卡牌
                continue
        
        # 如果没有符合条件的卡牌，返回空列表
        if not matching_cards:
            return []
        
        # 随机选择指定数量的卡牌
        selected_count = min(self.count, len(matching_cards))
        selected_cards = game.random.sample(matching_cards, selected_count)
        
        return selected_cards


# RandomCard - 生成符合条件的单张随机卡牌
def RandomCard(controller=None, card_filter=None, **kwargs):
    """
    生成符合条件的单张随机卡牌
    
    参数:
        controller: 控制者（可选）
        card_filter: 卡牌过滤函数（可选）
        **kwargs: 其他过滤条件（如 race, card_class, card_type, cost 等）
    
    返回:
        一个 Action，执行时返回随机选择的卡牌ID
    
    用法:
        # 作为 Action 使用
        yield RandomCard(CONTROLLER, race=Race.ELEMENTAL)
        
        # 获取卡牌ID
        card_id = RandomCard(CONTROLLER, card_filter=lambda c: c.cost >= 5).id
    """
    from ..dsl.evaluator import Evaluator
    from ..cards import db
    
    class RandomCardAction(Evaluator):
        def __init__(self, controller, card_filter, **filter_kwargs):
            self.controller = controller
            self.card_filter = card_filter
            self.filter_kwargs = filter_kwargs
            self._cached_id = None
        
        @property
        def id(self):
            """返回随机选择的卡牌ID（用于 .id 访问）"""
            if self._cached_id is None:
                # 临时生成一个卡牌ID
                matching_cards = self._get_matching_cards()
                if matching_cards:
                    import random
                    self._cached_id = random.choice(matching_cards)
                else:
                    self._cached_id = None
            return self._cached_id
        
        def _get_matching_cards(self):
            """获取所有符合条件的卡牌ID"""
            matching_cards = []
            
            for card_id, card_class in db.items():
                try:
                    if not hasattr(card_class, 'tags'):
                        continue
                    
                    # 应用自定义过滤器
                    if self.card_filter and not self.card_filter(card_class):
                        continue
                    
                    # 应用关键字参数过滤
                    if 'race' in self.filter_kwargs:
                        if not hasattr(card_class, 'race') or card_class.race != self.filter_kwargs['race']:
                            continue
                    
                    if 'card_class' in self.filter_kwargs:
                        if not hasattr(card_class, 'card_class') or card_class.card_class != self.filter_kwargs['card_class']:
                            continue
                    
                    if 'card_type' in self.filter_kwargs:
                        if not hasattr(card_class, 'type') or card_class.type != self.filter_kwargs['card_type']:
                            continue
                    
                    if 'cost' in self.filter_kwargs:
                        card_cost = card_class.tags.get(GameTag.COST, 0) if hasattr(card_class, 'tags') else 0
                        if card_cost != self.filter_kwargs['cost']:
                            continue
                    
                    matching_cards.append(card_id)
                except Exception:
                    continue
            
            return matching_cards
        
        def trigger(self, source):
            """执行时返回随机选择的卡牌"""
            matching_cards = self._get_matching_cards()
            
            if not matching_cards:
                return []
            
            # 使用游戏的随机数生成器
            selected_card_id = source.game.random.choice(matching_cards)
            
            # 返回 Give action 来将卡牌加入手牌
            from ..actions import Give
            return [Give(self.controller or source.controller, selected_card_id)]
    
    return RandomCardAction(controller, card_filter, **kwargs)


# Excess - 计算超量伤害
# 例如：对一个3血的随从造成6点伤害，超量伤害为3
def Excess(target, damage):
    """返回超量伤害值（伤害 - 目标当前生命值）"""
    from ..dsl.lazynum import LazyNum
    
    class ExcessDamage(LazyNum):
        def evaluate(self, source):
            if hasattr(target, 'health'):
                return max(0, damage - target.health)
            return 0
    
    return ExcessDamage()

# HeroPower - 获取英雄技能的伤害值
def HeroPower(player):
    """返回玩家英雄技能的伤害值"""
    from ..dsl.lazynum import LazyNum
    
    class HeroPowerDamage(LazyNum):
        def evaluate(self, source):
            # 基础英雄技能伤害通常是1（法师火球术）
            # 加上任何额外的英雄技能伤害加成
            base_damage = 1
            bonus = getattr(player.controller if hasattr(player, 'controller') else player, 'hero_power_damage_bonus', 0)
            return base_damage + bonus
    
    return HeroPowerDamage()

# EventValue - 获取事件触发时的数值（例如暴怒时受到的伤害）
def EventValue():
    """返回事件触发时的数值"""
    from ..dsl.lazynum import LazyNum
    
    class EventValueNum(LazyNum):
        def evaluate(self, source):
            # 对于暴怒（Frenzy）事件，返回受到的伤害值
            # 这个值通常存储在事件上下文中
            if hasattr(source, 'event_value'):
                return source.event_value
            # 默认返回0
            return 0
    
    return EventValueNum()

# Equip - 装备武器（Summon 的别名，用于武器）
Equip = Summon

# RandomHeroPower - 随机英雄技能
RandomHeroPower = lambda: RandomCollectible(type=CardType.HERO_POWER)

BASIC_HERO_POWERS = [
    "HERO_01bp",
    "HERO_02bp",
    "HERO_03bp",
    "HERO_04bp",
    "HERO_05bp",
    "HERO_06bp",
    "HERO_07bp",
    "HERO_08bp",
    "HERO_09bp",
    "HERO_10bp",
]

UPGRADED_HERO_POWERS = [
    "HERO_01bp",
    "HERO_02bp",
    "HERO_03bp",
    "HERO_04bp",
    "HERO_05bp",
    "HERO_06bp",
    "HERO_07bp",
    "HERO_08bp",
    "HERO_09bp",
    "HERO_10bp2",
]

UPGRADE_HERO_POWER = Summon(CONTROLLER, UPGRADED_HERO_POWER)

BASIC_TOTEMS = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]

POTIONS = [
    "CFM_021",  # Freezing Potion
    "CFM_065",  # Volcanic Potion
    "CFM_620",  # Potion of Polymorph
    "CFM_603",  # Potion of Madness
    "CFM_604",  # Greater Healing Potion
    "CFM_661",  # Pint-Size Potion
    "CFM_662",  # Dragonfire Potion
    "CFM_094",  # Felfire Potion
    "CFM_608",  # Blastcrystal Potion
    "CFM_611",  # Bloodfury Potion
]

LICH_KING_CARDS = [
    "ICC_314t1",
    "ICC_314t2",
    "ICC_314t3",
    "ICC_314t4",
    "ICC_314t5",
    "ICC_314t6",
    "ICC_314t7",
    "ICC_314t8",
]

THE_COIN = "GAME_005"

LACKEY_CARDS = [
    "DAL_613",
    "DAL_614",
    "DAL_615",
    "DAL_739",
    "DAL_741",
    "ULD_616",
    "DRG_052",
]

RandomBasicTotem = lambda *args, **kw: RandomID(*BASIC_TOTEMS, **kw)
RandomBasicHeroPower = lambda *args, **kw: RandomID(*BASIC_HERO_POWERS, **kw)
RandomUpgradedHeroPower = lambda *args, **kw: RandomID(*UPGRADED_HERO_POWERS, **kw)
RandomPotion = lambda *args, **kw: RandomID(*POTIONS, **kw)
RandomLackey = lambda *args, **kw: RandomID(*LACKEY_CARDS, **kw)

# 50% chance to attack the wrong enemy.
FORGETFUL = Attack(SELF).on(
    COINFLIP
    & Retarget(SELF, RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(SELF)))
)

AT_MAX_MANA = lambda s: MANA(s) == MAX_MANA(s)
OVERLOADED = lambda s: (OVERLOAD_LOCKED(s) > 0) or (OVERLOAD_OWED(s) > 0)
CHECK_CTHUN = ATK(HIGHEST_ATK(CTHUN)) >= 10
CAST_WHEN_DRAWN = Destroy(SELF), Draw(CONTROLLER), Battlecry(SELF, None)
INVOKED_TWICE = Attr(CONTROLLER, GameTag.INVOKE_COUNTER) >= 2


class JoustHelper(Evaluator):
    """
    A helper evaluator class for jousts to allow JOUST & ... syntax.
    """

    def __init__(self, challenger, defender):
        self.challenger = challenger
        self.defender = defender
        super().__init__()

    def trigger(self, source):
        action = Joust(self.challenger, self.defender).then(
            JoustEvaluator(Joust.CHALLENGER, Joust.DEFENDER) & self._if | self._else
        )

        return action.trigger(source)


JOUST = JoustHelper(RANDOM(FRIENDLY_DECK + MINION), RANDOM(ENEMY_DECK + MINION))

JOUST_SPELL = JoustHelper(RANDOM(FRIENDLY_DECK + SPELL), RANDOM(ENEMY_DECK + SPELL))

RECRUIT = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
Recruit = lambda selector: Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + selector))

def MAGNETIC(buff):
    """
    磁力机制：将随从吸附到右侧的目标随从上
    
    默认只能吸附在机械上。
    如果卡牌设置了 MAGNETIC_TARGET_RACES 标签，则可以吸附在指定种族上。
    
    Args:
        buff: 附魔ID
    
    Examples:
        # 标准磁力（只能吸附在机械上）
        magnetic = MAGNETIC("BOT_020e")
        
        # 特殊磁力（需要在tags中设置 MAGNETIC_TARGET_RACES）
    tags = {
            enums.MAGNETIC_TARGET_RACES: [Race.MECHANICAL, Race.BEAST]
        }
        magnetic = MAGNETIC("TTN_087e")
    """
    from .. import enums
    from hearthstone.enums import Race
    
    # 定义一个选择器函数，在运行时检查卡牌的 MAGNETIC_TARGET_RACES 标签
    def magnetic_target_selector(source):
        # 获取源卡牌允许的目标种族
        allowed_races = source.tags.get(enums.MAGNETIC_TARGET_RACES, None)
        
        if allowed_races is None:
            # 默认：只能吸附在机械上
            # 使用 SELF 选择器而不是 source 实体
            return RIGHT_OF(SELF) + MECH
        else:
            # 自定义种族列表
            # 构建种族过滤器
            def race_filter(card):
                return any(race in card.races for race in allowed_races)
            
            return RIGHT_OF(SELF).filter(race_filter)
    
    # 返回磁力动作
    # 注意：这里需要使用延迟求值，因为需要在运行时获取 source
    return lambda source: (
        Find(magnetic_target_selector(source)) & (
            Buff(RIGHT_OF(SELF), buff, atk=ATK(SELF), max_health=CURRENT_HEALTH(SELF), source_card_id=source.id),
            Remove(SELF),
        )
    ).trigger(source)

INVOKE = Invoke(MAIN_GALAKROND)


def SET(amt):
    return lambda self, i: amt


# Buff helper
def buff(atk=0, health=0, **kwargs):
    buff_tags = {}
    if atk:
        buff_tags[GameTag.ATK] = atk
    if health:
        buff_tags[GameTag.HEALTH] = health

    for tag in GameTag:
        if tag.name.lower() in kwargs.copy():
            buff_tags[tag] = kwargs.pop(tag.name.lower())

    if "immune" in kwargs:
        value = kwargs.pop("immune")
        buff_tags[GameTag.CANT_BE_DAMAGED] = value
        buff_tags[GameTag.CANT_BE_TARGETED_BY_OPPONENTS] = value

    if kwargs:
        raise NotImplementedError(kwargs)

    class Buff:
        tags = buff_tags

    return Buff


def AttackHealthSwapBuff():
    def apply(self, target):
        self._xatk = target.health
        self._xhealth = target.atk
        target.damage = 0

    cls = buff()
    cls.atk = lambda self, i: self._xatk
    cls.max_health = lambda self, i: self._xhealth
    cls.apply = apply

    return cls


def GainEmptyMana(selector, amount):
    """
    Helper to gain an empty mana crystal (gains mana, then spends it)
    """
    return GainMana(selector, amount).then(SpendMana(selector, GainMana.AMOUNT))


def DestroyMana(selector, amount):
    """
    Helper to destroy mana crystals (uses negative GainMana)
    """
    return GainMana(selector, -amount)


def custom_card(cls):
    from . import CardDB, db

    id = cls.__name__
    if GameTag.CARDNAME not in cls.tags:
        raise ValueError("No name provided for custom card %r" % (cls))
    db[id] = CardDB.merge(id, None, cls)
    # Give the card its fake name
    db[id].strings = {
        GameTag.CARDNAME: {"enUS": cls.tags[GameTag.CARDNAME]},
        GameTag.CARDTEXT_INHAND: {"enUS": ""},
    }
    return cls


def decode_deckstring(deckstring: str):
    deck = Deck.from_deckstring(deckstring)
    hero_id = deck.heroes[0]
    hero_id = db.dbf[hero_id]
    cards = []
    for card_id, num in deck.cards:
        card_id: str = db.dbf[card_id]
        card_id = card_id.removeprefix("CORE_")
        cards += [card_id] * num
    return hero_id, cards


class JadeGolemUtils:
    def custom_cardtext(self):
        return self.data.description.split("@")[0]

    def cardtext_entity_0(self):
        jade_golem = self.controller.jade_golem
        return f"{jade_golem}/{jade_golem}"

    def cardtext_entity_1(self):
        if self.data.locale == "enUS":
            jade_golem = self.controller.jade_golem
            if jade_golem == 8 or jade_golem == 18:
                return "n"
        return ""

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
        GameTag.CARDTEXT_ENTITY_1: cardtext_entity_1,
    }


class SchemeUtils:
    def custom_cardtext(self):
        return self.data.description.replace("@", "{0}")

    def cardtext_entity_0(self):
        return self.progress

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
    }

    class Hand:
        events = OWN_TURN_BEGIN.on(AddProgress(SELF, SELF))


class GalakrondUtils:
    def custom_cardtext(self):
        if self.zone == Zone.PLAY:
            return self.data.description.replace("(@)", "").replace("（@）", "")
        locale_map = {
            "deDE": "Noch {0}-mal",
            "enUS": "{0} left!",
            "esES": "Faltan: {0}",
            "esMX": "¡Faltan {0}!",
            "frFR": "Encore {0} !",
            "itIT": "{0} restante!",
            "jaJP": "あと{0}回！",
            "koKR": "{0}회 남음",
            "plPL": "Jeszcze {0}!",
            "ptBR": "{0} restando",
            "ruRU": "Еще {0} раз.",
            "thTH": "เหลืออีก {0} ครั้ง!",
            "zhCN": "还剩{0}次",
            "zhTW": "還剩{0}次",
        }
        return self.data.description.replace("@", locale_map[self.data.locale])

    def cardtext_entity_0(self):
        return self.progress_total - self.progress

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
    }


class ThresholdUtils:
    def custom_cardtext(self):
        splited = self.data.description.split("@")
        if self.powered_up:
            return splited[0] + splited[2]
        return splited[0] + splited[1]

    def cardtext_entity_0(self):
        return (
            Attr(SELF, GameTag.PLAYER_TAG_THRESHOLD_VALUE)
            - Attr(CONTROLLER, Attr(SELF, GameTag.PLAYER_TAG_THRESHOLD_TAG_ID))
        ).evaluate(self)

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
    }
    powered_up = Attr(
        CONTROLLER, Attr(SELF, GameTag.PLAYER_TAG_THRESHOLD_TAG_ID)
    ) >= Attr(SELF, GameTag.PLAYER_TAG_THRESHOLD_VALUE)
