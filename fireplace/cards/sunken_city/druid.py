# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 德鲁伊
"""

from ..utils import *


class TID_081:
    """Aquatic Form - 水栖形态
    2费法术 抽一张牌。如果你在本回合打出过娜迦牌，再抽一张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        抽一张牌，如果本回合打出过娜迦，再抽一张
        """
        yield Draw(CONTROLLER)
        
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            yield Draw(CONTROLLER)


class TID_082:
    """Moonlit Guidance - 月光指引
    2费法术 抽一张牌。如果你在本回合打出过法术牌，再抽一张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        抽一张牌，如果本回合打出过法术，再抽一张
        """
        yield Draw(CONTROLLER)
        
        # 检查本回合是否打出过法术
        spell_played_this_turn = any(
            card.type == CardType.SPELL
            for card in self.controller.cards_played_this_turn
        )
        
        if spell_played_this_turn:
            yield Draw(CONTROLLER)


class TID_084:
    """Bottomfeeder - 食腐者
    2费 2/2 战吼：探底。如果是野兽牌，使其获得+2/+2。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        探底，如果是野兽牌，使其获得+2/+2
        """
        yield Dredge(CONTROLLER)
        
        # 检查牌库顶的牌是否是野兽
        if self.controller.deck:
            top_card = self.controller.deck[0]
            if top_card.type == CardType.MINION and Race.BEAST in top_card.races:
                yield Buff(top_card, "TID_084e")


class TID_084e:
    """+2/+2"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class TSC_028:
    """Colaque - 科拉克
    7费 5/7 巨型+1 战吼：抽一张牌。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 7,
        GameTag.COST: 7,
    }
    # 巨型+1：召唤1个附属部件
    colossal_appendages = ["TSC_028t"]
    play = Draw(CONTROLLER)


class TSC_028t:
    """Colaque's Shell - 科拉克的壳
    3费 0/8 嘲讽
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 8,
        GameTag.COST: 3,
        GameTag.TAUNT: True,
    }


class TSC_031:
    """Flipper Friends - 划水好友
    4费法术 召唤两个2/2的水獭，并具有突袭。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    play = Summon(CONTROLLER, "TSC_031t") * 2


class TSC_031t:
    """Otter - 水獭
    2费 2/2 突袭
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RUSH: True,
    }


class TSC_032:
    """Planted Evidence - 栽赃证据
    1费法术 选择一项：将一张法术牌或一张野兽牌洗入对手的牌库。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    choose = [
        "TSC_032a",  # 法术牌
        "TSC_032b",  # 野兽牌
    ]


class TSC_032a:
    """Planted Evidence (Spell)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    play = ShuffleIntoDeck(OPPONENT, RandomSpell())


class TSC_032b:
    """Planted Evidence (Beast)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    play = ShuffleIntoDeck(OPPONENT, RandomMinion(race=Race.BEAST))


class TSC_034:
    """Glugg the Gulper - 吞食者格拉格
    7费 3/5 战吼：消灭一个敌方随从。如果你在本回合打出过娜迦牌，改为消灭所有敌方随从。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        """
        消灭一个敌方随从，如果本回合打出过娜迦，消灭所有敌方随从
        """
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            # 消灭所有敌方随从
            yield Destroy(ENEMY_MINIONS)
        else:
            # 消灭一个敌方随从
            yield Destroy(TARGET)


class TSC_035:
    """Feral Rage - 野性之怒
    3费法术 选择一项：造成4点伤害；或获得8点护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    choose = [
        "TSC_035a",  # 造成4点伤害
        "TSC_035b",  # 获得8点护甲
    ]


class TSC_035a:
    """Feral Rage (Damage)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)


class TSC_035b:
    """Feral Rage (Armor)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    play = GainArmor(FRIENDLY_HERO, 8)


class TSC_038:
    """Pestilent Swarm - 瘟疫虫群
    3费法术 召唤两个1/1的蝗虫，并具有突袭和剧毒。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Summon(CONTROLLER, "TSC_038t") * 2


class TSC_038t:
    """Locust - 蝗虫
    1费 1/1 突袭，剧毒
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.RUSH: True,
        GameTag.POISONOUS: True,
    }


class TSC_039:
    """Azsharan Gardens - 艾萨拉花园
    3费法术 抽一张牌。将一张"沉没的花园"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = (
        Draw(CONTROLLER),
        ShuffleIntoDeck(CONTROLLER, "TSC_039t"),
    )


