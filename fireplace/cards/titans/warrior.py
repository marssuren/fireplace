# -*- coding: utf-8 -*-
"""
TITANS 扩展包 - WARRIOR
"""
from ..utils import *
from ... import enums


# COMMON

class TTN_467:
    """匠人之锤 - Craftsman's Hammer
    每当你的英雄攻击时，便获得4点护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 3,
        GameTag.COST: 4,
    }
    
    # 英雄攻击时触发
    events = Attack(FRIENDLY_HERO).on(GainArmor(FRIENDLY_HERO, 4))


class TTN_468:
    """蒸汽守卫 - Steam Guardian
    <b>战吼：</b>抽一张法术牌。使你手牌中一张火焰法术牌的法力值消耗减少（1）点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }
    
    def play(self):
        # 抽一张法术牌
        yield ForceDraw(CONTROLLER) & SPELL
        
        # 使手牌中一张火焰法术减费
        fire_spells = [
            c for c in self.controller.hand 
            if c.type == CardType.SPELL and getattr(c, 'spell_school', None) == SpellSchool.FIRE
        ]
        
        if fire_spells:
            target = self.game.random.choice(fire_spells)
            yield Buff(target, "TTN_468e")


class TTN_468e:
    """蒸汽守卫附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -1,
    }


class TTN_753:
    """鼓动火焰 - Bellowing Flames
    对一个随从造成$5点伤害。<b>锻造：</b>然后造成$5点伤害，随机分配到所有敌方随从身上。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    play = Hit(TARGET, 5)
    forge = "TTN_753t"


class TTN_753t:
    """鼓动火焰 (锻造版) - Bellowing Flames (Forged)
    对一个随从造成$5点伤害。然后造成$5点伤害，随机分配到所有敌方随从身上。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 先对目标造成5点伤害
        yield Hit(TARGET, 5)
        
        # 然后造成5点伤害随机分配到所有敌方随从
        for _ in range(5):
            yield Hit(RANDOM_ENEMY_MINION, 1)


class YOG_502:
    """清理污染 - Sanitize
    对所有随从造成等同于你的护甲值的伤害。<b>锻造：</b>先获得3点护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 基于当前护甲值造成伤害
        armor = self.controller.hero.armor
        if armor > 0:
            yield Hit(ALL_MINIONS, armor)
    
    forge = "YOG_502t"


class YOG_502t:
    """清理污染 (锻造版) - Sanitize (Forged)
    先获得3点护甲值。对所有随从造成等同于你的护甲值的伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 先获得3点护甲
        yield GainArmor(FRIENDLY_HERO, 3)
        
        # 然后基于当前护甲值造成伤害
        armor = self.controller.hero.armor
        if armor > 0:
            yield Hit(ALL_MINIONS, armor)


# RARE

class TTN_466:
    """米诺陶牛头人 - Minotauren
    <b>突袭</b> 每当本随从造成伤害时，获得等量的护甲值。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
        GameTag.RUSH: True,
    }
    
    # 造成伤害时获得等量护甲
    events = Damage(SELF).on(GainArmor(FRIENDLY_HERO, Damage(SELF).amount))


class TTN_469:
    """岩肤护甲商 - Stoneskin Armorer
    <b>战吼：</b>在本回合中，如果你的护甲值发生变化，抽两张牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    play = Buff(CONTROLLER, "TTN_469e")


class TTN_469e:
    """岩肤护甲商附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 记录施放时的护甲值
        if hasattr(self, 'controller') and self.controller:
            self.initial_armor = self.controller.hero.armor
        else:
            self.initial_armor = 0
    
    def OWN_TURN_END(self):
        """回合结束时检查护甲变化"""
        if self.controller.hero.armor != self.initial_armor:
            yield Draw(CONTROLLER) * 2
        yield Destroy(SELF)


class TTN_803:
    """熔铸 - Smelt
    随机使你手牌中的一张随从牌获得+3/+3。失去3点护甲值以重复一次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    def play(self):
        # 第一次buff
        minions_in_hand = [c for c in self.controller.hand if c.type == CardType.MINION]
        if minions_in_hand:
            target = self.game.random.choice(minions_in_hand)
            yield Buff(target, "TTN_803e")
        
        # 如果有足够的护甲，失去3点护甲并重复
        if self.controller.hero.armor >= 3:
            yield GainArmor(FRIENDLY_HERO, -3)
            
            # 第二次buff
            minions_in_hand = [c for c in self.controller.hand if c.type == CardType.MINION]
            if minions_in_hand:
                target = self.game.random.choice(minions_in_hand)
                yield Buff(target, "TTN_803e")


class TTN_803e:
    """熔铸附魔"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class YOG_501:
    """历战无面者 - Battleworn Faceless
    <b>战吼：</b>变形成为一个受伤的随从的复制。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    
    play = Morph(SELF, Copy(TARGET))


# EPIC

class TTN_470:
    """火焰试炼 - Trial by Fire
    召唤五个1/1并具有<b>突袭</b>的瓦格里。当一个死亡时，使其他的获得+1/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    play = Summon(CONTROLLER, "TTN_470t") * 5


