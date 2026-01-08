from ..utils import *


##
# Minions


class OG_006:
    """Vilefin Inquisitor / 恶鳍审判者
    战吼： 你的英雄技能变为“召唤一个1/1的鱼人”。"""

    play = Summon(CONTROLLER, "OG_006b")


class OG_006b:
    """The Tidal Hand"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "OG_006a")


class OG_221:
    """Selfless Hero / 无私的英雄
    亡语：随机使一个友方随从获得圣盾。"""

    deathrattle = GiveDivineShield(RANDOM_FRIENDLY_MINION)


class OG_229:
    """Ragnaros, Lightlord / 光耀之主拉格纳罗斯
    在你的回合结束时，为一个受伤的友方角色恢复#8点生命值。"""

    events = OWN_TURN_END.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 8))


class OG_310:
    """Steward of Darkshire / 夜色镇执法官
    每当你召唤一个生命值为1的随从，便使其获得圣盾。"""

    events = Summon(CONTROLLER, MINION + (CURRENT_HEALTH == 1)).on(
        GiveDivineShield(Summon.CARD)
    )


##
# Spells


class OG_223:
    """Divine Strength / 神圣之力
    使一个随从获得+1/+2。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "OG_223e")


OG_223e = buff(+1, +2)


class OG_273:
    """Stand Against Darkness / 惩黑除恶
    召唤五个1/1的白银之手新兵。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "CS2_101t") * 5


class OG_311:
    """A Light in the Darkness / 黑暗曙光
    发现一张圣骑士随从牌。使其获得+2/+2。"""

    play = Discover(CONTROLLER, RandomMinion()).then(
        Give(CONTROLLER, Discover.CARD), Buff(Discover.CARD, "OG_311e")
    )


OG_311e = buff(+2, +2)


##
# Weapons


class OG_222:
    """Rallying Blade / 集结之刃
    战吼：使你具有圣盾的随从获得+1/+1。"""

    play = Buff(FRIENDLY_MINIONS + DIVINE_SHIELD, "OG_222e")


OG_222e = buff(+1, +1)


class OG_198:
    """Forbidden Healing / 禁忌治疗
    消耗你所有的法力值，恢复等同于所消耗法力值数量两倍的生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
        Heal(TARGET, SpendMana.AMOUNT * 2)
    )
