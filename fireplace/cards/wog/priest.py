from ..utils import *


##
# Minions


class OG_096:
    """Twilight Darkmender / 暮光暗愈者
    战吼：如果你的克苏恩至少有10点攻击力，便为你的英雄恢复#10点生命值。"""

    play = CHECK_CTHUN & Heal(FRIENDLY_HERO, 10)


class OG_334:
    """Hooded Acolyte / 兜帽侍僧
    嘲讽。每当一个角色获得治疗时，使你的克苏恩获得+1/+1（无论它在哪里）。"""

    events = Heal(ALL_CHARACTERS).on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


class OG_234:
    """Darkshire Alchemist / 夜色镇炼金师
    战吼： 恢复#5点生命值。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Heal(TARGET, 5)


class OG_335:
    """Shifting Shade / 变幻之影
    亡语：复制你对手的牌库中的一张牌，并将其置入你的手牌。"""

    deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class OG_316:
    """Herald Volazj / 传令官沃拉兹
    战吼：召唤所有其他友方随从的复制，他们均为1/1。"""

    play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS - SELF)).then(
        Buff(Summon.CARD, "OG_316k")
    )


class OG_316k:
    atk = SET(1)
    max_health = SET(1)


##
# Spells


class OG_104:
    """Embrace the Shadow / 暗影之握
    在本回合中，你的治疗效果转而造成等量的伤害。"""

    play = Buff(CONTROLLER, "OG_104e")


class OG_104e:
    update = Refresh(
        CONTROLLER,
        {
            GameTag.EMBRACE_THE_SHADOW: True,
        },
    )


class OG_094:
    """Power Word: Tentacles / 真言术：触
    使一个随从获得+2/+6。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "OG_094e")


OG_094e = buff(+2, +6)


class OG_100:
    """Shadow Word: Horror / 暗言术：骇
    消灭所有攻击力小于或等于2的随从。"""

    play = Destroy(ALL_MINIONS + (ATK <= 2))


class OG_101:
    """Forbidden Shaping / 禁忌畸变
    消耗你所有的法力值，随机 召唤一个法力值消耗相同的随从。"""

    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
        Summon(CONTROLLER, RandomMinion(cost=SpendMana.AMOUNT))
    )
