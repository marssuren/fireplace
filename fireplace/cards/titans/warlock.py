# -*- coding: utf-8 -*-
"""
TITANS 扩展包 - WARLOCK
"""
from ..utils import *


# COMMON

class TTN_456:
    """蔽刺触手 - Thornveil Tentacle
    <b>吸血</b>。<b>战吼:</b>随机对一个敌方随从造成2点伤害。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.LIFESTEAL: True,
    }
    
    play = Hit(RANDOM_ENEMY_MINION, 2)


class TTN_463:
    """飞翼焊装 - Wing Welding
    弃掉你法力值消耗最高的牌,对所有随从造成等同于其法力值消耗的伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 找到手牌中法力值消耗最高的牌
        if not self.controller.hand:
            return
        
        highest_cost_card = max(self.controller.hand, key=lambda c: c.cost)
        damage = highest_cost_card.cost
        
        # 弃掉该牌
        yield Discard(highest_cost_card)
        
        # 对所有随从造成伤害
        yield Hit(ALL_MINIONS, damage)


class TTN_486:
    """魔化形态 - Monstrous Form
    直到你的下个回合,使一个友方随从获得+3/+3。
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
    
    play = Buff(TARGET, "TTN_486e")


class TTN_486e:
    """魔化形态附魔"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    # 在你的下个回合开始时移除
    events = OwnTurnBegin(CONTROLLER).on(Destroy(SELF))


class YOG_517:
    """触须宠溺者 - Tentacle Tender
    在你的回合结束时,获取一张1/1的 混乱触须。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    events = OwnTurnEnd(CONTROLLER).on(Give(CONTROLLER, "YOG_517t"))


class YOG_517t:
    """混乱触须 - Chaotic Tendril"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


# RARE

class TTN_460:
    """致命诛灭 - Mortal Eradication
    造成$5点伤害,随机分配到所有敌方随从身上。每消灭一个随从,为你的英雄恢复#2点生命值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    def play(self):
        # 记录消灭的随从数量
        # 使用一个计数器追踪死亡的敌方随从
        killed_count = [0]  # 使用列表以便在闭包中修改
        
        # 造成5点伤害,随机分配
        for _ in range(5):
            # 记录当前敌方随从
            current_minions = list(self.controller.opponent.field)
            yield Hit(RANDOM_ENEMY_MINION, 1)
            # 检查是否有随从死亡
            new_minions = list(self.controller.opponent.field)
            if len(new_minions) < len(current_minions):
                killed_count[0] += 1
        
        # 每消灭一个随从恢复2点生命
        if killed_count[0] > 0:
            yield Heal(FRIENDLY_HERO, 2 * killed_count[0])


class TTN_465:
    """意志熔炉 - Forge of Wills
    选择一个友方随从。召唤一个具有其属性值和<b>突袭</b>的 巨人。
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 3,
        GameTag.HEALTH: 2,  # Location的耐久度
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def activate(self):
        """Location激活效果"""
        # 获取目标随从
        target = self.target
        if not target or target.type != CardType.MINION:
            return
        
        # 召唤一个具有目标随从属性的巨人
        # 创建巨人token并设置其属性
        giant = self.controller.card("TTN_465t", self.zone)
        giant.tags[GameTag.ATK] = target.atk
        giant.tags[GameTag.HEALTH] = target.health
        giant.tags[GameTag.RUSH] = True
        
        yield Summon(CONTROLLER, giant)


class TTN_465t:
    """意志巨人 - Giant of Will"""
    tags = {
        GameTag.ATK: 1,  # 会被覆盖
        GameTag.HEALTH: 1,  # 会被覆盖
        GameTag.RUSH: True,
    }


class TTN_490:
    """萨格拉斯的信徒 - Disciple of Sargeras
    <b>战吼:</b>弃掉一张法术牌以召唤两个3/2的小鬼。<b>锻造:</b>使其获得+2生命值和<b>嘲讽</b>。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 检查手牌中是否有法术牌
        spells_in_hand = [c for c in self.controller.hand if c.type == CardType.SPELL]
        
        if spells_in_hand:
            # 随机弃掉一张法术牌
            spell_to_discard = self.game.random.choice(spells_in_hand)
            yield Discard(spell_to_discard)
            
            # 召唤两个3/2的小鬼
            yield Summon(CONTROLLER, "TTN_490t") * 2


class TTN_490t:
    """萨格拉斯的信徒 (锻造版) - Disciple of Sargeras (Forged)
    <b>战吼:</b>弃掉一张法术牌以召唤两个3/4并具有<b>嘲讽</b>的小鬼。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,  # +2生命值
        GameTag.COST: 4,
        GameTag.TAUNT: True,
    }
    
    def play(self):
        # 检查手牌中是否有法术牌
        spells_in_hand = [c for c in self.controller.hand if c.type == CardType.SPELL]
        
        if spells_in_hand:
            # 随机弃掉一张法术牌
            spell_to_discard = self.game.random.choice(spells_in_hand)
            yield Discard(spell_to_discard)
            
            # 召唤两个3/4并具有嘲讽的小鬼
            yield Summon(CONTROLLER, "TTN_490t2") * 2


