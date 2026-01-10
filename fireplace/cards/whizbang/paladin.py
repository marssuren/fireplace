"""
威兹班的工坊 - PALADIN
"""
from ..utils import *


# COMMON

class MIS_700:
    """痛打豺狼人 - Whack-A-Gnoll
    Discover a Paladin weapon from the past. Give it +1/+1.
    发现一把过去的圣骑士武器,使其+1/+1
    """
    # 1费法术 发现一把圣骑士武器并给予+1/+1
    # 官方数据:Discover a Paladin weapon from the past. Give it +1/+1.
    def play(self):
        # Discover 一把圣骑士武器
        cards = yield DISCOVER(RandomCollectible(card_class=CardClass.PALADIN, type=CardType.WEAPON))
        if cards:
            # 给予+1/+1 Buff
            yield Buff(cards[0], "MIS_700e")


class MIS_709:
    """圣光荧光棒 - Holy Glowsticks
    Lifesteal Deal $4 damage to a minion. Costs (1) if you've cast a Holy spell this turn.
    吸血 对一个随从造成$4点伤害。如果你在本回合施放过圣光法术,则法力值消耗为(1)点
    """
    # 4费法术 吸血 造成4点伤害
    # 如果本回合施放过圣光法术,费用为1
    # 官方数据:Lifesteal Deal $4 damage to a minion. Costs (1) if you've cast a Holy spell this turn.
    lifesteal = True
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    play = Hit(TARGET, 4)
    
    # 费用修正:如果本回合施放过圣光法术,费用为1
    cost_mod = lambda self, i: -(self.cost - 1) if SpellSchool.HOLY in self.controller.spell_schools_played_this_turn else 0


class TOY_810:
    """画师的美德 - Painter's Virtue
    [x]After your hero attacks, give minions in your hand +1/+1.
    在你的英雄攻击后,使你手牌中的随从牌+1/+1
    """
    # 4费武器 2/3 在英雄攻击后,使手牌中的随从+1/+1
    # 官方数据:After your hero attacks, give minions in your hand +1/+1.
    events = Attack(FRIENDLY_HERO).after(Buff(FRIENDLY_HAND + MINION, "TOY_810e"))


class TOY_811:
    """绒绒虎 - Tigress Plushy
    Miniaturize Rush, Lifesteal, Divine Shield
    微缩 突袭,吸血,圣盾
    """
    # 4费 3/2 微缩 突袭,吸血,圣盾
    # 官方数据:Miniaturize Rush, Lifesteal, Divine Shield
    rush = True
    lifesteal = True
    divine_shield = True


class TOY_881:
    """光鲜包装 - Fancy Packaging
    Give a minion with Divine Shield +2/+3.
    使一个具有圣盾的随从+2/+3
    """
    # 1费法术 使一个具有圣盾的随从+2/+3
    # 官方数据:Give a minion with Divine Shield +2/+3.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_WITH_DIVINE_SHIELD: 0}
    
    play = Buff(TARGET, "TOY_881e")


# RARE

class MIS_918:
    """灯火机器人 - Flickering Lightbot
    [x]Gigantify Costs (1) less for each Holy spell you've cast this game.
    巨大化 你在本局对战中每施放一个圣光法术,本牌的法力值消耗便减少(1)点
    """
    # 5费 3/3 机械 巨大化
    # 本局对战中每施放一个圣光法术,费用减少1
    # 官方数据:Gigantify Costs (1) less for each Holy spell you've cast this game.
    
    cost_mod = lambda self, i: -self.controller.spell_schools_played.count(SpellSchool.HOLY)


class TOY_808:
    """工匠光环 - Crafter's Aura
    At the end of your turn, summon a random 6-Cost minion. Lasts 3 turns.
    在你的回合结束时,召唤一个随机的法力值消耗为6的随从。持续3回合
    """
    # 7费法术 圣光流派 在回合结束时召唤一个随机6费随从,持续3回合
    # 官方数据:At the end of your turn, summon a random 6-Cost minion. Lasts 3 turns.
    # 这是一个 Aura 类型的法术,创建持续效果
    
    def play(self):
        # 给控制者添加持续3回合的 Aura Buff
        yield Buff(CONTROLLER, "TOY_808e")


class TOY_880:
    """发条执行者 - Wind-Up Enforcer
    [x]Tradeable Battlecry: Summon 1 copy of this minion. <i>(Trade to upgrade!)</i>
    可交易 战吼:召唤本随从的1个复制。(交易后升级!)
    """
    # 6费 3/5 可交易
    # 战吼:召唤本随从的复制,数量 = 1 + 交易次数
    # 官方数据:Tradeable Battlecry: Summon 1 copy of this minion. (Trade to upgrade!)
    # 
    # 【交易升级机制】每次交易后,召唤的复制数量增加
    # - 基础版本:召唤 1 个复制
    # - 交易 1 次后:召唤 2 个复制
    # - 交易 2 次后:召唤 3 个复制
    # - 以此类推
    # 
    # 实现方式:使用卡牌自定义属性 times_traded 追踪交易次数
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化交易次数计数器
        if not hasattr(self, 'times_traded'):
            self.times_traded = 0
    
    def play(self):
        # 召唤复制,数量 = 1 + 交易次数
        copies_to_summon = 1 + getattr(self, 'times_traded', 0)
        for _ in range(copies_to_summon):
            yield Summon(CONTROLLER, ExactCopy(SELF))
    
    # 监听交易事件,增加交易计数器
    # 注意:Tradeable 机制由核心引擎处理,这里我们需要在卡牌返回牌库时增加计数器
    # 使用 ZoneChange 事件监听卡牌从手牌返回牌库
    events = ZoneChange(SELF, Zone.HAND, Zone.DECK).after(
        lambda self: setattr(self, 'times_traded', getattr(self, 'times_traded', 0) + 1)
    )


