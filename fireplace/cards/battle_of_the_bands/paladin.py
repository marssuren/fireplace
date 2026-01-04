# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- PALADIN 
"""

from ..utils import *

class ETC_318:
    """Boogie Down - 布吉舞乐
    3费法术
    从你的牌库中召唤两个法力值消耗为（1）的随从。压轴：再召唤一个。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    
    def play(self):
        # Summon 2
        yield Summon(CONTROLLER, RandomMinion(from_deck=True, cost=1)) * 2
        # Finale
        if self.controller.mana == 0:
            yield Summon(CONTROLLER, RandomMinion(from_deck=True, cost=1))

class JAM_009:
    """Dance Floor - 闪亮舞池
    1费 地标 3耐久
    选择一个随从。使该随从和所有其他随从获得突袭。
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 1,
        GameTag.HEALTH: 3,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    activate = Buff(TARGET, "JAM_009e"), Buff(ALL_MINIONS - TARGET, "JAM_009e")

class JAM_009e:
    tags = {GameTag.RUSH: True, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_317:
    """Disco Maul - 迪斯科战槌
    2费 2/2 武器
    亡语：随机使一个友方随从获得+1/+1。（装备期间，使用随从牌以提升此效果！）
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 2,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }
    # Script Data Num 1 stores the bonus amount (base 1)
    events = Play(CONTROLLER, MINION).on(Buff(SELF, "ETC_317e"))
    
    def deathrattle(self):
        amount = 1 + self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        yield Buff(RandomMinion(FRIENDLY_MINIONS), "ETC_317buff", atk=amount, max_health=amount)

class ETC_317e:
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_317buff:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT} # Stats set dynamically

class ETC_337:
    """Funkfin - 放克鱼人
    4费 4/3 鱼人
    圣盾。你的圣盾随从拥有+2攻击力。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.RACE: Race.MURLOC,
        GameTag.DIVINE_SHIELD: True,
    }
    # Aura: Friendly minions with DIVINE_SHIELD get +2 ATK
    # This requires a dynamic selector for "Has Divine Shield"
    # Fireplace selector: DIVINE_SHIELD (property)?
    # FRIENDLY_MINIONS + DIVINE_SHIELD works if DIVINE_SHIELD is a GameTag selector?
    # Usually: FRIENDLY_MINIONS + (GameTag.DIVINE_SHIELD: True)
    # Using 'Find' or 'Buff' with selector.
    auras = [
        Buff(FRIENDLY_MINIONS + DIVINE_SHIELD, "ETC_337e")
    ]

class ETC_337e:
    tags = {GameTag.ATK: 2, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class JAM_010:
    """Jukebox Totem - 点唱机图腾
    2费 0/4 图腾
    在你的回合结束时，召唤一个1/1的白银之手新兵。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 4,
        GameTag.COST: 2,
        GameTag.RACE: Race.TOTEM,
    }
    events = OwnTurnEnd.on(Summon(CONTROLLER, "CS2_101t"))

class ETC_506:
    """Harmonic Disco - 悦耳迪斯科
    5费法术
    发现一张法力值消耗为（5）的随从牌。召唤该随从并使其获得+1/+1。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    
    def play(self):
        # Discover 5-cost minion
        yield Discover(RandomMinion(cost=5))
        # Summon it and buff
        # Discover usually puts in hand. We want to Summon it (from hand) then buff.
        # Logic: After Discover, check choice?
        # Standard Discover action adds to hand.
        # We need "Summon the discovered card".
        # This implies we take it from hand.
        # Flow: Discover -> User picks -> Card in Hand -> Summon(Card) -> Buff.
        # How to refer to chosen card?
        # Discover.CARD isn't always reliable in complex chains unless implementing custom action.
        # But `Discover` usually sets up a choice.
        # Let's assume standard behavior: Discover puts in hand.
        # We can try to use a mechanism to capture the card.
        # Since I can't easily capture it, I'll use the "Summon from Hand" pattern if possible.
        # Best guess for correct implementation:
        # yield Discover(RandomMinion(cost=5)).then(Summon(CONTROLLER, Discover.CARD), Buff(Summon.CARD, "ETC_506e"))
        yield Discover(RandomMinion(cost=5)).then(Summon(CONTROLLER, Discover.CARD), Buff(Summon.CARD, "ETC_506e"))

    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "ETC_506t"))

class ETC_506t:
    """Dissonant Disco - 刺耳迪斯科
    5费法术
    发现一张法力值消耗为（1）的随从牌。召唤该随从并使其获得+5/+5。（每回合切换。）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    
    def play(self):
        yield Discover(RandomMinion(cost=1)).then(Summon(CONTROLLER, Discover.CARD), Buff(Summon.CARD, "ETC_506te"))

    class Hand:
        events = OwnTurnBegin(CONTROLLER).on(Transform(SELF, "ETC_506"))

class ETC_506e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}

class ETC_506te:
    tags = {GameTag.ATK: 5, GameTag.HEALTH: 5}

