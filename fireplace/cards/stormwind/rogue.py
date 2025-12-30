# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 潜行者
"""

from ..utils import *

class DED_004:
    """黑水弯刀 / Blackwater Cutlass
    Tradeable After you Trade this, reduce the Cost of a spell in your hand by (1)."""
    # TODO: Implement mechanics: TRADEABLE
    # TODO: Implement Tradeable mechanic

class DED_005:
    """海盗谈判 / Parrrley
    Swap this for a card in your opponent's deck."""
    # play = ...

class DED_510:
    """艾德温，迪菲亚首脑 / Edwin, Defias Kingpin
    Battlecry: Draw a card. If you play it this turn, gain +2/+2 and repeat this effect."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class SW_050:
    """变装大师 / Maestra of the Masquerade
    You start the game as a different class until you play a Rogue card."""
    pass

class SW_052:
    """探查内鬼 / Find the Imposter
    Questline: Play 2 SI:7 cards. Reward: Add a Spy Gizmo to your hand."""
    # TODO: Implement Questline mechanic
    # play = ...

class SW_310:
    """伪造的匕首 / Counterfeit Blade
    Battlecry: Get a copy of a random friendly Deathrattle minion that died this game."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...
    # deathrattle = ...

class SW_311:
    """锁喉 / Garrote
    Deal $2 damage to the enemy hero. Shuffle 3 Bleeds into your deck that deal $2 more when drawn."""
    # play = ...

class SW_405:
    """简略情报 / Sketchy Information
    Draw a Deathrattle card that costs (4) or less. Trigger its Deathrattle."""
    # deathrattle = ...
    # play = ...

class SW_411:
    """军情七处线人 / SI:7 Informant
    Battlecry: Gain +1/+1 for each other SI:7 card you've played this game."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class SW_412:
    """军情七处的要挟 / SI:7 Extortion
    Tradeable Deal $3 damage to an undamaged character."""
    # TODO: Implement mechanics: TRADEABLE
    # TODO: Implement Tradeable mechanic
    # play = ...

class SW_413:
    """军情七处探员 / SI:7 Operative
    Rush After this attacks a minion, gain Stealth."""
    # TODO: Implement mechanics: RUSH, TRIGGER_VISUAL

class SW_417:
    """军情七处刺客 / SI:7 Assassin
    Costs (1) less for each SI:7 card you've played this game. Combo: Destroy an enemy minion."""
    # TODO: Implement mechanics: COMBO

class SW_434:
    """放贷的鲨鱼 / Loan Shark
    Battlecry: Give your opponent a Coin.   Deathrattle: You get two."""
    # TODO: Implement mechanics: BATTLECRY, DEATHRATTLE
    # play = ...
    # deathrattle = ...

