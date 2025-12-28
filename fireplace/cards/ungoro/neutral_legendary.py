from ..utils import *


##
# Minions


class UNG_840:
    """Hemet, Jungle Hunter / “丛林猎人”赫米特
    战吼： 摧毁你牌库中所有法力值消耗小于或等于（3）点的卡牌。"""

    play = Destroy(FRIENDLY_DECK + (COST <= 3))


class UNG_843:
    """The Voraxx / 沃拉斯
    在你对本随从施放一个法术后，召唤一个1/1的植物，并对其施放相同的法术。"""

    events = Play(CONTROLLER, SPELL, SELF).after(
        CastSpell(Play.CARD, Summon(CONTROLLER, "UNG_999t2t1"))
    )


class UNG_851:
    """Elise the Trailblazer / “开拓者”伊莉斯
    战吼： 将一张安戈洛卡牌包洗入你的牌库。如果你的牌库里没有相同的牌，则抽取这张卡牌包。"""

    play = Shuffle(CONTROLLER, "UNG_851t1")


class UNG_851t1:
    """Un\'Goro Pack"""

    play = Give(CONTROLLER, RandomCollectible(card_set=CardSet.UNGORO)) * 5


class UNG_900:
    """Spiritsinger Umbra / 灵魂歌者安布拉
    在你召唤一个随从后，触发其亡语。"""

    events = Summon(CONTROLLER, MINION).after(Deathrattle(Summon.CARD))


class UNG_907:
    """Ozruk / 欧泽鲁克
    嘲讽，战吼：在上个回合，你每使用一张元素牌，便获得+5生命值。"""

    play = Buff(SELF, "UNG_907e") * Attr(CONTROLLER, enums.ELEMENTAL_PLAYED_LAST_TURN)


UNG_907e = buff(health=5)
