from ..utils import *


##
# Minions


class TRL_059:
    """Bog Slosher / 沼泽游荡者
    战吼：将一个友方随从移回你的手牌，并使其获得+2/+2。"""

    # <b>Battlecry:</b> Return a friendly minion to your hand and give it +2/+2.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Bounce(TARGET), Buff(TARGET, "TRL_059e")


TRL_059e = buff(+2, +2)


class TRL_060:
    """Spirit of the Frog / 青蛙之灵
    潜行一回合。每当你施放一个法术，从你的牌库中抽取一张法力值消耗增加（1）点的法术牌。"""

    # [x]<b>Stealth</b> for 1 turn. Whenever you cast a spell, draw a spell from your deck
    # that costs (1) more.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Play(CONTROLLER, SPELL).on(
            ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == (COST(Play.CARD) + 1))))
        ),
    )


class TRL_085:
    """Zentimo / 泽蒂摩
    每当你以一个随从为目标施放法术时，对该随从相邻的随从再次施放。"""

    # [x]Whenever you target a minion with a spell, cast it again on its neighbors.
    events = Play(CONTROLLER, SPELL, MINION).on(
        CastSpell(Play.CARD, ADJACENT(Play.TARGET))
    )


class TRL_345:
    """Krag'wa, the Frog / 卡格瓦，青蛙之神
    战吼：将你上回合使用的所有法术牌移回你的手牌。"""

    # <b>Battlecry:</b> Return all spells you played last turn to_your hand.
    play = Give(CONTROLLER, Copy(CARDS_PLAYED_LAST_TURN + SPELL))


class TRL_522:
    """Wartbringer / 疾疫使者
    战吼：如果你在本回合施放了两个法术，则造成2点伤害。"""

    # <b>Battlecry:</b> If you played 2_spells this turn, deal 2_damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_SPELLS_PLAYED_THIS_TURN: 2,
    }
    powered_up = Count(CARDS_PLAYED_THIS_TURN + SPELL) >= 2
    play = powered_up & Hit(TARGET, 2)


##
# Spells


class TRL_012:
    """Totemic Smash / 图腾重击
    造成$2点伤害。 超杀：召唤一个 基础图腾。"""

    # Deal $2 damage. <b>Overkill</b>: Summon a basic Totem.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)
    overkill = Summon(CONTROLLER, RandomBasicTotem())


class TRL_058:
    """Haunting Visions / 亡鬼幻象
    在本回合中，你所施放的下一个法术的法力值消耗减少（3）点。发现一张法术牌。"""

    # The next spell you cast this turn costs (3) less. <b>Discover</b> a spell.
    play = (Buff(CONTROLLER, "TRL_058e"), DISCOVER(RandomSpell()))


class TRL_058e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class TRL_082:
    """Big Bad Voodoo / 终极巫毒
    使一个友方随从获得“亡语：随机召唤一个法力值消耗增加（1）点的随从。”"""

    # Give a friendly minion "<b>Deathrattle:</b> Summon a random minion that costs (1)
    # more."
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "TRL_082e")


class TRL_082e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=COST(OWNER) + 1))


class TRL_351:
    """Rain of Toads / 蟾蜍雨
    召唤三个2/4并具有嘲讽的蟾蜍。 过载：（3）"""

    # Summon three 2/4 Toads with <b>Taunt</b>. <b>Overload:</b> (3)
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "TRL_351t") * 3


##
# Weapons


class TRL_352:
    """Likkim / 舔舔魔杖
    当你有过载的法力水晶时，拥有+2攻击力。"""

    # Has +2 Attack while you have <b>Overloaded</b> Mana Crystals.
    update = OVERLOADED(CONTROLLER) & Refresh(SELF, {GameTag.ATK: 2})
