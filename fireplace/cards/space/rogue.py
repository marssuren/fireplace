"""
深暗领域 - ROGUE
"""
from ..utils import *


# COMMON

class GDB_465:
    """桶滚动作 - Barrel Roll
    Deal $5 damage to an undamaged character. Costs (1) if you're building a Starship.
    
    3费 潜行者法术
    对一个未受伤的角色造成$5点伤害。如果你正在构筑<b>星舰</b>，则法力值消耗为（1）点。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,  # 只能选择未受伤的目标
    }
    
    # 动态费用：如果正在构筑星舰，费用为1
    @property
    def cost(self):
        base_cost = self.data.cost
        if self.controller.starship_in_progress:
            return 1
        return base_cost
    
    def play(self):
        # 对未受伤的目标造成5点伤害
        yield Hit(TARGET, 5)


class GDB_875:
    """星岩收藏家 - Spacerock Collector
    Battlecry: Your next Combo card costs (1) less.
    
    1费 2/1 潜行者随从 - 德莱尼
    <b>战吼：</b>你的下一张<b>连击</b>牌法力值消耗减少（1）点。
    """
    race = Race.DRAENEI
    
    def play(self):
        # 给控制者添加一个buff，使下一张连击牌减费1
        yield Buff(CONTROLLER, "GDB_875e")


class GDB_875e:
    """下一张连击牌减费1"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 给手牌中的连击牌添加减费buff
    auras = [
        Buff(FRIENDLY_HAND + COMBO, "GDB_875e2")
    ]
    
    # 当使用连击牌后，移除这个buff
    events = Play(CONTROLLER, COMBO).after(Destroy(SELF))


class GDB_875e2:
    """连击牌减费1"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_876:
    """四处搜刮的造舰师 - Scrounging Shipwright
    Battlecry: Get a random Starship Piece from another class.
    
    2费 3/2 潜行者随从 - 德莱尼
    <b>战吼：</b>随机获取一张另一职业的<b>星舰组件</b>。
    """
    race = Race.DRAENEI
    
    def play(self):
        # 获取一张另一职业的星舰组件
        # 使用 RandomCollectible 选择器，过滤星舰组件并排除本职业
        yield Give(CONTROLLER, RandomCollectible(
            mechanics=GameTag.STARSHIP_PIECE,
            exclude_class=CardClass.ROGUE  # 排除潜行者职业
        ))


class SC_761:
    """闪现 - Blink
    Draw a Protoss minion. Combo: It costs (2) less.
    
    2费 潜行者法术
    抽一张星灵随从牌。<b>连击：</b>其法力值消耗减少（2）点。
    """
    def play(self):
        # 使用 ForceDraw 抽一张星灵随从
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + RACE(Race.PROTOSS))
        
        # 如果是连击且成功抽到牌，减费2
        if self.powered_up and cards:
            yield Buff(cards[0], "SC_761e")


class SC_761e:
    """星灵随从减费2"""
    tags = {
        GameTag.COST: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# RARE

class GDB_102:
    """星舰详图 - Starship Schematic
    Discover a Starship Piece from another class. It costs (1) less.
    
    1费 潜行者法术
    <b>发现</b>一张另一职业的<b>星舰组件</b>，其法力值消耗减少（1）点。
    """
    def play(self):
        # 发现一张另一职业的星舰组件
        yield Discover(CONTROLLER, RandomCollectible(
            mechanics=GameTag.STARSHIP_PIECE,
            exclude_class=CardClass.ROGUE  # 排除潜行者职业
        )).then(
            Give(CONTROLLER, Discover.CARD),
            Buff(Discover.CARD, "GDB_102e")
        )


class GDB_102e:
    """星舰组件减费1"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_870:
    """艾瑞达潜藏者 - Eredar Skulker
    Combo and Spellburst: Gain +2 Attack and Stealth.
    
    2费 1/3 潜行者随从 - 恶魔
    <b>连击，<b>法术迸发</b>：</b>获得+2攻击力和<b>潜行</b>。
    """
    race = Race.DEMON
    tags = {
        GameTag.SPELLBURST: True,
    }
    
    def play(self):
        # 连击：获得+2攻击力和潜行
        if self.powered_up:
            yield Buff(SELF, "GDB_870e")
    
    # 法术迸发：获得+2攻击力和潜行
    events = OWN_SPELL_PLAY.on(
        Buff(SELF, "GDB_870e"),
        SetTag(SELF, {GameTag.SPELLBURST: False})
    )


