from ..utils import *


##
# Laykeys


class DAL_613:
    """Faceless Lackey / 无面跟班
    战吼：随机召唤一个法力值消耗为（2）的随从。"""

    # <b>Battlecry:</b> Summon a random 2-Cost minion.
    play = Summon(CONTROLLER, RandomMinion(cost=2))


class DAL_614:
    """Kobold Lackey / 狗头人跟班
    战吼：造成2点伤害。"""

    # <b>Battlecry:</b> Deal 2 damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)


class DAL_615:
    """Witchy Lackey / 女巫跟班
    战吼：将一个友方随从变形成为一个法力值消耗增加（1）点的随从。"""

    # <b>Battlecry:</b> Transform a friendly minion into one that costs (1) more.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Evolve(TARGET, 1)


class DAL_739:
    """Goblin Lackey / 地精跟班
    战吼： 使一个友方随从获得+1攻击力和突袭。"""

    # <b>Battlecry:</b> Give a friendly minion +1 Attack and_<b>Rush</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "DAL_739e")


DAL_739e = buff(atk=1, rush=True)


class DAL_741:
    """Ethereal Lackey / 虚灵跟班
    战吼： 发现一张法术牌。"""

    # <b>Battlecry:</b> <b>Discover</b> a spell.
    play = DISCOVER(RandomSpell())


class ULD_616:
    """Titanic Lackey / 泰坦造物跟班
    战吼：使一个友方随从获得+2生命值和 嘲讽。"""

    # <b>Battlecry:</b> Give a friendly minion +2 Health and_<b>Taunt</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "ULD_616e")


ULD_616e = buff(health=2, taunt=True)


class DRG_052:
    """Draconic Lackey / 龙族跟班
    战吼： 发现一张龙牌。"""

    # <b>Battlecry:</b> <b>Discover</b> a Dragon.
    play = DISCOVER(RandomDragon())
