"""
漫游翡翠梦境 - 中立 - RARE
"""
from ..utils import *
import random


class EDR_001:
    """满怀希望的树妖 - Hopeful Dryad
    Battlecry: Get a random Dream card.
    
    3费 3/3 随从
    战吼:随机获取一张梦境牌。
    """
    def play(self):
        # 随机获取一张梦境牌
        # 梦境牌包括:梦境、梦魇、翡翠梦境、笑声、醒梦等
        dream_cards = [
            "DREAM_01",  # 梦境 Dream
            "DREAM_02",  # 梦魇 Nightmare
            "DREAM_03",  # 翡翠梦境 Emerald Dream
            "DREAM_04",  # 笑声 Laughing Sister
            "DREAM_05",  # 醒梦 Ysera Awakens
        ]
        yield Give(CONTROLLER, random.choice(dream_cards))


class EDR_110:
    """孢子尖牙怪 - Sporegnasher
    Poisonous. Deathrattle: Deal 1 damage to a random enemy minion.
    
    5费 1/5 随从
    剧毒。亡语:随机对一个敌方随从造成1点伤害。
    """
    tags = {
        GameTag.POISONOUS: True,
    }
    
    def deathrattle(self):
        # 随机对一个敌方随从造成1点伤害
        enemy_minions = list(self.controller.opponent.field)
        if enemy_minions:
            yield Hit(random.choice(enemy_minions), 1)


class EDR_260:
    """幻影绿翼龙 - Illusory Greenwing
    Taunt. Deathrattle: Shuffle two 4/5 Dragons with Taunt into your deck. They're Summoned When Drawn.
    
    4费 4/5 龙
    嘲讽。亡语:将两张4/5并具有嘲讽的龙洗入你的牌库。抽到时召唤。
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    def deathrattle(self):
        # 将两张4/5龙洗入牌库
        for _ in range(2):
            yield Shuffle(CONTROLLER, "EDR_260t")


class EDR_484:
    """食腐捕蝇草 - Scavenging Flytrap
    After a minion dies, gain its Attack.
    
    7费 2/7 随从
    在一个随从死亡后,获得其攻击力。
    """
    # 监听随从死亡事件
    events = Death(ALL_MINIONS).on(
        lambda self, source, target: [
            Buff(SELF, "EDR_484e", atk_bonus=target.atk)
        ] if target.type == CardType.MINION else []
    )


class EDR_873:
    """林地特使 - Envoy of the Glade
    Battlecry: Transform all Neutral cards in your deck into random Druid ones.
    
    5费 5/5 随从
    战吼:将你牌库中的所有中立卡牌变形为随机德鲁伊卡牌。
    """
    def play(self):
        # 找到牌库中的所有中立卡牌
        neutral_cards = [c for c in self.controller.deck if c.card_class == CardClass.NEUTRAL]
        
        for card in neutral_cards:
            # 变形为随机德鲁伊卡牌
            # 根据卡牌类型选择对应的德鲁伊卡牌
            if card.type == CardType.MINION:
                new_card = RandomCollectible(card_class=CardClass.DRUID, card_type=CardType.MINION)
            elif card.type == CardType.SPELL:
                new_card = RandomCollectible(card_class=CardClass.DRUID, card_type=CardType.SPELL)
            else:
                continue
            
            yield Morph(card, new_card)


class FIR_921:
    """花木护侍 - Petal Picker
    Battlecry: If you've Imbued your Hero Power twice, draw 2 cards.
    
    3费 3/3 随从
    战吼:如果你已经灌注了你的英雄技能两次,抽2张牌。
    """
    def play(self):
        # 检查是否已经灌注了英雄技能两次
        if getattr(self.controller, 'imbue_level', 0) >= 2:
            # 抽2张牌
            yield Draw(CONTROLLER) * 2


# Enchantments


class EDR_484e:
    """食腐捕蝇草攻击力增益"""
    def __init__(self, *args, atk_bonus=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk_bonus = atk_bonus
    
    @property
    def atk(self):
        return self.atk_bonus
