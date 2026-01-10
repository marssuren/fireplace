"""
胜地历险记 - PALADIN
"""
from ..utils import *


# ========== COMMON ==========

class WORK_002:
    """忙碌机器人 - Busy-Bot
    Battlecry: Give your 1-Attack minions +1/+1.
    战吼:使你攻击力为1的随从获得+1/+1。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给所有攻击力为1的友方随从+1/+1
        for minion in self.controller.field:
            if minion.atk == 1:
                yield Buff(minion, "WORK_002e")


class WORK_002e:
    """忙碌机器人增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class VAC_921:
    """沙滩排槌 - Volley Maul
    After your hero attacks, get a 1-Cost Sunscreen that gives +1/+2.
    在你的英雄攻击后，获取一张法力值消耗为(1)的防晒霜。防晒霜可以使随从获得+1/+2。
    """
    # 武器效果：英雄攻击后触发
    events = Attack(FRIENDLY_HERO).after(
        Give(CONTROLLER, "VAC_921t")
    )


class VAC_917:
    """烧烤大师 - Grillmaster
    Battlecry: Draw your lowest Cost card. Deathrattle: Draw your highest Cost card.
    战吼：抽取你法力值消耗最低的牌。亡语：抽取你法力值消耗最高的牌。
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DEATHRATTLE]
    
    def play(self):
        # 抽取费用最低的牌
        if self.controller.deck:
            lowest_card = min(self.controller.deck, key=lambda c: c.cost)
            yield Draw(CONTROLLER, lowest_card)
    
    def deathrattle(self):
        # 抽取费用最高的牌
        if self.controller.deck:
            highest_card = max(self.controller.deck, key=lambda c: c.cost)
            yield Draw(CONTROLLER, highest_card)


class WORK_003:
    """假期规划 - Vacation Planning
    Restore #4 Health. Summon 3 Silver Hand Recruits. Draw 2 cards.
    恢复#4点生命值。召唤3个白银之手新兵。抽两张牌。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 恢复4点生命值
        if TARGET:
            yield Heal(TARGET, 4)
        # 召唤3个白银之手新兵
        yield Summon(CONTROLLER, "CS2_101t") * 3
        # 抽两张牌
        yield Draw(CONTROLLER) * 2


class VAC_915:
    """大力扣杀 - Power Spike
    Deal $4 damage. Give a random friendly minion +4/+4.
    造成$4点伤害。随机使一个友方随从获得+4/+4。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 造成4点伤害
        if TARGET:
            yield Hit(TARGET, 4)
        
        # 随机给一个友方随从+4/+4
        friendly_minions = list(self.controller.field)
        if friendly_minions:
            target_minion = self.game.random.choice(friendly_minions)
            yield Buff(target_minion, "VAC_915e")


class VAC_915e:
    """大力扣杀增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# ========== RARE ==========

class VAC_916:
    """神圣佳酿 - Divine Brew
    Give a character Divine Shield. (3 Drinks left!)
    使一个角色获得圣盾。（还剩3杯！）
    """
    # Drink Spell: 使用后返回手牌，最多使用3次
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 给予圣盾
        if TARGET:
            yield SetTags(TARGET, {GameTag.DIVINE_SHIELD: True})
        
        # Drink Spell机制：返回2杯版本
        yield Give(CONTROLLER, "VAC_916t")


class VAC_922:
    """救生光环 - Lifesaving Aura
    At the end of your turn, get a 1-Cost Sunscreen that gives +1/+2. Lasts 3 turns.
    在你的回合结束时，获取一张法力值消耗为(1)的可以使随从获得+1/+2的防晒霜。持续3回合。
    """
    def play(self):
        # 给玩家添加一个持续3回合的效果
        yield Buff(CONTROLLER, "VAC_922e")


class VAC_922e:
    """救生光环效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 持续3回合（在3个回合结束时触发效果）
        self.turns_remaining = 3
    
    # 回合结束时给予防晒霜并倒计时
    def on_turn_end(self):
        """回合结束时触发"""
        # 先给予防晒霜
        yield Give(CONTROLLER, "VAC_921t")
        # 然后倒计时
        self.turns_remaining -= 1
        # 如果倒计时结束，移除此效果
        if self.turns_remaining <= 0:
            yield Destroy(SELF)
    
    events = OWN_TURN_END.on(
        lambda self, source: self.on_turn_end()
    )


class VAC_919:
    """救生员 - Lifeguard
    Taunt. Battlecry: Your next spell has Lifesteal.
    嘲讽。战吼：你施放的下一个法术拥有吸血。
    """
    mechanics = [GameTag.TAUNT, GameTag.BATTLECRY]
    
    def play(self):
        # 给玩家添加效果：下一个法术拥有吸血
        yield Buff(CONTROLLER, "VAC_919e")


class VAC_919e:
    """救生员效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听施放法术，给予吸血效果
    events = Play(CONTROLLER, SPELL).on(
        lambda self, source, card: [
            Buff(card, "VAC_919e2"),
            Destroy(SELF)  # 施放法术后移除此效果
        ]
    )


