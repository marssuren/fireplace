# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 萨满
"""

from ..utils import *


class TID_701:
    """Schooling - 鱼群
    1费法术 使对手手牌中的一张牌在下回合无法打出。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """
        随机选择对手手牌中的一张牌，使其下回合无法打出
        """
        if self.controller.opponent.hand:
            # 随机选择一张牌
            target_card = self.game.random_choice(self.controller.opponent.hand)
            # 添加buff使其无法打出
            yield Buff(target_card, "TID_701e")


class TID_701e:
    """无法打出"""
    tags = {
        GameTag.CANT_PLAY: True,
    }
    # 下回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


class TID_707:
    """Bioluminescence - 生物发光
    1费法术 你本回合每打出过一张牌，便抽一张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """
        本回合每打出过一张牌，抽一张牌
        """
        # 统计本回合打出的牌数量
        cards_played = len(self.controller.cards_played_this_turn)
        
        if cards_played > 0:
            yield Draw(CONTROLLER) * cards_played


class TID_709:
    """Command of Neptulon - 奈普图隆的命令
    5费法术 获得5点护甲值。如果你在本回合打出过娜迦牌，召唤一个5/5的元素，并具有突袭和嘲讽。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    
    def play(self):
        """
        获得5点护甲，如果打出过娜迦，召唤元素
        """
        yield GainArmor(FRIENDLY_HERO, 5)
        
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            yield Summon(CONTROLLER, "TID_709t")


class TID_709t:
    """Elemental - 元素
    5费 5/5 突袭，嘲讽
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
    }


class TSC_642:
    """Piranha Swarmer - 食人鱼群
    1费 2/1 突袭 在本随从攻击并消灭一个随从后，召唤一个本随从的复制。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.RUSH: True,
    }
    # 攻击并消灭随从后，召唤复制
    events = Attack(SELF, MINION).after(
        Dead(Attack.DEFENDER) & Summon(CONTROLLER, ExactCopy(SELF))
    )


class TSC_643:
    """Azsharan Scroll - 艾萨拉卷轴
    1费法术 抽一张牌。将一张"沉没的卷轴"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = (
        Draw(CONTROLLER),
        ShuffleIntoDeck(CONTROLLER, "TSC_643t"),
    )


class TSC_643t:
    """Sunken Scroll - 沉没的卷轴
    1费法术 将你的手牌移到牌库底部。从牌库底部抽等量的牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """
        将手牌移到牌库底部，然后从底部抽等量的牌
        """
        hand_size = len(self.controller.hand)
        
        # 将手牌移到牌库底部
        for card in list(self.controller.hand):
            if card != self:  # 不包括自己
                yield ShuffleIntoDeck(CONTROLLER, card)
        
        # 从牌库底部抽牌
        for _ in range(hand_size - 1):  # -1因为不包括自己
            if self.controller.deck:
                bottom_card = self.controller.deck[-1]
                yield ForceDraw(CONTROLLER, bottom_card)


class TSC_645:
    """Scalding Geyser - 沸腾间歇泉
    3费法术 造成$4点伤害。过载：(1)
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.OVERLOAD: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)


class TSC_646:
    """Coral Keeper - 珊瑚守护者
    5费 3/4 战吼：召唤一个随机图腾。如果你在本回合打出过娜迦牌，再召唤一个。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    
    def play(self):
        """
        召唤一个随机图腾，如果打出过娜迦，再召唤一个
        """
        yield Summon(CONTROLLER, RandomTotem())
        
        # 检查本回合是否打出过娜迦
        naga_played_this_turn = any(
            Race.NAGA in card.races
            for card in self.controller.cards_played_this_turn
            if card.type == CardType.MINION
        )
        
        if naga_played_this_turn:
            yield Summon(CONTROLLER, RandomTotem())


class TSC_647:
    """Brilliant Macaw - 璀璨金刚鹦鹉
    3费 3/3 战吼：重复你上一个战吼。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    # 使用核心的 RepeatBattlecry action
    play = RepeatBattlecry(CONTROLLER)


class TSC_648:
    """Clownfish - 小丑鱼
    2费 3/2 战吼：你的下一个娜迦的法力值消耗减少(2)点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = Buff(CONTROLLER, "TSC_648e")


class TSC_648e:
    """Clownfish Buff"""
    # 下一个娜迦减少2费
    update = Refresh(FRIENDLY_HAND + MINION + NAGA, {GameTag.COST: -2})
    events = Play(CONTROLLER, MINION + NAGA).on(Destroy(SELF))


class TSC_649:
    """Anchored Totem - 锚定图腾
    2费 0/3 在你的回合结束时，召唤一个随机基础图腾。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomTotem()))


class TSC_776:
    """Gorloc Ravager - 鱼人掠夺者
    5费 4/3 战吼：抽三张过载牌。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
    }
    
    def play(self):
        """
        抽三张过载牌
        """
        for _ in range(3):
            # 从牌库中抽取有过载的牌
            yield ForceDraw(CONTROLLER, FRIENDLY_DECK + OVERLOAD)


class TSC_777:
    """Gigafin - 巨鳍
    8费 7/4 巨型+2 战吼：吞噬所有敌方随从。亡语：吐出它们。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 4,
        GameTag.COST: 8,
    }
    # 巨型+2：召唤2个附属部件
    colossal_appendages = ["TSC_777t", "TSC_777t"]
    
    def play(self):
        """
        吞噬所有敌方随从
        """
        # 将所有敌方随从移到暂存区
        for minion in list(self.controller.opponent.field):
            yield Setaside(minion)
        
        # 添加追踪buff
        yield Buff(SELF, "TSC_777e")


class TSC_777e:
    """Gigafin Tracker"""
    # 亡语：吐出所有随从
    deathrattle = Summon(OPPONENT, FRIENDLY_SETASIDE)


class TSC_777t:
    """Gigafin's Maw - 巨鳍之口
    2费 2/4
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 2,
    }
