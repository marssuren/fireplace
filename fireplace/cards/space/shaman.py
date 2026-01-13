"""
深暗领域 - SHAMAN
"""
from ..utils import *


# COMMON

class GDB_443:
    """宇航员 - Cosmonaut
    7费 5/5 萨满随从 - 德莱尼
    战吼：从你的牌库中发现一张法术牌，其法力值消耗减少（5）点。

    Battlecry: Discover a spell from your deck. Reduce its Cost by (5).
    """
    race = Race.DRAENEI

    def play(self):
        # 从牌库中发现一张法术牌
        discovered = yield Discover(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL))

        # 如果发现成功，减少其费用5点
        if discovered:
            yield Buff(discovered[0], "GDB_443e")


class GDB_443e:
    """费用减少"""
    tags = {
        GameTag.COST: -5,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_864:
    """第一次接触 - First Contact
    1费 萨满法术
    随机召唤两个法力值消耗为（1）的随从。过载：（1）

    Summon two random 1-Cost minions. Overload: (1)
    """
    tags = {
        GameTag.OVERLOAD: 1,
    }

    def play(self):
        # 随机召唤两个1费随从
        yield Summon(CONTROLLER, RandomMinion(cost=1)) * 2


class GDB_901:
    """极紫外破坏者 - Ultraviolet Breaker
    3费 3/2 萨满随从 - 元素
    战吼：对一个敌方随从造成3点伤害。将3张小行星洗入你的牌库。

    Battlecry: Deal 3 damage to an enemy minion. Shuffle 3 Asteroids into your deck.
    """
    race = Race.ELEMENTAL
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }

    def play(self):
        # 对目标造成3点伤害
        if TARGET:
            yield Hit(TARGET, 3)

        # 将3张小行星洗入牌库
        for i in range(3):
            yield Shuffle(CONTROLLER, "GDB_901t")


class SC_407:
    """锁定 - Lock On
    1费 萨满法术
    将一个随从的生命值变为1。你的下一次星舰发射的法力值消耗减少（2）点。

    Set a minion's Health to 1. Your next Starship launch costs (2) less.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }

    def play(self):
        # 将目标生命值设为1
        yield SetTags(TARGET, {GameTag.HEALTH: SET(1)})

        # 下一次星舰发射减费2点
        yield Buff(CONTROLLER, "SC_407e")


class SC_407e:
    """星舰发射减费 - Starship Launch Cost Reduction

    效果说明:
    - 使你的下一次星舰发射的法力值消耗减少(2)点
    - 这是一次性效果,使用后自动移除

    实现机制:
    - 通过starship_launch_cost_reduction属性标记减费数值
    - 核心引擎的LaunchStarship动作会检查此属性
    - 发射星舰时自动应用减费并移除此buff

    Your next Starship launch costs (2) less.
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }

    # 星舰发射减费数值(由核心引擎的LaunchStarship动作读取)
    starship_launch_cost_reduction = 2


class SC_409:
    """飞弹舱 - Missile Pod
    2费 1/3 萨满随从 - 机械 - 星舰组件
    战吼：对所有敌人造成1点伤害。发射时也会触发。

    Starship Piece
    Battlecry: Deal 1 damage to all enemies. Also triggers on launch.
    """
    race = Race.MECHANICAL

    # 战吼：对所有敌人造成1点伤害
    play = Hit(ALL_ENEMIES, 1)

    # 发射时也会触发
    def launch(self):
        """星舰发射时触发"""
        yield Hit(ALL_ENEMIES, 1)


# RARE

class GDB_444:
    """行星领航员 - Planetary Navigator
    2费 3/2 萨满随从 - 德莱尼
    战吼：你使用的下一个德莱尼的法力值消耗减少（2）点，但拥有过载：（2）。

    Battlecry: The next Draenei you play costs (2) less, but has Overload: (2).
    """
    race = Race.DRAENEI

    def play(self):
        # 给玩家添加buff，下一个德莱尼减费2点但有过载2
        yield Buff(CONTROLLER, "GDB_444e")


