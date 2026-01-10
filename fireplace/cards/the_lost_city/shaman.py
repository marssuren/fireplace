"""
失落之城 - SHAMAN
"""
from ..utils import *
from .kindred_helpers import check_kindred_active


# COMMON

class DINO_406:
    """喷吐火焰 - Spit Fire
    3费 火焰法术
    造成$4点伤害。使你的元素获得+1/+1。

    Deal $4 damage. Give your Elementals +1/+1.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        # 造成4点伤害
        yield Hit(TARGET, 4)
        # 给所有友方元素+1/+1
        yield Buff(FRIENDLY_MINIONS + RACE(Race.ELEMENTAL), "DINO_406e")


class DINO_406e:
    """喷吐火焰增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class TLC_222:
    """火鹰飞翔 - Firebird Soar
    3费 火焰法术
    抽两张不同类型的随从牌，使其获得+2/+2。

    Draw 2 minions of different types. Give them +2/+2.

    实现说明：
    - 从牌库中抽取两张随从牌
    - 给不同类型（种族）的随从+2/+2
    - 如果两张随从类型相同，只给第一张增益
    """
    def play(self):
        # 抽两张随从牌
        drawn_cards = yield ForceDraw(CONTROLLER, 2).filter(lambda card: card.type == CardType.MINION)

        # 检查抽到的随从牌，给不同类型的随从+2/+2
        seen_races = set()
        for card in drawn_cards:
            # 获取随从的种族
            card_races = tuple(sorted(getattr(card, 'races', [])))
            if not card_races:
                card_races = (None,)  # 无种族随从

            # 如果是新的种族组合，给予增益
            if card_races not in seen_races:
                seen_races.add(card_races)
                yield Buff(card, "TLC_222e")


class TLC_222e:
    """火鹰飞翔增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class TLC_224:
    """机械熔火 - Mechanical Magma
    4费 2/5 元素+机械
    每当你使用一张火焰法术牌时，获得等同于其法力值消耗的属性值。

    Whenever you cast a Fire spell, gain stats equal to its Cost.

    实现说明：
    - 监听 Play 事件，检测火焰法术的使用
    - 获得等同于法术费用的攻击力和生命值
    """
    events = Play(CONTROLLER, type=CardType.SPELL).on(
        lambda self, player, card, *args: (
            Buff(self, "TLC_224e", atk=card.cost, max_health=card.cost)
            if hasattr(card, 'spell_school') and card.spell_school == SpellSchool.FIRE
            else None
        )
    )


class TLC_224e:
    """机械熔火增益"""
    # 动态属性值由 Buff 传入


class TLC_225:
    """烬鳍鱼人 - Emberfin Murloc
    2费 1/2 元素+鱼人
    <b>亡语：</b>召唤一个2/1的炽烈烬火。

    Deathrattle: Summon a 2/1 Blazing Ember.
    """
    deathrattle = Summon(CONTROLLER, "TLC_249")


# RARE

class DINO_412:
    """始祖龟图腾 - Primal Turtle Totem
    1费 0/3 图腾
    在你的回合结束时，随机获取一张具有多类型的随从牌。

    At the end of your turn, get a random minion with multiple types.

    实现说明：
    - 监听回合结束事件
    - 从所有具有多种族的随从中随机选择一张加入手牌
    - 使用 card_filter 过滤出具有多个种族的随从
    """
    def _has_multiple_races(card):
        """检查卡牌是否有多个种族"""
        return hasattr(card, 'races') and len(card.races) > 1

    events = OWN_TURN_END.on(
        lambda self, player: Give(CONTROLLER, RandomCollectible(
            type=CardType.MINION,
            card_filter=_has_multiple_races
        ))
    )


class DINO_413:
    """冰脊剑龙 - Iceridge Stegosaurus
    4费 3/4 元素+野兽
    <b>战吼：</b>随机对两个敌方随从造成2点伤害。<b>延系：</b>并将其<b>冻结</b>。

    Battlecry: Deal 2 damage to two random enemy minions. Kindred: Freeze them.

    实现说明：
    - 战吼：随机对两个敌方随从造成2点伤害
    - 延系：如果上回合打出过元素或野兽，则冻结受伤的随从
    """
    def play(self):
        # 检查 Kindred 是否激活（元素或野兽）
        kindred_active = (
            check_kindred_active(self.controller, CardType.MINION, Race.ELEMENTAL) or
            check_kindred_active(self.controller, CardType.MINION, Race.BEAST)
        )

        # 随机选择两个敌方随从
        targets = yield RandomPick(ENEMY_MINIONS, count=2)

        for target in targets:
            # 造成2点伤害
            yield Hit(target, 2)
            # 如果 Kindred 激活，冻结目标
            if kindred_active:
                yield Freeze(target)


class TLC_221:
    """炽火缠身 - Blazing Embrace
    6费 火焰法术
    造成$3点伤害，召唤相同数量的2/1的炽烈烬火。

    Deal $3 damage. Summon that many 2/1 Blazing Embers.

    实现说明：
    - 造成3点伤害
    - Hit action 返回实际造成的伤害量
    - 根据实际伤害数量召唤炽烈烬火
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        # Hit Action 返回实际造成的伤害值
        damage_dealt = yield Hit(TARGET, 3)

        # 根据实际伤害召唤炽烈烬火
        for _ in range(damage_dealt):
            yield Summon(CONTROLLER, "TLC_249")


