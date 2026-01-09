# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 中立稀有
"""

from ..utils import *


class AV_112:
    """雪盲鹰身人 / Snowblind Harpy
    战吼：如果你的手牌中有冰霜法术，获得5点护甲值。"""
    play = (Find(FRIENDLY_HAND + SPELL + FROST), GainArmor(FRIENDLY_HERO, 5))


class AV_134:
    """霜狼将领 / Frostwolf Warmaster
    你本回合每打出一张牌，本牌的法力值消耗便减少（1）点。"""
    cost_mod = -Count(CARDS_PLAYED_THIS_TURN)


class AV_135:
    """雷矛元帅 / Stormpike Marshal
    嘲讽 如果你在对手的回合受到5点或更多伤害，本牌的法力值消耗为（1）点。"""
    def cost_mod(self, i):
        # 检查对手回合受到的伤害
        if self.controller.opponent.current_player:
            return 0
        # 检查上一个对手回合受到的伤害
        if self.controller.damage_taken_on_opponents_turn >= 5:
            return -(self.cost - 1)
        return 0


class AV_136:
    """狗头人监工 / Kobold Taskmaster
    战吼：将2张护甲碎片置入你的手牌，使一个随从获得+2生命值。"""
    play = Give(CONTROLLER, "AV_136t") * 2


class AV_136t:
    """护甲碎片 / Armor Scrap
    使一个随从获得+2生命值。"""
    play = Buff(TARGET, "AV_136te")


class AV_136te:
    """护甲碎片增益"""
    max_health = 2


class AV_137:
    """深铁穴居人 / Irondeep Trogg
    在你的对手施放一个法术后，召唤另一个深铁穴居人。"""
    events = Play(OPPONENT, SPELL).after(Summon(CONTROLLER, "AV_137"))


class ONY_002:
    """全需勇士 / Gear Grubber
    嘲讽 如果你在回合结束时有未使用的法力水晶，本牌的法力值消耗减少（1）点。"""
    events = OWN_TURN_END.on(
        lambda self, source: Buff(self, "ONY_002e") if source.mana - source.used_mana > 0 else None
    )


class ONY_002e:
    """全需勇士减费"""
    cost = -1
