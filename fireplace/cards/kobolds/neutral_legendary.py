from ..utils import *


##
# Minions


class LOOT_357:
    """Marin the Fox / “老狐狸”马林
    战吼：为你的对手召唤一个0/8的宝箱。（打破宝箱可以获得惊人的战利品！）"""

    # <b>Battlecry:</b> Summon a 0/8 Treasure Chest for your opponent. <i>(Break it for
    # awesome loot!)</i>
    play = Summon(OPPONENT, "LOOT_357l")


class LOOT_357l:
    entourage = ["LOOT_998h", "LOOT_998j", "LOOT_998l", "LOOT_998k"]
    deathrattle = Give(OPPONENT, RandomEntourage())


class LOOT_998h:
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Draw(CONTROLLER).then(
        Give(CONTROLLER, Copy(Draw.CARD))
        * (MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND))
    )


class LOOT_998j:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Discover(CONTROLLER, RandomLegendaryMinion()).then(
        Summon(CONTROLLER, Discover.CARD) * 2
    )


class LOOT_998l:
    play = (Draw(CONTROLLER) * 3).then(Buff(Draw.CARD, "LOOT_998le"))


class LOOT_998le:
    cost = SET(0)
    events = REMOVED_IN_PLAY


class LOOT_998k:
    play = Morph(FRIENDLY_HAND, RandomLegendaryMinion())


class LOOT_516:
    """Zola the Gorgon / 蛇发女妖佐拉
    战吼：选择一个友方随从。将它的金色复制置入你的手牌。"""

    # <b>Battlecry:</b> Choose a friendly minion. Add a Golden copy of it to your hand.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Give(CONTROLLER, Copy(TARGET))


class LOOT_521:
    """Master Oakheart / 欧克哈特大师
    战吼： 招募攻击力为1，2，3的随从各一个。"""

    # <b>Battlecry:</b> <b>Recruit</b> a 1, 2, and 3-Attack minion.
    play = Recruit(COST == 1), Recruit(COST == 2), Recruit(COST == 3)


class LOOT_526:
    """The Darkness / 黑暗之主
    起始休眠状态。 战吼：将三张蜡烛牌洗入对手的牌库。抽到三张蜡烛牌后唤醒本随从。"""

    # [x]Starts dormant. <b>Battlecry:</b> Shuffle 3 Candles into the enemy deck. When
    # drawn, this awakens.
    tags = {GameTag.DORMANT: True}
    progress_total = 3
    play = Shuffle(CONTROLLER, "LOOT_526t") * 3
    reward = Awaken(SELF)


class LOOT_526t:
    draw = CAST_WHEN_DRAWN
    play = AddProgress(FuncSelector(lambda entities, source: [source.creator]), SELF)


class LOOT_541:
    """King Togwaggle / 托瓦格尔国王
    战吼：与你的对手交换牌库。你的对手获得一张“赎金”法术牌，可以将牌库交换回来。"""

    # [x]<b>Battlecry:</b> Swap decks with your opponent. Give them a Ransom spell to swap
    # back.
    def play(self):
        controller = self.controller
        opponent = self.controller.opponent
        controller_deck = controller.deck
        opponent_deck = opponent.deck
        controller.deck = opponent_deck
        opponent.deck = controller_deck
        for card in controller.deck:
            card.controller = controller
        for card in opponent.deck:
            card.controller = opponent
        yield Give(OPPONENT, "LOOT_541t")


class LOOT_541t:
    def play(self):
        controller = self.controller
        opponent = self.controller.opponent
        controller_deck = controller.deck
        opponent_deck = opponent.deck
        controller.deck = opponent_deck
        opponent.deck = controller_deck
        for card in controller.deck:
            card.controller = controller
        for card in opponent.deck:
            card.controller = opponent
        yield Give(OPPONENT, "LOOT_541t")
