from ..utils import *


##
# Minions


class BT_155:
    """Scrapyard Colossus / 废料场巨像
    嘲讽，亡语：召唤一个7/7并具有嘲讽的邪爆巨像。"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 7/7 Felcracked Colossus with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "BT_155t")


class BT_721:
    """Blistering Rot / 起泡的腐泥怪
    在你的回合结束时，召唤一个属性值等同于本随从的腐质。"""

    # [x]At the end of your turn, summon a Rot with stats equal to this
    # minion's.
    events = OWN_TURN_END.on(
        SummonCustomMinion(CONTROLLER, "BT_721t", 1, ATK(SELF), CURRENT_HEALTH(SELF))
    )


class BT_731:
    """Infectious Sporeling / 传染孢子
    在对随从造成伤害后，将其变为 传染孢子。"""

    # After this damages a minion, turn it into an Infectious_Sporeling.
    events = Damage(source=SELF).on(Morph(Damage.TARGET, "BT_731"))
