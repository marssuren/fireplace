"""
漫游翡翠梦境 - 中立 - COMMON
"""
from ..utils import *
from .dark_gift_helpers import apply_dark_gift
from .imbue_helpers import trigger_imbue
import random


# COMMON 卡牌


class EDR_105:
    """疯狂生物 - Creature of Madness
    Battlecry: Discover a 3-Cost minion with a Dark Gift.
    
    2费 1/2 随从
    战吼:发现一张具有黑暗之赐的法力值消耗为(3)的随从牌。
    """
    def play(self):
        # 优化实现: 在发现选项展示前应用 Dark Gift
        # 创建3个带Dark Gift的3费随从选项
        minion_filter = lambda c: (c.type == CardType.MINION and c.cost == 3)
        
        # 生成3个选项
        # 注意：这里我们生成具体的卡牌实体，而不是使用 RandomCardGenerator 产生卡牌ID
        # 这样我们可以对这些实体应用 Buff
        option1 = self.controller.card(RandomCard(CONTROLLER, card_filter=minion_filter).id)
        option2 = self.controller.card(RandomCard(CONTROLLER, card_filter=minion_filter).id)
        option3 = self.controller.card(RandomCard(CONTROLLER, card_filter=minion_filter).id)
        
        # 应用黑暗之赐
        yield apply_dark_gift(option1)
        yield apply_dark_gift(option2)
        yield apply_dark_gift(option3)
        
        # 发现机制
        yield GenericChoice(CONTROLLER, cards=[option1, option2, option3])


class EDR_254:
    """活化月亮井 - Animated Moonwell
    After you cast a spell, gain Attack equal to its Cost.
    
    3费 1/4 元素
    在你施放一个法术后,获得等同于其法力值消耗的攻击力。
    """
    # 监听法术施放事件
    events = OWN_SPELL_PLAY.after(
        lambda self, source, card: [
            Buff(SELF, "EDR_254e", atk_bonus=card.cost)
        ]
    )


class EDR_453:
    """棘嗣幼龙 - Briarspawn Drake
    At the end of your turn, attack a random enemy minion (excess damage hits the enemy hero).
    
    10费 12/7 龙
    在你的回合结束时,攻击一个随机敌方随从(超量伤害会命中敌方英雄)。
    """
    # 回合结束时攻击随机敌方随从
    events = OWN_TURN_END.on(
        lambda self: [
            Attack(SELF, RANDOM_ENEMY_MINION)
        ] if self.controller.opponent.field else []
    )


class EDR_470:
    """树皮盾哨兵 - Barkshield Sentinel
    Taunt. After you use your Hero Power, gain +2 Health.
    
    2费 2/2 随从
    嘲讽。在你使用英雄技能后,获得+2生命值。
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    # 监听英雄技能使用事件
    events = Activate(CONTROLLER, HERO_POWER).after(
        lambda self: [
            Buff(SELF, "EDR_470e")
        ]
    )


class EDR_486:
    """纵火眼魔 - Scorching Observer
    Rush. Lifesteal.
    
    9费 7/9 恶魔
    突袭。吸血。
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.LIFESTEAL: True,
    }


class EDR_492:
    """鸭妈妈 - Mother Duck
    Battlecry: Summon three 1/1 Ducklings with Rush.
    
    4费 2/3 野兽
    战吼:召唤三只1/1并具有突袭的小鸭。
    """
    def play(self):
        # 召唤3只小鸭
        for _ in range(3):
            yield Summon(CONTROLLER, "EDR_492t")


class EDR_495:
    """扭曲的树人 - Twisted Treant
    Deathrattle: Give a random minion in each player's hand -2 Attack.
    
    3费 3/3 随从
    亡语:使双方玩家手牌中的一个随机随从获得-2攻击力。
    """
    def deathrattle(self):
        # 双方玩家手牌中的随机随从获得-2攻击力
        for player in [self.controller, self.controller.opponent]:
            minions_in_hand = [c for c in player.hand if c.type == CardType.MINION]
            if minions_in_hand:
                target = random.choice(minions_in_hand)
                yield Buff(target, "EDR_495e")


