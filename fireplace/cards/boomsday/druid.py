from ..utils import *


##
# Minions


class BOT_419:
    """Dendrologist / 树木学家
    战吼：如果你控制一个树人，发现一张法术牌。"""

    # <b>Battlecry:</b> If you control a Treant, <b>Discover</b> a spell.
    play = Find(FRIENDLY_MINIONS + TREANT) & DISCOVER(RandomSpell())


class BOT_422:
    """Tending Tauren / 牛头人园丁
    抉择： 使你的所有其他随从获得+1/+1；或者召唤两个2/2的树人。"""

    # [x]<b>Choose One -</b> Give your other minions +1/+1; or Summon two 2/2 Treants.
    choose = ("BOT_422a", "BOT_422b")
    play = ChooseBoth(CONTROLLER) & (
        SummonBothSides(CONTROLLER, "EX1_158t") * 2,
        Buff(FRIENDLY_MINIONS - SELF, "BOT_422ae"),
    )


class BOT_422a:
    play = Buff(FRIENDLY_MINIONS - SELF, "BOT_422ae")


BOT_422ae = buff(+1, +1)


class BOT_422b:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 2,
    }
    play = SummonBothSides(CONTROLLER, "EX1_158t") * 2


class BOT_423:
    """Dreampetal Florist / 梦境花栽种师
    在你的回合结束时，随机使你手牌中一张随从牌的法力值消耗减少（7）点。"""

    # At the end of your turn, reduce the Cost of a random minion in your hand by (7).
    events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_HAND + MINION), "BOT_423e"))


class BOT_423e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -7}


class BOT_434:
    """Flobbidinous Floop / 软泥教授弗洛普
    此牌在你的手牌中时，会变成你使用的上一张随从牌的3/4复制。"""

    # While in your hand, this is a 3/4 copy of the last minion you played.
    class Hand:
        events = Play(CONTROLLER, MINION).after(
            Morph(SELF, Copy(Play.CARD)).then(Buff(Morph.CARD, "BOT_434e"))
        )


class BOT_434e:
    class Hand:
        events = Play(CONTROLLER).after(
            Morph(OWNER, Copy(Play.CARD)).then(Buff(Morph.CARD, "BOT_434e"))
        )


class BOT_507:
    """Gloop Sprayer / 黏液喷射者
    战吼： 为相邻的随从各召唤一个复制。"""

    # <b>Battlecry:</b> Summon a copy of each adjacent minion.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(SELF_ADJACENT))


class BOT_523:
    """Mulchmuncher / 植被破碎机
    突袭 在本局对战中，每有一个友方树人死亡，本牌的法力值消耗便减少（1）点。"""

    # <b>Rush</b>. Costs (1) less for each friendly Treant that died this game.
    cost_mod = -Count(FRIENDLY + KILLED + TREANT)


##
# Spells


class BOT_054:
    """Biology Project / 生物计划
    每个玩家获得两个法力水晶。"""

    # Each player gains 2_Mana Crystals.
    play = GainMana(PLAYER, 2)


class BOT_404:
    """Juicy Psychmelon / 香甜的灵力瓜
    从你的牌库中抽取法力值消耗为（7），（8），（9）和（10）的随从牌各一张。"""

    # Draw a 7, 8, 9, and 10-Cost minion from your deck.
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 7))),
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 8))),
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 9))),
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 10))),
    )


class BOT_420:
    """Landscaping / 植树造林
    召唤两个2/2的树人。"""

    # Summon two 2/2 Treants.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "EX1_158t") * 2


class BOT_444:
    """Floop's Glorious Gloop / 弗洛普的神奇黏液
    在本回合中，每当一个随从死亡，复原一个法力水晶。"""

    # Whenever a minion dies this turn, gain 1 Mana Crystal this turn only.
    play = Buff(CONTROLLER, "BOT_444e")


class BOT_444e:
    events = Death(MINION).on(ManaThisTurn(CONTROLLER, 1))
