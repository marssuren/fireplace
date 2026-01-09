# -*- coding: utf-8 -*-
"""
TITANS 扩展包 - HUNTER
"""
from ..utils import *


# COMMON

class TTN_080:
    """神秘动物饲养员 - Fable Stablehand
    <b>突袭</b>。<b>战吼：</b>如果你控制一个攻击力大于或等于4的随从，便获得+2/+2。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.RUSH: True,
    }
    
    def play(self):
        # 检查是否有攻击力>=4的随从
        if Find(FRIENDLY_MINIONS + (ATK >= 4)):
            yield Buff(SELF, "TTN_080e")


class TTN_080e:
    """+2/+2 增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_081:
    """颤地觉醒 - Awakening Tremors
    获取三张4/1的冰虫，其法力值消耗为（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    play = Give(CONTROLLER, "TTN_081t") * 3


class TTN_081t:
    """冰虫 - Jormungar"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.BEAST,
    }


class TTN_504:
    """诱骗诡计 - Bait and Switch
    <b>奥秘：</b>当一个友方随从受到攻击时，使其获得+3/+3。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    secret = Attack(ALL_PLAYERS, FRIENDLY_MINIONS).on(
        Buff(Attack.DEFENDER, "TTN_504e")
    )


class TTN_504e:
    """+3/+3 增益"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class YOG_082:
    """星体射击 - Celestial Shot
    造成$3点伤害。你的下一个法术拥有<b>法术伤害+2</b>。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    play = [
        Hit(TARGET, 3),
        Buff(CONTROLLER, "YOG_082e")
    ]


class YOG_082e:
    """法术伤害+2"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    auras = [Buff(FRIENDLY_HERO, "YOG_082buff")]
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class YOG_082buff:
    """法术伤害+2"""
    tags = {
        GameTag.SPELLPOWER: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# RARE

class TTN_078:
    """神话观测者 - Observer of Myths
    在你召唤一个攻击力高于本随从的随从后，使所有友方随从获得+1攻击力。
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 4,
        GameTag.COST: 2,
    }
    
    events = Summon(CONTROLLER, MINION).on(
        Condition(
            Attr(Summon.CARD, GameTag.ATK) > Attr(SELF, GameTag.ATK),
            Buff(FRIENDLY_MINIONS, "TTN_078e")
        )
    )


class TTN_078e:
    """+1 攻击力"""
    tags = {
        GameTag.ATK: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_079:
    """虫外有虫 - Always a Bigger Jormungar
    使一个随从获得+2攻击力和"超过目标生命值的攻击伤害会命中敌方英雄。"
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    play = Buff(TARGET, "TTN_079e")


class TTN_079e:
    """+2 攻击力和溢出伤害
    
    超过目标生命值的攻击伤害会命中敌方英雄。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    def apply(self, target):
        super().apply(target)
        # 设置溢出伤害标记
        from ...enums import EXCESS_DAMAGE_TO_HERO
        target.tags[EXCESS_DAMAGE_TO_HERO] = True


class TTN_302:
    """泰坦锻造陷阱 - Titanforged Traps
    <b>发现</b>并施放一个<b>奥秘</b>。<b>锻造：</b>发现并施放两次。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        # 发现并施放一个奥秘
        yield Discover(RandomSecret()).then(Play(CONTROLLER, Discover.CARD))


class TTN_302t:
    """泰坦锻造陷阱 - Titanforged Traps (Forged)"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    def play(self):
        # 发现并施放两次
        yield Discover(RandomSecret()).then(Play(CONTROLLER, Discover.CARD))
        yield Discover(RandomSecret()).then(Play(CONTROLLER, Discover.CARD))


class YOG_505:
    """兽性癫狂 - Bestial Madness
    使你手牌，牌库和战场上的所有随从获得+1攻击力。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.NATURE,
    }
    
    play = [
        Buff(FRIENDLY_HAND + MINION, "YOG_505e"),
        Buff(FRIENDLY_DECK + MINION, "YOG_505e"),
        Buff(FRIENDLY_MINIONS, "YOG_505e")
    ]


