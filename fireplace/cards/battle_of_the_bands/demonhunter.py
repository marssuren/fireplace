# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- DEMONHUNTER 
"""

from ..utils import *

class JAM_016:
    """Abyssal Bassist - 渊狱贝斯手
    7费 4/7 恶魔
    嘲讽，吸血。在本局对战中，你每装备过一把武器，本牌的法力值消耗便减少（2）点。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 7,
        GameTag.COST: 7,
        GameTag.RACE: Race.DEMON,
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
    }
    # "Equipped a weapon" usually means Play weapon or Equip effect.
    # We use Play(WEAPON) as a proxy, or check generic counter.
    # Standard hearthstone rule for "played or equipped" counts total weapons.
    # Fireplace `num_weapons_played_this_game` tracks played cards.
    # There is no global "times equipped" counter easily accessible.
    # We will use TIMES_PLAYED_THIS_GAME(card_type=WEAPON) proxy.
    cost_mod = -2 * Count(FRIENDLY_HERO + TIMES_CARD_TYPE_PLAYED(CardType.WEAPON))

class ETC_026:
    """Guitar Soloist - 吉他独演者
    5费 4/3
    战吼：如果你没有控制其他随从，抽一张法术牌，一张随从牌和一张武器牌。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
    }
    
    def play(self):
        if len(self.controller.field.exclude(self)) == 0:
            yield Draw(CONTROLLER, RandomSpell())
            yield Draw(CONTROLLER, RandomMinion())
            yield Draw(CONTROLLER, RandomWeapon())

class ETC_411:
    """SECURITY!! - 保安！！
    2费法术 (Fel)
    召唤两个1/1并具有突袭的伊利达雷。流放：再召唤一个。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    def play(self):
        yield Summon(CONTROLLER, "ETC_411t") * 2
        if self.is_outcast:
             yield Summon(CONTROLLER, "ETC_411t")

class ETC_411t:
    """Illidari Initiate"""
    tags = {
        GameTag.ATK: 1, 
        GameTag.HEALTH: 1, 
        GameTag.RACE: Race.DEMON, 
        GameTag.RUSH: True
    }

class ETC_394:
    """Taste of Chaos - 混乱品味
    1费法术 (Fel)
    对一个随从造成2点伤害。压轴：发现一张邪能法术牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    def play(self):
        yield Hit(TARGET, 2)
        if self.controller.mana == 0:
            yield Discover(RandomSpell(spell_school=SpellSchool.FEL))

class ETC_405:
    """Glaivetar - 战刃吉他
    4费 4/2 武器
    亡语：抽1张牌。（装备期间，使用流放牌以提升此效果！）
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 4,
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
    }
    
    # Listen for Outcast card played
    events = Play(CONTROLLER, OUTCAST).on(Buff(SELF, "ETC_405e"))
    
    def deathrattle(self):
        amount = 1 + self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        yield Draw(CONTROLLER) * amount

class ETC_405e:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class JAM_018:
    """Remixed Rhapsody - 混搭狂想曲
    5费法术 (Fel)
    对所有随从造成3点伤害。在你的手牌中时会获得一项额外效果，该效果每回合都会改变。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "JAM_018a"))
        
    play = Hit(ALL_MINIONS, 3) # Default form if played (though usually transforms)

class JAM_018a:
    """Wailing Rhapsody - 哀嚎狂想曲 (Lifesteal)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 5, GameTag.SPELL_SCHOOL: SpellSchool.FEL, GameTag.LIFESTEAL: True}
    play = Hit(ALL_MINIONS, 3)
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "JAM_018b"))

class JAM_018b:
    """Emotional Rhapsody - 动情狂想曲 (Cost reduced)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 2, GameTag.SPELL_SCHOOL: SpellSchool.FEL}
    play = Hit(ALL_MINIONS, 3)
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "JAM_018c"))

class JAM_018c:
    """Resounding Rhapsody - 洪亮狂想曲 (Hit Enemy Hero)"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 5, GameTag.SPELL_SCHOOL: SpellSchool.FEL}
    play = Hit(ALL_MINIONS, 3), Hit(ENEMY_HERO, 3)
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "JAM_018d"))

