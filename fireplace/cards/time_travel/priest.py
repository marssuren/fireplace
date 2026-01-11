"""
穿越时间流 - PRIEST
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_037:
    """白鸽学徒 - Disciple of the Dove
    战吼：抽一张随从牌。使你手牌中的随从牌获得+2生命值。
    
    Battlecry: Draw a minion. Give minions in your hand +2 Health.
    """
    requirements = {}
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 抽一张随从牌
            yield ForceDraw(RANDOM(FRIENDLY_DECK + MINION))

            # 给手牌中的所有随从+2生命值
            yield Buff(FRIENDLY_HAND + MINION, "TIME_037e")

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_037e:
    """白鸽学徒 - +2生命值"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.HEALTH: 2,
    }


class TIME_431:
    """琥珀女祭司 - Amber Priestess
    嘲讽。战吼：为一个角色恢复等同于本随从生命值的生命值。
    
    Taunt. Battlecry: Restore Health to a character equal to this minion's Health.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0
    }
    
    def play(self):
        if self.target:
            # 恢复等同于本随从生命值的生命值
            # self.health 是本随从的当前生命值
            yield Heal(self.target, self.health)


class TIME_433:
    """抹除存在 - Cease to Exist
    回溯。沉默并消灭一个随机敌方随从。
    
    Rewind. Silence and destroy a random enemy minion.
    """
    requirements = {}
    
    def play(self):
        # 定义卡牌效果
        def effect():
            # 沉默并消灭一个随机敌方随从
            # 先获取所有敌方随从
            enemy_minions = list(self.controller.opponent.field)

            if enemy_minions:
                # 随机选择一个敌方随从
                target = self.game.random.choice(enemy_minions)

                # 沉默并消灭同一个目标
                yield Silence(target)
                yield Destroy(target)

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

# RARE

class TIME_427:
    """净化的光耀之子 - Cleansing Lightspawn
    吸血。战吼：对一个敌方随从造成等同于本随从生命值的伤害。
    
    Lifesteal. Battlecry: Deal damage to an enemy minion equal to this minion's Health.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        if self.target:
            # 造成等同于本随从生命值的伤害
            # self.health 是本随从的当前生命值
            yield Hit(self.target, self.health)


class TIME_432:
    """纠缠宿命 - Intertwined Fate
    从你的牌库和对手的牌库各发现一张牌的一张复制。
    
    Discover a copy of a card from your deck and one from your opponent's.
    """
    requirements = {}
    
    def play(self):
        # 从自己的牌库中发现一张牌
        yield Discover(self.controller, RANDOM(FRIENDLY_DECK))
        
        # 从对手的牌库中发现一张牌
        yield Discover(self.controller, RANDOM(ENEMY_DECK))


class TIME_447:
    """真言术：障 - Power Word: Barrier
    使一个角色获得圣盾。使你手牌中的随从牌获得+2生命值。
    
    Give a character Divine Shield. Give minions in your hand +2 Health.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0
    }
    
    def play(self):
        # 给目标角色圣盾
        yield Buff(TARGET, "divine_shield")
        
        # 给手牌中的所有随从+2生命值
        yield Buff(FRIENDLY_HAND + MINION, "TIME_447e")


class TIME_447e:
    """真言术：障 - +2生命值"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.HEALTH: 2,
    }


# EPIC

class TIME_429:
    """神圣预言师 - Divine Augur
    战吼：将你手牌中每张随从牌的攻击力和生命值变为两者中的高值。
    
    Battlecry: Set the Attack and Health of every minion in your hand to the higher of the two stats.
    """
    requirements = {}
    
    def play(self):
        # 遍历手牌中的所有随从
        for minion in self.controller.hand:
            if minion.type == CardType.MINION:
                # 获取攻击力和生命值
                atk = minion.atk
                health = minion.max_health
                
                # 取两者中的高值
                higher_value = max(atk, health)
                
                # 使用 Buff 设置攻击力和生命值为高值
                yield Buff(minion, "TIME_429e", atk=higher_value, health=higher_value)


class TIME_429e:
    """神圣预言师 - 设置攻击力和生命值"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: SetTag.SET,
        GameTag.HEALTH: SetTag.SET,
    }


class TIME_436:
    """过去的时光流汇 - Past Conflux
    随机召唤一条法力值消耗大于或等于（5）点的龙。推进到现在！
    
    Summon a random Dragon that costs (5) or more. Advance to the present!
    
    注：这是一个地标（Location）卡牌，有3个阶段：
    - 过去：召唤一条5费以上的龙
    - 现在：召唤一条5费以上的龙 + 给予其+2/+2
    - 未来：召唤一条5费以上的龙 + 给予其+4/+4
    """
    requirements = {}
    
    def activate(self):
        # 召唤一条法力值消耗大于或等于5的龙
        # 使用 RandomCollectible 选择器，指定种族为龙，费用>=5
        minion = yield Summon(
            self.controller,
            RandomCollectible(type=CardType.MINION, race=Race.DRAGON, cost_min=5)
        )


# LEGENDARY

class TIME_435:
    """伊特努丝 - Eternus
    战吼：夺取一个生命值小于或等于本随从的敌方随从的控制权。
    
    Battlecry: Take control of an enemy minion with this minion's Health or less.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        # PlayReq.REQ_TARGET_MAX_HEALTH: 2  # 这个 PlayReq 不存在，已注释
    }
    
    def play(self):
        if self.target:
            # 夺取目标随从的控制权
            yield Steal(self.target)


class TIME_890:
    """圣者麦迪文 - Medivh the Hallowed
    奇闻。如果你控制着卡拉赞，本牌的法力值消耗为（0）点。战吼：沉默并消灭所有其他随从。
    
    Fabled. Costs (0) if you control Karazhan. Battlecry: Silence and destroy all other minions.
    
    实现说明：
    - Fabled 机制在套牌构建时处理
    - 费用减免通过 cost_mod 实现
    - 战吼效果沉默并消灭所有其他随从
    """
    requirements = {}
    
    # 费用减免：如果控制卡拉赞（地标），费用为0
    # 参考 badlands/priest.py 的 WW_387 实现
    
    cost_mod = lambda self, i: -10 if any(entity.type == CardType.LOCATION and entity.id == "TIME_890t" for entity in self.controller.live_entities) else 0
    
    def play(self):
        # 沉默并消灭所有其他随从
        # 参考 badlands/neutral_legendary.py 的 WW_819 (Reno, Lone Ranger)
        # 使用选择器 ALL_MINIONS - SELF
        # 先沉默所有其他随从
        yield Silence(ALL_MINIONS - SELF)
        # 再消灭所有其他随从
        yield Destroy(ALL_MINIONS - SELF)


