"""
深暗领域 - DEATHKNIGHT
"""
from ..utils import *


# COMMON

class GDB_475:
    """近轨血月 - Orbital Moon
    1费 法术 - 血符文x2
    使一个随从获得<b>嘲讽</b>和<b>吸血</b>。如果你在本回合中使用过相邻的牌，还会使其获得<b>复生</b>。
    
    Give a minion Taunt and Lifesteal. If you played an adjacent card this turn, also give it Reborn.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 给予嘲讽和吸血
        yield Buff(TARGET, "GDB_475e")
        
        # 检查本回合是否使用过相邻的牌
        # 获取本牌在手牌中的位置（在打出前记录）
        my_position = None
        for card, position in self.controller.cards_played_this_turn_with_position:
            if card == self:
                my_position = position
                break
        
        if my_position is not None:
            # 检查是否有相邻位置的牌被打出
            for card, position in self.controller.cards_played_this_turn_with_position:
                if card != self:  # 排除自己
                    # 检查是否相邻（位置差为1）
                    if abs(position - my_position) == 1:
                        # 找到相邻的牌，给予复生
                        yield Buff(TARGET, "GDB_475e2")
                        break  # 只需要找到一张相邻的牌即可


class GDB_475e:
    """近轨血月 - 嘲讽吸血 Buff"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_475e2:
    """近轨血月 - 复生 Buff"""
    tags = {
        GameTag.REBORN: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_476:
    """难以喘息 - Suffocate
    4费 法术
    消灭一个随从。如果你正在构筑<b>星舰</b>，还会消灭一个随机相邻随从。
    
    Destroy a minion. If you're building a Starship, also destroy a random neighbor.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        target_minion = TARGET.entity
        
        # 如果正在构筑星舰，先获取相邻随从（在目标被消灭前）
        neighbors = []
        if self.controller.starship_in_progress and target_minion and target_minion.zone == Zone.PLAY:
            # 使用 adjacent_minions 属性获取相邻随从
            neighbors = list(target_minion.adjacent_minions)
        
        # 消灭目标随从
        yield Destroy(TARGET)
        
        # 如果有相邻随从，随机消灭一个
        if neighbors:
            neighbor = self.game.random.choice(neighbors)
            # 检查相邻随从是否还在场上（可能已被其他效果移除）
            if neighbor.zone == Zone.PLAY:
                yield Destroy(neighbor)


class GDB_478:
    """凋零同化 - Assimilating Blight
    3费 法术 - 血符文x1 + 邪符文x2
    <b>发现</b>并召唤一个法力值消耗为（3）的<b>亡语</b>随从，并使其具有<b>复生</b>。
    
    Discover a 3-Cost Deathrattle minion. Summon it with Reborn.
    """
    def play(self):
        # 发现一个3费亡语随从
        cards = yield DISCOVER(RandomCollectible(cost=3, type=CardType.MINION, deathrattle=True))
        
        if cards:
            # 召唤发现的随从
            minion = yield Summon(CONTROLLER, cards[0])
            
            # 给予复生
            if minion:
                yield Buff(minion[0], "GDB_478e")


class GDB_478e:
    """凋零同化 - 复生 Buff"""
    tags = {
        GameTag.REBORN: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class SC_001:
    """爆虫冲锋 - Baneling Barrage
    1费 法术
    获取一张1/1且会爆炸的爆虫。如果你控制着异虫随从，再获取一张爆虫。
    
    Get a 1/1 Baneling that explodes. If you control a Zerg minion, get another Baneling.
    """
    def play(self):
        # 获取一张爆虫
        yield Give(CONTROLLER, "SC_001t")
        
        # 如果控制异虫随从，再获取一张
        if self.controller.field.filter(race=Race.ZERG):
            yield Give(CONTROLLER, "SC_001t")


# RARE

class GDB_112:
    """魂缚尖塔 - Soulbound Spire
    3费 2/2 死亡骑士随从 - 星舰组件
    <b>亡语：</b>召唤一个法力值消耗等同于本随从攻击力的随从（最高不超过10点）。
    <b>星舰组件</b>
    
    Deathrattle: Summon a minion with Cost equal to this minion's Attack (up to 10). Starship Piece
    """
    mechanics = [GameTag.DEATHRATTLE, GameTag.STARSHIP_PIECE]
    
    def deathrattle(self):
        # 召唤一个法力值消耗等同于本随从攻击力的随从（最高不超过10点）
        cost = min(self.atk, 10)
        yield Summon(CONTROLLER, RandomCollectible(cost=cost, type=CardType.MINION))


class GDB_113:
    """气闸破损 - Airlock Breach
    6费 法术 - 血符文x1 + 邪符文x1
    召唤一个5/5并具有<b>嘲讽</b>的亡灵，并使你的英雄获得+5生命值。消耗5份<b>残骸</b>，重复一次。
    
    Summon a 5/5 Undead with Taunt and give your hero +5 Health. Spend 5 Corpses to do it again.
    """
    def play(self):
        # 召唤一个5/5嘲讽亡灵
        yield Summon(CONTROLLER, "GDB_113t")
        
        # 英雄获得+5生命值
        yield GainMaxHealth(FRIENDLY_HERO, 5)
        yield Heal(FRIENDLY_HERO, 5)
        
        # 如果有5份残骸，消耗并重复一次
        if self.controller.corpses >= 5:
            yield SpendCorpses(CONTROLLER, 5)
            yield Summon(CONTROLLER, "GDB_113t")
            yield GainMaxHealth(FRIENDLY_HERO, 5)
            yield Heal(FRIENDLY_HERO, 5)


class GDB_468:
    """灵魂唤醒者 - Wakener of Souls
    10费 8/7 死亡骑士随从 - 邪符文x1
    <b>嘲讽</b>。<b>复生</b>
    <b>亡语：</b>复活一个不同的友方<b>亡语</b>随从。
    
    Taunt, Reborn. Deathrattle: Resurrect a different friendly Deathrattle minion.
    """
    mechanics = [GameTag.TAUNT, GameTag.REBORN, GameTag.DEATHRATTLE]
    
    def deathrattle(self):
        # 复活一个不同的友方亡语随从
        # 从本局对战中死亡的友方亡语随从中随机选择一个（不包括自己）
        dead_deathrattle_minions = [
            card for card in self.controller.graveyard
            if card.type == CardType.MINION 
            and card != self 
            and (hasattr(card, 'deathrattles') and card.deathrattles or GameTag.DEATHRATTLE in card.tags)
        ]
        
        if dead_deathrattle_minions:
            target = self.game.random.choice(dead_deathrattle_minions)
            yield Summon(CONTROLLER, target.id)


class SC_002:
    """感染者 - Infestor
    3费 4/2 死亡骑士随从
    <b>亡语：</b>在本局对战的剩余时间内，你的异虫随从拥有+1攻击力。
    
    Deathrattle: Your Zerg minions have +1 Attack for the rest of the game.
    """
    mechanics = [GameTag.DEATHRATTLE]
    deathrattle = Buff(CONTROLLER, "SC_002e")


class SC_002e:
    """感染者 - 异虫+1攻 Buff (Player Aura)
    "For the rest of the game" 效果影响所有区域的异虫随从
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 对所有友方异虫随从生效的永久 Aura（手牌、牌库、场上）
    update = Refresh(FRIENDLY_MINIONS + ZERG)
    
    class Hand:
        # 手牌中的异虫随从获得 +1 攻击力
        def atk(self, i):
            if self.owner.race == Race.ZERG:
                return i + 1
            return i
    
    class Deck:
        # 牌库中的异虫随从获得 +1 攻击力
        def atk(self, i):
            if self.owner.race == Race.ZERG:
                return i + 1
            return i
    
    class Board:
        # 场上的异虫随从获得 +1 攻击力
        def atk(self, i):
            if self.owner.race == Race.ZERG:
                return i + 1
            return i


class SC_018:
    """飞蛇 - Viper
    4费 5/3 死亡骑士随从
    <b>战吼：</b>从你对手的手牌中召唤一个随从，你的其他异虫随从获得<b>复生</b>并攻击该随从。
    
    Battlecry: Summon a minion from your opponent's hand. Your other Zerg minions gain Reborn and attack it.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 从对手手牌中随机选择一个随从
        opponent_minions = [c for c in self.controller.opponent.hand if c.type == CardType.MINION]
        
        if opponent_minions:
            target_card = self.game.random.choice(opponent_minions)
            
            # 召唤该随从到对手场上
            summoned = yield Summon(self.controller.opponent, target_card)
            
            if summoned:
                summoned_minion = summoned[0]
                
                # 获取所有其他异虫随从
                zerg_minions = [m for m in self.controller.field if m.race == Race.ZERG and m != self]
                
                for zerg in zerg_minions:
                    # 给予复生
                    yield Buff(zerg, "SC_018e")
                    
                    # 攻击召唤的随从
                    if summoned_minion.zone == Zone.PLAY:
                        yield Attack(zerg, summoned_minion)


class SC_018e:
    """飞蛇 - 复生 Buff"""
    tags = {
        GameTag.REBORN: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# EPIC

class GDB_106:
    """引航舰首像 - Guiding Figure
    3费 3/2 死亡骑士随从 - 星舰组件
    <b><b>法术迸发</b>：</b>触发一个随机友方随从的<b>亡语</b>。
    <b>星舰组件</b>
    
    Spellburst: Trigger a random friendly minion's Deathrattle. Starship Piece
    """
    mechanics = [GameTag.SPELLBURST, GameTag.STARSHIP_PIECE]
    
    # 法术迸发：触发一个随机友方随从的亡语
    events = Spellburst(CONTROLLER, Deathrattle(RANDOM_FRIENDLY_MINION))


class GDB_469:
    """奥金尼亡语者 - Auchenai Death-Speaker
    1费 1/3 死亡骑士随从 - 邪符文x1
    在另一个友方随从<b>复生</b>后，召唤一个它的复制。
    
    After another friendly minion is Reborn, summon a copy of it.
    """
    # 监听友方随从召唤事件
    # 核心引擎会为复生召唤的随从设置 is_reborn_summon 标记
    events = Summon(CONTROLLER, MINION).after(
        lambda self, source, card: (
            # 检查是否是复生召唤：
            # 1. 不是自己
            # 2. 有 is_reborn_summon 标记（由核心引擎设置）
            card != self 
            and hasattr(card, 'is_reborn_summon')
            and card.is_reborn_summon
            and Summon(CONTROLLER, Copy(card))
        )
    )


class GDB_470:
    """大主教玛拉达尔 - Exarch Maladaar
    6费 5/5 死亡骑士随从 - 邪符文x1
    <b>战吼：</b>在本回合中，你使用的下一张牌会消耗<b>残骸</b>而非法力值。
    
    Battlecry: The next card you play this turn costs Corpses instead of Mana.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 设置玩家的残骸支付标志
        # 核心引擎会在下一张牌打出时检查此标志并消耗残骸
        self.controller.next_card_costs_corpses = True


class GDB_477:
    """深暗八爪怪 - The 8 Hands From Beyond
    8费 8/8 死亡骑士随从 - 血符文x2
    <b>战吼：</b>摧毁双方玩家牌库中除各自法力值消耗最高的8张牌之外的牌。
    
    Battlecry: Destroy both players' decks EXCEPT the 8 highest Cost cards in each.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 处理双方玩家的牌库
        for player in [self.controller, self.controller.opponent]:
            # 获取牌库中的所有牌
            deck_cards = list(player.deck)
            
            if len(deck_cards) > 8:
                # 按费用排序（降序）
                deck_cards.sort(key=lambda c: c.cost, reverse=True)
                
                # 保留费用最高的8张牌
                cards_to_keep = deck_cards[:8]
                cards_to_destroy = deck_cards[8:]
                
                # 摧毁其余的牌
                for card in cards_to_destroy:
                    yield Mill(card)


