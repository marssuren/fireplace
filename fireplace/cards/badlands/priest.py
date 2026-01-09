"""
决战荒芜之地 - PRIEST
"""
from ..utils import *


# COMMON

class DEEP_023:
    """隐藏宝石 - Hidden Gem
    潜行。在你的回合结束时，为所有友方角色恢复2点生命值。
    """
    # Type: MINION | Cost: 2 | Rarity: COMMON | Stats: 0/2 | Mechanics: STEALTH, TRIGGER_VISUAL
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.STEALTH: True,
    }

    # 回合结束时，为所有友方角色恢复2点生命值
    events = OWN_TURN_END.on(Heal(FRIENDLY_CHARACTERS, 2))


class DEEP_026:
    """大地坠饰 - Pendant of Earth
    从你的牌库中发现一张随从牌，为你的英雄恢复等同于其法力值消耗的生命值。
    """
    # Type: SPELL | Cost: 3 | Rarity: COMMON | Mechanics: DISCOVER
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }

    def play(self):
        # 从牌库中发现一张随从牌
        discovered_card = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
        )

        if discovered_card:
            # 为英雄恢复等同于其法力值消耗的生命值
            heal_amount = discovered_card.cost
            yield Heal(FRIENDLY_HERO, heal_amount)


class WW_053:
    """飞车劫掠 - Tram Heist
    获取你的对手上回合使用的每张卡牌的各一张复制。
    """
    # Type: SPELL | Cost: 4 | Rarity: COMMON
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }

    def play(self):
        # 获取对手上回合使用的所有卡牌
        if hasattr(self.controller.opponent, 'cards_played_last_turn'):
            for card_id in self.controller.opponent.cards_played_last_turn:
                # 为己方玩家创建该卡牌的复制
                copy = self.controller.card(card_id, self.controller)
                yield Give(CONTROLLER, copy)


class WW_381:
    """受伤的搬运工 - Injured Hauler
    战吼：对本随从造成4点伤害。过量治疗：对所有敌方随从造成2点伤害。
    """
    # Type: MINION | Cost: 3 | Rarity: COMMON | Stats: 0/7 | Mechanics: BATTLECRY, OVERHEAL
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 7,
        GameTag.COST: 3,
    }

    def play(self):
        # 战吼：对本随从造成4点伤害
        yield Hit(SELF, 4)

    # 过量治疗：对所有敌方随从造成2点伤害
    overheal = Hit(ENEMY_MINIONS, 2)


class WW_395:
    """神圣泉水 - Holy Springwater
    为一个受伤的角色恢复8点生命值。将超过目标生命值上限的治疗量存入法力值消耗为(1)的瓶子。
    """
    # Type: SPELL | Cost: 2 | Rarity: COMMON
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }

    def play(self):
        target = self.target
        # 记录治疗前的受伤值
        damage_before = target.damage

        # 恢复8点生命值
        yield Heal(target, 8)

        # 计算实际过量治疗量
        damage_after = target.damage
        actual_healing = damage_before - damage_after
        excess_healing = 8 - actual_healing

        # 如果有超出部分，生成瓶子
        if excess_healing > 0:
            yield Give(CONTROLLER, "WW_395t")


# RARE

class DEEP_021:
    """暗言术：窃 - Shadow Word: Steal
    将一个敌方随从移回你的手牌。
    """
    # Type: SPELL | Cost: 5 | Rarity: RARE | Mechanics: SHADOW
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    # 将敌方随从移回己方手牌（偷取）
    play = Steal(TARGET)


class DEEP_024:
    """亮石旋岩虫 - Glowstone Gyreworm
    吸血。快枪：造成5点伤害。锻造：将快枪改为战吼。
    """
    # Type: MINION | Cost: 5 | Rarity: RARE | Stats: 4/4 | Mechanics: FORGE, LIFESTEAL, QUICKDRAW
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.LIFESTEAL: True,
    }

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True}

    # 锻造升级为 DEEP_024t
    forge = "DEEP_024t"

    def play(self):
        # 普通版本：快枪触发造成5点伤害
        if self.drawn_this_turn and self.target:
            yield Hit(TARGET, 5)


class DEEP_024t:
    """亮石旋岩虫 - Glowstone Gyreworm (Forged)
    吸血。战吼：造成5点伤害。
    """
    # Type: MINION | Cost: 5 | Rarity: RARE | Stats: 4/4 | Mechanics: BATTLECRY, LIFESTEAL
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.LIFESTEAL: True,
    }

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True}

    # 锻造版本：战吼触发造成5点伤害（不检查 drawn_this_turn）
    play = Hit(TARGET, 5)


class DEEP_025:
    """破碎映像 - Shattered Reflections
    选择一个随从，将一个它的复制置入你的手牌，牌库和战场。
    """
    # Type: SPELL | Cost: 5 | Rarity: RARE
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        # 将目标随从的复制置入手牌
        yield Give(CONTROLLER, Copy(TARGET))
        # 将目标随从的复制洗入牌库
        yield Shuffle(CONTROLLER, Copy(TARGET))
        # 在战场上召唤目标随从的复制
        yield Summon(CONTROLLER, Copy(TARGET))


