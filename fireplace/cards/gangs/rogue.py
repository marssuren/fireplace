from ..utils import *


##
# Minions


class CFM_342:
    """Luckydo Buccaneer / 土地精海盗
    战吼： 如果你的武器至少有3点攻击力，便获得+4/+4。"""

    powered_up = Find(FRIENDLY_WEAPON + (ATK >= 3))
    play = powered_up & Buff(SELF, "CFM_342e")


CFM_342e = buff(+4, +4)


class CFM_634:
    """Lotus Assassin / 玉莲帮刺客
    潜行。每当本随从攻击并消灭一个随从时，便获得潜行。"""

    events = Attack(SELF, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & Stealth(SELF)
    )


class CFM_691(JadeGolemUtils):
    """Jade Swarmer"""

    deathrattle = SummonJadeGolem(CONTROLLER)


class CFM_693:
    """Gadgetzan Ferryman / 加基森摆渡人
    连击：将一个友方随从移回你的手牌。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
    }
    play = Bounce(TARGET)


class CFM_694:
    """Shadow Sensei / 暗影大师
    战吼：使一个潜行的随从获得+2/+2。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_STEALTHED_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "CFM_694e")


CFM_694e = buff(+2, +2)


class CFM_781:
    """Shaku, the Collector / 收集者沙库尔
    潜行。每当本随从攻击时，随机将一张（你对手职业的）牌置入你的手牌。"""

    events = Attack(SELF).on(
        Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))
    )


##
# Spells


class CFM_630:
    """Counterfeit Coin / 伪造的幸运币
    在本回合中，获得一个法力 水晶。"""

    play = ManaThisTurn(CONTROLLER, 1)


class CFM_690(JadeGolemUtils):
    """Jade Shuriken"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2)
    combo = Hit(TARGET, 2), SummonJadeGolem(CONTROLLER)
