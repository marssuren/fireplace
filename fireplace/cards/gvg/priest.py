from ..utils import *


##
# Minions


class GVG_009:
    """Shadowbomber / 暗影投弹手
    战吼：对每个英雄造成3点伤害。"""

    play = Hit(ALL_HEROES, 3)


class GVG_011:
    """Shrinkmeister / 缩小射线工程师
    战吼：在本回合中，使一个随从获得-3攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Buff(TARGET, "GVG_011a")


GVG_011a = buff(atk=-3)


class GVG_014:
    """Vol'jin / 沃金
    战吼：与另一个随从交换生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = SwapStateBuff(SELF, TARGET, "GVG_014a")


class GVG_014a:
    max_health = lambda self, i: self._xhealth


class GVG_072:
    """Shadowboxer / 暗影打击装甲
    每当一个随从获得治疗，便随机对一个敌人造成1点伤害。"""

    events = Heal(ALL_MINIONS).on(Hit(RANDOM_ENEMY_CHARACTER, 1))


class GVG_083:
    """Upgraded Repair Bot / 高级修理机器人
    战吼：使一个友方机械获得+4生命值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
    }
    # The Enchantment ID is correct
    play = Buff(TARGET, "GVG_069a")


GVG_069a = buff(health=4)


##
# Spells


class GVG_008:
    """Lightbomb / 圣光炸弹
    对所有随从造成等同于其攻击力的伤害。"""

    def play(self):
        for target in self.game.board:
            yield Hit(target, target.atk)


class GVG_010:
    """Velen's Chosen / 维伦的恩泽
    使一个随从获得+2/+4和法术伤害+1。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "GVG_010b")


GVG_010b = buff(+2, +4, spellpower=1)


class GVG_012:
    """Light of the Naaru / 纳鲁之光
    恢复#3点生命值。如果目标仍处于受伤状态，则召唤一个圣光护卫者。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 3), (DAMAGE(TARGET) >= 1) & Summon(CONTROLLER, "EX1_001")
