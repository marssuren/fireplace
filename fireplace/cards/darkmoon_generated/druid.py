from ..utils import *


##
# Minions

class DMF_059:
    """Fizzy Elemental (泡沫元素)
    Rush Taunt"""

    # TODO: Implement mechanics: RUSH, TAUNT

class DMF_060:
    """Umbral Owl (幽影猫头鹰)
    Rush Costs (1) less for each spell you've cast this game."""

    # TODO: Implement mechanics: RUSH

class DMF_061:
    """Faire Arborist (马戏团树艺师)
    Choose One - Draw a card; or Summon a 2/2 Treant. Corrupt: Do both."""

    # TODO: Implement mechanics: CHOOSE_ONE, CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement Choose One effect
    # choose = ...

class DMF_733:
    """Kiri, Chosen of Elune (基利，艾露恩之眷)
    Battlecry: Add a Solar Eclipse and Lunar Eclipse to your hand."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_734:
    """Greybough (格雷布)
    Taunt Deathrattle: Give a random friendly minion "Deathrattle: Summon Greybough.""""

    # TODO: Implement mechanics: DEATHRATTLE, TAUNT
    # TODO: Implement Deathrattle effect
    # deathrattle = ...

class YOP_025:
    """Dreaming Drake (迷梦幼龙)
    Taunt Corrupt: Gain +2/+2."""

    # TODO: Implement mechanics: CORRUPT, TAUNT
    # TODO: Implement Corrupt effect
    # corrupt = ...


##
# Spells

class DMF_057:
    """Lunar Eclipse (月蚀)
    Deal $3 damage to a minion. Your next spell this turn costs (2) less."""

    # TODO: Implement spell effect
    # play = ...

class DMF_058:
    """Solar Eclipse (日蚀)
    The next spell you cast this turn casts twice."""

    # TODO: Implement spell effect
    # play = ...

class DMF_075:
    """Guess the Weight (猜重量)
    Draw a card. Guess if your next card costs more or less to draw it."""

    # TODO: Implement spell effect
    # play = ...

class DMF_730:
    """Moontouched Amulet (月触项链)
    Give your hero +4 Attack this turn. Corrupt: And gain 6 Armor."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement spell effect
    # play = ...

class DMF_732:
    """Cenarion Ward (塞纳里奥结界)
    Gain 8 Armor. Summon a random 8-Cost minion."""

    # TODO: Implement spell effect
    # play = ...

class YOP_026:
    """Arbor Up (树木生长)
    Summon two 2/2 Treants. Give your minions +2/+1."""

    # TODO: Implement spell effect
    # play = ...
