from ..utils import *


# Luck of the Coin
GAME_001 = buff(health=3)


class GAME_003:
    """Coin's Vengeance / 幸运币复仇
    后手出牌会使你的第一个随从获得增强。"""

    events = Play(CONTROLLER, MINION).on(Buff(Play.CARD, "GAME_003e"), Destroy(SELF))


GAME_003e = buff(+1, +1)


class GAME_004:
    """AFK / 暂离
    你的回合时间减少。"""

    update = Refresh(CONTROLLER, {GameTag.TIMEOUT: 10})


class GAME_005:
    """The Coin / 幸运币
    在本回合中，获得一个 法力水晶。"""

    play = ManaThisTurn(CONTROLLER, 1)


class GBL_001e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class GBL_002e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class GBL_003e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class GBL_004e:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY


class GBL_005e:
    tags = {GameTag.COST: +2}
    events = REMOVED_IN_PLAY


class GBL_006e:
    cost = SET(2)
    events = REMOVED_IN_PLAY


class GBL_007e:
    cost = SET(10)
    events = REMOVED_IN_PLAY


class GBL_008e:
    tags = {GameTag.COST: -4}
    events = REMOVED_IN_PLAY


class GBL_009e:
    cost = SET(0)
    events = REMOVED_IN_PLAY
