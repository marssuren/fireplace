from ..utils import *


##
# Minions


class GIL_198:
    """Azalina Soulthief / 窃魂者阿扎莉娜
    战吼：将你的手牌替换成对手手牌的 复制。"""

    # <b>Battlecry:</b> Replace your hand with a copy of your_opponent's.
    play = Remove(FRIENDLY_HAND), Give(CONTROLLER, Copy(ENEMY_HAND))


class GIL_578:
    """Countess Ashmore / 女伯爵阿莎摩尔
    战吼：从你的牌库中抽一张突袭牌、吸血牌和亡语牌。"""

    # [x]<b>Battlecry:</b> Draw a <b>Rush</b>, <b>Lifesteal</b>, and <b>Deathrattle</b>
    # card from your deck.
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + RUSH)),
        ForceDraw(RANDOM(FRIENDLY_DECK + LIFESTEAL)),
        ForceDraw(RANDOM(FRIENDLY_DECK + DEATHRATTLE)),
    )


class GIL_620:
    """Dollmaster Dorian / 人偶大师多里安
    每当你抽到一张随从牌，召唤一个它的1/1复制。"""

    # Whenever you draw a minion, summon a 1/1 copy of it.
    events = Draw(CONTROLLER, MINION).after(
        Summon(CONTROLLER, Buff(Copy(Draw.CARD), "GIL_620e"))
    )


class GIL_620e:
    atk = SET(1)
    max_health = SET(1)


class GIL_692:
    """Genn Greymane / 吉恩·格雷迈恩
    对战开始时：如果你的套牌中只有法力值消耗为偶数的牌，你的初始英雄技能的法力值消耗变为（1）点。"""

    # [x]<b>Start of Game:</b> If your deck has only even- Cost cards, your starting Hero
    # Power costs (1).
    class Deck:
        events = GameStart().on(
            EvenCost(STARTING_DECK) & Buff(FRIENDLY_HERO_POWER, "GIL_692e")
        )

    class Hand:
        events = GameStart().on(
            EvenCost(STARTING_DECK) & Buff(FRIENDLY_HERO_POWER, "GIL_692e")
        )


class GIL_692e:
    cost = SET(1)


class GIL_826:
    """Baku the Mooneater / 噬月者巴库
    对战开始时：如果你的套牌中只有法力值消耗为奇数的牌，升级你的英雄技能。"""

    # [x]<b>Start of Game:</b> If your deck has only odd- Cost cards, upgrade your Hero
    # Power.
    class Deck:
        events = GameStart().on(OddCost(STARTING_DECK) & UPGRADE_HERO_POWER)

    class Hand:
        events = GameStart().on(OddCost(STARTING_DECK) & UPGRADE_HERO_POWER)
