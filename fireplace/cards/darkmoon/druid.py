"""
暗月马戏团 - 德鲁伊
"""
from ..utils import *


##
# Minions

class DMF_059:
    """泡沫元素 - Fizzy Elemental
    突袭，嘲讽
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 1,
        GameTag.COST: 4,
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
    }


class DMF_060:
    """幽影猫头鹰 - Umbral Owl
    突袭。你在本局对战中每施放一个法术，本牌的法力值消耗便减少(1)点。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 7,
        GameTag.RUSH: True,
    }
    # 你在本局对战中每施放一个法术,本牌的法力值消耗便减少(1)点
    cost_mod = lambda self: -len([c for c in self.controller.cards_played_this_game if c.type == CardType.SPELL])


class DMF_061:
    """马戏团树艺师 - Faire Arborist
    抉择：抽一张牌；或者召唤一个2/2的树人。腐蚀：全部执行。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("DMF_061a", "DMF_061b")
    corrupt = (
        Give(CONTROLLER, "DMF_061a"),
        Give(CONTROLLER, "DMF_061b"),
    )


class DMF_061a:
    """抽一张牌"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    play = Draw(CONTROLLER)


class DMF_061b:
    """召唤树人"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    play = Summon(CONTROLLER, "EX1_158t")  # 2/2 Treant


class DMF_733:
    """基利，艾露恩之眷 - Kiri, Chosen of Elune
    战吼：将一张日蚀和一张月蚀置入你的手牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = (
        Give(CONTROLLER, "DMF_058"),  # Solar Eclipse
        Give(CONTROLLER, "DMF_057"),  # Lunar Eclipse
    )


class DMF_734:
    """格雷布 - Greybough
    嘲讽，亡语：随机使一个友方随从获得"亡语：召唤格雷布"。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,
        GameTag.COST: 5,
        GameTag.TAUNT: True,
    }
    deathrattle = Buff(RANDOM(FRIENDLY + MINION), "DMF_734e")


class DMF_734e:
    """格雷布的亡语"""
    deathrattle = Summon(CONTROLLER, "DMF_734")


class YOP_025:
    """迷梦幼龙 - Dreaming Drake
    嘲讽。腐蚀：获得+2/+2。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.TAUNT: True,
    }
    corrupt = Buff(SELF, "YOP_025e")


class YOP_025e:
    """迷梦"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


##
# Spells

class DMF_057:
    """月蚀 - Lunar Eclipse
    对一个随从造成3点伤害。你在本回合中施放的下一个法术的法力值消耗减少(2)点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Hit(TARGET, 3),
        Buff(CONTROLLER, "DMF_057e"),
    )


class DMF_057e:
    """月蚀 - 下一个法术减费(2)"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -2})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class DMF_058:
    """日蚀 - Solar Eclipse
    你在本回合中施放的下一个法术会施放两次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    play = Buff(CONTROLLER, "DMF_058e")


class DMF_058e:
    """日蚀 - 下一个法术施放两次"""
    from fireplace.enums import SPELL_DOUBLE_CAST
    
    def apply(self, target):
        # 设置SPELL_DOUBLE_CAST标签，表示下一个法术施放两次
        if not hasattr(target, 'tags'):
            target.tags = {}
        target.tags[SPELL_DOUBLE_CAST] = target.tags.get(SPELL_DOUBLE_CAST, 0) + 1
    
    # 在法术施放后销毁buff
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class DMF_075:
    """猜重量 - Guess the Weight
    抽一张牌。猜测你的下一张牌的法力值消耗是更高还是更低，以便抽取该牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        # 先抽一张牌
        drawn_cards = yield Draw(CONTROLLER)
        if not drawn_cards:
            return
        
        first_card = drawn_cards[0]
        first_cost = first_card.cost
        
        # 检查牌库是否还有牌
        if not self.controller.deck:
            return
        
        # 查看牌库顶的牌（但不抽）
        next_card = self.controller.deck[-1]
        next_cost = next_card.cost
        
        # 让玩家选择：猜测下一张牌费用更高还是更低
        # 创建两个选项
        higher_choice = self.controller.card("DMF_075a", source=self)
        lower_choice = self.controller.card("DMF_075b", source=self)
        
        # 存储信息到选项卡牌上，用于后续判断
        higher_choice.first_cost = first_cost
        higher_choice.next_cost = next_cost
        lower_choice.first_cost = first_cost
        lower_choice.next_cost = next_cost
        
        # 让玩家选择
        yield GenericChoice(CONTROLLER, [higher_choice, lower_choice])


class DMF_075a:
    """更高 - Higher"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    def play(self):
        # 检查猜测是否正确
        if hasattr(self, 'next_cost') and hasattr(self, 'first_cost'):
            if self.next_cost > self.first_cost:
                # 猜对了，抽牌
                yield Draw(CONTROLLER)


class DMF_075b:
    """更低 - Lower"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    def play(self):
        # 检查猜测是否正确
        if hasattr(self, 'next_cost') and hasattr(self, 'first_cost'):
            if self.next_cost < self.first_cost:
                # 猜对了，抽牌
                yield Draw(CONTROLLER)


class DMF_730:
    """月触项链 - Moontouched Amulet
    在本回合中，使你的英雄获得+4攻击力。腐蚀：并获得6点护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    play = Buff(FRIENDLY_HERO, "DMF_730e")
    corrupt = GainArmor(FRIENDLY_HERO, 6)


class DMF_730e:
    """月触项链 - 英雄攻击力"""
    tags = {
        GameTag.ATK: 4,
        GameTag.DURABILITY: 1,
    }


class DMF_732:
    """塞纳里奥结界 - Cenarion Ward
    获得8点护甲值。召唤一个随机的法力值消耗为(8)的随从。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    play = (
        GainArmor(FRIENDLY_HERO, 8),
        Summon(CONTROLLER, RandomMinion(cost=8)),
    )


class YOP_026:
    """树木生长 - Arbor Up
    召唤两个2/2的树人。使你的所有随从获得+2/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    play = (
        Summon(CONTROLLER, "EX1_158t") * 2,  # 2/2 Treant
        Buff(FRIENDLY_MINIONS, "YOP_026e"),
    )


class YOP_026e:
    """树木生长"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }
