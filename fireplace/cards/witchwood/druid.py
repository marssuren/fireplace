from ..utils import *


##
# Minions


class GIL_130:
    """Gloom Stag / 阴郁的牡鹿
    嘲讽，战吼：如果你的牌库中只有法力值消耗为奇数的牌，则获得+2/+2。"""

    # <b>Taunt</b> <b>Battlecry:</b> If your deck has only odd-Cost cards, gain +2/+2.
    powered_up = OddCost(FRIENDLY_DECK)
    play = powered_up & Buff(SELF, "GIL_130e")


GIL_130e = buff(+2, +2)


class GIL_188:
    """Druid of the Scythe / 镰刀德鲁伊
    抉择：变形成为4/2并具有突袭；或者变形成为2/4并具有嘲讽。"""

    # [x]<b>Choose One -</b> Transform into a 4/2 with <b>Rush</b>; or a 2/4 with
    # <b>Taunt</b>.
    choose = ("GIL_188a", "GIL_188b")
    play = ChooseBoth(CONTROLLER) & Morph(SELF, "GIL_188t3")


class GIL_188a:
    play = Morph(SELF, "GIL_188t")


class GIL_188b:
    play = Morph(SELF, "GIL_188t2")


class GIL_507:
    """Bewitched Guardian / 失魂的守卫
    嘲讽，战吼： 你每有一张手牌，便获得+1生命值。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Gain +1 Health _for each card in your hand._
    play = Buff(SELF, "GIL_507e") * Count(FRIENDLY_HAND)


GIL_507e = buff(health=1)


class GIL_658:
    """Splintergraft / 碎枝
    战吼：选择一个友方随从。将它的一张10/10复制置入你的手牌，其法力值消耗为（10）点。"""

    # [x]<b>Battlecry:</b> Choose a friendly minion. Add a 10/10 copy to your hand that
    # costs (10).
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Give(CONTROLLER, MultiBuff(Copy(TARGET), ["GIL_658e", "GBL_007e"]))


class GIL_658e:
    atk = SET(10)
    max_health = SET(10)


class GIL_800:
    """Duskfallen Aviana / 暮陨者艾维娜
    在每个玩家的回合中，使用的第一张牌法力值消耗为（0）点。"""

    # On each player's turn, the first card played costs (0).
    events = TURN_BEGIN.on(Buff(CURRENT_PLAYER, "GIL_800e2"))


class GIL_800e2:
    update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(0)})
    events = Play(CONTROLLER).on(Destroy(SELF))


class GIL_833:
    """Forest Guide / 森林向导
    在你的回合结束时，双方玩家各抽 一张牌。"""

    # At the end of your turn, both players draw a card.
    events = OWN_TURN_END.on(Draw(PLAYER))


##
# Spells


class GIL_553:
    """Wispering Woods / 精灵之森
    你每有一张手牌，便召唤一个1/1的小精灵。"""

    # [x]Summon a 1/1 Wisp for each card in your hand.
    play = Summon(CONTROLLER, "GIL_553t") * Count(FRIENDLY_HAND)


class GIL_571:
    """Witching Hour / 巫术时刻
    随机召唤一个在本局对战中死亡的友方野兽。"""

    # Summon a random friendly Beast that died this game.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: 20,
    }
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + BEAST)))


class GIL_637:
    """Ferocious Howl / 凶猛咆哮
    抽一张牌。你每有一张手牌，便获得1点护甲值。"""

    # Draw a card. Gain 1 Armor for each card in your hand.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Draw(CONTROLLER), GainArmor(FRIENDLY_HERO, Count(FRIENDLY_HAND))


class GIL_663:
    """Witchwood Apple / 女巫森林苹果
    将两张2/2的树人置入你的手牌。"""

    # Add three 2/2 Treants to your hand.
    play = Give(CONTROLLER, "GIL_663t") * 2