class GDB_444e:
    """德莱尼减费+过载

    机制说明：
    - 光环效果：使手牌中的德莱尼减费2点
    - 触发效果：打出德莱尼时添加过载2并移除此buff
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }

    # 光环：下一个德莱尼减费2点
    update = Refresh(FRIENDLY_HAND + DRAENEI, {GameTag.COST: -2})

    # 监听打出德莱尼牌：添加过载并移除buff
    events = Play(CONTROLLER, DRAENEI).on(
        lambda self, player, played_card, target=None: Overload(CONTROLLER, 2),
        Destroy(SELF)
    )


class GDB_445:
    """陨石风暴 - Meteor Storm
    6费 萨满法术（自然）
    对所有随从造成5点伤害。将5张小行星洗入你的牌库。

    Deal $5 damage to all minions. Shuffle 5 Asteroids into your deck.
    """
    def play(self):
        # 对所有随从造成5点伤害
        yield Hit(ALL_MINIONS, 5)

        # 将5张小行星洗入牌库
        for i in range(5):
            yield Shuffle(CONTROLLER, "GDB_901t")


class GDB_451:
    """三角测量 - Triangulate
    2费 萨满法术
    从你的牌库中发现一张不同的法术牌，并将它的3张复制洗入你的牌库。

    Discover a different spell from your deck. Shuffle 3 copies of it into your deck.
    """
    def play(self):
        # 从牌库中发现一张法术牌
        discovered = yield Discover(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL))

        # 如果发现成功，将3张复制洗入牌库
        if discovered:
            spell_id = discovered[0].id
            for i in range(3):
                yield Shuffle(CONTROLLER, spell_id)


class SC_413:
    """攻城坦克 - Siege Tank
    5费 5/5 萨满随从 - 机械
    战吼：对一个随机敌方随从造成10点伤害。
    （如果你在本局对战中发射过星舰，则会变形。）

    Battlecry: Deal 10 damage to a random enemy minion.
    (Transforms if you launched a Starship this game.)
    """
    race = Race.MECHANICAL

    def play(self):
        # 对一个随机敌方随从造成10点伤害
        yield Hit(RANDOM_ENEMY_MINION, 10)

        # 如果发射过星舰，变形为强化版本
        if self.controller.starships_launched_this_game > 0:
            yield Morph(SELF, "SC_413t")


# EPIC

class GDB_434:
    """流彩巨岩 - Bolide Behemoth
    4费 3/6 萨满随从 - 元素
    战吼：在本局对战中，你的小行星造成的伤害增加1点。
    法术迸发：将3张小行星洗入你的牌库。

    Battlecry: Your Asteroids deal 1 more damage this game.
    Spellburst: Shuffle 3 of them into your deck.
    """
    race = Race.ELEMENTAL
    tags = {
        GameTag.SPELLBURST: True,
    }

    def play(self):
        # 在本局对战中，小行星伤害+1
        yield Buff(CONTROLLER, "GDB_434e")

    # 法术迸发：将3张小行星洗入牌库
    events = OWN_SPELL_PLAY.on(
        lambda self, player: [Shuffle(CONTROLLER, "GDB_901t") for _ in range(3)],
        SetTags(SELF, {GameTag.SPELLBURST: False})
    )


class GDB_434e:
    """小行星伤害增强"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }

    # 这个buff会被小行星的伤害计算逻辑读取
    # 小行星Token需要检查玩家是否有此buff，并增加伤害


class GDB_479:
    """星云 - Nebula
    9费 萨满法术（奥术）
    发现并召唤两个法力值消耗为（8）的随从，并使其具有嘲讽和扰魔。

    Discover two 8-Cost minions to summon with Taunt and Elusive.
    """
    def play(self):
        # 发现第一个8费随从
        discovered1 = yield Discover(CONTROLLER, RandomMinion(cost=8))
        if discovered1:
            minion1 = yield Summon(CONTROLLER, discovered1[0].id)
            if minion1:
                yield Buff(minion1[0], "GDB_479e")

        # 发现第二个8费随从
        discovered2 = yield Discover(CONTROLLER, RandomMinion(cost=8))
        if discovered2:
            minion2 = yield Summon(CONTROLLER, discovered2[0].id)
            if minion2:
                yield Buff(minion2[0], "GDB_479e")


class GDB_479e:
    """嘲讽+扰魔"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.ELUSIVE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# LEGENDARY

class GDB_447:
    """预言者努波顿 - Farseer Nobundo
    5费 6/4 萨满随从 - 德莱尼（传说）
    亡语：开启星系投影，投影会吸收你施放的下一个法术的能量。

    Deathrattle: Open the Galaxy's Lens. It absorbs the power of the next spell you cast.

    机制说明：
    - 亡语时召唤"星系投影"地标
    - 星系投影会吸收下一个法术的效果
    - 吸收后，星系投影会获得该法术的效果，并在使用时释放
    """
    race = Race.DRAENEI

    def deathrattle(self):
        # 召唤星系投影地标
        yield Summon(CONTROLLER, "GDB_447t")


class GDB_448:
    """摩摩尔 - Murmur
    7费 6/6 萨满随从 - 元素（传说）
    你每回合打出的第一个战吼随从的法力值消耗为（1）点，但在打出后会立即死亡。

    Your first Battlecry minion each turn costs (1), but immediately dies after being played.

    机制说明：
    - 光环效果：每回合第一个战吼随从费用变为1
    - 触发效果：该随从打出后立即死亡
    - 每回合重置计数
    - 使用buff来追踪状态，而不是动态属性
    """
    race = Race.ELEMENTAL

    # 进入场地时，给玩家添加追踪buff
    events = [
        Summon(SELF).after(
            Buff(CONTROLLER, "GDB_448e")
        ),
        # 离开场地时，移除追踪buff
        Death(SELF).after(
            lambda self, player: [
                Destroy(buff) for buff in self.controller.buffs
                if buff.id == "GDB_448e"
            ]
        )
    ]


class GDB_448e:
    """摩摩尔追踪buff

    机制说明：
    - 追踪本回合是否已使用摩摩尔效果
    - 光环：使第一个战吼随从费用变为1
    - 触发：打出战吼随从时摧毁它并标记已使用
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.used_this_turn = False

    # 光环：如果本回合未使用，使手牌中的战吼随从费用变为1
    def update(self, entities):
        if not self.used_this_turn:
            return [
                Refresh(card, {GameTag.COST: SET(1)})
                for card in self.controller.hand
                if card.type == CardType.MINION
                and card.tags.get(GameTag.BATTLECRY, False)
            ]
        return []

    # 监听战吼随从被打出
    events = [
        # 打出战吼随从时，如果本回合未使用，则摧毁该随从并标记已使用
        Play(CONTROLLER, MINION + BATTLECRY).after(
            lambda self, player, played_card, target=None: [
                Destroy(card),
                setattr(self, 'used_this_turn', True)
            ] if not self.used_this_turn else None
        ),
        # 回合开始时重置标记
        OWN_TURN_BEGIN.on(
            lambda self, player: setattr(self, 'used_this_turn', False)
        )
    ]


