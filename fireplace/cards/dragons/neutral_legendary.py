from ..utils import *


##
# Minions


class DRG_089:
    """Dragonqueen Alexstrasza / 红龙女王阿莱克丝塔萨
    战吼：如果你的牌库里没有相同的牌，则随机将两张其他龙牌置入你的手牌，其法力值消耗为（0）点。"""

    # [x]<b>Battlecry:</b> If your deck has no duplicates, add 2 other random Dragons to
    # your hand. They cost (0).
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = (
        powered_up
        & Give(CONTROLLER, RandomDragon(exclude=SELF)).then(Buff(Give.CARD, "DRG_089e"))
        * 2
    )


class DRG_089e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class DRG_091:
    """Shu'ma / 舒玛
    在你的回合结束时，用1/1的触手填满你的面板。"""

    # At the end of your turn, fill your board with 1/1_Tentacles.
    events = OWN_TURN_END.on(SummonBothSides(CONTROLLER, "DRG_091t") * 7)


class DRG_099:
    """Kronx Dragonhoof / 克罗斯·龙蹄
    战吼：抽取迦拉克隆。如果你已经变为迦拉克隆，则释放一场 灾难。"""

    # [x]<b>Battlecry:</b> Draw Galakrond. If you're already Galakrond, unleash a
    # Devastation.
    play = Find(GALAKROND + FRIENDLY_HERO) & (
        Choice(CONTROLLER, ["DRG_099t1", "DRG_099t2", "DRG_099t3", "DRG_099t4"]).then(
            Battlecry(Choice.CARD, None)
        )
    ) | (Find(GALAKROND + FRIENDLY_DECK) & ForceDraw(GALAKROND))


class DRG_099t1:
    """Decimation"""

    # Deal 5 damage to the enemy hero. Restore 5 Health to your hero.
    play = Hit(ENEMY_HERO, 5), Heal(FRIENDLY_HERO, 5)


class DRG_099t2:
    """Reanimation"""

    # Summon an 8/8 Dragon with <b>Taunt</b>.
    play = Summon(CONTROLLER, "DRG_099t2t")


class DRG_099t3:
    """Domination"""

    # Give your other minions +2/+2.
    play = Buff(FRIENDLY_MINIONS - SELF, "DRG_099t3e")


DRG_099t3e = buff(+2, +2)


class DRG_099t4:
    """Annihilation"""

    # Deal 5 damage to all other minions.
    play = Hit(ALL_MINIONS - SELF, 5)


class DRG_257:
    """Frizz Kindleroost / 弗瑞兹·光巢
    战吼：使你牌库中龙牌的法力值消耗减少（2）点。"""

    # <b>Battlecry:</b> Reduce the Cost of Dragons in your deck by_(2).
    play = Buff(FRIENDLY_DECK + DRAGON, "DRG_257e3")


class DRG_257e3:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class DRG_402:
    """Sathrovarr / 萨索瓦尔
    战吼：选择一个友方随从。将一个它的复制置入你的手牌，牌库以及战场。"""

    # <b>Battlecry:</b> Choose a friendly minion. Add a copy of it to_your hand, deck, and
    # battlefield.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = (
        Give(CONTROLLER, Copy(TARGET)),
        Shuffle(CONTROLLER, Copy(TARGET)),
        Summon(CONTROLLER, ExactCopy(TARGET)),
    )
