from .i18n import _ as translate
import time
from random import Random
from calendar import timegm
from itertools import chain
import copy
from typing import TYPE_CHECKING

from hearthstone.enums import BlockType, CardType, PlayState, State, Step, Zone

from .actions import (
    Attack,
    Awaken,
    BeginTurn,
    Death,
    EndTurn,
    EventListener,
    GameStart,
    Play,
)
from .card import THE_COIN
from .cards import standard_board_skins
from .enums import BoardEnum
from .entity import Entity
from .exceptions import GameOver, InfiniteLoopDetected
from .managers import GameManager
from .utils import CardList


if TYPE_CHECKING:
    from .actions import Action
    from .card import Character, PlayableCard
    from .player import Player


class BaseGame(Entity):
    type = CardType.GAME
    MAX_MINIONS_ON_FIELD = 7
    MAX_SECRETS_ON_PLAY = 5
    Manager = GameManager

    def __init__(self, players: "list[Player]", seed=None):
        self.random = Random(seed)
        self.player1: Player
        self.player2: Player
        self.data = None
        self.players = players
        super().__init__()
        for player in players:
            player.game = self
        self.state = State.INVALID
        self.step = Step.BEGIN_FIRST
        self.next_step = Step.BEGIN_SHUFFLE
        self.turn = 0
        self.current_player: Player = None
        self.next_players: list[Player] = []
        self.tick = 0
        self.active_aura_buffs = CardList()
        self.setaside = CardList()
        self._action_stack = 0

        # Anomaly 系统（用于古加尔等卡牌）- 泰坦诸神（2023年8月）
        self.active_anomaly = None  # 当前激活的畸变效果

        # Rewind Mechanism Snapshot Storage
        self.rewind_snapshot = None
        
        # 游戏历史记录系统（用于调试）
        # 记录卡牌使用和效果触发，类似炉石官方左侧的历史记录
        self.action_history = []  # [(turn, action_type, source_id, source_name, target_id, target_name, extra_info)]
        self.action_history_enabled = True  # 可以关闭以提升性能
        self.action_history_max_size = 200  # 最大记录数，防止内存溢出
        
        # 无限循环检测机制
        self._action_counter = 0  # 当前回合的操作计数
        self._max_actions_per_turn = 1000  # 单回合最大操作数，超过则认为是无限循环

    def __repr__(self):
        return "%s(players=%r)" % (self.__class__.__name__, self.players)

    def __iter__(self):
        return chain(
            self.entities, self.hands, self.decks, self.graveyard, self.setaside
        )

    @property
    def game(self):
        return self

    @property
    def is_standard(self):
        return self.player1.is_standard and self.player2.is_standard

    @property
    def board(self):
        ret = CardList(chain(self.players[0].field, self.players[1].field))
        ret.sort(key=lambda e: e.play_counter)
        return ret

    @property
    def decks(self):
        return CardList(chain(self.players[0].deck, self.players[1].deck))

    @property
    def hands(self):
        return CardList(chain(self.players[0].hand, self.players[1].hand))

    @property
    def characters(self):
        ret = CardList(chain(self.players[0].characters, self.players[1].characters))
        ret.sort(key=lambda e: e.play_counter)
        return ret

    @property
    def graveyard(self):
        return CardList(chain(self.players[0].graveyard, self.players[1].graveyard))

    @property
    def entities(self):
        ret = CardList(
            chain([self], self.players[0].entities, self.players[1].entities)
        )
        ret.sort(key=lambda e: e.play_counter)
        return ret

    @property
    def live_entities(self):
        ret = CardList(
            chain(self.players[0].live_entities, self.players[1].live_entities)
        )
        ret.sort(key=lambda e: e.play_counter)
        return ret

    @property
    def minions_killed_this_turn(self):
        return (
            self.players[0].minions_killed_this_turn
            + self.players[1].minions_killed_this_turn
        )

    @property
    def ended(self):
        return self.state == State.COMPLETE
    
    def log_action(self, action_type: str, source=None, target=None, extra_info: str = ""):
        """
        记录游戏操作到历史记录中
        用于调试无限循环和追踪卡牌效果触发
        """
        if not self.action_history_enabled:
            return
        
        # 获取源和目标的信息
        source_id = getattr(source, 'id', None) if source else None
        source_name = str(source) if source else None
        target_id = getattr(target, 'id', None) if target else None
        target_name = str(target) if target else None
        
        # 记录到历史
        entry = (
            self.turn,
            action_type,
            source_id,
            source_name,
            target_id,
            target_name,
            extra_info
        )
        self.action_history.append(entry)
        
        # 限制历史大小
        if len(self.action_history) > self.action_history_max_size:
            self.action_history = self.action_history[-self.action_history_max_size:]
    
    def get_recent_history(self, count: int = 30) -> list:
        """获取最近的操作历史记录"""
        return self.action_history[-count:]
    
    def print_recent_history(self, count: int = 30):
        """打印最近的操作历史记录（用于调试）"""
        print(f"\n{'='*60}")
        print(f"最近 {count} 条游戏操作历史:")
        print(f"{'='*60}")
        for entry in self.get_recent_history(count):
            turn, action_type, source_id, source_name, target_id, target_name, extra = entry
            target_str = f" -> {target_name}({target_id})" if target_id else ""
            extra_str = f" [{extra}]" if extra else ""
            print(f"[回合{turn}] {action_type}: {source_name}({source_id}){target_str}{extra_str}")
        print(f"{'='*60}\n")

    def action_start(self, type, source, index, target):
        self.manager.action_start(type, source, index, target)
        if type != BlockType.PLAY:
            self._action_stack += 1
        
        # 无限循环检测
        self._action_counter += 1
        
        if self._action_counter > self._max_actions_per_turn:
            # 生成详细的调试报告
            import sys
            import os
            from datetime import datetime
            
            # 创建日志目录
            log_dir = "test_logs/infinite_loop_debug"
            os.makedirs(log_dir, exist_ok=True)
            
            # 生成日志文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"infinite_loop_turn{self.turn}_{timestamp}.txt")
            
            # 收集详细信息
            debug_info = []
            debug_info.append("="*80)
            debug_info.append("INFINITE LOOP DETECTED")
            debug_info.append("="*80)
            debug_info.append(f"Turn: {self.turn}")
            debug_info.append(f"Action count: {self._action_counter}")
            debug_info.append(f"Last trigger source: {source} (ID: {getattr(source, 'id', 'N/A')})")
            debug_info.append(f"Current player: {self.current_player}")
            debug_info.append("")
            
            # 记录场上所有卡牌
            debug_info.append("="*80)
            debug_info.append("BOARD STATE")
            debug_info.append("="*80)
            for player in self.players:
                debug_info.append(f"\n{player.name}'s field:")
                for minion in player.field:
                    debug_info.append(f"  - {minion} (ID: {minion.id}, HP: {minion.health}/{minion.max_health}, dead: {minion.dead})")
                    # 检查是否有亡语
                    if hasattr(minion, 'deathrattle') and minion.deathrattle:
                        debug_info.append(f"    [DEATHRATTLE: {minion.deathrattle}]")
                    # 检查是否有触发器
                    if hasattr(minion, '_events') and minion._events:
                        debug_info.append(f"    [EVENTS: {len(minion._events)} registered]")
            
            # 记录最近的操作历史
            debug_info.append("\n" + "="*80)
            debug_info.append("RECENT ACTION HISTORY (last 100)")
            debug_info.append("="*80)
            for entry in self.get_recent_history(100):
                turn, action_type, source_id, source_name, target_id, target_name, extra = entry
                target_str = f" -> {target_name}({target_id})" if target_id else ""
                extra_str = f" [{extra}]" if extra else ""
                debug_info.append(f"[Turn{turn}] {action_type}: {source_name}({source_id}){target_str}{extra_str}")
            
            debug_info.append("\n" + "="*80)
            
            # 写入文件
            report = "\n".join(debug_info)
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"\n[!] Infinite loop debug report saved to: {log_file}", file=sys.stderr)
            except Exception as e:
                print(f"\n[!] Failed to save debug report: {e}", file=sys.stderr)
            
            # 也打印到 stderr（简短版本）
            print(f"\n{'!'*60}", file=sys.stderr)
            print(f"[WARNING] Detected possible infinite loop!", file=sys.stderr)
            print(f"Turn: {self.turn}, Actions: {self._action_counter}", file=sys.stderr)
            print(f"Source: {source} (ID: {getattr(source, 'id', 'N/A')})", file=sys.stderr)
            print(f"Debug report: {log_file}", file=sys.stderr)
            print(f"{'!'*60}\n", file=sys.stderr)
            
            raise InfiniteLoopDetected(
                f"Turn {self.turn} exceeded {self._max_actions_per_turn} actions, possible infinite loop. "
                f"Last action source: {source}. Debug report: {log_file}"
            )

    def action_end(self, type, source):
        self.manager.action_end(type, source)

        if self.ended:
            raise GameOver("The game has ended.")

        if type != BlockType.PLAY:
            self._action_stack -= 1
        if not self._action_stack:
            self.log(translate("empty_stack"))
            self.refresh_auras()
            self.process_deaths()
            self.check_for_end_game()  # 检查游戏是否应该结束
            # check_for_end_game 可能已经抛出异常，但如果没有，再次检查
            if self.ended:
                raise GameOver("The game has ended.")

    def action_block(
        self, source, actions, type, index=-1, target=None, event_args=None
    ):
        self.action_start(type, source, index, target)
        if actions:
            ret = self.queue_actions(source, actions, event_args)
        else:
            ret = []
        self.action_end(type, source)
        return ret

    def attack(self, source, target):
        type = BlockType.ATTACK
        actions = [Attack(source, target)]
        self.log_action("ATTACK", source, target)
        result = self.action_block(source, actions, type, target=target)
        if self.state != State.COMPLETE:
            self.manager.step(Step.MAIN_ACTION, Step.MAIN_END)
        return result

    def joust(self, source, challenger, defender, actions):
        type = BlockType.JOUST
        return self.action_block(
            source, actions, type, event_args=[challenger, defender]
        )

    def main_power(self, source, actions, target):
        type = BlockType.POWER
        return self.action_block(source, actions, type, target=target)

    def play_card(
        self,
        card: "PlayableCard",
        target: "Character",
        index: int,
        choose: "PlayableCard | str",
    ):
        type = BlockType.PLAY
        player = card.controller
        self.log_action("PLAY_CARD", card, target, f"cost={getattr(card, 'cost', '?')}")
        actions = [Play(card, target, index, choose)]
        return self.action_block(player, actions, type, index, target)

    def process_deaths(self):
        type = BlockType.DEATHS

        # 只处理在 PLAY 区域且标记为 dead 的卡牌
        # 过滤掉已经在墓地或其他区域的卡牌，防止无限循环
        dead_cards = [card for card in self.live_entities if card.dead and card.zone == Zone.PLAY]
        
        if dead_cards:
            self.action_start(type, self, 0, None)
            self.trigger(self, [Death(dead_cards)], event_args=None)
            self.action_end(type, self)

    def trigger(self, source, actions, event_args):
        """
        Perform actions as a result of an event listener (TRIGGER)
        """
        block_type = BlockType.TRIGGER
        # 记录触发的事件
        if actions and self.action_history_enabled:
            # 确保 actions 是 list 以支持切片操作
            actions_list = list(actions) if not isinstance(actions, list) else actions
            action_names = ", ".join(a.__class__.__name__ for a in actions_list[:3])
            if len(actions_list) > 3:
                action_names += f"... (+{len(actions_list)-3} more)"
            self.log_action("TRIGGER", source, extra_info=action_names)
            # 使用转换后的 list
            actions = actions_list
        return self.action_block(source, actions, block_type, event_args=event_args)

    def cheat_action(self, source, actions):
        """
        Perform actions as if a card had just triggered them
        """
        return self.trigger(source, actions, event_args=None)

    def check_for_end_game(self):
        """
        Check if one or more player is currently losing.
        End the game if they are.
        """
        gameover = False
        for player in self.players:
            # 检查英雄生命值和区域
            if player.hero:
                # 如果英雄生命值 <= 0 或已在墓地，设置为 LOSING
                if player.hero.health <= 0 or player.hero.zone == Zone.GRAVEYARD:
                    if player.playstate not in (PlayState.LOSING, PlayState.LOST):
                        # 特殊处理：如果英雄有亡语（如 TIME_618 永时收割者哈斯克）
                        # 则不立即设置 LOSING 状态，而是标记为 to_be_destroyed
                        # 让 process_deaths() 来处理，这样亡语可以先触发
                        # 如果亡语复活了英雄（health > 0），则游戏继续
                        if player.hero.health <= 0 and player.hero.has_deathrattle and player.hero.zone == Zone.PLAY:
                            # 标记英雄为待销毁，但不立即设置 LOSING
                            # process_deaths() 会将英雄移动到墓地，触发 _set_zone(GRAVEYARD)
                            # 在 _set_zone 中会先触发亡语，再检查是否真的死亡
                            player.hero.to_be_destroyed = True
                            self.log("%s's hero has %i health and deathrattle, marking for destruction", 
                                    player, player.hero.health)
                        else:
                            # 没有亡语，或者已经在墓地，直接设置 LOSING
                            self.log("%s's hero has %i health (zone=%s), setting playstate to LOSING", 
                                    player, player.hero.health, player.hero.zone)
                            player.playstate = PlayState.LOSING
            
            if player.playstate in (PlayState.CONCEDED, PlayState.DISCONNECTED):
                player.playstate = PlayState.LOSING
            if player.playstate == PlayState.LOSING:
                gameover = True

        if gameover:
            if self.players[0].playstate == self.players[1].playstate:
                for player in self.players:
                    player.playstate = PlayState.TIED
            else:
                for player in self.players:
                    if player.playstate == PlayState.LOSING:
                        player.playstate = PlayState.LOST
                    else:
                        player.playstate = PlayState.WON
            self.state = State.COMPLETE
            self.manager.step(self.next_step, Step.FINAL_WRAPUP)
            self.manager.step(self.next_step, Step.FINAL_GAMEOVER)
            self.manager.step(self.next_step)
            # 立即抛出 GameOver 异常，确保游戏停止
            raise GameOver("The game has ended.")
    def queue_actions(self, source: Entity, actions: "list[Action]", event_args=None):
        """
        Queue a list of \a actions for processing from \a source.
        Triggers an aura refresh afterwards.
        """
        old_event_args = source.event_args
        source.event_args = event_args
        ret = self.trigger_actions(source, actions)
        source.event_args = old_event_args
        return ret

    def trigger_actions(self, source: Entity, actions: "list[Action]"):
        """
        Performs a list of `actions` from `source`.
        This should seldom be called directly - use `queue_actions` instead.
        """
        ret = []
        for action in actions:
            if isinstance(action, EventListener):
                # Queuing an EventListener registers it as a one-time event
                # This allows registering events from eg. play actions
                self.log("Registering event listener %r on %r", action, self)
                action.once = True
                # FIXME: Figure out a cleaner way to get the event listener target
                if source.type == CardType.SPELL:
                    listener = source.controller
                else:
                    listener = source
                listener._events.append(action)
            elif hasattr(action, 'trigger'):
                # 只有具有 trigger 方法的对象才能触发
                ret.append(action.trigger(source))
            else:
                # 跳过非 Action 对象（例如 tuple、list 等）
                self.log("Warning: Skipping non-action object %r (type: %s)", action, type(action))
        return ret

    def pick_first_player(self):
        """
        Picks and returns first player, second player
        In the default implementation, the first player is always
        "Player 0". Use CoinRules to decide it randomly.
        """
        return self.players[0], self.players[1]

    def refresh_auras(self):
        refresh_queue = []
        for entity in self.entities:
            for script in entity.update_scripts:
                refresh_queue.append((entity, script))

        for hand in self.hands:
            for entity in hand.entities:
                for script in entity.data.scripts.Hand.update:
                    refresh_queue.append((entity, script))

        # Sort the refresh queue by refresh priority (used by eg. Lightspawn)
        refresh_queue.sort(key=lambda e: getattr(e[1], "priority", 50))
        for entity, action in refresh_queue:
            action.trigger(entity)

        buffs_to_destroy = []
        for buff in self.active_aura_buffs:
            if buff.tick < self.tick:
                buffs_to_destroy.append(buff)
        for buff in buffs_to_destroy:
            buff.remove()

        self.tick += 1

    def save_rewind_snapshot(self):
        """
        Save a deepcopy of the game state for the Rewind mechanic.
        Warning: This is an expensive operation! Only use when a Rewind card is played.
        """
        try:
            # Deepcopy includes the random state, entities, and everything reachable
            self.rewind_snapshot = copy.deepcopy(self)
        except Exception as e:
            self.log("FAILED TO SAVE REWIND SNAPSHOT: %s", e)
            self.rewind_snapshot = None

    def restore_rewind_snapshot(self):
        """
        Restore the game state from the saved snapshot.
        Returns True if successful, False otherwise.
        """
        if not self.rewind_snapshot:
            return False
            
        snapshot = self.rewind_snapshot
        
        # Update the internal state of THIS game object to match the snapshot
        self.__dict__.update(snapshot.__dict__)
        
        # Re-link internal references to 'self' instead of 'snapshot'
        # Since we copied the entities, their .game attribute points to the 'snapshot' object
        # We need to redirect them to 'self' (the current running game instance)
        
        # Fix Player references first (since entity.game depends on entity.controller.game)
        self.player1.game = self
        self.player2.game = self
        
        # Now fix entity controllers - this will automatically fix entity.game
        for entity in self.entities:
            # Skip the game object itself (its game property returns self)
            if entity is self:
                continue
            
            # Skip Player objects - their controller is a read-only property returning self
            if entity.type == CardType.PLAYER:
                continue
            
            # Fix controller references - check if controller is settable
            if hasattr(entity, "controller") and entity.controller:
                try:
                    if entity.controller == snapshot.player1:
                        entity.controller = self.player1
                    elif entity.controller == snapshot.player2:
                        entity.controller = self.player2
                except AttributeError:
                    # controller is a read-only property, skip
                    pass
        
        # Fix GameManager reference
        # The manager was also deepcopied, so it points to 'snapshot'
        self.manager.obj = self
        
        # Clear the snapshot after restore (optional, but prevents loops or stale data)
        self.rewind_snapshot = None
        
        return True

    def setup(self):
        self.log(translate("setting_up_game", game=self))
        self.state = State.RUNNING
        self.step = Step.BEGIN_DRAW
        self.zone = Zone.PLAY
        self.players[0].opponent = self.players[1]
        self.players[1].opponent = self.players[0]
        for player in self.players:
            player.zone = Zone.PLAY
            self.manager.new_entity(player)

        first, second = self.pick_first_player()
        self.player1 = first
        self.player1.first_player = True
        self.player2 = second
        self.player2.first_player = False

        for player in self.players:
            player.prepare_for_game()

        if self.is_standard:
            self.skin = self.random.choice(standard_board_skins)
        else:
            self.skin = self.random.choice(list(BoardEnum))

        self.manager.start_game()

    def start(self):
        self.setup()
        self.queue_actions(self, [GameStart()])
        self.begin_turn(self.player1)

    def end_turn(self):
        for player in self.players:
            player.minions_killed_this_turn = 0
        return self.queue_actions(self, [EndTurn(self.current_player)])

    def _end_turn(self):
        self.log("%s ends turn %i", self.current_player, self.turn)
        self.manager.step(self.next_step, Step.MAIN_CLEANUP)
        self.current_player.temp_mana = 0
        self.end_turn_cleanup()

    def end_turn_cleanup(self):
        self.manager.step(self.next_step, Step.MAIN_NEXT)
        for character in self.current_player.characters.filter(frozen=True):
            if not character.num_attacks and not character.exhausted:
                self.log("Freeze fades from %r", character)
                character.frozen = False
        for buff in self.entities.filter(one_turn_effect=True):
            self.log("Ending One-Turn effect: %r", buff)
            buff.remove()
        for entity in self.hands:
            for buff in CardList(entity.entities).filter(one_turn_effect=True):
                self.log("Ending One-Turn effect: %r", buff)
                buff.remove()
        
        # 重置本回合受到的伤害（用于"暗影之刃飞刀手"等卡牌）
        if hasattr(self.current_player, 'damage_taken_this_turn'):
            self.current_player.damage_taken_this_turn = 0

        # 更新上回合使用的卡牌追踪（用于WW_053飞车劫掠等卡牌）
        if hasattr(self.current_player, 'cards_played_this_turn_ids'):
            self.current_player.cards_played_last_turn = self.current_player.cards_played_this_turn_ids.copy()
            self.current_player.cards_played_this_turn_ids = []

        # 清除本回合从地图发现的卡牌记录（用于失落之城地图卡牌机制）- 失落之城（2025年7月）
        if hasattr(self.current_player, 'map_discovered_cards_this_turn'):
            self.current_player.map_discovered_cards_this_turn = []

        # Extra turn
        if self.next_players:
            next_player = self.next_players.pop(0)
        else:
            next_player = self.current_player.opponent
        self.begin_turn(next_player)

    def skip_turn(self):
        self.end_turn()
        self.end_turn()
        return self

    def begin_turn(self, player):
        # 重置无限循环检测计数器
        self._action_counter = 0
        ret = self.queue_actions(self, [BeginTurn(player)])
        self.manager.turn(player)
        return ret

    def _begin_turn(self, player: "Player"):
        self.manager.step(self.next_step, Step.MAIN_START)
        self.manager.step(self.next_step, Step.MAIN_ACTION)

        for p in self.players:
            p.cards_drawn_this_turn = 0

        player.turn_start = timegm(time.gmtime())
        player.last_turn = player.turn
        player.turn = self.turn
        player.cards_played_this_turn = 0
        player.minions_played_this_turn = 0
        player.minions_killed_this_turn = 0
        player.combo = False
        player.max_mana += 1
        player.used_mana = 0
        player.overload_locked = player.overloaded
        player.overloaded = 0
        player.elemental_played_last_turn = player.elemental_played_this_turn
        # 更新元素连续回合计数器
        if player.elemental_played_this_turn > 0:
            player.elemental_streak += 1
        else:
            player.elemental_streak = 0
        player.elemental_played_this_turn = 0
        # 更新上回合施放的法术数量（用于DEEP_010等卡牌）
        player.spells_played_last_turn = player.spells_played_this_turn
        player.spells_played_this_turn = 0
        # 清空本回合施放的法术流派列表（用于MIS_709圣光荧光棒等卡牌）
        if hasattr(player, 'spell_schools_played_this_turn'):
            player.spell_schools_played_this_turn = []
        
        # 重置本回合发现的卡牌数量（用于GDB_843视差光枪等卡牌）- 深暗领域（2024年11月）
        if hasattr(player, 'cards_discovered_this_turn'):
            player.cards_discovered_this_turn = 0

        # 重置本回合英雄受到的伤害（用于GDB_125治疗石等卡牌）- 深暗领域（2024年11月）
        if hasattr(player, 'damage_taken_this_turn'):
            player.damage_taken_this_turn = 0

        for entity in self.live_entities:
            if entity.type != CardType.PLAYER:
                entity.turns_in_play += 1

        # 处理休眠随从的计数递减
        # dormant_turns 的 property setter 会在计数清零时自动唤醒（card.py）
        for entity in player.live_entities:
            if getattr(entity, "dormant_turns", 0):
                entity.dormant_turns -= 1

        if player.hero.power:
            player.hero.power.activations_this_turn = 0
            player.hero.power.additional_activations_this_turn = 0

        for character in self.characters:
            character.num_attacks = 0
            character.damaged_this_turn = 0
            character.healed_this_turn = 0

        # 【Deck of Wonders (奇迹套牌) 特殊机制】
        # 每回合开始时,将手牌随机变形为法师或中立卡牌
        if getattr(player, "whizbang_deck_type", None) == "DECK_OF_WONDERS":
            from .actions import Morph
            from .cards import db
            from hearthstone.enums import CardClass
            
            # 获取所有可用的法师和中立卡牌
            # 只选择可收集的、标准模式的卡牌
            mage_and_neutral_cards = []
            for card_id, card_data in db.items():
                # 跳过英雄、英雄技能等非可打出卡牌
                if card_data.type not in (CardType.MINION, CardType.SPELL, CardType.WEAPON):
                    continue
                # 只选择法师和中立卡牌
                if card_data.card_class not in (CardClass.MAGE, CardClass.NEUTRAL):
                    continue
                # 只选择可收集的卡牌
                if not card_data.collectible:
                    continue
                # 如果是标准模式,只选择标准卡牌
                if player.is_standard and not card_data.is_standard:
                    continue
                
                mage_and_neutral_cards.append(card_id)
            
            # 将手牌中的每张卡随机变形
            if mage_and_neutral_cards:
                for card in list(player.hand):
                    # 随机选择一张法师或中立卡牌
                    random_card_id = self.random.choice(mage_and_neutral_cards)
                    # 使用 Morph action 变形
                    self.queue_actions(player, [Morph(card, random_card_id)])

        # 检查是否有随从阻止回合开始抽牌（用于 TIME_617 时空封冻者等卡牌）
        # 只有当场上没有任何随从拥有 blocks_turn_start_draw 属性时才抽牌
        should_draw = True
        for minion in player.field:
            if getattr(minion, 'blocks_turn_start_draw', False):
                self.log("%s blocks turn start draw for %s", minion, player)
                should_draw = False
                break
        
        if should_draw:
            player.draw()
        
        self.manager.step(self.next_step, Step.MAIN_END)


class CoinRules(BaseGame):
    """
    Randomly determines the starting player when the Game starts.
    The second player gets "The Coin" (GAME_005).
    """

    def pick_first_player(self):
        winner = self.random.choice(self.players)
        self.log(translate("tossing_coin", winner=winner))
        return winner, winner.opponent

    def begin_turn(self, player):
        if self.turn == 0:
            self.log(translate("player_gets_coin", player=self.player2))
            self.player2.give(THE_COIN)
        super().begin_turn(player)


class MulliganRules(BaseGame):
    """
    Performs a Mulligan phase when the Game starts.
    Only begin the game after both Mulligans have been chosen.
    """

    def start(self):
        from .actions import MulliganChoice

        self.setup()
        self.next_step = Step.BEGIN_MULLIGAN
        self.log(translate("entering_mulligan"))
        self.step, self.next_step = self.next_step, Step.MAIN_READY

        for player in self.players:
            self.queue_actions(
                self, [MulliganChoice(player, callback=self.mulligan_done)]
            )

    def mulligan_done(self):
        self.queue_actions(self, [GameStart()])
        for player in self.players:
            player.starting_hand = CardList(player.hand[:])
        self.begin_turn(self.player1)


class Game(MulliganRules, CoinRules, BaseGame):
    pass
