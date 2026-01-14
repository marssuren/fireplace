# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 牧师
"""

from ..utils import *


class TID_085:
    """Herald of Light - 圣光使徒
    3费 3/4 战吼：如果你在持有本牌期间施放过神圣法术，为所有友方角色恢复#6点生命值。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    
    # 在手牌中时监听神圣法术施放
    events = Play(CONTROLLER, SPELL + HOLY).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TID_085_tracker")
    )
    
    def play(self):
        """
        如果持有期间施放过神圣法术，为所有友方角色恢复6点生命值
        """
        # 检查是否有追踪标记
        has_tracker = any(
            buff.id == "TID_085_tracker"
            for buff in self.buffs
        )
        
        if has_tracker:
            yield Heal(FRIENDLY_CHARACTERS, 6)


class TID_085_tracker:
    """Herald of Light Tracker - 追踪标记"""
    pass


class TID_700:
    """Disarming Elemental - 缴械元素
    4费 4/4 战吼：为你的对手探底。使其法力值消耗变为(6)点。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    def play(self):
        """
        为对手探底，并将该牌费用设为6
        """
        # 为对手探底
        yield Dredge(OPPONENT)
        
        # 将牌库顶的牌费用设为6
        if self.controller.opponent.deck:
            top_card = self.controller.opponent.deck[0]
            yield Buff(top_card, "TID_700e")


class TID_700e:
    """费用设为6"""
    tags = {
        GameTag.COST: SET(6),
    }


class TID_920:
    """Drown - 溺水
    4费法术 将一个敌方随从置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = ShuffleIntoDeck(CONTROLLER, TARGET)


class TSC_209:
    """Whirlpool - 漩涡
    8费法术 消灭所有随从及其所有复制（无论它们在哪里）。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
    }
    
    def play(self):
        """
        消灭所有随从及其所有复制
        
        使用复制追踪机制的完整实现：
        ==================
        1. 收集场上所有随从的 copy_group_id
        2. 遍历所有区域（场上、手牌、牌库），找出所有属于这些组的卡牌
        3. 消灭所有找到的卡牌
        
        copy_group_id 的工作原理：
        - 原始卡牌的 copy_group_id = 其 entity_id
        - 复制卡牌的 copy_group_id = 原始卡牌的 entity_id
        - 复制的复制也会继承相同的 copy_group_id
        """
        # 收集场上所有随从的 copy_group_id
        copy_groups = set()
        for minion in list(self.game.board):
            if minion.type == CardType.MINION:
                # 使用 copy_group_id，如果没有则使用 entity_id（原始卡牌）
                group_id = minion.copy_group_id if minion.copy_group_id is not None else minion.entity_id
                copy_groups.add(group_id)
        
        # 如果场上没有随从，不需要做任何事
        if not copy_groups:
            return
        
        # 收集所有需要消灭的卡牌
        cards_to_destroy = []
        
        # 1. 场上的随从（已经在 copy_groups 中）
        for minion in list(self.game.board):
            if minion.type == CardType.MINION:
                cards_to_destroy.append(minion)
        
        # 2. 双方手牌中的复制
        for player in self.game.players:
            for card in list(player.hand):
                if card.type == CardType.MINION:
                    card_group_id = card.copy_group_id if card.copy_group_id is not None else card.entity_id
                    if card_group_id in copy_groups:
                        cards_to_destroy.append(card)
        
        # 3. 双方牌库中的复制
        for player in self.game.players:
            for card in list(player.deck):
                if card.type == CardType.MINION:
                    card_group_id = card.copy_group_id if card.copy_group_id is not None else card.entity_id
                    if card_group_id in copy_groups:
                        cards_to_destroy.append(card)
        
        # 4. SETASIDE 区域的复制（某些效果会将卡牌暂存在这里）
        for card in list(self.game.setaside):
            if card.type == CardType.MINION:
                card_group_id = card.copy_group_id if card.copy_group_id is not None else card.entity_id
                if card_group_id in copy_groups:
                    cards_to_destroy.append(card)
        
        # 消灭所有收集到的卡牌
        for card in cards_to_destroy:
            yield Destroy(card)



class TSC_210:
    """Illuminate - 照亮
    0费法术 探底。如果是法术牌，使其法力值消耗减少(3)点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    def play(self):
        """
        探底，如果是法术牌，减少3费
        """
        yield Dredge(CONTROLLER)
        
        # 检查牌库顶的牌是否是法术
        if self.controller.deck:
            top_card = self.controller.deck[0]
            if top_card.type == CardType.SPELL:
                yield Buff(top_card, "TSC_210e")


class TSC_210e:
    """-3费用"""
    tags = {
        GameTag.COST: -3,
    }


class TSC_211:
    """Whispers of the Deep - 深渊低语
    1费法术 沉默一个友方随从，然后造成等同于其攻击力的伤害，随机分配到所有敌方随从身上。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        """
        沉默友方随从，然后造成等同于其攻击力的伤害
        """
        # 获取攻击力
        attack = self.target.atk
        
        # 沉默
        yield Silence(TARGET)
        
        # 造成伤害
        for _ in range(attack):
            yield Hit(RANDOM_ENEMY_MINION, 1)


class TSC_212:
    """Handmaiden - 侍女
    3费 3/2 战吼：如果你在持有本牌期间施放过三个法术，抽三张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    # 在手牌中时监听法术施放，每次添加一个计数标记
    events = Play(CONTROLLER, SPELL).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TSC_212_tracker")
    )
    
    def play(self):
        """
        如果持有期间施放过3个法术，抽3张牌
        """
        # 统计追踪标记的数量
        tracker_count = sum(
            1 for buff in self.buffs
            if buff.id == "TSC_212_tracker"
        )
        
        if tracker_count >= 3:
            yield Draw(CONTROLLER) * 3


