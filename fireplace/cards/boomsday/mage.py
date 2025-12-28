from ..utils import *


##
# Minions


class BOT_103:
    """Stargazer Luna / 观星者露娜
    在你使用最右边的一张手牌后，抽 一张牌。"""

    # After you play the right-most card in your hand, draw a card.
    events = Play(CONTROLLER, PLAY_RIGHT_MOST).after(Draw(CONTROLLER))


class BOT_256:
    """Astromancer / 星术师
    战吼：随机召唤一个法力值消耗等同于你手牌数量的随从。"""

    # [x]<b>Battlecry:</b> Summon a random minion with Cost equal to your hand size.
    play = Summon(CONTROLLER, RandomMinion(cost=Count(FRIENDLY_HAND)))


class BOT_531:
    """Celestial Emissary / 星界密使
    战吼：在本回合中，你的下一个法术拥有法术伤害+2。"""

    # <b>Battlecry:</b> Your next spell_this turn has <b>Spell_Damage +2</b>.
    play = Buff(CONTROLLER, "BOT_531e")


class BOT_531e:
    update = Refresh(CONTROLLER, {GameTag.SPELLPOWER: 2})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class BOT_601:
    """Meteorologist / 气象学家
    战吼：你每有一张手牌，便随机对一个敌人造成1点伤害。"""

    # <b>Battlecry:</b> For each card in your hand, deal 1 damage to a random enemy.
    play = Hit(RANDOM_ENEMY_MINION, 1) * Count(FRIENDLY_HAND)


##
# Spells


class BOT_101:
    """Astral Rift / 星界裂隙
    随机将两张随从牌置入你的 手牌。"""

    # Add 2 random minions to your hand.
    play = Give(CONTROLLER, RandomMinion()) * 2


class BOT_254:
    """Unexpected Results / 鲁莽试验
    随机召唤两个法力值消耗为（$2）的随从（受法术伤害加成影响）。"""

    # [x]Summon two random $2-Cost minions <i>(improved by <b>Spell Damage</b>)</i>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RandomMinion(cost=SPELL_DAMAGE(2))) * 2


class BOT_257:
    """Luna's Pocket Galaxy / 露娜的口袋银河
    使你牌库中所有随从牌的法力值消耗变为（1）点。"""

    # Change the Cost of minions in your deck to (1).
    play = Buff(FRIENDLY_DECK + MINION, "BOT_257e")


class BOT_257e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class BOT_453:
    """Shooting Star / 迸射流星
    对一个随从及其相邻的随从造成$1点伤害。"""

    # Deal $1 damage to a minion and the minions next to it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Hit(TARGET_ADJACENT, 1)


class BOT_600:
    """Research Project / 研发计划
    每个玩家抽两张牌。"""

    # Each player draws 2_cards.
    play = Draw(PLAYER) * 2
