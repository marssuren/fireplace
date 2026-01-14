from __future__ import annotations

import os.path
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List, TypeVar, overload
from xml.etree import ElementTree

from hearthstone.enums import CardClass, CardType

from .logging import log
from .entity import Entity


# Autogenerate the list of cardset modules
_cards_module = os.path.join(os.path.dirname(__file__), "cards")
CARD_SETS = [cs for _, cs, ispkg in iter_modules([_cards_module]) if ispkg]
T = TypeVar("T")


class CardList(list[T], Entity):
    def __contains__(self, x: T) -> bool:
        for item in self:
            if x is item:
                return True
        return False

    @overload
    def __getitem__(self, index: int) -> T:
        pass

    @overload
    def __getitem__(self, index: slice) -> CardList[T]:
        pass

    def __getitem__(self, key):
        ret = super().__getitem__(key)
        if isinstance(key, slice):
            return self.__class__(ret)
        return ret

    def __int__(self) -> int:
        # Used in Kettle to easily serialize CardList to json
        return len(self)

    def contains(self, x: T | str) -> bool:
        """
        True if list contains any instance of x
        """
        for item in self:
            if x == item:
                return True
        return False

    def index(self, x: T) -> int:
        for i, item in enumerate(self):
            if x is item:
                return i
        raise ValueError

    def remove(self, x: T):
        for i, item in enumerate(self):
            if x is item:
                del self[i]
                return
        raise ValueError

    def exclude(self, *args, **kwargs):
        if args:
            return self.__class__(e for e in self for arg in args if e is not arg)
        else:
            return self.__class__(
                e for k, v in kwargs.items() for e in self if getattr(e, k) != v
            )

    def filter(self, **kwargs):
        def conditional(e, k, v):
            p = getattr(e, k, 0)
            if hasattr(p, "__iter__"):
                return v in p
            return p == v

        return self.__class__(
            e for k, v in kwargs.items() for e in self if conditional(e, k, v)
        )


def random_draft(card_class: CardClass, exclude=[], include=[], game=None, max_cards=None, expansions=None):
    """
    Return a deck of random cards for the \a card_class
    
    Args:
        card_class: 职业
        exclude: 排除的卡牌ID列表
        include: 必须包含的卡牌ID列表
        game: 游戏对象(用于随机数生成)
        max_cards: 套牌上限,None表示包含所有可收集卡牌(测试模式)
        expansions: 扩展包列表,None表示所有扩展包,[]表示仅基本卡
    """
    import random
    from . import cards
    from .deck import Deck

    deck = list(include)
    collection = []

    for card in cards.db.keys():
        if card in exclude:
            continue
        cls = cards.db[card]
        if not cls.collectible:
            continue
        if cls.type == CardType.HERO:
            # Heroes are collectible...
            continue
        if cls.card_class and cls.card_class not in [card_class, CardClass.NEUTRAL]:
            continue
        
        # 扩展包过滤
        if expansions is not None:
            # 获取卡牌的扩展包信息
            card_set = getattr(cls, 'card_set', None)
            if card_set is None:
                # 没有扩展包信息,跳过
                continue
            if expansions and card_set not in expansions:
                # 不在指定的扩展包列表中
                continue
        
        collection.append(cls)

    # 测试模式:添加所有可收集卡牌
    if max_cards is None:
        for card_cls in collection:
            # 每张卡添加最大允许数量
            for _ in range(card_cls.max_count_in_deck):
                deck.append(card_cls.id)
        return deck
    
    # 正常模式:限制为 max_cards 张
    while len(deck) < max_cards:
        if game:
            card = game.random.choice(collection)
        else:
            card = random.choice(collection)
        if deck.count(card.id) < card.max_count_in_deck:
            deck.append(card.id)

    return deck


def random_class(game=None):
    if game:
        return CardClass(game.random.randint(2, 10))
    import random

    return CardClass(random.randint(2, 10))


def entity_to_xml(entity):
    e = ElementTree.Element("Entity")
    for tag, value in entity.tags.items():
        if value and not isinstance(value, str):
            te = ElementTree.Element("Tag")
            te.attrib["enumID"] = str(int(tag))
            te.attrib["value"] = str(int(value))
            e.append(te)
    return e


def game_state_to_xml(game):
    tree = ElementTree.Element("HSGameState")
    tree.append(entity_to_xml(game))
    for player in game.players:
        tree.append(entity_to_xml(player))
    for entity in game:
        if entity.type in (CardType.GAME, CardType.PLAYER):
            # Serialized those above
            continue
        e = entity_to_xml(entity)
        e.attrib["CardID"] = entity.id
        tree.append(e)

    return ElementTree.tostring(tree)


