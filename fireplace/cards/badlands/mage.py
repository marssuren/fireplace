"""
决战荒芜之地 - MAGE
"""
from ..utils import *


# COMMON

class DEEP_004:
    """地幔塑型者 - Mantle Shaper
    本牌在你手中时，你每施放一个法术，本牌的法力值消耗便减少（1）点。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }

    # 每施放一个法术，减少（1）点法力值消耗
    cost_mod = -Attr(SELF, "spells_cast_while_in_hand")


class WW_009:
    """低温贮藏 - Cryopreservation
    冻结一个敌人。发掘一个宝藏。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FROST,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    play = Freeze(TARGET), Excavate(CONTROLLER)


class WW_424:
    """溢流熔岩 - Overflow Surger
    战吼：每有一个你使用过元素牌的连续的回合，召唤一个本随从的复制。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 4,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }

    def play(self):
        # 计算连续回合使用元素牌的次数
        # 使用核心的 elemental_streak 计数器
        consecutive_turns = getattr(self.controller, 'elemental_streak', 0)

        # 召唤对应数量的复制
        for _ in range(consecutive_turns):
            yield Summon(CONTROLLER, ExactCopy(SELF))


class WW_427:
    """夕阳漫射 - Sunset Volley
    造成$10点伤害，随机分配到所有敌人身上。随机召唤一个法力值消耗为(10)点的随从。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 9,
        GameTag.ImmuneToSpellpower: True,
    }

    play = [
        Hit(RANDOM_ENEMY_CHARACTER, 1) * 10,
        Summon(CONTROLLER, RandomMinion(cost=10))
    ]


# RARE

class DEEP_000:
    """召唤结界 - Summoning Ward
    奥秘：当你的回合开始时，召唤你法力值消耗最高的随从的一个复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
    }

    secret = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + HIGHEST_COST))
    )


class DEEP_002:
    """元素伙伴 - Elemental Companion
    随机召唤一个元素伙伴。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }

    # 随机召唤一个元素伙伴（从3个token中选择）
    play = Summon(CONTROLLER, RandomID("DEEP_002t", "DEEP_002t2", "DEEP_002t3"))


class WW_377:
    """热浪来袭 - Heat Wave
    对一个敌方随从及其相邻的随从造成$2点伤害。快枪：改为对所有敌人造成伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        # 快枪：本回合获得并立即使用时触发
        if self.drawn_this_turn:
            # 快枪效果：对所有敌人造成伤害
            yield Hit(ENEMY_CHARACTERS, 2)
        else:
            # 正常效果：对目标及其相邻随从造成伤害
            yield Hit(TARGET | TARGET_ADJACENT, 2)


class WW_425:
    """观星 - Stargazing
    抽一张不同的奥术法术牌。如果你在本回合中使用这张抽到的牌，则会施放两次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }

    def play(self):
        # 抽一张不同的奥术法术牌
        yield ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL + ARCANE - ID(self.id)))
        # 给抽到的牌添加"本回合施放两次"的buff
        drawn_card = ForceDraw.CARD
        if drawn_card:
            yield Buff(drawn_card, "WW_425e")


class WW_425e:
    """观星增益 - 本回合施放两次"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 当这张牌被使用时，再次触发其战吼效果
    events = [
        Play(OWNER, SELF).after(Battlecry(Play.CARD, Play.TARGET)),
        OWN_TURN_END.on(Destroy(SELF))
    ]


class WW_426:
    """矿工炎术师 - Blastmage Miner
    战吼：发掘一个宝藏。你每有一张手牌，便随机对一个敌人造成1点伤害。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 6,
    }

    def play(self):
        # 发掘一个宝藏
        yield Excavate(CONTROLLER)
        # 计算手牌数量（包括刚发掘的牌）
        hand_count = len(self.controller.hand)
        # 对每张手牌造成1点伤害
        for _ in range(hand_count):
            yield Hit(RANDOM_ENEMY_CHARACTER, 1)


# EPIC

class WW_422:
    """艾泽里特矿脉 - Azerite Vein
    奥秘：当敌人使用一张在本回合进入其手牌的卡牌时，获取一张法力值消耗为(0)点的复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
    }

    # 当敌方使用卡牌时触发
    # 检查该卡牌是否在本回合进入手牌（通过 turn_entered_hand 属性）
    def _on_enemy_play(self, source, target):
        card = target
        # 检查卡牌是否在本回合进入手牌
        if hasattr(card, 'turn_entered_hand') and card.turn_entered_hand == source.game.turn:
            # 获取一张法力值消耗为(0)点的复制
            copy = source.controller.card(card.id, source=source.controller)
            copy.cost = 0
            source.controller.give(copy)

    secret = Play(OPPONENT).on(
        lambda self, source, target: self._on_enemy_play(source, target)
    )


class WW_432:
    """神圣遗物学会研究员 - Reliquary Researcher
    战吼：如果你已发掘过两次，则施放两个随机的法师奥秘。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }

    def play(self):
        # 检查是否已发掘过至少两次
        excavate_count = getattr(self.controller, 'times_excavated', 0)
        if excavate_count >= 2:
            # 施放两个随机的法师奥秘
            yield CastSpell(RandomSpell(secret=True, card_class=CardClass.MAGE))
            yield CastSpell(RandomSpell(secret=True, card_class=CardClass.MAGE))


# LEGENDARY

class WW_429:
    """碎裂巨岩迈沙顿 - Mes'Adune the Fractured
    战吼：抽一张元素牌，将其拆成两半。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.ELITE: True,
    }

    def play(self):
        # 抽一张元素牌
        yield ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + ELEMENTAL))
        drawn_card = ForceDraw.CARD

        if drawn_card and drawn_card.type == CardType.MINION:
            # 移除抽到的牌
            yield Destroy(drawn_card)

            # 使用核心的 SplitCard 动作拆分卡牌
            half1, half2 = SplitCard(drawn_card).trigger(self)[0]

            # 将两张"一半"的牌置入手牌
            if half1 and half2:
                self.controller.give(half1)
                self.controller.give(half2)


class WW_430:
    """泰瑟兰·血望者 - Tae'thelan Bloodwatcher
    不在你初始套牌中的卡牌的法力值消耗减少(4)点（但不会少于1点）。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
        GameTag.ELITE: True,
    }

    # 光环效果：减少不在初始套牌中的卡牌的法力值消耗
    update = Refresh(FRIENDLY_HAND - STARTING_DECK, {GameTag.COST: -4})


# 元素伙伴 Token 定义
# 参考经典的动物伙伴（Huffer, Leokk, Misha）

class DEEP_002t:
    """霍法 - Hiffar (元素版 Huffer)
    冲锋
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.CHARGE: True,
    }


class DEEP_002t2:
    """卢克 - Luekk (元素版 Leokk)
    你的其他随从获得+1攻击力。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.AURA: True,
    }

    update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: +1})


class DEEP_002t3:
    """米绍 - Me'sho (元素版 Misha)
    嘲讽
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.TAUNT: True,
    }
