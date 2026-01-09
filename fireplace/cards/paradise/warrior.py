"""
胜地历险记 - WARRIOR
"""
from ..utils import *


# COMMON

class VAC_337:
    """灶头厨师 - Line Cook
    [x]Tradeable Taunt. When you draw this, get a copy of it.
    可交易，嘲讽。当你抽到本牌时，获得一张本牌的复制。
    """
    requirements = {}
    mechanics = [GameTag.TAUNT, GameTag.TRADEABLE]

    # 当抽到这张牌时，给玩家一张复制
    events = Draw(CONTROLLER, SELF).after(
        Give(CONTROLLER, Copy(SELF))
    )


class VAC_338:
    """腱力金杯 - Cup o' Muscle
    [x]Give a minion in your hand +2/+1. <i>(3 Drinks left!)</i>
    给你手牌中的一个随从+2/+1。（剩余3杯！）
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_IN_HAND: 0}

    def play(self):
        # 给手牌中的目标随从 +2/+1
        yield Buff(TARGET, "VAC_338e")
        # 给玩家一张 VAC_338t (2杯剩余版本)
        yield Give(CONTROLLER, "VAC_338t")

class VAC_338e:
    """腱力金杯 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    def apply(self, target):
        target.atk += 2
        target.max_health += 1


class VAC_339:
    """芝士怪物 - Muensterosity
    [x]Taunt. At the end of your turn, summon an Elemental with stats equal to this minion's.
    嘲讽。在你的回合结束时，召唤一个属性等同于本随从的元素。
    """
    mechanics = [GameTag.TAUNT, GameTag.TRIGGER_VISUAL]

    # 在回合结束时，召唤一个属性等同于本随从的元素
    events = OWN_TURN_END.on(
        lambda self, source: [
            Summon(CONTROLLER, ExactCopy(source))
        ]
    )


class WORK_023:
    """合金顾问 - Alloy Advisor
    Taunt. Whenever this takes damage, gain 3 Armor.
    嘲讽。每当本随从受到伤害时，获得3点护甲值。
    """
    mechanics = [GameTag.TAUNT, GameTag.TRIGGER_VISUAL]

    # 监听本随从受到伤害事件
    events = Damage(SELF).on(
        GainArmor(FRIENDLY_HERO, 3)
    )


# RARE

class VAC_341:
    """断生鱿鱼 - Undercooked Calamari
    [x]Battlecry: Destroy an enemy minion with Attack less than or equal to this minion's.
    战吼：消灭一个攻击力小于或等于本随从攻击力的敌方随从。
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 消灭攻击力小于或等于本随从攻击力的敌方随从
        if TARGET and TARGET.atk <= self.atk:
            yield Destroy(TARGET)


class VAC_526:
    """炭火 - Char
    Deal $7 damage to a minion. Give a minion in your hand stats equal to the excess damage.
    对一个随从造成$7点伤害。使你手牌中的一个随从获得等同于超额伤害的属性。
    """
    mechanics = [GameTag.ImmuneToSpellpower]
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 对目标造成7点伤害
        target_health = TARGET.health
        yield Hit(TARGET, 7)

        # 计算超额伤害
        excess_damage = max(0, 7 - target_health)

        if excess_damage > 0:
            # 给手牌中的一个随机随从 +X/+X (X = 超额伤害)
            minions_in_hand = self.controller.hand.filter(type=CardType.MINION)
            if minions_in_hand:
                target_minion = self.game.random.choice(minions_in_hand)
                yield Buff(target_minion, "VAC_526e", atk=excess_damage, health=excess_damage)

class VAC_526e:
    """炭火 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    def apply(self, target):
        target.atk += self.tags.get("atk", 0)
        target.max_health += self.tags.get("health", 0)


class VAC_528:
    """自助大餐 - All You Can Eat
    Draw three minions of different minion types.
    抽取三个不同种族的随从。
    """
    def play(self):
        # 从牌库中抽取3个不同种族的随从
        drawn_races = set()
        for card in list(self.controller.deck):  # 使用list避免迭代时修改
            if card.type == CardType.MINION and card.race != Race.INVALID and card.race not in drawn_races:
                yield ForceDraw(card)
                drawn_races.add(card.race)
                if len(drawn_races) >= 3:
                    break


