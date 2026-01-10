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
FRIENDLY_HERO_HEALED_THIS_TURN = Attr(FRIENDLY_HERO, "healed_this_turn") > 0

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
            return RIGHT_OF(source) + MECH
        else:
            # 自定义种族列表
            # 构建种族过滤器
            def race_filter(card):
                return any(race in card.races for race in allowed_races)
            
            return RIGHT_OF(source).filter(race_filter)
    
    # 返回磁力动作
    # 注意：这里需要使用延迟求值，因为需要在运行时获取 source
    return lambda source: (
        Find(magnetic_target_selector(source)) & (
            Buff(RIGHT_OF(source), buff, atk=ATK(source), max_health=CURRENT_HEALTH(source), source_card_id=source.id),
            Remove(source),
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
