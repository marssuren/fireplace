from ..utils import *


##
# Minions


class GVG_020:
    """Fel Cannon / 邪能火炮
    在你的回合结束时，对一个非机械随从造成2点伤害。"""

    events = OWN_TURN_END.on(Hit(RANDOM(ALL_MINIONS - MECH), 2))


class GVG_021:
    """Mal'Ganis / 玛尔加尼斯
    你的英雄免疫。你的其他恶魔拥有+2/+2。"""

    update = (
        Refresh(FRIENDLY_MINIONS + DEMON - SELF, buff="GVG_021e"),
        Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True}),
    )


GVG_021e = buff(+2, +2)


class GVG_077:
    """Anima Golem / 心能魔像
    在每个回合结束时，如果本随从是你唯一的随从，则消灭 本随从。"""

    def _check_and_destroy(self, source):
        # 检查是否是唯一的随从
        other_minions = [m for m in self.controller.field if m != self]
        if len(other_minions) == 0:
            # 是唯一的随从,销毁自己
            yield Destroy(SELF)
    
    events = TURN_END.on(_check_and_destroy)


class GVG_100:
    """Floating Watcher / 漂浮观察者
    每当你的英雄在你的回合受到伤害，便获得+2/+2。"""

    events = Damage(FRIENDLY_HERO).on(
        CurrentPlayer(CONTROLLER) & Buff(SELF, "GVG_100e")
    )


GVG_100e = buff(+2, +2)


##
# Spells


class GVG_015:
    """Darkbomb / 暗色炸弹
    对一个角色造成$3点伤害。如果该角色死亡，抽一张暗影法术牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)


class GVG_019:
    """Demonheart / 恶魔之心
    对一个随从造成$5点伤害，如果该随从是友方恶魔，则改为使其获得+5/+5。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 检查目标是否为友方恶魔
        if self.target.controller == self.controller and Race.DEMON in self.target.races:
            # 友方恶魔:+5/+5
            yield Buff(TARGET, "GVG_019e")
        else:
            # 非友方恶魔:造成5点伤害
            yield Hit(TARGET, 5)


GVG_019e = buff(+5, +5)


class GVG_045:
    """Imp-losion / 小鬼爆破
    对一个随从造成$2-$4点伤害。每造成1点伤害，便召唤一个1/1的小鬼。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Summon(CONTROLLER, "GVG_045t") * Hit(TARGET, RandomNumber(2, 3, 4))
