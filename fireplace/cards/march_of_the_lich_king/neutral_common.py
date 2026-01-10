"""巫妖王的进军 - 迷你扩展包 (March of the Lich King)"""
from ..utils import *


class RLK_029:
    """裂肤石像鬼 (Shatterskin Gargoyle)
    嘲讽，亡语：随机对一个敌人造成4点伤害。
    机制: DEATHRATTLE, TAUNT
    """
    tags = {GameTag.TAUNT: True}
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 4)


class RLK_070:
    """被感染的农夫 (Infected Peasant)
    亡语：召唤一个2/2的亡灵农夫。
    机制: DEATHRATTLE
    """
    deathrattle = Summon(CONTROLLER, "RLK_070t")


class RLK_070t:
    """亡灵农夫 (Undead Peasant)"""
    tags = {GameTag.UNDEAD: True}


class RLK_104:
    """街头扫把 (Street Sweeper)
    战吼：对所有其他随从造成2点伤害。
    机制: BATTLECRY
    """
    play = Hit(ALL_MINIONS - SELF, 2)


class RLK_113:
    """脆皮僵尸 (Brittleskin Zombie)
    亡语：如果此时是你对手的回合，则对你的对手造成3点伤害。
    机制: DEATHRATTLE
    """
    deathrattle = (CurrentPlayer(OPPONENT), Hit(ENEMY_HERO, 3))


class RLK_117:
    """虚魂下士 (Incorporeal Corporal)
    在本随从攻击后消灭本随从。
    机制: TRIGGER_VISUAL
    """
    events = Attack(SELF).after(Destroy(SELF))


class RLK_119:
    """达卡莱入殓师 (Drakkari Embalmer)
    战吼：使一个友方亡灵获得复生。
    机制: BATTLECRY
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_WITH_RACE: Race.UNDEAD}
    play = Buff(TARGET, "RLK_119e")


class RLK_119e:
    """复生增益 (Reborn Buff)"""
    tags = {GameTag.REBORN: True}


class RLK_123:
    """白骨投手 (Bone Flinger)
    战吼：
如果在你的上回合之后有友方亡灵死亡，造成2点伤害。
    机制: BATTLECRY
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    powered_up = lambda self: self.controller.undead_died_last_turn
    play = (Find(SELF_POWERED_UP), Hit(TARGET, 2))


class RLK_218:
    """银月城奥术师 (Silvermoon Arcanist)
    法术伤害+2。战吼：在本回合中，你的法术不能以英雄为目标。
    机制: BATTLECRY, SPELLPOWER
    """
    tags = {GameTag.SPELLPOWER: 2}
    play = Buff(CONTROLLER, "RLK_218e")


class RLK_218e:
    """银月城奥术师增益 (Silvermoon Arcanist Buff)
    在本回合中，你的法术不能以英雄为目标。
    """
    update = Refresh(FRIENDLY + SPELL, {GameTag.CANT_TARGET_HEROES: True})
    events = OWN_TURN_END.on(Destroy(SELF))


class RLK_219:
    """日怒教士 (Sunfury Clergy)
    战吼：为所有友方角色恢复3点生命值。法力渴求（6）：改为恢复6点。
    机制: BATTLECRY, MANATHIRST
    """
    def play(self):
        if self.controller.max_mana >= 6:
            yield Heal(FRIENDLY_CHARACTERS, 6)
        else:
            yield Heal(FRIENDLY_CHARACTERS, 3)


class RLK_518:
    """银月城哨兵 (Silvermoon Sentinel)
    嘲讽。法力渴求（8）：获得+2/+2和圣盾。
    机制: MANATHIRST, TAUNT
    """
    tags = {GameTag.TAUNT: True}

    def play(self):
        # 法力渴求（8）：获得+2/+2和圣盾
        if self.controller.max_mana >= 8:
            yield Buff(SELF, "RLK_518e")


class RLK_518e:
    """银月城哨兵增益 (Silvermoon Sentinel Buff)"""
    tags = {GameTag.DIVINE_SHIELD: True}
    atk = lambda self, i: 2
    health = lambda self, i: 2


class RLK_824:
    """肢体商贩 (Arms Dealer)
    在你召唤一个亡灵后，使其获得+1攻击力。
    机制: TRIGGER_VISUAL
    """
    events = Summon(CONTROLLER, UNDEAD).after(Buff(Summon.CARD, "RLK_824e"))


class RLK_824e:
    """肢体商贩增益 (Arms Dealer Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


class RLK_833:
    """骨鸡蛋 (Foul Egg)
    亡语：召唤一只3/3的亡灵小鸡。
    机制: DEATHRATTLE
    """
    deathrattle = Summon(CONTROLLER, "RLK_833t")


class RLK_833t:
    """亡灵小鸡 (Undead Chicken)"""
    tags = {GameTag.UNDEAD: True}


class RLK_834:
    """蛛魔元老 (Nerubian Vizier)
    战吼：发现一张法术牌。如果在你的上回合之后有友方亡灵死亡，其法力值消耗减少（2）点。
    机制: BATTLECRY, DISCOVER
    """
    def play(self):
        if self.controller.undead_died_last_turn:
            yield GenericChoice(CONTROLLER, DISCOVER(SPELL), lambda card: [Buff(card, "RLK_834e"), Give(CONTROLLER, card)])
        else:
            yield GenericChoice(CONTROLLER, DISCOVER(SPELL))


class RLK_834e:
    """蛛魔元老增益 (Nerubian Vizier Buff)"""
    cost = -2


class RLK_867:
    """维库通灵师 (Vrykul Necrolyte)
    战吼：使一个友方随从获得"亡语：召唤一个2/2并具有突袭的僵尸。"
    机制: BATTLECRY, DEATH_KNIGHT
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "RLK_867e")


class RLK_867e:
    """维库通灵师增益 (Vrykul Necrolyte Buff)"""
    deathrattle = Summon(CONTROLLER, "RLK_867t")


class RLK_867t:
    """僵尸 (Zombie)"""
    tags = {GameTag.RUSH: True, GameTag.UNDEAD: True}


class RLK_900:
    """天灾暴怒者 (Scourge Rager)
    复生，战吼：死亡。
    机制: BATTLECRY, REBORN
    """
    tags = {GameTag.REBORN: True}
    play = Destroy(SELF)


class RLK_914:
    """幽影恶鬼 (Umbral Geist)
    亡语：
随机将一张暗影法术牌置入你的手牌。
    机制: DEATHRATTLE
    """
    deathrattle = Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.SHADOW))


class RLK_915:
    """琥珀雏龙 (Amber Whelp)
    战吼：如果你的手牌中有龙牌，则造成3点伤害。
    机制: BATTLECRY
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    powered_up = Find(FRIENDLY_HAND + DRAGON)
    play = (Find(SELF_POWERED_UP), Hit(TARGET, 3))


class RLK_926:
    """浴血骑士 (Bloodied Knight)
    在你的回合结束时，对你的英雄造成2点伤害。
    机制: TRIGGER_VISUAL
    """
    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 2))


class RLK_955:
    """银月城军备官 (Silvermoon Armorer)
    突袭。法力渴求（7）：获得+2/+2。
    机制: MANATHIRST, RUSH
    """
    tags = {GameTag.RUSH: True}

    def play(self):
        # 法力渴求（7）：获得+2/+2
        if self.controller.max_mana >= 7:
            yield Buff(SELF, "RLK_955e")


class RLK_955e:
    """银月城军备官增益 (Silvermoon Armorer Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }
    health = 2


