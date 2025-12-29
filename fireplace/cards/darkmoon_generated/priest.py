from ..utils import *


##
# Minions

class DMF_053:
    """Blood of G'huun (戈霍恩之血)
    Taunt At the end of your turn, summon a 5/5 copy of a minion in your deck."""

    # TODO: Implement mechanics: TAUNT, TRIGGER_VISUAL

class DMF_056:
    """G'huun the Blood God (戈霍恩，鲜血之神)
    Battlecry: Draw 2 cards. They cost Health instead of Mana."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_116:
    """The Nameless One (无名者)
    Battlecry: Choose a minion. Become a 4/4 copy of it, then Silence it."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_120:
    """Nazmani Bloodweaver (纳兹曼尼织血者)
    After you cast a spell, reduce the Cost of a random card in your hand by (1)."""

    # TODO: Implement mechanics: TRIGGER_VISUAL

class DMF_121:
    """Fortune Teller (占卜机)
    Taunt Battlecry: Gain +1/+1 for each spell in your hand."""

    # TODO: Implement mechanics: BATTLECRY, TAUNT
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_184:
    """Fairground Fool (游乐园小丑)
    Taunt Corrupt: Gain +4 Health."""

    # TODO: Implement mechanics: CORRUPT, TAUNT
    # TODO: Implement Corrupt effect
    # corrupt = ...

class YOP_007:
    """Dark Inquisitor Xanesh (黑暗审判官夏奈什)
    Battlecry: Reduce the Cost of all Corrupt and Corrupted cards in your hand and deck by (2)."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class YOP_008:
    """Lightsteed (圣光战马)
    Your healing effects also give affected minions +2 Health."""

    # TODO: Implement mechanics: TRIGGER_VISUAL


##
# Spells

class DMF_054:
    """Insight (洞察)
    Draw a minion. Corrupt: Reduce its Cost by (2)."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement spell effect
    # play = ...

class DMF_055:
    """Idol of Y'Shaarj (亚煞极神像)
    Summon a 10/10 copy of a minion in your deck."""

    # TODO: Implement spell effect
    # play = ...

class DMF_186:
    """Auspicious Spirits (吉兆)
    Summon a random 4-Cost minion. Corrupt: Summon a 7-Cost minion instead."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement spell effect
    # play = ...

class DMF_187:
    """Palm Reading (解读手相)
    Discover a spell. Reduce the Cost of spells in your hand by (1)."""

    # TODO: Implement mechanics: DISCOVER
    # TODO: Implement spell effect
    # play = ...
