from ..utils import *


##
# Minions


class AT_075:
    """Warhorse Trainer / 战马训练师
    你的白银之手新兵拥有+2攻击力和嘲讽。"""

    update = Refresh(FRIENDLY + ID("CS2_101t"), buff="AT_075e")


AT_075e = buff(atk=1)


class AT_076:
    """Murloc Knight / 鱼人骑士
    激励：随机召唤一个鱼人。"""

    inspire = Summon(CONTROLLER, RandomMurloc())


class AT_079:
    """Mysterious Challenger / 神秘挑战者
    战吼：将每种不同的奥秘从你的牌库中置入战场。"""

    play = Summon(CONTROLLER, FRIENDLY_DECK + SECRET)


class AT_081:
    """Eadric the Pure / 纯洁者耶德瑞克
    战吼：使所有敌方随从的攻击力变为1。"""

    play = Buff(ENEMY_MINIONS, "AT_081e")


class AT_081e:
    atk = SET(1)


class AT_104:
    """Tuskarr Jouster / 海象人龟骑士
    战吼：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，则为你的英雄恢复#7点生命值。"""

    play = JOUST & Heal(FRIENDLY_HERO, 7)


##
# Spells


class AT_074:
    """Seal of Champions / 英勇圣印
    使一个随从获得+3攻击力和 圣盾。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "AT_074e2"), GiveDivineShield(TARGET)


AT_074e2 = buff(atk=3)


##
# Secrets


class AT_073:
    """Competitive Spirit / 争强好胜
    奥秘：在你的回合开始时，使你的所有随从获得+1/+1。"""

    events = OWN_TURN_BEGIN.on(
        EMPTY_BOARD | (Reveal(SELF), Buff(FRIENDLY_MINIONS, "AT_073e"))
    )


AT_073e = buff(+1, +1)


class AT_078:
    """Enter the Coliseum / 精英对决
    除了每个玩家攻击力最高的随从之外，消灭所有 其他随从。"""

    play = Destroy(
        ALL_MINIONS - HIGHEST_ATK(FRIENDLY_MINIONS) - HIGHEST_ATK(ENEMY_MINIONS)
    )


##
# Weapons


class AT_077:
    """Argent Lance / 白银之枪
    战吼：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，+1耐久度。"""

    play = JOUST & Buff(SELF, "AT_077e")


AT_077e = buff(health=1)
