from ..utils import *


##
# Minions


class CFM_062:
    """Grimestreet Protector / 污手街守护者
    嘲讽，战吼：使相邻的随从获得圣盾。"""

    play = GiveDivineShield(SELF_ADJACENT)


class CFM_639:
    """Grimestreet Enforcer / 污手街惩罚者
    在你的回合结束时，使你手牌中的所有随从牌获得+1/+1。"""

    events = OWN_TURN_END.on(Buff(FRIENDLY_HAND + MINION, "CFM_639e"))


CFM_639e = buff(+1, +1)


class CFM_650:
    """Grimscale Chum / 暗鳞劫掠者
    战吼：随机使你手牌中的一张鱼人牌获得+1/+1。"""

    play = Buff(FRIENDLY_HAND + MURLOC, "CFM_650e")


CFM_650e = buff(+1, +1)


class CFM_753:
    """Grimestreet Outfitter / 污手街供货商
    战吼：使你手牌中的所有随从牌获得+1/+1。"""

    play = Buff(FRIENDLY_HAND + MINION, "CFM_753e")


CFM_753e = buff(+1, +1)


class CFM_759:
    """Meanstreet Marshal / 海象人执法官
    亡语：如果本随从的攻击力大于或等于2，抽一张牌。"""

    deathrattle = (ATK(SELF) >= 2) & Draw(CONTROLLER)


##
# Spells


class CFM_305:
    """Smuggler's Run / 风驰电掣
    使你手牌中的所有随从牌获得+1/+1。"""

    play = Buff(FRIENDLY_HAND + MINION, "CFM_305e")


CFM_305e = buff(+1, +1)


class CFM_800:
    """Getaway Kodo / 战术撤离
    奥秘：当一个友方随从死亡时，将其移回你的手牌。"""

    secret = Death(FRIENDLY + MINION).on(Reveal(SELF), Bounce(Death.ENTITY))


class CFM_905:
    """Small-Time Recruits / 三教九流
    从你的牌库中抽三张法力值消耗为（1）的随从牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 1))) * 3