def weighted_card_choice(source, weights: List[int], card_sets: List[str], count: int):
    """
    Take a list of weights and a list of card pools and produce
    a random weighted sample without replacement.
    len(weights) == len(card_sets) (one weight per card set)
    """

    chosen_cards = []

    # sum all the weights
    cum_weights = []
    totalweight = 0
    for i, w in enumerate(weights):
        totalweight += w * len(card_sets[i])
        cum_weights.append(totalweight)

    if totalweight == 0:
        return []

    # for each card
    for i in range(count):
        # choose a set according to weighting
        chosen_set = bisect(cum_weights, source.game.random.random() * totalweight)
        
        # bisect可能返回len(cum_weights)，需要限制在有效范围内
        chosen_set = min(chosen_set, len(card_sets) - 1)
        
        # 检查选中的集合是否为空
        if not card_sets[chosen_set]:
            # 如果选中的集合为空，跳过这次选择
            continue

        # choose a random card from that set
        chosen_card_index = source.game.random.randint(
            0, len(card_sets[chosen_set]) - 1
        )

        chosen_cards.append(card_sets[chosen_set].pop(chosen_card_index))
        totalweight -= weights[chosen_set]
        cum_weights[chosen_set:] = [
            x - weights[chosen_set] for x in cum_weights[chosen_set:]
        ]

    # 将选中的卡牌转换为卡牌对象
    # 处理不同类型的输入：字符串ID、卡牌对象、列表等
    result = []
    for card in chosen_cards:
        if card is None:
            continue
        # 如果已经是卡牌对象，直接使用
        if hasattr(card, 'id') and hasattr(card, 'controller'):
            result.append(card)
        # 如果是字符串ID，创建新卡牌
        elif isinstance(card, str):
            result.append(source.controller.card(card, source=source))
        # 如果是列表（错误情况），尝试从列表中提取
        elif isinstance(card, list):
            for item in card:
                if hasattr(item, 'id') and hasattr(item, 'controller'):
                    result.append(item)
                elif isinstance(item, str):
                    result.append(source.controller.card(item, source=source))
        else:
            # 尝试将其作为ID处理
            try:
                result.append(source.controller.card(str(card), source=source))
            except Exception:
                log.warning(f"weighted_card_choice: Unable to process card: {card} (type: {type(card)})")
    
    return result


