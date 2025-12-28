"""
Southshore vs. Tarren Mill
"""

from ..utils import *


class TBST_002:
    """OLDN3wb Mage / OLDN3wb Mage
    At the end of your turn, deal 1 damage to random enemy minion."""

    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_MINION, 1))


class TBST_003:
    """OLDN3wb Healer / OLDN3wb Healer
    At the end of your turn, heal 2 damage from adjacent minions."""

    events = OWN_TURN_END.on(Heal(SELF_ADJACENT, 2))


class TBST_004:
    """OLDLegit Healer / OLDLegit Healer
    At the end of your turn, summon a random friendly minion that died this turn."""

    events = OWN_TURN_END.on(
        Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + MINION + KILLED_THIS_TURN)))
    )


class TBST_005:
    """OLDPvP Rogue / OLDPvP Rogue
    Stealth Regain Stealth when PvP Rogue kills a minion."""

    events = Death(MINION, SELF).on(Stealth(SELF))


class TBST_006:
    """OLDTBST Push Common Card / OLDTBST Push Common Card
    push a common card into player's hand"""

    pass