class YOG_505e:
    """+1 攻击力"""
    tags = {
        GameTag.ATK: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class YOG_506:
    """扭曲的霜翼龙 - Twisted Frostwing
    <b>突袭</b>。<b>亡语：</b>召唤一只属性值等同于本随从攻击力的奇美拉。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.CARDRACE: Race.BEAST,
        GameTag.RUSH: True,
    }
    
    def deathrattle(self):
        # 召唤一个攻击力/生命值等于本随从攻击力的奇美拉
        atk_value = self.atk
        yield Summon(CONTROLLER, "YOG_506t").then(
            Buff(Summon.CARD, "YOG_506e", atk=atk_value, max_health=atk_value)
        )


class YOG_506t:
    """奇美拉 - Chimera"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDRACE: Race.BEAST,
    }


class YOG_506e:
    """属性增益"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


# EPIC

class TTN_087:
    """吸附寄生体 - Absorbent Parasite
    <b>磁力</b>。<b>突袭</b>。可以<b>磁力吸附</b>在机械和野兽上。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.MECHANICAL,
        GameTag.MAGNETIC: True,
        GameTag.RUSH: True,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置可以吸附的目标种族：机械和野兽
        from ...enums import MAGNETIC_TARGET_RACES
        self.tags[MAGNETIC_TARGET_RACES] = [Race.MECHANICAL, Race.BEAST]
    
    # 使用标准磁力函数
    magnetic = MAGNETIC("TTN_087e")


class TTN_087e:
    """吸附寄生体附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.MAGNETIC: True,
        GameTag.RUSH: True,
    }


class TTN_088:
    """牵星短弓 - Starstrung Bow
    在本局对战中，每触发一个友方<b>奥秘</b>，本牌的法力值消耗便减少（1）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 5,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }
    
    # 每触发奥秘减少1费
    events = Reveal(CONTROLLER, SECRET).on(Buff(SELF, "TTN_088e"))


class TTN_088e:
    """法力值消耗减少"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# LEGENDARY

class TTN_092:
    """复仇者阿格拉玛 - Aggramar, the Avenger
    <b>泰坦</b> <b>战吼：</b>装备一把3/3的泰沙拉克。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 7,
        GameTag.COST: 6,
        GameTag.LEGENDARY: True,
        GameTag.TITAN: True,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 泰坦技能次数
    }
    
    play = Summon(CONTROLLER, "TTN_092t")
    
    def titan_ability_1(self):
        """维持秩序 - Maintain Order
        给你的武器附加"在你的英雄攻击后，抽一张牌"效果
        """
        if self.controller.weapon:
            yield Buff(FRIENDLY_WEAPON, "TTN_092e1")
    
    def titan_ability_2(self):
        """指挥威仪 - Commanding Presence
        给你的武器附加"在你的英雄攻击后，召唤一个3/3并具有嘲讽的执行者"效果
        """
        if self.controller.weapon:
            yield Buff(FRIENDLY_WEAPON, "TTN_092e2")
    
    def titan_ability_3(self):
        """迅捷斩击 - Swift Slash
        给你的武器+2攻击力和"你的英雄在攻击时免疫"效果
        """
        if self.controller.weapon:
            yield Buff(FRIENDLY_WEAPON, "TTN_092e3")


class TTN_092t:
    """泰沙拉克 - Taeshalach"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class TTN_092e1:
    """维持秩序 - Maintain Order
    在你的英雄攻击后，抽一张牌。
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = Attack(FRIENDLY_HERO).after(Draw(CONTROLLER))


class TTN_092e2:
    """指挥威仪 - Commanding Presence
    在你的英雄攻击后，召唤一个3/3并具有嘲讽的执行者。
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "TTN_092e2t"))


class TTN_092e2t:
    """维库执行者 - Vry'kul Enforcer"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.TAUNT: True,
    }


class TTN_092e3:
    """迅捷斩击 - Swift Slash
    +2攻击力，你的英雄在攻击时免疫。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.IMMUNE_WHILE_ATTACKING: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_752:
    """巨人之父霍迪尔 - Hodir, Father of Giants
    <b>战吼：</b>将你使用的下三张随从牌的属性值变为8/8。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 8,
        GameTag.LEGENDARY: True,
    }
    
    play = Buff(CONTROLLER, "TTN_752e")


class TTN_752e:
    """巨人化效果"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 剩余次数
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    
    events = Play(CONTROLLER, MINION).on(
        Buff(Play.CARD, "TTN_752buff"),
        Buff(SELF, "TTN_752tick"),
        Condition(
            Equal(Tag(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1), 0),
            Destroy(SELF)
        )
    )


class TTN_752tick:
    """计数器减少"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TTN_752buff:
    """8/8 属性"""
    tags = {
        GameTag.ATK_SET: 8,
        GameTag.HEALTH_SET: 8,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }

