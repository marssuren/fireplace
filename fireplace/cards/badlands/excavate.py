from ..utils import *

# ========================================
# Sheriff Barrelbrim Token
# ========================================

class WW_359t:
    """荒芜之地监狱 - Badlands Jail
    地标，耐久度3。使一个随从休眠3回合。
    Location with 3 Durability. Make a minion go Dormant for 3 turns.
    """
    # 地标的激活效果：使目标随从休眠3回合
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def activate(self):
        # 使目标休眠3回合
        yield Buff(TARGET, "WW_359te")


class WW_359te:
    """休眠3回合"""
    tags = {GameTag.DORMANT: True}
    # 3回合后苏醒
    events = OWN_TURN_BEGIN.on(
        AddProgress(OWNER, OWNER, 1),
        (Count(OWNER) >= 3) & (
            SetTags(OWNER, {GameTag.DORMANT: False}),
            Destroy(SELF),
        )
    )


# ========================================
# Tier 1 Excavate Treasures (1 Mana, Common)
# ========================================

class WW_001t:
    """岩石 - Rock
    造成$3点伤害。
    Deal $3 damage.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)


class WW_001t18:
    """钱袋 - Pouch of Coins
    获得两个幸运币。
    Give you two Coins.
    """
    play = Give(CONTROLLER, "GAME_005") * 2  # The Coin


class WW_001t2:
    """水源 - Water Source
    恢复#3点生命值并抽一张牌。
    Restore 3 Health and draw a card.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        yield Heal(TARGET, 3)
        yield Draw(CONTROLLER)


class WW_001t3:
    """愚人艾泽里特 - Fool's Azerite
    发现一张法力值消耗为（2）点的卡牌，其法力值消耗为（0）点。
    Discover a 2-Cost card. It costs (0).
    """
    def play(self):
        # 发现一张2费卡牌
        card = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RandomCollectible(cost=2))
        )
        if card:
            # 将卡牌加入手牌并设置费用为0
            yield Give(CONTROLLER, card)
            if card in self.controller.hand:
                yield Buff(card, "WW_001t3e")


class WW_001t3e:
    """法力值消耗为0"""
    tags = {GameTag.COST: SET(0)}


class WW_001t4:
    """逃跑的穴居人 - Escaping Trogg
    2/2 突袭随从
    """
    rush = True


class DEEP_999t1:
    """心花 - Heartblossom
    使一个友方随从获得+2/+2，对一个随机敌方随从造成$2点伤害。
    Give a friendly minion +2/+2. Deal $2 damage to a random enemy minion.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0}
    
    def play(self):
        # 给友方随从+2/+2
        yield Buff(TARGET, "DEEP_999t1e")
        # 对随机敌方随从造成2点伤害
        yield Hit(RANDOM(ENEMY_MINIONS), 2)


class DEEP_999t1e:
    """+2/+2 增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


# ========================================
# Tier 2 Excavate Treasures (2 Mana, Rare)
# ========================================

class DEEP_999t2:
    """深岩之洲晶簇 - Deepholm Geode
    2/4 嘲讽元素，亡语：召唤一个随机法力值消耗为（2）点的随从。
    2/4 Taunt Elemental. Deathrattle: Summon a random 2-Cost minion.
    """
    taunt = True
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=2))


class WW_001t16:
    """活石 - Living Stone
    2/4 嘲讽元素，亡语：召唤一个随机法力值消耗为（2）点的随从。
    2/4 Taunt Elemental. Deathrattle: Summon a random 2-Cost minion.
    """
    taunt = True
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=2))


class WW_001t5:
    """坠落钟乳石 - Falling Stalactite
    对一个随从和敌方英雄造成$3点伤害。
    Deal $3 damage to a minion and the enemy hero.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        yield Hit(TARGET, 3)
        yield Hit(ENEMY_HERO, 3)


class WW_001t7:
    """金丝雀 - Canary
    2/1 野兽，战吼：将一个敌方随从移回其拥有者的手牌。
    2/1 Beast. Battlecry: Return an enemy minion to its owner's hand.
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_ENEMY_TARGET: 0}
    play = Bounce(TARGET)


