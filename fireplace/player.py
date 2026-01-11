from .i18n import _ as translate
from itertools import chain
from typing import TYPE_CHECKING

from hearthstone.enums import CardType, GameTag, PlayState, Race, Zone

from .actions import Concede, Draw, Fatigue, Give, Hit, SpendMana, Steal, Summon
from .aura import TargetableByAuras
from .card import Card
from .deck import Deck
from .entity import Entity, slot_property
from .managers import PlayerManager
from .utils import CardList


if TYPE_CHECKING:
    from .card import (
        Character,
        Hero,
        Minion,
        PlayableCard,
        Quest,
        Secret,
        SideQuest,
        HeroPower,
    )
    from .game import Game


class Player(Entity, TargetableByAuras):
    Manager = PlayerManager
    all_targets_random = slot_property("all_targets_random")
    # excavate_tier 改为普通属性，在 __init__ 中初始化
    # times_excavated 改为普通属性，在 __init__ 中初始化
    cant_overload = slot_property("cant_overload")
    choose_both = slot_property("choose_both")
    extra_battlecries = slot_property("extra_battlecries")
    extra_trigger_secret = slot_property("extra_trigger_secret")
    minion_extra_battlecries = slot_property("minion_extra_battlecries")
    minion_extra_combos = slot_property("minion_extra_combos")
    extra_deathrattles = slot_property("extra_deathrattles")
    extra_end_turn_effect = slot_property("extra_end_turn_effect")
    healing_double = slot_property("healing_double", sum)
    hero_power_double = slot_property("hero_power_double", sum)
    healing_as_damage = slot_property("healing_as_damage")
    shadowform = slot_property("shadowform")
    spellpower_double = slot_property("spellpower_double", sum)
    spellpower_adjustment = slot_property("spellpower", sum)
    heropower_damage_adjustment = slot_property("heropower_damage", sum)
    spells_cost_health = slot_property("spells_cost_health")
    murlocs_cost_health = slot_property("murlocs_cost_health")
    minions_cost_health = slot_property("minions_cost_health")
    type = CardType.PLAYER

    def __init__(self, name, deck: list[str], hero: str, is_standard=True):
        self.game: Game = None
        self.opponent: Player = None
        self.first_player: bool = False
        self.starting_deck = deck
        self.starting_hero = hero
        self.data = None
        self.name = name
        self.hero: Hero = None
        self.hero_power: HeroPower = None
        self.is_standard = is_standard
        super().__init__()
        self.deck = Deck()
        self.hand = CardList["PlayableCard"]()
        self.field = CardList["Minion"]()
        self.graveyard = CardList["PlayableCard"]()
        self.secrets = CardList["Secret | Quest | SideQuest"]()
        self.locations = CardList()  # 地标区域
        self.choice = None
        self.max_hand_size = 10
        self.max_resources = 10
        self.max_deck_size = 60
        self.cant_draw = False
        self.cant_fatigue = False
        self.combo = False
        self.fatigue_counter = 0
        self.last_card_played = None
        self.last_played_spell = None
        self.overloaded = 0
        self.overload_locked = 0
        self.overloaded_this_game = 0
        self._max_mana = 0
        self._start_hand_size = 3
        self.playstate = PlayState.INVALID
        self.temp_mana = 0
        self.timeout = 75
        self.times_hero_power_used_this_game = 0
        self.used_mana = 0
        self.minions_killed_this_turn = 0
        self.minions_killed_this_game = 0  # 本局对战中死亡的随从数量
        self.minions_played_this_turn = 0
        self.beasts_summoned_this_game = 0  # 本局对战中召唤的野兽数量
        self.non_rogue_cards_added_to_hand = 0  # 本局对战中加入手牌的非潜行者职业牌数量
        self.weapon = None
        self.zone = Zone.INVALID
        self.turn = None
        self.last_turn = None
        self.jade_golem = 1
        self.times_totem_summoned_this_game = 0
        self.elemental_played_this_turn = 0
        self.elemental_played_last_turn = 0
        self.elemental_streak = 0  # 连续回合使用元素牌的次数（用于WW_424等卡牌）
        self.spells_played_this_turn = 0  # 本回合施放的法术数量（用于DEEP_010等卡牌）
        self.spells_played_last_turn = 0  # 上回合施放的法术数量（用于DEEP_010等卡牌）
        self.cards_drawn_this_turn = 0
        self.cards_drawn_this_game = 0  # 本局游戏抽牌总数（用于TOY_530游乐巨人等卡牌）
        self.cards_played_this_turn = 0
        self.cards_played_this_game = CardList()
        self.hero_power_damage_this_game = 0
        self.spent_mana_on_spells_this_game = 0
        self.healed_this_game = 0
        self.cthun = None
        self.invoke_counter = 0
        
        # 挖掘机制 - 决战荒芜之地（2023年11月）
        self.excavate_tier = 0  # 当前挖掘层级（0-4）
        self.times_excavated = 0  # 本局对战中挖掘的次数
        
        # 追踪最后一个战吼效果（用于"重复战吼"类卡牌）
        self.last_battlecry = None  # (card, target) 元组

        # 追踪本局游戏施放过的法术学派（用�?多系施法�?等卡牌）
        self.spell_schools_played_this_game = set()  # 使用 set 自动去重
        
        # 追踪本回合施放过的法术学派（用于MIS_709圣光荧光棒等卡牌�? 威兹班的工坊�?024�?月）
        self.spell_schools_played_this_turn = []  # 使用 list 保留顺序和重�?

        # 追踪本局游戏施放过的法术费用（用于TOY_378星空投影球等卡牌�? 威兹班的工坊�?024�?月）
        self.spell_costs_played_this_game = set()  # 使用 set 自动去重

        # 追踪上回合之后是否有友方亡灵死亡（用于RLK_116等卡牌）
        self.undead_died_last_turn = False
        self.undead_died_last_turn_list = []  # 存储上回合之后死亡的友方亡灵

        # 追踪本局游戏英雄攻击次数（用于RLK_825等卡牌）
        self.hero_attacks_this_game = 0

        # 英雄技能伤害加成（用于"瞄准射击"等卡牌）
        self.hero_power_damage_bonus = 0
        
        # 追踪每回合施放的法术（用�?首席法师安东尼达�?等卡牌）
        self.spells_by_turn = {}  # {turn_number: [spells]}
        
        # 追踪上一个对友方随从施放的法术（用于"金翼鹦鹉"等卡牌）
        self.last_spell_on_friendly_minion = None
        
        # 追踪上一个战吼随从（用于"艳丽的金刚鹦�?等卡牌）
        self.last_battlecry = None
        
        # 追踪本回合受到的伤害（用�?暗影之刃飞刀�?等卡牌）
        self.damage_taken_this_turn = 0
        
        # 追踪在自己回合受到的伤害（本局游戏累计,用于TTN_462被禁锢的恐魔等卡牌）
        self.damage_taken_on_own_turn_this_game = 0
        
        # 追踪本回合对敌方英雄造成的伤害（用于"邪恶的厨�?等卡牌）
        self.hero_damage_this_turn = 0
        
        # 追踪英雄在己方回合受到伤害的次数（用于VAC_418桑拿常客等卡牌）- 胜地历险记（2024�?月）
        self.hero_damage_count_on_own_turn = 0

        # 待对手猜测的发现队列（用�?可疑的炼金师"等卡牌）
        # 每个元素: {"options": [card1, card2, card3], "chosen": card_id}
        self.pending_guesses = []
        
        # 追踪最后的抉择法术（用�?开路�?等卡牌）
        self.last_choose_one_card = None
        self.last_choose_one_choice = None

        # 追踪本局游戏施放的冰霜法术数量（用于"熊人格拉希尔"等卡牌）
        self.frost_spells_cast = 0
        
        # 追踪下一张卡的费用减少（用于"锯齿骨刺"等卡牌）
        # 格式: int，表示减少的费用
        self.next_card_cost_reduction = 0
        
        # 追踪本局游戏召唤的图腾数量（用于"图腾巨像"等卡牌）
        self.totems_summoned_this_game = 0
        
        # 追踪本回合死亡的随从数量（用�?暗影华尔�?等卡牌）
        self.minions_killed_this_turn = 0
        
        # 追踪上一个暗影法术（用于"暗脉女勋�?等卡牌）
        self.last_shadow_spell = None
        
        # 残骸系统（死亡骑士专属资源）- 巫妖王的进军�?022�?2月）
        self.corpses = 0  # 当前残骸数量
        self.total_corpses_spent = 0  # 本局对战中累积消耗的残骸总数（用于ETC_210通灵最强音等卡牌）


        # 追踪本局游戏使用过的流放牌数量（用于RLK_213等卡牌）
        self.outcast_cards_played_this_game = 0

        # 追踪本局游戏施放的套牌之外的法术（用于RLK_803等卡牌）
        self.spells_cast_not_from_deck = []  # 存储施放过的套牌外法术的ID

        # 追踪本局游戏使用的套牌之外的随从（用于TTN_481莱登等卡牌）
        self.minions_played_from_outside_deck = []  # 存储使用过的套牌外随从的ID

        # 下一份药剂减费机制（用于RLK_570食尸鬼炼金师等卡牌）
        self.next_potion_cost_zero = False  # 标记下一份药剂费用为0
        
        # 追踪本回合获得的护甲值和攻击力（用于"ETC_386 佐克·雾鼻"等卡牌）
        self.armor_gained_this_turn = 0
        self.attack_gained_this_turn = 0
        
        # 追踪本局对战中获得的护甲总量（用于"AV_145 加尔范上尉"等卡牌）- 奥特兰克的决裂（2021年12月）
        self.armor_gained_this_game = 0

        # 追踪本局对战洗入对手牌库瘟疫
        self.plagues_shuffled_into_enemy = 0

        # 追踪本局对战锻造的卡牌数量（用于TTN_751伊格尼斯等卡牌）- 泰坦诸神�?023�?月）
        self.forged_cards_this_game = 0

        # 追踪本局对战召唤的土灵数量（用于TTN_900石心之王等卡牌）- 泰坦诸神�?023�?月）
        self.earthen_summoned_this_game = 0

        # 追踪上回合使用的卡牌（用于WW_053飞车劫掠等卡牌）- 决战荒芜之地�?023�?1月）
        self.cards_played_last_turn = []  # 存储上回合使用的卡牌ID列表
        self.cards_played_this_turn_ids = []  # 临时存储本回合使用的卡牌ID

        # 追踪本局对战中触发过的奥秘（用于MIS_914量产泰迪等卡牌）- 威兹班的工坊�?024�?月）
        self.triggered_secrets = []  # 存储触发过的奥秘ID列表

        # 追踪使用的威兹班实验套牌类型（用于实现特殊套牌机制）- 威兹班的工坊�?024�?月）
        # 可能的�? None, "DECK_OF_WONDERS", "NONUPLET_DECK", "SHRUNKEN_DECK" �?
        self.whizbang_deck_type = None

        # 追踪本局游戏使用地标的次数（用于VAC_439海滨巨人等卡牌）- 胜地历险记（2024�?月）
        self.locations_used_this_game = 0

        # 追踪本局游戏对角色施放的法术数量（用于VAC_558海上船歌等卡牌）- 胜地历险记（2024�?月）
        self.spells_cast_on_characters_this_game = 0

        # 追踪使用过的另一职业卡牌（用于VAC_700横夺硬抢等卡牌）- 胜地历险记（2024�?月）
        self.cards_played_from_other_class_count = 0  # 使用过的另一职业卡牌数量

        # 星舰机制 - 深暗领域�?024�?1月）
        self.starship_in_progress = None  # 当前正在构筑的星舰实�?
        self.starships_launched_this_game = 0  # 本局对战中发射的星舰数量
        self.starship_pieces_died_this_game = []  # 本局对战中死亡的星舰组件列表
        self.last_card_played_from_other_class = None  # 上一张使用的另一职业卡牌

        # 手牌位置追踪 - 深暗领域�?024�?1月）
        # 用于 GDB_475 近轨血月等需要检测相邻卡牌的卡牌
        self.cards_played_this_turn_with_position = []  # [(card, hand_position), ...]
        
        # 残骸支付机制 - 深暗领域�?024�?1月）
        # 用于 GDB_470 大主教玛拉达�?
        self.next_card_costs_corpses = False  # 标记下一张牌是否消耗残骸而非法力�?

        # Discover追踪机制 - 深暗领域�?024�?1月）
        # 用于 GDB_237 接触异星生物（本局发现次数减费）和 GDB_843 视差光枪（本回合发现�?2攻）
        self.cards_discovered_this_game = 0  # 本局对战中发现的卡牌数量
        self.cards_discovered_this_turn = 0  # 本回合发现的卡牌数量

        # 星灵法术追踪机制 - 深暗领域�?024�?1月）
        # 用于 SC_758 巨像（本局施放的星灵法术数量提升效果）
        self.protoss_spells_cast_this_game = 0  # 本局对战中施放的星灵法术数量

        # 卡牌摧毁追踪 - 深暗领域�?024�?1月）
        # 用于 GDB_142 无界空宇（每次抽�?打牌/摧毁牌减费）
        self.cards_destroyed_this_game = 0  # 本局对战中摧毁的卡牌数量

        # 随从打出追踪 - 深暗领域�?024�?1月）
        # 用于 GDB_131 维伦（触发本局所有德莱尼的战吼和亡语�?
        self.minions_played_this_game = []  # 本局对战中打出的随从ID列表

        # 基尔加丹恶魔传送门 - 深暗领域�?024�?1月）
        # 用于 GDB_145 基尔加丹（无尽恶魔传送门机制�?
        self.kiljaeden_portal_active = False  # 是否激活基尔加丹传送门
        self.kiljaeden_portal_buff_stacks = 0  # 传送门buff层数（每回合+1，恶魔获�?2/+2�?

        # 阿塔尼斯神族减费 - 深暗领域�?024�?1月）
        # 用于 SC_754 阿塔尼斯（神族随从本局减少2费）
        self.artanis_protoss_discount = False  # 是否拥有阿塔尼斯的神族减费效�?

        # 星舰发射历史 - 深暗领域�?024�?1月）
        # 用于 SC_400 吉姆·雷诺（重新发射所有星舰）
        # 存储每次发射的星舰的完整快照：{id, accumulated_atk, accumulated_health, keywords, pieces}

        # 套牌外恶魔追踪 - 深暗领域（2024年11月）
        self.demons_not_started_in_deck_played = []  # 本局对战中使用过的套牌外恶魔ID列表

        # 套牌外卡牌追踪 - 失落之城（2025年7月）
        # 用于 DINO_409 科技恐龙等卡牌
        self.cards_not_started_in_deck_played = []  # 本局对战中使用过的所有套牌外卡牌ID列表


        # 本回合伤害追踪 - 深暗领域（2024年11月）
        self.damage_taken_this_turn = 0  # 本回合英雄受到的伤害总量

        # 友方随从死亡追踪 - 深入翡翠梦境（2025年3月）
        self.friendly_minions_died_this_game = 0  # 本局对战中死亡的友方随从数量（用于EDR_941星涌术、EDR_430艾森娜等卡牌）
        self.minions_died_this_turn = []  # 本回合死亡的友方随从列表（用于EDR_491荆棘大德鲁伊等卡牌）

        # Imbue 机制 - 深入翡翠梦境（2025年3月）
        self.imbue_level = 0  # 当前 Imbue 等级（0=未激活，1=初始，2+=升级）
        self.original_hero_power = None  # 保存原始英雄技能（用于恢复）
        self.imbued_hero_power_id = None  # 当前 Imbued 英雄技能的ID

        # 任务追踪 - 失落之城（2025年7月）
        # 用于 TLC_987 任务助理等卡牌
        self.quest_played = False  # 本局对战中是否打出过任务牌

        # Kindred 双倍触发机制 - 失落之城（2025年7月）
        # 用于 TLC_251 蛮鱼挑战者等卡牌
        self.kindred_double_trigger = False  # 下一个延系效果是否触发两次

        # 洗牌追踪机制 - 失落之城（2025年7月）
        # 用于 TLC_517 一脚踢飞、TLC_520 灌林追踪者等卡牌
        self.cards_shuffled_into_deck = 0  # 本局对战中洗入牌库的卡牌次数

        # 对敌法术追踪 - 胜地历险记（2024年7月）
        # 用于 VAC_407 话痨鹦鹉等卡牌
        self.last_spell_cast_at_enemy = None  # 最后一张对敌人施放的法术（卡牌对象）

        # 弃牌追踪 - Return to Naxxramas (重返纳克萨玛斯) - 2023年2月
        # 用于 NX2_017 瘟疫爆发等卡牌
        self.has_discarded_this_game = False  # 本局对战中是否弃过牌








    def dump(self):
        data = super().dump()
        # data["name"], data["avatar"] = self.name
        if self.hero:
            data["hero"] = self.hero.dump()
            if self.hero.power:
                data["heropower"] = self.hero.power.dump()
        if self.weapon:
            data["weapon"] = self.weapon.dump()
        data["deck"] = len(self.deck)
        data["fatigue_counter"] = self.fatigue_counter
        data["hand"] = [card.dump() for card in self.hand]
        data["field"] = [card.dump() for card in self.field]
        data["secrets"] = [card.dump() for card in self.secrets]
        data["locations"] = [card.dump() for card in self.locations]
        if self.choice:
            choice = data["choice"] = {}
            choice["cards"] = [card.dump() for card in self.choice.cards]
            choice["max_count"] = self.choice.max_count
            choice["min_count"] = self.choice.min_count
        data["max_mana"] = self.max_mana
        data["mana"] = self.mana
        data["timeout"] = self.timeout
        data["playstate"] = int(self.playstate)
        return data

    def dump_hidden(self):
        data = super().dump()
        # data["name"], data["avatar"] = self.name
        if self.hero:
            data["hero"] = self.hero.dump()
            if self.hero.power:
                data["heropower"] = self.hero.power.dump()
        if self.weapon:
            data["weapon"] = self.weapon.dump()
        data["deck"] = len(self.deck)
        data["fatigue_counter"] = self.fatigue_counter
        data["hand"] = [card.dump_hidden() for card in self.hand]
        data["field"] = [card.dump() for card in self.field]
        data["secrets"] = [card.dump_hidden() for card in self.secrets]
        data["locations"] = [card.dump() for card in self.locations]  # 地标对双方可�?
        if self.choice:
            choice = data["choice"] = {}
            choice["cards"] = [card.dump_hidden() for card in self.choice.cards]
            choice["max_count"] = self.choice.max_count
            choice["min_count"] = self.choice.min_count
        data["max_mana"] = self.max_mana
        data["mana"] = self.mana
        data["timeout"] = self.timeout
        data["playstate"] = int(self.playstate)
        return data

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(name=%r, hero=%r)" % (self.__class__.__name__, self.name, self.hero)

    @property
    def current_player(self):
        return self.game.current_player is self

    @property
    def controller(self):
        return self

    @property
    def mana(self):
        mana = (
            max(0, self.max_mana - self.used_mana - self.overload_locked)
            + self.temp_mana
        )
        return mana

    @property
    def max_mana(self):
        return self._max_mana

    @max_mana.setter
    def max_mana(self, amount):
        old_max_mana = self._max_mana
        self._max_mana = min(self.max_resources, max(0, amount))
        self.log(translate("player_mana_crystals", player=self, count=self._max_mana))
        
        # 等级法术自动升级机制
        # 当玩家的最大法力水晶增加时，检查并升级手牌和牌库中的等级法�?
        if self._max_mana > old_max_mana and self.game:
            self._upgrade_ranked_spells()

    @property
    def heropower_damage(self):
        aura_power = self.controller.heropower_damage_adjustment
        minion_power = sum(
            minion.heropower_damage for minion in self.field.filter(dormant=False)
        )
        return aura_power + minion_power

    @property
    def spellpower(self):
        aura_power = self.controller.spellpower_adjustment
        minion_power = sum(
            minion.spellpower for minion in self.field.filter(dormant=False)
        )
        return aura_power + minion_power

    @property
    def start_hand_size(self):
        if not self.first_player:
            # Give the second player an extra card
            return self._start_hand_size + 1
        return self._start_hand_size

    @property
    def characters(self):
        return CardList(chain([self.hero] if self.hero else [], self.field))

    @property
    def entities(self):
        for entity in self.field:
            yield from entity.entities
        yield from self.secrets
        yield from self.locations  # 包含地标
        yield from self.buffs
        if self.hero:
            yield from self.hero.entities
        yield self

    @property
    def live_entities(self):
        yield from self.field
        yield from self.locations  # 包含地标
        if self.hero:
            yield self.hero
        if self.weapon:
            yield self.weapon

    @property
    def actionable_entities(self):
        yield from self.characters
        yield from self.hand
        if self.hero.power:
            yield self.hero.power

    @property
    def minion_slots(self):
        return max(0, self.game.MAX_MINIONS_ON_FIELD - len(self.field))

    def copy_cthun_buff(self, card):
        for buff in self.cthun.buffs:
            buff.source.buff(
                card,
                buff.id,
                atk=buff.atk,
                max_health=buff.max_health,
                taunt=getattr(buff, "taunt", False),
            )

    def card(self, id, source=None, parent=None, zone=Zone.SETASIDE):
        card = Card(id)
        card.controller = self
        card.zone = zone
        if source is not None:
            card.creator = source
        if parent is not None:
            card.parent_card = parent

        # 标记卡牌是否起始于套牌（用于GDB_121恶兆邪火、GDB_128阿克蒙德等卡牌）
        # 如果是从牌库区域创建，标记为起始套牌卡牌
        card.started_in_deck = (zone == Zone.DECK)

        # C'THUN
        if self.cthun and id == self.cthun.id:
            self.copy_cthun_buff(card)
        self.game.manager.new_entity(card)
        return card

    def prepare_for_game(self):
        # Whizbang the Wonderful (原版威兹�?
        if self.starting_hero == "BOT_914h" or self.starting_deck == ["BOT_914"]:
            from .cards.boomsday.whizbang_decks import WHIZBANG_DECKS

            self.starting_hero, self.starting_deck = self.game.random.choice(
                WHIZBANG_DECKS
            )

        # Zayle, Shadow Cloak (暗影斗篷扎伊�?
        if self.starting_hero == "DAL_800h" or self.starting_deck == ["DAL_800"]:
            from .cards.dalaran.zayle_decks import ZAYLE_DECKS

            self.starting_hero, self.starting_deck = self.game.random.choice(
                ZAYLE_DECKS
            )

        # Splendiferous Whizbang (酷炫的威兹班) - 威兹班的工坊 (2024�?�?
        # 当套牌中只有 TOY_700 �?随机选择一个实验套�?
        if self.starting_deck == ["TOY_700"]:
            from .cards.whizbang.whizbang_experimental_decks import WHIZBANG_EXPERIMENTAL_DECKS

            # 随机选择一个实验套�?
            # 返回格式: (英雄ID, 卡牌ID列表, 套牌类型)
            selected_deck = self.game.random.choice(WHIZBANG_EXPERIMENTAL_DECKS)
            self.starting_hero, self.starting_deck, self.whizbang_deck_type = selected_deck

        self.summon(self.starting_hero)
        # self.game.trigger(self, [Summon(self, self.starting_hero)], event_args=None)
        self.starting_hero = self.hero
        for id in self.starting_deck:
            card = self.card(id, zone=Zone.DECK)
            if self.is_standard and not card.is_standard:
                self.is_standard = False
        self.starting_deck = CardList(self.deck[:])
        self.shuffle_deck()
        self.cthun = self.card("OG_280")
        self.playstate = PlayState.PLAYING

        # Draw initial hand (but not any more than what we have in the deck)
        hand_size = min(len(self.deck), self.start_hand_size)
        # Quest cards are automatically included in the player's mulligan as
        # the left-most card
        quests = []
        exclude_quests = []
        for card in self.deck:
            if card.data.quest:
                quests.append(card)
            else:
                exclude_quests.append(card)
        
        # 确保不会尝试抽取超过可用卡牌数量的牌
        non_quest_cards_needed = max(0, min(hand_size - len(quests), len(exclude_quests)))
        
        self.starting_hand = CardList["PlayableCard"](
            quests + self.game.random.sample(exclude_quests, non_quest_cards_needed)
        )
        # It's faster to move cards directly to the hand instead of drawing
        for card in self.starting_hand:
            card.zone = Zone.HAND

    def get_spell_damage(self, amount: int) -> int:
        """
        Returns the amount of damage \a amount will do, taking
        SPELLPOWER and SPELLPOWER_DOUBLE into account.
        """
        amount += self.spellpower
        amount <<= self.controller.spellpower_double
        return amount

    def get_spell_heal(self, amount: int) -> int:
        """
        Returns the amount of heal \a amount will do, taking
        SPELLPOWER and SPELLPOWER_DOUBLE into account.
        """
        amount <<= self.controller.healing_double
        return amount

    def get_heropower_damage(self, amount: int) -> int:
        amount += self.heropower_damage
        amount <<= self.controller.hero_power_double
        return amount

    def get_heropower_heal(self, amount: int) -> int:
        amount <<= self.controller.hero_power_double
        return amount

    @property
    def num_spells_played_this_game(self):
        return len([card for card in self.cards_played_this_game if card.type == CardType.SPELL])

    def discard_hand(self):
        self.log("%r discards their entire hand!", self)
        # iterate the list in reverse so we don't skip over cards in the process
        # yes it's stupid.
        for card in self.hand[::-1]:
            card.discard()

    def can_pay_cost(self, card):
        """
        Returns whether the player can pay the resource cost of a card.
        """
        # 添加详细的类型检查和错误日志
        if not hasattr(card, 'type'):
            import sys
            import traceback
            error_msg = (
                f"\n{'='*80}\n"
                f"TYPE ACCESS ERROR in can_pay_cost\n"
                f"{'='*80}\n"
                f"Card object: {card}\n"
                f"  Type: {type(card)}\n"
                f"  Class: {card.__class__.__name__}\n"
                f"  Has 'type' attr: {hasattr(card, 'type')}\n"
                f"  Dir: {[a for a in dir(card) if not a.startswith('_')]}\n"
                f"Player: {self}\n"
                f"Stacktrace:\n"
            )
            print(error_msg, file=sys.stderr)
            traceback.print_stack(file=sys.stderr)
            print(f"{'='*80}\n", file=sys.stderr)
            raise AttributeError(f"Object {card} (type: {type(card)}) has no attribute 'type'")
        
        if self.spells_cost_health and card.type == CardType.SPELL:
            return self.hero.health > card.cost
        if self.murlocs_cost_health:
            if card.type == CardType.MINION and Race.MURLOC in card.races:
                return self.hero.health > card.cost
        if self.minions_cost_health:
            if card.type == CardType.MINION:
                return self.hero.health > card.cost
        return self.mana >= card.cost

    def pay_cost(self, source: Entity, amount: int) -> int:
        """
        Make player pay \a amount mana.
        Returns how much mana is spent, after temporary mana adjustments.
        """
        if self.spells_cost_health and source.type == CardType.SPELL:
            self.log("%s spells cost %i health", self, amount)
            self.game.queue_actions(self, [Hit(self.hero, amount)])
            return amount
        if self.murlocs_cost_health:
            if source.type == CardType.MINION and Race.MURLOC in source.races:
                self.log("%s murlocs cost %i health", self, amount)
                self.game.queue_actions(self, [Hit(self.hero, amount)])
                return amount
        if self.minions_cost_health:
            if source.type == CardType.MINION:
                self.log("%s minions cost %i health", self, amount)
                self.game.queue_actions(self, [Hit(self.hero, amount)])
                return amount
        if source.type == CardType.SPELL:
            self.spent_mana_on_spells_this_game += amount
        self.game.queue_actions(source, [SpendMana(self, amount)])
        return amount

    def shuffle_deck(self):
        self.log(translate("player_shuffles_deck", player=self))
        self.game.random.shuffle(self.deck)

    def draw(self, count=1):
        if self.cant_draw:
            self.log("%s tries to draw %i cards, but can't draw", self, count)
            return None

        ret = self.game.cheat_action(self, [Draw(self) * count])[0]
        if count == 1:
            if not ret[0]:  # fatigue
                return None
            return ret[0][0]
        return ret

    def give(self, id: str) -> "PlayableCard":
        cards = self.game.cheat_action(self, [Give(self, id)])[0][0]
        if len(cards) > 0:
            return cards[0]

    def concede(self):
        ret = self.game.cheat_action(self, [Concede(self)])
        return ret

    def fatigue(self):
        return self.game.cheat_action(self, [Fatigue(self)])[0]

    def steal(self, card):
        return self.game.cheat_action(self, [Steal(card)])

    def summon(self, card) -> "PlayableCard":
        """
        Puts \a card in the PLAY zone
        """
        if isinstance(card, str):
            card = self.card(card)
        self.game.cheat_action(self, [Summon(self, card)])
        return card

    def _upgrade_ranked_spells(self):
        """
        等级法术自动升级机制
        
        当玩家的最大法力水晶增加时，自动升级手牌和牌库中的等级法术�?
        检查卡牌的 RANKED_SPELL_NEXT_RANK �?RANKED_SPELL_THRESHOLD 标签�?
        如果当前法力水晶达到阈值，则将卡牌变形为下一等级�?
        """
        from . import enums
        from .actions import Morph
        
        # 检查并升级手牌中的等级法术
        for card in list(self.hand):
            self._try_upgrade_ranked_spell(card)
        
        # 检查并升级牌库中的等级法术
        for card in list(self.deck):
            self._try_upgrade_ranked_spell(card)
    
    def _try_upgrade_ranked_spell(self, card):
        """
        尝试升级单张等级法术卡牌
        
        Args:
            card: 要检查的卡牌
        """
        from . import enums
        from .actions import Morph
        
        # 检查卡牌是否有等级法术标签
        next_rank = card.tags.get(enums.RANKED_SPELL_NEXT_RANK)
        threshold = card.tags.get(enums.RANKED_SPELL_THRESHOLD)
        
        # 如果卡牌有下一等级且达到了升级阈值，则升�?
        if next_rank and threshold and self._max_mana >= threshold:
            self.log("%s upgrades %s to %s (reached %d mana)", 
                    self, card, next_rank, threshold)
            # 使用 Morph 将卡牌变形为下一等级
            self.game.queue_actions(self, [Morph(card, next_rank)])

