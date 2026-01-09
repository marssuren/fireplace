"""
暗月马戏团 - 潜行者
"""
from ..utils import *


##
# Minions

class DMF_511:
    """甜牙贼 - Sweet Tooth
    腐蚀：获得+2攻击力和隐身。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    corrupt = Buff(SELF, "DMF_511e")


class DMF_511e:
    """+2攻击力和隐身"""
    tags = {
        GameTag.ATK: 2,
        GameTag.STEALTH: True,
    }


class DMF_512:
    """影刃大师 - Shadow Clone
    隐身。亡语：召唤一个本随从的复制。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.STEALTH: True,
    }
    deathrattle = Summon(CONTROLLER, ExactCopy(SELF))


class DMF_513:
    """票务大师 - Ticket Master
    战吼：随机将你牌库中的一张牌洗入对手的牌库。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    play = Shuffle(OPPONENT, RANDOM(FRIENDLY_DECK))


class DMF_515:
    """恶意打击 - Malevolent Strike
    连击：获得+1攻击力。
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    combo = Buff(SELF, "DMF_515e")


class DMF_515e:
    """+1攻击力"""
    tags = {
        GameTag.ATK: 1,
    }


class DMF_516:
    """狡猾诈骗者 - Foxy Fraud
    战吼：你的下一个连击牌在本回合中的法力值消耗减少(2)点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = Buff(CONTROLLER, "DMF_516e")


class DMF_516e:
    """连击牌减费"""
    update = Refresh(FRIENDLY_HAND + COMBO, {GameTag.COST: -2})
    events = Play(CONTROLLER, COMBO).on(Destroy(SELF))


class DMF_517:
    """红烟天乌 - Tenwu of the Red Smoke
    战吼：将一个友方随从移回你的手牌。该牌在本回合中的法力值消耗为(1)点。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Bounce(TARGET),
        Buff(TARGET, "DMF_517e"),
    )


class DMF_517e:
    """本回合费用为1"""
    tags = {
        GameTag.COST: SET(1),
    }
    events = OWN_TURN_END.on(Destroy(SELF))


##
# Spells

class DMF_510:
    """奖品掠夺者 - Prize Plunderer
    造成3点伤害。连击：并抽一张牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3)
    combo = Draw(CONTROLLER)


class DMF_514:
    """诈骗 - Swindle
    抽一张法术牌。连击：并抽一张武器牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
    combo = ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)


class DMF_518:
    """暗影斗篷 - Cloak of Shadows
    你的英雄获得免疫，直到你的下个回合开始。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    play = Buff(FRIENDLY_HERO, "DMF_518e")


class DMF_518e:
    """免疫"""
    tags = {
        GameTag.IMMUNE: True,
    }
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class DMF_519:
    """八爪机器人 - Octobot
    秘密：当你的随从被攻击时，召唤三个2/2的海盗。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SECRET: True,
    }
    secret = Attack(ALL_PLAYERS, FRIENDLY_MINIONS).on(
        Summon(CONTROLLER, "DMF_519t") * 3,
        Reveal(SELF),
    )


class DMF_519t:
    """海盗 - Pirate"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.PIRATE,
    }


##
# Weapons

class DMF_520:
    """切割课程 - Cutting Class
    抽一张牌。连击：再抽一张。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 2,
        GameTag.COST: 2,
    }
    play = Draw(CONTROLLER)
    combo = Draw(CONTROLLER)
