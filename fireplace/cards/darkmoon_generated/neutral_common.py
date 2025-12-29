from ..utils import *


##
# Minions

class DMF_044:
    """Rock Rager (岩石暴怒者)
    Taunt"""

    # TODO: Implement mechanics: TAUNT

class DMF_062:
    """Gyreworm (旋岩虫)
    Battlecry: If you played an Elemental last turn, deal 3 damage."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_065:
    """Banana Vendor (香蕉商贩)
    Battlecry: Add 2 Bananas to each player's hand."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_066:
    """Knife Vendor (小刀商贩)
    Battlecry: Deal 4 damage to each hero."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_067:
    """Prize Vendor (奖品商贩)
    Battlecry and Deathrattle: Each player draws a card."""

    # TODO: Implement mechanics: BATTLECRY, DEATHRATTLE
    # TODO: Implement Battlecry effect
    # play = ...
    # TODO: Implement Deathrattle effect
    # deathrattle = ...

class DMF_068:
    """Optimistic Ogre (乐观的食人魔)
    50% chance to attack the correct enemy."""

    # TODO: Implement mechanics: FORGETFUL

class DMF_069:
    """Claw Machine (娃娃机)
    Rush. Deathrattle: Draw a minion and give it +3/+3."""

    # TODO: Implement mechanics: DEATHRATTLE, RUSH
    # TODO: Implement Deathrattle effect
    # deathrattle = ...

class DMF_073:
    """Darkmoon Dirigible (暗月飞船)
    Divine Shield Corrupt: Gain Rush."""

    # TODO: Implement mechanics: CORRUPT, DIVINE_SHIELD
    # TODO: Implement Corrupt effect
    # corrupt = ...

class DMF_078:
    """Strongman (大力士)
    Taunt Corrupt: This costs (0)."""

    # TODO: Implement mechanics: CORRUPT, TAUNT
    # TODO: Implement Corrupt effect
    # corrupt = ...

class DMF_079:
    """Inconspicuous Rider (低调的游客)
    Battlecry: Cast a Secret from your deck."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_080:
    """Fleethoof Pearltusk (迅蹄珠齿象)
    Rush Corrupt: Gain +4/+4."""

    # TODO: Implement mechanics: CORRUPT, RUSH
    # TODO: Implement Corrupt effect
    # corrupt = ...

class DMF_082:
    """Darkmoon Statue (暗月雕像)
    Your other minions have +1 Attack. Corrupt: This gains +4 Attack."""

    # TODO: Implement mechanics: AURA, CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...

class DMF_091:
    """Wriggling Horror (蠕动的恐魔)
    Battlecry: Give adjacent minions +1/+1."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_174:
    """Circus Medic (马戏团医师)
    Battlecry: Restore #4 Health. Corrupt: Deal 4 damage instead."""

    # TODO: Implement mechanics: BATTLECRY, CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_189:
    """Costumed Entertainer (盛装演员)
    Battlecry: Give a random minion in your hand +2/+2."""

    # TODO: Implement mechanics: BATTLECRY
    # TODO: Implement Battlecry effect
    # play = ...

class DMF_190:
    """Fantastic Firebird (炫目火鸟)
    Windfury"""

    # TODO: Implement mechanics: WINDFURY

class DMF_191:
    """Showstopper (砸场游客)
    Deathrattle: Silence all minions."""

    # TODO: Implement mechanics: DEATHRATTLE
    # TODO: Implement Deathrattle effect
    # deathrattle = ...

class DMF_520:
    """Parade Leader (巡游领队)
    After you summon a Rush minion, give it +2 Attack."""

    # TODO: Implement mechanics: TRIGGER_VISUAL

class DMF_532:
    """Circus Amalgam (马戏团融合怪)
    Taunt This has all minion types."""

    # TODO: Implement mechanics: TAUNT

class YOP_021:
    """Imprisoned Phoenix (被禁锢的凤凰)
    Dormant for 2 turns. Spell Damage +2"""

    # TODO: Implement mechanics: SPELLPOWER

class YOP_030:
    """Felfire Deadeye (邪火神射手)
    Your Hero Power costs (1) less."""

    # TODO: Implement mechanics: AURA

class YOP_031:
    """Crabrider (螃蟹骑士)
    Rush Windfury"""

    # TODO: Implement mechanics: RUSH, WINDFURY


##
# Spells

class YOP_005:
    """Barricade (路障)
    Summon a 2/4 Guard with Taunt. If it's your only minion, summon another."""

    # TODO: Implement spell effect
    # play = ...

class YOP_015:
    """Nitroboost Poison (氮素药膏)
    Give a minion +2 Attack. Corrupt: And your weapon."""

    # TODO: Implement mechanics: CORRUPT
    # TODO: Implement Corrupt effect
    # corrupt = ...
    # TODO: Implement spell effect
    # play = ...

class YOP_029:
    """Resizing Pouch (随心口袋)
    Discover a card with Cost equal to your remaining Mana Crystals."""

    # TODO: Implement mechanics: DISCOVER
    # TODO: Implement spell effect
    # play = ...
