"""
Base game rules (events, etc)
"""

from .cards.utils import *


HEAVILY_ARMORED = [Predamage(SELF, lambda i: i > 1).on(Predamage(SELF, 1))]


class WeaponRules:
    base_events = [Attack(FRIENDLY_HERO).after(Hit(SELF, 1))]


class LocationRules:
    """
    地标基础规则

    地标的核心规则:
    1. 回合开始时重置激活次数
    2. 回合开始时解除冷却状态
    3. 耐久度归零时自动销毁
    """
    base_events = [
        # 回合开始时重置激活次数和冷却状态
        OWN_TURN_BEGIN.on(
            SetTag(SELF, (GameTag.ACTIVATIONS_THIS_TURN, 0)),
            SetTag(SELF, (GameTag.COOLDOWN, False))
        )
    ]

