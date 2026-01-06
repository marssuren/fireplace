from collections import OrderedDict

from hearthstone.enums import (
    BlockType,
    CardClass,
    CardType,
    GameTag,
    Mulligan,
    PlayState,
    Race,
    SpellSchool,
    Step,
    Zone,
)

from .dsl import LazyNum, LazyValue, Selector
from .dsl.copy import Copy, RebornCopy
from .dsl.random_picker import RandomMinion
from .dsl.selector import SELF
from .entity import Entity
from .enums import DISCARDED
from .exceptions import InvalidAction
from .logging import log, log_info
from .i18n import _ as translate
from .utils import random_class
from . import cards


def _eval_card(source, card):
    """
    Return a Card instance from \a card
    The card argument can be:
    - A Card instance (nothing is done)
    - The string ID of the card (the card is created)
    - A LazyValue (the card is dynamically created)
    - A Selector (take entity lists and returns a sub-list)
    """
    if isinstance(card, LazyValue):
        card = card.evaluate(source)

    if isinstance(card, Action):
        card = card.trigger(source)[0]

    if isinstance(card, Selector):
        card = card.eval(source.game, source)

    if not isinstance(card, list):
        cards = [card]
    else:
        cards = card

    ret = []
    for card in cards:
        if isinstance(card, str):
            ret.append(source.controller.card(card, source))
        else:
            ret.append(card)

    return ret


class EventListener:
    ON = 1
    AFTER = 2

    def __init__(self, trigger, actions, at):
        self.trigger = trigger
        self.actions = actions
        self.at = at
        self.once = False

    def __repr__(self):
        return "<EventListener %r>" % (self.trigger)


class ActionMeta(type):
    def __new__(metacls, name, bases, namespace):
        cls = type.__new__(metacls, name, bases, dict(namespace))
        argslist = []
        for k, v in namespace.items():
            if not isinstance(v, ActionArg):
                continue
            v._setup(len(argslist), k, cls)
            argslist.append(v)
        cls.ARGS = tuple(argslist)
        return cls

    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()


class ActionArg(LazyValue):
    def _setup(self, index, name, owner):
        self.index = index
        self.name = name
        self.owner = owner

    def __repr__(self):
        return "<%s.%s>" % (self.owner.__name__, self.name)

    def evaluate(self, source):
        # This is used when an event listener triggers and the callback
        # Action has arguments of the type Action.FOO
        # XXX we rely on source.event_args to be set, but it's very racey.
        # If multiple events happen on an entity at once, stuff will go wrong.
        assert source.event_args
        return source.event_args[self.index]


class CardArg(ActionArg):
    # Type hint
    pass


class IntArg(ActionArg, LazyNum):
    def evaluate(self, source):
        ret = super().evaluate(source)
        return self.num(ret)


class BoolArg(ActionArg):
    """Boolean argument for actions"""
    def __init__(self, default=False):
        self.default = default
    
    def evaluate(self, source):
        ret = super().evaluate(source)
        return bool(ret) if ret is not None else self.default



class Action(metaclass=ActionMeta):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.callback = ()
        self.times = 1
        self.event_queue = []
        self.choice_callback = []

    def __repr__(self):
        args = ["%s=%r" % (k, v) for k, v in zip(self.ARGS, self._args)]
        return "<Action: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

    def after(self, *actions):
        return EventListener(self, actions, EventListener.AFTER)

    def on(self, *actions):
        return EventListener(self, actions, EventListener.ON)

    def then(self, *args):
        """
        Create a callback containing an action queue, called upon the
        action's trigger with the action's arguments available.
        """
        ret = self.__class__(*self._args, **self._kwargs)
        ret.callback = args
        ret.times = self.times
        return ret

    def _broadcast(self, entity, source, at, *args):
        for event in entity.events:
            if event.at != at:
                continue
            if isinstance(event.trigger, self.__class__) and event.trigger.matches(
                entity, source, args
            ):
                log_info("trigger_off", entity=entity, trigger=self, source=source)
                entity.trigger_event(source, event, args)
                if (
                    entity.type == CardType.SPELL
                    and entity.data.secret
                    and entity.controller.extra_trigger_secret
                ):
                    entity.trigger_event(source, event, args)

    def broadcast(self, source, at, *args):
        source.game.action_start(BlockType.TRIGGER, source, 0, None)

        for entity in source.game.entities:
            self._broadcast(entity, source, at, *args)
        for hand in source.game.hands:
            for entity in hand.entities:
                self._broadcast(entity, source, at, *args)
        for deck in source.game.decks:
            for entity in deck.entities:
                self._broadcast(entity, source, at, *args)

        source.game.action_end(BlockType.TRIGGER, source)

    def queue_broadcast(self, obj, args):
        self.event_queue.append((obj, args))

    def resolve_broadcasts(self):
        for obj, args in self.event_queue:
            obj.broadcast(*args)
        self.event_queue = []

    def get_args(self, source):
        return self._args

    def matches(self, entity, source, args):
        for arg, match in zip(args, self._args):
            if match is None:
                # Allow matching Action(None, None, z) to Action(x, y, z)
                continue
            if arg is None:
                # We got an arg of None and a match not None. Bad.
                return False
            if callable(match):
                res = match(arg)
                if not res:
                    return False
            else:
                # this stuff is stupidslow
                res = match.eval([arg], entity)
                if not res or res[0] is not arg:
                    return False
        if hasattr(self, "source") and self.source:
            res = self.source.eval([source], entity)
            if not res or res[0] is not source:
                return False
        return True

    def trigger_choice_callback(self):
        callbacks = self.choice_callback
        self.choice_callback = []
        for callback in callbacks:
            callback()


class GameAction(Action):
    def trigger(self, source):
        args = self.get_args(source)
        self.do(source, *args)


class Attack(GameAction):
    """
    Make \a ATTACKER attack \a DEFENDER
    """

    ATTACKER = ActionArg()
    DEFENDER = ActionArg()

    def get_args(self, source):
        attackers = _eval_card(source, self._args[0])
        attacker = attackers[0] if attackers else None
        defenders = _eval_card(source, self._args[1])
        defender = defenders[0] if defenders else None
        return attacker, defender

    def do(self, source, attacker, defender):
        log_info("attacks", attacker=attacker, defender=defender)
        if not attacker or not defender:
            return
        attacker.attack_target = defender
        defender.defending = True
        source.game.proposed_attacker = attacker
        source.game.proposed_defender = defender
        source.game.manager.step(Step.MAIN_COMBAT, Step.MAIN_ACTION)
        source.game.refresh_auras()  # XXX Needed for Gorehowl
        source.game.manager.game_action(self, source, attacker, defender)
        self.broadcast(source, EventListener.ON, attacker, defender)

        defender = source.game.proposed_defender
        source.game.proposed_attacker = None
        source.game.proposed_defender = None
        if attacker.should_exit_combat:
            log_info("attack_interrupted")
            attacker.attack_target = None
            defender.defending = False
            return

        assert attacker is not defender, "Why are you hitting yourself %r?" % (attacker)

        # Save the attacker/defender atk values in case they change during the attack
        # (eg. in case of Enrage)
        def_atk = defender.atk
        attacker_atk = attacker.atk
        
        # 检查是否有溢出伤害效果（用于虫外有虫等）
        from . import enums
        has_excess_damage = attacker.tags.get(enums.EXCESS_DAMAGE_TO_HERO, False)
        
        if has_excess_damage and defender.type == CardType.MINION:
            # 计算溢出伤害
            defender_health = defender.health
            if attacker_atk > defender_health:
                # 先对目标造成伤害
                source.game.queue_actions(attacker, [Hit(defender, attacker_atk)])
                # 溢出部分伤害命中敌方英雄
                excess_damage = attacker_atk - defender_health
                source.game.queue_actions(attacker, [Hit(defender.controller.hero, excess_damage)])
            else:
                # 没有溢出，正常伤害
                source.game.queue_actions(attacker, [Hit(defender, attacker_atk)])
        else:
            # 正常攻击逻辑
            source.game.queue_actions(attacker, [Hit(defender, attacker_atk)])
        
        if def_atk:
            source.game.queue_actions(defender, [Hit(attacker, def_atk)])

        self.broadcast(source, EventListener.AFTER, attacker, defender)

        # 追踪英雄攻击次数（用于RLK_825等卡牌）
        if attacker.type == CardType.HERO:
            attacker.controller.hero_attacks_this_game += 1

        attacker.attack_target = None
        defender.defending = False
        if source == attacker:
            attacker.num_attacks += 1


class BeginTurn(GameAction):
    """
    Make \a player begin the turn
    """

    PLAYER = ActionArg()

    def do(self, source, player):
        source.manager.step(source.next_step, Step.MAIN_READY)
        source.turn += 1
        source.log(translate("player_begins_turn", player=player, turn=source.turn))
        source.current_player = player
        source.manager.step(source.next_step, Step.MAIN_START_TRIGGERS)
        source.manager.step(source.next_step, source.next_step)
        source.game.manager.game_action(self, source, player)
        self.broadcast(source, EventListener.ON, player)

        # 处理对手的待猜测发现（用于"可疑的炼金师"等卡牌）
        opponent = player.opponent
        if opponent and hasattr(opponent, 'pending_guesses') and opponent.pending_guesses:
            for guess_data in opponent.pending_guesses:
                # 对手从相同的选项中猜测
                options = guess_data["options"]
                chosen_id = guess_data["chosen"]

                # 对手AI进行猜测（通过choice机制）
                guess_id = player.choice(options) if hasattr(player, 'choice') and callable(player.choice) else None

                # 如果猜中，对手获得一张复制
                if guess_id == chosen_id:
                    from .dsl.lazynum import Copy
                    Give(player, Copy(chosen_id)).trigger(source)

            # 清空队列
            opponent.pending_guesses.clear()

        # 重置"上回合之后友方亡灵是否死亡"标记
        player.undead_died_last_turn = False
        player.undead_died_last_turn_list = []  # 清空上回合死亡的亡灵列表

        # 重置本回合获得的护甲值和攻击力（用于 Etc_386 等卡牌）
        player.armor_gained_this_turn = 0
        player.attack_gained_this_turn = 0

        source._begin_turn(player)


class Concede(GameAction):
    """
    Make \a player concede
    """

    PLAYER = ActionArg()

    def do(self, source, player):
        player.playstate = PlayState.CONCEDED
        source.game.manager.game_action(self, source, player)
        source.game.check_for_end_game()


class Disconnect(GameAction):
    """
    Make \a player disconnect
    """

    PLAYER = ActionArg()

    def do(self, source, player):
        player.playstate = PlayState.DISCONNECTED
        source.game.manager.game_action(self, source, player)


class Deaths(GameAction):
    """
    Process all deaths in the PLAY Zone.
    """

    def do(self, source, *args):
        source.game.process_deaths()


class Death(GameAction):
    """
    Move target to the GRAVEYARD Zone.
    """

    ENTITY = ActionArg()

    def _broadcast(self, entity, source, at, *args):
        # https://github.com/jleclanche/fireplace/issues/126
        target = args[0]
        if (not self._trigger) and entity.play_counter > target.play_counter:
            self._trigger = True
            if at == EventListener.ON and target.has_deathrattle:
                source.game.queue_actions(target, [Deathrattle(target)])
            if (
                at == EventListener.AFTER
                and target.type == CardType.MINION
                and target.reborn
            ):
                source.game.queue_actions(
                    target, [Summon(target.controller, RebornCopy(SELF))]
                )
        return super()._broadcast(entity, source, at, *args)

    def do(self, source, cards):
        for card in cards:
            if not card.dead:
                continue
            if card.zone == Zone.PLAY:
                card._dead_position = card.zone_position - 1
            card.zone = Zone.GRAVEYARD
            source.game.check_for_end_game()
            source.game.refresh_auras()
            log_info("processing_deathrattle", card=card)
            self._trigger = False
            source.game.manager.game_action(self, source, card)
            self.broadcast(source, EventListener.ON, card)

            # INFUSE 机制：友方随从死亡时，为手牌中的 Infuse 卡牌充能
            if card.type == CardType.MINION and card.controller:
                # 追踪友方亡灵死亡（用于RLK_116等卡牌）
                if hasattr(card, 'race') and Race.UNDEAD in card.races:
                    card.controller.undead_died_last_turn = True
                    # 添加到死亡亡灵列表（用于RLK_832等卡牌）
                    card.controller.undead_died_last_turn_list.append(card)

                # 为手牌中的 Infuse 卡充能
                for hand_card in card.controller.hand:
                    if hasattr(hand_card, 'infuse_threshold') and hand_card.infuse_threshold > 0:
                        # 检查是否有种族限制（infuse_race属性）
                        infuse_race = getattr(hand_card, 'infuse_race', None)

                        # 如果有种族限制，检查死亡随从是否匹配
                        if infuse_race is not None and card.race != infuse_race:
                            continue  # 跳过不匹配的随从

                        # 增加充能计数
                        if not hasattr(hand_card, 'infuse_counter'):
                            hand_card.infuse_counter = 0
                        hand_card.infuse_counter += 1
                        
                        # 追踪死亡随从的信息（用于 REV_843 等卡牌）
                        if not hasattr(hand_card, 'infused_minions'):
                            hand_card.infused_minions = []
                        hand_card.infused_minions.append({
                            'atk': card.atk,
                            'health': card.health,
                            'id': card.id,
                            'race': card.race
                        })

                        # 检查是否达到充能阈值
                        if hand_card.infuse_counter >= hand_card.infuse_threshold:
                            # 触发 infuse 效果
                            if hasattr(hand_card, 'infuse'):
                                # 检查是否为无尽注能（如德纳修斯大帝）
                                # 无尽注能不锁定计数器，可以继续充能
                                if not getattr(hand_card, 'endless_infuse', False):
                                    hand_card.infuse_counter = hand_card.infuse_threshold  # 锁定计数器
                                # 触发 infuse 效果（通过 trigger 方法）
                                if callable(hand_card.infuse):
                                    hand_card.infuse()
                
                # 牌库注能机制（MAW_031 冥界侍从）
                # 检查控制者是否有"牌库注能激活"标记
                from ..enums import GameTag
                controller = card.controller
                hero = controller.hero
                
                # 检查英雄是否有 MAW_031e buff（牌库注能激活标记）
                has_deck_infuse = any(
                    buff.id == "MAW_031e" 
                    for buff in hero.buffs 
                    if hasattr(buff, 'id')
                )
                
                # 如果有牌库注能标记，也为牌库中的 Infuse 卡充能
                if has_deck_infuse:
                    for deck_card in controller.deck:
                        if hasattr(deck_card, 'infuse_threshold') and deck_card.infuse_threshold > 0:
                            # 检查是否有种族限制
                            infuse_race = getattr(deck_card, 'infuse_race', None)
                            
                            # 如果有种族限制，检查死亡随从是否匹配
                            if infuse_race is not None and card.race != infuse_race:
                                continue  # 跳过不匹配的随从
                            
                            # 增加充能计数
                            if not hasattr(deck_card, 'infuse_counter'):
                                deck_card.infuse_counter = 0
                            deck_card.infuse_counter += 1
                            
                            # 追踪死亡随从的信息
                            if not hasattr(deck_card, 'infused_minions'):
                                deck_card.infused_minions = []
                            deck_card.infused_minions.append({
                                'atk': card.atk,
                                'health': card.health,
                                'id': card.id,
                                'race': card.race
                            })
                            
                            # 注意：牌库中的卡不触发 infuse 效果
                            # 只是累积充能计数，等抽到手牌时已经是充能状态
                
                # 残骸系统：友方随从死亡时，为死亡骑士玩家生成残骸
                # CORPSE 机制 - 巫妖王的进军（2022年12月）
                if card.type == CardType.MINION and card.controller:
                    # 检查控制者是否为死亡骑士
                    if card.controller.hero and card.controller.hero.card_class == CardClass.DEATHKNIGHT:
                        # 友方随从死亡时生成1份残骸
                        card.controller.corpses += 1
                        log_info("corpse_generated", player=card.controller, corpses=card.controller.corpses)

        for card in cards:
            if not card.dead:
                continue
            self._trigger = False
            self.broadcast(source, EventListener.AFTER, card)


