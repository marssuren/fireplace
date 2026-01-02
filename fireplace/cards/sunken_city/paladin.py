# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 圣骑士
"""

from ..utils import *


class TID_077:
    """Lightray - 光鳐
    9费 5/5 嘲讽。你每打出一张圣骑士牌，本牌的法力值消耗便减少(1)点。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 9,
        GameTag.TAUNT: True,
    }
    # 每打出一张圣骑士牌减少1费
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + PALADIN)


class TID_098:
    """Myrmidon - 米尔米顿
    3费 3/4 在你对本随从施放法术后，抽一张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    # 在对本随从施放法术后，抽一张牌
    events = Play(CONTROLLER, SPELL, SELF).after(Draw(CONTROLLER))


class TID_949:
    """Front Lines - 前线
    9费法术 从双方牌库中各召唤一个随从。重复此过程，直到任意一方的战场被占满。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 9,
    }
    
    def play(self):
        """
        从双方牌库中各召唤一个随从，直到任意一方战场满
        """
        while True:
            # 检查双方战场是否已满
            if len(self.controller.field) >= 7 or len(self.controller.opponent.field) >= 7:
                break
            
            # 从己方牌库召唤随从
            if len(self.controller.field) < 7:
                yield Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
            
            # 从对方牌库召唤随从
            if len(self.controller.opponent.field) < 7:
                yield Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))


class TSC_030:
    """The Leviathan - 海兽号
    7费 4/5 巨型+1 突袭，圣盾 在本随从攻击后，探底。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
        GameTag.RUSH: True,
        GameTag.DIVINE_SHIELD: True,
    }
    # 巨型+1：召唤1个附属部件
    colossal_appendages = ["TSC_030t"]
    # 攻击后探底
    events = Attack(SELF).after(Dredge(CONTROLLER))


class TSC_030t:
    """Leviathan's Lure - 利维坦的诱饵
    1费 1/4 嘲讽
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 4,
        GameTag.COST: 1,
        GameTag.TAUNT: True,
    }


class TSC_059:
    """Bubblebot - 泡泡机器人
    4费 4/4 战吼：使你的其他机械获得圣盾和嘲讽。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    play = (
        SetAttr(FRIENDLY_MINIONS + MECH - SELF, GameTag.DIVINE_SHIELD, True),
        SetAttr(FRIENDLY_MINIONS + MECH - SELF, GameTag.TAUNT, True),
    )


class TSC_060:
    """Shimmering Sunfish - 闪光太阳鱼
    3费 2/5 战吼：如果你的手牌中有神圣法术牌，获得嘲讽和圣盾。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
    }
    play = Find(FRIENDLY_HAND + SPELL + HOLY) & (
        SetAttr(SELF, GameTag.TAUNT, True),
        SetAttr(SELF, GameTag.DIVINE_SHIELD, True),
    )


class TSC_061:
    """The Garden's Grace - 花园的恩典
    10费法术 使一个随从获得+4/+4和圣盾。你每在神圣法术上花费1点法力值，本牌的法力值消耗便减少(1)点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 10,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(TARGET, "TSC_061e"),
        SetAttr(TARGET, GameTag.DIVINE_SHIELD, True),
    )
    
    # 追踪神圣法术消耗的法力值
    # 统计本局游戏中打出的所有神圣法术实际支付的费用
    def cost_mod(self):
        """
        计算费用减免
        
        遍历 cards_played_this_game，找出所有神圣法术，
        累加它们实际支付的费用（存储在 card.tags.get(GameTag.COST_PAID, card.cost)）
        """
        total_mana_spent = 0
        
        for card in self.controller.cards_played_this_game:
            # 检查是否是法术
            if card.type != CardType.SPELL:
                continue
            
            # 检查是否是神圣法术
            spell_school = card.tags.get(GameTag.SPELL_SCHOOL)
            if spell_school != SpellSchool.HOLY:
                continue
            
            # 累加实际支付的费用
            # 优先使用 COST_PAID（实际支付），否则使用 cost（基础费用）
            mana_paid = card.tags.get(GameTag.COST_PAID, card.cost)
            total_mana_spent += mana_paid
        
        # 返回负数表示减费
        return -total_mana_spent



class TSC_061e:
    """+4/+4"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
    }


