# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立普通
"""

from ..utils import *


class DED_523:
    """葛拉卡蟹杀手 / Golakka Glutton
    战吼：消灭一个野兽并获得+1/+1。"""
    play = Find(ENEMY_MINIONS + BEAST) & (
        (Destroy(TARGET), Buff(SELF, "DED_523e"))
    )


class DED_523e:
    """葛拉卡蟹杀手增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_006:
    """顽固的嫌疑人 / Stubborn Suspect
    亡语：召唤一个随机的法力值消耗为（3）的随从。"""
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=3))


class SW_054:
    """暴风城卫兵 / Stormwind Guard
    嘲讽 战吼：使相邻的随从获得+1/+1。"""
    play = Buff(SELF_ADJACENT, "SW_054e")


class SW_054e:
    """暴风城卫兵增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_055:
    """不耐烦的店长 / Impatient Shopkeep
    可交易 突袭"""
    pass  # Tradeable 和 Rush 在 CardDefs.xml 中定义


class SW_056:
    """香料面包师 / Spice Bread Baker
    战吼：为你的英雄恢复等同于你手牌数量的生命值。"""
    play = Heal(FRIENDLY_HERO, Count(FRIENDLY_HAND))


class SW_057:
    """包裹速递员 / Package Runner
    只有在你的手牌中至少有8张牌时才能攻击。"""
    update = Refresh(SELF, {GameTag.CANT_ATTACK: Count(FRIENDLY_HAND) < 8})


class SW_059:
    """矿道工程师 / Deeprun Engineer
    战吼：发现一张机械牌。其法力值消耗减少（1）点。"""
    def play(self):
        discovered = yield Discover(CONTROLLER, RandomCollectible(race=Race.MECHANICAL))
        if discovered:
            yield Buff(discovered[0], "SW_059e")


class SW_059e:
    """矿道工程师减费"""
    cost = -1


class SW_060:
    """卖花女郎 / Florist
    在你的回合结束时，使你手牌中一张自然法术牌的法力值消耗减少（1）点。"""
    events = OWN_TURN_END.on(
        Find(FRIENDLY_HAND + SPELL + NATURE) & Buff(RANDOM(FRIENDLY_HAND + SPELL + NATURE), "SW_060e")
    )


class SW_060e:
    """卖花女郎减费"""
    cost = -1


class SW_061:
    """公会商人 / Guild Trader
    可交易 法术伤害+2"""
    pass  # Tradeable 和 Spell Damage 在 CardDefs.xml 中定义


class SW_063:
    """战场军官 / Battleground Battlemaster
    相邻的随从具有风怒。"""
    update = Refresh(SELF_ADJACENT, {GameTag.WINDFURY: True})


class SW_064:
    """北郡农民 / Northshire Farmer
    战吼：选择一个友方野兽。将三张3/3的复制洗入你的牌库。"""
    play = Find(FRIENDLY_MINIONS + BEAST) & (
        Shuffle(CONTROLLER, Copy(TARGET)) * 3
    )


class SW_065:
    """熊猫人进口商 / Pandaren Importer
    战吼：发现一张不在你初始牌组中的法术牌。"""
    # 发现一张不在初始牌组中的法术
    play = Discover(CONTROLLER, RandomSpell())


class SW_066:
    """王室图书管理员 / Royal Librarian
    可交易 战吼：沉默一个随从。"""
    play = Silence(TARGET)


class SW_067:
    """监狱守卫 / Stockades Guard
    战吼：使一个友方随从获得嘲讽。"""
    play = (Find(FRIENDLY_MINIONS), SetTags(TARGET, {GameTag.TAUNT: True}))


class SW_068:
    """莫尔葛熔魔 / Mo'arg Forgefiend
    嘲讽 亡语：获得8点护甲值。"""
    deathrattle = GainArmor(FRIENDLY_HERO, 8)


class SW_071:
    """雄狮卫士 / Lion's Guard
    战吼：如果你的生命值小于或等于15点，获得+2/+4和嘲讽。"""
    play = Find(FRIENDLY_HERO + (CURRENT_HEALTH <= 15)) & (
        (Buff(SELF, "SW_071e"), SetTags(SELF, {GameTag.TAUNT: True}))
    )


class SW_071e:
    """雄狮卫士增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
    }


class SW_072:
    """锈烂蝰蛇 / Rustrot Viper
    可交易 战吼：摧毁你对手的武器。"""
    play = Destroy(ENEMY_WEAPON)


class SW_076:
    """城市建筑师 / City Architect
    战吼：召唤两个0/5并具有嘲讽的城墙。"""
    play = Summon(CONTROLLER, "SW_076t") * 2


class SW_076t:
    """城墙 / Castle Wall"""
    # 0/5 嘲讽随从，在 CardDefs.xml 中定义


class SW_307:
    """旅行商人 / Traveling Merchant
    可交易 战吼：每有一个其他友方随从，便获得+1/+1。"""
    play = Buff(SELF, "SW_307e") * Count(FRIENDLY_MINIONS - SELF)


class SW_307e:
    """旅行商人增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_319:
    """农夫 / Peasant
    在你的回合开始时，抽一张牌。"""
    events = OWN_TURN_BEGIN.on(Draw(CONTROLLER))


class SW_418:
    """军情七处潜伏者 / SI:7 Skulker
    潜行 战吼：你抽到的下一张牌法力值消耗减少（1）点。"""
    play = Buff(CONTROLLER, "SW_418e")


class SW_418e:
    """军情七处潜伏者减费"""
    update = Refresh(FRIENDLY_HAND, {"cost": -1})
    events = Draw(CONTROLLER).on(Destroy(SELF))