class EndTurn(GameAction):
    """
    End the current turn
    """

    PLAYER = ActionArg()

    def do(self, source, player):
        if player.choice:
            raise InvalidAction(
                "%r cannot end turn with the open choice %r." % (player, player.choice)
            )
        source.game.manager.game_action(self, source, player)
        self.broadcast(source, EventListener.ON, player)
        if player.extra_end_turn_effect:
            self.broadcast(source, EventListener.ON, player)

        source.game._end_turn()


class Joust(GameAction):
    """
    Perform a joust between \a challenger and \a defender.
    Note that this does not evaluate the results of the joust. For that,
    see dsl.evaluators.JoustEvaluator.
    """

    CHALLENGER = ActionArg()
    DEFENDER = ActionArg()

    def get_args(self, source):
        challenger = self._args[0].eval(source.game, source)
        defender = self._args[1].eval(source.game, source)
        return challenger and challenger[0], defender and defender[0]

    def do(self, source, challenger, defender):
        log_info("jousting", challenger=challenger, defender=defender)
        source.game.manager.game_action(self, source, challenger, defender)
        source.game.joust(source, challenger, defender, self.callback)


class MulliganChoice(GameAction):
    PLAYER = ActionArg()

    def __init__(self, *args, callback):
        super().__init__(*args)
        self.callback = callback

    def do(self, source, player):
        player.mulligan_state = Mulligan.INPUT
        player.choice = self
        # NOTE: Ideally, we give The Coin when the Mulligan is over.
        # Unfortunately, that's not compatible with Blizzard's way.
        self.cards = player.hand.exclude(id="GAME_005")
        self.source = source
        self.player = player
        self.min_count = 0
        # but weirdly, the game server includes the coin in the mulligan count
        self.max_count = len(player.hand)
        source.game.manager.game_action(self, source, player)

    def choose(self, *cards):
        for card in cards:
            assert card in self.cards
        self.player.choice = None
        for card in cards:
            card._summon_index = 0
            new_card = self.player.deck[-1]
            new_card._summon_index = card.zone_position
            card.zone = Zone.DECK
            new_card.zone = Zone.HAND
        self.player.shuffle_deck()
        self.player.mulligan_state = Mulligan.DONE

        if self.player.opponent.mulligan_state == Mulligan.DONE:
            self.callback()


class Play(GameAction):
    """
    Make the source player play \a card, on \a target or None.
    Choose play action from \a choose or None.
    """

    PLAYER = ActionArg()
    CARD = CardArg()
    TARGET = ActionArg()
    INDEX = IntArg()
    CHOOSE = ActionArg()

    def _broadcast(self, entity, source, at, *args):
        # Prevent cards from triggering off their own play
        if entity is args[1]:
            return
        return super()._broadcast(entity, source, at, *args)

    def do(self, source, card, target, index, choose):
        player = source
        log_info("plays_card", player=player, card=card, target=target, index=index)

        player.last_card_played = card
        if card.type == CardType.SPELL:
            player.last_played_spell = card

        player.pay_cost(card, card.cost)

        card.target = target
        card._summon_index = index

        battlecry_card = choose or card
        # We check whether the battlecry will trigger, before the card.zone changes
        if battlecry_card.battlecry_requires_target() and not target:
            log_info("requires_target_battlecry", card=card)
            trigger_battlecry = False
        else:
            trigger_battlecry = True

        card.play_left_most = card is card.controller.hand[0]
        card.play_right_most = card is card.controller.hand[-1]

        card.zone = Zone.PLAY

        # Remember cast on friendly characters
        if card.type == CardType.SPELL and target and target.controller == source:
            card.cast_on_friendly_characters = True
            if target.type == CardType.MINION:
                card.cast_on_friendly_minions = True
        
        # 追踪对角色施放的法术数量（用于VAC_558海上船歌等卡牌）- 胜地历险记（2024年7月）
        if card.type == CardType.SPELL and target:
            # 检查目标是否为角色（英雄或随从）
            if target.type in [CardType.HERO, CardType.MINION]:
                source.spells_cast_on_characters_this_game += 1

        # 追踪套牌之外的法术（用于RLK_803等卡牌）
        if card.type == CardType.SPELL and hasattr(card, 'creator'):
            # 如果法术有 creator 属性，说明是套牌之外的卡牌
            source.spells_cast_not_from_deck.append(card.id)

        # 追踪套牌之外的随从（用于TTN_481莱登等卡牌）
        if card.type == CardType.MINION and hasattr(card, 'creator'):
            # 如果随从有 creator 属性，说明是套牌之外的卡牌
            source.minions_played_from_outside_deck.append(card.id)

        source.game.manager.game_action(self, source, card, target, index, choose)
        # NOTE: A Play is not a summon! But it sure looks like one.
        # We need to fake a Summon broadcast.
        summon_action = Summon(player, card)

        if card.type == CardType.SPELL and card.twinspell:
            source.game.queue_actions(card, [Give(player, card.twinspell_copy)])

        # LOCATION 机制：销毁旧地标
        if card.type == CardType.LOCATION:
            existing_locations = [c for c in player.field if c.type == CardType.LOCATION]
            for loc in existing_locations:
                loc.destroy()

        if card.type in (CardType.MINION, CardType.WEAPON, CardType.LOCATION):
            self.queue_broadcast(
                summon_action, (player, EventListener.ON, player, card)
            )
        self.broadcast(player, EventListener.ON, player, card, target)
        self.resolve_broadcasts()

        # "Can't Play" (aka Counter) means triggers don't happen either
        if not card.cant_play:
            if card.play_outcast and card.get_actions("outcast"):
                # 追踪本局游戏使用过的流放牌数量（用于RLK_213等卡牌）
                player.outcast_cards_played_this_game += 1
                source.game.trigger(card, card.get_actions("outcast"), event_args=None)
            elif trigger_battlecry:
                # 记录最后的战吼（用于"重复战吼"类卡牌）
                player.last_battlecry = (battlecry_card, card.target)
                source.game.queue_actions(
                    card, [Battlecry(battlecry_card, card.target)]
                )
            
            # 记录最后的抉择法术（用于"开路者"等卡牌）
            if choose and card.has_choose_one:
                player.last_choose_one_card = card
                player.last_choose_one_choice = choose

            if card.echo:
                source.game.queue_actions(
                    card, [Give(player, Buff(Copy(SELF), "GIL_000"))]
                )

            actions = card.get_actions("magnetic")
            if actions:
                source.game.trigger(card, actions, event_args=None)

            # If the play action transforms the card (eg. Druid of the Claw), we
            # have to broadcast the morph result as minion instead.
            played_card = card.morphed or card
            played_card.play_right_most = card.play_right_most
            if played_card.type in (CardType.MINION, CardType.WEAPON, CardType.LOCATION):
                summon_action.broadcast(
                    player, EventListener.AFTER, player, played_card
                )
            self.broadcast(player, EventListener.AFTER, player, played_card, target)
            
            # 低费法术施放两次机制（用于VAC_507阳光汲取者莱妮莎等卡牌）- 胜地历险记（2024年7月）
            # 检查是否为法术且费用<=2，以及玩家是否有"低费法术施放两次"效果
            if card.type == CardType.SPELL and card.cost <= 2:
                # 检查玩家的所有buff，查找low_cost_spells_cast_twice标记
                has_cast_twice_effect = False
                for buff in player.buffs:
                    if hasattr(buff, 'low_cost_spells_cast_twice') and buff.low_cost_spells_cast_twice:
                        has_cast_twice_effect = True
                        break
                
                if has_cast_twice_effect:
                    # 重复触发法术效果
                    # 使用标记防止无限循环
                    if not getattr(card, '_cast_twice_triggered', False):
                        card._cast_twice_triggered = True
                        # 重复触发法术的play效果
                        actions = card.get_actions("play")
                        if actions:
                            source.game.trigger(card, actions, event_args=None)
                        card._cast_twice_triggered = False

        player.combo = True
        player.last_card_played = card
        if card.type == CardType.MINION:
            player.minions_played_this_turn += 1
            if Race.TOTEM in card.races:
                card.controller.times_totem_summoned_this_game += 1
            if Race.ELEMENTAL in card.races:
                player.elemental_played_this_turn += 1
        player.cards_played_this_turn += 1
        player.cards_played_this_game.append(card)

        # 追踪本回合使用的卡牌ID（用于WW_053飞车劫掠等卡牌）
        if hasattr(player, 'cards_played_this_turn_ids'):
            player.cards_played_this_turn_ids.append(card.id)

        # 追踪使用过的另一职业卡牌（用于VAC_700横夺硬抢、VAC_333蓄谋诈骗犯等卡牌）- 胜地历险记（2024年7月）
        # 判断是否为另一职业的卡牌（排除中立和本职业）
        if hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL:
            player_class = player.hero.card_class if player.hero else None
            if player_class and card.card_class != player_class:
                # 这是另一职业的卡牌
                player.cards_played_from_other_class_count += 1
                player.last_card_played_from_other_class = card

        # Miniaturize / Gigantify mechanism (Whizbang's Workshop)
        # 微缩 / 巨大化 机制（威兹班的工坊）
        # When a card with MINIATURIZE or GIGANTIFY is played, add the corresponding token to hand
        # 当打出带有 MINIATURIZE 或 GIGANTIFY 标签的卡牌时，将对应的 Token 加入手牌
        if card.type == CardType.MINION:
            # Check for Miniaturize
            if GameTag.MINIATURIZE in card.tags:
                token_id = card.id + "t"
                if token_id in cards.db:
                    # Create 1-cost 1/1 miniaturized token
                    source.game.queue_actions(card, [Give(player, token_id)])
            
            # Check for Gigantify
            if GameTag.GIGANTIFY in card.tags:
                # Gigantify tokens usually have "t1" suffix (or just "t" if no Miniaturize)
                # Check both possibilities
                token_id = card.id + "t1" if (card.id + "t1") in cards.db else card.id + "t"
                if token_id in cards.db and token_id != card.id + "t":  # Avoid duplicate if Miniaturize exists
                    # Create 8-cost 8/8 gigantified token
                    source.game.queue_actions(card, [Give(player, token_id)])


        card.turn_played = source.game.turn
        card.choose = None
        
        # 纳迦施法计数机制 - 巫妖王的进军（2022年12月）
        # 当施放法术时，更新手牌中所有纳迦卡牌的施法计数器
        if card.type == CardType.SPELL:
            # 追踪本回合施放的法术数量（用于DEEP_010等卡牌）
            player.spells_played_this_turn += 1
            
            # Update spell schools played
            if hasattr(card, "spell_school") and card.spell_school != SpellSchool.NONE:
                player.spell_schools_played_this_game.add(card.spell_school)
                # 追踪本回合施放的法术流派（用于MIS_709圣光荧光棒等卡牌）
                if hasattr(player, 'spell_schools_played_this_turn'):
                    player.spell_schools_played_this_turn.append(card.spell_school)
            
            # Update spell costs played (用于TOY_378星空投影球等卡牌)
            player.spell_costs_played_this_game.add(card.cost)

            for hand_card in player.hand:
                # 检查是否为纳迦卡牌（包括多种族）
                if Race.NAGA in getattr(hand_card, 'races', []):
                    hand_card.spells_cast_while_in_hand += 1

        # Trigger Corrupt effects
        # 触发腐蚀效果
        # When a card is played, all cards in hand with Corrupt and cost < played card cost
        # will trigger their corrupt effect (upgrade)
        # 当打出一张卡牌后，手牌中所有带有腐蚀属性且费用小于打出卡牌费用的卡牌会触发腐蚀效果（升级）
        # 
        # Extended to support multiple corruptions (corrupt, corrupt2, corrupt3, etc.)
        # 扩展支持多次腐蚀（corrupt, corrupt2, corrupt3 等）
        if card.cost > 0:  # Only trigger on cards with cost / 只在打出有费用的卡牌时触发
            for hand_card in player.hand:
                if not hand_card.ignore_scripts and hasattr(hand_card, 'corrupt_active'):
                    if hand_card.corrupt_active and hand_card.cost < card.cost:
                        # Initialize corrupt_count if not present
                        # 如果不存在则初始化腐蚀计数器
                        if not hasattr(hand_card, 'corrupt_count'):
                            hand_card.corrupt_count = 0
                        
                        # Increment corrupt count
                        # 增加腐蚀计数
                        hand_card.corrupt_count += 1
                        
                        # Try to get the appropriate corrupt action based on count
                        # 根据计数尝试获取相应的腐蚀动作
                        # corrupt_count=1 -> "corrupt", corrupt_count=2 -> "corrupt2", etc.
                        corrupt_action_name = "corrupt" if hand_card.corrupt_count == 1 else f"corrupt{hand_card.corrupt_count}"
                        actions = hand_card.get_actions(corrupt_action_name)
                        
                        if actions:
                            # Pass the triggering card as event_args so Corrupt effects can access it
                            # 将触发卡牌作为 event_args 传递，这样腐蚀效果可以访问触发卡牌的信息
                            source.game.trigger(hand_card, actions, event_args={'card': card})
                        
                        # Check if there are more corrupt levels available
                        # 检查是否还有更多腐蚀等级可用
                        next_corrupt_name = f"corrupt{hand_card.corrupt_count + 1}"
                        if not hasattr(hand_card, next_corrupt_name):
                            # No more corrupt levels, deactivate
                            # 没有更多腐蚀等级，停用腐蚀
                            hand_card.corrupt_active = False

        # Trigger Finale effects
        # 触发压轴效果
        # Finale triggers if the player has 0 remaining mana after paying for the card
        # 压轴：当玩家支付卡牌费用后剩余法力值为0时触发
        if player.mana == 0 and hasattr(card, 'finale'):
             actions = card.get_actions("finale")
             if actions:
                 source.game.trigger(card, actions, event_args=None)



