"""
决战荒芜之地 - DRUID
"""
from ..utils import *


# COMMON

class DEEP_028:
    """晶体结积 - Crystal Cluster
    获得三个空的法力水晶，每有一个超过上限的法力水晶，召唤一个3/7并具有嘲讽的元素。
    """
    # Type: SPELL | Cost: 7 | Rarity: COMMON
    
    def play(self):
        # 计算当前法力水晶和最大法力水晶
        current_max_mana = self.controller.max_mana
        
        # 尝试获得3个空法力水晶
        overflow_count = 0
        for i in range(3):
            if current_max_mana + i + 1 > 10:
                # 超过上限，记录溢出数量
                overflow_count += 1
            else:
                # 可以获得，增加空法力水晶
                yield GainEmptyMana(CONTROLLER, 1)
        
        # 每个溢出的法力水晶召唤一个3/7嘲讽元素
        if overflow_count > 0:
            yield Summon(CONTROLLER, "DEEP_028t") * overflow_count


class DEEP_028t:
    """晶簇元素 - Crystal Elemental"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 7,
        GameTag.TAUNT: True,
        GameTag.CARDRACE: Race.ELEMENTAL,
    }


class DEEP_029:
    """穴居人宝石投掷者 - Trogg Gemtosser
    压轴：你每有一个法力水晶，随机对一个敌人造成1点伤害。
    """
    # Type: MINION | Cost: 3 | Rarity: COMMON | Stats: 3/2
    
    def play(self):
        # Finale: 手牌打空时触发
        is_finale = len(self.controller.hand) == 0
        if is_finale:
            # 每个法力水晶造成1点伤害
            mana_crystals = self.controller.max_mana
            for i in range(mana_crystals):
                yield Hit(RANDOM(ENEMY_CHARACTERS), 1)


class WW_816:
    """飞向天空 - Take to the Skies
    抽两张龙牌，使其获得+1/+1。
    """
    # Type: SPELL | Cost: 2 | Rarity: COMMON
    
    def play(self):
        # 抽两张龙牌
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + DRAGON) * 2
        # 给抽到的龙牌+1/+1
        for card_list in cards:
            if card_list:
                for card in card_list:
                    if card:
                        yield Buff(card, "WW_816e")


class WW_816e:
    """+1/+1 增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class WW_820:
    """棘尾幼龙 - Spinetail Drake
    战吼：如果你的手牌中有龙牌，则对一个敌方随从造成5点伤害。
    """
    # Type: MINION | Cost: 4 | Rarity: COMMON | Stats: 5/4 | Race: DRAGON
    # Mechanics: BATTLECRY
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0}
    powered_up = HOLDING_DRAGON
    
    play = powered_up & Hit(TARGET, 5)


class WW_823:
    """补水 - Rehydrate
    恢复#7点生命值。快枪：复原两个法力水晶。
    """
    # Type: SPELL | Cost: 2 | Rarity: COMMON | Mechanics: QUICKDRAW
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    
    def play(self):
        # 恢复7点生命值
        yield Heal(self.target, 7)
        
        # 快枪：本回合获得并立即使用时触发
        if self.drawn_this_turn:
            yield FillMana(CONTROLLER, 2)



# RARE

class DEEP_027:
    """暗石守卫 - Gloomstone Guardian
    嘲讽。抉择：弃两张牌；或者摧毁你的一个法力水晶。锻造：无需弃牌或摧毁。
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 6/8 | Race: ELEMENTAL
    # Mechanics: CHOOSE_ONE, FORGE, TAUNT
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("DEEP_027a", "DEEP_027b")
    
    def play(self):
        if self.choice == "DEEP_027a":
            # 弃两张牌
            yield Discard(RANDOM(FRIENDLY_HAND) * 2)
        elif self.choice == "DEEP_027b":
            # 摧毁一个法力水晶
            yield DestroyMana(CONTROLLER, 1)


class DEEP_027a:
    """弃牌 - Discard"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class DEEP_027b:
    """摧毁法力水晶 - Destroy Mana"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class DEEP_027t:
    """暗石守卫 - Gloomstone Guardian (Forged)
    嘲讽。锻造版本：无需代价。
    6/8 Taunt Elemental (Forged). No cost required.
    """
    # 锻造版本：6/8 嘲讽元素，无需弃牌或摧毁法力水晶
    taunt = True
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 8,
        GameTag.CARDRACE: Race.ELEMENTAL,
        GameTag.CARDTYPE: CardType.MINION
    }
    # 锻造版本没有战吼，直接召唤即可


class WW_818:
    """仙人掌构造术 - Cactus Construct
    发现一张法力值消耗为（2）的随从牌，召唤一个它的1/2的复制。
    """
    # Type: SPELL | Cost: 1 | Rarity: RARE | Mechanics: DISCOVER
    
    def play(self):
        # 发现一张2费随从
        yield Discover(CONTROLLER, RandomMinion(cost=2)).then(
            Give(CONTROLLER, Discover.CARD),
            # 召唤一个1/2的复制
            Summon(CONTROLLER, ExactCopy(Discover.CARD)).then(
                Buff(Summon.CARD, "WW_818e")
            )
        )


class WW_818e:
    """1/2 属性设置"""
    def apply(self, target):
        target.atk = 1
        target.max_health = 2
        target.damage = 0


class WW_819:
    """戏水雏龙 - Splish-Splash Whelp
    战吼：如果你的手牌中有龙牌，获得一个空的法力水晶。
    """
    # Type: MINION | Cost: 2 | Rarity: RARE | Stats: 2/1 | Race: DRAGON
    # Mechanics: BATTLECRY
    powered_up = HOLDING_DRAGON
    
    play = powered_up & GainEmptyMana(CONTROLLER, 1)


class WW_826:
    """沙漠巢母 - Desert Nestmatron
    嘲讽。战吼：如果你的手牌中有龙牌，复原四个法力水晶。
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 3/5 | Race: DRAGON
    # Mechanics: BATTLECRY, TAUNT
    powered_up = HOLDING_DRAGON
    
    play = powered_up & FillMana(CONTROLLER, 4)


# EPIC

class WW_821:
    """巨龙传说 - Dragon Tales
    抉择：获取两张法力值消耗小于或等于（5）点的随机龙牌；或者获取两张法力值消耗大于（5）点的随机龙牌。
    """
    # Type: SPELL | Cost: 2 | Rarity: EPIC | Mechanics: CHOOSE_ONE
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("WW_821a", "WW_821b")
    
    def play(self):
        if self.choice == "WW_821a":
            # 获取两张≤5费的龙牌
            yield Give(CONTROLLER, RandomDragon(max_cost=5)) * 2
        elif self.choice == "WW_821b":
            # 获取两张>5费的龙牌
            yield Give(CONTROLLER, RandomDragon(min_cost=6)) * 2


class WW_821a:
    """小龙 - Small Dragons"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class WW_821b:
    """大龙 - Large Dragons"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class WW_822:
    """巨龙魔像 - Dragon Golem
    嘲讽。战吼：你手牌中每有一张龙牌，召唤一个本随从的复制。
    """
    # Type: MINION | Cost: 7 | Rarity: EPIC | Stats: 3/4 | Race: DRAGON
    # Mechanics: BATTLECRY, TAUNT
    
    def play(self):
        # 计算手牌中的龙牌数量
        dragon_count = len([c for c in self.controller.hand if hasattr(c, 'races') and Race.DRAGON in c.races])
        # 召唤对应数量的复制
        if dragon_count > 0:
            yield Summon(CONTROLLER, ExactCopy(SELF)) * dragon_count


# LEGENDARY

class WW_824:
    """瑞亚丝塔萨 - Rheastrasza
    战吼：如果你的套牌里没有相同的牌，则召唤纯净龙巢。
    """
    # Type: MINION | Cost: 8 | Rarity: LEGENDARY | Stats: 8/8 | Race: DRAGON
    # Mechanics: BATTLECRY
    
    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK + FRIENDLY_HAND + FRIENDLY_HERO)
    
    play = powered_up & Summon(CONTROLLER, "WW_824t")


class WW_824t:
    """纯净龙巢 - Purified Dragon Nest
    在你的回合结束时，召唤一条随机龙。
    """
    # Type: LOCATION | Cost: 0 | Health: 3
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 0,
        GameTag.HEALTH: 3,
    }
    
    # 地标的被动效果：回合结束时召唤龙
    events = OWN_TURN_END.on(
        Summon(CONTROLLER, RandomDragon())
    )




class WW_825:
    """落日灵龙菲伊 - Fye, the Setting Sun
    突袭。吸血。嘲讽。在本局对战中，你每召唤一条龙，本牌的法力值消耗便减少（1）点。
    """
    # Type: MINION | Cost: 9 | Rarity: LEGENDARY | Stats: 4/12 | Race: DRAGON
    # Mechanics: LIFESTEAL, RUSH, TAUNT
    
    # 每召唤一条龙减1费
    events = Summon(CONTROLLER, DRAGON).on(Buff(SELF, "WW_825e"))


class WW_825e:
    """法力值消耗减少"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }



