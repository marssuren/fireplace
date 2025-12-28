from ..utils import *


##
# Minions


class BOT_066:
    """Mechanical Whelp / 机械雏龙
    亡语：召唤一个7/7的机械巨龙。"""

    # <b>Deathrattle:</b> Summon a 7/7 Mechanical Dragon.
    deathrattle = Summon(CONTROLLER, "BOT_066t")


class BOT_098:
    """Unpowered Mauler / 没电的铁皮人
    在本回合中，除非你施放过法术，否则无法进行攻击。"""

    # Can only attack if you cast a spell this turn.
    update = Find(CARDS_PLAYED_THIS_TURN + SPELL) | Refresh(
        SELF, {GameTag.CANT_ATTACK: True}
    )


class BOT_102:
    """Spark Drill / 火花钻机
    突袭，亡语：将两张1/1并具有突袭的“火花”置入你的手牌。"""

    # <b>Rush</b> <b>Deathrattle:</b> Add two 1/1 Sparks with <b>Rush</b> to your hand.
    deathrattle = Give(CONTROLLER, "BOT_102t") * 2


class BOT_107:
    """Missile Launcher / 飞弹机器人
    磁力 在你的回合结束时，对所有其他角色造成1点伤害。"""

    # [x]<b>Magnetic</b> At the end of your turn, deal 1 damage to all other characters.
    magnetic = MAGNETIC("BOT_107e")
    events = OWN_TURN_END.on(Hit(ALL_CHARACTERS - SELF, 1))


class BOT_107e:
    events = OWN_TURN_END.on(Hit(ALL_CHARACTERS - OWNER, 1))


class BOT_270:
    """Giggling Inventor / 欢乐的发明家
    战吼：召唤两个1/2并具有嘲讽和圣盾的 机械。"""

    # <b>Battlecry:</b> Summon two 1/2 Mechs with <b>Taunt</b> and_<b>Divine Shield</b>.
    play = SummonBothSides(CONTROLLER, "BOT_270t") * 2


class BOT_312:
    """Replicating Menace / 量产型恐吓机
    磁力 亡语：召唤三个1/1的微型机器人。"""

    # <b>Magnetic</b> <b>Deathrattle:</b> Summon three 1/1 Microbots.
    magnetic = MAGNETIC("BOT_312e")
    deathrattle = Summon(CONTROLLER, "BOT_312t") * 3


class BOT_312e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "BOT_312t") * 3


class BOT_538:
    """Spark Engine / 火花引擎
    战吼：将一张1/1并具有突袭的“火花”置入你的手牌。"""

    # <b>Battlecry:</b> Add a 1/1 Spark with <b>Rush</b> to_your hand.
    play = Give(CONTROLLER, "BOT_102t")


class BOT_539:
    """Arcane Dynamo / 奥能水母
    战吼：发现一张法力值消耗大于或等于（5）点的法术牌。"""

    # <b>Battlecry:</b> <b>Discover</b> a spell that costs (5) or more.
    play = DISCOVER(RandomSpell(cost=range(5, 100)))


class BOT_907:
    """Galvanizer / 通电机器人
    战吼：使你手牌中所有机械牌的法力值消耗减少（1）点。"""

    # [x]<b>Battlecry:</b> Reduce the Cost of Mechs in your hand by (1).
    play = Buff(FRIENDLY_HAND + MECH, "BOT_907e")


class BOT_907e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}
