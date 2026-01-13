# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- DRUID 
"""

from ..utils import *

class JAM_028:
    """Blood Treant - 鲜血树人
    5费 5/5
    消耗生命值，而非法力值。
    """
    race = Race.TREANT
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        # COSTS_HEALTH 功能暂不支持，需要在核心实现
    }

class ETC_379:
    """Harmonic Mood - 悦耳轻音乐
    1费法术
    在本回合中，使你的英雄获得+2攻击力。获得4点护甲值。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        yield GainArmor(FRIENDLY_HERO, 4)
        yield Buff(FRIENDLY_HERO, "ETC_379e")

    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "ETC_379t"))

class ETC_379e:
    tags = {GameTag.ATK: 2, GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = OWN_TURN_END.on(Destroy(SELF))
    
    def apply(self, target):
         super().apply(target)
         if target.type == CardType.HERO:
             target.controller.attack_gained_this_turn += 2

class ETC_379t:
    """Dissonant Mood - 刺耳轻音乐
    1费法术
    在本回合中，使你的英雄获得+4攻击力。获得2点护甲值。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        yield GainArmor(FRIENDLY_HERO, 2)
        yield Buff(FRIENDLY_HERO, "ETC_379te")

    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "ETC_379"))

class ETC_379te:
    tags = {GameTag.ATK: 4, GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = OWN_TURN_END.on(Destroy(SELF))
    
    def apply(self, target):
         super().apply(target)
         if target.type == CardType.HERO:
             target.controller.attack_gained_this_turn += 4

class ETC_375:
    """Peaceful Piper - 沉静的吹笛人
    3费 2/2 野兽
    抉择：抽一张野兽牌；或者发现一张野兽牌。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("ETC_375a", "ETC_375b")
    
    def play(self):
        if self.choice == "ETC_375a":
            yield Draw(CONTROLLER, RandomMinion(race=Race.BEAST))
        elif self.choice == "ETC_375b":
            yield Discover(RandomMinion(race=Race.BEAST))

class ETC_375a:
    """Piper's Song - 悠扬笛声 (Draw)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}
class ETC_375b:
    """Piper's Tune - 动人曲调 (Discover)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}

class JAM_026:
    """Popular Pixie - 人气树精
    2费 3/2
    抉择：复原你的英雄技能；或者使你的下一个英雄技能的法力值消耗为（0）点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("JAM_026a", "JAM_026b")
    
    def play(self):
        if self.choice == "JAM_026a":
            yield RefreshHeroPower(CONTROLLER)
        elif self.choice == "JAM_026b":
            yield Buff(CONTROLLER, "JAM_026e")

class JAM_026a:
    """Refreshment - 提神醒脑"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}
class JAM_026b:
    """Performance - 精彩演出"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}

class JAM_026e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    auras = [Buff(FRIENDLY_HERO_POWER, "JAM_026boost")]
    events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))

class JAM_026boost:
    tags = {GameTag.COST: SET(0)}

class ETC_384:
    """Spread the Word - 散布消息
    4费法术
    抽两张牌。你的英雄每有一点攻击力，本牌的法力值消耗便减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    cost_mod = lambda self, i: -self.controller.hero.atk if self.controller.hero else 0

    play = Draw(CONTROLLER) * 2

class JAM_029:
    """Doomkin - 末日枭兽
    6费 3/4 野兽
    战吼：夺取你对手的一个空的法力水晶。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 6,
        
    }
    
    def play(self):
        # Steal Logic: +1 Empty to self, -1 Max (Empty) from opponent.
        yield GainEmptyMana(CONTROLLER, 1)
        yield DestroyMana(OPPONENT, 1)

class ETC_373:
    """Drum Circle - 集会鼓圈
    7费法术
    抉择：召唤五个2/2的树人；或者使你的所有随从获得+2/+4和嘲讽。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("ETC_373a", "ETC_373b")
    
    def play(self):
        if self.played_as == "ETC_373a":
            yield Summon(CONTROLLER, "ETC_373t") * 5
        elif self.played_as == "ETC_373b":
            yield Buff(FRIENDLY_MINIONS, "ETC_373e")

class ETC_373a:
    """Beat - 鼓点"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}
class ETC_373b:
    """Rhythm - 节奏"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}

class ETC_373t:
    """Treant - 2/2"""
    race = Race.TREANT
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2, }