class Activate(GameAction):
    PLAYER = ActionArg()
    CARD = CardArg()
    TARGET = ActionArg()
    CHOOSE = ActionArg()

    def get_args(self, source):
        return (source,) + super().get_args(source)

    def do(self, source, player, heropower, target, choose):
        player.pay_cost(heropower, heropower.cost)
        source.game.manager.game_action(self, source, player, heropower, target, choose)
        self.broadcast(source, EventListener.ON, player, heropower, target, choose)

        card = choose or heropower
        source.game.action_start(BlockType.PLAY, heropower, 0, target)
        source.game.queue_actions(source, [PlayHeroPower(card, target)])
        source.game.action_end(BlockType.PLAY, heropower)

        for entity in player.live_entities:
            if not entity.ignore_scripts:
                actions = entity.get_actions("inspire")
                if actions:
                    source.game.trigger(entity, actions, event_args=None)

        self.broadcast(source, EventListener.AFTER, player, heropower, target, choose)
        heropower.activations_this_turn += 1
        
        # 简单启发式：如果英雄技能增加了英雄攻击力（例如德鲁伊变身），累加 attack_gained_this_turn
        # 由于无法精确追踪所有来源，这里主要捕获英雄技能带来的攻击力
        # 实际更准确的做法是在 Buff/Enchantment 应用时追踪，但这涉及核心重构
        # 此处只检查 Hero Power 施放后的 Hero Attack 变化？不，这比较难比较前后。
        # 假设 Druid HP (+1 Atk) 是主要来源。
        # 该值需由具体卡牌逻辑维护，或者通过特定 Action 增加。
        # 鉴于无法修改所有 Gain Attack 的源头，我们可以在 Druid 的 HP 逻辑或其他卡牌中手动增加这个计数器。
        # 但既然我们修改了 Player，最好有一个通用的入口。
        # 暂时在 Activate 中不做通用处理，依靠卡牌脚本手动更新 player.attack_gained_this_turn。


class ActivateLocation(GameAction):
    """
    激活地标
    
    地标激活流程:
    1. 检查地标是否可激活(未耗尽、未冷却、有耐久度)
    2. 验证目标(如果需要)
    3. 执行地标的 activate 脚本
    4. 消耗1点耐久度
    5. 增加激活次数
    6. 触发相关事件
    7. 如果耐久度归零,销毁地标
    """
    LOCATION = CardArg()
    TARGET = ActionArg()
    
    def get_args(self, source):
        # source 是 player
        return (source,) + super().get_args(source)
    
    def do(self, source, location, target):
        """
        执行地标激活
        
        Args:
            source: 激活地标的玩家
            location: 要激活的地标
            target: 激活目标(如果需要)
        """
        player = source
        
        # 验证地标是否可激活
        if not location.is_usable():
            raise InvalidAction("%r cannot be activated (exhausted or no durability)" % location)
        
        # 验证目标
        if location.requires_target():
            if not target:
                raise InvalidAction("%r requires a target" % location)
            # TODO: 验证目标是否有效(类似 play_targets 检查)
        
        log_info("activates_location", player=player, location=location, target=target)
        
        # 记录目标
        location.target = target
        
        # 广播激活事件(ON)
        source.game.manager.game_action(self, source, location, target)
        self.broadcast(source, EventListener.ON, player, location, target)
        
        # 执行地标的 activate 脚本
        source.game.action_start(BlockType.PLAY, location, 0, target)
        actions = location.get_actions("activate")
        if actions:
            source.game.trigger(location, actions, event_args=None)
        source.game.action_end(BlockType.PLAY, location)
        
        # 消耗耐久度
        source.game.queue_actions(source, [Hit(location, 1)])
        
        # 增加激活次数
        location.activations_this_turn += 1
        
        # 追踪本局游戏使用地标的次数（用于VAC_439海滨巨人等卡牌）- 胜地历险记（2024年7月）
        player.locations_used_this_game += 1
        
        # 广播激活事件(AFTER)
        self.broadcast(source, EventListener.AFTER, player, location, target)
        
        # 清除目标
        location.target = None
        
        # 检查耐久度,如果归零则销毁
        if location.durability <= 0:
            log_info("location_destroyed", location=location)
            source.game.queue_actions(source, [Destroy(location)])


class Overload(GameAction):
    PLAYER = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, player, amount):
        if player.cant_overload:
            log_info("cannot_overload", source=source, player=player)
            return
        log_info("overloads", source=source, player=player, amount=amount)
        source.game.manager.game_action(self, source, player, amount)
        self.broadcast(source, EventListener.ON, player, amount)
        player.overloaded += amount
        player.overloaded_this_game += amount


class SpendCorpses(GameAction):
    """
    消耗残骸（死亡骑士专属资源）
    CORPSE 机制 - 巫妖王的进军（2022年12月）
    """
    PLAYER = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, player, amount):
        if player.corpses < amount:
            log_info("insufficient_corpses", source=source, player=player, required=amount, available=player.corpses)
            return False
        log_info("spends_corpses", source=source, player=player, amount=amount)
        source.game.manager.game_action(self, source, player, amount)
        self.broadcast(source, EventListener.ON, player, amount)
        player.corpses -= amount
        return True


class GainCorpses(GameAction):
    """
    获得残骸（死亡骑士专属资源）
    CORPSE 机制 - 巫妖王的进军（2022年12月）
    """
    PLAYER = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, player, amount):
        log_info("gains_corpses", source=source, player=player, amount=amount)
        source.game.manager.game_action(self, source, player, amount)
        self.broadcast(source, EventListener.ON, player, amount)
        player.corpses += amount


class TargetedAction(Action):
    TARGET = ActionArg()

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop("source", None)
        super().__init__(*args, **kwargs)
        self.trigger_index = 0

    def __repr__(self):
        args = ["%s=%r" % (k, v) for k, v in zip(self.ARGS[1:], self._args[1:])]
        return "<TargetedAction: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

    def __mul__(self, value):
        self.times = value
        return self

    def eval(self, selector, source):
        if isinstance(selector, Entity):
            return [selector]
        else:
            return selector.eval(source.game, source)

    def get_target_args(self, source, target):
        ret = []
        for k, v in zip(self.ARGS[1:], self._args[1:]):
            if isinstance(v, Selector):
                # evaluate Selector arguments
                v = v.eval(source.game, source)
            elif isinstance(v, LazyValue):
                v = v.evaluate(source)
            elif isinstance(v, Action):
                v = v.trigger(source)[0]
            elif isinstance(k, CardArg):
                v = _eval_card(source, v)
            ret.append(v)
        return ret

    def get_targets(self, source, t):
        if isinstance(t, Entity):
            ret = t
        elif isinstance(t, LazyValue):
            ret = t.evaluate(source)
        elif isinstance(t, str):
            ret = source.controller.card(t, source=source)
        elif isinstance(t, Action):
            ret = t.trigger(source)[0]
        else:
            ret = t.eval(source.game, source)
        if not ret:
            return []
        if not hasattr(ret, "__iter__"):
            # Bit of a hack to ensure we always get a list back
            ret = [ret]
        return ret

    def trigger(self, source):
        ret = []

        if self.source is not None and isinstance(self.source, Selector):
            source = self.source.eval(source.game, source)
            assert len(source) == 1
            source = source[0]

        times = self.times
        if isinstance(times, LazyValue):
            times = times.evaluate(source)
        elif isinstance(times, Action):
            times = times.trigger(source)[0]
        elif isinstance(times, Selector):
            times = times.eval(source.game, source)

        for i in range(times):
            ret += self._trigger(i, source)

        self.resolve_broadcasts()

        return ret

    def _trigger(self, i, source):
        if source.controller.choice:
            self.choice_callback.append(lambda: self._trigger(i, source))
            return []
        ret = []
        self.trigger_index = i
        args = self.get_args(source)
        targets = self.get_targets(source, args[0])
        args = args[1:]
        log_info("triggering_targeting", source=source, trigger=self, targets=targets)
        for target in targets:
            target_args = self.get_target_args(source, target)
            ret.append(self.do(source, target, *target_args))

            for action in self.callback:
                log_info("queues_callback", action=self, callback=action)
                ret += source.game.queue_actions(
                    source, [action], event_args=[target] + target_args
                )
        return ret


class Buff(TargetedAction):
    """
    Buff character targets with Enchantment \a id
    NOTE: Any Card can buff any other Card. The controller of the
    Card that buffs the target becomes the controller of the buff.
    """

    TARGET = ActionArg()
    BUFF = ActionArg()

    def get_target_args(self, source, target):
        buff = self._args[1]
        buff = source.controller.card(buff, source=source)
        buff.source = source
        return [buff]

    def do(self, source, target, buff):
        kwargs = self._kwargs.copy()
        for k, v in kwargs.items():
            if isinstance(v, LazyValue):
                v = v.evaluate(source)
            setattr(buff, k, v)
        
        # 检查是否给英雄增加了攻击力（用于德鲁伊任务线等卡牌）
        is_hero_attack_buff = (
            target.type == CardType.HERO and 
            hasattr(buff, 'tags') and 
            buff.tags.get(GameTag.ATK, 0) > 0
        )
        attack_gained = buff.tags.get(GameTag.ATK, 0) if is_hero_attack_buff else 0
        
        buff.apply(target)
        source.game.manager.targeted_action(self, source, target, buff)
        
        # 触发"英雄获得攻击力"事件
        if is_hero_attack_buff and attack_gained > 0:
            # 触发所有监听该事件的实体
            for entity in target.controller.live_entities:
                if hasattr(entity, 'hero_attack_gained'):
                    actions = entity.get_actions("hero_attack_gained")
                    if actions:
                        source.game.trigger(entity, actions, event_args={'attack': attack_gained})
        
        return target



class MultiBuff(TargetedAction):
    TARGET = ActionArg()
    BUFFS = ActionArg()

    def get_target_args(self, source, target):
        buffs = self._args[1]
        buffs = [source.controller.card(buff, source=source) for buff in buffs]
        for buff in buffs:
            buff.source = source
        return [buffs]

    def do(self, source, target, buffs):
        for buff in buffs:
            kwargs = self._kwargs.copy()
            for k, v in kwargs.items():
                if isinstance(v, LazyValue):
                    v = v.evaluate(source)
                setattr(buff, k, v)
            buff.apply(target)
            source.game.manager.targeted_action(self, source, target, buff)
        return target


class StoringBuff(TargetedAction):
    TARGET = ActionArg()
    BUFF = ActionArg()
    CARD = ActionArg()

    def get_target_args(self, source, target):
        buff = self._args[1]
        card = _eval_card(source, self._args[2])[0]
        buff = source.controller.card(buff, source=source)
        buff.source = source
        return [buff, card]

    def do(self, source, target, buff, card):
        log_info("store_card", buff=buff, card=card)
        buff.store_card = card
        return buff.apply(target)


class Bounce(TargetedAction):
    """
    Bounce minion targets on the field back into the hand.
    """

    def do(self, source, target):
        if len(target.controller.hand) >= target.controller.max_hand_size:
            log_info("bounced_destroyed", target=target)
            return source.game.queue_actions(source, [Destroy(target)])
        else:
            log_info("bounced_to_hand", target=target, controller=target.controller)
            target.zone = Zone.HAND
            source.game.manager.targeted_action(self, source, target)


class Choice(TargetedAction):
    CARDS = ActionArg()
    CARD = ActionArg()

    def get_target_args(self, source, target):
        cards = self._args[1]
        if isinstance(cards, Selector):
            cards = cards.eval(source.game, source)
        elif isinstance(cards, LazyValue):
            cards = cards.evaluate(source)
        elif isinstance(cards, list):
            eval_cards = []
            for card in cards:
                if isinstance(card, LazyValue):
                    eval_cards.append(card.evaluate(source)[0])
                elif isinstance(card, str):
                    eval_cards.append(source.controller.card(card, source))
                else:
                    eval_cards.append(card)
            cards = eval_cards

        return [cards]

    def do(self, source, player, cards):
        if len(cards) == 0:
            return
        log_info("choice_from", player=player, cards=cards)
        player.choice = self
        self._callback = self.callback
        self.callback = []
        self.source = source
        self.player = player
        self.cards = cards
        self.min_count = 1
        self.max_count = 1
        source.game.manager.targeted_action(self, source, player, cards)

    def choose(self, card):
        if card not in self.cards:
            raise InvalidAction(
                "%r is not a valid choice (one of %r)" % (card, self.cards)
            )
        self.player.choice = None
        for action in self._callback:
            self.source.game.trigger(self.source, [action], [self.cards, card])
        self.callback = self._callback
        self.trigger_choice_callback()


class GenericChoice(Choice):
    def choose(self, card):
        super().choose(card)
        for _card in self.cards:
            if _card is card:
                if card.type == CardType.HERO_POWER:
                    _card.zone = Zone.PLAY
                elif len(self.player.hand) < self.player.max_hand_size:
                    _card.zone = Zone.HAND
                else:
                    _card.discard()
            else:
                _card.discard()


class SecretChoice(GenericChoice):
    """
    秘密选择（Secret Choice）- 对手看不到玩家的选择内容
    用于实现类似"剑圣奥卡尼"这样的秘密选择机制
    """
    def do(self, source, player, cards):
        # 标记这是一个秘密选择
        result = super().do(source, player, cards)
        if hasattr(self, 'player') and self.player:
            # 为选择添加秘密标记，供游戏管理器使用
            self.secret = True
        return result


