from ..utils import *


##
# Minions


class GIL_152:
    """Blackhowl Gunspire / 黑嚎炮塔
    无法攻击。每当本随从受到伤害时，随机对一个敌人造成3点 伤害。"""

    # [x]Can't attack. Whenever this minion takes damage, deal 3 damage to a random enemy.
    events = SELF_DAMAGE.on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class GIL_155:
    """Redband Wasp / 赤环蜂
    突袭 受伤时拥有+3攻 击力。"""

    # <b>Rush</b> Has +3 Attack while damaged.
    enrage = Refresh(SELF, buff="GIL_155e")


GIL_155e = buff(atk=3)


class GIL_547:
    """Darius Crowley / 达利乌斯·克罗雷
    突袭 在克罗雷攻击并消灭一个随从后，获得+2/+2。"""

    # [x]<b>Rush</b> After this attacks and kills a minion, gain +2/+2.
    events = Attack(SELF, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & Buff(SELF, "GIL_547e")
    )


GIL_547e = buff(+2, +2)


class GIL_580:
    """Town Crier / 城镇公告员
    战吼：从你的牌库中抽一张具有突袭的随从牌。"""

    # <b>Battlecry:</b> Draw a <b>Rush</b> minion from your deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + RUSH))


class GIL_655:
    """Festeroot Hulk / 腐树巨人
    在一个友方随从攻击后，获得+1攻击力。"""

    # After a friendly minion attacks, gain +1 Attack.
    events = Attack(FRIENDLY_MINIONS).after(Buff(SELF, "GIL_655e"))


GIL_655e = buff(atk=1)


class GIL_803:
    """Militia Commander / 民兵指挥官
    突袭，战吼：在本回合获得+3攻击力。"""

    # <b>Rush</b> <b>Battlecry:</b> Gain +3_Attack this turn.
    play = Buff(SELF, "GIL_803e")


GIL_803e = buff(atk=3)


##
# Spells


class GIL_537:
    """Deadly Arsenal / 致命武装
    揭示你牌库中的一张武器牌。对所有随从造成等同于其攻击力的伤害。"""

    # Reveal a weapon from your deck. Deal its Attack to all minions.
    play = Reveal(RANDOM(FRIENDLY_DECK + WEAPON)).then(
        Hit(ALL_MINIONS, ATK(Reveal.TARGET))
    )


class GIL_654:
    """Warpath / 战路
    回响 对所有随从造成 $1点伤害。"""

    # <b>Echo</b> Deal $1 damage to all_minions.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(ALL_MINIONS, 1)


##
# Weapons


class GIL_653:
    """Woodcutter's Axe / 樵夫之斧
    亡语：随机使一个友方随从获得+2/+1。"""

    # <b>Deathrattle:</b> Give +2/+1 to a random friendly minion.
    deathrattle = Buff(RANDOM_FRIENDLY_MINION, "GIL_653e")


GIL_653e = buff(+2, +1)
