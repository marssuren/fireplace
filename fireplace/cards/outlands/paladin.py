from ..utils import *


##
# Minions


class BT_009:
    """Imprisoned Sungill / 被禁锢的阳鳃鱼人
    休眠2回合。唤醒时，召唤两个1/1的 鱼人。"""

    # <b>Dormant</b> for 2 turns. When this awakens, summon two 1/1 Murlocs.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Summon(CONTROLLER, "BT_009t") * 2


class BT_019:
    """Murgur Murgurgle / 莫戈尔·莫戈尔格
    圣盾 亡语：将“终极莫戈尔格”洗入你的牌库。"""

    # [x]<b>Divine Shield</b> <b>Deathrattle:</b> Shuffle 'Murgurgle Prime'
    # into your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_019t")


class BT_019t:
    """Murgurgle Prime"""

    # <b>Divine Shield</b> <b>Battlecry:</b> Summon 4 random Murlocs. Give them
    # <b>Divine Shield</b>.
    play = Summon(CONTROLLER, RandomMurloc()).then(GiveDivineShield(Summon.CARD)) * 4


class BT_020:
    """Aldor Attendant / 奥尔多侍从
    战吼：在本局对战中，你的圣契的法力值消耗减少（1）点。"""

    # <b>Battlecry:</b> Reduce the Cost_of your Librams by_(1) this game.
    play = Buff(CONTROLLER, "BT_020e")


class BT_020e:
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + LIBRAM, {GameTag.COST: -1})


class BT_026:
    """Aldor Truthseeker / 奥尔多真理追寻者
    嘲讽，战吼： 在本局对战中，你的圣契的法力值消耗减少（2）点。"""

    # <b>Taunt</b>. <b>Battlecry:</b> Reduce the Cost of your Librams by (2)
    # this game.
    play = Buff(CONTROLLER, "BT_026e")


class BT_026e:
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + LIBRAM, {GameTag.COST: -2})


class BT_334:
    """Lady Liadrin / 女伯爵莉亚德琳
    战吼：将你在本局对战中施放在友方角色上的所有法术的复制置入你的手牌。"""

    # [x]<b>Battlecry:</b> Add a copy of each spell you cast on friendly
    # characters this game to your hand.
    play = Give(
        CONTROLLER, Copy(SHUFFLE(CARDS_PLAYED_THIS_GAME + CAST_ON_FRIENDLY_CHARACTERS))
    )


##
# Spells


class BT_011:
    """Libram of Justice / 正义圣契
    装备一把1/4的武器。将所有敌方随从的生命值变为1。"""

    # Equip a 1/4 weapon. Change the Health of all enemy minions to 1.
    play = Summon(CONTROLLER, "BT_011t"), Buff(ENEMY_MINIONS, "BT_011e")


class BT_011e:
    max_health = SET(1)


class BT_024:
    """Libram of Hope / 希望圣契
    恢复8点生命值。召唤一个8/8并具有嘲讽和圣盾的 守卫。"""

    # Restore 8 Health. Summon an 8/8 Guardian with <b>Taunt</b> and_<b>Divine
    # Shield</b>.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 8), Summon(CONTROLLER, "BT_024t")


class BT_025:
    """Libram of Wisdom / 智慧圣契
    使一个随从获得+1/+1，以及“亡语：将一张‘智慧圣契’法术牌置入你的手牌。”"""

    # [x]Give a minion +1/+1 and "<b>Deathrattle:</b> Add a 'Libram of Wisdom'
    # spell to your hand."
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "BT_025e")


class BT_025e:
    tags = {GameTag.ATK: +1, GameTag.HEALTH: +1, GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, "BT_025")


class BT_292:
    """Hand of A'dal / 阿达尔之手
    使一个随从获得+2/+1。 抽一张牌。"""

    # Give a minion +2/+1. Draw a card.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "BT_292e"), Draw(CONTROLLER)


BT_292e = buff(+2, +1)


##
# Weapons


class BT_018:
    """Underlight Angling Rod / 幽光鱼竿
    在你的英雄攻击后，随机将一张鱼人牌置入你的手牌。"""

    # After your Hero attacks, add a random Murloc to your hand.
    events = Attack(FRIENDLY_HERO).after(Give(CONTROLLER, RandomMurloc()))
