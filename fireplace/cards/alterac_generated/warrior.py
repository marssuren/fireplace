# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 战士
"""

from ..utils import *


class AV_108:
    """裂盾一击 / Shield Shatter
    对所有随从造成$5点伤害。你每有1点护甲值，本牌的法力值消耗便减少（1）点。"""
    play = Hit(ALL_MINIONS, 5)
    cost_mod = lambda self, i: -min(self.controller.hero.armor, self.cost - 1)


class AV_109:
    """凝冰护盾 / Frozen Buckler
    获得10点护甲值。在你的下个回合开始时，失去5点护甲值。"""
    play = GainArmor(FRIENDLY_HERO, 10) & Buff(FRIENDLY_HERO, "AV_109e")


class AV_109e:
    """凝冰护盾效果"""
    events = OwnTurnBegins(CONTROLLER).on(
        GainArmor(FRIENDLY_HERO, -5) & Destroy(SELF)
    )


class AV_119:
    """奔赴前线 / To the Front!
    在本回合中，你的随从牌的法力值消耗减少（2）点（但不能少于1点）。"""
    play = Buff(CONTROLLER, "AV_119e")


class AV_119e:
    """奔赴前线效果"""
    update = Refresh(FRIENDLY_HAND + MINION, {
        GameTag.COST: lambda self, i: max(1, self.cost - 2)
    })
    events = OwnTurnEnds(CONTROLLER).on(Destroy(SELF))


class AV_145:
    """加尔范上尉 / Captain Galvangar
    战吼：在本局对战中，如果你获得的护甲值大于或等于15点，便获得+3/+3和冲锋。"""
    def play(self):
        """检查护甲值获得"""
        if self.controller.armor_gained_this_game >= 15:
            yield Buff(SELF, "AV_145e") & SetTag(SELF, {GameTag.CHARGE: True})


class AV_145e:
    """加尔范上尉增益"""
    atk = 3
    max_health = 3


class AV_321:
    """荣耀追逐者 / Glory Chaser
    在你打出一张嘲讽随从后，抽一张牌。"""
    events = Play(CONTROLLER, MINION + TAUNT).after(Draw(CONTROLLER))


class AV_322:
    """冰雪围困 / Snowed In
    消灭一个受伤的随从。冻结所有其他随从。"""
    play = Destroy(TARGET) & Freeze(ALL_MINIONS - TARGET)


class AV_323:
    """废料铁匠 / Scrapsmith
    嘲讽 战吼：将两张2/4并具有嘲讽的步兵牌置入你的手牌。"""
    play = Give(CONTROLLER, "AV_323t") * 2


class AV_323t:
    """步兵 / Grunt
    2/4 嘲讽随从"""
    # 在 CardDefs.xml 中定义


class AV_565:
    """执斧狂战士 / Axe Berserker
    突袭 荣誉击杀：抽一张武器牌。"""
    honorable_kill = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON))


class AV_660:
    """冰血要塞 / Iceblood Garrison
    在你的回合结束时，对所有随从造成$1点伤害。持续3个回合。"""
    # 前地标时代的伪地标设计
    # 使用 PseudoSecret 核心类实现
    
    # 设置持续时间
    duration = 3
    
    # 伪奥秘事件：每回合结束时触发
    pseudo_secret = [
        OwnTurnEnds(CONTROLLER).on(
            Hit(ALL_MINIONS, 1)
        ).then(
            # 递减持续时间
            lambda self: self.decrement_duration()
        )
    ]


class ONY_023:
    """猛力进攻 / Hit It Very Hard
    在本回合中，获得+10攻击力和"无法攻击英雄"。"""
    play = Buff(FRIENDLY_HERO, "ONY_023e")


class ONY_023e:
    """猛力进攻效果"""
    tags = {
        GameTag.ATK: 10,
        GameTag.CANNOT_ATTACK_HEROES: True
    }
    events = OwnTurnEnds(CONTROLLER).on(Destroy(SELF))


class ONY_024:
    """奥妮克希亚幼龙 / Onyxian Drake
    嘲讽 战吼：对一个敌方随从造成等同于你护甲值的伤害。"""
    play = Hit(TARGET, Count(FRIENDLY_HERO + ARMOR))


class ONY_025:
    """铁肩冲撞 / Shoulder Check
    可交易 使一个随从获得+2/+1和突袭。"""
    play = Buff(TARGET, "ONY_025e") & SetTag(TARGET, {GameTag.RUSH: True})


class ONY_025e:
    """铁肩冲撞增益"""
    atk = 2
    max_health = 1
