"""
Banana Brawl
"""

from ..utils import *


RandomBanana = RandomID("EX1_014t", "TB_006", "TB_007", "TB_008")


class TB_006:
    """Big Banana / 大香蕉
    使一个随从获得+2/+2。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "TB_006e")


TB_006e = buff(+2, +2)


class TB_007:
    """Deviate Banana / 改造香蕉
    使一个随从的攻击力和生命值 互换。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "TB_007e")


TB_007e = AttackHealthSwapBuff()


class TB_008:
    """Rotten Banana / 烂香蕉
    造成$1点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1)
