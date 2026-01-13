# -*- coding: utf-8 -*-
"""
TITANS 扩展包 - MAGE
"""
from ..utils import *
from ... import enums


# COMMON

class TTN_077:
    """酷冰机器人 - Chill-o-matic
    <b>磁力</b>。<b>冻结</b>任何受到本随从伤害的角色。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.MECHANICAL,
        GameTag.MAGNETIC: True,
    }
    
    magnetic = MAGNETIC("TTN_077e")


class TTN_077e:
    """酷冰机器人附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.MAGNETIC: True,
    }
    # 造成伤害后冻结目标
    events = Damage(SELF).on(Freeze(Damage.TARGET))


class TTN_095:
    """流水档案管理员 - Aqua Archivist
    <b>战吼：</b>你的下一张元素牌的法力值消耗减少（2）点。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }
    
    play = Buff(CONTROLLER, "TTN_095e")


class TTN_095e:
    """古老之水 - Ancient Waters"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    auras = [Buff(FRIENDLY_HAND + ELEMENTAL, "TTN_095e2")]
    events = Play(CONTROLLER, ELEMENTAL).on(Destroy(SELF))


class TTN_095e2:
    """减费附魔"""
    tags = {
        GameTag.COST: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_477:
    """熔火符文 - Molten Rune
    造成$3点伤害。随机获取一张法术牌。<b>锻造：</b>本牌施放两次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    play = [
        Hit(TARGET, 3),
        Give(CONTROLLER, RandomSpell())
    ]


class TTN_477t:
    """熔火符文 - Molten Rune (Forged)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 施放两次
        yield Hit(TARGET, 3)
        yield Give(CONTROLLER, RandomSpell())
        yield Hit(TARGET, 3)
        yield Give(CONTROLLER, RandomSpell())


class YOG_519:
    """腐化残渣 - Tainted Remnant
    <b>战吼：</b>如果你在上个回合使用过元素牌，则造成7点伤害，随机分配到所有敌人身上。
    """
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }
    
    def play(self):
        # 检查上回合是否使用过元素牌
        if ELEMENTAL_PLAYED_LAST_TURN.evaluate(self):
            yield Hit(RANDOM_ENEMY_CHARACTER, 1) * 7


# RARE

class TTN_475:
    """破链角斗士 - Unchained Gladiator
    <b>战吼：</b>抽一张牌。你在上个回合每使用一张元素牌，重复一次。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }
    
    def play(self):
        # 获取上回合使用的元素牌数量
        elementals_played = getattr(self.controller, 'elemental_played_last_turn', 0)
        # 至少抽1张，加上上回合的元素牌数
        for _ in range(1 + elementals_played):
            yield Draw(CONTROLLER)



class UnusedSchoolSpellPicker(RandomCardPicker):
    def find_cards(self, source, **filters):
        card_ids = super().find_cards(source, **filters)
        used_schools = getattr(source.controller, 'spell_schools_played_this_game', set())
        
        from fireplace.cards import db
        valid_cards = []
        for card_id in card_ids:
            school = getattr(db[card_id], 'spell_school', 0)
            if school and school not in used_schools:
                valid_cards.append(card_id)
        return valid_cards


class TTN_476:
    """魔法新发现 - Discovery of Magic
    <b>发现</b>一张你在本局对战中尚未施放过的派系的法术牌<i>（任意职业）</i>。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        # 使用自定义挑选器发现未使用过派系的法术
        picker = UnusedSchoolSpellPicker(type=CardType.SPELL, collectible=True)
        yield Discover(picker).then(Give(CONTROLLER, Discover.CARD))


class TTN_478:
    """求知造物 - Inquisitive Creation
    <b>战吼：</b>对所有敌方随从造成1点伤害。<i>（在本局对战中，你每施放过一个派系的法术都会提升！）</i>
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.CARDRACE: Race.MECHANICAL,
    }
    
    def play(self):
        # 获取已使用的法术派系数量
        spell_schools_count = len(getattr(self.controller, 'spell_schools_played_this_game', set()))
        damage = 1 + spell_schools_count
        yield Hit(ENEMY_MINIONS, damage)


class YOG_507:
    """虚空经文 - Void Scripture
    <b>发现</b>一张法术牌。如果你有足够的法力值使用发现的法术牌，则随机对一个敌人施放它的复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    def play(self):
        # 发现一张法术
        cards = yield Discover(RandomSpell()).then(Give(CONTROLLER, Discover.CARD))
        
        if cards and cards[0]:
            discovered_spell = cards[0]
            # 检查是否有足够法力值
            if self.controller.mana >= discovered_spell.cost:
                # 施放复制到随机敌人
                yield CastSpell(Copy(discovered_spell), TARGET=RANDOM_ENEMY_CHARACTER)