class WW_052:
    """萤光虫群 - Swarm of Lightbugs
    召唤10个1/1并具有吸血的萤光虫。将超过随从数量上限的萤光虫存入法力值消耗为(1)的瓶子。
    """
    # Type: SPELL | Cost: 5 | Rarity: RARE
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }

    def play(self):
        # 记录召唤前的随从数量
        field_size_before = len(self.controller.field)
        max_field_size = 7  # 战场最大随从数量

        # 尝试召唤10个萤光虫
        for _ in range(10):
            yield Summon(CONTROLLER, "WW_052t")

        # 计算实际召唤的数量和超出的数量
        field_size_after = len(self.controller.field)
        summoned = field_size_after - field_size_before
        excess = 10 - summoned

        # 如果有超出部分，生成瓶子
        if excess > 0:
            yield Give(CONTROLLER, "WW_052t2")


class WW_052t:
    """萤光虫 - Lightbug (Token)"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.LIFESTEAL: True,
    }


class WW_387:
    """口渴的流浪者 - Thirsty Drifter
    嘲讽。在本局对战中，你每使用过一张法力值消耗为(1)的牌，本牌的法力值消耗便减少(1)点。
    """
    # Type: MINION | Cost: 6 | Rarity: RARE | Stats: 4/6 | Mechanics: TAUNT
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,
        GameTag.COST: 6,
        GameTag.TAUNT: True,
    }

    @property
    def cost_mod(self):
        # 计算本局对战中使用过的1费卡牌数量
        one_cost_played = sum(1 for card in self.controller.cards_played_this_game if card.cost == 1)
        return -one_cost_played


class WW_393:
    """影叶入侵 - Invasive Shadeleaf
    对一个敌方随从造成$10点伤害。将超过目标生命值的伤害存入法力值消耗为(1)的瓶子。
    """
    # Type: SPELL | Cost: 4 | Rarity: RARE | Mechanics: ImmuneToSpellpower
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
        GameTag.ImmuneToSpellpower: True,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        target = self.target
        # 记录伤害前的生命值
        health_before = target.health

        # 造成10点伤害
        yield Hit(target, 10)

        # 计算超出伤害量（如果随从死亡，超出部分 = 10 - 原生命值）
        if target.dead:
            excess_damage = 10 - health_before
        else:
            excess_damage = 0

        # 如果有超出部分，生成瓶子
        if excess_damage > 0:
            yield Give(CONTROLLER, "WW_393t")


# EPIC

class WW_384:
    """和善的银行职员 - Benevolent Banker
    战吼：从你的牌库中发现一张法术牌。快枪：改为从敌方牌库中发现。
    """
    # Type: MINION | Cost: 3 | Rarity: EPIC | Stats: 3/4 | Mechanics: BATTLECRY, DISCOVER, QUICKDRAW
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }

    def play(self):
        if self.drawn_this_turn:
            # 快枪：从敌方牌库中发现法术牌
            yield Discover(CONTROLLER, RANDOM(ENEMY_DECK + SPELL))
        else:
            # 普通：从己方牌库中发现法术牌
            yield Discover(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL))


class WW_600:
    """夺舍对射 - Posse Possession
    召唤你对手手牌中一个随机随从的4/4的复制。
    """
    # Type: SPELL | Cost: 4 | Rarity: EPIC
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }

    def play(self):
        # 从对手手牌中随机选择一个随从
        minions_in_hand = [card for card in self.controller.opponent.hand if card.type == CardType.MINION]
        if minions_in_hand:
            import random
            target_minion = random.choice(minions_in_hand)
            # 召唤一个4/4的复制
            copy = self.controller.card(target_minion.id, self.controller)
            copy.tags[GameTag.ATK] = 4
            copy.tags[GameTag.HEALTH] = 4
            yield Summon(CONTROLLER, copy)


# LEGENDARY

class WW_392:
    """荒地奇兵伊莉斯 - Elise, Badlands Savior
    战吼：如果你的套牌里没有相同的牌，随机召唤你牌库中4个随从的5/5的复制。
    """
    # Type: MINION | Cost: 8 | Rarity: LEGENDARY | Stats: 5/5 | Mechanics: BATTLECRY
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 8,
    }

    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK)

    def play(self):
        if self.powered_up:
            # 从牌库中随机选择4个随从
            minions_in_deck = [card for card in self.controller.deck if card.type == CardType.MINION]
            if minions_in_deck:
                import random
                # 随机选择最多4个随从
                selected = random.sample(minions_in_deck, min(4, len(minions_in_deck)))
                for minion in selected:
                    # 召唤5/5的复制
                    copy = self.controller.card(minion.id, self.controller)
                    copy.tags[GameTag.ATK] = 5
                    copy.tags[GameTag.HEALTH] = 5
                    yield Summon(CONTROLLER, copy)


class WW_394:
    """皮普，强力水霸 - Pip the Potent
    战吼：复制你手牌中法力值消耗为(1)的牌。
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 3/3 | Mechanics: BATTLECRY
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }

    def play(self):
        # 复制手牌中所有法力值消耗为1的牌
        one_cost_cards = [card for card in self.controller.hand if card.cost == 1 and card != self]
        for card in one_cost_cards:
            yield Give(CONTROLLER, Copy(card))


# ========== Token Cards ==========

class WW_395t:
    """治疗瓶 - Bottle of Healing (Token)
    恢复8点生命值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    play = Heal(TARGET, 8)


class WW_393t:
    """伤害瓶 - Bottle of Damage (Token)
    对一个敌方随从造成$10点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    play = Hit(TARGET, 10)


class WW_052t2:
    """萤光虫瓶 - Bottle of Lightbugs (Token)
    召唤10个1/1并具有吸血的萤光虫。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }

    def play(self):
        # 召唤10个萤光虫
        for _ in range(10):
            yield Summon(CONTROLLER, "WW_052t")