class DiscoverWithPendingGuess(GenericChoice):
    """
    发现并记录待对手猜测（Discover with Pending Guess）
    用于实现"可疑的炼金师"等卡牌

    流程：
    1. 玩家发现一张卡牌（从3个选项中选择）
    2. 记录选项和选择到对手的 pending_guesses 队列
    3. 在对手回合开始时，对手猜测玩家的选择
    4. 如果猜中，对手也获得一张复制
    """
    def do(self, source, player, cards):
        # 玩家正常发现
        result = super().do(source, player, cards)

        # 记录到对手的待猜测队列
        opponent = player.opponent
        if opponent and hasattr(opponent, 'pending_guesses'):
            # 获取选中的卡牌ID
            chosen_card = None
            for card in cards:
                if card.zone == Zone.HAND or card.zone == Zone.PLAY:
                    chosen_card = card
                    break

            if chosen_card:
                # 记录选项和选择
                opponent.pending_guesses.append({
                    "options": [c.card_id for c in cards],  # 3个选项的ID
                    "chosen": chosen_card.card_id           # 玩家选择的ID
                })

        return result


class CopyDeathrattleBuff(TargetedAction):
    """
    Copy the deathrattles from a card onto the target
    """

    TARGET = ActionArg()
    Buff = ActionArg()

    def get_target_args(self, source, target):
        buff = self._args[1]
        buff = source.controller.card(buff, source=source)
        buff.tags[GameTag.DEATHRATTLE] = True
        buff.source = source
        return [buff]

    def create_buff(self, source):
        buff = self._args[1]
        buff = source.controller.card(buff, source=source)
        buff.tags[GameTag.DEATHRATTLE] = True
        buff.source = source
        return buff

    def do(self, source, target, buff):
        log_info("copy_deathrattle", source=source, target=target, buff=buff)
        if target.has_deathrattle:
            for deathrattle in target.deathrattles:
                source.additional_deathrattles.append(deathrattle)
            buff.apply(source)
            for entity in target.buffs:
                if not entity.has_deathrattle:
                    continue
                new_buff = self.create_buff(source)
                if hasattr(entity, "store_card"):
                    new_buff.store_card = entity.store_card
                for deathrattle in entity.deathrattles:
                    new_buff.additional_deathrattles.append(deathrattle)
                new_buff.apply(source)
        source.game.manager.targeted_action(self, source, target, buff)


class Counter(TargetedAction):
    """
    Counter a card, making it unplayable.
    """

    def do(self, source, target):
        target.cant_play = True
        source.game.manager.targeted_action(self, source, target)


class Predamage(TargetedAction):
    """
    Predamage target by \a amount.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()
    TRIGGER_LIFESTEAL = BoolArg(default=True)

    def do(self, source, target, amount, trigger_lifesteal):
        amount <<= target.incoming_damage_multiplier
        target.predamage = amount
        if amount:
            self.broadcast(source, EventListener.ON, target, amount)
            return source.game.trigger_actions(source, [Damage(target, None, trigger_lifesteal)])[0][0]
        return 0


class PutOnTop(TargetedAction):
    """
    Put card on deck top
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def do(self, source, target, cards):
        log_info("put_on_deck_top", cards=cards, target=target)
        if not isinstance(cards, list):
            cards = [cards]

        if cards:
            target.shuffle_deck()

        for card in cards:
            if card.controller != target:
                card.zone = Zone.SETASIDE
                card.controller = target
            if card.zone != Zone.DECK and len(target.deck) >= target.max_deck_size:
                log_info("put_fails_deck_full", card=card, target=target)
                continue
            card.zone = Zone.DECK
            card, card.controller.deck[-1] = card.controller.deck[-1], card
            source.game.manager.targeted_action(self, source, target, card)


class Damage(TargetedAction):
    """
    Damage target by \a amount.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()
    TRIGGER_LIFESTEAL = BoolArg(default=True)

    def do(self, source, target, amount=None, trigger_lifesteal=True):
        if not amount:
            amount = target.predamage
        amount = target._hit(amount)
        target.predamage = 0
        if (
            source.type == CardType.MINION or source.type == CardType.HERO
        ) and source.stealthed:
            # TODO this should be an event listener of sorts
            source.stealthed = False
        source.game.manager.targeted_action(self, source, target, amount)
        if amount:
            # check hasattr: some sources of damage are game or player (like fatigue)
            # weapon damage itself after hero attack, but does not trigger lifesteal
            if (
                trigger_lifesteal
                and hasattr(source, "lifesteal")
                and source.lifesteal
                and source.type != CardType.WEAPON
            ):
                from fireplace.enums import LIFESTEAL_DAMAGES_ENEMY
                if source.controller.tags.get(LIFESTEAL_DAMAGES_ENEMY, 0):
                    # Inverted Lifesteal: Deal damage to enemy hero
                    # Pass trigger_lifesteal=False to prevent infinite loop
                    source.game.queue_actions(source, [Hit(source.controller.opponent.hero, amount, False)])
                else:
                    source.heal(source.controller.hero, amount)
            self.broadcast(source, EventListener.ON, target, amount, source)
            # poisonous can not destroy hero
            if (
                hasattr(source, "poisonous")
                and source.poisonous
                and (target.type != CardType.HERO and source.type != CardType.WEAPON)
            ):
                target.destroy()
            if (
                hasattr(source, "has_overkill")
                and source.has_overkill
                and source.controller.current_player
                and target.type != CardType.WEAPON
                and target.health < 0
            ):
                if source.type == CardType.HERO:
                    actions = source.controller.weapon.get_actions("overkill")
                else:
                    actions = source.get_actions("overkill")
                if actions:
                    source.game.trigger(source, actions, event_args=None)
            target.damaged_this_turn += amount
            if source.type == CardType.HERO_POWER:
                source.controller.hero_power_damage_this_game += amount

            # Frenzy: 当随从首次受到伤害并存活时触发
            # Trigger Frenzy if the target is a minion, survived the damage, and has frenzy_active
            if (
                target.type == CardType.MINION
                and target.zone == Zone.PLAY
                and hasattr(target, 'frenzy_active')
                and target.frenzy_active
            ):
                actions = target.get_actions("frenzy")
                if actions:
                    source.game.trigger(target, actions, event_args={'damage': amount})
                    target.frenzy_active = False  # Frenzy 只触发一次

            # Honorable Kill: 当精确击杀目标时触发（伤害值恰好等于目标剩余生命值）
            # Trigger Honorable Kill if the damage exactly killed the target
            if (
                amount > 0
                and target.type == CardType.MINION
                and target.health == 0  # 精确击杀：生命值降为0
                and target.zone == Zone.GRAVEYARD  # 目标已死亡
                and hasattr(source, 'honorable_kill')
            ):
                actions = source.get_actions("honorable_kill")
                if actions:
                    source.game.trigger(source, actions, event_args={'target': target})
        return amount


class Deathrattle(TargetedAction):
    """
    Trigger deathrattles on card targets.
    """

    def do(self, source, target):
        if not target.has_deathrattle:
            return

        for entity in target.entities:
            source.game.manager.targeted_action(self, source, target)
            for deathrattle in entity.deathrattles:
                if callable(deathrattle):
                    actions = deathrattle(entity)
                else:
                    actions = deathrattle
                source.game.queue_actions(entity, actions)

                if target.controller.extra_deathrattles:
                    log_info("triggering_deathrattles_again", target=target)
                    source.game.queue_actions(entity, actions)


class Battlecry(TargetedAction):
    """
    Trigger Battlecry on card targets
    """

    CARD = CardArg()
    TARGET = ActionArg()

    def get_target_args(self, source, target):
        arg = self._args[1]
        if isinstance(arg, Selector):
            arg = arg.eval(source.game, source)
            assert len(arg) == 1
            arg = arg[0]
        elif isinstance(arg, LazyValue):
            arg = arg.evaluate(source)
            if hasattr(arg, "__iter__"):
                arg = arg[0]
        else:
            arg = _eval_card(source, arg)[0]
        return [arg]

    def has_extra_battlecries(self, player, card):
        # Brann Bronzebeard
        if player.extra_battlecries and card.has_battlecry:
            return True

        # Spirit of the Shark
        if card.type == CardType.MINION:
            if player.minion_extra_combos and card.has_combo and player.combo:
                return True
            if player.minion_extra_battlecries and card.has_battlecry:
                return True

        return False

    def get_extra_battlecry_count(self, player, card):
        """
        计算战吼额外触发的次数
        返回额外触发次数（不包括原始的1次）
        
        支持：
        - 布尔值 extra_battlecries：额外触发1次
        - 多个 extra_battlecries buff：叠加触发次数
        """
        if not card.has_battlecry:
            return 0
        
        extra_count = 0
        
        # 检查玩家的所有 buff，统计 EXTRA_BATTLECRIES 的数量
        for buff in player.buffs:
            if hasattr(buff, 'tags') and buff.tags.get(enums.EXTRA_BATTLECRIES):
                extra_count += 1
        
        # 检查随从的额外战吼（Spirit of the Shark）
        if card.type == CardType.MINION:
            if player.minion_extra_combos and card.has_combo and player.combo:
                extra_count += 1
            elif player.minion_extra_battlecries:
                for buff in player.buffs:
                    if hasattr(buff, 'tags') and buff.tags.get(enums.MINION_EXTRA_BATTLECRIES):
                        extra_count += 1
        
        return extra_count

    def do(self, source, card, target=None):
        player = source.controller

        if card.has_combo and player.combo:
            log_info("activating_combo", card=card, target=target)
            actions = card.get_actions("combo")
        else:
            log_info("activating_action", card=card, target=target)
            actions = card.get_actions("play")

        if card.battlecry_requires_target() and not target:
            log_info("requires_target_battlecry", card=card)
            return

        source.game.manager.targeted_action(self, source, card, target)
        source.target = target
        
        # 原始触发（1次）
        source.game.main_power(source, actions, target)

        # 额外触发（根据 buff 数量决定）
        extra_count = self.get_extra_battlecry_count(player, card)
        for _ in range(extra_count):
            source.game.main_power(source, actions, target)

        if card.overload:
            source.game.queue_actions(card, [Overload(player, card.overload)])


class RepeatBattlecry(GameAction):
    """
    重复上一个战吼效果
    用于"璀璨金刚鹦鹉"等卡牌
    """
    PLAYER = ActionArg()
    
    def do(self, source, player):
        """
        重复上一个战吼
        
        从 player.last_battlecry 获取最后的战吼信息并重新触发
        """
        if not player.last_battlecry:
            # 没有上一个战吼
            return
        
        battlecry_card, original_target = player.last_battlecry
        
        # 检查卡牌是否需要目标
        if battlecry_card.battlecry_requires_target():
            # 需要目标，验证原目标是否仍然有效
            from .targeting import is_valid_target
            
            valid_targets = [
                t for t in source.game.characters
                if is_valid_target(battlecry_card, t)
            ]
            
            if not valid_targets:
                # 没有有效目标，无法重复战吼
                return
            
            # 如果原目标仍然有效，使用原目标；否则随机选择
            if original_target and original_target in valid_targets:
                target = original_target
            else:
                target = source.game.random_choice(valid_targets)
        else:
            target = None
        
        # 触发战吼
        source.game.queue_actions(source, [Battlecry(battlecry_card, target)])



class ExtraBattlecry(Battlecry):
    def has_extra_battlecries(self, player, card):
        return False

    def do(self, source, card, target=None):
        if target is None:
            old_requirements = source.requirements
            source.requirements = card.requirements
            if source.requires_target():
                target = source.game.random.choice(source.play_targets)
            source.requirements = old_requirements

        return super().do(source, card, target)


class PlayHeroPower(TargetedAction):
    HERO_POWER = CardArg()
    TARGET = ActionArg()

    def do(self, source, heropower, targets):
        actions = heropower.get_actions("activate")
        if not hasattr(targets, "__iter__"):
            targets = [targets]
        for target in targets:
            heropower.target = target
            source.game.manager.targeted_action(self, source, heropower, target)
            source.game.main_power(heropower, actions, target)


class Destroy(TargetedAction):
    """
    Destroy character targets.
    """

    def do(self, source, target):
        if getattr(target, "dormant", False) and target.zone == Zone.PLAY:
            log_info("dormant_cannot_destroy", target=target)
            return
        if target.delayed_destruction:
            #  If the card is in PLAY, it is instead scheduled to be destroyed
            # It will be moved to the graveyard on the next Death event
            log_info("marks_imminent_death", source=source, target=target)
            target.to_be_destroyed = True
            source.game.manager.targeted_action(self, source, target)
        else:
            log_info("destroys", source=source, target=target)
            if target.type == CardType.ENCHANTMENT:
                target.remove()
            else:
                target.zone = Zone.GRAVEYARD
                source.game.manager.targeted_action(self, source, target)


class Discard(TargetedAction):
    """
    Discard card targets in a player's hand
    """

    def do(self, source, target):
        self.broadcast(source, EventListener.ON, target)
        log_info("discarding", target=target)
        old_zone = target.zone
        target.zone = Zone.REMOVEDFROMGAME
        source.game.manager.targeted_action(self, source, target)
        if old_zone == Zone.HAND:
            target.tags[DISCARDED] = True
            actions = target.get_actions("discard")
            source.game.cheat_action(target, actions)


class Setaside(TargetedAction):
    """
    Move card targets to the SETASIDE zone.
    This is used for temporarily storing cards that will be retrieved later.
    """

    def do(self, source, target):
        log_info("setting_aside", target=target)
        target.zone = Zone.SETASIDE
        source.game.manager.targeted_action(self, source, target)


class Discover(TargetedAction):
    """
    Opens a generic choice for three random cards matching a filter.
    """

    TARGET = ActionArg()
    CARDS = CardArg()
    CARD = CardArg()

    def get_target_args(self, source, target):
        if target.hero.data.card_class != CardClass.NEUTRAL:
            # use hero class for Discover if not neutral (eg. Ragnaros)
            discover_class = target.hero.data.card_class
        elif source.data.card_class != CardClass.NEUTRAL:
            # use card class for neutral hero classes
            discover_class = source.data.card_class
        else:
            # use random class for neutral hero classes with neutral cards
            discover_class = random_class()
        if "card_class" in self._args[1].filters:
            picker = self._args[1] * 3
            return [picker.evaluate(source)]
        picker = self._args[1] * 3
        picker = picker.copy_with_weighting(1, card_class=CardClass.NEUTRAL)
        picker = picker.copy_with_weighting(1, card_class=discover_class)
        return [picker.evaluate(source)]

    def do(self, source, target, cards):
        log_info("discovers", source=source, cards=cards, target=target)
        self.cards = cards
        player = source.controller
        player.choice = self
        self._callback = self.callback
        self.callback = []
        self.player = player
        self.source = source
        self.target = target
        self.cards = cards
        self.min_count = 1
        self.max_count = 1
        source.game.manager.targeted_action(self, source, target, cards)

    def choose(self, card):
        if card not in self.cards:
            raise InvalidAction(
                "%r is not a valid choice (one of %r)" % (card, self.cards)
            )
        self.player.choice = None
        for action in self._callback:
            self.source.game.trigger(
                self.source, [action], [self.target, self.cards, card]
            )
        self.callback = self._callback
        self.trigger_choice_callback()


class Draw(TargetedAction):
    """
    Make player targets draw a card from their deck.
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def get_target_args(self, source, target):
        args = super().get_target_args(source, target)
        if args:
            card = args[0]
            if hasattr(card, "__iter__"):
                card = card[0]
            return [card]

        # 检查"机会敲门"畸变效果（YOG_530 古加尔的畸变）
        # 如果是本回合第一次抽牌，且畸变生效，则从牌库中选择可支付的牌
        if (target.deck and
            target.cards_drawn_this_turn == 0 and
            hasattr(source.game, 'active_anomaly') and
            source.game.active_anomaly == 'opportunity_knocks'):
            # 筛选牌库中可支付的牌
            affordable_cards = [c for c in target.deck if c.cost <= target.mana]
            if affordable_cards:
                # 随机选择一张可支付的牌
                card = source.game.random.choice(affordable_cards)
            else:
                # 如果没有可支付的牌，则正常抽取牌库顶的牌
                card = target.deck[-1]
        elif target.deck:
            card = target.deck[-1]
        else:
            card = None
        return [card]

    def do(self, source, target, card):
        if card is None:
            target.fatigue()
            return []
        if len(target.hand) >= target.max_hand_size:
            log_info("overdraws", target=target, card=card)
            card.discard()
        else:
            log_info("draws", target=target, card=card)
            card.zone = Zone.HAND
            card.turn_drawn = source.game.turn
            source.controller.cards_drawn_this_turn += 1
            source.controller.cards_drawn_this_game += 1  # 更新本局游戏抽牌总数（用于TOY_530等卡牌）
            # Initialize Corrupt state for cards with corrupt when drawn to hand
            # 当卡牌被抽到手牌时，初始化腐蚀状态（如果卡牌有腐蚀属性）
            if hasattr(card, 'corrupt'):
                card.corrupt_active = True
                card.corrupt_count = 0  # Initialize corrupt counter for multi-level corruption
            # Initialize Forge state for cards with forge when drawn to hand
            # 当卡牌被抽到手牌时，初始化锻造状态（如果卡牌有锻造属性）
            if hasattr(card, 'forge'):
                card.forge_active = True
                card.forged = False
            source.game.manager.targeted_action(self, source, target, card)
            if source.game.step > Step.BEGIN_MULLIGAN:
                # Proc the draw script, but only if we are past mulligan
                actions = card.get_actions("draw")
                source.game.cheat_action(card, actions)
            self.broadcast(source, EventListener.ON, target, card, source)

        return [card]