class ETC_373e:
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 4, GameTag.TAUNT: True, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_385:
    """Groovy Cat - 潮流猎豹
    2费 2/1 野兽
    战吼，亡语：在本局对战中，你的英雄技能使你的英雄多获得1点攻击力。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
        
    }
    
    def play(self):
        yield Buff(CONTROLLER, "ETC_385e")
        
    deathrattle = Buff(CONTROLLER, "ETC_385e")

class ETC_385e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # When Hero Power is activated, give Hero +1 Attack (Temporary for turn)
    events = Activate(CONTROLLER, HERO_POWER).on(Buff(FRIENDLY_HERO, "ETC_385buff"))

class ETC_385buff:
    tags = {GameTag.ATK: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = OWN_TURN_END.on(Destroy(SELF))
    
    def apply(self, target):
         super().apply(target)
         if target.type == CardType.HERO:
             target.controller.attack_gained_this_turn += 1

class ETC_376:
    """Summer Flowerchild - 盛夏花童
    5费 3/5
    战吼：抽两张法力值消耗大于或等于（6）点的牌。压轴：使其法力值消耗减少（1）点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
    }
    
    def play(self):
        # Draw 2 cards with cost >= 6
        cards = yield Draw(CONTROLLER, RandomCard(FRIENDLY_DECK + (COST >= 6))) * 2
        
        # Finale check
        if self.controller.mana == 0 and cards:
            # Cards might be nested lists if multiple draws
            # Draw returns list of lists if multiple
            # [[Card1], [Card2]]
             for batch in cards:
                  if batch:
                      for c in batch:
                          yield Buff(c, "ETC_376e")

class ETC_376e:
    tags = {GameTag.COST: -1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_382:
    """Free Spirit - 自由之魂
    1费 1/2 野兽
    战吼，亡语：在本局对战中，你的英雄技能多获得1点护甲值。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        
    }
    
    def play(self):
        yield Buff(CONTROLLER, "ETC_382e")
        
    deathrattle = Buff(CONTROLLER, "ETC_382e")

class ETC_382e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = Activate(CONTROLLER, HERO_POWER).on(GainArmor(FRIENDLY_HERO, 1))

class ETC_388:
    """Timber Tambourine - 实木手鼓
    4费 2/2 武器
    亡语：召唤1棵5/5的古树。（装备期间，使用法力值消耗5点或以上的卡牌以提升此效果！）
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 4,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }
    
    events = Play(CONTROLLER, (COST >= 5)).on(Buff(SELF, "ETC_388e"))
    
    def deathrattle(self):
        count = 1 + self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        yield Summon(CONTROLLER, "ETC_388t") * count

class ETC_388e:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_388t:
    """Ancient - 5/5 古树"""
    tags = {GameTag.ATK: 5, GameTag.HEALTH: 5}

class ETC_387:
    """Rhythm and Roots - 根音古韵
    4费法术
    秘密抉择：2回合后召唤三棵5/5的古树；或者4回合后召唤三个8/8的巨人。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("ETC_387a", "ETC_387b")
    
    def play(self):
        if self.played_as == "ETC_387a":
            yield Buff(CONTROLLER, "ETC_387e_a")
        elif self.played_as == "ETC_387b":
            yield Buff(CONTROLLER, "ETC_387e_b")

class ETC_387a:
    """Root Down - 扎根"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}
class ETC_387b:
    """Create Rhythm - 创作"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}

class ETC_387e_a:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 2, GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def _on_turn_begin(self):
        # 减少计数器
        yield Buff(SELF, "ETC_387tick")
        # 检查计数器是否为0
        if self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) <= 0:
            yield Summon(CONTROLLER, "ETC_387t_a") * 3
            yield Destroy(SELF)
    
    events = OWN_TURN_BEGIN.on(lambda self, player: self._on_turn_begin())

class ETC_387e_b:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 4, GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def _on_turn_begin(self):
        # 减少计数器
        yield Buff(SELF, "ETC_387tick")
        # 检查计数器是否为0
        if self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) <= 0:
            yield Summon(CONTROLLER, "ETC_387t_b") * 3
            yield Destroy(SELF)
    
    events = OWN_TURN_BEGIN.on(lambda self, player: self._on_turn_begin())

class ETC_387tick:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: -1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_387t_a:
    """Ancient - 5/5"""
    tags = {GameTag.ATK: 5, GameTag.HEALTH: 5}
class ETC_387t_b:
    """Giant - 8/8"""
    tags = {GameTag.ATK: 8, GameTag.HEALTH: 8}

class ETC_386:
    """Zok Fogsnout - 佐克·雾鼻
    7费 6/6 野猪人
    战吼：召唤两个{0}/{1}并具有嘲讽的野猪人。（随你的英雄本回合获得的攻击力和护甲值提升！）
    """
    race = Race.QUILBOAR
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
    }

    def play(self):
        # 召唤两个野猪人
        # Summon returns the list of summoned minions
        token1 = yield Summon(CONTROLLER, "ETC_386t")
        token2 = yield Summon(CONTROLLER, "ETC_386t")
        
        # 获取本回合获得的攻击力和护甲
        atk_gained = self.controller.attack_gained_this_turn
        armor_gained = self.controller.armor_gained_this_turn
        
        # 如果有增益，应用 Buff
        if atk_gained > 0 or armor_gained > 0:
            for token in [token1, token2]:
                if token: # 确保召唤成功
                    # Create custom buff with dynamic stats
                    # Zok's buff is permanent on the tokens
                    yield Buff(token, "ETC_386e", atk=atk_gained, max_health=armor_gained)

class ETC_386e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_386t:
    """Quilboar - Token"""
    race = Race.QUILBOAR
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1, GameTag.TAUNT: True, }