class TSC_074:
    """Kotori Lightblade - 光刃小鸟
    2费 2/3 在你对本随从施放神圣法术后，再次对另一个友方随从施放该法术。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    # 在对本随从施放神圣法术后，再次对另一个友方随从施放
    events = Play(CONTROLLER, SPELL + HOLY, SELF).after(
        CastSpell(Play.CARD, RANDOM(FRIENDLY_MINIONS - SELF))
    )


class TSC_076:
    """Immortalized in Stone - 石化永生
    7费法术 召唤一个4/8、一个2/4和一个1/2并具有嘲讽的元素。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
    }
    play = (
        Summon(CONTROLLER, "TSC_076t"),  # 4/8
        Summon(CONTROLLER, "TSC_076t2"),  # 2/4
        Summon(CONTROLLER, "TSC_076t3"),  # 1/2
    )


class TSC_076t:
    """Stone Guardian - 石头守卫者
    4费 4/8 嘲讽
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 8,
        GameTag.COST: 4,
        GameTag.TAUNT: True,
    }


class TSC_076t2:
    """Stone Defender - 石头防御者
    2费 2/4 嘲讽
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 2,
        GameTag.TAUNT: True,
    }


class TSC_076t3:
    """Stone Sentinel - 石头哨兵
    1费 1/2 嘲讽
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        GameTag.TAUNT: True,
    }


class TSC_079:
    """Radar Detector - 雷达探测器
    2费法术 扫描你牌库底部的5张牌。抽出所有以此法找到的机械牌，然后洗牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        扫描牌库底部5张牌，抽出所有机械牌，然后洗牌
        """
        deck = self.controller.deck
        if not deck:
            return
        
        # 查看底部最多5张牌
        num_cards = min(5, len(deck))
        bottom_cards = deck[-num_cards:]
        
        # 找出所有机械牌
        mech_cards = [card for card in bottom_cards if Race.MECH in card.races]
        
        # 抽出机械牌
        for card in mech_cards:
            yield ForceDraw(CONTROLLER, card)
        
        # 洗牌
        self.controller.shuffle_deck()


class TSC_083:
    """Seafloor Savior - 海底救星
    2费 2/2 战吼：探底。如果是随从牌，使其获得本随从的攻击力和生命值。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        探底，如果是随从牌，使其获得本随从的攻击力和生命值
        """
        # 探底
        yield Dredge(CONTROLLER)
        
        # 检查牌库顶的牌是否是随从
        if self.controller.deck:
            top_card = self.controller.deck[0]
            if top_card.type == CardType.MINION:
                # 使其获得本随从的攻击力和生命值
                yield Buff(top_card, "TSC_083e", atk=self.atk, max_health=self.health)


class TSC_083e:
    """Seafloor Savior Buff"""
    atk = lambda self, i: self.atk
    max_health = lambda self, i: self.max_health


class TSC_644:
    """Azsharan Mooncatcher - 艾萨拉追月者
    3费 4/2 圣盾 战吼：将一张"沉没的追月者"置于你的牌库底部。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.DIVINE_SHIELD: True,
    }
    play = ShuffleIntoDeck(CONTROLLER, "TSC_644t")


class TSC_644t:
    """Sunken Mooncatcher - 沉没的追月者
    3费 4/2 圣盾 战吼：使你的手牌中的所有随从牌获得圣盾。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.DIVINE_SHIELD: True,
    }
    play = SetAttr(FRIENDLY_HAND + MINION, GameTag.DIVINE_SHIELD, True)


class TSC_952:
    """Holy Maki Roll - 神圣寿司卷
    1费法术 恢复#2点生命值。本回合可重复使用。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Heal(TARGET, 2), Give(CONTROLLER, "TSC_952")  # 返回一张复制到手牌