class Fatigue(TargetedAction):
    """
    Hit a player with a tick of fatigue
    """

    def do(self, source, target):
        if target.cant_fatigue:
            log_info("cant_fatigue", target=target)
            return
        target.fatigue_counter += 1
        log_info("fatigue_damage", target=target, amount=target.fatigue_counter)
        source.game.manager.targeted_action(self, source, target)
        return source.game.queue_actions(
            source, [Hit(target.hero, target.fatigue_counter)]
        )


class ForceDraw(TargetedAction):
    """
    Draw card targets into their owners hand
    """

    def do(self, source, target):
        target.draw()
        return [target]


class DrawUntil(TargetedAction):
    """
    Make target player target draw up to \a amount cards minus their hand count.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        if target not in target.game.players:
            raise InvalidAction("%r is not a player" % target)
        difference = max(0, amount - len(target.hand))
        if difference > 0:
            return source.game.queue_actions(source, [Draw(target) * difference])


class FullHeal(TargetedAction):
    """
    Fully heal character targets.
    """

    def do(self, source, target):
        source.heal(target, target.max_health)


class GainArmor(TargetedAction):
    """
    Make hero targets gain \a amount armor.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        target.armor += amount
        
        # 追踪本回合获得的护甲（如果目标是英雄）
        if target.type == CardType.HERO and hasattr(target.controller, 'armor_gained_this_turn'):
            target.controller.armor_gained_this_turn += amount
            
        source.game.manager.targeted_action(self, source, target, amount)
        self.broadcast(source, EventListener.ON, target, amount)


class GainMana(TargetedAction):
    """
    Give player targets \a Mana crystals.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def get_target_args(self, source, target):
        ret = super().get_target_args(source, target)
        amount = ret[0]
        if target.max_mana + amount > target.max_resources:
            amount = target.max_resources - target.max_mana
        return [amount]

    def do(self, source, target, amount):
        target.max_mana = max(target.max_mana + amount, 0)
        source.game.manager.targeted_action(self, source, target, amount)


class SpendMana(TargetedAction):
    """
    Make player targets spend \a amount Mana.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        log_info("pays_mana", target=target, amount=amount)
        _amount = amount
        if target.temp_mana:
            # Coin, Innervate etc
            used_temp = min(target.temp_mana, amount)
            _amount -= used_temp
            target.temp_mana -= used_temp
        target.used_mana = max(target.used_mana + _amount, 0)
        source.game.manager.targeted_action(self, source, target, amount)
        self.broadcast(source, EventListener.AFTER, target, amount)


class SetMana(TargetedAction):
    """
    Set player to targets Mana crystals.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        old_mana = target.mana
        target.max_mana = amount
        target.used_mana = max(
            0, target.max_mana - target.overload_locked - old_mana + target.temp_mana
        )
        source.game.manager.targeted_action(self, source, target, amount)


class SpendArmor(TargetedAction):
    """
    Make hero targets spend \a amount Armor.
    Used for cards like Anub'Rekhan (RLK_659) that allow paying with armor instead of mana.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        # Reduce armor by the specified amount
        target.armor = max(0, target.armor - amount)
        source.game.manager.targeted_action(self, source, target, amount)
        self.broadcast(source, EventListener.AFTER, target, amount)


class Give(TargetedAction):
    """
    Give player targets card \a id.
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def do(self, source, target, cards):
        log_info("giving_to", cards=cards, target=target)
        ret = []
        if not hasattr(cards, "__iter__"):
            # Support Give on multiple cards at once (eg. Echo of Medivh)
            cards = [cards]
        for card in cards:
            if len(target.hand) >= target.max_hand_size:
                log_info("give_fails_hand_full", card=card, target=target)
                continue
            card.controller = target
            card.zone = Zone.HAND
            ret.append(card)

            # 追踪非潜行者职业牌加入手牌（用于 AV_298 野爪豺狼人）
            if hasattr(card, 'card_class') and card.card_class != CardClass.ROGUE and card.card_class != CardClass.NEUTRAL:
                target.non_rogue_cards_added_to_hand += 1

            source.game.manager.targeted_action(self, source, target, card)
            self.broadcast(source, EventListener.AFTER, target, card)
        return ret


class Hit(TargetedAction):
    """
    Hit character targets by \a amount.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()
    TRIGGER_LIFESTEAL = BoolArg(default=True)

    def do(self, source, target, amount, trigger_lifesteal):
        # 检查"战吼无法伤害敌方英雄"限制（用于 TOY_501 Shudderblock）
        # 如果源卡牌的控制者有此 buff，且目标是敌方英雄，则跳过伤害
        if target.type == CardType.HERO and target.controller != source.controller:
            # 检查控制者是否有"战吼无法伤害敌方英雄"的 buff
            for buff in source.controller.buffs:
                if hasattr(buff, 'battlecry_cant_damage_enemy_hero') and buff.battlecry_cant_damage_enemy_hero:
                    # 跳过对敌方英雄的伤害
                    log_info("battlecry_cant_damage_enemy_hero", source=source, target=target)
                    return 0
        
        # 应用英雄技能伤害加成（用于"瞄准射击"等卡牌）
        if source.type == CardType.HERO_POWER and hasattr(source.controller, 'hero_power_damage_bonus'):
            bonus = source.controller.hero_power_damage_bonus
            if bonus > 0:
                amount += bonus
                # 使用后重置加成
                source.controller.hero_power_damage_bonus = 0
        
        amount = source.get_damage(amount, target)
        if amount:
            source.game.manager.targeted_action(self, source, target, amount)
            
            # 追踪本回合受到的伤害（用于"暗影之刃飞刀手"等卡牌）
            if target.type == CardType.HERO and hasattr(target.controller, 'damage_taken_this_turn'):
                target.controller.damage_taken_this_turn += amount
            
            # 追踪在自己回合受到的伤害（本局游戏累计,用于TTN_462被禁锢的恐魔等卡牌）
            if target.type == CardType.HERO and target.controller.current_player:
                if hasattr(target.controller, 'damage_taken_on_own_turn_this_game'):
                    target.controller.damage_taken_on_own_turn_this_game += amount
            
            return source.game.queue_actions(source, [Predamage(target, amount, trigger_lifesteal)])[0][0]
        return 0



class HitExcessDamage(TargetedAction):
    """
    Hit character targets by \a amount and excess damage to other.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()
    TRIGGER_LIFESTEAL = BoolArg(default=True)

    def do(self, source, target, amount, trigger_lifesteal):
        amount = source.get_damage(amount, target)
        if amount:
            source.game.manager.targeted_action(self, source, target, amount)
            if target.health >= amount:
                source.game.queue_actions(source, [Predamage(target, amount, trigger_lifesteal)])
                return 0
            else:
                excess_amount = amount - target.health
                source.game.queue_actions(source, [Predamage(target, amount, trigger_lifesteal)])
                return excess_amount
        return 0


class Heal(TargetedAction):
    """
    Heal character targets by \a amount.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        if source.controller.healing_as_damage:
            return source.game.queue_actions(source.controller, [Hit(target, amount)])

        amount = source.get_heal(amount, target)

        # Calculate overheal amount before capping
        # 在限制治疗量之前计算过量治疗数值
        overheal_amount = max(0, amount - target.damage)

        amount = min(amount, target.damage)
        if amount:
            # Undamaged targets do not receive heals
            log_info("heals", source=source, target=target, amount=amount)
            target.damage -= amount
            source.game.manager.targeted_action(self, source, target, amount)
            self.queue_broadcast(self, (source, EventListener.ON, target, amount))
            target.healed_this_turn += amount
            source.controller.healed_this_game += amount

        # Trigger Overheal effects
        # Trigger Overheal effects
        # 触发过量治疗效果
        # Overheal triggers on the minion being healed
        # 过量治疗：当随从受到过量治疗时触发（只触发目标随从的效果）
        if overheal_amount > 0 and hasattr(target, 'overheal'):
             actions = target.get_actions("overheal")
             if actions:
                 # Pass overheal amount as event_args
                 source.game.trigger(target, actions, event_args={'amount': overheal_amount})


class ManaThisTurn(TargetedAction):
    """
    Give player targets \a amount Mana this turn.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        target.temp_mana += min(target.max_resources - target.mana, amount)
        source.game.manager.targeted_action(self, source, target, amount)


class Mill(TargetedAction):
    """
    Mill \a count cards from the top of the player targets' deck.
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def get_target_args(self, source, target):
        if target.deck:
            card = target.deck[-1]
        else:
            card = None
        return [card]

    def do(self, source, target, card):
        if card is None:
            return []
        source.game.manager.targeted_action(self, source, target, card)
        card.discard()
        self.broadcast(source, EventListener.ON, target, card, source)

        return [card]


class Morph(TargetedAction):
    """
    Morph minion target into \a minion id
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def get_target_args(self, source, target):
        card = _eval_card(source, self._args[1])
        assert len(card) == 1
        card = card[0]
        card.controller = target.controller
        return [card]

    def do(self, source, target, card):
        log_info("morphing", target=target, card=card)
        
        # 检查目标是否免疫变形（用于 REV_925 瓦丝琪女男爵）
        # 如果目标有 TRANSFORM_IMMUNE 标签，改为召唤新随从
        from . import enums
        if hasattr(target, 'tags') and target.tags.get(enums.TRANSFORM_IMMUNE, False):
            # 免疫变形：召唤新随从而不是变形
            log_info("transform_immune", target=target, card=card)
            # 召唤新随从
            source.game.queue_actions(source, [Summon(target.controller, card)])
            # 返回新召唤的随从
            return card
        
        target_zone = target.zone
        if card.zone != target_zone:
            # Transfer the zone position
            card._summon_index = target.zone_position
            # In-place morph is OK, eg. in the case of Lord Jaraxxus
            card.zone = target_zone
        target.clear_buffs()
        target.zone = Zone.SETASIDE
        target.morphed = card
        
        # 保存原随从信息到变形后的卡牌
        # 用于支持"恢复原随从"的效果（如 REV_828t 绑架的麻袋）
        card.morphed_from = target
        
        source.game.manager.targeted_action(self, source, target, card)
        return card


class FillMana(TargetedAction):
    """
    Refill \a amount mana crystals from player targets.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        target.used_mana = max(0, target.used_mana - amount)
        source.game.manager.targeted_action(self, source, target, amount)


class Retarget(TargetedAction):
    TARGET = ActionArg()
    CARD = CardArg()

    def do(self, source, target, new_target):
        if not new_target:
            return
        if isinstance(new_target, list):
            assert len(new_target) == 1
            new_target = new_target[0]
        if target.type in (CardType.HERO, CardType.MINION) and target.attacking:
            log_info("retargeting_attack", target=target, new_target=new_target)
            source.game.proposed_defender.defending = False
            source.game.proposed_defender = new_target
        else:
            log_info("retargeting_from_to", target=target, old_target=target.target, new_target=new_target)
            target.target = new_target
        source.game.manager.targeted_action(self, source, target, new_target)

        return new_target


class Reveal(TargetedAction):
    """
    Reveal secret targets.
    """

    def do(self, source, target):
        log_info("revealing", target=target)
        if target.zone == Zone.SECRET and target.data.secret:
            # 检查奥秘是否被保护（MAW_032 无语的证人）
            from .enums import CANT_BE_REVEALED
            if target.tags.get(CANT_BE_REVEALED, False):
                log_info("secret_protected", target=target)
                return  # 奥秘被保护，不能被揭示
            
            self.broadcast(source, EventListener.ON, target)
            target.zone = Zone.GRAVEYARD
            
            # 累加玩家的奥秘触发计数器
            # 用于支持 DMF_109（暗月先知塞格）等卡牌
            from .enums import NUM_SECRETS_REVEALED
            controller = target.controller
            controller.tags[NUM_SECRETS_REVEALED] = controller.tags.get(NUM_SECRETS_REVEALED, 0) + 1
            
            # 记录触发的奥秘ID（用于MIS_914量产泰迪等卡牌）
            if not hasattr(controller, 'triggered_secrets'):
                controller.triggered_secrets = []
            if target.id not in controller.triggered_secrets:
                controller.triggered_secrets.append(target.id)
            
        source.game.manager.targeted_action(self, source, target)


