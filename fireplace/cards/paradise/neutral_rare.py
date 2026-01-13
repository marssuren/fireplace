"""
胜地历险记 - 中立 - RARE
"""
from ..utils import *


# ========== VAC_438 - 旅行社职员 ==========
class VAC_438:
    """旅行社职员 - Travel Agent
    战吼：发现一张任意职业的地标牌。
    Battlecry: Discover a location from any class.
    """
    # 2费 2/2 海盗
    mechanics = [GameTag.BATTLECRY, GameTag.DISCOVER]
    race = Race.PIRATE
    
    def play(self):
        # 发现一张任意职业的地标牌
        yield Discover(CONTROLLER, RandomCollectible(type=CardType.LOCATION))


# ========== VAC_440 - 海关执法者 ==========
class VAC_440:
    """海关执法者 - Customs Enforcer
    敌方套牌之外的敌方卡牌法力值消耗增加（2）点。
    Enemy cards that didn't start in their deck cost (2) more.
    """
    # 3费 2/5 海盗
    mechanics = [GameTag.AURA]
    race = Race.PIRATE
    
    # 使用 update 来影响敌方手牌
    # 对于不在起始套牌中的敌方卡牌，增加2费
    update = Refresh(ENEMY_HAND - STARTING_DECK, {GameTag.COST: +2})


# ========== VAC_441 - 包裹分拣工 ==========
class VAC_441:
    """包裹分拣工 - Parcel Handler
    在你抽牌后，有50%的几率再抽一张。
    After you draw a card, 50% chance to draw another.
    """
    # 6费 6/7
    
    def on_draw(self, target, card):
        """当玩家抽牌后触发"""
        # 50%几率再抽一张
        if self.game.random.random() < 0.5:
            yield Draw(CONTROLLER)
    
    # 监听玩家抽牌
    events = Draw(CONTROLLER).after(
        lambda self, target, card: self.on_draw(target, card)
    )


# ========== VAC_521 - 笨拙的搬运工 ==========
class VAC_521:
    """笨拙的搬运工 - Clumsy Courier
    嘲讽。战吼：如果你的手牌中有法力值消耗大于或等于（5）点的法术牌，召唤一个本随从的复制。
    Taunt. Battlecry: If you have a spell that costs (5) or more, summon a copy of this.
    """
    # 3费 3/3 亡灵+海盗
    mechanics = [GameTag.BATTLECRY, GameTag.TAUNT]
    races = [Race.UNDEAD, Race.PIRATE]
    
    def play(self):
        # 检查手牌中是否有5费或以上的法术
        has_expensive_spell = any(
            card.type == CardType.SPELL and card.cost >= 5
            for card in self.controller.hand
        )
        
        if has_expensive_spell:
            # 召唤一个本随从的复制
            yield Summon(CONTROLLER, ExactCopy(SELF))


# ========== VAC_936 - 八爪按摩机 ==========
class VAC_936:
    """八爪按摩机 - Octosari Massager
    对随从造成八倍伤害。
    Deals 8 times damage to minions.
    
    实现说明：
    - 当这个随从攻击随从时，在正常伤害之外额外造成7倍攻击力的伤害
    - 总伤害 = 1倍（正常）+ 7倍（额外）= 8倍
    """
    # 4费 1/8 机械+野兽
    races = [Race.MECHANICAL, Race.BEAST]
    
    # 监听自己攻击随从的事件
    # 在攻击后额外造成7倍攻击力的伤害
    events = Attack(SELF, MINION).after(
        lambda self, attacker, defender: Hit(defender, attacker.atk * 7)
    )


# ========== WORK_040 - 笨拙的杂役 ==========
class WORK_040:
    """笨拙的杂役 - Clumsy Waiter
    在任意卡牌被抽到后，将其变为临时卡牌。
    After a card is drawn, make it Temporary.
    """
    # 3费 2/4
    
    def on_draw(self, target, card):
        """当任意玩家抽牌后触发"""
        # 将抽到的牌变为临时卡牌
        # 临时卡牌：在回合结束时消失
        if card:
            yield Buff(card, "WORK_040e")
    
    # 监听任意玩家抽牌
    events = Draw(ALL_PLAYERS).after(
        lambda self, target, card: self.on_draw(target, card)
    )


class WORK_040e:
    """笨拙的杂役 - 临时卡牌效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.GHOSTLY: True  # 临时卡牌标记
    }
    
    # 回合结束时移除卡牌
    events = OWN_TURN_END.on(
        Destroy(OWNER)
    )
