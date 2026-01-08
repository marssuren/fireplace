from ..utils import *


##
# Minions


class GIL_118:
    """Deranged Doctor / 癫狂的医生
    亡语：为你的英雄恢复#8点生命值。"""

    # <b>Deathrattle:</b> Restore 8 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 8)


class GIL_119:
    """Cauldron Elemental / 坩埚元素
    你的其他元素拥有+2攻击力。"""

    # Your other Elementals have +2 Attack.
    update = Refresh(FRIENDLY_MINIONS - SELF + ELEMENTAL, buff="GIL_119e")


GIL_119e = buff(atk=2)


class GIL_201:
    """Pumpkin Peasant / 南瓜农夫
    吸血 如果这张牌在你的手牌中，每个回合使其攻击力和生命值互换。"""

    # [x]<b>Lifesteal</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_201t", "GIL_200e")))


class GIL_201t:
    """Pumpkin Peasant"""

    # [x]<b>Lifesteal</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_201", "GIL_200e")))


class GIL_212:
    """Ravencaller / 唤鸦者
    战吼：随机将两张法力值消耗为（1）的随从牌置入你的手牌。"""

    # [x]<b>Battlecry:</b> Add two random 1-Cost minions to your hand.
    play = Give(CONTROLLER, RandomMinion(cost=1)) * 2


class GIL_213:
    """Tanglefur Mystic / 杂毛秘术师
    战吼： 随机将一张法力值消耗为（2）的随从牌置入每个玩家的手牌。"""

    # <b>Battlecry:</b> Add a random 2-Cost minion to each player's hand.
    play = Give(PLAYER, RandomMinion(cost=2))


class GIL_513:
    """Lost Spirit / 迷失的幽魂
    亡语：使你的所有随从获得+1攻击力。"""

    # <b>Deathrattle:</b> Give your minions +1 Attack.
    deathrattle = Buff(FRIENDLY_MINIONS, "GIL_513e")


GIL_513e = buff(atk=1)


class GIL_526:
    """Wyrmguard / 龙骨卫士
    战吼：如果你的手牌中有龙牌，便获得+1攻击力和嘲讽。"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain +1 Attack and <b>Taunt</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "GIL_526e")


GIL_526e = buff(atk=1, taunt=True)


class GIL_528:
    """Swift Messenger / 迅捷的信使
    突袭 如果这张牌在你的手牌中，每个回合使其攻击力和生命值互换。"""

    # [x]<b>Rush</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_528t", "GIL_200e")))


class GIL_528t:
    """Swift Messenger"""

    # [x]<b>Rush</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_528", "GIL_200e")))


class GIL_529:
    """Spellshifter / 幻术士
    法术伤害+1 如果这张牌在你的手牌中，每个回合使其攻击力和生命值互换。"""

    # [x]<b>Spell Damage +1</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_529t", "GIL_200e")))


class GIL_529t:
    """Spellshifter"""

    # [x]<b>Spell Damage +1</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_529", "GIL_200e")))


class GIL_534:
    """Hench-Clan Thug / 荆棘帮暴徒
    在你的英雄攻击后，使本随从获得+1/+1。"""

    # After your hero attacks, give this minion +1/+1.
    events = Attack(FRIENDLY_HERO).after(Buff(SELF, "GIL_534t"))


GIL_534t = buff(+1, +1)


class GIL_561:
    """Blackwald Pixie / 黑瘴林树精
    战吼：复原你的英雄技能。"""

    # <b>Battlecry:</b> Refresh your Hero Power.
    play = RefreshHeroPower(FRIENDLY_HERO_POWER)


class GIL_646:
    """Clockwork Automaton / 发条自动机
    使你的英雄技能的伤害和治疗效果翻倍。"""

    # Double the damage and_healing of your Hero_Power.
    update = Refresh(
        CONTROLLER,
        {
            GameTag.HERO_POWER_DOUBLE: 1,
        },
    )


class GIL_667:
    """Rotten Applebaum / 腐烂的苹果树
    嘲讽。亡语：为你的英雄恢复#6点生命值。"""

    # <b>Taunt</b> <b>Deathrattle:</b> Restore 6 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 6)


class GIL_683:
    """Marsh Drake / 沼泽幼龙
    战吼：为你的对手召唤一个2/1并具有剧毒的幼龙猎手。"""

    # <b>Battlecry:</b> Summon a 2/1 <b>Poisonous</b> Drakeslayer for your opponent.
    play = Summon(OPPONENT, "GIL_683t")


class GIL_816:
    """Swamp Dragon Egg / 沼泽龙蛋
    亡语：随机将一张龙牌置入你的手牌。"""

    # <b>Deathrattle:</b> Add a random Dragon to your hand.
    deathrattle = Give(CONTROLLER, RandomDragon())
