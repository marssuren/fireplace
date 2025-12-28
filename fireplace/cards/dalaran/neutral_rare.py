from ..utils import *


##
# Minions


class DAL_058:
    """Hecklebot / 机械拷问者
    嘲讽，战吼：使你的对手从牌库中召唤一个随从。"""

    # <b>Taunt</b> <b>Battlecry:</b> Your opponent summons a minion from their deck.
    play = Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))


class DAL_081:
    """Spellward Jeweler / 破咒珠宝师
    战吼：直到下个回合，你的英雄拥有扰魔。"""

    # [x]<b>Battlecry:</b> Your hero can't be targeted by spells or Hero Powers until your
    # next turn.
    play = Buff(FRIENDLY_HERO, "DAL_081e")


class DAL_081e:
    tags = {
        GameTag.CANT_BE_TARGETED_BY_SPELLS: True,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
    }
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class DAL_434:
    """Arcane Watcher / 奥术守望者
    除非你拥有法术伤害， 否则无法进行攻击。"""

    # Can't attack unless you have <b>Spell Damage</b>.
    update = Find(FRIENDLY + SPELLPOWER) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class DAL_539:
    """Sunreaver Warmage / 夺日者战斗法师
    战吼：如果你的手牌中有法力值消耗大于或等于（5）点的法术牌，则造成4点伤害。"""

    # <b>Battlecry:</b> If you're holding a spell that costs (5) or more, deal 4 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_COST_5_OR_MORE_SPELL_IN_HAND: 0,
    }
    powered_up = Find(FRIENDLY_HAND + SPELL + (COST >= 5))
    play = powered_up & Hit(TARGET, 4)


class DAL_550:
    """Underbelly Ooze / 下水道软泥怪
    在本随从受到伤害并存活下来后，召唤一个它的复制。"""

    # After this minion survives damage, summon a copy_of it.
    events = SELF_DAMAGE.on(Dead(SELF) | Summon(CONTROLLER, ExactCopy(SELF)))


class DAL_582:
    """Portal Keeper / 传送门守护者
    战吼：将三张传送门洗入你的牌库。当抽到传送门时，召唤一个2/2并具有突袭的恶魔。"""

    # [x]<b>Battlecry:</b> Shuffle 3 Portals into your deck. When drawn, summon a 2/2 Demon
    # with <b>Rush</b>.
    play = Shuffle(CONTROLLER, "DAL_582t") * 3


class DAL_582t:
    play = Summon(CONTROLLER, "DAL_582t2")
    draw = CAST_WHEN_DRAWN


class DAL_749:
    """Recurring Villain / 再生大盗
    亡语：如果本随从的攻击力大于或等于4，则再次召唤本随从。"""

    # <b>Deathrattle:</b> If this minion has 4 or more Attack, resummon it.
    deathrattle = (ATK(SELF) >= 4) & Summon(CONTROLLER, "DAL_749")


class DAL_751:
    """Mad Summoner / 疯狂召唤师
    战吼：用1/1的小鬼填满每个玩家的面板。"""

    # [x]<b>Battlecry:</b> Fill each player's board with 1/1 Imps.
    play = (
        SummonBothSides(CONTROLLER, "DAL_751t") * 7,
        Summon(OPPONENT, "DAL_751t") * 7,
    )


class DAL_774:
    """Exotic Mountseller / 特殊坐骑商人
    每当你施放一个法术，随机召唤一个法力值消耗为（3）的 野兽。"""

    # Whenever you cast a spell, summon a random 3-Cost Beast.
    events = Play(CONTROLLER, SPELL).on(Summon(CONTROLLER, RandomBeast(cost=3)))


class DAL_775:
    """Tunnel Blaster / 坑道爆破师
    嘲讽，亡语：对所有随从造成3点伤害。"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Deal 3 damage to all minions.
    deathrattle = Hit(ALL_MINIONS, 3)
