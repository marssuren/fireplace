# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- WARLOCK 
"""

from ..utils import *
from ..actions import Fatigue

class ETC_068:
    """Baritone Imp - 次中音号小鬼
    2费 2/2 恶魔
    战吼：受到疲劳伤害。获得等量的攻击力和生命值。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RACE: Race.DEMON,
    }
    
    def play(self):
        yield Fatigue(CONTROLLER)
        amount = self.controller.fatigue_counter
        yield Buff(SELF, "ETC_068e", atk=amount, max_health=amount)

class ETC_068e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_034:
    """Opera Soloist - 歌剧独演者
    5费 4/6 恶魔
    战吼：如果你没有控制其他随从，对所有敌方随从造成3点伤害。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,
        GameTag.COST: 5,
        GameTag.RACE: Race.DEMON,
    }
    
    def play(self):
        others = self.controller.field.exclude(self)
        if len(others) == 0:
            yield Hit(ENEMY_MINIONS, 3)

class ETC_081:
    """Void Virtuoso - 虚空协奏者
    1费 1/3 恶魔
    在你的回合中，你的英雄免疫。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
        GameTag.RACE: Race.DEMON,
    }
    update = Find(CURRENT_PLAYER + CONTROLLER) & Refresh(
        FRIENDLY_HERO, {GameTag.IMMUNE: True}
    )

class ETC_069:
    """Crescendo - 渐强声浪
    2费法术
    受到疲劳伤害。对所有敌人造成等量的伤害。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    def play(self):
        yield Fatigue(CONTROLLER)
        amount = self.controller.fatigue_counter
        yield Hit(ALL_ENEMIES, amount)

class ETC_083:
    """Demonic Dynamics - 邪魔修音
    3费法术
    发现两张恶魔牌。压轴：使其获得+1/+2。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    def play(self):
        def _discover_with_finite():
            action = Discover(RandomMinion(race=Race.DEMON))
            if self.controller.mana == 0:
                action = action.then(Give(CONTROLLER, Discover.CARD), Buff(Discover.CARD, "ETC_083e"))
            else:
                action = action.then(Give(CONTROLLER, Discover.CARD))
            return action

        yield _discover_with_finite()
        yield _discover_with_finite()

class ETC_083e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 2, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_082:
    """Dirge of Despair - 绝望哀歌
    6费法术
    对一个角色造成3点伤害。如果消灭该角色，从你的牌库中召唤一个恶魔。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    def play(self):
        target = self.target
        yield Hit(target, 3)
        if target.to_be_destroyed or (target.type == CardType.MINION and target.health <= 0) or (target.type == CardType.HERO and target.health <= 0):
             yield Summon(CONTROLLER, RandomMinion(race=Race.DEMON, from_deck=True))

class JAM_031:
    """Reverberations - 回荡混响
    3费法术
    召唤一个随从的复制。复制和本体都会在受到伤害后死亡。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    def play(self):
        target = self.target
        yield Buff(target, "JAM_031e")
        copy = yield Summon(CONTROLLER, ExactCopy(target))
        if copy:
            yield Buff(copy, "JAM_031e")

class JAM_031e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = Damage(OWNER).after(Destroy(OWNER))

class ETC_070:
    """Crazed Conductor - 疯狂的指挥
    4费 3/4 恶魔
    战吼：受到疲劳伤害。召唤相同数量的3/3的小鬼。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.RACE: Race.DEMON,
    }
    
    def play(self):
        yield Fatigue(CONTROLLER)
        amount = self.controller.fatigue_counter
        yield Summon(CONTROLLER, "ETC_070t") * amount

class ETC_070t:
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.RACE: Race.DEMON}

class ETC_084:
    """Felstring Harp - 邪弦竖琴
    2费 0/3 武器
    每当你的英雄即将在你的回合受到伤害，改为恢复2点生命值。失去1点耐久度。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 2,
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
    }
    events = Predamage(FRIENDLY_HERO, CURRENT_TURN).on(
        Predamage(FRIENDLY_HERO, 0),
        Heal(FRIENDLY_HERO, 2),
        Hit(SELF, 1)
    )

class JAM_030:
    """Fanottem, Lord of the Opera - 歌剧魔神范诺登
    30费 15/15 恶魔
    嘲讽，吸血。本牌的法力值消耗等同于你的牌库中卡牌的数量。
    """
    tags = {
        GameTag.ATK: 15,
        GameTag.HEALTH: 15,
        GameTag.COST: 30,
        GameTag.RACE: Race.DEMON,
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
    }
    update = Refresh(SELF, {GameTag.COST: SET(Count(FRIENDLY_DECK))})