class WW_001t8:
    """发光雕文 - Glowing Glyph
    使一个随从及其相邻随从获得+1/+2。
    Give a minion and its neighbors +1/+2.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 给目标及其相邻随从+1/+2
        yield Buff(TARGET + TARGET_ADJACENT, "WW_001t8e")


class WW_001t8e:
    """+1/+2 增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class WW_001t9:
    """艾泽里特碎块 - Azerite Chunk
    发现一张法力值消耗为（3）点的卡牌，其法力值消耗为（0）点。
    Discover a 3-Cost card. It costs (0).
    """
    def play(self):
        # 发现一张3费卡牌
        card = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RandomCollectible(cost=3))
        )
        if card:
            # 将卡牌加入手牌并设置费用为0
            yield Give(CONTROLLER, card)
            if card in self.controller.hand:
                yield Buff(card, "WW_001t9e")


class WW_001t9e:
    """法力值消耗为0"""
    tags = {GameTag.COST: SET(0)}


# ========================================
# Tier 3 Excavate Treasures (3 Mana, Epic)
# ========================================

class DEEP_999t3:
    """世界之柱碎片 - World Pillar Fragment
    发现一个元素并召唤它，然后获得两个元素。
    Discover an Elemental to summon. Add 2 Elementals to your hand.
    """
    def play(self):
        # 发现一个元素并召唤
        elemental = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RandomMinion(race=Race.ELEMENTAL))
        )
        if elemental:
            yield Summon(CONTROLLER, elemental)
        
        # 获得2个随机元素到手牌
        yield Give(CONTROLLER, RandomMinion(race=Race.ELEMENTAL)) * 2


class WW_001t11:
    """食人魔之拳巨石 - Ogrefist Boulder
    地标，耐久度2。将一个随从的属性设置为6/7。
    Location with 2 Durability. Set a minion's stats to 6/7.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def activate(self):
        # 将目标随从的属性设置为6/7
        yield Buff(TARGET, "WW_001t11e")


class WW_001t11e:
    """属性设置为6/7"""
    def apply(self, target):
        target.atk = 6
        target.max_health = 7
        target.damage = 0


class WW_001t12:
    """坍塌！ - Collapse!
    对所有敌人造成$3点伤害。
    Deal $3 damage to all enemies.
    """
    play = Hit(ENEMY_CHARACTERS, 3)


class WW_001t13:
    """钢皮鼹鼠 - Steelhide Mole
    2/7 嘲讽野兽，复生，无法被法术或英雄技能指定。
    2/7 Taunt Beast. Reborn. Can't be targeted by spells or Hero Powers.
    """
    taunt = True
    reborn = True
    tags = {GameTag.CANT_BE_TARGETED_BY_SPELLS: True, GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True}


class WW_001t14:
    """艾泽里特宝石 - Azerite Gem
    发现一张法力值消耗为（5）点的卡牌，其法力值消耗为（0）点。
    Discover a 5-Cost card. It costs (0).
    """
    def play(self):
        # 发现一张5费卡牌
        card = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RandomCollectible(cost=5))
        )
        if card:
            # 将卡牌加入手牌并设置费用为0
            yield Give(CONTROLLER, card)
            if card in self.controller.hand:
                yield Buff(card, "WW_001t14e")


class WW_001t14e:
    """法力值消耗为0"""
    tags = {GameTag.COST: SET(0)}


class WW_001t17:
    """母矿幼龙 - Motherlode Drake
    4/3 龙，突袭，圣盾，吸血。
    4/3 Dragon. Rush, Divine Shield, Lifesteal.
    """
    rush = True
    divine_shield = True
    lifesteal = True


# ========================================
# Tier 4 Excavate Treasures (4 Mana, Legendary, Class-Specific)
# 所有都是 5/5 元素+野兽双种族随从
# ========================================

class DEEP_999t4:
    """艾泽里特龙 - The Azerite Dragon (Paladin)
    5/5 元素+龙，战吼：使你手牌、牌库和战场上的所有其他随从获得+3/+3。
    5/5 Elemental Dragon. Battlecry: Give all other minions in your hand, deck, and battlefield +3/+3.
    """
    def play(self):
        # 给手牌、牌库和战场上的所有其他随从+3/+3
        yield Buff(FRIENDLY_HAND + MINION - SELF, "DEEP_999t4e")
        yield Buff(FRIENDLY_DECK + MINION, "DEEP_999t4e")
        yield Buff(FRIENDLY_MINIONS - SELF, "DEEP_999t4e")


class DEEP_999t4e:
    """+3/+3 增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class DEEP_999t5:
    """艾泽里特鱼人 - The Azerite Murloc (Shaman)
    5/5 元素+鱼人，战吼：将你手牌和牌库中的所有其他随从变形成为法力值消耗多（3）点的随机随从。
    5/5 Elemental Murloc. Battlecry: Transform all other minions in your hand and deck into random ones that cost (3) more.
    """
    def play(self):
        # 变形手牌中的其他随从
        for card in list(self.controller.hand):
            if card != self and card.type == CardType.MINION:
                new_cost = card.cost + 3
                yield Morph(card, RandomMinion(cost=new_cost))
        
        # 变形牌库中的随从
        for card in list(self.controller.deck):
            if card.type == CardType.MINION:
                new_cost = card.cost + 3
                yield Morph(card, RandomMinion(cost=new_cost))


