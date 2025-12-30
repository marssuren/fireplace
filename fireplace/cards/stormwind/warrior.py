# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 战士
"""

from ..utils import *

class DED_518:
    """操纵火炮 / Man the Cannons
    Deal $3 damage to a minion and $1 damage to all other minions."""
    # play = ...

class DED_519:
    """迪菲亚炮手 / Defias Cannoneer
    After your hero attacks, deal 2 damage to a random enemy twice."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class DED_527:
    """铁匠锤 / Blacksmithing Hammer
    Tradeable After you Trade this,  gain +2 Durability."""
    # TODO: Implement mechanics: TRADEABLE
    # TODO: Implement Tradeable mechanic

class SW_021:
    """怯懦的步兵 / Cowardly Grunt
    Deathrattle: Summon a minion from your deck."""
    # deathrattle = ...
    pass

class SW_023:
    """挑衅 / Provoke
    Tradeable Choose a friendly minion. Enemy minions attack it."""
    # TODO: Implement mechanics: TRADEABLE
    # TODO: Implement Tradeable mechanic
    # play = ...

class SW_024:
    """洛萨 / Lothar
    At the end of your turn, attack a random enemy minion. If it dies, gain +3/+3."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class SW_027:
    """海上威胁 / Shiver Their Timbers!
    Deal $2 damage to a minion. If you control a Pirate, deal $5 instead."""
    # play = ...

class SW_028:
    """开进码头 / Raid the Docks
    Questline: Play 3 Pirates. Reward: Draw a weapon."""
    # TODO: Implement Questline mechanic
    # play = ...

class SW_029:
    """港口匪徒 / Harbor Scamp
    Battlecry: Draw a Pirate."""
    # play = ...
    pass

class SW_030:
    """货物保镖 / Cargo Guard
    At the end of your turn, gain 3 Armor."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class SW_093:
    """暴风城海盗 / Stormwind Freebooter
    Battlecry: Give your hero +2 Attack this turn."""
    # play = ...
    pass

class SW_094:
    """厚重板甲 / Heavy Plate
    Tradeable Gain 8 Armor."""
    # play = ...

class SW_097:
    """遥控傀儡 / Remote-Controlled Golem
    After this takes damage, shuffle two Golem Parts into your deck. When drawn,   summon a 2/1 Mech."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