class ETC_071:
    """Rin, Orchestrator of Doom - 末日管弦家林恩
    5费 3/6 恶魔
    嘲讽。亡语：双方玩家各抽两张牌，各弃两张牌，并各摧毁牌库顶的两张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 5,
        GameTag.RACE: Race.DEMON,
        GameTag.TAUNT: True,
    }
    
    deathrattle = (
        Draw(ALL_PLAYERS) * 2,
        Discard(ALL_PLAYERS, amount=2),
        Destroy(RANDOM(FRIENDLY_DECK) * 2),
        Destroy(RANDOM(ENEMY_DECK) * 2),
    )

class ETC_085:
    """Symphony of Sins - 罪孽交响曲
    6费法术
    发现并演奏一段乐章。将其他六段乐章洗入你的牌库。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
        GameTag.LEGENDARY: True,
    }
    
    def play(self):
        movements = [
            "ETC_085t", "ETC_085t2", "ETC_085t3", "ETC_085t4", 
            "ETC_085t5", "ETC_085t6", "ETC_085t7"
        ]
        cards = [self.controller.card(id, zone=Zone.SETASIDE) for id in movements]
        yield Discover(GenericChoice(cards))
        
        chosen_cards = []
        for c in cards:
            if c.zone == Zone.HAND:
                chosen_cards.append(c)
        
        unchosen_cards = []
        for c in cards:
            if c.zone != Zone.HAND and c.zone != Zone.PLAY and c.zone != Zone.GRAVEYARD:
                 unchosen_cards.append(c)
                 
        if chosen_cards:
            yield Play(CONTROLLER, chosen_cards[0])
            
        if unchosen_cards:
            yield Shuffle(CONTROLLER, unchosen_cards)

class ETC_085t:
    """Movement of Desire - 欲望乐章
    3费 暗影
    吸血，抽到时施放。对敌方英雄造成6点伤害。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.LIFESTEAL: True, GameTag.CASTSWHENDRAWN: True}
    play = Hit(ENEMY_HERO, 6)
    
class ETC_085t2:
    """Movement of Envy - 嫉妒乐章
    3费 暗影
    抽到时施放。移除对手牌库顶的6张牌。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.CASTSWHENDRAWN: True}
    play = Destroy(RANDOM(ENEMY_DECK) * 6)

class ETC_085t3:
    """Movement of Gluttony - 暴食乐章
    3费 暗影
    抽到时施放。使你手牌中的所有随从牌获得+2/+2。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.CASTSWHENDRAWN: True}
    play = Buff(FRIENDLY_HAND + MINION, "ETC_085t3e")

class ETC_085t3e:
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_085t4:
    """Movement of Greed - 贪婪乐章
    3费 暗影
    抽到时施放。抽六张牌。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.CASTSWHENDRAWN: True}
    play = Draw(CONTROLLER) * 6

class ETC_085t5: 
    """Movement of Pride - 傲慢乐章
    3费 暗影
    抽到时施放。抽一张随从牌，并使其法力值消耗减少（6）点。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.CASTSWHENDRAWN: True}
    play = Draw(CONTROLLER, RandomMinion()).then(Buff(Draw.CARD, "ETC_085t5e"))

class ETC_085t5e:
    tags = {GameTag.COST: -6, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_085t6:
    """Movement of Sloth - 怠惰乐章
    3费 暗影
    抽到时施放。召唤一个6/6并具有嘲讽和复生的恶魔。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.CASTSWHENDRAWN: True}
    play = Summon(CONTROLLER, "ETC_085t6t")

class ETC_085t6t:
    """Sargeras's Spawn - 萨格拉斯的子嗣"""
    tags = {GameTag.ATK: 6, GameTag.HEALTH: 6, GameTag.TAUNT: True, GameTag.REBORN: True, GameTag.RACE: Race.DEMON}

class ETC_085t7:
    """Movement of Wrath - 暴怒乐章
    3费 暗影
    抽到时施放。对所有角色造成6点伤害。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 3, GameTag.SPELL_SCHOOL: SpellSchool.SHADOW, GameTag.CASTSWHENDRAWN: True}
    play = Hit(ALL_CHARACTERS, 6)
    
class JAM_032:
    """Fiddlefire Imp - 燃琴小鬼
    2费 3/2 恶魔
    战吼：随机将法师和术士的各一张火焰法术牌置入你的手牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RACE: Race.DEMON,
    }
    
    def play(self):
        yield Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE, spell_school=SpellSchool.FIRE))
        yield Give(CONTROLLER, RandomSpell(card_class=CardClass.WARLOCK, spell_school=SpellSchool.FIRE))
