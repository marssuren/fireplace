from ..utils import *


##
# Minions


class BT_126:
    """Teron Gorefiend / 塔隆·血魔
    战吼：消灭所有其他友方随从。亡语：再次召唤被消灭的随从并使其获得+1/+1。"""

    # [x]<b>Battlecry:</b> Destroy all other friendly minions.
    # <b>Deathrattle:</b> Resummon them with +1/+1.
    play = Destroy(FRIENDLY_MINIONS - SELF).then(
        StoringBuff(SELF, "BT_126e", Destroy.TARGET)
    )


class BT_126e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, STORE_CARD).then(Buff(Summon.CARD, "BT_126e2"))


BT_126e2 = buff(+1, +1)


class BT_255:
    """Kael'thas Sunstrider / 凯尔萨斯·逐日者
    在每回合中，你每施放三个法术，第三个法术的法力值消耗为（1）点。"""

    # Every third spell you cast each turn costs (1).
    update = (Count(CARDS_PLAYED_THIS_TURN + SPELL) % 3 == 2) & (
        Refresh(FRIENDLY_HAND + SPELL, buff="BT_255e")
    )


class BT_255e:
    cost = SET(1)


class BT_735:
    """Al'ar / 奥
    亡语：召唤一个0/3的可以在你的下个回合 复活本随从的“奥的灰烬”。"""

    # <b>Deathrattle</b>: Summon a 0/3 Ashes of Al'ar that resurrects this
    # minion on your next turn.
    deathrattle = Summon(CONTROLLER, "BT_735t")


class BT_735t:
    """Ashes of Al'ar"""

    # At the start of your turn, transform this into Al'ar.
    events = OWN_TURN_BEGIN.on(Morph(SELF, "BT_735"))


class BT_737:
    """Maiev Shadowsong / 玛维·影歌
    战吼： 选择一个随从。使其休眠2回合。"""

    # <b>Battlecry:</b> Choose a minion. It goes <b>Dormant</b> for 2 turns.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Dormant(TARGET, 2)


class BT_850:
    """Magtheridon / 玛瑟里顿
    休眠。 战吼：为你的对手召唤三个1/3的典狱官。当她们死亡时，消灭所有随从并唤醒。"""

    # [x]<b>Dormant</b>. <b>Battlecry:</b> Summon three 1/3 enemy Warders. When
    # they die, destroy all minions and awaken.
    tags = {GameTag.DORMANT: True}
    progress_total = 3
    play = Summon(OPPONENT, "BT_850t") * 3
    dormant_events = Death(ENEMY_MINIONS + ID("BT_850t")).on(
        AddProgress(SELF, Death.ENTITY)
    )
    reward = Awaken(SELF)
    awaken = Destroy(ALL_MINIONS - SELF)