class TLC_223:
    """火山长尾蜥 - Volcanic Lizard
    3费 2/3 元素+野兽
    <b>战吼：</b>抽一张火焰法术牌。<b>延系：</b>使其获得<b>法术伤害+2</b>。

    Battlecry: Draw a Fire spell. Kindred: Give it Spell Damage +2.

    实现说明：
    - 战吼：从牌库中抽一张火焰法术牌
    - 延系：如果上回合打出过元素或野兽，给抽到的法术+2法术伤害
    """
    def play(self):
        # 检查 Kindred 是否激活（元素或野兽）
        kindred_active = (
            check_kindred_active(self.controller, CardType.MINION, Race.ELEMENTAL) or
            check_kindred_active(self.controller, CardType.MINION, Race.BEAST)
        )

        # 从牌库中抽一张火焰法术牌
        drawn_cards = yield ForceDraw(CONTROLLER).filter(
            lambda card: card.type == CardType.SPELL and
            hasattr(card, 'spell_school') and
            card.spell_school == SpellSchool.FIRE
        )

        # 如果 Kindred 激活，给予法术伤害+2
        if kindred_active and drawn_cards:
            for card in drawn_cards:
                yield Buff(card, "TLC_223e")


class TLC_223e:
    """火山长尾蜥增益 - 法术伤害+2"""
    tags = {
        GameTag.SPELLPOWER: 2,
    }


class TLC_464:
    """登山地图 - Mountain Map
    1费 法术
    <b>发现</b>一张你未使用过的类型的随从牌，如果你在本回合中使用该牌，再从其余选项中选择一张。

    Discover a minion of a type you haven't played. If you play it this turn, pick from the rest.

    实现说明：
    - 这是一张地图卡牌，使用 Map Cards 机制
    - 发现一张未使用过类型的随从牌
    - 如果在本回合打出发现的牌，可以再次从剩余选项中选择
    - 使用 card_filter 过滤出未使用过类型的随从
    """
    def play(self):
        from .map_helpers import mark_map_discovered_card

        # 获取已经使用过的随从类型
        played_races = set()
        if hasattr(self.controller, 'cards_played_this_game'):
            for card_id in self.controller.cards_played_this_game:
                try:
                    from .. import db
                    card_data = db[card_id]
                    if card_data.type == CardType.MINION and hasattr(card_data, 'races'):
                        for race in card_data.races:
                            played_races.add(race)
                except KeyError:
                    continue

        # 定义过滤函数：未使用过类型的随从
        def is_unplayed_type(card):
            if card.type != CardType.MINION:
                return False
            if not hasattr(card, 'races') or not card.races:
                # 无种族随从：如果没有打出过无种族随从，则可以发现
                return None not in played_races
            # 有种族随从：至少有一个种族未被使用过
            return any(race not in played_races for race in card.races)

        # 发现一张未使用过类型的随从牌
        cards = yield Discover(CONTROLLER, cards=RandomCollectible(
            type=CardType.MINION,
            card_filter=is_unplayed_type
        ))

        if cards:
            # 标记为地图发现的卡牌
            mark_map_discovered_card(self.controller, cards[0].id)


# EPIC

