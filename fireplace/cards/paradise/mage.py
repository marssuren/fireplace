"""
胜地历险记 - MAGE
"""
from ..utils import *


# COMMON

class VAC_435:
    """落难的大法师 - Marooned Archmage
    Your first spell each turn costs (2) less.
    你每个回合使用的第一张法术牌的法力值消耗减少（2）点。
    """
    # 光环效果：当本回合还未施放法术时（spells_played_this_turn == 0），手牌法术减2费
    # 当第一张法术打出后，spells_played_this_turn 变为 1，光环失效
    auras = [
        Buff(FRIENDLY_HAND + SPELL, "VAC_435e")
    ]


class VAC_435e:
    """落难的大法师减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 条件：本回合还未施放法术
    def cost(self, i):
        if self.owner.controller.spells_played_this_turn == 0:
            return i - 2
        return None


class VAC_520:
    """银樽海韵 - Seabreeze Chalice
    Deal $2 damage randomly split among all enemy minions. (3 Drinks left!)
    造成$2点伤害，随机分配到所有敌方随从身上。（还剩3杯！）
    """
    # 饮品法术：使用后返回手牌，最多使用3次
    # ImmuneToSpellpower: 不受法术伤害加成影响
    
    def play(self):
        # 造成2点伤害，随机分配到所有敌方随从
        for _ in range(2):
            targets = list(ENEMY_MINIONS.eval(self.game, self))
            if targets:
                target = self.game.random.choice(targets)
                yield Hit(target, 1)
        
        # 饮品法术机制：使用后返回手牌，减少剩余次数
        # 第一次使用（3杯）-> 返回2杯版本
        yield Give(CONTROLLER, "VAC_520t")


class VAC_522:
    """潮汐之池 - Tide Pools
    Discover a spell that costs (3) or less. After you cast a spell, reopen this.
    发现一张法力值消耗小于或等于（3）点的法术牌。在你施放一个法术后，重新开启本地标。
    """
    def activate(self):
        # 发现一张3费以下的法术牌
        yield Discover(CONTROLLER, RandomSpell(cost_max=3))
    
    # 施放法术后重新开启地标
    events = Play(CONTROLLER, SPELL).after(
        Refresh(SELF)
    )


class WORK_012:
    """抱团 - Huddle Up
    Fill your board with random Naga.
    用随机纳迦填满你的面板。
    """
    def play(self):
        # 填满场面（最多7个随从）
        space = self.controller.max_minions - len(self.controller.field)
        for _ in range(space):
            # 召唤随机纳迦
            yield Summon(CONTROLLER, RandomMinion(race=Race.NAGA))


# RARE

class VAC_431:
    """畅游海底 - Under the Sea
    Draw a different spell. Summon a random minion of that spell's Cost.
    抽一张与本牌不同的法术牌，随机召唤一个法力值消耗与其相同的随从。
    """
    def play(self):
        # 抽一张法术牌
        drawn = yield Draw(CONTROLLER)
        
        if drawn and drawn[0].type == CardType.SPELL and drawn[0].id != "VAC_431":
            spell_cost = drawn[0].cost
            # 召唤一个相同费用的随机随从
            yield Summon(CONTROLLER, RandomMinion(cost=spell_cost))


class VAC_443:
    """冲浪章鱼 - Surfalopod
    Battlecry: The next spell you draw is Cast When Drawn.
    战吼：使你抽到的下一张法术牌获得抽到时施放效果。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给玩家添加一个效果：下一张抽到的法术获得抽到时施放
        yield Buff(CONTROLLER, "VAC_443e")


class VAC_443e:
    """冲浪章鱼效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听抽牌事件
    events = Draw(CONTROLLER).after(
        lambda self, target, card: [
            Buff(card, "VAC_443e2") if card.type == CardType.SPELL else None,
            Destroy(SELF)  # 移除此效果（无论抽到的是否是法术）
        ]
    )


class VAC_443e2:
    """抽到时施放效果 - Card Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.TOPDECK: True}
    
    # 抽到时施放
    cast_when_drawn = Play(CONTROLLER, OWNER)


class VAC_953:
    """浪潮涌起 - Rising Waves
    Deal $2 damage to all minions. If none die, deal $2 more.
    对所有随从造成$2点伤害。如果没有随从死亡，再造成$2点。
    """
    def play(self):
        # 记录场上所有随从
        minions_before = list(self.game.board)
        
        # 对所有随从造成2点伤害
        yield Hit(ALL_MINIONS, 2)
        
        # 检查是否有随从死亡
        minions_after = list(self.game.board)
        if len(minions_before) == len(minions_after):
            # 没有随从死亡，再造成2点伤害
            yield Hit(ALL_MINIONS, 2)


class WORK_026:
    """失火 - Burndown
    Draw 3 cards and light them on fire. In 3 turns, any still in hand are destroyed!
    抽三张牌并将其点燃。3回合后，摧毁其中仍在手中的牌。
    """
    def play(self):
        # 抽3张牌
        for _ in range(3):
            drawn = yield Draw(CONTROLLER)
            if drawn and drawn[0].zone == Zone.HAND:
                # 给抽到的牌添加"点燃"标记
                yield Buff(drawn[0], "WORK_026e")


