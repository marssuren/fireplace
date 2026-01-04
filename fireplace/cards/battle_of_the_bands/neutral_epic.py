# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- 中立 史诗
"""

from ..utils import *

class ETC_087:
    """扩音机 / Audio Amplifier
    <b>战吼：</b>将你的法力值上限和手牌上限变为11。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    play = (
        SetTag(FRIENDLY_HERO, {GameTag.RESOURCES: 11}),
        SetTag(FRIENDLY_HERO, {GameTag.HAND_SIZE_BASE: 11})
    )
class ETC_110:
    """封面艺人 / Cover Artist
    <b>战吼：</b>变形成为一个随从的3/3的复制。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Morph(SELF, ExactCopy(TARGET)), SetTag(SELF, {GameTag.ATK: 3, GameTag.HEALTH: 3})
class ETC_104:
    """人潮冲浪者 / Crowd Surfer
    <b>亡语：</b>使任意一个其他随从获得+1/+1和此<b>亡语</b>。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    deathrattle = Buff(RANDOM(ALL_MINIONS - SELF), "ETC_104e")


class ETC_104e:
    """获得+1/+1和亡语"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}
    deathrattle = Buff(RANDOM(ALL_MINIONS - SELF), "ETC_104e")
class ETC_336:
    """自由飞鸟 / Freebird
    <b>冲锋</b>。<b>战吼：</b>在本局对战中，你每使用过一张其他自由飞鸟，便获得+1/+1。0<i>（已使用0张）</i>"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 4,
        GameTag.CHARGE: True,
    }
    play = Buff(SELF, "ETC_336e") * Count(FRIENDLY_HERO + TIMES_PLAYED_THIS_GAME("ETC_336"))


class ETC_336e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}
class JAM_035:
    """恐怖图腾扫兴怪 / Grimtotem Buzzkill
    <b>战吼：</b>弃一张武器牌以抽三张牌。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    play = Find(FRIENDLY_HAND + WEAPON) & (Discard(RANDOM(FRIENDLY_HAND + WEAPON)), Draw(CONTROLLER) * 3)
class ETC_349:
    """过气明星 / Unpopular Has-Been
    <b>亡语：</b>随机召唤一个来自过去的法力值消耗为（5）的随从。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=5, card_set=CardSet.WILD))