def setup_game(test_mode=False, expansions='random'):
    """
    创建游戏
    
    Args:
        test_mode: 测试模式,True时套牌包含所有可收集卡牌(用于测试fireplace引擎)
        expansions: 扩展包设置
            - None: 所有扩展包
            - 'random': 随机选择一个扩展包(每个玩家独立随机)
            - 'random_same': 随机选择一个扩展包(两个玩家使用相同扩展包)
            - [CardSet.XXX, ...]: 指定扩展包列表
    """
    from .game import Game
    from .player import Player
    import random as py_random

    card_class1 = random_class()
    card_class2 = random_class()
    
    # 处理扩展包参数
    expansion_list1 = None
    expansion_list2 = None
    
    if expansions == 'random':
        # 每个玩家随机选择一个扩展包
        from hearthstone.enums import CardSet
        available_sets = [
            CardSet.CORE, CardSet.EXPERT1,  # 基本+经典
            CardSet.NAXX, CardSet.GVG,  # 2014
            CardSet.BRM, CardSet.TGT, CardSet.LOE,  # 2015
            CardSet.OG, CardSet.KARA, CardSet.GANGS,  # 2016
            CardSet.UNGORO, CardSet.ICECROWN, CardSet.LOOTAPALOOZA,  # 2017
            CardSet.GILNEAS, CardSet.BOOMSDAY, CardSet.TROLL,  # 2018
            CardSet.DALARAN, CardSet.ULDUM, CardSet.DRAGONS,  # 2019
            CardSet.BLACK_TEMPLE, CardSet.SCHOLOMANCE, CardSet.DARKMOON_FAIRE,  # 2020
            CardSet.THE_BARRENS, CardSet.STORMWIND, CardSet.ALTERAC_VALLEY,  # 2021
            CardSet.THE_SUNKEN_CITY, CardSet.REVENDRETH, CardSet.RETURN_OF_THE_LICH_KING,  # 2022
            CardSet.BATTLE_OF_THE_BANDS, CardSet.TITANS, CardSet.WILD_WEST,  # 2023
            CardSet.WHIZBANGS_WORKSHOP, CardSet.ISLAND_VACATION, CardSet.SPACE,  # 2024
            CardSet.EMERALD_DREAM, CardSet.THE_LOST_CITY, CardSet.TIME_TRAVEL,  # 2025
        ]
        expansion_list1 = [py_random.choice(available_sets)]
        expansion_list2 = [py_random.choice(available_sets)]
    elif expansions == 'random_same':
        # 两个玩家使用相同的随机扩展包
        from hearthstone.enums import CardSet
        available_sets = [
            CardSet.CORE, CardSet.EXPERT1,
            CardSet.NAXX, CardSet.GVG,
            CardSet.BRM, CardSet.TGT, CardSet.LOE,
            CardSet.OG, CardSet.KARA, CardSet.GANGS,
            CardSet.UNGORO, CardSet.ICECROWN, CardSet.LOOTAPALOOZA,
            CardSet.GILNEAS, CardSet.BOOMSDAY, CardSet.TROLL,
            CardSet.DALARAN, CardSet.ULDUM, CardSet.DRAGONS,
            CardSet.BLACK_TEMPLE, CardSet.SCHOLOMANCE, CardSet.DARKMOON_FAIRE,
            CardSet.THE_BARRENS, CardSet.STORMWIND, CardSet.ALTERAC_VALLEY,
            CardSet.THE_SUNKEN_CITY, CardSet.REVENDRETH, CardSet.RETURN_OF_THE_LICH_KING,
            CardSet.BATTLE_OF_THE_BANDS, CardSet.TITANS, CardSet.WILD_WEST,
            CardSet.WHIZBANGS_WORKSHOP, CardSet.ISLAND_VACATION, CardSet.SPACE,
            CardSet.EMERALD_DREAM, CardSet.THE_LOST_CITY, CardSet.TIME_TRAVEL,
        ]
        chosen_set = py_random.choice(available_sets)
        expansion_list1 = [chosen_set]
        expansion_list2 = [chosen_set]
    elif isinstance(expansions, list):
        # 使用指定的扩展包列表
        expansion_list1 = expansions
        expansion_list2 = expansions
    # else: expansions is None, use all expansions
    
    # 测试模式:无限制套牌
    max_cards = None if test_mode else 30
    deck1 = random_draft(card_class1, max_cards=max_cards, expansions=expansion_list1)
    deck2 = random_draft(card_class2, max_cards=max_cards, expansions=expansion_list2)
    
    if test_mode:
        exp_info1 = f"扩展包:{expansion_list1[0].name}" if expansion_list1 else "全部扩展包"
        exp_info2 = f"扩展包:{expansion_list2[0].name}" if expansion_list2 else "全部扩展包"
        print(f"[测试模式] {card_class1.name} vs {card_class2.name}")
        print(f"  P1套牌: {len(deck1)} 张卡 ({exp_info1})")
        print(f"  P2套牌: {len(deck2)} 张卡 ({exp_info2})")
    
    player1 = Player("Player1", deck1, card_class1.default_hero)
    player2 = Player("Player2", deck2, card_class2.default_hero)

    game = Game(players=(player1, player2))

    return game


def play_turn(game):
    player = game.current_player

    while True:
        while player.choice:
            choice = game.random.choice(player.choice.cards)
            log.info("Choosing card %r" % (choice))
            player.choice.choose(choice)

        heropower = player.hero.power
        if heropower.is_usable() and game.random.random() < 0.1:
            choose = None
            target = None
            if heropower.must_choose_one:
                choose = game.random.choice(heropower.choose_cards)
            if heropower.requires_target():
                target = game.random.choice(heropower.targets)
            heropower.use(target=target, choose=choose)
            continue

        # eg. Deathstalker Rexxar
        while player.choice:
            choice = game.random.choice(player.choice.cards)
            log.info("Choosing card %r" % (choice))
            player.choice.choose(choice)

        # iterate over our hand and play whatever is playable
        for card in player.hand:
            if card.is_playable() and game.random.random() < 0.5:
                target = None
                if card.must_choose_one:
                    card = game.random.choice(card.choose_cards)
                    if not card.is_playable():
                        continue
                log.info("Playing %r" % card)
                if card.requires_target():
                    target = game.random.choice(card.targets)
                log.info("Target on %r" % target)
                card.play(target=target)

                while player.choice:
                    choice = game.random.choice(player.choice.cards)
                    log.info("Choosing card %r" % (choice))
                    player.choice.choose(choice)

                continue

        # Randomly attack with whatever can attack
        for character in player.characters:
            if character.can_attack():
                character.attack(game.random.choice(character.targets))
                # eg. Vicious Fledgling
                while player.choice:
                    choice = game.random.choice(player.choice.cards)
                    log.info("Choosing card %r" % (choice))
                    player.choice.choose(choice)

        break

    game.end_turn()
    return game


def play_full_game():
    game = setup_game()

    for player in game.players:
        log.info("Can mulligan %r" % (player.choice.cards))
        mull_count = game.random.randint(0, len(player.choice.cards))
        cards_to_mulligan = game.random.sample(player.choice.cards, mull_count)
        player.choice.choose(*cards_to_mulligan)

    while True:
        play_turn(game)

    return game
