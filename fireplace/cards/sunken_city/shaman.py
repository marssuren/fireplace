from ..utils import *


class TSC_631:
    """Schooling - 鱼群聚集
    1费法术 将三张1/1的食人鱼群置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Give(CONTROLLER, "TSC_631t") * 3


class TSC_631t:
    """Piranha Swarmer - 食人鱼群
    1费 1/1 野兽
    在你的战场上每有另一个食人鱼群，便获得+1攻击力。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.BEAST,
        GameTag.RUSH: True,
    }
    auras = [
        Buff(SELF, "TSC_631te")
    ]


class TSC_631te:
    def atk(self, value):
        others = len([m for m in self.source.controller.field if m.card_id == "TSC_631t" and m is not self.source])
        return value + others


class TSC_637:
    """Scalding Geyser - 间歇热泉
    1费法术 造成$2点伤害。探底。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), Dredge(CONTROLLER)


class TSC_772:
    """Azsharan Scroll - 艾萨拉的卷轴
    1费法术 发现一张火焰、冰霜或自然法术牌。将一张"沉没的卷轴"置于你的牌库底部。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Discover(CONTROLLER, RandomSpell(spell_school=[SpellSchool.FIRE, SpellSchool.FROST, SpellSchool.NATURE])).then(
        Give(CONTROLLER, Discover.CARD),
        ShuffleIntoDeck(CONTROLLER, "TSC_772t", position='bottom')
    )


class TSC_772t:
    """Sunken Scroll - 沉没的卷轴
    1费法术 对敌方英雄造成$3点伤害，随机将两张火焰、冰霜或自然法术牌置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    play = Hit(ENEMY_HERO, 3), Give(CONTROLLER, RandomSpell(spell_school=[SpellSchool.FIRE, SpellSchool.FROST, SpellSchool.NATURE])) * 2


class TSC_922:
    """Anchored Totem - 驻锚图腾
    2费 0/3 图腾
    在你召唤一个法力值消耗为(1)的随从后，使其获得+2/+1。
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.TOTEM,
    }
    events = Summon(CONTROLLER, MINION + (COST == 1)).after(Buff(Summon.CARD, "TSC_922e"))


class TSC_922e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }


class TID_004:
    """Clownfish - 小丑鱼
    3费 3/2 鱼人
    战吼：你的下两张鱼人牌法力值消耗减少(2)点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.MURLOC,
    }
    # 使用带计数器的Buff
    play = Buff(CONTROLLER, "TID_004e")


class TID_004e:
    """Clownfish Cost Reduction"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 2, # 使用这个Tag作为计数器
    }
    # 光环：手牌中鱼人减2费
    update = Refresh(FRIENDLY_HAND + MURLOC, {GameTag.COST: -2})
    
    # 监听打出事件
    events = Play(CONTROLLER, MURLOC).on(
        (
            # 减少计数: SetTag(SELF, {TAG: Attr(SELF, TAG) - 1})
            SetTag(SELF, {GameTag.TAG_SCRIPT_DATA_NUM_1: Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1) - 1}),
            # 如果计数归零，销毁自身
            (Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1) <= 0) & Destroy(SELF)
        )
    )


class TSC_633:
    """Piranha Poacher - 食人鱼偷猎者
    3费 2/5
    在你的回合结束时，将一张1/1的食人鱼群置入你的手牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
    }
    events = OWN_TURN_END.on(Give(CONTROLLER, "TSC_631t"))


class TSC_635:
    """Radiance of Azshara - 艾萨拉之辉
    3费 3/4 元素
    法术伤害+2。你的自然法术法力值消耗减少(1)点。在你施放一个自然法术后，获得3点护甲值。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.SPELLPOWER: 2,
    }
    # Aura: Nature spells cost -1
    # Events: Cast Natural spell -> Gain Armor
    update = Refresh(FRIENDLY_HAND + SPELL + NATURE, {GameTag.COST: -1})
    events = Play(CONTROLLER, SPELL + NATURE).after(GainArmor(FRIENDLY_HERO, 3))


