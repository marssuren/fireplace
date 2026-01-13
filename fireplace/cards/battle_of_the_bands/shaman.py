from ..utils import *
from ... import enums as fireplace_enums

class ETC_369:
    """Chill Vibes - 清冷音韵
    3费 法术 (Frost)
    恢复#8点生命值。压轴：召唤一个3/3并具有嘲讽的元素。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.FROST,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        yield Heal(TARGET, 8)
        if self.controller.mana == 0:
            yield Summon(CONTROLLER, "ETC_369t")

class ETC_369t:
    """Cold Elemental - 清冷元素"""
    race = Race.ELEMENTAL
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 3,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        
        GameTag.TAUNT: True
    }

class ETC_359:
    """Flowrider - 驭流骑士
    1费 2/1 纳迦
    战吼：如果你有过载的法力水晶，从你的牌库中发现一张法术牌。
    """
    race = Race.NAGA
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 1,
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        
    }

    def play(self):
        if self.controller.overloaded > 0 or self.controller.locked_mana > 0:
            yield Discover(RandomSpell(FRIENDLY_DECK))

class ETC_370:
    """Pack the House - 聚集观众
    7费 法术
    随机召唤法力值消耗为（6），（5），（4）和（3）的随从各一个。过载：（2）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
        GameTag.OVERLOAD: 2,
    }

    def play(self):
        for cost in [6, 5, 4, 3]:
            yield Summon(CONTROLLER, RandomMinion(cost=cost))

class ETC_356:
    """Altered Chord - 变音和弦
    5费 法术 (Nature)
    吸血。对一个随从造成6点伤害。如果你有过载的法力水晶，本牌的法力值消耗减少（3）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
        GameTag.LIFESTEAL: True,
    }

    def play(self):
        yield Hit(TARGET, 6)


    cost_mod = lambda self, i: -3 if (self.controller.overloaded > 0 or self.controller.locked_mana > 0) else 0

class ETC_357:
    """Brass Elemental - 铜管元素
    4费 3/3 元素
    突袭，圣盾，嘲讽，风怒
    """
    race = Race.ELEMENTAL
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 4,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        
        GameTag.RUSH: True,
        GameTag.DIVINE_SHIELD: True,
        GameTag.TAUNT: True,
        GameTag.WINDFURY: True,
    }

class JAM_011:
    """Horn of the Windlord - 风领主的管号
    6费 3/4 武器
    风怒。每当你的英雄攻击随从时，将被攻击随从的属性值变为3/3。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 6,
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.WINDFURY: True,
    }

    events = Attack(FRIENDLY_HERO, MINION).on(
        Buff(Attack.DEFENDER, "JAM_011e")
    )

class JAM_011e:
    tags = {
        GameTag.ATK: SET(3),
        GameTag.HEALTH: SET(3),
    }

class ETC_813:
    """爵士贝斯 - Jazz Bass
    3费 3/2 武器
    亡语：你的下一张法术牌法力值消耗减少（1）点。（装备期间，过载以提升此效果！）
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 3,
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        fireplace_enums.SPELL_COST_REDUCTION: 1,  # 存储减费数量（使用语义化标签）
    }
    
    # 监听过载事件，增加减费数量
    events = Overload(CONTROLLER).on(
        Buff(SELF, "ETC_813e")
    )
    
    def deathrattle(self):
        # 获取累积的减费数量（使用语义化标签）
        reduction = self.tags.get(fireplace_enums.SPELL_COST_REDUCTION, 1)
        
        # 给手牌中的法术施加减费
        spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        if spells:
            for spell in spells:
                yield Buff(spell, "ETC_813_Discount", discount=reduction)
        
        # 给控制器添加管理器，监听后续抽到的法术
        yield Buff(CONTROLLER, "ETC_813_Manager", discount=reduction)

class ETC_813e:
    """增加减费数量"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        fireplace_enums.SPELL_COST_REDUCTION: 1,
    }

class ETC_813_Discount:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, discount=1):
        super().__init__()
        self.discount = discount
    
    cost_mod = lambda self, i: -self.discount
    # 使用法术后销毁此 Buff
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))

class ETC_813_Manager:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, discount=1):
        super().__init__()
        self.discount = discount

    # 抽到法术时施加减费，使用法术后销毁管理器
    events = [
        Draw(CONTROLLER, SPELL).on(
            Buff(Draw.CARD, "ETC_813_Discount", discount=Attr(SELF, "discount"))
        ),
        Play(CONTROLLER, SPELL).on(Destroy(SELF))
    ]

class JAM_012:
    """Remixed Totemcarver - 混搭图腾师"""
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 3,
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
    }
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_012a"))

class JAM_012a: # Bluesy - Summon Totem
    tags = {GameTag.CARDTYPE: CardType.MINION, GameTag.COST: 3, GameTag.ATK: 3, GameTag.HEALTH: 2}
    def play(self):
        yield Summon(CONTROLLER, RandomBasicTotem())
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_012b"))

class JAM_012b: # Loud - +2 Health, Taunt
    tags = {GameTag.CARDTYPE: CardType.MINION, GameTag.COST: 3, GameTag.ATK: 3, GameTag.HEALTH: 2}
    def play(self):
        yield Buff(SELF, "JAM_012be")
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_012c"))

class JAM_012be:
    tags = {GameTag.HEALTH: 2, GameTag.TAUNT: True}

class JAM_012c: # Smooth - Deal 2
    tags = {GameTag.CARDTYPE: CardType.MINION, GameTag.COST: 3, GameTag.ATK: 3, GameTag.HEALTH: 2}
    def play(self):
        yield Hit(TARGET, 2)
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_012d"))

class JAM_012d: # Jazzy - +1 Attack, Rush
    tags = {GameTag.CARDTYPE: CardType.MINION, GameTag.COST: 3, GameTag.ATK: 3, GameTag.HEALTH: 2}
    def play(self):
        yield Buff(SELF, "JAM_012de")
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_012"))

class JAM_012de:
    tags = {GameTag.ATK: 1, GameTag.RUSH: True}

class ETC_367:
    """Melomania"""
    tags = {GameTag.CARDTYPE: CardType.SPELL, GameTag.COST: 0}
    def play(self):
        yield Buff(CONTROLLER, "ETC_367e")

class ETC_367e:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = [
        Play(CONTROLLER, MINION).on(Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))),
        OWN_TURN_END.on(Destroy(SELF))
    ]

class ETC_358:
    """Saxophone Soloist"""
    race = Race.MURLOC
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 1,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        
    }
    def play(self):
        if len(self.controller.field) == 1:
            yield Give(CONTROLLER, "ETC_358")

class ETC_371:
    """Inzah"""
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.COST: 5,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.RARITY: Rarity.LEGENDARY,
    }
    def play(self):
        overload_cards = [c for c in self.controller.hand if c.overload > 0]
        if overload_cards:
            yield Buff(overload_cards, "ETC_371_Discount")
        yield Buff(CONTROLLER, "ETC_371e")

class ETC_371e:
    """Inzah Manager"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听抽牌事件，如果抽到的是过载卡牌，施加减费
    events = Draw(CONTROLLER).on(
        # 检查抽到的卡牌是否有过载，如果有则施加减费
        # 使用 Find 和 & 操作符实现条件判断
        (Attr(Draw.CARD, "overload") > 0) & Buff(Draw.CARD, "ETC_371_Discount")
    )

class ETC_371_Discount:
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -1

class ETC_362:
    """JIVE, INSECT!"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
        GameTag.OVERLOAD: 2,
    }
    def play(self):
        yield Morph(TARGET, "EX1_298")
