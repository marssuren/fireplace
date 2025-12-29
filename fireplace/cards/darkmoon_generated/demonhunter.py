from ..utils import *


##
# Minions

class DMF_217:
    """Line Hopper (越线的游客)
    Your Outcast cards cost (1) less."""

    # TODO: Implement mechanics: AURA

class DMF_222:
    """Redeemed Pariah (获救的流民)
    After you play an Outcast card, gain +1/+1."""

    # TODO: Implement mechanics: TRIGGER_VISUAL

class DMF_223:
    """Renowned Performer (知名表演者)
    Rush Deathrattle: Summon two   1/1 Assistants with Taunt.  """

    # TODO: Implement mechanics: DEATHRATTLE
    # TODO: Implement Deathrattle effect
    # deathrattle = ...

class DMF_226:
    """Bladed Lady (刀锋舞娘)
    Rush Costs (1) if your hero has 6 or more Attack."""

    # TODO: Implement mechanics: RUSH

class DMF_229:
    """Stiltstepper (高跷艺人)
    Battlecry: Draw a card. If you play it this turn, give your hero +4 Attack this turn."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_230:
    """Il'gynoth (伊格诺斯)
    Lifesteal Your Lifesteal damages the enemy hero instead of healing you."""

    # TODO: Implement card effect
    pass

class DMF_231:
    """Zai, the Incredible (扎依，出彩艺人)
    Battlecry: Copy the left- and right-most cards in your hand."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_247:
    """Insatiable Felhound (贪食地狱犬)
    Taunt  Corrupt: Gain +1/+1 and Lifesteal."""

    # TODO: Implement mechanics: CORRUPT, TAUNT
    # TODO: Implement Corrupt effect
    # corrupt = ...

class DMF_248:
    """Felsteel Executioner (魔钢处决者)
    Corrupt: Become a weapon."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...

class YOP_002:
    """Felsaber (邪刃豹)
    Can only attack if your hero attacked this turn."""

    # TODO: Implement card effect
    pass


##
# Spells

class DMF_219:
    """Relentless Pursuit (冷酷追杀)
    Give your hero +4 Attack and Immune this turn."""

    # TODO: Implement spell effect
    # play = ...

class DMF_221:
    """Felscream Blast (邪吼冲击)
    Lifesteal. Deal $1 damage to a minion and its neighbors."""

    # TODO: Implement mechanics: LIFESTEAL
    # TODO: Implement spell effect
    # play = ...

class DMF_224:
    """Expendable Performers (演员大接力)
    Summon seven 1/1 Illidari with Rush. If they all die this turn, summon seven more."""

    # TODO: Implement spell effect
    # play = ...

class DMF_225:
    """Throw Glaive (投掷利刃)
    Deal $2 damage to a minion. If it dies, add a Temporary copy of this to your hand."""

    # TODO: Implement spell effect
    # play = ...

class DMF_249:
    """Acrobatics (空翻杂技)
    Draw 2 cards. If you play both this turn, draw 2 more."""

    # TODO: Implement spell effect
    # play = ...

class YOP_001:
    """Illidari Studies (伊利达雷研习)
    Discover an Outcast card. Your next one costs (1) less."""

    # TODO: Implement mechanics: DISCOVER
    # TODO: Implement spell effect
    # play = ...


##
# Weapons

class DMF_227:
    """Dreadlord's Bite (恐惧魔王之咬)
    Outcast: Deal 1 damage to all enemies."""

    # TODO: Implement mechanics: OUTCAST
