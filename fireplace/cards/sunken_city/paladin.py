# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 圣骑士
"""

from ..utils import *

class TID_077:
    """Lightray - 9费 5/5
    Taunt Costs (1) less for each Paladin card you've played this game."""
    # TODO: Implement mechanics: TAUNT

class TID_098:
    """Myrmidon - 3费 3/4
    After you cast a spell on this minion, draw a card."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class TID_949:
    """Front Lines - 9费法术
    Summon a minion from each player's deck. Repeat until either side of the battlefield is full."""
    # play = ...

class TSC_030:
    """The Leviathan - 7费 4/5
    Colossal +1 Rush, Divine Shield After this attacks, Dredge."""
    # TODO: Implement mechanics: COLOSSAL, DIVINE_SHIELD, DREDGE, RUSH, TRIGGER_VISUAL
    # TODO: Implement Dredge mechanic
    # TODO: Implement Colossal mechanic

class TSC_059:
    """Bubblebot - 4费 4/4
    Battlecry: Give your other Mechs Divine Shield and Taunt."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_060:
    """Shimmering Sunfish - 3费 2/5
    Battlecry: If you're holding a Holy Spell, gain Taunt and Divine Shield."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_061:
    """The Garden's Grace - 10费法术
    Give a minion +4/+4 and Divine Shield. Costs (1) less for each Mana you've spent on Holy spells this game."""
    # play = ...

class TSC_074:
    """Kotori Lightblade - 2费 2/3
    After you cast a Holy spell on this, cast it again on   another friendly minion."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class TSC_076:
    """Immortalized in Stone - 7费法术
    Summon a 4/8, 2/4, and 1/2 Elemental with Taunt."""
    # play = ...

class TSC_079:
    """Radar Detector - 2费法术
    Scan the bottom 5 cards of your deck. Draw any Mechs found this way, then shuffle your deck."""
    # play = ...

class TSC_083:
    """Seafloor Savior - 2费 2/2
    Battlecry: Dredge. If it's a minion, give it this minion's Attack and Health."""
    # TODO: Implement mechanics: BATTLECRY, DREDGE
    # TODO: Implement Dredge mechanic
    # play = ...

class TSC_644:
    """Azsharan Mooncatcher - 3费 4/2
    Divine Shield. Battlecry: Put a 'Sunken Mooncatcher' on the bottom of your deck."""
    # TODO: Implement mechanics: BATTLECRY, DIVINE_SHIELD
    # TODO: Implement Azsharan mechanic (shuffle Sunken version)
    # play = ...

class TSC_952:
    """Holy Maki Roll - 1费法术
    Restore #2 Health. Repeatable this turn."""
    # play = ...

