from ..utils import *


##
# Minions


class LOOT_216:
    """Lynessa Sunsorrow / 莱妮莎·炎伤
    战吼：将你在本局对战中对友方随从施放过的所有法术施放在本随从身上。"""

    # [x]<b>Battlecry:</b> Cast each spell you cast on your minions this game on this one.
    play = CastSpell(CARDS_PLAYED_THIS_GAME + CAST_ON_FRIENDLY_MINIONS, SELF)


class LOOT_313:
    """Crystal Lion / 水晶雄狮
    圣盾 你每控制一个白银之手新兵，本牌的法力值消耗便减少（1）点。"""

    # [x]<b>Divine Shield</b> Costs (1) less for each Silver Hand Recruit you control.
    cost_mod = -Count(FRIENDLY_MINIONS + ID("CS2_101t"))


class LOOT_363:
    """Drygulch Jailor / 旱谷狱卒
    亡语： 将三张“白银之手新兵”置入你的手牌。"""

    # <b>Deathrattle:</b> Add 3 Silver_Hand Recruits to_your_hand.
    deathrattle = Give(CONTROLLER, "CS2_101t") * 3


class LOOT_398:
    """Benevolent Djinn / 和蔼的灯神
    在你的回合结束时，为你的英雄恢复#3点生命值。"""

    # At the end of your turn, restore 3 Health to your_hero.
    events = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 3))


##
# Spells


class LOOT_088:
    """Potion of Heroism / 英勇药水
    使一个随从获得圣盾。抽 一张牌。"""

    # Give a minion <b>Divine_Shield</b>. Draw a card.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = GiveDivineShield(TARGET), Draw(CONTROLLER)


class LOOT_091:
    """Lesser Pearl Spellstone / 小型法术珍珠
    召唤一个2/2并具有嘲讽的灵魂。@（恢复3点生命值后升级。）"""

    # Summon a 2/2 Spirit with <b>Taunt</b>. @<i>(Restore 3 Health to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    progress_total = 3
    play = Summon(CONTROLLER, "LOOT_091t")
    reward = Morph(SELF, "LOOT_091t1")

    class Hand:
        events = Heal().on(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))


class LOOT_091t1:
    """Pearl Spellstone"""

    # Summon a 4/4 Spirit with <b>Taunt</b>. @
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    progress_total = 3
    play = Summon(CONTROLLER, "LOOT_091t1t")
    reward = Morph(SELF, "LOOT_091t2")

    class Hand:
        events = Heal().on(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))


class LOOT_091t2:
    """Greater Pearl Spellstone"""

    # Summon a 6/6 Spirit with <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "LOOT_091t2t")


class LOOT_093:
    """Call to Arms / 战斗号角
    招募三个法力值消耗小于或等于（2）点的随从。"""

    # [x]<b>Recruit</b> 3 minions that cost (2) or less.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Recruit(COST <= 2) * 3


class LOOT_333:
    """Level Up! / 等级提升
    使你的白银之手新兵获得+2/+2和嘲讽。"""

    # Give your Silver Hand Recruits +2/+2 and_<b>Taunt</b>.
    play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "LOOT_333e")


LOOT_333e = buff(+2, +2, taunt=True)


##
# Weapons


class LOOT_286:
    """Unidentified Maul / 未鉴定的重槌
    在你手牌中时获得额外效果。"""

    # Gains a bonus effect in_your hand.
    entourage = ["LOOT_286t1", "LOOT_286t2", "LOOT_286t3", "LOOT_286t4"]
    draw = Morph(SELF, RandomEntourage())


class LOOT_286t1:
    """Champion's Maul"""

    # <b>Battlecry:</b> Summon two 1/1 Silver Hand Recruits.
    play = Summon(CONTROLLER, "CS2_101t") * 2


class LOOT_286t2:
    """Sacred Maul"""

    # <b>Battlecry:</b> Give your minions <b>Taunt</b>.
    play = Taunt(FRIENDLY_MINIONS)


class LOOT_286t3:
    """Blessed Maul"""

    # <b>Battlecry:</b> Give your minions +1 Attack.
    play = Buff(FRIENDLY_MINIONS, "LOOT_286t3e")


LOOT_286t3e = buff(atk=1)


class LOOT_286t4:
    """Purifier's Maul"""

    # <b>Battlecry:</b> Give your minions <b>Divine Shield</b>.
    play = GiveDivineShield(FRIENDLY_MINIONS)


class LOOT_500:
    """Val'anyr / 瓦兰奈尔
    亡语：使你手牌中的一张随从牌获得+4/+2。当该随从死亡时，重新装备这把武器。"""

    # <b>Deathrattle:</b> Give a minion in your hand +4/+2. When it dies, reequip this.
    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS), "LOOT_500e")


class LOOT_500e:
    tags = {
        GameTag.DEATHRATTLE: True,
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
    }
    deathrattle = Summon(CONTROLLER, "LOOT_500")