class WW_001t23:
    """艾泽里特蝎子 - The Azerite Scorpion (Rogue)
    5/5 野兽+元素，战吼：将4张随机法术牌置入你的手牌。如果你已发掘过8次，这些法术牌的法力值消耗为（0）点。
    5/5 Beast Elemental. Battlecry: Add 4 random spells to your hand. If you've Excavated 8 times, they cost (0).
    """
    def play(self):
        # 检查是否已发掘8次
        excavated_8_times = self.controller.times_excavated >= 8
        
        # 获得4张随机法术
        for _ in range(4):
            card = yield Give(CONTROLLER, RandomSpell())
            # 如果已发掘8次，设置费用为0
            if card and excavated_8_times and card in self.controller.hand:
                yield Buff(card, "WW_001t23e")


class WW_001t23e:
    """法力值消耗为0"""
    tags = {GameTag.COST: SET(0)}


class WW_001t24:
    """艾泽里特鹰 - The Azerite Hawk (Mage)
    5/5 野兽+元素，战吼：将一张随机泰坦牌置入你的手牌，其法力值消耗为（1）点。
    5/5 Beast Elemental. Battlecry: Add a random Titan to your hand that costs (1).
    """
    def play(self):
        # 获得一张随机泰坦牌
        # 泰坦牌的标记是 TITAN 标签
        card = yield Give(CONTROLLER, RandomCard(titan=True))
        if card and card in self.controller.hand:
            # 设置费用为1
            yield Buff(card, "WW_001t24e")


class WW_001t24e:
    """法力值消耗为1"""
    tags = {GameTag.COST: SET(1)}


class WW_001t25:
    """艾泽里特蛇 - The Azerite Snake (Warlock)
    5/5 元素+野兽，战吼：你的英雄从敌方英雄处偷取10点生命值（同时增加你的最大生命值）。
    5/5 Elemental Beast. Battlecry: Your hero steals 10 Health from the enemy hero.
    """
    def play(self):
        # 从敌方英雄偷取10点生命值
        # 这会同时增加己方英雄的最大生命值
        yield Steal(FRIENDLY_HERO, ENEMY_HERO, 10)


class WW_001t26:
    """艾泽里特老鼠 - The Azerite Rat (Death Knight)
    5/5 野兽+元素，战吼：复活你法力值消耗最高的随从，使其获得+2/+2，复生和吸血。
    5/5 Beast Elemental. Battlecry: Resurrect your highest Cost minion. Give it +2/+2, Reborn, and Lifesteal.
    """
    def play(self):
        # 复活法力值消耗最高的随从
        minion = yield Summon(CONTROLLER, Copy(FRIENDLY + KILLED + MINION + HIGHEST_COST))
        if minion:
            # 给予+2/+2，复生和吸血
            yield Buff(minion, "WW_001t26e")


class WW_001t26e:
    """+2/+2，复生和吸血"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.REBORN: True,
        GameTag.LIFESTEAL: True
    }


class WW_001t27:
    """艾泽里特公牛 - The Azerite Ox (Warrior)
    5/5 野兽+元素，战吼：发现两个法力值消耗为（8）点的随从并召唤它们。
    5/5 Beast Elemental. Battlecry: Discover two 8-Cost minions and summon them.
    """
    def play(self):
        # 发现第一个8费随从
        minion1 = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RandomMinion(cost=8))
        )
        if minion1:
            yield Summon(CONTROLLER, minion1)
        
        # 发现第二个8费随从
        minion2 = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, RandomMinion(cost=8))
        )
        if minion2:
            yield Summon(CONTROLLER, minion2)

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
