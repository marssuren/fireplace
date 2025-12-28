from ..utils import *


##
# Minions


class LOOT_130:
    """Arcane Tyrant / 奥术统御者
    在本回合中，如果你施放过法力值消耗大于或等于（5）的法术，则这张牌的法力值消耗为（0）点。"""

    # Costs (0) if you've cast a spell that costs (5) or more this turn.
    class Hand:
        events = Play(CONTROLLER, SPELL + (COST >= 5)).after(Buff(SELF, "LOOT_130e"))


@custom_card
class LOOT_130e:
    tags = {
        GameTag.CARDNAME: "Arcane Tyrant Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    cost = SET(0)
    events = REMOVED_IN_PLAY


class LOOT_149:
    """Corridor Creeper / 通道爬行者
    当本牌在你的手牌中时，每当一个随从死亡，法力值消耗便减少（1）点。"""

    # Costs (1) less whenever a minion dies while this is_in_your hand.
    class Hand:
        events = Death(MINION).on(Buff(SELF, "LOOT_149e"))


class LOOT_149e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class LOOT_161:
    """Carnivorous Cube / 食肉魔块
    战吼： 消灭一个友方随从。 亡语：召唤两个被消灭随从的复制。"""

    # <b>Battlecry:</b> Destroy a friendly minion. <b>Deathrattle:</b> Summon 2 copies of
    # it.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Destroy(TARGET)
    deathrattle = HAS_TARGET & Summon(CONTROLLER, Copy(TARGET)) * 2


class LOOT_193:
    """Shimmering Courser / 闪光的骏马
    在你对手的回合扰魔。"""

    # Only you can target this with spells and Hero Powers.
    update = CurrentPlayer(OPPONENT) & Refresh(
        SELF,
        {
            GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
            GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
        },
    )


class LOOT_389:
    """Rummaging Kobold / 狗头人拾荒者
    战吼：将你的一把被摧毁的武器置入你的手牌。"""

    # <b>Battlecry:</b> Return one of your destroyed weapons to your hand.
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + WEAPON)))


class LOOT_414:
    """Grand Archivist / 资深档案管理员
    在你的回合结束时，从你的牌库中施放一张法术牌（目标随机而定）。"""

    # At the end of your turn, cast a spell from your deck <i>(targets chosen
    # randomly)</i>.
    events = OWN_TURN_END.on(CastSpell(RANDOM(FRIENDLY_DECK + SPELL)))


class LOOT_529:
    """Void Ripper / 虚空撕裂者
    战吼： 使所有其他随从的攻击力和生命值互换。"""

    # <b>Battlecry:</b> Swap the Attack and Health of all_other_minions.
    play = Buff(ALL_MINIONS, "LOOT_529e")


LOOT_529e = AttackHealthSwapBuff()


class LOOT_539:
    """Spiteful Summoner / 恶毒的召唤师
    战吼：揭示你牌库中的一张法术牌。随机召唤一个法力值消耗与其相同的随从。"""

    # [x]<b>Battlecry:</b> Reveal a spell from your deck. Summon a random minion with the
    # same Cost.
    play = Reveal(RANDOM(FRIENDLY_DECK + SPELL)).then(
        Summon(CONTROLLER, RandomMinion(cost=COST(Reveal.TARGET)))
    )


class LOOT_540:
    """Dragonhatcher / 驯龙师
    在你的回合结束时，招募一条龙。"""

    # At the end of your turn, <b>Recruit</b> a Dragon.
    events = OWN_TURN_END.on(Recruit(DRAGON))