class EDR_530:
    """痴梦树精 - Daydreaming Pixie
    At the end of your turn, get a random Nature spell.
    
    2费 1/3 随从
    在你的回合结束时,随机获取一张自然法术牌。
    """
    # 回合结束时获取随机自然法术
    events = OWN_TURN_END.on(
        lambda self: [
            RandomCard(
                CONTROLLER,
                card_filter=lambda c: c.type == CardType.SPELL and c.spell_school == SpellSchool.NATURE
            )
        ]
    )


class EDR_571:
    """法夜欺诈者 - Fae Trickster
    Deathrattle: Draw a spell that costs (5) or more.
    
    4费 3/4 随从
    亡语:抽取一张法力值消耗大于或等于(5)点的法术牌。
    """
    def deathrattle(self):
        # 抽取一张5费以上的法术牌
        spells_5_plus = [c for c in self.controller.deck if c.type == CardType.SPELL and c.cost >= 5]
        if spells_5_plus:
            yield ForceDraw(CONTROLLER, random.choice(spells_5_plus))


class EDR_572:
    """受难的恐翼巨龙 - Tormented Dreadwing
    Deathrattle: Draw 2 Dragons. Reduce their Costs by (1).
    
    5费 4/5 龙
    亡语:抽2张龙牌,其法力值消耗减少(1)点。
    """
    def deathrattle(self):
        # 抽2张龙牌
        dragons_in_deck = [c for c in self.controller.deck if c.type == CardType.MINION and Race.DRAGON in c.races]
        
        for _ in range(2):
            if dragons_in_deck:
                # 随机选择一张龙牌
                dragon = random.choice(dragons_in_deck)
                dragons_in_deck.remove(dragon)  # 避免重复抽取同一张
                
                # 抽取龙牌
                yield ForceDraw(CONTROLLER, dragon)
                # 减少1费
                yield Buff(dragon, "EDR_572e")


class EDR_598:
    """梦境暴怒者 - Dream Rager
    Elusive
    
    3费 5/1 随从
    扰魔。
    """
    tags = {
        GameTag.ELUSIVE: True,
    }


