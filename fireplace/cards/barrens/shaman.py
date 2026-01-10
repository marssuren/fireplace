"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_040:
    """South Coast Chieftain - 南海岸酋长
    Battlecry: If you control another Murloc, deal 2 damage.
    战吼：如果你控制另一个鱼人，造成2点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    powered_up = Find(FRIENDLY_MINIONS + MURLOC - SELF)
    play = powered_up & Hit(TARGET, 2)


class BAR_041:
    """Nofin Can Stop Us - 鱼勇可贾
    Give your minions +1/+1. Give your Murlocs an extra +1/+1.
    使你的随从获得+1/+1。使你的鱼人额外获得+1/+1。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(FRIENDLY_MINIONS, "BAR_041e"),
        Buff(FRIENDLY_MINIONS + MURLOC, "BAR_041e2"),
    )


class BAR_041e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_041e2:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_043:
    """Tinyfin's Caravan - 鱼人宝宝车队
    At the start of your turn, draw a Murloc.
    在你的回合开始时，抽一张鱼人牌。
    """
    events = OWN_TURN_BEGIN.on(
        ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC))
    )


class BAR_044:
    """Chain Lightning (Rank 1) - 闪电链（等级1）
    Deal $2 damage to a minion and a random adjacent one. (Upgrades when you have 5 Mana.)
    对一个随从和一个随机相邻的随从造成$2点伤害。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_044t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), Hit(TARGET_ADJACENT, 2)


class BAR_044t:
    """Chain Lightning (Rank 2) - 闪电链（等级2）
    Deal $3 damage to a minion and a random adjacent one. (Upgrades when you have 10 Mana.)
    对一个随从和一个随机相邻的随从造成$3点伤害。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_044t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Hit(TARGET_ADJACENT, 3)


class BAR_044t2:
    """Chain Lightning (Rank 3) - 闪电链（等级3）
    Deal $4 damage to a minion and a random adjacent one.
    对一个随从和一个随机相邻的随从造成$4点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), Hit(TARGET_ADJACENT, 4)


class BAR_045:
    """Arid Stormer - 旱地风暴
    Battlecry: If you played an Elemental last turn, gain Rush and Windfury.
    战吼：如果你在上个回合打出过元素，获得突袭和风怒。
    """
    def play(self):
        if getattr(self.controller, 'elemental_played_last_turn', 0) > 0:
            yield SetTags(SELF, {GameTag.RUSH: True})
            yield SetTags(SELF, {GameTag.WINDFURY: True})


class BAR_048:
    """Bru'kan - 布鲁坎
    Nature Spell Damage +3
    自然法术伤害+3。
    """
    update = Refresh(CONTROLLER, {enums.NATURE_SPELL_DAMAGE: +3})


class BAR_750:
    """Earth Revenant - 大地亡魂
    Taunt. Battlecry: Deal 1 damage to all enemy minions.
    嘲讽。战吼：对所有敌方随从造成1点伤害。
    """
    play = Hit(ENEMY_MINIONS, 1)


class BAR_751:
    """Spawnpool Forager - 孵化池觅食者
    Deathrattle: Summon a 1/1 Tinyfin.
    亡语：召唤一个1/1的鱼人宝宝。
    """
    deathrattle = Summon(CONTROLLER, "CS2_173")


class BAR_848:
    """Lilypad Lurker - 荷塘潜伏者
    Battlecry: If you played an Elemental last turn, transform an enemy minion into a 0/1 Frog with Taunt.
    战吼:如果你在上个回合打出过元素,将一个敌方随从变形成为一个0/1并具有嘲讽的青蛙。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    play = powered_up & Morph(TARGET, "hexfrog")


class BAR_860:
    """Firemancer Flurgl - 火焰术士弗洛格尔
    After you play a Murloc, deal 1 damage to all enemies.
    在你打出一个鱼人后，对所有敌人造成1点伤害。
    """
    events = Play(CONTROLLER, MURLOC).after(
        Hit(ENEMY_CHARACTERS, 1)
    )


class WC_005:
    """Primal Dungeoneer - 原初地下城历险家
    Battlecry: Draw a spell. If it's a Nature spell, also draw an Elemental.
    战吼:抽一张法术牌。如果是自然法术,同时抽一张元素牌。
    """
    play = Draw(CONTROLLER).then(
        Find(Draw.CARD + SPELL + NATURE) & ForceDraw(RANDOM(FRIENDLY_DECK + ELEMENTAL))
    )


class WC_020:
    """Perpetual Flame - 永恒之火
    Deal $3 damage to a random enemy minion. If it dies, recast this. Overload: (1)
    对一个随机敌方随从造成$3点伤害。如果其死亡，重新施放该法术。过载：（1）
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(RANDOM_ENEMY_MINION, 3).then(
        Dead(Hit.TARGET) & CastSpell("WC_020")
    )


class WC_042:
    """Wailing Vapor - 哀嚎蒸汽
    After you play an Elemental, gain +1 Attack.
    在你打出一个元素后，获得+1攻击力。
    """
    events = Play(CONTROLLER, ELEMENTAL).after(
        Buff(SELF, "WC_042e")
    )


class WC_042e:
    tags = {
        GameTag.ATK: 1,
    }


