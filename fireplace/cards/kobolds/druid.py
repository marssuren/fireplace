from ..utils import *


##
# Minions


class LOOT_048:
    """Ironwood Golem / 铁木魔像
    嘲讽 除非你的护甲值大于或等于3点，否则无法进行攻击。"""

    # <b>Taunt</b> Can only attack if you have 3 or more Armor.
    update = (ARMOR(FRIENDLY_HAND) >= 3) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class LOOT_056:
    """Astral Tiger / 星界猛虎
    亡语： 将本随从的一张复制洗入你的牌库。"""

    # <b>Deathrattle:</b> Shuffle a copy of this minion into_your_deck.
    deathrattle = Shuffle(CONTROLLER, Copy(SELF))


class LOOT_314:
    """Grizzled Guardian / 灰熊守护者
    嘲讽，亡语：招募两个法力值消耗小于或等于（4）点的随从。"""

    # <b>Taunt</b> <b>Deathrattle:</b> <b>Recruit</b> 2_minions that cost (4)_or_less.
    deathrattle = Recruit(COST <= 4) * 2


class LOOT_329:
    """Ixlid, Fungal Lord / 伊克斯里德，真菌之王
    在你使用一张随从牌后，召唤一个它的复制。"""

    # After you play a minion, summon a copy of it.
    events = Play(CONTROLLER, MINION).after(Summon(CONTROLLER, ExactCopy(Play.CARD)))


class LOOT_351:
    """Greedy Sprite / 贪婪的林精
    亡语：获得一个空的法力水晶。"""

    # <b>Deathrattle:</b> Gain an empty Mana Crystal.
    deathrattle = GainEmptyMana(CONTROLLER, 1)


##
# Spells


class LOOT_047:
    """Barkskin / 树皮术
    使一个随从 获得+3生命值。 获得3点护甲值。"""

    # Give a minion +3 Health. Gain 3 Armor.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "LOOT_047e"), GainArmor(FRIENDLY_HERO, 3)


LOOT_047e = buff(health=3)


class LOOT_051:
    """Lesser Jasper Spellstone / 小型法术玉石
    对一个随从造成$2点伤害。@（获得3点护甲值后升级。）"""

    # Deal $2 damage to a minion. @<i>(Gain 3 Armor to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    progress_total = 3
    play = Hit(TARGET, 2)
    reward = Morph(SELF, "LOOT_051t1")

    class Hand:
        events = GainArmor(FRIENDLY_HERO).on(
            AddProgress(SELF, GainArmor.TARGET, GainArmor.AMOUNT)
        )


class LOOT_051t1:
    """Jasper Spellstone"""

    # Deal $4 damage to a minion. @
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)
    progress_total = 3
    reward = Morph(SELF, "LOOT_051t2")

    class Hand:
        events = GainArmor(FRIENDLY_HERO).on(
            AddProgress(SELF, GainArmor.TARGET, GainArmor.AMOUNT)
        )


class LOOT_051t2:
    """Greater Jasper Spellstone"""

    # Deal $6 damage to a minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 6)


class LOOT_054:
    """Branching Paths / 分岔路口
    选择两次： 抽一张牌；使你的所有随从获得+1攻击力；或者获得6点护甲值。"""

    # [x]<b>Choose Twice -</b> Draw a card; Give your minions +1 Attack; Gain 6 Armor.
    play = Choice(CONTROLLER, ["LOOT_054b", "LOOT_054c", "LOOT_054d"]).then(
        Battlecry(Choice.CARD, None),
        Choice(CONTROLLER, ["LOOT_054b", "LOOT_054c", "LOOT_054d"]).then(
            Battlecry(Choice.CARD, None),
        ),
    )


class LOOT_054b:
    """Explore the Darkness"""

    # Give your minions +1 Attack.
    play = Buff(FRIENDLY_MINIONS, "LOOT_054be")


LOOT_054be = buff(atk=1)


class LOOT_054c:
    """Loot the Chest"""

    # Gain 6 Armor.
    play = GainArmor(FRIENDLY_HERO, 6)


class LOOT_054d:
    """Eat the Mushroom"""

    # Draw a card.
    play = Draw(CONTROLLER)


class LOOT_309:
    """Oaken Summons / 橡树的召唤
    获得6点护甲值。从你的牌库中召唤一个法力值消耗小于或等于（4）点的随从。"""

    # Gain 6 Armor. <b>Recruit</b> a minion that costs (4) or less.
    play = GainArmor(FRIENDLY_HERO, 6), Recruit(COST <= 4)


##
# Weapons


class LOOT_392:
    """Twig of the World Tree / 世界之树的嫩枝
    亡语：复原你的法力水晶。"""

    # <b>Deathrattle:</b> Gain 10 Mana Crystals.
    deathrattle = GainMana(CONTROLLER, 10)
