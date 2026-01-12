"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_334:
    """Overlord Saurfang - 萨鲁法尔大王
    Battlecry: Resurrect 2 friendly Frenzy minions. Deal 1 damage to all other minions.
    战吼：复活2个友方暴怒随从。对所有其他随从造成1点伤害。
    """
    play = (
        Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + DEAD + MINION + Attr(GameTag.FRENZY, True)))) * 2,
        Hit(ALL_MINIONS - SELF, 1),
    )


class BAR_840:
    """Whirling Combatant - 旋风争斗者
    Battlecry and Frenzy: Deal 1 damage to all other minions.
    战吼和暴怒：对所有其他随从造成1点伤害。
    """
    play = Hit(ALL_MINIONS - SELF, 1)
    frenzy = Hit(ALL_MINIONS - SELF, 1)


class BAR_841:
    """Bulk Up - 重装上阵
    Give a random Taunt minion in your hand +1/+1 and copy it.
    随机使你手牌中的一张嘲讽随从牌获得+1/+1，并复制它。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(RANDOM(FRIENDLY_HAND + MINION + TAUNT), "BAR_841e"),
        Give(CONTROLLER, Copy(RANDOM(FRIENDLY_HAND + MINION + TAUNT))),
    )


class BAR_841e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_842:
    """Conditioning (Rank 1) - 体格训练（等级1）
    Give minions in your hand +1/+1. (Upgrades when you have 5 Mana.)
    使你手牌中的随从牌获得+1/+1。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_842t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_HAND + MINION, "BAR_842e")


class BAR_842e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_842t:
    """Conditioning (Rank 2) - 体格训练（等级2）
    Give minions in your hand +2/+2. (Upgrades when you have 10 Mana.)
    使你手牌中的随从牌获得+2/+2。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_842t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_HAND + MINION, "BAR_842t_e")


class BAR_842t_e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class BAR_842t2:
    """Conditioning (Rank 3) - 体格训练（等级3）
    Give minions in your hand +3/+3.
    使你手牌中的随从牌获得+3/+3。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_HAND + MINION, "BAR_842t2_e")


class BAR_842t2_e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class BAR_843:
    """Warsong Envoy - 战歌大使
    Frenzy: Gain +1 Attack for each damaged character.
    暴怒：每有一个受伤的角色，便获得+1攻击力。
    """
    frenzy = Buff(SELF, "BAR_843e", atk=Count(ALL_CHARACTERS + DAMAGED))


class BAR_843e:
    """Warsong Envoy buff"""
    pass


class BAR_844:
    """Outrider's Axe - 前锋战斧
    After your hero attacks and kills a minion, draw a card.
    在你的英雄攻击并消灭一个随从后，抽一张牌。
    """
    events = Attack(FRIENDLY_HERO, MINION).after(
        Dead(Attack.DEFENDER) & Draw(CONTROLLER)
    )


class BAR_845:
    """Rancor - 仇怨累积
    Deal $2 damage to all minions. Gain 2 Armor for each destroyed.
    对所有随从造成$2点伤害。每有一个随从被摧毁,便获得2点护甲值。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    def play(self):
        # 记录造成伤害前场上的随从
        minions_before = list(self.game.board)
        yield Hit(ALL_MINIONS, 2)
        # 计算死亡的随从数量
        minions_after = list(self.game.board)
        killed_count = len(minions_before) - len(minions_after)
        # 获得相应的护甲
        if killed_count > 0:
            yield GainArmor(FRIENDLY_HERO, 2 * killed_count)


class BAR_846:
    """Mor'shan Elite - 莫尔杉精锐
    Taunt. Battlecry: If your hero attacked this turn, summon a copy of this.
    嘲讽。战吼:如果你的英雄在本回合中攻击过,召唤一个该随从的复制。
    """
    powered_up = Attr(FRIENDLY_HERO, GameTag.NUM_ATTACKS_THIS_TURN) > 0
    play = powered_up & Summon(CONTROLLER, Copy(SELF))


class BAR_847:
    """Rokara - 洛卡拉
    Rush. After a friendly minion attacks and survives, give it +1/+1.
    突袭。在一个友方随从攻击并存活后，使其获得+1/+1。
    """
    events = Attack(FRIENDLY + MINION).after(
        Alive(Attack.ATTACKER) & Buff(Attack.ATTACKER, "BAR_847e")
    )


class BAR_847e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_896:
    """Stonemaul Anchorman - 石槌掌锚手
    Rush. Frenzy: Draw a card.
    突袭。暴怒：抽一张牌。
    """
    frenzy = Draw(CONTROLLER)


class WC_024:
    """Man-at-Arms - 武装战士
    Battlecry: If you have a weapon equipped, gain +1/+1.
    战吼：如果你装备了武器，获得+1/+1。
    """
    powered_up = Find(FRIENDLY_WEAPON)
    play = powered_up & Buff(SELF, "WC_024e")


class WC_024e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class WC_025:
    """Whetstone Hatchet - 砥石战斧
    After your hero attacks, give a minion in your hand +1 Attack.
    在你的英雄攻击后，随机使你手牌中的一张随从牌获得+1攻击力。
    """
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "WC_025e")
    )


class WC_025e:
    tags = {
        GameTag.ATK: 1,
    }


class WC_026:
    """Kresh, Lord of Turtling - 克雷什，群龟之王
    Frenzy: Gain 8 Armor. Deathrattle: Equip a 2/5 Turtle Spike.
    暴怒：获得8点护甲值。亡语：装备一把2/5的龟刺。
    """
    frenzy = GainArmor(FRIENDLY_HERO, 8)
    deathrattle = Equip("WC_026t")


