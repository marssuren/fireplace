# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 中立普通
"""

from ..utils import *


class AV_101:
    """洛克霍拉的使者 / Herald of Lokholar
    战吼：抽一张冰霜法术牌。"""
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + FROST))


class AV_121:
    """侏儒列兵 / Gnome Private
    荣誉击杀：获得+2攻击力。"""
    honorable_kill = Buff(SELF, "AV_121e")


class AV_121e:
    """侏儒列兵增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }


class AV_122:
    """下士 / Corporal
    荣誉击杀：使你的其他随从获得圣盾。"""
    honorable_kill = SetTag(FRIENDLY_MINIONS - SELF, {GameTag.DIVINE_SHIELD: True})


class AV_123:
    """潜匿斥候 / Sneaky Scout
    潜行 荣誉击杀：你的下一个英雄技能法力值消耗为（0）点。"""
    honorable_kill = Buff(FRIENDLY_HERO, "AV_123e")


class AV_123e:
    """潜匿斥候增益"""
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))


class AV_124:
    """恐狼指挥官 / Direwolf Commander
    荣誉击杀：召唤一个2/2并具有潜行的狼。"""
    honorable_kill = Summon(CONTROLLER, "AV_124t")


class AV_124t:
    """狼 / Wolf
    2/2 潜行随从"""
    # 在 CardDefs.xml 中定义


class AV_125:
    """塔楼中士 / Tower Sergeant
    战吼：如果你控制至少2个其他随从，获得+2/+2。"""
    play = (Find(FRIENDLY_MINIONS - SELF, count=2), Buff(SELF, "AV_125e"))


class AV_125e:
    """塔楼中士增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class AV_126:
    """碉堡中士 / Bunker Sergeant
    战吼：如果你的对手控制2个或更多随从，对所有敌方随从造成1点伤害。"""
    play = (Find(ENEMY_MINIONS, count=2), Hit(ENEMY_MINIONS, 1))


class AV_127:
    """冰雪亡魂 / Ice Revenant
    每当你施放一个冰霜法术，获得+2/+2。"""
    events = Play(CONTROLLER, SPELL + FROST).after(Buff(SELF, "AV_127e"))


class AV_127e:
    """冰雪亡魂增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class AV_129:
    """血卫士 / Blood Guard
    每当该随从受到伤害，使你的所有随从获得+1攻击力。"""
    events = Damage(SELF).on(Buff(FRIENDLY_MINIONS, "AV_129e"))


class AV_129e:
    """血卫士增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


class AV_130:
    """军团士兵 / Legionnaire
    亡语：使你手牌中的所有随从获得+2/+2。"""
    deathrattle = Buff(FRIENDLY_HAND + MINION, "AV_130e")


class AV_130e:
    """军团士兵增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class AV_131:
    """骑士队长 / Knight-Captain
    战吼：造成3点伤害。荣誉击杀：获得+3/+3。"""
    play = Hit(TARGET, 3)
    honorable_kill = Buff(SELF, "AV_131e")


class AV_131e:
    """骑士队长增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class AV_132:
    """巨魔百夫长 / Troll Centurion
    突袭 荣誉击杀：对敌方英雄造成8点伤害。"""
    honorable_kill = Hit(ENEMY_HERO, 8)


class AV_133:
    """冰蹄护卫 / Icehoof Protector
    嘲讽 冻结任何受到该随从伤害的角色。"""
    events = Damage(ALL_CHARACTERS, SELF).on(Freeze(Damage.TARGET))


class AV_215:
    """狂乱角鹰兽 / Frantic Hippogryph
    突袭 荣誉击杀：获得风怒。"""
    honorable_kill = SetTag(SELF, {GameTag.WINDFURY: True})


class AV_219:
    """群羊指挥官 / Ram Commander
    战吼：将两张1/1并具有突袭的山羊牌置入你的手牌。"""
    play = Give(CONTROLLER, "AV_219t") * 2


class AV_219t:
    """山羊 / Ram
    1/1 突袭随从"""
    # 在 CardDefs.xml 中定义


class AV_238:
    """伏兵 / Gankster
    潜行 在你的对手打出一张随从牌后，攻击该随从。"""
    events = Play(OPPONENT, MINION).after(Attack(SELF, Play.CARD))


class AV_256:
    """反射工程师 / Reflecto Engineer
    战吼：交换双方玩家手牌中所有随从的攻击力和生命值。"""
    play = (Buff(FRIENDLY_HAND + MINION, "AV_256e"), Buff(ENEMY_HAND + MINION, "AV_256e"))


class AV_256e:
    """反射工程师增益"""
    tags = {
        GameTag.ATK: lambda self, i: self._xatk,
        GameTag.HEALTH: lambda self, i: self._xhealth,
    }

    def apply(self, target):
        self._xatk = target.health
        self._xhealth = target.atk
        super().apply(target)


class AV_309:
    """被背小鬼 / Piggyback Imp
    亡语：召唤一个4/1的小鬼。"""
    deathrattle = Summon(CONTROLLER, "AV_309t")


class AV_309t:
    """小鬼 / Imp
    4/1 随从"""
    # 在 CardDefs.xml 中定义


class AV_401:
    """雷矛军需官 / Stormpike Quartermaster
    在你施放一个法术后，随机使你手牌中的一个随从获得+1/+1。"""
    events = Play(CONTROLLER, SPELL).after(
        Find(FRIENDLY_HAND + MINION) & Buff(RANDOM(FRIENDLY_HAND + MINION), "AV_401e")
    )


class AV_401e:
    """雷矛军需官增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class AV_704:
    """巨型猫头鹰 / Humongous Owl
    亡语：对一个随机敌人造成8点伤害。"""
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 8)


class ONY_001:
    """奥妮克希亚守卫 / Onyxian Warder
    战吼：如果你的手牌中有龙，召唤两个2/1并具有突袭的雏龙。"""
    play = (Find(FRIENDLY_HAND + DRAGON), Summon(CONTROLLER, "ONY_001t")) * 2


class ONY_001t:
    """雏龙 / Whelp
    2/1 突袭随从"""
    # 在 CardDefs.xml 中定义
