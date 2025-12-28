from ..utils import *


##
# Minions


class BT_190:
    """Replicat-o-tron / 复制机器人
    在你的回合结束时，将一个相邻的随从变形成为本随从的复制。"""

    # At the end of your turn, transform a neighbor into a copy of this.
    events = OWN_TURN_END.on(Morph(RANDOM(SELF_ADJACENT), ExactCopy(SELF)))


class BT_729:
    """Waste Warden / 废土守望者
    战吼： 对一个随从及所有相同类型的其他随从造成3点伤害。"""

    # [x]<b>Battlecry:</b> Deal 3 damage to a minion and all others of the same
    # minion type.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Hit(ALL_MINIONS + SAME_RACE_TARGET - TARGET, 3)


class BT_733:
    """Mo'arg Artificer / 莫尔葛工匠
    所有随从受到的法术伤害翻倍。"""

    # All minions take double damage from spells.
    update = Refresh(ALL_MINIONS, {GameTag.INCOMING_DAMAGE_MULTIPLIER: 1})
