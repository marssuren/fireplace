# -*- coding: utf-8 -*-
"""
TITANS 扩展包 - DRUID
"""
from ..utils import *


# COMMON

class TTN_950:
    """林木幼苗 - Forest Seedlings
    召唤两个1/1的树苗。<i>（2回合后长成）</i>
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        # 召唤两个树苗，2回合后成长
        yield Summon(CONTROLLER, "TTN_950t") * 2


class TTN_950t:
    """树苗 - Sapling"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDRACE: Race.TREANT,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 2,  # 成长计数器
    }
    
    events = OWN_TURN_BEGIN.on(
        Buff(SELF, "TTN_950tick"),
        Condition(
            Equal(Tag(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1), 0),
            (Morph(SELF, "TTN_950t2"), )
        )
    )


class TTN_950tick:
    """成长计数"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_950t2:
    """树人 - Treant (Grown)"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDRACE: Race.TREANT,
    }


class TTN_954:
    """栽培 - Cultivation
    使你的随从获得+2/+2。在本局对战中，你每召唤一个树人，本牌的法力值消耗便减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 8,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    # 每召唤树人减少1费
    events = Summon(CONTROLLER, MINION + TREANT).on(Buff(SELF, "TTN_954e"))
    
    play = Buff(FRIENDLY_MINIONS, "TTN_954buff")


class TTN_954e:
    """法力值消耗减少"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_954buff:
    """+2/+2 增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_955:
    """生命缚誓者的礼物 - Lifebinder's Gift
    <b>抉择：</b>随机获取2张自然法术牌；或者使你手牌中法术牌的法力值消耗减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("TTN_955a", "TTN_955b")
    
    def play(self):
        if self.choice == "TTN_955a":
            # 获取2张自然法术
            yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.NATURE)) * 2
        elif self.choice == "TTN_955b":
            # 手牌法术减费
            yield Buff(FRIENDLY_HAND + SPELL, "TTN_955e")


class TTN_955a:
    """自然的恩赐 - Nature's Gift"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class TTN_955b:
    """法力涌动 - Mana Surge"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class TTN_955e:
    """法力值消耗减少"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class YOG_403:
    """空中施肥者 - Aerosoilizer
    <b>战吼，亡语：</b>召唤一个2/2的树人。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    play = Summon(CONTROLLER, "YOG_403t")
    deathrattle = Summon(CONTROLLER, "YOG_403t")


class YOG_403t:
    """树人 - Treant"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDRACE: Race.TREANT,
    }


# RARE

class TTN_927:
    """护园森灵 - Conservator Nymph
    <b>战吼：</b>将一个友方树人变形成为5/5并具有<b>嘲讽</b>的古树。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    play = Morph(TARGET, "TTN_927t")
    powered_up = Find(FRIENDLY_MINIONS + TREANT)


class TTN_927t:
    """古树 - Ancient"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True,
    }


class TTN_930:
    """雪莲幼苗 - Frost Lotus Seedling
    抽一张牌。获得5点护甲值。<i>（3回合后长成。）</i>
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        # 抽牌并获得护甲
        yield Draw(CONTROLLER)
        yield GainArmor(FRIENDLY_HERO, 5)
        # 3回合后效果增强
        yield Buff(CONTROLLER, "TTN_930e")


class TTN_930e:
    """雪莲成长效果"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 成长计数器
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    events = OWN_TURN_BEGIN.on(
        Buff(SELF, "TTN_930tick"),
        Condition(
            Equal(Tag(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1), 0),
            (
                Draw(CONTROLLER),
                GainArmor(FRIENDLY_HERO, 5),
                Destroy(SELF)
            )
        )
    )


class TTN_930tick:
    """成长计数"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_951:
    """自然之拥 - Embrace of Nature
    抽一张<b>抉择</b>牌。<b>锻造：</b>并使其同时拥有两种效果。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        # 抽一张抉择牌
        cards = yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + CHOOSE_ONE))
        # Forge 版本会给予双重效果 buff
        # 这需要在 Forge 版本中实现


class TTN_951t:
    """自然之拥 - Embrace of Nature (Forged)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        # 抽一张抉择牌并使其拥有双重效果
        cards = yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + CHOOSE_ONE))
        if cards and cards[0]:
            # 给予 Fandral 效果（双重抉择）
            yield Buff(cards[0], "TTN_951e")


