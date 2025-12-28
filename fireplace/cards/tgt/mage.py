from ..utils import *


##
# Minions


class AT_006:
    """Dalaran Aspirant / 达拉然铁骑士
    法术伤害+1 激励：获得法术伤害+1。"""

    inspire = Buff(SELF, "AT_006e")


AT_006e = buff(spellpower=1)


class AT_007:
    """Spellslinger / 嗜法者
    战吼：双方玩家各获取一张随机法术牌，你获取的那张法力值消耗减少（2）点。"""

    play = Give(ALL_PLAYERS, RandomSpell())


class AT_008:
    """Coldarra Drake / 考达拉幼龙
    你可以使用任意次数的英雄技能。"""

    update = Refresh(
        FRIENDLY_HERO_POWER, {GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: SET(-1)}
    )


class AT_009:
    """Rhonin / 罗宁
    亡语：将三张奥术飞弹置入你的手牌。"""

    deathrattle = Give(CONTROLLER, "EX1_277") * 3


##
# Spells


class AT_001:
    """Flame Lance / 炎枪术
    对一个随从造成$25点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 8)


class AT_004:
    """Arcane Blast / 奥术冲击
    对一个随从造成$2点伤害。该法术受到的法术伤害增益效果翻倍。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2)


class AT_005:
    """Polymorph: Boar / 变形术：野猪
    使一个随从变形成为一个4/2并具有冲锋的野猪。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Morph(TARGET, "AT_005t")


##
# Secrets


class AT_002:
    """Effigy / 轮回
    奥秘：当一个友方随从死亡时，随机召唤一个法力值消耗相同的随从。"""

    secret = Death(FRIENDLY + MINION).on(
        FULL_BOARD
        | (Reveal(SELF), Summon(CONTROLLER, RandomMinion(cost=COST(Death.ENTITY))))
    )
