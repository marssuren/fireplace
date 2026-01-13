# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 恶魔猎手
"""

from ..utils import *


class AV_118:
    """历战先锋 / Veteran Warmedic
    在你的英雄攻击后，召唤两只1/1的邪翼蝠。"""
    events = Attack(FRIENDLY_HERO).after(
        Summon(CONTROLLER, "AV_118t") * 2
    )


class AV_118t:
    """邪翼蝠 / Felwing
    1/1 恶魔"""
    # 在 CardDefs.xml 中定义


class AV_204:
    """裂魔者库尔特鲁斯 / Kurtrus, Demon-Render
    战吼：召唤两个1/4并具有突袭的恶魔。（在本局对战中，你的英雄每攻击一次都会提升。）"""
    play = Summon(CONTROLLER, "AV_204t") * 2


class AV_204t:
    """裂魔者的恶魔 / Demon Render
    1/4 突袭 恶魔"""
    # 在 CardDefs.xml 中定义


class AV_209:
    """恐惧牢笼战刃 / Felscale Armor
    荣誉消灭：对敌方英雄造成等同于你英雄的攻击力的伤害。"""
    honorable_kill = Hit(ENEMY_HERO, Count(FRIENDLY_HERO + ATK))


class AV_261:
    """擎旗奔行者 / Flag Runner
    每当一个友方随从死亡，便获得+1攻击力。"""
    events = Death(FRIENDLY + MINION).on(Buff(SELF, "AV_261e"))


class AV_261e:
    """擎旗奔行者增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


class AV_262:
    """锁链守望者 / Flanking Maneuver
    嘲讽 战吼：如果你的手牌中有法力值消耗大于或等于（5）点的恶魔牌，便获得+1/+2。"""
    powered_up = Find(FRIENDLY_HAND + DEMON + (COST >= 5))
    play = powered_up & Buff(SELF, "AV_262e")


class AV_262e:
    """锁链守望者增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class AV_264:
    """清算咒符 / Sigil of Reckoning
    在你的下个回合开始时，从你的手牌中召唤一个恶魔。"""
    play = Buff(FRIENDLY_HERO, "AV_264e")


class AV_264e:
    """清算咒符效果"""
    events = OWN_TURN_BEGIN.on(
        Find(FRIENDLY_HAND + DEMON) & Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON)) & Destroy(SELF)
    )


class AV_265:
    """乌祖尔巨兽 / Ur'zul Giant
    在本局对战中，每有一个友方随从死亡，本牌的法力值消耗便减少（1）点。"""
    cost_mod = lambda self, i: -self.controller.minions_killed_this_game


class AV_267:
    """凯丽娅·邪语 / Kael'thas Sinstrider
    战吼：变形成为你牌库中一个恶魔的6/6复制。"""
    def play(self):
        """变形为牌库中的恶魔"""
        demons = self.controller.deck.filter(race=Race.DEMON)
        if demons:
            demon = self.game.random.choice(demons)
            # 创建6/6复制
            yield Morph(SELF, Copy(demon))
            # 设置属性为6/6
            yield SetTags(SELF, {GameTag.ATK: 6, GameTag.HEALTH: 6})


class AV_269:
    """侧翼合击 / Flanking Strike
    召唤一个4/2并具有突袭的恶魔。如果它在本回合中死亡,再召唤一个。"""
    def play(self):
        """召唤恶魔并添加追踪器"""
        yield Summon(CONTROLLER, "AV_269t")
        yield Buff(CONTROLLER, "AV_269e")


class AV_269t:
    """侧翼恶魔 / Flanking Demon
    4/2 突袭 恶魔"""
    # 在 CardDefs.xml 中定义


class AV_269e:
    """侧翼合击追踪器"""
    events = Death(FRIENDLY + MINION + ID("AV_269t")).on(
        lambda self: (
            getattr(self.controller, 'turn_played', -1) == self.game.turn and
            (Summon(CONTROLLER, "AV_269t"), Destroy(SELF))
        ) or None
    )


class AV_661:
    """征战平原 / Battle Grounds
    你的随从拥有+1攻击力。持续3回合。"""
    # 前地标时代的伪地标设计
    # 使用 PseudoSecret 核心类实现
    
    # 设置持续时间
    duration = 3
    
    # 伪奥秘事件：持续给予随从+1攻击力
    pseudo_secret = [
        # 使用update刷新随从攻击力
    ]
    
    # 更新效果
    update = Refresh(FRIENDLY_MINIONS, {GameTag.ATK: +1})
    
    # 回合结束时递减持续时间
    events = OWN_TURN_END.on(
        lambda self: self.decrement_duration()
    )


class ONY_014:
    """敏锐反应 / Keen Reflex
    对所有随从造成$1点伤害。荣誉消灭：在本回合中获得+1攻击力。"""
    play = Hit(ALL_MINIONS, 1)
    honorable_kill = Buff(FRIENDLY_HERO, "ONY_014e")


class ONY_014e:
    """敏锐反应增益"""
    tags = {GameTag.ATK: 1}
    events = OWN_TURN_END.on(Destroy(SELF))


class ONY_016:
    """憎恨之翼（等级1） / Wings of Hate (Rank 1)
    召唤两只1/1的邪翼蝠。（当你有5点法力值时升级。）"""
    
    # 升级机制
    powered_up = lambda self: self.controller.max_mana >= 5
    
    def play(self):
        """召唤邪翼蝠，如果满足条件则升级"""
        yield Summon(CONTROLLER, "AV_118t") * 2
        if self.controller.max_mana >= 5:
            # 升级为等级2
            yield Morph(SELF, "ONY_016t")


class ONY_016t:
    """憎恨之翼（等级2） / Wings of Hate (Rank 2)
    召唤两只2/2的邪翼蝠。"""
    play = Summon(CONTROLLER, "ONY_016t2") * 2


class ONY_016t2:
    """强化邪翼蝠 / Enhanced Felwing
    2/2 恶魔"""
    # 在 CardDefs.xml 中定义


class ONY_036:
    """爪刃哨兵 / Claw Machine
    在你使用最左或最右边的一张手牌后，抽一张牌。"""
    events = Play(CONTROLLER).on(
        lambda self, player, card, *args: (
            (card.play_left_most or card.play_right_most) and Draw(CONTROLLER)
        ) or None
    )
