from ..utils import *


##
# Minions


class TRL_323:
    """Emberscale Drake / 烬鳞幼龙
    战吼：如果你的手牌中有龙牌，便获得5点护甲值。"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain 5 Armor.
    powered_up = HOLDING_DRAGON
    play = powered_up & GainArmor(FRIENDLY_HERO, 5)


class TRL_326:
    """Smolderthorn Lancer / 燃棘枪兵
    战吼：如果你的手牌中有龙牌，则消灭一个受伤的敌方随从。"""

    # <b>Battlecry:</b> If you're holding a Dragon, destroy a damaged enemy minion.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    powered_up = HOLDING_DRAGON
    play = powered_up & Destroy(TARGET)


class TRL_327:
    """Spirit of the Rhino / 犀牛之灵
    潜行一回合。你的具有突袭的随从在它被召唤的回合免疫。"""

    # <b>Stealth</b> for 1 turn. Your <b>Rush</b> minions are <b>Immune</b> the turn
    # they're summoned.
    events = (OWN_TURN_BEGIN.on(Unstealth(SELF)),)
    update = Refresh(
        FRIENDLY_MINIONS + RUSH + THE_TURN_SUMMONED, {GameTag.CANT_BE_DAMAGED: True}
    )


class TRL_328:
    """War Master Voone / 指挥官沃恩
    战吼：复制你手牌中的所有龙牌。"""

    # <b>Battlecry:</b> Copy all Dragons in your hand.
    play = Give(CONTROLLER, Copy(FRIENDLY_HAND + DRAGON))


class TRL_329:
    """Akali, the Rhino / 阿卡里，犀牛之神
    突袭，超杀：从你的牌库中抽一张具有突袭的随从牌，并使其获得+5/+5。"""

    # <b>Rush</b> <b>Overkill:</b> Draw a <b>Rush</b> minion from your deck. Give it +5/+5.
    overkill = ForceDraw(RANDOM(FRIENDLY_DECK + RUSH + MINION)).then(
        Buff(ForceDraw.TARGET, "TRL_329e")
    )


TRL_329e = buff(+5, +5)


##
# Spells


class TRL_321:
    """Devastate / 毁灭打击
    对一个受伤的随从造成$4点 伤害。"""

    # Deal $4 damage to a damaged minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4)


class TRL_324:
    """Heavy Metal! / 重金属狂潮
    随机召唤一个法力值消耗等同于你的护甲值（最高不超过10点）的随从。"""

    # [x]Summon a random minion with Cost equal to your Armor <i>(up to 10).</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RandomMinion(cost=Min(ARMOR(FRIENDLY_HERO), 10)))


class TRL_362:
    """Dragon Roar / 巨龙怒吼
    随机将两张龙牌置入你的手牌。"""

    # Add 2 random Dragons to your hand.
    play = Give(CONTROLLER, RandomDragon()) * 2


##
# Weapons


class TRL_325:
    """Sul'thraze / 鞭笞者苏萨斯
    超杀：你可以再次攻击。"""

    # <b>Overkill</b>: You may attack again.
    overkill = ExtraAttack(FRIENDLY_HERO)


class TRL_360:
    """Overlord's Whip / 领主之鞭
    在你使用一张随从牌后，对其造成1点伤害。"""

    # After you play a minion, deal 1 damage to it.
    events = Play(CONTROLLER, MINION).after(Hit(Play.CARD, 1))
