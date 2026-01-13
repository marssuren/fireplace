"""
漫游翡翠梦境 - 中立 - EPIC
"""
from ..utils import *
from .dark_gift_helpers import apply_dark_gift


# ============================================================
# EPIC 卡牌
# ============================================================


class EDR_102:
    """狡诈拷问者 - Treacherous Tormentor
    Battlecry: Discover a Legendary minion with a Dark Gift.
    
    4费 5/4 恶魔
    战吼:发现一张具有黑暗之赐的传说随从牌。
    """
    # 战吼:发现一张具有黑暗之赐的传说随从牌
    def play(self):
        # 发现一张传说随从
        # 使用 GenericChoice + RandomCardGenerator 实现发现机制
        yield GenericChoice(
            CONTROLLER, RandomCardGenerator(
                CONTROLLER,
                card_filter=lambda c: c.type == CardType.MINION and c.rarity == Rarity.LEGENDARY,
                count=3
            )
        )
        
        # 获取刚发现的卡牌(手牌中最后一张)
        if self.controller.hand:
            discovered_card = self.controller.hand[-1]
            # 应用黑暗之赐
            yield apply_dark_gift(discovered_card)


class EDR_469:
    """沉睡的林精 - Slumbering Sprite
    Starts Dormant. After you use your Hero Power, this awakens.
    
    1费 3/3 随从
    起始休眠状态。在你使用英雄技能后唤醒。
    """
    # 起始休眠状态
    tags = {
        GameTag.DORMANT: True,
    }
    
    # 在你使用英雄技能后唤醒
    events = Activate(CONTROLLER, HERO_POWER).after(
        lambda self: [
            SetTags(SELF, {GameTag.DORMANT: False})
        ]
    )


class EDR_780:
    """血蓟幻术师 - Bloodthistle Illusionist
    Battlecry: Summon a copy of this. One secretly dies when it takes damage.
    
    3费 2/4 恶魔
    战吼:召唤一个本随从的复制。本体和复制中会秘密区分出一个,在受到伤害时死亡。
    """
    # 战吼:召唤一个本随从的复制,其中一个会在受到伤害时死亡
    def play(self):
        # 随机决定哪一个会在受到伤害时死亡
        # 50%概率是本体,50%概率是复制
        is_original_fragile = self.game.random.choice([True, False])
        
        # 如果本体是脆弱的,给本体添加标记
        if is_original_fragile:
            yield Buff(SELF, "EDR_780e")
        
        # 召唤复制
        yield Summon(CONTROLLER, "EDR_780")
        
        # 如果复制是脆弱的,给刚召唤的复制添加标记
        if not is_original_fragile:
            # 获取刚召唤的复制(场上最后一个随从)
            if self.controller.field:
                copy = self.controller.field[-1]
                if copy.id == "EDR_780" and copy != self:
                    yield Buff(copy, "EDR_780e")


class EDR_780e:
    """血蓟幻术师增益 - 受到伤害时死亡"""
    # 受到伤害时死亡
    events = Damage(OWNER).on(
        lambda self, target, amount: [
            Destroy(OWNER)
        ]
    )


class EDR_860:
    """明耀织梦者 - Resplendent Dreamweaver
    Lifesteal. Battlecry: If you've Imbued your Hero Power twice, deal 4 damage to a minion.
    
    4费 4/4 随从
    吸血。战吼:如果你已灌注过你的英雄技能两次,对一个随从造成4点伤害。
    """
    tags = {
        GameTag.LIFESTEAL: True,
    }
    
    # 战吼:如果已灌注两次,对一个随从造成4点伤害
    def play(self, target=None):
        # 检查是否已灌注两次(使用getattr防御性访问)
        if getattr(self.controller, 'imbue_level', 0) >= 2:
            if target:
                yield Hit(target, 4)
    
    # 需要目标(如果已灌注两次)
    @property
    def requires_target(self):
        return getattr(self.controller, 'imbue_level', 0) >= 2
    
    # 目标必须是随从
    play_reqs = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }


class EDR_979:
    """昔时古树 - Ancient of Yore
    Dormant for 2 turns. While Dormant, gain 3 Armor and draw a card at the end of your turn.
    
    5费 5/5 随从
    休眠2回合。休眠状态下,在你的回合结束时,获得3点护甲值并抽一张牌。
    """
    # 休眠2回合(使用标准的dormant_turns属性)
    tags = {
        GameTag.DORMANT: True,
    }
    
    dormant_turns = 2  # 标准的休眠回合数设置方式
    
    # 在回合结束时,如果处于休眠状态,获得3点护甲值并抽一张牌
    events = OWN_TURN_END.on(
        lambda self: [
            GainArmor(FRIENDLY_HERO, 3),
            Draw(CONTROLLER)
        ] if self.tags.get(GameTag.DORMANT, False) else []
    )


class FIR_940:
    """扎卡利驭焰者 - Zaqali Flamemencer
    Battlecry: If every card in your hand is of a different Cost, reduce their Costs by (2).
    
    6费 4/4 随从
    战吼:如果你每张手牌的法力值消耗各不相同,使其法力值消耗减少(2)点。
    """
    # 战吼:如果每张手牌的法力值消耗各不相同,使其法力值消耗减少(2)点
    def play(self):
        # 获取手牌中所有卡牌的费用(不包括自己)
        hand_costs = [card.cost for card in self.controller.hand if card != self]
        
        # 检查是否所有费用都不相同
        if len(hand_costs) == len(set(hand_costs)):
            # 所有费用都不相同,减少所有手牌的费用
            for card in self.controller.hand:
                if card != self:
                    yield Buff(card, "FIR_940e")


class FIR_940e:
    """扎卡利驭焰者增益 - 费用减少(2)点"""
    tags = {
        GameTag.COST: -2,
    }
