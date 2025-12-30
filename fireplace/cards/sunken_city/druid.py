# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 德鲁伊
"""

from ..utils import *

class TID_000:
    """Spirit of the Tides - 2费 2/2
    If you have any unspent Mana at the end of  your turn, gain +1/+2."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class TID_001:
    """Moonbeam - 1费法术
    Deal $1 damage to an enemy, twice."""
    # play = ...

class TID_002:
    """Herald of Nature - 3费 3/3
    Battlecry: If you've cast a Nature spell while holding this, give your other minions +1/+1."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_026:
    """Colaque - 7费 6/5
    Colossal +1  Immune while you control Colaque's Shell."""
    # TODO: Implement mechanics: COLOSSAL
    # TODO: Implement Colossal mechanic

class TSC_650:
    """Flipper Friends - 5费法术
    Choose One - Summon a 6/6 Orca with Taunt; or six 1/1 Otters with Rush."""
    # TODO: Implement mechanics: CHOOSE_ONE
    # play = ...

class TSC_651:
    """Seaweed Strike - 3费法术
    Deal $4 damage to a minion. If you played a Naga while holding this, also give your hero +4 Attack this turn."""
    # play = ...

class TSC_652:
    """Green-Thumb Gardener - 6费 5/5
    Battlecry: Refresh empty Mana Crystals equal to the Cost of the highest Cost spell in your hand."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_653:
    """Bottomfeeder - 1费 1/3
    Deathrattle: Add a Bottomfeeder to the bottom of your deck with permanent +2/+2."""
    # TODO: Implement mechanics: DEATHRATTLE
    # deathrattle = ...

class TSC_654:
    """Aquatic Form - 0费法术
    Dredge. If you have the Mana to play the card this turn, draw it."""
    # TODO: Implement mechanics: DREDGE
    # TODO: Implement Dredge mechanic
    # play = ...

class TSC_656:
    """Miracle Growth - 7费法术
    Draw 3 cards. Summon a Plant with Taunt and stats equal to your hand size."""
    # play = ...

class TSC_657:
    """Dozing Kelpkeeper - 1费 4/4
    Rush. Starts Dormant. After you've cast 5 Mana  worth of spells, awaken."""
    # TODO: Implement mechanics: RUSH

class TSC_658:
    """Hedra the Heretic - 7费 4/5
    Battlecry: For each spell you've cast while holding this, summon a minion of that spell's Cost."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_927:
    """Azsharan Gardens - 1费法术
    Give all minions in your hand +1/+1. Put a 'Sunken Gardens' on the bottom of your deck."""
    # TODO: Implement Azsharan mechanic (shuffle Sunken version)
    # play = ...

