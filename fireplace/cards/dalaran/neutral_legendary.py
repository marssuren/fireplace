from ..utils import *


##
# Minions


class DAL_546:
    """Barista Lynchen / 咖啡师林彻
    战吼：将你的所有其他战吼随从的复制置入你的手牌。"""

    # <b>Battlecry:</b> Add a copy of each of your other <b>Battlecry</b>
    # minions_to_your_hand.
    play = Give(CONTROLLER, Copy(FRIENDLY_HAND + BATTLECRY + MINION))


class DAL_554:
    """Chef Nomi / 大厨诺米
    战吼：如果你的牌库里没有牌，则召唤六个6/6的猛火元素。"""

    # <b>Battlecry:</b> If your deck is empty, summon six 6/6 Greasefire_Elementals.
    play = Find(FRIENDLY_DECK) | SummonBothSides(CONTROLLER, "DAL_554t") * 6


class DAL_558:
    """Archmage Vargoth / 大法师瓦格斯
    在你的回合结束时，施放你在本回合中施放过的一个法术（目标随机而定）。"""

    # [x]At the end of your turn, cast a spell you've cast this turn <i>(targets are
    # random)</i>.
    events = OWN_TURN_END.on(CastSpell(Copy(RANDOM(CARDS_PLAYED_THIS_TURN + SPELL))))


class DAL_736:
    """Archivist Elysiana / 档案员艾丽西娜
    战吼：发现五张卡牌，将你牌库里的所有卡牌替换成每张卡牌的两张复制。"""

    # <b>Battlecry:</b> <b>Discover</b> 5 cards. Replace your deck with 2_copies of each.
    play = (
        Destroy(FRIENDLY_DECK),
        Discover(CONTROLLER, RandomCollectible()).then(
            Shuffle(CONTROLLER, Copy(Discover.CARD)) * 2
        )
        * 5,
    )


class DAL_752:
    """Jepetto Joybuzz / 耶比托·乔巴斯
    战吼：从你的牌库中抽两张随从牌。将其攻击力，生命值和法力值消耗变为1。"""

    # <b>Battlecry:</b> Draw 2 minions from your deck. Set their Attack, Health, and Cost
    # to 1.
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
            MultiBuff(ForceDraw.TARGET, ["DAL_752e", "DAL_752e2"])
        )
        * 2
    )


class DAL_752e:
    atk = SET(1)
    max_health = SET(1)


class DAL_752e2:
    cost = SET(1)
    events = REMOVED_IN_PLAY
