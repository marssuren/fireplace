# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立普通
"""

from ..utils import *


class DED_523:
    """葛拉卡蟹杀手 / Golakka Glutton
    Battlecry: Destroy a Beast and gain +1/+1."""
    play = Find(ENEMY_MINIONS + BEAST) & (
        Destroy(TARGET) & Buff(SELF, "DED_523e")
    )


class DED_523e:
    """葛拉卡蟹杀手增益"""
    atk = 1
    max_health = 1


class SW_006:
    """顽固的嫌疑人 / Stubborn Suspect
    Deathrattle: Summon a random 3-Cost minion."""
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=3))


class SW_054:
    """暴风城卫兵 / Stormwind Guard
    Taunt Battlecry: Give adjacent minions +1/+1."""
    play = Buff(SELF_ADJACENT, "SW_054e")


class SW_054e:
    """暴风城卫兵增益"""
    atk = 1
    max_health = 1


class SW_055:
    """不耐烦的店长 / Impatient Shopkeep
    Tradeable Rush"""
    pass  # Tradeable 和 Rush 在 CardDefs.xml 中定义


class SW_056:
    """香料面包师 / Spice Bread Baker
    Battlecry: Restore Health to your hero equal to your hand size."""
    play = Heal(FRIENDLY_HERO, Count(FRIENDLY_HAND))


class SW_057:
    """包裹速递员 / Package Runner
    Can only attack if you have at least 8 cards in hand."""
    update = Refresh(SELF, {GameTag.CANNOT_ATTACK: Count(FRIENDLY_HAND) < 8})


class SW_059:
    """矿道工程师 / Deeprun Engineer
    Battlecry: Discover a Mech. It costs (1) less."""
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomCollectible(race=Race.MECHANICAL))) & Buff(CARD, "SW_059e")


class SW_059e:
    """矿道工程师减费"""
    cost = -1


class SW_060:
    """卖花女郎 / Florist
    At the end of your turn, reduce the Cost of a Nature spell in your hand by (1)."""
    events = OwnTurnEnds(CONTROLLER).on(
        Find(FRIENDLY_HAND + SPELL + NATURE) & Buff(RANDOM(FRIENDLY_HAND + SPELL + NATURE), "SW_060e")
    )


class SW_060e:
    """卖花女郎减费"""
    cost = -1


class SW_061:
    """公会商人 / Guild Trader
    Tradeable Spell Damage +2"""
    pass  # Tradeable 和 Spell Damage 在 CardDefs.xml 中定义


class SW_063:
    """战场军官 / Battleground Battlemaster
    Adjacent minions have Windfury."""
    update = Refresh(SELF_ADJACENT, {GameTag.WINDFURY: True})


class SW_064:
    """北郡农民 / Northshire Farmer
    Battlecry: Choose a friendly Beast. Shuffle three 3/3 copies into your deck."""
    play = Find(FRIENDLY_MINIONS + BEAST) & (
        Shuffle(CONTROLLER, Copy(TARGET)) * 3
    )


class SW_065:
    """熊猫人进口商 / Pandaren Importer
    Battlecry: Discover a spell that didn't start in your deck."""
    # 发现一张不在初始牌组中的法术
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomSpell()))


class SW_066:
    """王室图书管理员 / Royal Librarian
    Tradeable Battlecry: Silence a minion."""
    play = Silence(TARGET)


class SW_067:
    """监狱守卫 / Stockades Guard
    Battlecry: Give a friendly minion Taunt."""
    play = Find(FRIENDLY_MINIONS) & SetTag(TARGET, {GameTag.TAUNT: True})


class SW_068:
    """莫尔葛熔魔 / Mo'arg Forgefiend
    Taunt Deathrattle: Gain 8 Armor."""
    deathrattle = GainArmor(FRIENDLY_HERO, 8)


class SW_071:
    """雄狮卫士 / Lion's Guard
    Battlecry: If you have 15 or less Health, gain +2/+4 and Taunt."""
    play = Find(FRIENDLY_HERO + (CURRENT_HEALTH <= 15)) & (
        Buff(SELF, "SW_071e") & SetTag(SELF, {GameTag.TAUNT: True})
    )


class SW_071e:
    """雄狮卫士增益"""
    atk = 2
    max_health = 4


class SW_072:
    """锈烂蝰蛇 / Rustrot Viper
    Tradeable Battlecry: Destroy your opponent's weapon."""
    play = Destroy(ENEMY_WEAPON)


class SW_076:
    """城市建筑师 / City Architect
    Battlecry: Summon two 0/5 Castle Walls with Taunt."""
    play = Summon(CONTROLLER, "SW_076t") * 2


class SW_076t:
    """城墙 / Castle Wall"""
    # 0/5 嘲讽随从，在 CardDefs.xml 中定义


class SW_307:
    """旅行商人 / Traveling Merchant
    Tradeable Battlecry: Gain +1/+1 for each other friendly minion you control."""
    play = Buff(SELF, "SW_307e") * Count(FRIENDLY_MINIONS - SELF)


class SW_307e:
    """旅行商人增益"""
    atk = 1
    max_health = 1


class SW_319:
    """农夫 / Peasant
    At the start of your turn, draw a card."""
    events = OwnTurnBegins(CONTROLLER).on(Draw(CONTROLLER))


class SW_418:
    """军情七处潜伏者 / SI:7 Skulker
    Stealth Battlecry: The next card you draw costs (1) less."""
    play = Buff(CONTROLLER, "SW_418e")


class SW_418e:
    """军情七处潜伏者减费"""
    update = Refresh(FRIENDLY_HAND, {"cost": -1})
    events = Draw(CONTROLLER).on(Destroy(SELF))