class JAM_018d:
    """Angsty Rhapsody - 焦虑狂想曲 (Finale: Enemies instead?)"""
    # Assuming Finale: Deal 3 to all enemies.
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 5, GameTag.SPELL_SCHOOL: SpellSchool.FEL}
    def play(self):
        if self.controller.mana == 0:
             yield Hit(ALL_ENEMIES, 3)
        else:
             yield Hit(ALL_MINIONS, 3)
    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "JAM_018"))


class ETC_200:
    """Rush the Stage - 突进舞台
    3费法术 (Fel)
    抽两张突袭随从牌，使其法力值消耗减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,  
    }
    
    def play(self):
         # Draw Rush minion x 2
         for _ in range(2):
            yield Draw(CONTROLLER, RandomMinion(mechanics="RUSH")).then(
                Buff(Draw.CARD, "ETC_200e")
            )

class ETC_200e:
    tags = {GameTag.COST: -1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_410:
    """Snakebite - 蛇啮鼓手
    2费 1/1 纳迦
    突袭。战吼：在本回合中每有一个随从死亡，便获得+1/+1。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
        GameTag.RACE: Race.NAGA,
        GameTag.RUSH: True,
    }
    
    def play(self):
        count = len(self.controller.game.killed_this_turn)
        if count > 0:
            yield Buff(SELF, "ETC_410e", atk=count, max_health=count)

class ETC_410e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_398:
    """Eye of Shadow - 暗影之眼
    2费 2/3 恶魔
    你的英雄拥有吸血。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.RACE: Race.DEMON,
    }
    # Aura giving lifesteal to Hero
    auras = [Buff(FRIENDLY_HERO, "ETC_398e")]

class ETC_398e:
    tags = {GameTag.LIFESTEAL: True, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_400:
    """Instrument Smasher - 乐器杀手
    4费 3/6
    每当你的武器被摧毁时，随机装备一把恶魔猎手武器。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 4,
    }
    
    # Event: Friend weapon destroyed -> Equip random DH weapon
    events = Destroy(FRIENDLY_WEAPON).on(
        Equip(CONTROLLER, RandomWeapon(card_class=CardClass.DEMONHUNTER))
    )

class ETC_413:
    """Going Down Swinging - 低沉摇摆
    4费法术 (Fel)
    在本回合中，使你的英雄获得+2攻击力和免疫，然后攻击每个敌方随从。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.FEL,
    }
    
    def play(self):
        # Give Attack + Immune
        yield Buff(FRIENDLY_HERO, "ETC_413e")

        # 攻击所有敌方随从
        # 参考：
        # - badlands/hunter.py WW_815 - 使用 list() 存储目标快照
        # - nathria/warrior.py REV_934 - 使用 can_attack() 检查
        enemies = list(self.controller.opponent.field)
        for enemy in enemies:
            if self.controller.hero.can_attack() and enemy.zone == Zone.PLAY:
                yield Attack(FRIENDLY_HERO, enemy)

class ETC_413e:
    tags = {GameTag.ATK: 2, GameTag.IMMUNE: True, GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))

class ETC_399:
    """Halveria Darkraven - 哈维利亚·墨鸦
    4费 4/3 恶魔
    突袭。在一个友方突袭随从攻击后，使你的随从获得+1攻击力。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.RACE: Race.DEMON,
        GameTag.RUSH: True,
        GameTag.LEGENDARY: True,
    }
    events = Attack(FRIENDLY_MINIONS + RUSH).after(Buff(FRIENDLY_MINIONS, "ETC_399e"))

class ETC_399e:
    tags = {GameTag.ATK: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}