class TOY_882:
    """装饰美术家 - Trinket Artist
    Battlecry: Draw a Divine Shield minion and an Aura.
    战吼:抽一张圣盾随从牌和一张光环牌
    """
    # 3费 2/3 战吼:抽一张圣盾随从和一张光环
    # 官方数据:Battlecry: Draw a Divine Shield minion and an Aura.
    
    def play(self):
        # 抽一张圣盾随从
        yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + DIVINE_SHIELD)
        # 抽一张光环牌 (Aura 类型的法术)
        # 光环牌通常是持续效果的法术,使用 SPELL 类型过滤
        # 在炉石中,Aura 通常指有持续时间的法术
        yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)


# EPIC

class TOY_716:
    """光速抢购 - Flash Sale
    Summon a 1/2 Mech with Divine Shield and Taunt. Give your minions +1/+2.
    召唤一个1/2并具有圣盾和嘲讽的机械,使你的所有随从+1/+2
    """
    # 4费法术 召唤一个1/2圣盾嘲讽机械,使所有友方随从+1/+2
    # 官方数据:Summon a 1/2 Mech with Divine Shield and Taunt. Give your minions +1/+2.
    
    def play(self):
        # 召唤一个1/2圣盾嘲讽机械 (使用 Token)
        yield Summon(CONTROLLER, "TOY_716t")
        # 使所有友方随从+1/+2
        yield Buff(FRIENDLY_MINIONS, "TOY_716e")


class TOY_809:
    """纸板魔像 - Cardboard Golem
    Battlecry: Increase the duration of Auras in your hand, deck, and battlefield by 1.
    战吼:使你的手牌、牌库和战场上的光环的持续时间增加1
    """
    # 3费 3/3 战吼:使手牌、牌库和战场上的光环持续时间+1
    # 官方数据:Battlecry: Increase the duration of Auras in your hand, deck, and battlefield by 1.
    
    def play(self):
        # 增加光环的持续时间
        # 光环通常是有 COOLDOWN 标签的卡牌
        # 遍历手牌、牌库和战场上的所有卡牌
        targets = (FRIENDLY_HAND + FRIENDLY_DECK + FRIENDLY_MINIONS).eval(self.game, self)
        
        for target in targets:
            # 检查是否是光环类型的卡牌 (有持续时间的法术/随从)
            if hasattr(target, 'tags') and GameTag.COOLDOWN in target.tags:
                # 增加持续时间 (COOLDOWN 值+1)
                current_cooldown = target.tags.get(GameTag.COOLDOWN, 0)
                target.tags[GameTag.COOLDOWN] = current_cooldown + 1


# LEGENDARY

class TOY_812:
    """皮普希·彩蹄 - Pipsi Painthoof
    [x]Deathrattle: Summon a random Divine Shield, Rush, and Taunt minion from your deck.
    亡语:从你的牌库中召唤一个随机的同时具有圣盾、突袭和嘲讽的随从
    """
    # 7费 4/4 亡语:从牌库中召唤一个同时具有圣盾、突袭和嘲讽的随从
    # 官方数据:Deathrattle: Summon a random Divine Shield, Rush, and Taunt minion from your deck.
    
    def deathrattle(self):
        # 从牌库中找到同时具有圣盾、突袭和嘲讽的随从
        minions = (FRIENDLY_DECK + MINION + DIVINE_SHIELD + RUSH + TAUNT).eval(self.game, self)
        
        if minions:
            # 随机选择一个并召唤
            minion = yield RandomChoice(minions)
            if minion:
                yield Summon(CONTROLLER, minion[0])


class TOY_813:
    """玩具队长塔林姆 - Toy Captain Tarim
    [x]Miniaturize Taunt. Battlecry: Set a minion's Attack and Health to this minion's.
    微缩 嘲讽 战吼:将一个随从的攻击力和生命值变为与本随从相同
    """
    # 5费 3/7 微缩 嘲讽
    # 战吼:将一个随从的攻击力和生命值变为与本随从相同
    # 官方数据:Miniaturize Taunt. Battlecry: Set a minion's Attack and Health to this minion's.
    taunt = True
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 将目标的攻击力和生命值设置为本随从的属性值
            yield Buff(TARGET, "TOY_813e3", atk=self.atk, max_health=self.max_health)


# ========================================
# Buff 定义
# ========================================

class MIS_700e:
    """武器增强 - +1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.DURABILITY: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_810e:
    """画师的美德 Buff - +1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_881e:
    """光鲜包装 Buff - +2/+3"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_716e:
    """光速抢购 Buff - +1/+2"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_813e3:
    """塔林姆的祝福 - 设置攻击力和生命值"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def apply(self, target):
        # 设置攻击力和生命值
        target.atk = self.atk
        target.max_health = self.max_health
        target.health = self.max_health


class TOY_808e:
    """工匠光环 Buff - 持续3回合的回合结束效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化剩余回合数
        self.turns_remaining = 3
    
    # 回合结束时触发
    events = OWN_TURN_END.on(
        lambda self, player: [
            # 召唤一个随机6费随从
            Summon(CONTROLLER, RandomCollectible(cost=6, type=CardType.MINION)),
            # 减少剩余回合数并检查是否移除
            self._decrease_turns(),
        ]
    )
    
    def _decrease_turns(self):
        """减少剩余回合数,如果为0则移除"""
        self.turns_remaining -= 1
        if self.turns_remaining <= 0:
            # 移除自己
            return [Destroy(SELF)]
        return []


