from ..utils import *


##
# Minions


class BOT_224:
    """Doubling Imp / 双生小鬼
    战吼：召唤一个本随从的复制。"""

    # <b>Battlecry:</b> Summon a copy of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class BOT_226:
    """Nethersoul Buster / 虚魂破坏者
    战吼：在本回合中，你的英雄每受到一点伤害，便获得+1攻击力。"""

    # <b>Battlecry:</b> Gain +1 Attack for each damage your hero has taken this turn.
    play = Buff(SELF, "BOT_226e") * DAMAGED_THIS_TURN(FRIENDLY_HERO)


BOT_226e = buff(atk=1)


class BOT_433:
    """Dr. Morrigan / 莫瑞甘博士
    亡语： 将本随从与你牌库中的一个随从互换。"""

    # <b>Deathrattle:</b> Swap this with a minion from your deck.
    deathrattle = Swap(SELF, RANDOM(FRIENDLY_DECK + MINION))


class BOT_443:
    """Void Analyst / 虚空分析师
    亡语：使你手牌中的所有恶魔牌获得+1/+1。"""

    # <b>Deathrattle:</b> Give all Demons in your hand +1/+1.
    deathrattle = Buff(FRIENDLY_HAND + DEMON, "BOT_443e")


BOT_443e = buff(+1, +1)


class BOT_536:
    """Omega Agent / 欧米茄探员
    战吼：如果你有十个法力水晶，召唤本随从的两个复制。"""

    # [x]<b>Battlecry:</b> If you have 10 Mana Crystals, summon _2 copies of this minion.
    powered_up = AT_MAX_MANA(CONTROLLER)
    play = powered_up & SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 2


##
# Spells


class BOT_222:
    """Spirit Bomb / 灵魂炸弹
    对一个随从和你的英雄各造成$4点伤害。"""

    # Deal $4 damage to a minion and your hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), Hit(FRIENDLY_HERO, 4)


class BOT_263:
    """Soul Infusion / 灵魂灌注
    使你手牌中最左边的随从牌获得+2/+2。"""

    # Give the left-most minion in your hand +2/+2.
    play = Buff((FRIENDLY_HAND + MINION)[:1], "BOT_263e")


BOT_263e = buff(+2, +2)


class BOT_521:
    """Ectomancy / 炼魂术
    召唤你控制的所有恶魔的复制。"""

    # Summon copies of all Demons you control.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + DEMON))


class BOT_568:
    """The Soularium / 莫瑞甘的灵界
    抽三张牌。这些牌为临时牌。"""

    # Draw 3 cards. At the end of your turn, discard them.
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "BOT_568e")) * 3


class BOT_568e:
    class Hand:
        events = OWN_TURN_END.on(Discard(OWNER))

    events = REMOVED_IN_PLAY


class BOT_913:
    """Demonic Project / 恶魔计划
    随机将每个玩家手牌中的一张随从牌变形成为一张 恶魔牌。"""

    # Each player transforms a random minion in their hand into a Demon.
    play = (
        Morph(RANDOM(FRIENDLY_HAND + MINION), RandomDemon()),
        Morph(RANDOM(ENEMY_HAND + MINION), RandomDemon()),
    )
