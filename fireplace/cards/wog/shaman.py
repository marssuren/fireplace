from ..utils import *


##
# Minions


class OG_023:
    """Primal Fusion / 原始融合
    你每有一个图腾，就使一个随从获得+1/+1。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "OG_023t") * Count(FRIENDLY_MINIONS + TOTEM)


OG_023t = buff(+1, +1)


class OG_026:
    """Eternal Sentinel / 永恒哨卫
    战吼：将你所有过载的法力水晶解锁。"""

    play = UnlockOverload(CONTROLLER)


class OG_209:
    """Hallazeal the Ascended / 升腾者海纳泽尔
    法术伤害+1 你的法术拥有吸血。"""

    events = Damage(source=SPELL + FRIENDLY).on(Heal(FRIENDLY_HERO, Damage.AMOUNT))


class OG_328:
    """Master of Evolution / 异变之主
    战吼：将一个友方随从随机变形成为一个法力值消耗增加（1）点的随从。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Evolve(TARGET, 1)


class OG_028:
    """Thing from Below / 深渊魔物
    嘲讽 在本局对战中，你每召唤一个图腾，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Attr(CONTROLLER, "times_totem_summoned_this_game")


##
# Spells


class OG_027:
    """Evolve / 异变
    随机将你的 所有随从变形成为法力值消耗增加（1）点的随从。"""

    play = Evolve(FRIENDLY_MINIONS, 1)


class OG_206:
    """Stormcrack / 雷暴术
    对一个随从造成$4点伤害，过载：（1）"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4)


##
# Weapons


class OG_031:
    """Hammer of Twilight / 暮光神锤
    亡语：召唤一个4/2的元素。"""

    deathrattle = Summon(CONTROLLER, "OG_031a")
