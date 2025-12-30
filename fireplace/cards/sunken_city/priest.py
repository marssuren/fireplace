# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 牧师
"""

from ..utils import *

class TID_085:
    """Herald of Light - 3费 3/4
    Battlecry: If you've cast a Holy spell while holding this, restore #6 Health to all friendly characters."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TID_700:
    """Disarming Elemental - 4费 4/4
    Battlecry: Dredge for your opponent. Set its Cost to (6)."""
    # TODO: Implement mechanics: BATTLECRY, DREDGE
    # TODO: Implement Dredge mechanic
    # play = ...

class TID_920:
    """Drown - 4费法术
    Put an enemy minion on the bottom of your deck."""
    # play = ...

class TSC_209:
    """Whirlpool - 8费法术
    Destroy all minions and all copies of them (wherever they are)."""
    # play = ...

class TSC_210:
    """Illuminate - 0费法术
    Dredge. If it's a spell, reduce its Cost by (3)."""
    # TODO: Implement mechanics: DREDGE
    # TODO: Implement Dredge mechanic
    # play = ...

class TSC_211:
    """Whispers of the Deep - 1费法术
    Silence a friendly minion, then deal damage equal to its Attack randomly split among all enemy minions."""
    # TODO: Implement mechanics: AFFECTED_BY_SPELL_POWER, ImmuneToSpellpower
    # play = ...

class TSC_212:
    """Handmaiden - 3费 3/2
    Battlecry: If you've cast three spells while holding this, draw 3 cards.@ ({0} left!)@ (Ready!)"""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_213:
    """Queensguard - 2费 2/3
    Battlecry: Gain +1/+1 for each spell you've cast this turn."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_215:
    """Serpent Wig - 1费法术
    Give a minion +1/+2. If you played a Naga while holding this, add a Serpent Wig to your hand."""
    # play = ...

class TSC_216:
    """Blackwater Behemoth - 7费 8/10
    Colossal +1 Lifesteal"""
    # TODO: Implement mechanics: COLOSSAL, LIFESTEAL
    # TODO: Implement Colossal mechanic

class TSC_702:
    """Switcheroo - 5费法术
    Draw 2 minions. Swap their Health."""
    # play = ...

class TSC_775:
    """Azsharan Ritual - 4费法术
    Silence a minion and summon a copy of it. Put a 'Sunken Ritual' on the bottom of your deck."""
    # TODO: Implement mechanics: SILENCE
    # TODO: Implement Azsharan mechanic (shuffle Sunken version)
    # play = ...

class TSC_828:
    """Priestess Valishj - 1费 1/1
    Battlecry: Refresh an empty Mana Crystal for each spell    you've cast this turn.@ (@)"""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

