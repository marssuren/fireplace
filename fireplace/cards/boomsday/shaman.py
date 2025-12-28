from ..utils import *


##
# Minions


class BOT_291:
    """Storm Chaser / 风暴追逐者
    战吼：从你的牌库中抽一张法力值消耗大于或等于（5）点的法术牌。"""

    # <b>Battlecry:</b> Draw a spell from your deck that costs_(5) or more.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST >= 5)))


class BOT_407:
    """Thunderhead / 雷云元素
    在你使用一张过载牌后，召唤两个1/1并具有突袭的“火花”。"""

    # [x]After you play a card with <b>Overload</b>, summon two 1/1 Sparks with
    # <b>Rush</b>.
    events = Play(CONTROLLER, OVERLOAD).after(
        SummonBothSides(CONTROLLER, "BOT_102t") * 2
    )


class BOT_411:
    """Electra Stormsurge / 伊莱克特拉·风潮
    战吼：在本回合中，你的下一个法术将施放两次。"""

    # <b>Battlecry:</b> Your next spell this turn casts twice.
    play = Buff(CONTROLLER, "BOT_411e")


class BOT_411e:
    events = Play(CONTROLLER, SPELL).after(
        Battlecry(Play.CARD, Play.TARGET), Destroy(SELF)
    )


class BOT_533:
    """Menacing Nimbus / 凶恶的雨云
    战吼：随机将一张元素牌置入你的手牌。"""

    # <b>Battlecry:</b> Add a random Elemental to your hand.
    play = Give(CONTROLLER, RandomElemental())


class BOT_543:
    """Omega Mind / 欧米茄灵能者
    战吼：如果你有十个法力水晶，在本回合中你的所有法术拥有 吸血。"""

    # [x]<b>Battlecry:</b> If you have 10 Mana Crystals, your spells have <b>Lifesteal</b>
    # this turn.
    powered_up = AT_MAX_MANA(CONTROLLER)
    play = powered_up & Buff(CONTROLLER, "BOT_543e")


class BOT_543e:
    update = Refresh(FRIENDLY + SPELL, {GameTag.LIFESTEAL: True})


##
# Spells


class BOT_093:
    """Elementary Reaction / 元素反应
    抽一张牌。如果你在上个回合使用过元素牌，则复制抽到的牌。"""

    # Draw a card. Copy it if_you played an Elemental last turn.
    play = Draw(CONTROLLER).then(
        ELEMENTAL_PLAYED_LAST_TURN & Give(CONTROLLER, ExactCopy(Draw.CARD))
    )


class BOT_099:
    """Eureka! / 我找到了
    随机召唤你手牌中的一张随从牌的一个复制。"""

    # Summon a copy of_a_random minion from your hand.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, ExactCopy(RANDOM(FRIENDLY_HAND + MINION)))


class BOT_245:
    """The Storm Bringer / 风暴聚合器
    随机将你的所有随从变形成为传说随从。"""

    # Transform your minions into random <b>Legendary</b> minions.
    play = Morph(FRIENDLY_MINIONS, RandomLegendaryMinion())


class BOT_246:
    """Beakered Lightning / 瓶装闪电
    对所有随从造成$1点伤害。 过载：（2）"""

    # Deal $1 damage to all minions. <b>Overload:</b> (2)
    play = Hit(ALL_MINIONS, 1)


class BOT_451:
    """Voltaic Burst / 流电爆裂
    召唤两个1/1并具有突袭的“火花”。过载：（1）"""

    # Summon two 1/1 Sparks with <b>Rush</b>. <b>Overload:</b> (1)
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BOT_102t") * 2