class WORK_026e:
    """失火点燃效果 - Card Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 记录剩余回合数
        self.turns_remaining = 3
    
    # 监听回合开始，倒计时
    events = OWN_TURN_BEGIN.on(
        lambda self, player: (
            setattr(self, 'turns_remaining', self.turns_remaining - 1),
            Destroy(OWNER) if self.turns_remaining <= 0 and OWNER.zone == Zone.HAND else None
        )
    )


# EPIC

class VAC_428:
    """顺水漂流 - Go with the Flow
    Choose a minion. If it's an enemy, Freeze it. If it's friendly, give it Spell Damage +1.
    选择一个随从。如果是敌方随从，将其冻结；如果是友方随从，使其获得法术伤害+1。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if self.target.controller == self.controller.opponent:
            # 敌方随从：冻结
            yield Freeze(TARGET)
        else:
            # 友方随从：法术伤害+1
            yield Buff(TARGET, "VAC_428e")


class VAC_428e:
    """顺水漂流增益效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.SPELLPOWER: 1}


class VAC_509:
    """海啸 - Tsunami
    Summon three 3/6 Water Elementals that Freeze. They attack random enemies.
    召唤三个3/6的可以冻结攻击目标的水元素，并使其随机攻击敌人。
    """
    def play(self):
        # 召唤3个水元素 Token
        elementals = yield Summon(CONTROLLER, "VAC_509t") * 3
        
        # 让每个水元素攻击随机敌人
        # 检查 elementals 是否存在且可迭代
        if elementals:
            for elemental in elementals:
                if elemental and elemental.zone == Zone.PLAY:
                    enemies = list(ENEMY_CHARACTERS.eval(self.game, self))
                    if enemies:
                        target = self.game.random.choice(enemies)
                        yield Attack(elemental, target)


# LEGENDARY

class VAC_424:
    """沙滩塑形师蕾拉 - Raylla, Sand Sculptor
    Paladin Tourist. After you cast a spell, summon a random 2-Cost minion and give it Divine Shield.
    圣骑士游客。在你施放一个法术后，随机召唤一个法力值消耗为（2）的随从并使其获得圣盾。
    """
    # 施放法术后触发
    def _after_spell_cast(self, player, played_card, target=None):
        """施放法术后的触发效果"""
        # 召唤一个2费随从
        minion = yield Summon(CONTROLLER, RandomMinion(cost=2))
        if minion:
            # 给予圣盾
            yield SetTags(minion[0], {GameTag.DIVINE_SHIELD: True})
    
    events = Play(CONTROLLER, SPELL).after(_after_spell_cast)


class VAC_524:
    """海潮之王泰德 - King Tide
    Battlecry: Both players' spells cost (5) until the end of your next turn.
    战吼：直到你的下个回合结束，双方玩家的法术的法力值消耗为（5）点。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给双方玩家添加效果：法术费用变为5
        yield Buff(CONTROLLER, "VAC_524e")
        yield Buff(OPPONENT, "VAC_524e")


class VAC_524e:
    """海潮之王泰德效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 记录剩余回合数（持续到施放者的下个回合结束）
        self.turns_remaining = 2  # 当前回合结束 + 下个回合
    
    # 光环效果：手牌中的法术费用设置为5
    auras = [
        Buff(FRIENDLY_HAND + SPELL, "VAC_524e2")
    ]
    
    # 监听回合结束,倒计时
    events = OWN_TURN_END.on(
        lambda self, player: (
            setattr(self, 'turns_remaining', getattr(self, 'turns_remaining', 2) - 1),
            Destroy(SELF) if getattr(self, 'turns_remaining', 2) <= 0 else None
        )
    )


class VAC_524e2:
    """法术费用设置为5"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost = SET(5)


class WORK_063:
    """传送门操控师斯奇拉 - Portalmancer Skyla
    Rogue Tourist. Battlecry: Swap the Costs of the lowest and highest Cost spells in your hand.
    潜行者游客。战吼：使你手牌中法力值消耗最低和最高的法术牌的法力值消耗互换。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 获取手牌中的所有法术
        spells = [card for card in self.controller.hand if card.type == CardType.SPELL]
        
        if len(spells) < 2:
            return  # 少于2张法术，无法交换
        
        # 找到最低和最高费用的法术
        min_spell = min(spells, key=lambda c: c.cost)
        max_spell = max(spells, key=lambda c: c.cost)
        
        if min_spell == max_spell:
            return  # 同一张牌，无需交换
        
        # 记录原始费用
        min_cost = min_spell.cost
        max_cost = max_spell.cost
        
        # 使用 COST_SET 标签直接设置费用
        # 给最低费法术设置为最高费
        yield Buff(min_spell, "WORK_063e", cost_set=max_cost)
        # 给最高费法术设置为最低费
        yield Buff(max_spell, "WORK_063e", cost_set=min_cost)


class WORK_063e:
    """费用设置效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, cost_set=0, **kwargs):
        super().__init__(*args, **kwargs)
        self._cost_set = cost_set
    
    def cost(self, i):
        # 如果_cost_set属性存在,返回设置的费用;否则返回原值
        if hasattr(self, '_cost_set'):
            return self._cost_set
        return i
