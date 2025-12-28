"""
Decks Assemble
"""

from ..utils import *


class TB_010:
    """Deckbuilding Enchant / 套牌构筑强化"""

    events = (
        OWN_TURN_BEGIN.on(DISCOVER(RandomCollectible())),
        Play(CONTROLLER).on(Shuffle(CONTROLLER, Copy(Play.CARD))),
        OWN_TURN_END.on(Shuffle(CONTROLLER, FRIENDLY_HAND)),
    )


class TB_011:
    """Tarnished Coin / 生锈的硬币
    在本回合中，获得一个法力水晶。"""

    play = ManaThisTurn(CONTROLLER, 1)
