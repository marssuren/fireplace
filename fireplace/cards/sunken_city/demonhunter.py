# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 恶魔猎手
"""

from ..utils import *

class TID_703:
    """Topple the Idol - 4费法术
    Dredge. Reveal it and deal damage equal to  its Cost to all minions."""
    # TODO: Implement mechanics: AFFECTED_BY_SPELL_POWER, DREDGE
    # TODO: Implement Dredge mechanic
    # play = ...

class TID_704:
    """Fossil Fanatic - 2费 2/2
    After your hero attacks, draw a Fel spell."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class TID_706:
    """Herald of Chaos - 3费 3/4
    Lifesteal Battlecry: If you've cast a Fel spell while holding this, gain Rush."""
    # TODO: Implement mechanics: BATTLECRY, LIFESTEAL
    # play = ...

class TSC_006:
    """Multi-Strike - 2费法术
    Give your hero +2 Attack this turn. They may attack an additional enemy minion."""
    # play = ...

class TSC_057:
    """Azsharan Defector - 4费 5/3
    Rush. Deathrattle: Put a 'Sunken Defector' on the  bottom of your deck."""
    # TODO: Implement mechanics: DEATHRATTLE, RUSH
    # TODO: Implement Azsharan mechanic (shuffle Sunken version)
    # deathrattle = ...

class TSC_058:
    """Predation - 2费法术
    Deal $2 damage. Costs (0) if you played a Naga while holding this."""
    # play = ...

class TSC_217:
    """Wayward Sage - 2费 2/2
    Outcast: Reduce the Cost of the left and right-most  cards in your hand by (1)."""
    # TODO: Implement mechanics: OUTCAST

class TSC_218:
    """Lady S'theno - 3费 1/4
    Immune while attacking. After you cast a spell, attack the lowest Health enemy."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class TSC_219:
    """Xhilag of the Abyss - 7费 3/6
    Colossal +4 At the start of your turn, increase the damage of Xhilag's Stalks by 1."""
    # TODO: Implement mechanics: COLOSSAL, TRIGGER_VISUAL
    # TODO: Implement Colossal mechanic

class TSC_608:
    """Abyssal Depths - 3费法术
    Draw your two lowest Cost minions."""
    # play = ...

class TSC_609:
    """Coilskar Commander - 6费 3/7
    Taunt. Battlecry: If you've cast three spells while holding this, summon two   copies of this.@ ({0} left!)@ (Ready!)"""
    # TODO: Implement mechanics: BATTLECRY, TAUNT
    # play = ...

class TSC_610:
    """Glaiveshark - 4费 4/3
    Battlecry: If your hero attacked this turn, deal 2 damage to all enemies."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class TSC_915:
    """Bone Glaive - 5费 5/0武器
    Battlecry: Dredge."""
    # TODO: Implement mechanics: BATTLECRY, DREDGE
    # TODO: Implement Dredge mechanic
    # play = ...

