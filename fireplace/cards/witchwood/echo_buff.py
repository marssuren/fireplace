from ..utils import *


class GIL_000:
    """Echo Enchant / 回响附魔
    回合结束时如果这张牌仍在手牌中，将其摧毁。"""

    events = REMOVED_IN_PLAY

    class Hand:
        events = OWN_TURN_END.on(Destroy(OWNER))
        update = Refresh(OWNER, {GameTag.COST: lambda self, i: max(i, 1)}, priority=100)