class TSC_212_tracker:
    """Handmaiden Tracker - 法术计数标记"""
    pass


class TSC_213:
    """Queensguard - 女王卫士
    2费 2/3 战吼：你本回合每施放过一个法术，便获得+1/+1。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    
    def play(self):
        """
        本回合每施放过一个法术,获得+1/+1
        """
        # 统计本回合施放的法术数量
        spell_count = getattr(self.controller, 'num_spells_played_this_turn', 0)
        
        if spell_count > 0:
            yield Buff(SELF, "TSC_213e", atk=spell_count, max_health=spell_count)


class TSC_213e:
    """Queensguard Buff"""
    # 注意：不能用 self.atk 或 self.max_health，会导致无限递归
    def atk(self, i):
        return i + getattr(self, '_atk', 0)
    
    def max_health(self, i):
        return i + getattr(self, '_max_health', 0)


class TSC_215:
    """Serpent Wig - 蛇发
    1费法术 使一个随从获得+1/+2。如果你在持有本牌期间打出过娜迦牌，将一张蛇发牌置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    # 在手牌中时监听娜迦打出
    events = Play(CONTROLLER, MINION + NAGA).on(
        Find(SELF + IN_HAND) & Buff(SELF, "TSC_215_tracker")
    )
    
    def play(self):
        """
        使随从获得+1/+2，如果打出过娜迦，再给一张
        """
        yield Buff(TARGET, "TSC_215e")
        
        # 检查是否有追踪标记
        has_tracker = any(
            buff.id == "TSC_215_tracker"
            for buff in self.buffs
        )
        
        if has_tracker:
            yield Give(CONTROLLER, "TSC_215")


class TSC_215_tracker:
    """Serpent Wig Tracker - 追踪标记"""
    pass


class TSC_215e:
    """+1/+2"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class TSC_216:
    """Blackwater Behemoth - 黑水巨兽
    7费 8/10 巨型+1 吸血
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 10,
        GameTag.COST: 7,
        GameTag.LIFESTEAL: True,
    }
    # 巨型+1：召唤1个附属部件
    colossal_appendages = ["TSC_216t"]


class TSC_216t:
    """Blackwater Tentacle - 黑水触须
    2费 2/8 嘲讽
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 8,
        GameTag.COST: 2,
        GameTag.TAUNT: True,
    }


class TSC_702:
    """Switcheroo - 调包
    5费法术 抽两张随从牌。交换它们的生命值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
    }
    
    def play(self):
        """
        抽两张随从牌并交换生命值
        """
        # 抽第一张随从
        cards1 = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
        # 抽第二张随从
        cards2 = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
        
        if cards1 and cards2:
            card1 = cards1[0]
            card2 = cards2[0]
            
            # 交换生命值
            health1 = card1.health
            health2 = card2.health
            
            yield Buff(card1, "TSC_702e", max_health=health2 - health1)
            yield Buff(card2, "TSC_702e", max_health=health1 - health2)


class TSC_702e:
    """Switcheroo Buff"""
    # 注意：不能用 self.max_health，会导致无限递归
    def max_health(self, i):
        return i + getattr(self, '_max_health', 0)


class TSC_775:
    """Azsharan Ritual - 艾萨拉仪式
    4费法术 沉默一个随从并召唤一个它的复制。将一张"沉没的仪式"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Silence(TARGET),
        Summon(CONTROLLER, ExactCopy(TARGET)),
        ShuffleIntoDeck(CONTROLLER, "TSC_775t"),
    )


class TSC_775t:
    """Sunken Ritual - 沉没的仪式
    4费法术 沉默两个随从并召唤它们的复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_MULTIPLE_TARGETS: 0,  # 需要多个目标
        PlayReq.REQ_TARGET_COUNT: 2,  # 需要2个目标
    }
    
    def play(self):
        """
        沉默两个随从并召唤复制
        
        使用扩展的多目标系统：
        - self.target 现在是一个包含2个目标的列表
        - 遍历列表，对每个目标执行沉默和召唤复制
        """
        # target 是一个包含2个目标的列表
        targets = self.target if isinstance(self.target, list) else [self.target]
        
        for target in targets:
            # 沉默目标
            yield Silence(target)
            # 召唤复制
            yield Summon(CONTROLLER, ExactCopy(target))




class TSC_828:
    """Priestess Valishj - 女祭司瓦利什
    1费 1/1 战吼：你本回合每施放过一个法术，便刷新一个空的法力水晶。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    
    def play(self):
        """
        本回合每施放过一个法术,刷新一个空的法力水晶
        """
        # 统计本回合施放的法术数量
        spell_count = getattr(self.controller, 'num_spells_played_this_turn', 0)
        
        if spell_count > 0:
            yield ManaThisTurn(CONTROLLER, spell_count)
