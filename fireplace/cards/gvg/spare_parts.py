"""
Spare Parts
"""

from ..utils import *


class PART_001:
    """Armor Plating / 重型护甲
    使一个随从获得+1生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "PART_001e")
    tags = {GameTag.SPARE_PART: True}


PART_001e = buff(health=1)


class PART_002:
    """Time Rewinder / 时间回溯装置
    将一个友方随从移回你的手牌。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Bounce(TARGET)
    tags = {GameTag.SPARE_PART: True}


class PART_003:
    """Rusty Horn / 生锈的号角
    使一个随从获得嘲讽。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Taunt(TARGET)
    tags = {GameTag.SPARE_PART: True}


class PART_004:
    """Finicky Cloakfield / 隐秘力场
    直到你的下个回合，使一个友方随从获得潜行。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET - STEALTH, "PART_004e")
    tags = {GameTag.SPARE_PART: True}


class PART_004e:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class PART_005:
    """Emergency Coolant / 紧急冷冻剂
    冻结一个随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Freeze(TARGET)
    tags = {GameTag.SPARE_PART: True}


class PART_006:
    """Reversing Switch / 形体改造仪
    使一个随从的攻击力和生命值 互换。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "PART_006a")
    tags = {GameTag.SPARE_PART: True}


PART_006a = AttackHealthSwapBuff()


class PART_007:
    """Whirling Blades / 旋风之刃
    使一个随从获得+1攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "PART_007e")
    tags = {GameTag.SPARE_PART: True}


PART_007e = buff(atk=1)