class TTN_470t:
    """瓦格里 - Valkyr
    <b>突袭</b>。当本随从死亡时，使其他瓦格里获得+1/+1。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.RUSH: True,
    }
    
    # 死亡时给其他瓦格里+1/+1
    deathrattle = Buff(FRIENDLY_MINIONS + ID("TTN_470t") - SELF, "TTN_470e")


class TTN_470e:
    """火焰试炼附魔"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class TTN_471:
    """愤怒焚炉 - Furious Furnace
    <b>磁力</b>。同时对其攻击目标相邻的随从造成伤害。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.MECHANICAL,
        GameTag.MAGNETIC: True,
    }
    
    magnetic = MAGNETIC("TTN_471e")
    
    # 攻击时对相邻随从造成伤害（溅射效果）
    events = Attack(SELF).on(CLEAVE)


class TTN_471e:
    """愤怒焚炉附魔"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.MAGNETIC: True,
    }
    
    # 磁力附魔也需要溅射效果
    events = Attack(OWNER).on(CLEAVE)


# LEGENDARY

class TTN_415:
    """卡兹格罗斯 - Khaz'goroth
    <b>泰坦</b> 在本随从使用一个技能后，在本回合中获得<b>免疫</b>并随机攻击一个敌方随从。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
        GameTag.LEGENDARY: True,
        GameTag.TITAN: True,
        enums.TITAN_ABILITY_COUNT: 3,  # 泰坦技能次数
    }
    
    # 泰坦技能使用后触发：获得免疫并随机攻击敌方随从
    # 参考德鲁伊泰坦艾欧娜尔的实现模式
    events = Activate(CONTROLLER, TITAN_ABILITY).on(
        Buff(SELF, "TTN_415e"),  # 获得本回合免疫
        Attack(SELF, RANDOM_ENEMY_MINION)  # 随机攻击敌方随从
    )
    
    def titan_ability_1(self):
        """泰坦之握 - Titan's Grasp
        使一个随从获得+2/+2和<b>嘲讽</b>。
        """
        # 需要目标的技能
        yield Buff(TARGET, "TTN_415te")
    
    # 技能1的目标要求
    titan_ability_1_requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def titan_ability_2(self):
        """战争回响 - War Echoes
        获得+5护甲。在本回合中，使你的英雄获得+5攻击力。
        """
        # 给予英雄+5护甲
        yield GainArmor(FRIENDLY_HERO, 5)
        # 在本回合中给予英雄+5攻击力
        yield Buff(FRIENDLY_HERO, "TTN_415t2e")
    
    def titan_ability_3(self):
        """锻造之力 - Forge Power
        使你的武器获得+5攻击力和+5耐久度。
        """
        weapon = self.controller.hero.weapon
        if weapon:
            yield Buff(weapon, "TTN_415t3e")


class TTN_415e:
    """锻造免疫附魔 - 本回合免疫"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 在回合结束时移除免疫
    events = OWN_TURN_END.on(Destroy(SELF))


class TTN_415te:
    """泰坦之握附魔"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class TTN_415t2e:
    """战争回响附魔 - 临时攻击力"""
    tags = {
        GameTag.ATK: 5,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 在回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


class TTN_415t3e:
    """锻造之力附魔"""
    tags = {
        GameTag.ATK: 5,
        GameTag.DURABILITY: 5,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class TTN_811:
    """首席管理官奥丁 - Odyn, Prime Designate
    <b>战吼：</b>在本局对战的剩余时间内，在你的英雄获得护甲值后，还会在当回合获得等量的攻击力。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 8,
        GameTag.LEGENDARY: True,
    }
    
    play = Buff(CONTROLLER, "TTN_811e")


class TTN_811e:
    """奥丁祝福附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 获得护甲时，英雄在本回合获得等量攻击力
    # 使用.after确保在护甲获得之后触发
    events = GainArmor(FRIENDLY_HERO).after(
        Buff(FRIENDLY_HERO, "TTN_811e2", atk=GainArmor.AMOUNT)
    )


class TTN_811e2:
    """奥丁临时攻击力附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 在回合结束时移除临时攻击力
    events = OWN_TURN_END.on(Destroy(SELF))


class YOG_500:
    """维扎克斯将军 - General Vezax
    <b>突袭</b>。<b>战吼：</b>获得4点护甲值。<b>亡语：</b>失去4点护甲值以再次召唤本随从。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
        GameTag.LEGENDARY: True,
        GameTag.RUSH: True,
    }
    
    play = GainArmor(FRIENDLY_HERO, 4)
    
    def deathrattle(self):
        # 如果有足够的护甲，失去4点护甲并复活
        if self.controller.hero.armor >= 4:
            yield GainArmor(FRIENDLY_HERO, -4)
            yield Summon(CONTROLLER, "YOG_500")
