
"""
穿越时间流 - HUNTER
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_601:
    """拾箭龙鹰 - Arrow Retriever
    3/1 野兽
    **战吼：**抽牌，直到你拥有三张手牌。
    
    Battlecry: Draw until you have 3 cards.
    """
    # Mechanics: BATTLECRY
    def play(self):
        # 抽牌直到手牌数量达到3张
        while len(self.controller.hand) < 3:
            yield Draw(self.controller)


class TIME_603:
    """计时炸弹 - Ticking Timebomb
    1/1 机械
    **亡语：**随机消灭一个敌方随从。
    
    Deathrattle: Destroy a random enemy minion.
    """
    # Mechanics: DEATHRATTLE
    deathrattle = Destroy(RANDOM_ENEMY_MINION)


class TIME_605:
    """纪元追猎者 - Epoch Stalker
    3/4 野兽
    **突袭。扰魔**
    **战吼：**召唤一个本随从的复制。
    
    Rush, Elusive. Battlecry: Summon a copy of this.
    """
    # Mechanics: BATTLECRY, ELUSIVE, RUSH
    # Rush 和 Elusive 由卡牌定义中的标签处理
    def play(self):
        # 召唤自身的复制
        yield Summon(self.controller, ExactCopy(SELF))


# RARE

class TIME_602:
    """虫洞 - Wormhole
    3费 法术
    **回溯**。随机召唤一只法力值消耗为（3）的野兽并使其攻击随机敌人。

    Rewind. Summon a random 3-Cost Beast. It attacks a random enemy.
    """
    # Mechanics: REWIND
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 召唤一只随机3费野兽
            minion = yield Summon(self.controller, RandomMinion(cost=3, race=Race.BEAST))

            # 使其攻击随机敌人
            if minion and ENEMY_CHARACTERS:
                yield Attack(minion[0], RANDOM(ENEMY_CHARACTERS))

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_606:
    """奎尔多雷造箭师 - Quel'dorei Fletcher
    1/3
    当你的手牌少于或等于三张时，你的英雄技能的法力值消耗为（0）点。
    
    Your Hero Power costs (0) while your hand has 3 or less cards.
    """
    # Mechanics: AURA
    # 参考 TOY_381 (纸艺天使) 的实现
    class Hand:
        """在手牌时也生效的光环"""
        update = Refresh(FRIENDLY_HERO_POWER, {
            GameTag.COST: lambda self, i: 0 if len(self.controller.hand) <= 3 else i
        })
    
    update = Refresh(FRIENDLY_HERO_POWER, {
        GameTag.COST: lambda self, i: 0 if len(self.controller.hand) <= 3 else i
    })


# EPIC

class TIME_600:
    """精确射击 - Precise Shot
    2费 法术
    造成$3点伤害。如果本牌位于你手牌的正中间，改为造成$5点。
    
    Deal $3 damage. If this is EXACTLY in the center of your hand, deal $5 instead.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 检查是否在手牌正中间
        hand = self.controller.hand
        hand_size = len(hand)
        is_center = False
        
        # 如果手牌为奇数张，检查是否在正中间
        if hand_size % 2 == 1 and hand_size > 0:
            try:
                card_index = hand.index(self)
                center_index = hand_size // 2
                is_center = (card_index == center_index)
            except ValueError:
                is_center = False
        
        # 根据位置造成不同伤害
        damage = 5 if is_center else 3
        yield Hit(TARGET, damage)


# LEGENDARY

class TIME_042:
    """穆拉克 - King Maluk
    5/6 野兽
    **战吼：**弃掉你的手牌。获取一张无穷香蕉。
    
    Battlecry: Discard your hand. Get an Infinite Banana.
    """
    # Mechanics: BATTLECRY
    def play(self):
        # 弃掉所有手牌
        # 注意：战吼触发时，穆拉克已经在场上，不在手牌中
        # 所以 FRIENDLY_HAND 不包含穆拉克自己
        yield Discard(FRIENDLY_HAND)
        
        # 获取一张无穷香蕉
        yield Give(self.controller, "TIME_042t")


class TIME_609:
    """游侠将军希尔瓦娜斯 - Ranger General Sylvanas
    2/4 传说
    **奇闻**
    **战吼：**对所有敌人造成2点伤害。如果你使用过奥蕾莉亚或温蕾萨，每使用过一位，重复一次。
    
    Fabled. Battlecry: Deal 2 damage to all enemies. If you've played Alleria or Vereesa, repeat for each.
    """
    # Mechanics: BATTLECRY, FABLED
    def play(self):
        # 基础效果：对所有敌人造成2点伤害
        yield Hit(ENEMY_CHARACTERS, 2)
        
        # 检查是否使用过奥蕾莉亚（Alleria）或温蕾萨（Vereesa）
        # 这些是 Fabled 附带卡牌
        played_alleria = False
        played_vereesa = False
        
        # 检查已打出的卡牌
        for card in self.controller.cards_played_this_game:
            if card.id == "TIME_609t1":  # Alleria
                played_alleria = True
            elif card.id == "TIME_609t2":  # Vereesa
                played_vereesa = True
        
        # 每使用过一位，重复一次效果
        if played_alleria:
            yield Hit(ENEMY_CHARACTERS, 2)
        
        if played_vereesa:
            yield Hit(ENEMY_CHARACTERS, 2)
