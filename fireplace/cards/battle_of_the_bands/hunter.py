# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- HUNTER 
"""

from ..utils import *

class ETC_833:
    """Arrow Smith - 箭矢工匠
    2费 2/3
    在你施放一个法术后，对生命值最低的敌人造成1点伤害。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    events = Play(CONTROLLER, SPELL).after(Hit(
            RANDOM(ENEMY_CHARACTERS + (CURRENT_HEALTH == OpAttr(ENEMY_CHARACTERS, "health", min))),
            1
        ))

class ETC_201:
    """Bunch of Bananas - 一串香蕉
    1费法术
    使一个随从获得+1/+1。将一串还剩2根的香蕉置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    play = Buff(TARGET, "EX1_014t"), Give(CONTROLLER, "ETC_201t")

class ETC_201t:
    """Bunch of Bananas - 一串香蕉 (2 left)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 1, GameTag.SPELL_SCHOOL: SpellSchool.NATURE}
    play = Buff(TARGET, "EX1_014t"), Give(CONTROLLER, "ETC_201t2")

class ETC_201t2:
    """Bunch of Bananas - 一串香蕉 (1 left)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 1, GameTag.SPELL_SCHOOL: SpellSchool.NATURE}
    play = Buff(TARGET, "EX1_014t"), Give(CONTROLLER, "ETC_201t3")

class ETC_201t3:
    """Bunch of Bananas - 一串香蕉 (Last)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 1, GameTag.SPELL_SCHOOL: SpellSchool.NATURE}
    play = Buff(TARGET, "EX1_014t")

class JAM_004:
    """Hollow Hound - 镂骨恶犬
    6费 3/6 野兽
    吸血，突袭。同时对其攻击目标相邻的随从造成伤害。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 6,
        
        GameTag.LIFESTEAL: True,
        GameTag.RUSH: True,
    }
    # CLEAVE targets ADJACENT_TO(Attack.DEFENDER).
    # Trigger on Attack event.
    events = Attack(SELF, MINION).on(CLEAVE)

class ETC_831:
    """Thornmantle Musician - 刺鬃乐师
    1费 1/3 野兽
    压轴：你召唤的下一只野兽获得+1/+1。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
        
    }
    
    def play(self):
        if self.controller.mana == 0:
            yield Buff(CONTROLLER, "ETC_831e")

class ETC_831e:
    """Musician's Aura"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = Summon(CONTROLLER, BEAST).on(Buff(Summon.CARD, "ETC_831buff"), Destroy(SELF))

class ETC_831buff:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_840:
    """Banjosaur - 班卓龙
    10费 5/5 野兽
    突袭。每当本随从攻击时，抽一张野兽牌并获得其属性值。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 6, # 5/6 stats commonly
        GameTag.COST: 10,
        
        GameTag.RUSH: True,
    }
    
    # "Whenever this attacks" -> Attack(SELF). 
    # Draw beast, then buff self.
    events = Attack(SELF).on(
        Draw(CONTROLLER, RandomMinion(race=Race.BEAST)).then(
            Buff(SELF, "ETC_840e", atk=Attr(Draw.CARD, GameTag.ATK), max_health=Attr(Draw.CARD, GameTag.HEALTH))
        )
    )

class ETC_840e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_207:
    """Barrel of Monkeys - 一桶欢猢
    2费法术
    召唤一只1/4并具有嘲讽的猴子。将一桶还剩2只的欢猢置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    play = Summon(CONTROLLER, "ETC_207t"), Give(CONTROLLER, "ETC_207t2")

class ETC_207t:
    """Monkey - 猴子"""
    race = Race.BEAST
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 4, GameTag.TAUNT: True, }

class ETC_207t2:
    """Barrel of Monkeys (2 left)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 2, GameTag.SPELL_SCHOOL: SpellSchool.NATURE}
    play = Summon(CONTROLLER, "ETC_207t"), Give(CONTROLLER, "ETC_207t3")

class ETC_207t3:
    """Barrel of Monkeys (1 left)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 2, GameTag.SPELL_SCHOOL: SpellSchool.NATURE}
    play = Summon(CONTROLLER, "ETC_207t"), Give(CONTROLLER, "ETC_207t4")

class ETC_207t4:
    """Barrel of Monkeys (Last)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 2, GameTag.SPELL_SCHOOL: SpellSchool.NATURE}
    play = Summon(CONTROLLER, "ETC_207t")

class ETC_838:
    """Big Dreams - 宏大梦想
    5费法术
    从你的手牌中召唤法力值消耗最高的野兽，使其休眠2回合。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        beasts = [c for c in self.controller.hand if c.race == Race.BEAST]
        if beasts:
            max_cost = max(c.cost for c in beasts)
            targets = [c for c in beasts if c.cost == max_cost]
            target = self.game.random.choice(targets)
            # Summon then apply Dormant
            minion = yield Summon(CONTROLLER, target)
            if minion:
                yield Dormant(minion, 2)

class JAM_003:
    """Hidden Meaning - 暗藏深意
    2费 奥秘
    奥秘：当你的对手在没有法力值的情况下结束其回合时，随机召唤一个法力值消耗为（3）的随从。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SECRET: True,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    # Check enemy mana at end of turn.
    # MANA(OPPONENT) gives current available mana.
    secret = EndTurn(OPPONENT).on(
        (MANA(OPPONENT) == 0) & (Summon(CONTROLLER, RandomMinion(cost=3)))
    )

class ETC_028:
    """Harmonica Soloist - 口琴独演者
    4费 3/3 野兽
    战吼：如果你没有控制其他随从，发现并施放一个奥秘。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        
    }
    
    def play(self):
        if len(self.controller.field.exclude(self)) == 0:
             # Discover and Play
             yield Discover(RandomSecret()).then(Play(CONTROLLER, Discover.CARD))

class ETC_832:
    """Jungle Jammer - 丛林弹唱琴
    4费 4/2 武器
    亡语：随机召唤一只法力值消耗为（1）的野兽。（装备期间，施放法术以提升此效果！）
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 4,
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
    }
    # Store upgrade level in TAG_SCRIPT_DATA_NUM_1
    # Base 1.
    events = Play(CONTROLLER, SPELL).on(Buff(SELF, "ETC_832e"))
    
    def deathrattle(self):
        # Base 1 + upgrades
        cost = 1 + self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        yield Summon(CONTROLLER, RandomMinion(race=Race.BEAST, cost=cost))

class ETC_832e:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_836:
    """Mister Mukla - 穆克拉先生
    6费 10/10 野兽
    突袭。战吼：用香蕉填满你对手的手牌。
    """
    race = Race.BEAST
    tags = {
        GameTag.ATK: 10,
        GameTag.HEALTH: 10,
        GameTag.COST: 6,
        
        GameTag.RUSH: True,
    }
    
    def play(self):
        # Fill hand
        amount = 10 - len(self.controller.opponent.hand)
        if amount > 0:
            yield Give(OPPONENT, "EX1_014t") * amount

class ETC_208:
    """Stranglethorn Heart - 荆棘谷之心
    10费法术
    可交易。复活所有法力值消耗大于或等于（5）点的友方野兽。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 10,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
        GameTag.TRADEABLE: True,
    }
    play = Summon(CONTROLLER, Copy(FRIENDLY_GRAVEYARD + BEAST + (COST >= 5)))