class TTN_490t2:
    """小鬼 (锻造) - Imp (Forged)"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,  # +2生命值
        GameTag.RACE: Race.DEMON,
        GameTag.TAUNT: True,
    }


class YOG_301:
    """狂乱侵蚀 - Encroaching Insanity
    双方英雄受到疲劳伤害,受到两次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 双方英雄各受到两次疲劳伤害
        for _ in range(2):
            yield Fatigue(FRIENDLY_HERO)
        
        for _ in range(2):
            yield Fatigue(ENEMY_HERO)


class YOG_503:
    """血肉诅咒 - Curse of Flesh
    下个回合,敌方随从牌消耗生命值,而非法力值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    play = Buff(OPPONENT, "YOG_503e")


class YOG_503e:
    """血肉诅咒附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 使对手的随从消耗生命值而非法力值
    update = Refresh(OPPONENT, {enums.MINIONS_COST_HEALTH: True})
    
    # 在对手的回合结束时移除效果
    events = OwnTurnEnd(OPPONENT).on(Destroy(SELF))


# EPIC

class TTN_462:
    """被禁锢的恐魔 - Imprisoned Horror
    在本局对战中,你每在你的回合受到一点伤害,本牌的法力值消耗便减少(1)点。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 9,
    }
    
    @property
    def cost_mod(self):
        # 获取在自己回合受到的伤害总量
        damage_taken = getattr(self.controller, 'damage_taken_on_own_turn_this_game', 0)
        return -damage_taken


class TTN_932:
    """混乱吞噬 - Chaotic Consumption
    消灭一个友方随从以消灭一个敌方随从。
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
        # 消灭友方目标
        yield Destroy(TARGET)
        
        # 消灭一个随机敌方随从
        yield Destroy(RANDOM_ENEMY_MINION)


# LEGENDARY

class TTN_487:
    """洛肯,尤格-萨隆的看守 - Loken, Jailer of Yogg-Saron
    <b>战吼:</b>从你的牌库中<b>发现</b>一张随从牌,召唤一条具有其属性值和<b>嘲讽</b>的触手。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
        GameTag.LEGENDARY: True,
    }
    
    def play(self):
        # 从牌库中发现一张随从牌
        # 使用Discover从牌库中选择
        minions_in_deck = [c for c in self.controller.deck if c.type == CardType.MINION]
        
        if not minions_in_deck:
            return
        
        # 随机选择3张随从(如果不足3张则全部选择)
        import random
        choices = random.sample(minions_in_deck, min(3, len(minions_in_deck)))
        
        # 发现并召唤触手
        discovered = yield GenericChoice(CONTROLLER, choices)
        
        if discovered and discovered[0]:
            card = discovered[0]
            # 创建触手并设置属性
            tentacle = self.controller.card("TTN_487t", self.zone)
            tentacle.tags[GameTag.ATK] = card.atk
            tentacle.tags[GameTag.HEALTH] = card.health
            tentacle.tags[GameTag.TAUNT] = True
            
            yield Summon(CONTROLLER, tentacle)


class TTN_487t:
    """触手 - Tentacle"""
    tags = {
        GameTag.ATK: 1,  # 会被覆盖
        GameTag.HEALTH: 1,  # 会被覆盖
        GameTag.TAUNT: True,
    }


class TTN_960:
    """灭世泰坦萨格拉斯 - Sargeras, the Destroyer
    <b>泰坦</b> <b>战吼:</b>打开一道传送门,每回合召唤两个3/2的小鬼。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 12,
        GameTag.COST: 9,
        GameTag.LEGENDARY: True,
        GameTag.TITAN: True,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 泰坦技能次数
    }
    
    play = Buff(CONTROLLER, "TTN_960e")
    
    def titan_ability_1(self):
        """暗影之握 - Shadow Grasp
        对所有敌方随从造成3点伤害。
        """
        yield Hit(ENEMY_MINIONS, 3)
    
    def titan_ability_2(self):
        """燃烧军团 - Burning Legion
        召唤三个3/2的小鬼。
        """
        yield Summon(CONTROLLER, "TTN_960t") * 3
    
    def titan_ability_3(self):
        """毁灭打击 - Destructive Strike
        对敌方英雄造成5点伤害。
        """
        yield Hit(ENEMY_HERO, 5)


class TTN_960e:
    """传送门附魔 - Portal"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 每回合开始时召唤两个小鬼
    events = OwnTurnBegin(CONTROLLER).on(
        Summon(CONTROLLER, "TTN_960t") * 2
    )


class TTN_960t:
    """小鬼 - Imp"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.RACE: Race.DEMON,
    }