class VAC_919e2:
    """法术吸血效果"""
    tags = {
        GameTag.LIFESTEAL: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class WORK_001:
    """信任背摔 - Trust Fall
    Discover two minions that cost (5) or less. They gain each other's Attack and Health.
    发现两张法力值消耗小于或等于(5)点的随从牌，并使其获得彼此的攻击力和生命值。
    """
    mechanics = [GameTag.DISCOVER]
    
    def play(self):
        # 第一次发现
        first_discovered = yield Discover(CONTROLLER, RandomCollectible(type=CardType.MINION, cost_max=5))
        
        if first_discovered:
            first_minion = first_discovered[0]
            first_atk = first_minion.atk
            first_health = first_minion.max_health
            
            # 第二次发现
            second_discovered = yield Discover(CONTROLLER, RandomCollectible(type=CardType.MINION, cost_max=5))
            
            if second_discovered:
                second_minion = second_discovered[0]
                second_atk = second_minion.atk
                second_health = second_minion.max_health
                
                # 交换属性值
                # 第一个随从获得第二个随从的攻击力和生命值
                yield Buff(first_minion, "WORK_001e", atk_value=second_atk, health_value=second_health)
                # 第二个随从获得第一个随从的攻击力和生命值
                yield Buff(second_minion, "WORK_001e", atk_value=first_atk, health_value=first_health)


class WORK_001e:
    """信任背摔属性交换效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 从参数中获取属性值
        if 'atk_value' in kwargs:
            self.atk = kwargs['atk_value']
        if 'health_value' in kwargs:
            self.max_health = kwargs['health_value']


# ========== EPIC ==========

class VAC_920:
    """王牌发球手 - Service Ace
    After this minion gains Attack, reduce the Cost of the highest Cost card in your hand by (1).
    在本随从获得攻击力后，使你手牌中法力值消耗最高的牌的法力值消耗减少(1)点。
    """
    # 监听本随从获得攻击力
    def on_buff_applied(self, source, buff):
        """当本随从获得增益时触发"""
        # 检查是否获得了攻击力
        if hasattr(buff, 'atk') and buff.atk > 0:
            # 找到手牌中费用最高的牌
            if self.controller.hand:
                highest_card = max(self.controller.hand, key=lambda c: c.cost)
                yield Buff(highest_card, "VAC_920e")
    
    # 监听增益事件
    events = Buff(SELF).after(
        lambda self, source, buff: self.on_buff_applied(source, buff)
    )


class VAC_920e:
    """王牌发球手减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost = -1


class VAC_558:
    """海上船歌 - Sea Shanty
    Summon three 5/5 Pirates. Costs (1) less for each spell you've cast on characters this game.
    召唤三个5/5的海盗。在本局对战中，你每对角色施放一个法术，本牌的法力值消耗便减少(1)点。
    """
    def play(self):
        # 召唤3个5/5海盗
        yield Summon(CONTROLLER, "VAC_558t") * 3
    
    # 费用减免光环
    class Hand:
        """手牌中的费用减免"""
        def cost(self, i):
            # 使用核心引擎追踪的对角色施放法术数量
            spells_on_characters = self.controller.spells_cast_on_characters_this_game
            return i - spells_on_characters


# ========== LEGENDARY ==========

class VAC_507:
    """阳光汲取者莱妮莎 - Sunsapper Lynessa
    Rogue Tourist. Your spells that cost (2) or less cast twice.
    潜行者游客。你的法力值消耗小于或等于(2)点的法术会施放两次。
    """
    # 给玩家添加光环效果，使2费以下法术施放两次
    # 使用 slot_property 机制，类似 extra_battlecries
    
    # 光环效果：给玩家添加"低费法术施放两次"的标记
    auras = [
        Buff(CONTROLLER, "VAC_507e")
    ]


class VAC_507e:
    """莱妮莎光环效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 标记玩家拥有"低费法术施放两次"效果
    # 这个标记会在 Play action 中被检查
    low_cost_spells_cast_twice = True


class VAC_923:
    """圣沙泽尔 - Sanc'Azel
    Rush. After this attacks, turn into a location.
    突袭。在本随从攻击后，变成地标。
    """
    mechanics = [GameTag.RUSH]
    
    # 攻击后变形为地标
    events = Attack(SELF).after(
        Morph(SELF, "VAC_923t")
    )

