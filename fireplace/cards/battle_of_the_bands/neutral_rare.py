# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- 中立 稀有
"""

from ..utils import *

class ETC_542:
    """音乐节保安 / Festival Security
    <b>嘲讽</b>。<b>压轴：</b>迫使所有敌方随从攻击本随从。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
        GameTag.TAUNT: True,
    }
    finale = Attack(ENEMY_MINIONS, SELF)
class ETC_422:
    """计拍侏儒 / Metrognome
    在你使用一张法力值消耗为（{0}）的卡牌后，抽一张法力值消耗为（{1}）的牌。<i>（然后调高！）</i>"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    # 这个卡牌需要追踪当前的费用值，每次触发后递增
    # 初始值为 0 和 1
    events = Play(CONTROLLER).after(
        Find(PLAYED_CARD + (COST == SELF_NUM_MINIONS_PLAYED_THIS_TURN)) &
        ForceDraw(CONTROLLER, FRIENDLY_DECK + (COST == SELF_NUM_MINIONS_PLAYED_THIS_TURN + 1)) &
        Buff(SELF, "ETC_422e")
    )


class ETC_422e:
    """递增计数"""
    tags = {GameTag.TAG_SCRIPT_DATA_NUM_1: 1}
class ETC_419:
    """摇滚缝合怪 / Mish-Mash Mosher
    <b>突袭</b>。在本随从攻击后，获得+1攻击力并随机攻击一个敌方随从。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 10,
        GameTag.COST: 8,
        GameTag.RUSH: True,
    }
    events = Attack(SELF).after(Buff(SELF, "ETC_419e"), Attack(SELF, RANDOM_ENEMY_MINION))


class ETC_419e:
    tags = {GameTag.ATK: 1}
class JAM_034:
    """音箱践踏者 / Speaker Stomper
    <b>可交易</b>
<b>战吼：</b>下个回合敌方法术的法力值消耗增加（2）点。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
        GameTag.TRADEABLE: True,
    }
    play = Buff(OPPONENT, "JAM_034e")


class JAM_034e:
    """敌方法术增加费用"""
    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +2})
    events = TURN_BEGIN.on(Destroy(SELF))
class ETC_089:
    """静滞波形 / Static Waveform
    在每个回合开始时，失去1点攻击力或生命值<i>（随机而定）。</i>"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 6,
        GameTag.COST: 3,
    }
    events = TURN_BEGIN.on(
        RANDOM(
            Buff(SELF, "ETC_089e"),
            Buff(SELF, "ETC_089e2")
        )
    )


class ETC_089e:
    """失去攻击力"""
    tags = {GameTag.ATK: -1}


class ETC_089e2:
    """失去生命值"""
    tags = {GameTag.HEALTH: -1}
class ETC_098:
    """狼人场务 / Worgen Roadie
    <b>战吼：</b>为你的对手召唤一个0/3的乐器箱。<i>（打破乐器箱可以获得一张随机武器牌！）</i>"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    play = Summon(OPPONENT, "ETC_098t")
