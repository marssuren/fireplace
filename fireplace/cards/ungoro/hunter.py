from ..utils import *


##
# Minions


class UNG_800:
    """Terrorscale Stalker / 恐鳞追猎者
    战吼：触发一个友方随从的亡语。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Deathrattle(TARGET)


class UNG_912:
    """Jeweled Macaw / 宝石鹦鹉
    战吼：随机将一张野兽牌置入你的手牌。"""

    play = Give(CONTROLLER, RandomBeast())


class UNG_913:
    """Tol'vir Warden / 托维尔守卫
    战吼：从你的牌库中抽两张法力值消耗为（1）的随从牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 1))) * 2


class UNG_914:
    """Raptor Hatchling / 迅猛龙宝宝
    亡语：将一张4/5的“迅猛龙头领”洗入你的 牌库。"""

    deathrattle = Shuffle(CONTROLLER, "UNG_914t1")


class UNG_915:
    """Crackling Razormaw / 雷鸣刺喉龙
    战吼：进化一个友方野兽。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Adapt(TARGET)


class UNG_919:
    """Swamp King Dred / 沼泽之王爵德
    在你的对手使用一张随从牌后，攻击该随从。"""

    events = Play(OPPONENT, MINION).after(
        Find(Play.CARD + IN_PLAY - DEAD)
        & (Find(SELF - FROZEN) & Attack(SELF, Play.CARD))
    )


##
# Spells


class UNG_910:
    """Grievous Bite / 凶残撕咬
    对一个随从造成$3点伤害，并对其相邻的随从 造成$1点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Hit(TARGET_ADJACENT, 1)


class UNG_916:
    """Stampede / 奔踏
    在本回合中，每当你使用一张野兽牌，随机将一张野兽牌置入你的手牌。"""

    play = Buff(CONTROLLER, "UNG_916e")


class UNG_916e:
    events = Play(CONTROLLER, BEAST).after(lambda self, source, *args: Give(CONTROLLER, RandomBeast()))


class UNG_917:
    """Dinomancy / 恐龙学
    将你的英雄技能替换为“使一只野兽获得+3/+3”。"""

    play = Summon(CONTROLLER, "UNG_917t1")


class UNG_917t1:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    activate = Buff(TARGET, "UNG_917e")


UNG_917e = buff(+3, +3)


class UNG_920:
    """The Marsh Queen / 湿地女王
    任务：使用七张法力值消耗为（1）的随从牌。 奖励：卡纳莎女王。"""

    progress_total = 7
    quest = Play(CONTROLLER, MINION + (COST == 1)).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_920t1")


class UNG_920t1:
    play = Shuffle(CONTROLLER, "UNG_920t2") * 15


class UNG_920t2:
    play = Draw(CONTROLLER)