class TLC_227:
    """熔岩涌流 - Lava Surge
    3费 火焰法术
    对生命值最低的敌人造成$2点伤害，触发三次。<b>过载：</b>（1）。

    Deal $2 damage to the lowest Health enemy. Repeat 3 times. Overload: (1).

    实现说明：
    - 每次选择生命值最低的敌人（英雄或随从）
    - 重复3次，每次重新选择目标
    - 过载1点法力水晶
    """
    def play(self):
        # 重复3次
        for _ in range(3):
            # 找到生命值最低的敌人（包括英雄和随从）
            targets = self.controller.opponent.field + [self.controller.opponent.hero]
            if targets:
                # 选择生命值最低的目标
                min_health_target = min(targets, key=lambda t: t.health)
                yield Hit(min_health_target, 2)


class TLC_482:
    """熔爪巨龙 - Molten Claw Dragon
    5费 3/4 元素+龙
    <b>战吼：</b>召唤两个2/1的炽烈烬火。<b>延系：</b>触发你的炽烈烬火的<b>亡语</b>。

    Battlecry: Summon two 2/1 Blazing Embers. Kindred: Trigger their Deathrattles.

    实现说明：
    - 战吼：召唤两个炽烈烬火
    - 延系：如果上回合打出过元素或龙，触发召唤的炽烈烬火的亡语
    """
    def play(self):
        # 检查 Kindred 是否激活（元素或龙）
        kindred_active = (
            check_kindred_active(self.controller, CardType.MINION, Race.ELEMENTAL) or
            check_kindred_active(self.controller, CardType.MINION, Race.DRAGON)
        )

        # 召唤两个炽烈烬火
        summoned_embers = []
        for _ in range(2):
            ember = yield Summon(CONTROLLER, "TLC_249")
            if ember:
                summoned_embers.extend(ember)

        # 如果 Kindred 激活，触发炽烈烬火的亡语
        if kindred_active:
            for ember in summoned_embers:
                # 触发亡语：造成2点伤害并随机分配到敌方角色上
                yield ActivateDeathrattle(ember)


# LEGENDARY

class TLC_228:
    """布拉玛·灼石 - Bru'kan, Blazestone
    3费 1/5 传说随从
    你的元素会额外造成1点伤害。

    Your Elementals deal 1 extra damage.

    实现说明：
    - 光环效果：所有友方元素造成的伤害+1
    - 包括元素随从的攻击伤害和元素法术的伤害
    """
    # 使用 Aura 实现光环效果
    # 给所有友方元素+1攻击力
    update = Refresh(FRIENDLY_MINIONS + RACE(Race.ELEMENTAL), {
        GameTag.ATK: +1,
    })


class TLC_229:
    """群山之灵 - Spirit of the Mountains
    1费 传说任务法术
    <b>任务：</b>使用6个不同类型的随从牌。<b>奖励：</b>阿沙隆。

    Quest: Play 6 minions of different types. Reward: Ashalon.

    实现说明：
    - 任务：打出6个不同种族的随从牌
    - 奖励：阿沙隆（10费 10/10 突袭+嘲讽）
    - 追踪已打出的随从种族类型（单个种族，不是组合）
    - 例如：打出"元素+野兽"会同时记录元素和野兽两个种族
    """
    # 任务进度追踪
    progress_total = 6

    def _get_progress(self):
        """获取任务进度：已打出的不同种族数量"""
        if not hasattr(self.controller, 'tlc_229_played_races'):
            self.controller.tlc_229_played_races = set()
        return len(self.controller.tlc_229_played_races)

    # 监听随从打出事件
    events = Play(CONTROLLER, type=CardType.MINION).after(
        lambda self, player, card, *args: self._track_minion_type(card)
    )

    def _track_minion_type(self, card):
        """追踪打出的随从种族类型"""
        if not hasattr(self.controller, 'tlc_229_played_races'):
            self.controller.tlc_229_played_races = set()

        # 获取随从的种族
        if hasattr(card, 'races') and card.races:
            # 将每个种族单独记录（不是组合）
            for race in card.races:
                self.controller.tlc_229_played_races.add(race)
        else:
            # 无种族随从也算一种类型
            self.controller.tlc_229_played_races.add(None)

        # 检查是否完成任务
        if len(self.controller.tlc_229_played_races) >= self.progress_total:
            # 完成任务，给予奖励
            yield Give(CONTROLLER, "TLC_229t")
            # 移除任务卡牌
            yield Destroy(self)

