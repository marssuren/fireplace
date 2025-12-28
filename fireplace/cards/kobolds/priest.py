from ..utils import *


##
# Minions


class LOOT_410:
    """Duskbreaker / 破晓之龙
    战吼： 如果你的手牌中有龙牌，则对所有其他随从造成3点伤害。"""

    # <b>Battlecry:</b> If you're holding a Dragon, deal 3 damage to all other minions.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = HOLDING_DRAGON & Hit(ALL_MINIONS - SELF, 3)


class LOOT_528:
    """Twilight Acolyte / 暮光侍僧
    战吼：如果你的手牌中有龙牌，则将本随从的攻击力与另一个随从交换。"""

    # <b>Battlecry:</b> If you're holding a Dragon, swap this minion's Attack with another
    # minion's.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0,
    }
    play = HOLDING_DRAGON & SwapStateBuff(TARGET, SELF, "LOOT_528e")


class LOOT_528e:
    atk = lambda self, i: self._xatk


class LOOT_534:
    """Gilded Gargoyle / 镀金的石像鬼
    亡语：将一张幸运币置入你的手牌。"""

    # <b>Deathrattle:</b> Add a Coin to your hand.
    deathrattle = Give(CONTROLLER, THE_COIN)


class LOOT_538:
    """Temporus / 坦普卢斯
    战吼：在本回合结束后，你的对手连续行动两个回合。然后你行动两个回合。"""

    # <b>Battlecry:</b> Your opponent takes two turns. Then you take two turns.
    def play(self):
        self.game.next_players.append(self.controller.opponent)
        self.game.next_players.append(self.controller.opponent)
        self.game.next_players.append(self.controller)
        self.game.next_players.append(self.controller)


##
# Spells


class LOOT_008:
    """Psychic Scream / 心灵尖啸
    将所有随从洗入你对手的牌库。"""

    # Shuffle all minions into your opponent's deck.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Shuffle(OPPONENT, ALL_MINIONS)


class LOOT_187:
    """Twilight's Call / 暮光召唤
    召唤两个在本局对战中死亡，并具有亡语的友方随从的1/1复制。"""

    # Summon 1/1 copies of 2 friendly <b>Deathrattle</b> minions that died this game.
    requirements = {
        PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
    }
    play = (
        Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE))).then(
            Buff(Summon.CARD, "LOOT_187e")
        )
        * 2
    )


class LOOT_187e:
    atk = SET(1)
    max_health = SET(1)


class LOOT_278:
    """Unidentified Elixir / 未鉴定的药剂
    使一个随从获得+2/+2。在你手牌中时获得额外效果。"""

    # Give a minion +2/+2. Gains a bonus effect in_your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "LOOT_278e")
    entourage = ["LOOT_278t1", "LOOT_278t2", "LOOT_278t3", "LOOT_278t4"]
    draw = Morph(SELF, RandomEntourage())


LOOT_278e = buff(+2, +2)


class LOOT_278t1:
    """Elixir of Life"""

    # Give a minion +2/+2 and <b>Lifesteal</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "LOOT_278t1e")


LOOT_278t1e = buff(+2, +2, lifesteal=True)


class LOOT_278t2:
    """Elixir of Purity"""

    # Give a minion +2/+2 and <b>Divine Shield</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "LOOT_278t2e")


class LOOT_278t2e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }

    def apply(self, target):
        self.game.trigger(self, (GiveDivineShield(target),), None)


class LOOT_278t3:
    """Elixir of Shadows"""

    # Give a minion +2/+2. Summon a 1/1 copy of_it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(TARGET, "LOOT_278t3e"),
        Summon(CONTROLLER, ExactCopy(TARGET)).then(Buff(Summon.CARD, "LOOT_278t3e2")),
    )


LOOT_278t3e = buff(+2, +2)


class LOOT_278t3e2:
    atk = SET(1)
    max_health = SET(1)


class LOOT_278t4:
    """Elixir of Hope"""

    # [x]Give a minion +2/+2 and "<b>Deathrattle:</b> Return this minion to your hand."
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "LOOT_278t4e")


class LOOT_278t4e:
    tags = {
        GameTag.DEATHRATTLE: True,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }
    deathrattle = Summon(CONTROLLER, Copy(OWNER))


class LOOT_353:
    """Psionic Probe / 灵能窥探
    复制你对手的牌库中的一张法术牌，并将其置入你的 手牌。"""

    # Copy a spell in your opponent's deck and add it to your hand.
    play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK + SPELL)))


class LOOT_507:
    """Lesser Diamond Spellstone / 小型法术钻石
    复活两个不同的友方随从。@（施放四个法术后升级。）"""

    # Resurrect 2 different friendly minions. @<i>(Cast 4 spells to upgrade.)</i>
    play = Summon(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 2))
    progress_total = 4
    reward = Morph(SELF, "LOOT_507t")

    class Hand:
        events = Play(CONTROLLER, SPELL).after(AddProgress(SELF, Play.CARD))


class LOOT_507t:
    """Diamond Spellstone"""

    # Resurrect 3 different friendly minions. @
    play = Summon(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 3))
    progress_total = 4
    reward = Morph(SELF, "LOOT_507t2")

    class Hand:
        events = Play(CONTROLLER, SPELL).after(AddProgress(SELF, Play.CARD))


class LOOT_507t2:
    """Greater Diamond Spellstone"""

    # Resurrect 4 different friendly minions.
    play = Summon(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 4))


##
# Weapons


class LOOT_209:
    """Dragon Soul / 巨龙之魂
    你在一回合中施放三个法术后，召唤一条5/5的龙。"""

    # After you cast 3 spells in a turn, summon a 5/5 Dragon.
    progress_total = 3
    reward = Summon(CONTROLLER, "LOOT_209t"), ClearProgress(SELF)
    events = (
        Play(CONTROLLER, SPELL).after(AddProgress(SELF, Play.CARD)),
        TURN_BEGIN.on(ClearProgress(SELF)),
    )
