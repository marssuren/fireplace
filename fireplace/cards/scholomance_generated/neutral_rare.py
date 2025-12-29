from ..utils import *


##
# Minions

class SCH_713:
    """Cult Neophyte
    Battlecry: Your opponent's spells cost (1) more next turn."""

    # 战吼：在下个回合中，你的对手的法术牌的法力值消耗增加（1）点
    play = Buff(OPPONENT, "SCH_713e")

class SCH_537:
    """Trick Totem
    At the end of your turn, cast a random spell that costs (3) or less."""

    # 在你的回合结束时，施放一个随机的法力值消耗小于或等于（3）的法术
    events = OWN_TURN_END.on(CastSpell(RandomSpell(cost=3)))

class SCH_146:
    """Robes of Protection
    Your minions have Elusive."""

    # 你的随从具有无法被法术或英雄技能指定为目标
    update = Refresh(FRIENDLY_MINIONS, {GameTag.CANT_BE_TARGETED_BY_SPELLS: True})

class SCH_142:
    """Voracious Reader
    At the end of your turn, draw until you have 3 cards."""

    # 在你的回合结束时，抽牌直到你有3张手牌
    events = OWN_TURN_END.on(DrawUntil(CONTROLLER, 3))


##
# Spells

class SCH_509:
    """Brain Freeze
    Freeze a minion. Combo: Also deal $3 damage to it."""

    # 冻结一个随从。连击：同时对其造成3点伤害
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Freeze(TARGET)
    combo = Hit(TARGET, 3)

class SCH_521:
    """Coerce
    Destroy a damaged minion. Combo: Destroy any minion."""

    # 消灭一个受伤的随从。连击：消灭任意一个随从
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    combo_requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET)