class WORK_021:
    """预留泊位 - Reserved Spot
    [x]Give a random minion in your hand +4/+4. If it's the only one there, reduce its Cost by (2).
    随机使你手牌中的一个随从获得+4/+4。如果它是你手牌中唯一的随从，则使其法力值消耗减少（2）点。
    """
    def play(self):
        # 找到手牌中的所有随从
        minions_in_hand = self.controller.hand.filter(type=CardType.MINION)

        if minions_in_hand:
            # 随机选择一个随从
            target = self.game.random.choice(minions_in_hand)

            # 给予 +4/+4
            yield Buff(target, "WORK_021e")

            # 如果是唯一的随从，减少2费
            if len(minions_in_hand) == 1:
                yield Buff(target, "WORK_021e2")

class WORK_021e:
    """预留泊位 Buff (+4/+4)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    def apply(self, target):
        target.atk += 4
        target.max_health += 4

class WORK_021e2:
    """预留泊位 Buff (减费)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    class Hand:
        def cost_func(self, i):
            return max(0, i - 2)


class WORK_022:
    """打卡 - Punch Card
    Give your hero +3 Attack and "Also damages adjacent minions" this turn.
    在本回合中，使你的英雄获得+3攻击力和"同时对相邻的随从造成伤害"。
    """
    def play(self):
        # 给英雄 +3 攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "WORK_022e")

class WORK_022e:
    """打卡 Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True
    }

    def apply(self, target):
        target.atk += 3

    # 添加 CLEAVE 效果（攻击时同时伤害相邻随从）
    events = Attack(FRIENDLY_HERO).after(CLEAVE)


# EPIC

class VAC_527:
    """龙族美餐 - Draconic Delicacy
    Rush, Elusive. Can only take 1 damage at a time.
    突袭，扰魔。每次只能受到1点伤害。
    """
    mechanics = [GameTag.ELUSIVE, GameTag.RUSH, GameTag.TRIGGER_VISUAL]

    # 监听本随从即将受到伤害的事件，将伤害限制为1
    events = Predamage(SELF).on(
        lambda self, source, target, amount: [
            SetTag(target, {GameTag.PREDAMAGE: min(amount, 1)})
        ]
    )


class VAC_533:
    """食物大战 - Food Fight
    Summon a 0/4 Entrée for your opponent. When it dies, summon a minion from your deck.
    为你的对手召唤一个0/4的主菜。当它死亡时，从你的牌库中召唤一个随从。
    """
    def play(self):
        # 为对手召唤一个 0/4 的主菜 Token
        entrees = yield Summon(OPPONENT, "VAC_533t")

        if entrees:
            entree = entrees[0]
            # 给这个 Token 添加一个 Buff，记录创建者
            yield Buff(entree, "VAC_533e")

class VAC_533e:
    """食物大战 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 当这个随从死亡时，从创建者（对手）的牌库中召唤一个随从
    events = Death(OWNER).on(
        lambda self, source, target: [
            Summon(source.controller.opponent, RandomMinion(source.controller.opponent.deck.filter(type=CardType.MINION)))
        ] if source.controller.opponent.deck.filter(type=CardType.MINION) else []
    )


# LEGENDARY

class VAC_340:
    """饥饿食客哈姆 - Hamm, the Hungry
    [x]Druid Tourist. Taunt. At the end of your turn, eat a minion in the enemy's deck to gain +2/+2.
    德鲁伊游客。嘲讽。在你的回合结束时，吃掉敌方牌库中的一个随从并获得+2/+2。
    """
    mechanics = [GameTag.TAUNT, GameTag.TRIGGER_VISUAL]

    def OWN_TURN_END(self):
        # 找到敌方牌库中的随从
        enemy_minions = [c for c in self.controller.opponent.deck if c.type == CardType.MINION]
        if enemy_minions:
            # 随机选择一个并移除
            minion = self.game.random.choice(enemy_minions)
            yield Destroy(minion)
            # 获得 +2/+2
            yield Buff(self, "VAC_340e")

class VAC_340e:
    """饥饿食客哈姆 Buff"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    def apply(self, target):
        target.atk += 2
        target.max_health += 2


class VAC_525:
    """黑麦切割者 - The Ryecleaver
    [x]Battlecry and Deathrattle: Get a Slice of Bread. <i>(Get 2 to Sandwich any minions in between!)</i>
    战吼和亡语：获得一片面包。（获得2片来夹住中间的随从！）
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DEATHRATTLE]

    def play(self):
        # 战吼：获得一片面包
        yield Give(CONTROLLER, "VAC_525t")

    def deathrattle(self):
        # 亡语：获得一片面包
        yield Give(CONTROLLER, "VAC_525t")
