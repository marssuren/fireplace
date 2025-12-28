from ..utils import *


##
# Minions


class UNG_201:
    """Primalfin Totem / 蛮鱼图腾
    在你的回合结束时，召唤一个1/1的鱼人。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "UNG_201t"))


class UNG_202:
    """Fire Plume Harbinger / 火羽先锋
    战吼：使你手牌中所有元素牌的法力值消耗减少（1）点。"""

    play = Buff(FRIENDLY_HAND + ELEMENTAL, "GBL_003e")


class UNG_208:
    """Stone Sentinel / 岩石哨兵
    战吼：如果你在上个回合使用过元素牌，则召唤两个2/3并具有嘲讽的元素。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = ELEMENTAL_PLAYED_LAST_TURN & (SummonBothSides(CONTROLLER, "UNG_208t") * 2)


class UNG_211:
    """Kalimos, Primal Lord / 荒蛮之主卡利莫斯
    战吼：如果你在上个回合使用过元素牌，则施放一个元素祈咒。"""

    play = ELEMENTAL_PLAYED_LAST_TURN & Choice(
        CONTROLLER, ["UNG_211a", "UNG_211b", "UNG_211c", "UNG_211d"]
    ).then(Battlecry(Choice.CARD, None))


class UNG_211a:
    play = (Summon(CONTROLLER, "UNG_211aa") * 7,)


class UNG_211b:
    play = (Heal(FRIENDLY_HERO, 12),)


class UNG_211c:
    play = (Hit(ENEMY_HERO, 6),)


class UNG_211d:
    play = (Hit(ENEMY_MINIONS, 3),)


class UNG_938:
    """Hot Spring Guardian / 温泉守卫
    嘲讽，战吼： 恢复#3点生命值。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Heal(TARGET, 3)


##
# Spells


class UNG_025:
    """Volcano / 火山喷发
    造成$15点伤害，随机分配到所有随从身上。 过载：（1）"""

    play = Hit(RANDOM_MINION, 1) * SPELL_DAMAGE(15)


class UNG_817:
    """Tidal Surge / 海潮涌动
    吸血 对一个随从造成$5点伤害。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4), Heal(FRIENDLY_HERO, 4)


class UNG_942:
    """Unite the Murlocs / 鱼人总动员
    任务：召唤8个鱼人。 奖励：老鲨嘴。"""

    progress_total = 10
    quest = Summon(CONTROLLER, MURLOC).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_942t")


class UNG_942t:
    play = Give(CONTROLLER, RandomMurloc()) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class UNG_956:
    """Spirit Echo / 灵魂回响
    使你的所有随从获得“亡语：将本随从移回你的手牌”。"""

    play = Buff(FRIENDLY_MINIONS, "UNG_956e")


class UNG_956e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, Copy(OWNER))