class TID_003:
    """Tidelost Burrower - 迷潮挖掘者
    4费 4/4 鱼人
    战吼：探底。如果选中的牌是鱼人牌，召唤一个它的2/2复制。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.CARDRACE: Race.MURLOC,
    }
    
    def play(self):
        yield Dredge(CONTROLLER)
        if self.controller.deck:
            top_card = self.controller.deck[0]
            if top_card.type == CardType.MINION and Race.MURLOC in top_card.races:
                yield Summon(CONTROLLER, ExactCopy(top_card), {GameTag.ATK: 2, GameTag.HEALTH: 2})


class TSC_923:
    """Bioluminescence - 生物荧光
    3费法术 使你的随从获得法术伤害+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Buff(FRIENDLY_MINIONS, "TSC_923e")


class TSC_923e:
    tags = {
        GameTag.SPELLPOWER: 1,
    }


class TID_005:
    """Command of Neptulon - 耐普图隆的指令
    5费法术 召唤两个5/4并具有突袭的元素。过载：(1)。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.OVERLOAD: 1,
    }
    play = Summon(CONTROLLER, "TID_005t") * 2


class TID_005t:
    """Elemental (5/4 Rush)"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.RUSH: True,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }


class TSC_630:
    """Wrathspine Enchanter - 怒脊附魔师
    7费 5/4
    战吼：从你的手牌中施放一张火焰、冰霜和自然法术牌的复制（目标随机而定）。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 7,
    }
    
    def play(self):
        # Fire
        fire_spells = [c for c in self.controller.hand if c.type == CardType.SPELL and SpellSchool.FIRE in c.spell_school]
        frost_spells = [c for c in self.controller.hand if c.type == CardType.SPELL and SpellSchool.FROST in c.spell_school]
        nature_spells = [c for c in self.controller.hand if c.type == CardType.SPELL and SpellSchool.NATURE in c.spell_school]
        
        if fire_spells:
             target = self.game.random.choice(fire_spells)
             yield CastSpell(Copy(target))
             
        if frost_spells:
             target = self.game.random.choice(frost_spells)
             yield CastSpell(Copy(target))
             
        if nature_spells:
             target = self.game.random.choice(nature_spells)
             yield CastSpell(Copy(target))


class GluggAbsorb(Action):
    def do(self, source, target):
        atk = target.original_atk
        health = target.original_health
        source.buff(atk=atk, max_health=health)


class TSC_639:
    """Glugg the Gulper - 暴食巨鳗格拉格
    7费 3/5 野兽
    巨型+3。嘲讽。在一个友方随从死亡后，获得其原始属性值。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 7,
        GameTag.CARDRACE: Race.BEAST,
        GameTag.COLOSSAL: 3,
        GameTag.TAUNT: True,
    }
    colossal_appendages = ["TSC_639t", "TSC_639t", "TSC_639t"]
    
    events = Death(FRIENDLY_MINIONS - SELF).after(GluggAbsorb(SELF, Death.ENTITY))


class TSC_639t:
    """Glugg's Tail"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.BEAST,
    }


class TSC_648:
    """Coral Keeper - 珊瑚培育师
    5费 3/4
    战吼：在本局对战中，你每施放过一个派系的法术，召唤一个3/3的元素。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.NAGA, 
    }
    
    def play(self):
        # 统计已施放的法术派系
        schools = set()
        for c in self.controller.cards_played_this_game:
            if c.type == CardType.SPELL:
                if hasattr(c, 'spell_school'):
                     # spell_school might be a list or single enum?
                     # In Fireplace usually list.
                     # But some implementations might use single. 
                     # Check if iterable.
                     try:
                         for s in c.spell_school:
                             if s != SpellSchool.NONE:
                                 schools.add(s)
                     except:
                         # Single value
                         if c.spell_school != SpellSchool.NONE:
                             schools.add(c.spell_school)
        
        count = len(schools)
        if count > 0:
            yield Summon(CONTROLLER, "TSC_648t") * count


class TSC_648t:
    """Coral Elemental"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }
