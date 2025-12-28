from ..utils import *


##
# Minions


class OG_173:
    """Blood of The Ancient One / 远古造物之血
    在你的回合结束时，如果你控制两个远古造物之血，则将其融合成远古造物。"""

    events = OWN_TURN_END.on(
        Dead(SELF)
        | (
            Find(FRIENDLY_MINIONS - SELF + ID("OG_173"))
            & (
                Destroy(SELF),
                Destroy((FRIENDLY_MINIONS - SELF + ID("OG_173"))[:1]),
                Deaths(),
                Summon(CONTROLLER, "OG_173a"),
            )
        )
    )


class OG_200:
    """Validated Doomsayer / 末日践行者
    在你的回合开始时，将本随从的攻击力 变为7。"""

    events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_200e"))


class OG_200e:
    """Doom Free"""

    atk = SET(7)


class OG_271:
    """Scaled Nightmare / 梦魇之龙
    在你的回合开始时，本随从的攻击力 翻倍。"""

    events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_271e"))


class OG_271e:
    atk = lambda self, i: i * 2


class OG_272:
    """Twilight Summoner / 暮光召唤师
    亡语：召唤一个5/5的无面破坏者。"""

    deathrattle = Summon(CONTROLLER, "OG_272t")


class OG_290:
    """Ancient Harbinger / 上古之神先驱
    在你的回合开始时，将一个法力值消耗为（10）的随从从你的牌库置入你的手牌。"""

    events = OWN_TURN_BEGIN.on(ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 10))))


class OG_337:
    """Cyclopian Horror / 巨型独眼怪
    嘲讽，战吼：每有一个敌方随从，便获得+1生命值。"""

    play = Buff(SELF, "OG_337e") * Count(ENEMY_MINIONS)


OG_337e = buff(health=1)


class OG_102:
    """Darkspeaker / 黑暗低语者
    战吼：与另一个友方随从交换属性值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = SwapStateBuff(TARGET, SELF, "OG_102e")


class OG_102e:
    atk = lambda self, i: self._xatk
    max_health = lambda self, i: self._xhealth


class OG_174:
    """Faceless Shambler / 无面蹒跚者
    嘲讽，战吼：复制一个友方随从的攻击力和生命值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = CopyStateBuff(TARGET, "OG_174e")


class OG_174e:
    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


class OG_321:
    """Crazed Worshipper / 疯狂的信徒
    嘲讽。每当本随从受到伤害，使你的克苏恩获得+1/+1（无论它在哪里）。"""

    events = SELF_DAMAGE.on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))
