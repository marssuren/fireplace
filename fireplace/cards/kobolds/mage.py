from ..utils import *


##
# Minions


class LOOT_170:
    """Raven Familiar / 乌鸦魔仆
    战吼：揭示双方牌库里的一张法术牌。如果你的牌法力值消耗较大，抽这张牌。"""

    # <b>Battlecry:</b> Reveal a spell in each deck. If yours costs more, draw it.
    play = JOUST_SPELL & ForceDraw(Joust.CHALLENGER)


class LOOT_231:
    """Arcane Artificer / 奥术工匠
    每当你施放一个法术，便获得等同于其法力值消耗的护甲值。"""

    # Whenever you cast a spell, gain Armor equal to its_Cost.
    events = Play(CONTROLLER, SPELL).after(GainArmor(FRIENDLY_HERO, COST(Play.CARD)))


class LOOT_535:
    """Dragoncaller Alanna / 巨龙召唤者奥兰纳
    战吼：在本局对战中，你每施放过一个法力值消耗大于或等于（5）点的法术，便召唤一个5/5的龙。"""

    # <b>Battlecry:</b> Summon a 5/5 Dragon for each spell you cast this game that costs
    # (5) or more.
    play = SummonBothSides(CONTROLLER, "LOOT_535t") * Count(
        CARDS_PLAYED_THIS_GAME + SPELL + (COST >= 5)
    )


class LOOT_537:
    """Leyline Manipulator / 魔网操控者
    战吼：如果你的手牌中有你的套牌之外的牌，则这些牌的法力值消耗减少（2）点。"""

    # <b>Battlecry:</b> If you're holding any cards that didn't start in your deck, reduce
    # their Cost by (2).
    play = Buff(FRIENDLY_HAND + STARTING_DECK, "LOOT_537e")


@custom_card
class LOOT_537e:
    tags = {
        GameTag.CARDNAME: "Leyline Manipulator Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -2,
    }
    events = REMOVED_IN_PLAY


##
# Spells


class LOOT_101:
    """Explosive Runes / 爆炸符文
    奥秘：在你的对手使用一张随从牌后，对该随从造成$6点伤害，超过其生命值的伤害将由对方英雄 承受。"""

    # <b>Secret:</b> After your opponent plays a minion, deal $6 damage to it and any
    # excess to their hero.
    secret = Play(OPPONENT, MINION).on(
        Reveal(SELF), Hit(ENEMY_HERO, HitExcessDamage(Play.CARD, SPELL_DAMAGE(6)))
    )


class LOOT_103:
    """Lesser Ruby Spellstone / 小型法术红宝石
    随机将一张法师法术牌置入你的手牌。@（使用两张元素牌后升级。）"""

    # Add 1 random Mage spell to your hand. @<i>(Play 2 Elementals to_upgrade.)</i>
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))
    progress_total = 2
    reward = Morph(SELF, "LOOT_103t1")

    class Hand:
        events = Play(CONTROLLER, ELEMENTAL).after(AddProgress(SELF, Play.CARD))


class LOOT_103t1:
    """Ruby Spellstone"""

    # Add 2 random Mage spells to your hand. @
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 2
    progress_total = 2
    reward = Morph(SELF, "LOOT_103t2")

    class Hand:
        events = Play(CONTROLLER, ELEMENTAL).after(AddProgress(SELF, Play.CARD))


class LOOT_103t2:
    """Greater Ruby Spellstone"""

    # Add 3 random Mage spells to your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 3


class LOOT_104:
    """Shifting Scroll / 变形卷轴
    如果这张牌在你的手牌中，每个回合都会变成一张随机法师法术牌。"""

    # Each turn this is in your hand, transform it into a random Mage spell.
    requirements = {
        PlayReq.REQ_CANNOT_PLAY_THIS: 0,
    }

    class Hand:
        events = OWN_TURN_BEGIN.on(
            lambda self: [
                Morph(SELF, RandomSpell(card_class=CardClass.MAGE)),
                Buff(SELF, "LOOT_104e")
            ]
        )


class LOOT_104e:
    class Hand:
        events = OWN_TURN_BEGIN.on(
            lambda self: [
                Morph(OWNER, RandomSpell(card_class=CardClass.MAGE)),
                Buff(OWNER, "LOOT_104e")
            ]
        )

    events = REMOVED_IN_PLAY


class LOOT_106:
    """Deck of Wonders / 惊奇套牌
    将五张惊奇卡牌洗入你的牌库。抽到时随机施放一个 法术。"""

    # Shuffle 5 Scrolls into your deck. When drawn, cast a random spell.
    play = Shuffle(CONTROLLER, "LOOT_106t") * 5


class LOOT_106t:
    """Scroll of Wonder"""

    # Cast a random spell. Draw a card. Cast this when drawn.
    play = CastSpell(RandomSpell())
    draw = CAST_WHEN_DRAWN


class LOOT_172:
    """Dragon's Fury / 巨龙怒火
    揭示你牌库中的一张法术牌。对所有随从造成等同于其法力值消耗的伤害。"""

    # Reveal a spell from your deck. Deal damage equal to its Cost to all_minions.
    play = Reveal(RANDOM(FRIENDLY_DECK + SPELL)).then(
        Hit(ALL_MINIONS, COST(Reveal.TARGET))
    )


##
# Weapons


class LOOT_108:
    """Aluneth / 艾露尼斯
    在你的回合结束时，抽三张牌。"""

    # At the end of your turn, draw 3 cards.
    events = OWN_TURN_END.on(Draw(CONTROLLER) * 3)