class TTN_951e:
    """双重抉择"""
    tags = {
        GameTag.CHOOSE_BOTH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class YOG_528:
    """受污染的鞭笞者 - Contaminated Lasher
    <b>战吼：</b>在本局对战中， 如果你施放过5个或以上法术，复原4个法力水晶。@<i>（还剩{0}个！）</i>@<i>（已经就绪！）</i>
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 检查是否施放过5个或以上法术
        if self.controller.num_spells_played_this_game >= 5:
            yield FillMana(CONTROLLER, 4)


class YOG_529:
    """禁忌之果 - Forbidden Fruit
    消耗你所有的法力值。<b>抉择：</b>获得在本回合中的等量攻击力；或者获得双倍的护甲值。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("YOG_529a", "YOG_529b")
    
    def play(self):
        mana_spent = self.controller.mana
        # 消耗所有法力值
        yield SpendMana(CONTROLLER, mana_spent)
        
        if self.choice == "YOG_529a":
            # 获得等量攻击力
            if mana_spent > 0:
                yield Buff(FRIENDLY_HERO, "YOG_529e_atk", atk=mana_spent)
        elif self.choice == "YOG_529b":
            # 获得双倍护甲值
            yield GainArmor(FRIENDLY_HERO, mana_spent * 2)


class YOG_529a:
    """力量 - Strength"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class YOG_529b:
    """坚韧 - Resilience"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class YOG_529e_atk:
    """攻击力增益"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = OWN_TURN_END.on(Destroy(SELF))
    
    def apply(self, target):
        super().apply(target)
        if target.type == CardType.HERO:
            target.controller.attack_gained_this_turn += self.tags.get(GameTag.ATK, 0)


# EPIC

class TTN_503:
    """艾欧娜尔的信徒 - Disciple of Eonar
    <b>战吼：</b>你的下一个<b>抉择</b>牌或技能同时拥有两种效果。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    play = Buff(CONTROLLER, "TTN_503e")


class TTN_503e:
    """双重抉择效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 下一张抉择牌拥有双重效果
    auras = [Buff(FRIENDLY_HAND + CHOOSE_ONE, "TTN_503buff")]
    events = Play(CONTROLLER, CHOOSE_ONE).on(Destroy(SELF))


class TTN_503buff:
    """双重抉择"""
    tags = {
        GameTag.CHOOSE_BOTH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_926:
    """生长古树 - Ancient of Growth
    <b>抉择：</b>召唤三个2/2的树人；或者将你的树人变形成为5/5并具有<b>嘲讽</b>的古树。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("TTN_926a", "TTN_926b")
    
    def play(self):
        if self.choice == "TTN_926a":
            # 召唤三个2/2树人
            yield Summon(CONTROLLER, "TTN_926t") * 3
        elif self.choice == "TTN_926b":
            # 将所有树人变形为古树
            yield Morph(FRIENDLY_MINIONS + TREANT, "TTN_927t")


class TTN_926a:
    """召唤树人 - Summon Treants"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class TTN_926b:
    """成长 - Growth"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class TTN_926t:
    """树人 - Treant"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDRACE: Race.TREANT,
    }


# LEGENDARY

class TTN_903:
    """生命的缚誓者艾欧娜尔 - Eonar, the Life-Binder
    <b>泰坦</b> 在本随从使用一个技能后，召唤一棵5/5并具有<b>嘲讽</b>的古树。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 7,
        GameTag.COST: 10,
        GameTag.LEGENDARY: True,
        GameTag.TITAN: True,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 泰坦技能次数
    }
    
    # 泰坦技能使用后触发
    events = Activate(CONTROLLER, TITAN_ABILITY).on(
        Summon(CONTROLLER, "TTN_903t4")
    )
    
    def titan_ability_1(self):
        """自然生长 - Spontaneous Growth
        抽牌直到你的手牌满。
        """
        hand_size = len(self.controller.hand)
        max_hand_size = self.controller.max_hand_size
        cards_to_draw = max_hand_size - hand_size
        if cards_to_draw > 0:
            yield Draw(CONTROLLER, cards_to_draw)
    
    def titan_ability_2(self):
        """丰收 - Bountiful Harvest
        将你的英雄恢复至满生命值。
        """
        yield FullHeal(FRIENDLY_HERO)
    
    def titan_ability_3(self):
        """繁荣 - Flourish
        刷新你的法力水晶。
        """
        yield FillMana(CONTROLLER, self.controller.max_mana)


class TTN_903t:
    """古树 - Ancient"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True,
    }


class TTN_903t4:
    """永恒古树 - Timeless Ancient
    泰坦技能使用后召唤的古树
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True,
    }


class TTN_940:
    """自然守护者弗蕾亚 - Freya, Keeper of Nature
    <b>抉择：</b>复制你的手牌；或者召唤所有其他友方随从的复制。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6,
        GameTag.COST: 8,
        GameTag.LEGENDARY: True,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("TTN_940a", "TTN_940b")
    
    def play(self):
        if self.choice == "TTN_940a":
            # 复制手牌
            for card in self.controller.hand:
                if card != self:
                    yield Give(CONTROLLER, Copy(card))
        elif self.choice == "TTN_940b":
            # 召唤所有其他随从的复制
            minions = [m for m in self.controller.field if m != self]
            for minion in minions:
                yield Summon(CONTROLLER, Copy(minion))


class TTN_940a:
    """复制手牌 - Copy Hand"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class TTN_940b:
    """复制随从 - Copy Minions"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}

