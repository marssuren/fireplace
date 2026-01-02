# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 术士
"""

from ..utils import *


class TID_710:
    """Bloodscent Vilefin - 血腥鱼人
    3费 3/4 战吼：消灭一个友方随从。如果是恶魔，抽一张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        """
        消灭一个友方随从，如果是恶魔，抽一张牌
        """
        is_demon = Race.DEMON in self.target.races
        
        yield Destroy(TARGET)
        
        if is_demon:
            yield Draw(CONTROLLER)


class TID_711:
    """Dragged Below - 拖入深渊
    2费法术 消灭一个攻击力小于或等于2的随从。探底。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_MAX_ATTACK: 2,
    }
    play = (
        Destroy(TARGET),
        Dredge(CONTROLLER),
    )


class TID_960:
    """Abyssal Wave - 深渊波浪
    2费法术 对所有随从造成$2点伤害。如果你在本回合打出过娜迦牌，改为造成$4点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        对所有随从造成2点伤害，如果打出过娜迦，改为4点
        """
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        damage = 4 if naga_played_this_turn else 2
        yield Hit(ALL_MINIONS, damage)


class TSC_055:
    """Azsharan Scavenger - 艾萨拉拾荒者
    2费 2/3 战吼：将一张"沉没的拾荒者"置于你的牌库底部。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    play = ShuffleIntoDeck(CONTROLLER, "TSC_055t")


class TSC_055t:
    """Sunken Scavenger - 沉没的拾荒者
    2费 2/3 战吼：抽一张牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    play = Draw(CONTROLLER)


class TSC_056:
    """Chum Bucket - 鱼饵桶
    2费法术 对你的英雄造成$2点伤害。召唤两个2/1的鱼人。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = (
        Hit(FRIENDLY_HERO, 2),
        Summon(CONTROLLER, "TSC_056t") * 2,
    )


class TSC_056t:
    """Murloc - 鱼人
    1费 2/1
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


class TSC_620:
    """Immolate - 献祭
    2费法术 对一个友方随从造成$3点伤害。对一个敌方随从造成$3点伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        """
        对友方和敌方随从各造成3点伤害
        """
        yield Hit(TARGET, 3)
        
        # 对一个随机敌方随从造成3点伤害
        yield Hit(RANDOM_ENEMY_MINION, 3)


class TSC_621:
    """Abyssal Depths - 深渊深处
    3费法术 抽两张牌。如果你的手牌中有娜迦牌，再抽一张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        """
        抽两张牌，如果手牌中有娜迦，再抽一张
        """
        yield Draw(CONTROLLER) * 2
        
        # 检查手牌中是否有娜迦
        has_naga = any(
            Race.NAGA in card.races
            for card in self.controller.hand
            if card.type == CardType.MINION
        )
        
        if has_naga:
            yield Draw(CONTROLLER)


class TSC_622:
    """Shadowborn - 暗影之子
    2费 2/2 亡语：召唤一个2/2的暗影之子。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    deathrattle = Summon(CONTROLLER, "TSC_622")


class TSC_623:
    """Imposing Angler - 威严钓者
    5费 4/4 嘲讽 战吼：如果你在本回合打出过娜迦牌，获得吸血。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.TAUNT: True,
    }
    
    def play(self):
        """
        如果本回合打出过娜迦，获得吸血
        """
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            yield SetAttr(SELF, GameTag.LIFESTEAL, True)


class TSC_624:
    """Gigafin - 巨鳍
    8费 7/4 巨型+2 战吼：吞噬所有敌方随从。亡语：吐出它们。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 4,
        GameTag.COST: 8,
    }
    # 巨型+2：召唤2个附属部件
    colossal_appendages = ["TSC_624t", "TSC_624t"]
    
    def play(self):
        """
        吞噬所有敌方随从
        """
        # 将所有敌方随从移到暂存区
        for minion in list(self.controller.opponent.field):
            yield Setaside(minion)
        
        # 添加追踪buff
        yield Buff(SELF, "TSC_624e")


class TSC_624e:
    """Gigafin Tracker"""
    # 亡语：吐出所有随从
    deathrattle = Summon(OPPONENT, FRIENDLY_SETASIDE)


class TSC_624t:
    """Gigafin's Maw - 巨鳍之口
    2费 2/4
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 2,
    }


class TSC_625:
    """Caria Felsoul - 卡莉亚·邪魂
    6费 6/6 战吼：消灭所有其他随从。如果你在本回合打出过娜迦牌，改为消灭所有其他敌方随从。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6,
        GameTag.COST: 6,
    }
    
    def play(self):
        """
        消灭所有其他随从，如果打出过娜迦，只消灭敌方
        """
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            # 只消灭敌方随从
            yield Destroy(ENEMY_MINIONS)
        else:
            # 消灭所有其他随从
            yield Destroy(ALL_MINIONS - SELF)


class TSC_626:
    """Entitled Customer - 傲慢顾客
    3费 4/4 战吼：对你的英雄造成$4点伤害。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    play = Hit(FRIENDLY_HERO, 4)


class TSC_919:
    """Bloodscent Vilefin - 血腥鱼人
    3费 3/4 战吼：消灭一个友方随从。如果是鱼人，抽一张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        """
        消灭一个友方随从，如果是鱼人，抽一张牌
        """
        is_murloc = Race.MURLOC in self.target.races
        
        yield Destroy(TARGET)
        
        if is_murloc:
            yield Draw(CONTROLLER)