class SetCurrentHealth(TargetedAction):
    """
    Sets the current health of the character target to \a amount.
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        log_info("setting_health", target=target, amount=amount)
        maxhp = target.max_health
        target.damage = max(0, maxhp - amount)
        source.game.manager.targeted_action(self, source, target, amount)
        return target


class SetTags(TargetedAction):
    """
    Sets targets' given tags.
    """

    TARGET = ActionArg()
    TAGS = ActionArg()

    def do(self, source, target, tags):
        if isinstance(tags, dict):
            for tag, value in tags.items():
                target.tags[tag] = _eval_card(source, value)[0]
        else:
            for tag in tags:
                target.tags[tag] = True
        self.broadcast(source, EventListener.AFTER, target)


class UnsetTags(TargetedAction):
    """
    Unset targets' given tags.
    """

    TARGET = ActionArg()
    TAGS = ActionArg()

    def do(self, source, target, tags):
        for tag in tags:
            target.tags[tag] = False


class GetTag(TargetedAction):
    TARGET = ActionArg()
    TAG = ActionArg()

    def do(self, source, target, tag):
        return target.tags[tag]


class Silence(TargetedAction):
    """
    Silence minion targets.
    """

    def do(self, source, target):
        log_info("silencing", target=self)
        if target.type != CardType.MINION:
            return
        self.broadcast(source, EventListener.ON, target)
        target.clear_buffs()
        for attr in target.silenceable_attributes:
            if getattr(target, attr):
                setattr(target, attr, False)

        # Wipe the event listeners
        target._events = []
        target.silenced = True
        source.game.manager.targeted_action(self, source, target)


class ForgeCard(TargetedAction):
    """
    Forge a card in hand, spending 2 mana to upgrade it.
    锻造手牌中的卡牌，花费2点法力值来升级它。
    """

    TARGET = ActionArg()  # The card to forge

    def do(self, source, target):
        """
        Execute the forge action on a card.
        target: The card to be forged
        """
        if not hasattr(target, 'forge'):
            log_info("card_has_no_forge", card=target)
            return

        if not getattr(target, 'forge_active', False):
            log_info("forge_not_active", card=target)
            return

        if getattr(target, 'forged', False):
            log_info("already_forged", card=target)
            return

        # Check if player has enough mana (2 mana cost)
        if source.controller.mana < 2:
            log_info("not_enough_mana_to_forge", card=target)
            return

        # Spend 2 mana
        source.controller.used_mana += 2

        # Mark as forged
        target.forged = True
        target.forge_active = False

        log_info("forging_card", card=target)

        # Trigger the forge effect
        actions = target.data.scripts.get('forge', [])
        if actions:
            source.game.cheat_action(target, actions)

        # Check for card transformation (convention: ID + "t")
        token_id = target.id + "t"
        if token_id in cards.db:
            source.game.queue_actions(target, [Morph(target, token_id)])

        source.game.manager.targeted_action(self, source, target)
        self.broadcast(source, EventListener.ON, target)


class TitanAbility(TargetedAction):
    """
    Activate a Titan ability.
    """
    TARGET = ActionArg()  # The Titan Minion
    ABILITY_INDEX = IntArg()  # The ability index (1, 2, or 3)

    def do(self, source, target, ability_index):
        if not target.titan:
            log_info("target_is_not_titan", target=target)
            return

        if target.frozen:
            log_info("target_is_frozen", target=target)
            return
            
        # Check if already attacked/used ability this turn
        # Titans can only use 1 ability per turn replacing attack.
        # If num_attacks >= max_attacks (usually 1), can't use.
        # Note: Titans usually have "Charge" for abilities implicitly, so summoning sickness doesn't block abilities.
        # But if they attacked (Windfury?), they might be able to use ability?
        # Rule: "Each turn, you can choose one of their 3 abilities... instead of attacking."
        # If they attacked, they can't use ability.
        if target.num_attacks >= target.max_attacks:
             log_info("titan_exhausted", target=target)
             return

        from . import enums
        
        # Check if ability already used
        used_tag_name = f"TITAN_ABILITY_USED_{ability_index}"
        if not hasattr(enums, used_tag_name):
             log_info(f"Invalid ability index {ability_index}")
             return
             
        used_tag = getattr(enums, used_tag_name)
        if target.tags.get(used_tag):
            log_info(f"Ability {ability_index} already used")
            return

        # Execute Ability
        # Look for script "titan_ability_X"
        script_name = f"titan_ability_{ability_index}"
        actions = target.get_actions(script_name)
        
        if not actions:
             log_info(f"No actions for {script_name}")
             return
             
        log_info("activates_titan_ability", target=target, index=ability_index)

        # Mark used
        target.tags[used_tag] = True
        target.tags[enums.TITAN_ABILITY_USED] = target.tags.get(enums.TITAN_ABILITY_USED, 0) + 1
        
        # Consume Attack
        target.num_attacks += 1
        
        # Execute actions
        source.game.queue_actions(target, actions)
        
        source.game.manager.targeted_action(self, source, target, ability_index)
        self.broadcast(source, EventListener.ON, target, ability_index)


class Summon(TargetedAction):
    """
    Make player targets summon \a id onto their field.
    This works for equipping weapons as well as summoning minions.
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def _broadcast(self, entity, source, at, *args):
        # Prevent cards from triggering off their own summon
        if entity is args[1]:
            return
        return super()._broadcast(entity, source, at, *args)

    def get_summon_index(self, source_index):
        return source_index + 1

    def do(self, source, target, cards):
        log_info("summons", target=target, cards=cards)
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            if not card.is_summonable():
                continue
            if card.controller != target:
                card.controller = target
            # Poisoned Blade
            if (
                card.controller.weapon
                and card.controller.weapon.id == "AT_034"
                and source.type == CardType.HERO_POWER
                and card.type == CardType.WEAPON
            ):
                continue
            if card.zone != Zone.PLAY:
                if source.type == CardType.MINION:
                    if source.zone == Zone.PLAY:
                        source_index = source.controller.field.index(source)
                        card._summon_index = self.get_summon_index(source_index)
                    elif source.zone == Zone.GRAVEYARD:
                        card._summon_index = getattr(source, "_dead_position", None)
                        if card._summon_index is not None:
                            card._summon_index += cards.index(card)
                card.zone = Zone.PLAY
                # Initialize Spellburst state for minions with spellburst
                # 为带有法术迸发的随从初始化法术迸发状态
                if card.type == CardType.MINION and hasattr(card, 'spellburst'):
                    card.spellburst_active = True
                # Initialize Corrupt state for cards with corrupt
                # 为带有腐蚀属性的卡牌初始化腐蚀状态
                if hasattr(card, 'corrupt'):
                    card.corrupt_active = True
                # Initialize Frenzy state for minions with frenzy
                # 为带有狂怒的随从初始化狂怒状态
                if card.type == CardType.MINION and hasattr(card, 'frenzy'):
                    card.frenzy_active = True
                # Track battlecry minions for Brilliant Macaw
                # 追踪战吼随从（用于"艳丽的金刚鹦鹉"等卡牌）
                if card.type == CardType.MINION and hasattr(card, 'play') and callable(card.play):
                    card.controller.last_battlecry = card

                # Summon Colossal appendages
                # 召唤巨型随从的附属部件
                if card.type == CardType.MINION and hasattr(card, 'colossal_appendages'):
                    for appendage_id in card.colossal_appendages:
                        source.game.queue_actions(source, [Summon(target, appendage_id)])
            if card.type == CardType.MINION and Race.TOTEM in card.races:
                card.controller.times_totem_summoned_this_game += 1
            # 追踪野兽召唤（用于"霜刃豹头领"等卡牌）
            if card.type == CardType.MINION and Race.BEAST in card.races:
                if not hasattr(card.controller, 'beasts_summoned_this_game'):
                    card.controller.beasts_summoned_this_game = 0
                card.controller.beasts_summoned_this_game += 1
            source.game.manager.targeted_action(self, source, target, card)
            self.queue_broadcast(self, (source, EventListener.ON, target, card))
            self.broadcast(source, EventListener.AFTER, target, card)

        return cards


class SummonBothSides(Summon):
    TARGET = ActionArg()
    CARD = CardArg()

    def get_summon_index(self, source_index):
        return source_index + ((self.trigger_index + 1) % 2)


class SummonCustomMinion(TargetedAction):
    """
    Summon custom minion with cost/atk/max_health
    """

    TARGET = ActionArg()
    CARD = CardArg()
    COST = IntArg()
    ATK = IntArg()
    HEALTH = IntArg()

    def do(self, source, target, cards, cost, atk, health):
        if health <= 0:
            return
        if not isinstance(cards, list):
            cards = [cards]
        for card in cards:
            card.custom_card = True

            def create_custom_card(card):
                card.cost = cost
                card.atk = atk
                card.max_health = health

            card.create_custom_card = create_custom_card
            card.create_custom_card(card)

            if card.is_summonable():
                source.game.queue_actions(source, [Summon(target, card)])


class Shuffle(TargetedAction):
    """
    Shuffle card targets into player target's deck.
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def do(self, source, target, cards):
        log_info("shuffles_into_deck", cards=cards, target=target)
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            if card.controller != target:
                card.zone = Zone.SETASIDE
                card.controller = target
            if len(target.deck) >= target.max_deck_size:
                log_info("shuffle_fails_deck_full", card=card, target=target)
                continue
            card.zone = Zone.DECK
            target.shuffle_deck()
            
            # 追踪洗入对手牌库的瘟疫数量（用于 TTN_459 Chained Guardian）
            # 瘟疫 ID: TTN_450t, TTN_450t2, TTN_450t3
            if card.id in ("TTN_450t", "TTN_450t2", "TTN_450t3"):
                 # 如果 source.controller (洗入者) 和 target (被洗入者) 是对手关系
                 # 洗入者的 plaques_shuffled_into_enemy 计数 +1
                 # Shuffle 参数: source (引发者), target (牌库归属玩家), cards (被洗入卡牌)
                 # 通常 source 是打出的牌（归属 Controller），target 是 Opponent
                 if source.controller and source.controller != target:
                     if hasattr(source.controller, 'plagues_shuffled_into_enemy'):
                         source.controller.plagues_shuffled_into_enemy += 1
            
            source.game.manager.targeted_action(self, source, target, card)
            self.broadcast(source, EventListener.AFTER, target, card)


class Trade(TargetedAction):
    """
    Trade a card from hand: shuffle it into deck and draw a card.
    Used for Tradeable mechanic in United in Stormwind expansion.

    交易机制：将手牌中的卡牌洗回牌库，然后抽一张牌。
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def do(self, source, target, cards):
        """
        Execute the trade action.

        Args:
            source: The source entity triggering the trade
            target: The player performing the trade
            cards: The card(s) to trade
        """
        log_info("trades_card", cards=cards, target=target)
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            # 标记卡牌已被交易
            from .enums import TRADED_THIS_TURN
            card.tags[TRADED_THIS_TURN] = True

            # 触发交易前事件（用于某些卡牌的"交易后"效果）
            if hasattr(card, 'trade'):
                # 执行卡牌的 trade 效果
                actions = card.trade
                if actions:
                    source.game.queue_actions(source, [actions])

            # 将卡牌洗回牌库
            if card.zone == Zone.HAND:
                card.zone = Zone.DECK
                target.shuffle_deck()
                log_info("card_shuffled_into_deck", card=card, target=target)

            # 抽一张牌
            target.draw()

            # 广播交易事件
            source.game.manager.targeted_action(self, source, target, card)
            self.broadcast(source, EventListener.AFTER, target, card)