class TSC_039t:
    """Sunken Gardens - 沉没的花园
    3费法术 抽三张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Draw(CONTROLLER) * 3


class TSC_656:
    """Miracle Growth - 奇迹生长
    7费法术 抽三张牌。召唤一个属性值等同于你的手牌数量并具有嘲讽的植物。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
    }
    
    def play(self):
        """
        抽三张牌，然后召唤一个属性等于手牌数量的植物
        """
        # 抽三张牌
        yield Draw(CONTROLLER) * 3
        
        # 获取手牌数量
        hand_size = len(self.controller.hand)
        
        # 召唤植物
        yield Summon(CONTROLLER, "TSC_656t", {
            GameTag.ATK: hand_size,
            GameTag.HEALTH: hand_size,
            GameTag.TAUNT: True
        })


class TSC_656t:
    """Plant - 植物
    Token随从，属性动态设置
    """
    tags = {
        GameTag.COST: 0,
        GameTag.TAUNT: True,
    }


class TSC_960:
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
    }


class TSC_031:
    """Flipper Friends - 鳍足朋友
    4费法术 召唤两个2/2的水獭，并具有突袭。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    play = Summon(CONTROLLER, "TSC_031t") * 2


class TSC_031t:
    """Otter - 水獭
    2费 2/2 突袭
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RUSH: True,
    }


class TSC_032:
    """Planted Evidence - 栽赃证据
    1费法术 选择一项：将一张法术牌或一张野兽牌洗入对手的牌库。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    choose = [
        "TSC_032a",  # 法术牌
        "TSC_032b",  # 野兽牌
    ]


class TSC_032a:
    """Planted Evidence (Spell)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    play = ShuffleIntoDeck(OPPONENT, RandomSpell())


class TSC_032b:
    """Planted Evidence (Beast)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    play = ShuffleIntoDeck(OPPONENT, RandomMinion(race=Race.BEAST))


class TSC_034:
    """Glugg the Gulper - 吞食者格拉格
    7费 3/5 战吼：消灭一个敌方随从。如果你在本回合打出过娜迦牌，改为消灭所有敌方随从。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        """
        消灭一个敌方随从，如果本回合打出过娜迦，消灭所有敌方随从
        """
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            # 消灭所有敌方随从
            yield Destroy(ENEMY_MINIONS)
        else:
            # 消灭一个敌方随从
            yield Destroy(TARGET)


class TSC_035:
    """Feral Rage - 野性之怒
    3费法术 选择一项：造成4点伤害；或获得8点护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    choose = [
        "TSC_035a",  # 造成4点伤害
        "TSC_035b",  # 获得8点护甲
    ]


class TSC_035a:
    """Feral Rage (Damage)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)


class TSC_035b:
    """Feral Rage (Armor)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    play = GainArmor(FRIENDLY_HERO, 8)


class TSC_038:
    """Pestilent Swarm - 瘟疫虫群
    3费法术 召唤两个1/1的蝗虫，并具有突袭和剧毒。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Summon(CONTROLLER, "TSC_038t") * 2


class TSC_038t:
    """Locust - 蝗虫
    1费 1/1 突袭，剧毒
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.RUSH: True,
        GameTag.POISONOUS: True,
    }


class TSC_039:
    """Azsharan Gardens - 艾萨拉花园
    3费法术 抽一张牌。将一张"沉没的花园"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = (
        Draw(CONTROLLER),
        ShuffleIntoDeck(CONTROLLER, "TSC_039t"),
    )


class TSC_039t:
    """Sunken Gardens - 沉没的花园
    3费法术 抽三张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Draw(CONTROLLER) * 3


class TSC_960:
    """Capture Coldtooth Mine - 占领寒齿矿洞
    2费法术 获得5点护甲值。如果你在本回合打出过娜迦牌，改为获得10点护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        获得5点护甲，如果本回合打出过娜迦，改为10点
        """
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        armor_amount = 10 if naga_played_this_turn else 5
        yield GainArmor(FRIENDLY_HERO, armor_amount)
