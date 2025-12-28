from ..utils import *


##
# Minions


class DAL_185:
    """Aranasi Broodmother / 阿兰纳丝蛛后
    嘲讽 当你抽到该牌时，为你的英雄恢复#4点生命值。"""

    # [x]<b>Taunt</b> When you draw this, restore #4 Health to your hero.
    draw = Heal(FRIENDLY_HERO, 4)


class DAL_422:
    """Arch-Villain Rafaam / 至尊盗王拉法姆
    嘲讽 战吼：将你的手牌和牌库里的卡牌替换为传说随从。"""

    # <b><b>Taunt</b> Battlecry:</b> Replace your hand and deck with <b>Legendary</b>
    # minions.
    play = Morph(FRIENDLY_HAND + FRIENDLY_DECK, RandomLegendaryMinion())


class DAL_561:
    """Jumbo Imp / 巨型小鬼
    当本牌在你的手牌中时，每当一个友方恶魔死亡，法力值消耗便减少（1）点。"""

    # Costs (1) less whenever a friendly Demon dies while this is in your hand.
    class Hand:
        events = Death(FRIENDLY + DEMON).on(Buff(SELF, "DAL_561e"))


class DAL_561e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class DAL_563:
    """Eager Underling / 性急的杂兵
    亡语：随机使两个友方随从获得+2/+2。"""

    # <b>Deathrattle:</b> Give two random friendly minions +2/+2.
    deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION * 2, "DAL_563e")


DAL_563e = buff(+2, +2)


class DAL_606:
    """EVIL Genius / 怪盗天才
    战吼：消灭一个友方随从，随机将两张跟班牌置入你的手牌。"""

    # <b>Battlecry:</b> Destroy a friendly minion to add 2 random
    # <b>Lackeys</b>_to_your_hand.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Give(CONTROLLER, RandomLackey()) * 2


class DAL_607:
    """Fel Lord Betrug / 邪能领主贝图格
    每当你抽到一张随从牌，召唤一个它的复制。该复制具有突袭，并会在回合结束时死亡。"""

    # [x]Whenever you draw a minion, summon a copy with <b>Rush</b> that dies at end of
    # turn.
    events = Draw(CONTROLLER, MINION).on(
        Summon(CONTROLLER, Copy(Draw.CARD)).then(Buff(Summon.CARD, "DAL_607e"))
    )


class DAL_607e:
    tags = {GameTag.RUSH: True}
    events = OWN_TURN_END.on(Destroy(OWNER))


##
# Spells


class DAL_007(SchemeUtils):
    """Rafaam's Scheme"""

    # Summon @ 1/1 |4(Imp, Imps). <i>(Upgrades each turn!)</i>
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "DAL_751t") * (Attr(SELF, GameTag.QUEST_PROGRESS) + 1)


class DAL_173:
    """Darkest Hour / 至暗时刻
    消灭所有友方随从。每消灭一个随从，便随机从你的牌库中召唤一个随从。"""

    # Destroy all friendly minions. For each one, summon a random minion from your deck.
    play = Destroy(FRIENDLY_MINIONS).then(
        Deaths(), Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
    )


class DAL_602:
    """Plot Twist / 情势反转
    将你的手牌洗入牌库。抽取相同数量的牌。"""

    # Shuffle your hand into your deck. Draw that many cards.
    def play(self):
        count = len(self.controller.hand)
        yield Shuffle(CONTROLLER, FRIENDLY_HAND)
        yield Draw(CONTROLLER) * count


class DAL_605:
    """Impferno / 小鬼狱火
    使你的恶魔获得+1攻击力。对所有敌方随从造成$1点 伤害。"""

    # Give your Demons +1 Attack. Deal $1 damage to all enemy minions.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 15,
    }
    play = Buff(FRIENDLY_MINIONS + DEMON, "DAL_605e"), Hit(ENEMY_MINIONS, 1)


DAL_605e = buff(atk=1)