class GDB_870e:
    """+2攻击力和潜行"""
    tags = {
        GameTag.ATK: 2,
        GameTag.STEALTH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_881:
    """正中要害 - Pressure Points
    Deal $3 damage to a minion. Reduce the Cost of Combo cards in your hand by (1).
    
    3费 潜行者法术 - 暗影
    对一个随从造成$3点伤害。使你手牌中的<b>连击</b>牌法力值消耗减少（1）点。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 对目标造成3点伤害
        yield Hit(TARGET, 3)
        
        # 使手牌中的所有连击牌减费1
        for card in self.controller.hand:
            if card.combo:
                yield Buff(card, "GDB_881e")


class GDB_881e:
    """连击牌减费1"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_752:
    """黑暗圣堂武士 - Dark Templar
    Stealth. Battlecry: Destroy an enemy minion. <i>Play another Templar to merge into an Archon!</i>
    
    6费 5/3 潜行者随从
    <b>潜行</b>。<b>战吼：</b>消灭一个敌方随从。<i>再使用一张圣堂武士即可融合为执政官！</i>
    """
    tags = {
        GameTag.STEALTH: True,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 战吼：消灭一个敌方随从
        if self.target:
            yield Destroy(TARGET)
        
        # 检查是否已经有圣堂武士在场，如果有则融合为执政官
        yield CheckTemplarMerge(CONTROLLER)


class SC_765:
    """高阶圣堂武士 - High Templar
    Battlecry: Deal 2 damage to all enemies. <i>Play another Templar to merge into an Archon!</i>
    
    6费 3/5 潜行者随从
    <b>战吼：</b>对所有敌人造成2点伤害。<i>再使用一张圣堂武士即可融合为执政官！</i>
    """
    def play(self):
        # 战吼：对所有敌人造成2点伤害
        yield Hit(ENEMY_CHARACTERS, 2)
        
        # 检查是否已经有圣堂武士在场，如果有则融合为执政官
        yield CheckTemplarMerge(CONTROLLER)


def CheckTemplarMerge(target):
    """检查圣堂武士融合
    
    如果场上已经有一个圣堂武士（SC_752或SC_765），则将两个圣堂武士融合为执政官。
    """
    def action(self):
        # 获取场上的所有圣堂武士
        templars = [m for m in self.controller.field if m.id in ["SC_752", "SC_765"]]
        
        # 如果有2个或更多圣堂武士，融合为执政官
        if len(templars) >= 2:
            # 摧毁两个圣堂武士
            yield Destroy(templars[0])
            yield Destroy(templars[1])
            
            # 召唤执政官
            yield Summon(CONTROLLER, "SC_752t")
    
    return action


# EPIC

class GDB_467:
    """类星体 - Quasar
    Shuffle your hand into your deck. Reduce the Cost of cards in your deck by (3).
    
    8费 潜行者法术
    将你的手牌洗入你的牌库。使你牌库中卡牌的法力值消耗减少（3）点。
    """
    def play(self):
        # 将手牌洗入牌库
        hand_cards = list(self.controller.hand)
        for card in hand_cards:
            if card != self:  # 不包括本牌自己
                yield Shuffle(CONTROLLER, card)
        
        # 使牌库中所有卡牌减费3
        for card in self.controller.deck:
            yield Buff(card, "GDB_467e")


class GDB_467e:
    """牌库卡牌减费3"""
    tags = {
        GameTag.COST: -3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_873:
    """幸运彗星 - Lucky Comet
    Discover a Combo minion. The next one you play triggers its Combo twice.
    
    2费 潜行者法术
    <b>发现</b>一张<b>连击</b>随从牌。你使用的下一张<b>连击</b>随从牌的<b>连击</b>会触发两次。
    """
    def play(self):
        # 发现一张连击随从牌
        yield Discover(CONTROLLER, RandomMinion(mechanics=GameTag.COMBO)).then(
            Give(CONTROLLER, Discover.CARD)
        )
        
        # 给控制者添加buff，使下一张连击随从的连击触发两次
        yield Buff(CONTROLLER, "GDB_873e")


class GDB_873e:
    """下一张连击随从的连击触发两次
    
    这个 buff 会在玩家身上，当玩家使用连击随从时：
    1. 给该随从添加一个特殊标记 (combo_double_trigger)
    2. 移除这个 player buff
    
    实际的"触发两次"逻辑需要在核心引擎的 Play action 中实现。
    核心引擎会检测随从的 combo_double_trigger 属性并重复执行连击效果。
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听连击随从的使用
    events = Play(CONTROLLER, MINION + COMBO).on(
        # 给使用的连击随从添加双倍触发标记
        Buff(Play.CARD, "GDB_873e2"),
        # 移除这个 player buff（只对下一张生效）
        Destroy(SELF)
    )


class GDB_873e2:
    """连击双倍触发标记
    
    这个 buff 标记该随从的连击应该触发两次。
    核心引擎会检测这个 buff 的 combo_double_trigger 属性并重复执行连击效果。
    
    注意：这需要在 fireplace/fireplace/actions.py 的 Play action 中实现：
    - 检测 minion 是否有 combo_double_trigger 属性的 buff
    - 如果有，执行连击效果两次
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 添加一个自定义属性来标记双倍触发
    # 核心引擎会检查这个属性
    combo_double_trigger = True


# LEGENDARY

class GDB_466:
    """引力置换器 - The Gravitational Displacer
    Starship Piece. When this is launched, summon a copy of the Starship.

    5费 5/4 潜行者随从 - 星舰组件
    <b>星舰组件</b>
    当本随从被发射时，召唤<b>星舰</b>的一个复制。
    """
    # 当本随从被发射时，召唤星舰的一个复制
    # 这个效果需要在发射时触发，通过 launch 动作实现
    def launch(self):
        # 获取当前星舰
        starship = self.controller.starship_in_progress
        if starship:
            # 召唤星舰的复制
            yield Summon(CONTROLLER, Copy(starship))


class GDB_472:
    """塔尔加斯 - Talgath
    Undamaged enemy minions take double damage. Combo: Get a Backstab.
    
    3费 3/3 潜行者随从 - 恶魔（传说）
    未受伤的敌方随从受到的伤害翻倍。<b>连击：</b>获取一张背刺。
    """
    race = Race.DEMON
    
    # 未受伤的敌方随从受到双倍伤害
    # 使用 Predamage 事件，当目标是未受伤的敌方随从时，将伤害翻倍
    # 参考 titans/paladin.py 的 Predamage 用法
    events = Predamage(ENEMY_MINIONS).on(
        lambda self, source, target, amount: 
            # 如果目标未受伤，将伤害设置为原伤害的2倍
            Predamage(target, amount * 2) if target.damage == 0 else None
    )
    
    def play(self):
        # 连击：获取一张背刺
        if self.powered_up:
            yield Give(CONTROLLER, "CS2_072")  # 背刺的卡牌ID
