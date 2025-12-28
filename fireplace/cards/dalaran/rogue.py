from ..utils import *


##
# Minions


class DAL_415:
    """EVIL Miscreant / 怪盗恶霸
    连击：随机将两张跟班牌置入你的手牌。"""

    # <b>Combo:</b> Add two random <b>Lackeys</b> to your hand.
    combo = Give(CONTROLLER, RandomLackey()) * 2


class DAL_416:
    """Hench-Clan Burglar / 荆棘帮蟊贼
    战吼：发现一张另一职业的法术牌。"""

    # <b>Battlecry:</b> <b>Discover</b> a spell from another class.
    play = GenericChoice(CONTROLLER, RandomSpell(card_class=ANOTHER_CLASS) * 3)


class DAL_417:
    """Heistbaron Togwaggle / 劫匪之王托瓦格尔
    战吼：如果你控制一个跟班，就可以选择一张神奇宝藏。"""

    # <b>Battlecry:</b> If you control a_<b>Lackey</b>, choose a fantastic treasure.
    powered_up = Find(FRIENDLY_MINIONS + LACKEY)
    play = powered_up & GenericChoice(
        CONTROLLER, ["LOOT_998h", "LOOT_998j", "LOOT_998l", "LOOT_998k"]
    )


class DAL_714:
    """Underbelly Fence / 下水道销赃人
    战吼：如果你手牌中有另一职业的卡牌，则获得+1/+1和突袭。"""

    # [x]<b>Battlecry:</b> If you're holding a card from another class, _gain +1/+1 and
    # <b><b>Rush</b>.</b>
    powered_up = Find(FRIENDLY_HAND + ANOTHER_CLASS)
    play = powered_up & Buff(SELF, "DAL_714e")


DAL_714e = buff(+1, +1, rush=True)


class DAL_719:
    """Tak Nozwhisker / 塔克·诺兹维克
    每当你将一张牌洗入你的牌库时，将该牌的一张复制置入你的 手牌。"""

    # [x]Whenever you shuffle a card into your deck, add a copy to your hand.
    events = Shuffle(CONTROLLER, source=FRIENDLY).after(
        Give(CONTROLLER, Copy(Shuffle.CARD))
    )


##
# Spells


class DAL_010(SchemeUtils):
    """Togwaggle's Scheme"""

    # Choose a minion. Shuffle @ |4(copy, copies) of it into your deck. <i>(Upgrades each
    # turn!)</i>
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Shuffle(CONTROLLER, Copy(TARGET)) * (Attr(SELF, GameTag.QUEST_PROGRESS) + 1)


class DAL_366:
    """Unidentified Contract / 未鉴定的合约
    消灭一个随从。在你手牌中时获得额外效果。"""

    # Destroy a minion. Gains a bonus effect in_your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    entourage = ["DAL_366t1", "DAL_366t2", "DAL_366t3", "DAL_366t4"]
    play = Destroy(TARGET)
    draw = Morph(SELF, RandomEntourage())


class DAL_366t1:
    """Assassin's Contract"""

    # Destroy a minion. Summon a 1/1 Patient Assassin.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Summon(CONTROLLER, "EX1_522")


class DAL_366t2:
    """Recruitment Contract"""

    # Destroy a minion. Add_a copy of it to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Give(CONTROLLER, Copy(TARGET))


class DAL_366t3:
    """Lucrative Contract"""

    # Destroy a minion. Add 2 Coins to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Give(CONTROLLER, THE_COIN) * 2


class DAL_366t4:
    """Turncoat Contract"""

    # Destroy a minion. It_deals its damage to adjacent minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(SELF_ADJACENT, ATK(SELF), source=TARGET), Destroy(TARGET)


class DAL_716:
    """Vendetta / 宿敌
    对一个随从造成$4点伤害。如果你的手牌中有另一职业的卡牌，则法力值消耗为（0）点。"""

    # Deal $4 damage to a minion. Costs (0) if you're holding a card from another class.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4)

    class Hand:
        update = Find(FRIENDLY_HAND + ANOTHER_CLASS) & Refresh(
            SELF, {GameTag.COST: SET(0)}
        )


class DAL_728:
    """Daring Escape / 战略转移
    将所有友方随从移回你的手牌。"""

    # Return all friendly minions to your hand.
    play = Bounce(FRIENDLY_MINIONS)


##
# Weapons


class DAL_720:
    """Waggle Pick / 摇摆矿锄
    亡语：随机将一个友方随从移回你的手牌。它的法力值消耗减少（2）点。"""

    # [x]<b>Deathrattle:</b> Return a random friendly minion to your hand. It costs (2)
    # less.
    deathrattle = Bounce(RANDOM_OTHER_FRIENDLY_MINION).then(
        Buff(Bounce.TARGET, "GBL_002e")
    )