class ShuffleIntoDeck(TargetedAction):
    """
    Shuffle card(s) into player's deck at a specific position.
    Used for Azsharan mechanic in Voyage to the Sunken City expansion.

    将卡牌洗入牌库的指定位置（顶部或底部）。
    用于探寻沉没之城的艾萨拉（Azsharan）机制。
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def __init__(self, *args, position='random', **kwargs):
        """
        Args:
            position: 'top', 'bottom', or 'random' (default)
        """
        super().__init__(*args, **kwargs)
        self.position = position

    def do(self, source, target, cards):
        log_info("shuffles_into_deck_position", cards=cards, target=target, position=self.position)
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            if card.controller != target:
                card.zone = Zone.SETASIDE
                card.controller = target
            if len(target.deck) >= target.max_deck_size:
                log_info("shuffle_fails_deck_full", card=card, target=target)
                continue

            # 根据位置放置卡牌
            if self.position == 'bottom':
                # 放到牌库底部
                card.zone = Zone.DECK
                target.deck.append(card)
            elif self.position == 'top':
                # 放到牌库顶部
                card.zone = Zone.DECK
                target.deck.insert(0, card)
            else:
                # 随机洗入（默认行为）
                card.zone = Zone.DECK
                target.shuffle_deck()

            source.game.manager.targeted_action(self, source, target, card)
            self.broadcast(source, EventListener.AFTER, target, card)


class Dredge(TargetedAction):
    """
    Dredge: Look at the bottom 3 cards of your deck. Put one on top.
    Used in Voyage to the Sunken City expansion.

    疏浚：查看你牌库底部的3张牌，将其中一张置于牌库顶部。
    用于探寻沉没之城扩展包。
    """

    TARGET = ActionArg()

    def do(self, source, target):
        log_info("dredge", source=source, target=target)

        deck = target.deck
        if len(deck) < 1:
            return

        # 查看底部最多3张牌
        num_cards = min(3, len(deck))
        bottom_cards = deck[-num_cards:]

        # 在AI训练中，随机选择一张（或使用策略）
        # 实际游戏中应该让玩家选择
        import random
        chosen = random.choice(bottom_cards)

        # 将选中的牌移到顶部
        deck.remove(chosen)
        deck.insert(0, chosen)

        log_info("dredge_chosen", card=chosen, target=target)
        source.game.manager.targeted_action(self, source, target, chosen)
        self.broadcast(source, EventListener.AFTER, target, chosen)


class Swap(TargetedAction):
    TARGET = ActionArg()
    OTHER = ActionArg()

    def get_target_args(self, source, target):
        other = self.eval(self._args[1], source)
        if not other:
            return (None,)
        assert len(other) == 1
        return [other[0]]

    def clear_buff(self, target, old_zone):
        if old_zone == Zone.PLAY and target.zone not in (
            Zone.PLAY,
            Zone.GRAVEYARD,
            Zone.SETASIDE,
        ):
            if not target.keep_buff:
                target.clear_buffs()
            if target.id == target.controller.cthun.id:
                target.controller.copy_cthun_buff(target)

    def do(self, source, target, other):
        if other is not None:
            other._summon_index = target.zone_position - 1
            target._summon_index = other.zone_position - 1
            target_old_zone = target.zone
            other_old_zone = other.zone
            target.zone = Zone.SETASIDE
            other.zone = Zone.SETASIDE
            target.controller, other.controller = other.controller, target.controller
            target.zone = other_old_zone
            other.zone = target_old_zone
            self.clear_buff(target, target_old_zone)
            self.clear_buff(other, other_old_zone)
            source.game.manager.targeted_action(self, source, target, other)


class Steal(TargetedAction):
    """
    Make the controller take control of targets.
    The controller is the controller of the source of the action.
    """

    TARGET = ActionArg()
    CONTROLLER = ActionArg()

    def get_target_args(self, source, target):
        if len(self._args) > 1:
            # Controller was specified
            controller = self.eval(self._args[1], source)
            assert len(controller) == 1
            controller = controller[0]
        else:
            # Default to the source's controller
            controller = source.controller
        return [controller]

    def do(self, source, target, controller):
        log_info("takes_control", controller=controller, target=target)
        zone = target.zone
        target.zone = Zone.SETASIDE
        target.controller = controller
        target.turns_in_play = 0  # To ensure summoning sickness
        target.zone = zone
        source.game.manager.targeted_action(self, source, target, controller)


class UnlockOverload(TargetedAction):
    """
    Unlock the target player's overload, both current and owed.
    """

    def do(self, source, target):
        log_info("overload_cleared", target=target)
        target.overloaded = 0
        target.overload_locked = 0
        source.game.manager.targeted_action(self, source, target)


class SummonJadeGolem(TargetedAction):
    """
    Summons a Jade Golem for target player according to his Jade Golem Status
    """

    TARGET = ActionArg()
    CARD = CardArg()

    def get_target_args(self, source, target):
        jade_id = f"CFM_712_t{target.jade_golem:02d}"
        return _eval_card(source, jade_id)

    def do(self, source, target, card):
        log_info("summons_jade_golem", source=source, target=target)
        target.jade_golem = min(
            30, target.jade_golem + 1
        )  # Jade golem maximum of 30/30.
        if card.is_summonable():
            source.game.queue_actions(source, [Summon(target, card)])


class CastSpell(TargetedAction):
    """
    Cast a spell target random
    """

    SPELL = CardArg()
    SPELL_TARGET = CardArg()

    def get_target_args(self, source, target):
        ret = super().get_target_args(source, target)
        spell_target = [None]
        if ret:
            spell_target = ret[0]
        return [spell_target]

    def choose_target(self, source, card):
        return source.game.random.choice(card.targets)

    def do(self, source, card, targets):
        if source.type == CardType.MINION and (
            source.dead or source.silenced or source.zone != Zone.PLAY
        ):
            return

        player = source.controller
        old_choice = player.choice
        player.choice = None

        if card.twinspell:
            source.game.queue_actions(card, [Give(player, card.twinspell_copy)])
        if card.must_choose_one:
            card = source.game.random.choice(card.choose_cards)
        for target in targets:
            if card.requires_target() and not target:
                if len(card.targets) > 0:
                    if target not in card.targets:
                        target = self.choose_target(source, card)
                else:
                    log_info("spell_no_legal_target", source=source, card=card)
                    return
            card.target = target
            card.zone = Zone.PLAY
            log_info("cast_spell_target", source=source, card=card, target=target)
            source.game.manager.targeted_action(self, source, card, target)
            source.game.queue_actions(card, [Battlecry(card, card.target)])
            while player.choice:
                choice = source.game.random.choice(player.choice.cards)
                log_info("choosing_card", choice=choice)
                player.choice.choose(choice)
            while player.opponent.choice:
                choice = source.game.random.choice(player.opponent.choice.cards)
                log_info("choosing_card", choice=choice)
                player.opponent.choice.choose(choice)
            player.choice = old_choice

        # Trigger Spellburst effects
        for entity in player.live_entities:
            if not entity.ignore_scripts and hasattr(entity, 'spellburst_active'):
                if entity.spellburst_active:
                    actions = entity.get_actions("spellburst")
                    if actions:
                        # Pass the spell card as event_args so Spellburst effects can access it
                        source.game.trigger(entity, actions, event_args={'spell': card})
                        entity.spellburst_active = False
        
        # 追踪施放过的法术学派（用于"多系施法者"等卡牌）
        spell_school = card.tags.get(GameTag.SPELL_SCHOOL)
        if spell_school:
            player.spell_schools_played_this_game.add(spell_school)

            # 追踪冰霜法术数量（用于"熊人格拉希尔"等卡牌）
            if spell_school == enums.SpellSchool.FROST:
                player.frost_spells_cast += 1
        
        # 追踪每回合施放的法术（用于"首席法师安东尼达斯"等卡牌）
        current_turn = source.game.turn
        if current_turn not in player.spells_by_turn:
            player.spells_by_turn[current_turn] = []
        player.spells_by_turn[current_turn].append(card)
        
        # 追踪对友方随从施放的法术（用于"金翼鹦鹉"等卡牌）
        if hasattr(card, 'target') and card.target:
            target = card.target
            if (hasattr(target, 'type') and target.type == CardType.MINION and 
                hasattr(target, 'controller') and target.controller == player):
                player.last_spell_on_friendly_minion = card




class CastSpellTargetsEnemiesIfPossible(CastSpell):
    def choose_target(self, source, card):
        enemy_targets = []
        for entity in card.targets:
            if entity.controller == source.controller.opponent:
                enemy_targets.append(entity)
        if enemy_targets:
            return source.game.random.choice(enemy_targets)
        return source.game.random.choice(card.targets)


class CastSpellPreferSource(CastSpell):
    """
    Cast a spell, preferring to target the source minion if possible.
    Used by High Abbess Alura (SCH_141).
    """
    def choose_target(self, source, card):
        # If the source minion is a valid target, prefer it
        if source in card.targets:
            return source
        # Otherwise, choose randomly from available targets
        if card.targets:
            return source.game.random.choice(card.targets)
        return None


class DiscoverAndCastChoice(GenericChoice):
    """
    发现并施放的特殊选择
    选择后自动将卡牌施放到场上（不需要支付费用）
    """
    
    def __init__(self, player, cards, source):
        super().__init__(player, cards)
        self.source_card = source  # 保存触发源（如武器）
    
    def choose(self, card):
        """重写choose方法，在选择后自动施放卡牌"""
        # 先执行正常的选择逻辑（将卡牌放入手牌）
        super().choose(card)
        
        # 然后立即施放该卡牌
        if card.zone == Zone.HAND:
            if card.type == CardType.SPELL:
                # 如果是法术，施放到场上
                if card.secret:
                    # 奥秘直接放到场上
                    card.zone = Zone.PLAY
                else:
                    # 普通法术需要选择目标并施放
                    # 使用 CastSpell 动作来处理
                    if card.requires_target():
                        # 需要目标的法术，随机选择目标
                        if card.targets:
                            target = self.player.game.random.choice(card.targets)
                        else:
                            # 没有合法目标，法术失效
                            card.discard()
                            return
                    else:
                        target = None
                    
                    # 施放法术
                    CastSpell(card, target).trigger(self.source_card)


class DiscoverAndCastSecret(TargetedAction):
    """
    发现并施放奥秘（通用动作）
    
    功能：
    - 从指定的奥秘池中发现一张奥秘
    - 自动排除已在场的奥秘（避免重复）
    - 自动检查奥秘数量限制（最多5个）
    - 选择后自动施放（不需要支付费用）
    - 不经过手牌，直接从 SETASIDE 施放到场上
    
    用于：Rinling's Rifle 等卡牌
    """
    
    PLAYER = ActionArg()
    CARDS = ActionArg()  # 奥秘池（Selector）
    
    def get_target_args(self, source, target):
        # 获取奥秘池
        cards = self._args[1]
        if isinstance(cards, Selector):
            cards = cards.eval(source.game, source)
        elif callable(cards):
            cards = cards()
        return [cards]
    
    def do(self, source, player, cards):
        """执行发现并施放奥秘"""
        if not cards:
            return
        
        # 1. 过滤出未在场的奥秘（避免重复）
        active_secret_ids = {secret.id for secret in player.secrets}
        available_secrets = [
            c for c in cards 
            if c.id not in active_secret_ids
        ]
        
        # 2. 如果没有可用的奥秘，直接返回
        if not available_secrets:
            log_info("no_unique_secrets_available", player=player)
            return
        
        # 3. 检查奥秘数量限制
        if len(player.secrets) >= 5:
            log_info("secret_zone_full", player=player)
            return
        
        # 4. 从可用奥秘中随机选择3张（或更少）
        import random
        if len(available_secrets) > 3:
            choices = random.sample(available_secrets, 3)
        else:
            choices = available_secrets
        
        # 5. 创建发现选择
        choice_cards = [player.card(c.id if hasattr(c, 'id') else c, source=source) for c in choices]
        
        # 6. 使用自定义的 Choice 类，不经过手牌直接施放
        choice = DiscoverSecretChoice(player, choice_cards)
        choice.trigger(source)


class DiscoverSecretChoice(Choice):
    """
    发现奥秘的特殊选择
    选择后直接施放到场上，不经过手牌
    """
    
    def choose(self, card):
        """选择奥秘并直接施放"""
        # 调用父类的 choose 来处理基本逻辑（清除选择状态等）
        super().choose(card)
        
        # 将选中的卡牌直接施放到场上
        # 其他未选中的卡牌丢弃
        for _card in self.cards:
            if _card is card:
                # 选中的卡牌：直接施放到场上
                _card.zone = Zone.PLAY
            else:
                # 未选中的卡牌：丢弃
                _card.discard()


class Evolve(TargetedAction):
    """
    Transform your minions into random minions that cost (\a amount) more
    """

    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        cost = target.cost + amount
        card_set = RandomMinion(cost=cost).find_cards(source)
        if card_set:
            card = source.game.random.choice(card_set)
            return source.game.queue_actions(source, [Morph(target, card)])[0]


class ExtraAttack(TargetedAction):
    """
    Get target an extra attack change
    """

    TARGET = ActionArg()

    def do(self, source, target):
        log_info("extra_attack_change", target=target)
        target.num_attacks -= 1
        source.game.manager.targeted_action(self, source, target)


class SwapStateBuff(TargetedAction):
    """
    Swap stats between two minions using \a buff.
    """

    TARGET = ActionArg()
    OTHER = ActionArg()
    BUFF = ActionArg()

    def do(self, source, target, other, buff):
        log_info("swap_state", target=target, other=other)
        if not target or not other:
            return
        other = other[0]
        buff1 = source.controller.card(buff, source=source)
        buff1.source = source
        buff1._xcost = other.cost
        if other.type == CardType.MINION:
            buff1._xatk = other.atk
            buff1._xhealth = other.health
        buff2 = source.controller.card(buff, source=source)
        buff2.source = source
        buff2._xcost = target.cost
        if target.type == CardType.MINION:
            buff2._xatk = target.atk
            buff2._xhealth = target.health
        buff1.apply(target)
        buff2.apply(other)
        source.game.manager.targeted_action(self, source, target, other, buff)


class CopyStateBuff(TargetedAction):
    """
    Copy target state, buff on self
    """

    TARGET = ActionArg()
    OTHER = ActionArg()
    BUFF = ActionArg()

    def do(self, source, target, buff):
        target = target
        buff = source.controller.card(buff, source=source)
        buff.source = source
        buff._xatk = target.atk
        buff._xhealth = target.health
        buff.apply(source)
        source.game.manager.targeted_action(self, source, target, buff)


class SetStateBuff(TargetedAction):
    """
    Set target state, buff on self
    """

    TARGET = ActionArg()
    OTHER = ActionArg()
    BUFF = ActionArg()

    def do(self, source, target, buff):
        target = target
        buff = source.controller.card(buff, source=source)
        buff.source = source
        buff._xatk = source.atk
        buff._xhealth = source.health
        buff.apply(target)
        source.game.manager.targeted_action(self, source, target, buff)


class RefreshHeroPower(TargetedAction):
    """
    Helper to Refresh Hero Power
    """

    HEROPOWER = ActionArg()

    def do(self, source, heropower):
        log_info("refresh_hero_power", heropower=heropower)
        if heropower.heropower_disabled:
            return
        if not heropower.exhausted:
            return
        heropower.additional_activations_this_turn += 1
        source.game.manager.targeted_action(self, source, heropower)


class MultipleChoice(TargetedAction):
    PLAYER = ActionArg()
    choose_times = 2

    def do(self, source, player):
        self.player = player
        self.source = source
        self.min_count = 1
        self.max_count = 1
        self.choosed_cards = []
        self.player.choice = self
        self._callback = self.callback
        self.callback = []
        getattr(self, "do_step1")()
        source.game.manager.targeted_action(self, source, player)

    def choose(self, card):
        if card not in self.cards:
            raise InvalidAction(
                "%r is not a valid choice (one of %r)" % (card, self.cards)
            )
        else:
            self.choosed_cards.append(card)
            lens = len(self.choosed_cards)
            if lens < self.choose_times:
                getattr(self, f"do_step{lens+1}")()
            else:
                self.player.choice = None
                self.done()
                self.callback = self._callback
                self.trigger_choice_callback()


class GameStart(GameAction):
    """
    Setup game
    """

    def do(self, source):
        log_info("game_start")
        source.game.manager.game_action(self, source)
        self.broadcast(source, EventListener.ON)


class Adapt(TargetedAction):
    """
    Adapt target
    """

    TARGET = ActionArg()
    CARDS = CardArg()
    CARD = CardArg()

    def get_target_args(self, source, target):
        choices = [
            "UNG_999t10",
            "UNG_999t2",
            "UNG_999t3",
            "UNG_999t4",
            "UNG_999t5",
            "UNG_999t6",
            "UNG_999t7",
            "UNG_999t8",
            "UNG_999t13",
            "UNG_999t14",
        ]
        cards = source.game.random.sample(choices, 3)
        cards = [source.controller.card(card, source=source) for card in cards]
        return [cards]

    def do(self, source, target, cards):
        log_info("adapts", source=source, cards=cards, target=target)
        self.cards = cards
        player = source.controller
        player.choice = self
        self.player = player
        self.source = source
        self.target = target
        self.cards = cards
        self.min_count = 1
        self.max_count = 1
        source.game.manager.targeted_action(self, source, target, cards)

    def choose(self, card):
        if card not in self.cards:
            raise InvalidAction(
                "%r is not a valid choice (one of %r)" % (card, self.cards)
            )
        self.player.choice = None
        self.source.game.trigger(self.source, (Battlecry(card, self.target),), None)
        self.trigger_choice_callback()


class AddProgress(TargetedAction):
    """
    Add Progress for target, such as quest card and upgradeable card
    """

    TARGET = ActionArg()
    CARD = CardArg()
    AMOUNT = IntArg()

    def do(self, source, target, card, amount=1):
        log_info("add_progress", target=target, card=card)
        if not target:
            return
        target.add_progress(card, amount)
        source.game.manager.targeted_action(self, source, target, card, amount)
        if target.progress >= target.progress_total:
            source.game.trigger(target, target.get_actions("reward"), event_args=None)
            if target.data.quest or target.data.sidequest:
                target.zone = Zone.GRAVEYARD


class ClearProgress(TargetedAction):
    """
    Clear Progress for target
    """

    def do(self, source, target):
        log_info("clear_progress", target=target)
        target.clear_progress()
        source.game.manager.targeted_action(self, source, target)


class LosesDivineShield(TargetedAction):
    """
    Losses Divine Shield
    """

    def do(self, source, target):
        target.divine_shield = False
        source.game.manager.targeted_action(self, source, target)
        self.broadcast(source, EventListener.AFTER, target)


class Remove(TargetedAction):
    """
    Remove character targets
    """

    def do(self, source, target):
        target.zone = Zone.REMOVEDFROMGAME
        source.game.manager.targeted_action(self, source, target)


class Replay(TargetedAction):
    """
    Cast it if it's spell, otherwise summon it (minion, weapon, hero).
    Now only for Tess Greymane (GIL_598)
    """

    def do(self, source, target):
        source.game.manager.targeted_action(self, source, target)
        if target.type == CardType.SPELL:
            source.game.queue_actions(source, [CastSpell(target)])
        else:
            source.game.queue_actions(source, [Summon(source.controller, target)])


class Invoke(TargetedAction):
    def do(self, source, galakrond):
        source.game.manager.targeted_action(self, source, galakrond)
        source.controller.invoke_counter += 1
        if galakrond is not None:
            source.game.queue_actions(
                source,
                [
                    Reveal(galakrond),
                    PlayHeroPower(galakrond.data.hero_power, None),
                    AddProgress(galakrond, source),
                ],
            )


class Awaken(TargetedAction):
    def do(self, source, target):
        if not target.dormant:
            return
        target.dormant = False
        target.turns_in_play = 0
        source.game.manager.targeted_action(self, source, target)
        actions = target.get_actions("awaken")
        if actions:
            source.game.trigger(target, actions, event_args=None)


class Dormant(TargetedAction):
    TARGET = ActionArg()
    AMOUNT = IntArg()

    def do(self, source, target, amount):
        target.dormant = True
        target.dormant_turns += amount
        source.game.manager.targeted_action(self, source, target, amount)


class RotateMinions(GameAction):
    """
    Rotate all minions relative to the caster's perspective.
    
    Counterclockwise (False):
    - Caster's minions: move right
    - Opponent's minions: move left
    
    Clockwise (True):
    - Caster's minions: move left
    - Opponent's minions: move right
    """
    DIRECTION = ActionArg()
    
    def do(self, source, direction):
        """
        Example (counterclockwise):
        Caster: [A][B][C]  Opponent: [D][E]
        After: Caster: [D][A][B]  Opponent: [E][C]
        """
        caster = source.controller
        opponent = source.controller.opponent
        
        caster_minions = list(caster.field)
        opponent_minions = list(opponent.field)
        
        if not caster_minions and not opponent_minions:
            return
        
        if not direction:  # Counterclockwise
            new_caster = []
            new_opponent = []
            
            if opponent_minions:
                new_caster.append(opponent_minions[0])
                new_opponent = opponent_minions[1:]
            
            new_caster.extend(caster_minions[:-1] if caster_minions else [])
            
            if caster_minions:
                new_opponent.append(caster_minions[-1])
                
        else:  # Clockwise
            new_caster = []
            new_opponent = []
            
            if caster_minions:
                new_caster = caster_minions[1:]
            
            if opponent_minions:
                new_caster.append(opponent_minions[-1])
                new_opponent = opponent_minions[:-1]
            
            if caster_minions:
                new_opponent.insert(0, caster_minions[0])
        
        for minion in caster_minions + opponent_minions:
            minion.zone = Zone.SETASIDE
        
        for i, minion in enumerate(new_caster):
            minion.controller = caster
            minion.zone = Zone.PLAY
            minion._summon_index = i
            minion.turns_in_play = 0
        
        for i, minion in enumerate(new_opponent):
            minion.controller = opponent
            minion.zone = Zone.PLAY
            minion._summon_index = i
            minion.turns_in_play = 0
        
        source.game.refresh_auras()
        source.game.manager.game_action(self, source, direction)


# ========================================
# Questline（任务线）机制 - 暴风城（2021年8月）
# ========================================

class QuestlineProgress(GameAction):
    """
    任务线进度增加
    
    当满足任务线条件时，增加进度
    达到目标后自动升级到下一阶段
    """
    QUEST = CardArg()
    AMOUNT = IntArg()
    
    def do(self, source, quest, amount=1):
        """
        增加任务线进度
        
        Args:
            quest: 任务线卡牌
            amount: 增加的进度量（默认1）
        """
        from .enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        # 获取当前阶段和进度
        current_stage = quest.tags.get(QUESTLINE_STAGE, 1)
        current_progress = quest.tags.get(QUESTLINE_PROGRESS, 0)
        
        # 增加进度
        new_progress = current_progress + amount
        quest.tags[QUESTLINE_PROGRESS] = new_progress
        
        # 检查是否完成当前阶段
        # 每个任务线都有自己的目标值，存储在 questline_requirements 属性中
        if hasattr(quest, 'questline_requirements'):
            requirements = quest.questline_requirements
            if current_stage <= len(requirements):
                target = requirements[current_stage - 1]
                
                if new_progress >= target:
                    # 完成当前阶段，升级到下一阶段
                    source.game.queue_actions(quest, [QuestlineAdvance(quest)])


class QuestlineAdvance(GameAction):
    """
    任务线升级到下一阶段
    
    完成当前阶段后：
    1. 给予奖励
    2. 升级到下一阶段（如果还有）
    3. 重置进度
    """
    QUEST = CardArg()
    
    def do(self, source, quest):
        """
        升级任务线到下一阶段
        
        Args:
            quest: 任务线卡牌
        """
        from .enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        # 获取当前阶段
        current_stage = quest.tags.get(QUESTLINE_STAGE, 1)
        
        # 触发当前阶段的奖励
        reward_action_name = f"questline_reward_{current_stage}"
        if hasattr(quest, reward_action_name):
            reward_actions = getattr(quest, reward_action_name)
            if callable(reward_actions):
                reward_actions = reward_actions(quest)
            source.game.queue_actions(quest, reward_actions)
        
        # 检查是否还有下一阶段
        if hasattr(quest, 'questline_requirements'):
            max_stages = len(quest.questline_requirements)
            
            if current_stage < max_stages:
                # 升级到下一阶段
                quest.tags[QUESTLINE_STAGE] = current_stage + 1
                quest.tags[QUESTLINE_PROGRESS] = 0
                
                log_info(f"Questline {quest} advanced to stage {current_stage + 1}")
            else:
                # 已完成所有阶段，移除任务线
                log_info(f"Questline {quest} completed all stages!")
                quest.destroy()

class ReplaceHero(TargetedAction):
	"""
	Replace a player's hero with a new hero card.
	Preserves health, armor, and other important stats.
	用新的英雄卡牌替换玩家的英雄。
	保留生命值、护甲和其他重要属性。
	"""
	
	TARGET = ActionArg()
	CARD = CardArg()
	
	def do(self, source, target, cards):
		"""
		Replace target player's hero with the specified hero card
		
		Args:
			source: The source of this action
			target: The player whose hero to replace
			cards: The new hero card(s) to use
		"""
		log_info("replace_hero", target=target, cards=cards)
		
		if not isinstance(cards, list):
			cards = [cards]
		
		for card in cards:
			if card.type != CardType.HERO:
				log_info(f"Cannot replace hero with non-hero card: {card}")
				continue
			
			old_hero = target.hero
			
			# Create the new hero
			if isinstance(card, str):
				new_hero = target.card(card, source=source)
			else:
				new_hero = card
			
			# Preserve important stats from old hero
			new_hero.controller = target
			new_hero.zone = Zone.PLAY
			
			# Preserve health and armor
			current_health = old_hero.health
			current_armor = old_hero.armor
			max_health = new_hero.max_health
			
			# Set health (don't exceed new max health)
			new_hero.health = min(current_health, max_health)
			new_hero.armor = current_armor
			
			# Preserve attack if hero had a weapon
			if old_hero.atk > 0 and not target.weapon:
				new_hero.atk = old_hero.atk
			
			# Preserve damage taken
			damage_taken = old_hero.max_health - current_health
			if damage_taken > 0:
				new_hero.damage = min(damage_taken, new_hero.max_health)
			
			# Replace the hero
			old_hero.zone = Zone.GRAVEYARD
			target.hero = new_hero
			
			# Handle hero power
			if hasattr(new_hero, 'power') and new_hero.power:
				# Create the new hero power
				if isinstance(new_hero.power, str):
					power_card = target.card(new_hero.power, source=new_hero)
				else:
					power_card = new_hero.power
				
				# Remove old hero power
				if old_hero.power:
					old_hero.power.zone = Zone.GRAVEYARD
				
				# Set new hero power
				power_card.controller = target
				power_card.zone = Zone.PLAY
				new_hero.power = power_card
			
			log_info(f"Hero replaced: {old_hero} -> {new_hero}")
			
			# Broadcast the hero replacement event
			source.game.manager.targeted_action(self, source, target, new_hero)
			self.broadcast(source, EventListener.AFTER, target, new_hero)
		
		return cards


class Excavate(GameAction):
    """
    Excavate a treasure.
    """
    PLAYER = ActionArg()
    
    def do(self, source, controller):
        from fireplace.cards.badlands.excavate import TIER_1_IDS, TIER_2_IDS, TIER_3_IDS, TIER_4_IDS
        
        # Broadcast ON event (before excavate)
        source.game.manager.game_action(self, source, controller)
        self.broadcast(source, EventListener.ON, controller)
        
        # Increment total excavates
        controller.times_excavated += 1
        
        current_stage = controller.excavate_tier
        
        reward_tier_int = 0
        next_stage = 0
        
        if current_stage == 0:
            reward_tier_int = 1
            next_stage = 1
        elif current_stage == 1:
            reward_tier_int = 2
            next_stage = 2
        elif current_stage == 2:
            reward_tier_int = 3
            next_stage = 3
        elif current_stage == 3:
            # Check for Tier 4 eligibility
            has_tier_4 = controller.hero.card_class in TIER_4_IDS
            if has_tier_4:
                reward_tier_int = 4
                next_stage = 0
            else:
                reward_tier_int = 1
                next_stage = 1
        
        controller.excavate_tier = next_stage
        
        # Select Card
        card_id = None
        if reward_tier_int == 1:
            card_id = source.game.random.choice(TIER_1_IDS)
        elif reward_tier_int == 2:
            card_id = source.game.random.choice(TIER_2_IDS)
        elif reward_tier_int == 3:
            card_id = source.game.random.choice(TIER_3_IDS)
        elif reward_tier_int == 4:
            card_id = TIER_4_IDS.get(controller.hero.card_class)
            
        if card_id:
             source.game.add_card(controller, card_id, source=source)
        
        # Broadcast AFTER event (after excavate)
        self.broadcast(source, EventListener.AFTER, controller)


class SplitCard(GameAction):
    """
    Split a card into two halves.
    将一张卡牌拆分成两半（用于 Mes'Adune the Fractured 等卡牌）

    拆分规则：
    - 偶数属性：均分（如 4 → 2 + 2）
    - 奇数属性：随机不均等拆分（如 5 → 3 + 2 或 2 + 3）
    - Cost/Attack 为 1：拆分为 0 + 1
    - Health 为 1：拆分为 1 + 1（特殊规则，避免随从立即死亡）
    - 保留原卡的所有效果（战吼、光环等）
    """
    CARD = ActionArg()

    def do(self, source, card):
        """
        拆分一张卡牌

        Args:
            source: 触发拆分的来源
            card: 要拆分的卡牌

        Returns:
            tuple: (half1, half2) 两张拆分后的卡牌
        """
        import random

        if card.type != CardType.MINION:
            # 只能拆分随从卡牌
            return None, None

        # 获取原始属性
        original_cost = card.cost
        original_atk = card.atk
        original_health = card.health

        # Cost 拆分
        if original_cost == 1:
            cost1, cost2 = 0, 1
        else:
            half_cost = original_cost // 2
            if original_cost % 2 == 1:  # 奇数
                if random.random() < 0.5:
                    cost1, cost2 = half_cost + 1, half_cost
                else:
                    cost1, cost2 = half_cost, half_cost + 1
            else:  # 偶数
                cost1 = cost2 = half_cost

        # Attack 拆分
        if original_atk == 1:
            atk1, atk2 = 0, 1
        else:
            half_atk = original_atk // 2
            if original_atk % 2 == 1:  # 奇数
                if random.random() < 0.5:
                    atk1, atk2 = half_atk + 1, half_atk
                else:
                    atk1, atk2 = half_atk, half_atk + 1
            else:  # 偶数
                atk1 = atk2 = half_atk

        # Health 拆分（特殊规则：1 拆分为 1 + 1）
        if original_health == 1:
            health1, health2 = 1, 1
        else:
            half_health = original_health // 2
            if original_health % 2 == 1:  # 奇数
                if random.random() < 0.5:
                    health1, health2 = half_health + 1, half_health
                else:
                    health1, health2 = half_health, half_health + 1
            else:  # 偶数
                health1 = health2 = half_health

        # 创建两张"一半"的牌（保留原卡 ID 和所有效果）
        controller = card.controller
        half1 = controller.card(card.id, source=controller)
        half1.cost = max(0, cost1)
        half1.atk = atk1
        half1.health = max(1, health1)

        half2 = controller.card(card.id, source=controller)
        half2.cost = max(0, cost2)
        half2.atk = atk2
        half2.health = max(1, health2)

        return half1, half2