class YOG_518:
    """多事的仆从 - Meddlesome Servant
    <b>战吼：</b>在本局对战中，如果你施放过5个或以上法术，抽两张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 检查本局施放的法术数量
        if self.controller.num_spells_played_this_game >= 5:
            yield Draw(CONTROLLER, 2)


# EPIC

class TTN_085:
    """诺甘农的智慧 - Wisdom of Norgannon
    抽两张牌。在本局对战中，你每施放过一个不同派系的法术，本牌的法力值消耗便减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    
    cost_mod = lambda self, i: -len(getattr(self.controller, 'spell_schools_played_this_game', set()))
    
    play = Draw(CONTROLLER, 2)


class TTN_480:
    """元素激励 - Elemental Inspiration
    在本局对战中，你每施放过一个派系的法术，召唤一个4/5并具有一项随机<b>额外效果</b>的元素。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
    }
    
    def play(self):
        # 获取已使用的法术派系数量
        spell_schools_count = len(getattr(self.controller, 'spell_schools_played_this_game', set()))
        
        for _ in range(spell_schools_count):
            yield Summon(CONTROLLER, "TTN_480t")


class TTN_480t:
    """激励元素 - Inspired Elemental"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }
    def play(self):
        # 随机额外效果（嘲讽、冲锋、圣盾等）
        keywords = [
            GameTag.DIVINE_SHIELD,
            GameTag.TAUNT,
            GameTag.RUSH,
            GameTag.WINDFURY,
            GameTag.STEALTH,
            GameTag.POISONOUS,
            GameTag.REBORN,
            GameTag.LIFESTEAL
        ]
        
        # 随机选择一个buff
        # 注意：这里使用游戏随机数生成器以保证确定性
        effect = self.game.random.choice(keywords)
        yield SetTags(self, {effect: True})


# LEGENDARY

class TTN_071:
    """西芙 - Sif
    <b>法术伤害+1</b> <i>（在本局对战中，你每施放过一个派系的法术都会提升！）</i>
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,
        GameTag.COST: 6,
        GameTag.LEGENDARY: True,
        GameTag.CARDRACE: Race.DRAGON,
    }
    
    @property
    def spellpower(self):
        # 基础法伤+1，每个派系额外+1
        spell_schools_count = len(getattr(self.controller, 'spell_schools_played_this_game', set()))
        return 1 + spell_schools_count


class TTN_075:
    """诺甘农 - Norgannon
    <b>泰坦</b> 在本随从使用一个技能后，其他技能的效果翻倍。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 8,
        GameTag.COST: 6,
        GameTag.LEGENDARY: True,
        GameTag.TITAN: True,
        enums.TITAN_ABILITY_COUNT: 3,  # 泰坦技能次数
    }
    
    # 泰坦技能使用后，标记效果翻倍
    # 使用 POWER_MULTIPLIER 存储翻倍次数（指数），值为 N 代表 2^N 倍

    def _update_multiplier(self):
        # 增加翻倍指数
        yield SetTags(self, {
            enums.POWER_MULTIPLIER: getattr(self, 'power_multiplier', 0) + 1
        })
    
    def titan_ability_1(self):
        """魔法洞察 - Arcane Insight
        抽两张牌。
        """
        # 计算当前倍率
        power = 1 << self.tags.get(enums.POWER_MULTIPLIER, 0)
        yield Draw(CONTROLLER, 2 * power)
        yield self._update_multiplier()
    
    def titan_ability_2(self):
        """奥术爆发 - Arcane Burst  
        对所有敌方随从造成2点伤害。
        """
        power = 1 << self.tags.get(enums.POWER_MULTIPLIER, 0)
        yield Hit(ENEMY_MINIONS, 2 * power)
        yield self._update_multiplier()
    
    def titan_ability_3(self):
        """奥术护盾 - Arcane Shield
        获得8点护甲值。
        """
        power = 1 << self.tags.get(enums.POWER_MULTIPLIER, 0)
        yield GainArmor(FRIENDLY_HERO, 8 * power)
        yield self._update_multiplier()
