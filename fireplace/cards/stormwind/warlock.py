# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 术士
"""

from ..utils import *

class DED_503:
    """暗影之刃飞刀手 / Shadowblade Slinger
    Battlecry: If you've taken damage this turn, deal that  much to an enemy minion."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class DED_504:
    """邪恶船运 / Wicked Shipment
    Tradeable Summon 2 1/1 Imps. (Upgrades by 2 when Traded!)"""
    # TODO: Implement mechanics: TRADEABLE
    # TODO: Implement Tradeable mechanic
    # play = ...

class DED_505:
    """碎舰恶魔 / Hullbreaker
    Battlecry and Deathrattle: Draw a spell. Your hero takes damage equal to its Cost."""
    # TODO: Implement mechanics: BATTLECRY, DEATHRATTLE
    # play = ...
    # deathrattle = ...

class SW_003:
    """符文秘银杖 / Runed Mithril Rod
    After you draw 4 cards, reduce the Cost of cards in your hand by (1). Lose 1 Durability."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class SW_084:
    """血缚小鬼 / Bloodbound Imp
    Whenever this attacks, deal 2 damage to your hero."""
    # TODO: Implement mechanics: TRIGGER_VISUAL

class SW_085:
    """暗巷契约 / Dark Alley Pact
    Summon a Fiend with Taunt and stats equal to your hand size."""
    # play = ...

class SW_086:
    """阴暗的酒保 / Shady Bartender
    Tradeable Battlecry: Give your Demons +2/+2."""
    # TODO: Implement mechanics: BATTLECRY, TRADEABLE
    # TODO: Implement Tradeable mechanic
    # play = ...

class SW_087:
    """恐惧坐骑 / Dreaded Mount
    Give a minion +1/+1. When it dies, summon an endless Dreadsteed."""
    # play = ...

class SW_088:
    """恶魔来袭 / Demonic Assault
    Deal $3 damage. Summon two 1/3 Voidwalkers with Taunt."""
    # play = ...

class SW_089:
    """资深顾客 / Entitled Customer
    Battlecry: Deal damage equal to your hand size to all other minions."""
    # TODO: Implement mechanics: BATTLECRY
    # play = ...

class SW_090:
    """纳斯雷兹姆之触 / Touch of the Nathrezim
    Deal $2 damage to a minion. If it dies, restore 3 Health to your hero."""
    # play = ...

class SW_091:
    """恶魔之种 / The Demon Seed
    Questline: Take 12 damage on your turns. Reward: Lifesteal. Deal $3 damage to the enemy hero."""
    # TODO: Implement mechanics: LIFESTEAL
    # TODO: Implement Questline mechanic
    # play = ...

class SW_092:
    """安纳塞隆 / Anetheron
    Costs (1) if your hand is full."""
    pass

