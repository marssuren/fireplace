from fireplace.card import Minion, Spell, Location
from fireplace.enums import Race, CardClass

# Tier 1
class WW_001t(Spell): # Rock
    pass
class WW_001t18(Spell): # Pouch of Coins
    pass
class WW_001t2(Spell): # Water Source
    pass
class WW_001t3(Spell): # Fool's Azerite
    pass
class WW_001t4(Minion): # Escaping Trogg
    pass
class DEEP_999t1(Spell): # Heartblossom
    pass

# Tier 2
class DEEP_999t2(Minion): # Deepholm Geode
    pass
class WW_001t16(Minion): # Living Stone
    pass
class WW_001t5(Spell): # Falling Stalactite
    pass
class WW_001t7(Minion): # Canary
    pass
class WW_001t8(Spell): # Glowing Glyph
    pass
class WW_001t9(Spell): # Azerite Chunk
    pass

# Tier 3
class DEEP_999t3(Spell): # World Pillar Fragment
    pass
class WW_001t11(Location): # Ogrefist Boulder
    pass
class WW_001t12(Spell): # Collapse!
    pass
class WW_001t13(Minion): # Steelhide Mole
    pass
class WW_001t14(Spell): # Azerite Gem
    pass
class WW_001t17(Minion): # Motherlode Drake
    pass

# Tier 4
class DEEP_999t4(Minion): # Azerite Dragon (Paladin)
    pass
class DEEP_999t5(Minion): # Azerite Murloc (Shaman)
    pass
class WW_001t23(Minion): # Azerite Scorpion (Rogue)
    pass
class WW_001t24(Minion): # Azerite Hawk (Mage)
    pass
class WW_001t25(Minion): # Azerite Snake (Warlock)
    pass
class WW_001t26(Minion): # Azerite Rat (DK)
    pass
class WW_001t27(Minion): # Azerite Ox (Warrior)
    pass

TIER_1_IDS = ['WW_001t', 'WW_001t18', 'WW_001t2', 'WW_001t3', 'WW_001t4', 'DEEP_999t1']
TIER_2_IDS = ['DEEP_999t2', 'WW_001t16', 'WW_001t5', 'WW_001t7', 'WW_001t8', 'WW_001t9']
TIER_3_IDS = ['DEEP_999t3', 'WW_001t11', 'WW_001t12', 'WW_001t13', 'WW_001t14', 'WW_001t17']

# Map CardClass enum to Tier 4 Treasure ID
TIER_4_IDS = {
    CardClass.PALADIN: 'DEEP_999t4',
    CardClass.SHAMAN: 'DEEP_999t5',
    CardClass.ROGUE: 'WW_001t23',
    CardClass.MAGE: 'WW_001t24',
    CardClass.WARLOCK: 'WW_001t25',
    CardClass.DEATHKNIGHT: 'WW_001t26',
    CardClass.WARRIOR: 'WW_001t27'
}
