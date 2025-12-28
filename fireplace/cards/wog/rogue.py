from ..utils import *


##
# Minions


class OG_070:
    """Bladed Cultist / 执刃教徒
    连击：获得+1/+1。"""

    combo = Buff(SELF, "OG_070e")


OG_070e = buff(+1, +1)


class OG_080:
    """Xaril, Poisoned Mind / 毒心者夏克里尔
    战吼，亡语：随机将一张毒素牌置入你的手牌。"""

    entourage = ["OG_080d", "OG_080e", "OG_080f", "OG_080c", "OG_080b"]
    play = deathrattle = Give(CONTROLLER, RandomEntourage())


class OG_267:
    """Southsea Squidface / 南海畸变船长
    亡语：使你的武器获得+2攻击力。"""

    deathrattle = Buff(FRIENDLY_WEAPON, "OG_267e")


OG_267e = buff(atk=2)


class OG_330:
    """Undercity Huckster / 幽暗城商贩
    亡语：随机获取一张（你对手职业的）卡牌。"""

    deathrattle = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


class OG_291:
    """Shadowcaster / 暗影施法者
    战吼：选择一个友方随从，将它的一张1/1的复制置入你的手牌，其法力值消耗为（1）点。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Give(CONTROLLER, Buff(Copy(TARGET), "OG_291e"))


class OG_291e:
    atk = SET(1)
    max_health = SET(1)


class OG_282:
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(CTHUN, "OG_281e", atk=ATK(TARGET), max_health=CURRENT_HEALTH(TARGET)),
        Destroy(TARGET),
    )


##
# Spells


class OG_072:
    """Journey Below / 深渊探险
    发现一张亡语牌。"""

    play = DISCOVER(RandomCollectible(deathrattle=True))


class OG_073:
    """Thistle Tea / 菊花茶
    抽一张牌。将两张该牌的复制置入你的手牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * 2)


class OG_176:
    """Shadow Strike / 暗影打击
    对一个 未受伤的角色造成$5点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_UNDAMAGED_TARGET: 0}
    play = Hit(TARGET, 5)