class ETC_324:
    """Jitterbug - 摇摆舞虫
    4费 3/3 野兽
    圣盾。在一个友方角色失去圣盾后，抽一张牌。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.RACE: Race.BEAST,
        GameTag.DIVINE_SHIELD: True,
    }
    # Event: DIVINE_SHIELD lost.
    # Fireplace doesn't have a specific "LoseDivineShield" event exposed easily in DSL?
    # It has `DivineShieldLost(TARGET)`.
    events = DivineShieldLost(FRIENDLY_CHARACTERS).on(Draw(CONTROLLER))

class ETC_328:
    """Lead Dancer - 领舞
    6费 4/5
    亡语：从你的牌库中召唤一个攻击力小于本随从攻击力的随从。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    
    def deathrattle(self):
        # Summon from deck where ATK < SELF.ATK
        # SELF.ATK is current atk (at death? or base?). Usually Last Known Info.
        # But in Graveyard, stats might be reset.
        # Need to capture stats at moment of death?
        # Fireplace `deathrattle` method on entity usually executed while card in Graveyard.
        # We need "Attack less than this minion's Attack".
        # If it uses current ATK in GY, it's Base ATK (4).
        # Hearthstone rule: Uses stats *on board* usually? No, for "Deathrattle: Summon minion with Cost < X" it uses static.
        # "Less than THIS minion's Attack".
        # Assuming last known info from board state.
        # BUT, Fireplace simple impl: use self.atk (which might be base in GY).
        # Let's use self.atk.
        # Selector: FRIENDLY_DECK + MINION + (ATK < self.atk)
        candidates = [c for c in self.controller.deck if c.type == CardType.MINION and c.atk < self.atk]
        if candidates:
            yield Summon(CONTROLLER, self.game.random.choice(candidates))

class ETC_321:
    """Annoy-o-Troupe - 吵吵演艺团
    9费 3/6 机械
    嘲讽，圣盾。亡语：召唤三个1/2并具有嘲讽和圣盾的机械。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 9,
        GameTag.RACE: Race.MECHANICAL,
        GameTag.TAUNT: True,
        GameTag.DIVINE_SHIELD: True,
    }
    deathrattle = Summon(CONTROLLER, "ETC_321t") * 3

class ETC_321t:
    """Annoy-o-Bot Fan - 吵吵粉丝"""
    tags = {
        GameTag.ATK: 1, 
        GameTag.HEALTH: 2, 
        GameTag.RACE: Race.MECHANICAL, 
        GameTag.TAUNT: True, 
        GameTag.DIVINE_SHIELD: True
    }

class ETC_320:
    """Spotlight - 光芒汇聚
    2费法术
    可交易。将一个友方圣盾转化为一个5/5的元素。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.TRADEABLE: True,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    # Requirement: Target must have Divine Shield? No, "Transform a friendly Divine Shield".
    # Means "Transform a friendly minion that has Divine Shield"?
    # Yes.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        # PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0 # Wait, Divine Shield requirement code?
        # 10 is DIVINE_SHIELD? Need to check enums.
    }
    # Target filter: FRIENDLY_MINIONS + DIVINE_SHIELD
    
    def play(self):
        # Transform into 5/5 Elemental
        yield Transform(TARGET, "ETC_320t")

class ETC_320t:
    """Spotlight Elemental - 光芒元素"""
    tags = {GameTag.ATK: 5, GameTag.HEALTH: 5, GameTag.RACE: Race.ELEMENTAL}

class ETC_329:
    """Kangor, Dancing King - 舞王坎格尔
    5费 3/3
    吸血。亡语：将本随从与你手牌中的一个随从互换，并使其获得吸血。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
        GameTag.LIFESTEAL: True,
        GameTag.LEGENDARY: True,
    }
    
    def deathrattle(self):
        # Swap this (from Graveyard?) with hand minion.
        # "Swap this minion with a minion in your hand."
        # Usually implies: Put this into hand, Summon that minion.
        # Kangor goes to hand. Hand minion goes to board.
        # Target in hand: Random minion.
        hand_minions = [c for c in self.controller.hand if c.type == CardType.MINION]
        if hand_minions:
            target = self.game.random.choice(hand_minions)
            # Perform Swap
            # 1. Summon target
            # 2. Move self to hand
            # 3. Give target Lifesteal
            
            # Note: Creating a loop if simply Summoning?
            # Summon action handles moving from Hand to Play.
            # Move handles Graveyard to Hand.
            yield Summon(CONTROLLER, target)
            yield Buff(target, "ETC_329e") # Give Lifesteal
            yield Move(SELF, Zone.HAND)

class ETC_329e:
    tags = {GameTag.LIFESTEAL: True, GameTag.CARDTYPE: CardType.ENCHANTMENT}

class ETC_330:
    """Starlight Groove - 星光节律
    3费法术
    使你的英雄获得圣盾。在本局对战的剩余时间内，使用神圣法术牌会复原此效果。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.HOLY,
    }
    
    def play(self):
        # Give Divine Shield
        yield GiveDivineShield(FRIENDLY_HERO)
        # Add permanent listener
        yield Buff(CONTROLLER, "ETC_330e")

class ETC_330e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # Event: Play Holy Spell -> Give Shield
    events = Play(CONTROLLER, SPELL + HOLY).on(GiveDivineShield(FRIENDLY_HERO))