class EDR_800:
    """振翅守卫 - Flutterwing Guardian
    Taunt, Divine Shield. Battlecry: Imbue your Hero Power.
    
    5费 4/5 随从
    嘲讽,圣盾。战吼:灌注你的英雄技能。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DIVINE_SHIELD: True,
    }
    
    def play(self):
        # 触发 Imbue
        trigger_imbue(self.controller)


class EDR_849:
    """梦缚迅猛龙 - Dreambound Raptor
    After you play a minion, give it a random Bonus Effect.
    
    3费 3/3 野兽
    在你打出一个随从后,使其获得一个随机奖励效果。
    """
    # 监听随从打出事件
    events = Play(CONTROLLER, MINION - SELF).after(
        lambda self, source, card: [
            # 随机选择一个奖励效果
            Buff(card, random.choice([
                "EDR_849e1",  # +1/+1
                "EDR_849e2",  # 突袭
                "EDR_849e3",  # 圣盾
                "EDR_849e4",  # 嘲讽
                "EDR_849e5",  # 吸血
            ]))
        ]
    )


class EDR_852:
    """苦花骑士 - Bitterbloom Knight
    Battlecry: Imbue your Hero Power.
    
    3费 3/3 随从
    战吼:灌注你的英雄技能。
    """
    def play(self):
        # 触发 Imbue
        trigger_imbue(self.controller)


class EDR_861:
    """宁静树人 - Tranquil Treant
    Deathrattle: Both players gain an empty Mana Crystal.
    
    2费 2/2 随从
    亡语:双方玩家各获得一个空的法力水晶。
    """
    def deathrattle(self):
        # 双方玩家各获得一个空的法力水晶
        yield GainEmptyMana(CONTROLLER, 1)
        yield GainEmptyMana(OPPONENT, 1)


class EDR_889:
    """鲜花商贩 - Petal Peddler
    At the end of your turn, give another random friendly Dragon +1/+1.
    
    3费 2/4 随从
    在你的回合结束时,使另一个随机友方龙获得+1/+1。
    """
    # 回合结束时给随机友方龙+1/+1
    events = OWN_TURN_END.on(
        lambda self: [
            # 选择一个随机友方龙(不包括自己)
            Buff(
                RANDOM(FRIENDLY_MINIONS - SELF).filter(lambda c: Race.DRAGON in c.races),
                "EDR_889e"
            )
        ] if any(m != self and Race.DRAGON in m.races for m in self.controller.field) else []
    )


class EDR_942:
    """好奇的积云 - Curious Cumulus
    At the end of your turn, give your hero Divine Shield.
    
    2费 2/2 元素
    在你的回合结束时,使你的英雄获得圣盾。
    """
    # 回合结束时给英雄圣盾
    events = OWN_TURN_END.on(
        lambda self: [
            SetTags(FRIENDLY_HERO, {GameTag.DIVINE_SHIELD: True})
        ]
    )


class EDR_971:
    """小动物看护者 - Critter Caretaker
    At the end of your turn, restore #3 Health to both heroes.
    
    3费 2/4 随从
    在你的回合结束时,为双方英雄恢复3点生命值。
    """
    # 回合结束时为双方英雄恢复3点生命值
    events = OWN_TURN_END.on(
        lambda self: [
            Heal(FRIENDLY_HERO, 3),
            Heal(ENEMY_HERO, 3)
        ]
    )


class EDR_978:
    """踏青驼鹿 - Meadowstrider
    Taunt. Deathrattle: Put a Meadowstrider on the bottom of your deck. It costs (1).
    
    5费 4/4 野兽
    嘲讽。亡语:将一张法力值消耗为(1)点的踏青驼鹿置于你的牌库底。
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    def deathrattle(self):
        # 创建一张1费的踏青驼鹿
        meadowstrider = self.controller.card("EDR_978t", source=self)
        # 放到牌库底
        yield Shuffle(CONTROLLER, meadowstrider)


class EDR_999:
    """啮齿绿鳍鱼人 - Gnawing Greenfin
    Battlecry: Get a random Murloc.
    
    2费 2/3 鱼人
    战吼:随机获取一张鱼人牌。
    """
    def play(self):
        # 随机获取一张鱼人牌
        yield RandomCard(
            CONTROLLER,
            card_filter=lambda c: Race.MURLOC in c.races
        )


class FIR_929:
    """活体烈焰 - Living Flame
    Deathrattle: Draw a Fire spell.
    
    1费 1/2 元素
    亡语:抽取一张火焰法术牌。
    """
    def deathrattle(self):
        # 抽取一张火焰法术牌
        fire_spells = [c for c in self.controller.deck if c.type == CardType.SPELL and c.spell_school == SpellSchool.FIRE]
        if fire_spells:
            yield ForceDraw(CONTROLLER, random.choice(fire_spells))


# Enchantments (增益效果)


class EDR_254e:
    """活化月亮井攻击力增益"""
    def __init__(self, *args, atk_bonus=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk_bonus = atk_bonus
    
    @property
    def atk(self):
        return self.atk_bonus


class EDR_470e:
    """+2生命值"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.HEALTH: 2,
    }


class EDR_495e:
    """-2攻击力"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: -2,
    }


class EDR_572e:
    """法力值消耗减少1点"""
    cost = -1


class EDR_849e1:
    """+1/+1"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class EDR_849e2:
    """突袭"""
    tags = {GameTag.RUSH: True}


class EDR_849e3:
    """圣盾"""
    tags = {GameTag.DIVINE_SHIELD: True}


class EDR_849e4:
    """嘲讽"""
    tags = {GameTag.TAUNT: True}


class EDR_849e5:
    """吸血"""
    tags = {GameTag.LIFESTEAL: True}


class EDR_889e:
    """+1/+1"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }
