"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_042:
    """Primordial Protector - 始生保护者
    Battlecry: Draw your highest Cost spell. Summon a random minion with the same Cost.
    战吼：抽你牌库中法力值消耗最高的法术牌。召唤一个法力值消耗相同的随从。
    """
    def play(self):
        # 抽取费用最高的法术牌
        cards = yield ForceDraw(CONTROLLER, TOP(FRIENDLY_DECK + SPELL, COST))
        if cards:
            for card in cards:
                if card:
                    # 召唤一个相同费用的随机随从
                    yield Summon(CONTROLLER, RandomMinion(cost=card.cost))


class BAR_073:
    """Barrens Blacksmith - 贫瘠之地铁匠
    Frenzy: Give your other minions +2/+2.
    暴怒：使你的其他随从获得+2/+2。
    """
    frenzy = Buff(FRIENDLY_MINIONS - SELF, "BAR_073e")


class BAR_073e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class BAR_075:
    """Crossroads Watch Post - 十字路口哨所
    Can't attack. Whenever your opponent casts a spell, give your minions +1/+1.
    无法攻击。每当你的对手施放一个法术时，使你的随从获得+1/+1。
    """
    events = Play(OPPONENT, SPELL).after(
        Buff(FRIENDLY_MINIONS, "BAR_075e")
    )


class BAR_075e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_081:
    """Southsea Scoundrel - 南海恶徒
    Battlecry: Discover a card in your opponent's deck. They draw theirs as well.
    战吼：从你对手的牌库中发现一张牌。对手也会抽到他们的那张牌。
    """
    play = DISCOVER(ENEMY_DECK).then(
        Give(CONTROLLER, Copy(Discover.CARD)),
        ForceDraw(Discover.CARD),
    )


class BAR_744:
    """Spirit Healer - 灵魂医者
    After you cast a Holy spell, give a random friendly minion +2 Health.
    在你施放一个神圣法术后，随机使一个友方随从获得+2生命值。
    """
    events = Play(CONTROLLER, SPELL + HOLY).after(
        Buff(RANDOM_FRIENDLY_MINION, "BAR_744e")
    )


class BAR_744e:
    tags = {
        GameTag.HEALTH: 2,
    }


