"""
决战荒芜之地 - 中立 - LEGENDARY
"""
from ..utils import *


class DEEP_036:
    """塞拉赞恩 - Therazane
    [x]Taunt  Deathrattle: Double the stats of all Elementals in your hand and deck.
    嘲讽 亡语：使你手牌和牌库中的所有元素牌属性值翻倍。
    """
    # 亡语：使手牌和牌库中的所有元素牌属性值翻倍
    deathrattle = (Buff(FRIENDLY_HAND + ELEMENTAL, "DEEP_036e"), Buff(FRIENDLY_DECK + ELEMENTAL, "DEEP_036e"))


class DEEP_036e:
    """塞拉赞恩增益 - 属性值翻倍"""
    def apply(self, target):
        # 保存目标当前的攻击力和生命值,然后翻倍
        self._doubled_atk = target.atk * 2
        self._doubled_health = target.health * 2
    
    tags = {
        GameTag.ATK: lambda self, i: getattr(self, '_doubled_atk', i * 2),
        GameTag.HEALTH: lambda self, i: getattr(self, '_doubled_health', i * 2),
    }


class DEEP_037:
    """玛鲁特·缚石 - Maruut Stonebinder
    [x]Battlecry: If your deck started with no duplicates, Discover an Elemental to summon. Add the others to your hand.
    战吼：如果你的套牌里没有相同的牌，发现一个元素并召唤，并将其他的置入你的手牌。
    """
    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK)

    def play(self):
        if self.powered_up:
            # 从卡牌数据库中获取所有可收集的元素随从
            from fireplace.cards import db
            elemental_cards = db.filter(
                type=CardType.MINION,
                race=Race.ELEMENTAL,
                collectible=True
            )
            
            if len(elemental_cards) >= 3:
                # 随机选择3张元素随从
                import random
                selected_ids = random.sample(elemental_cards, 3)
                
                # 让玩家从3张中选择1张
                discovered = yield GenericChoice(CONTROLLER, selected_ids)
                
                if discovered:
                    chosen_id = discovered[0]
                    
                    # 召唤被选中的元素
                    yield Summon(CONTROLLER, chosen_id)
                    
                    # 将其他未被选中的元素置入手牌
                    for card_id in selected_ids:
                        if card_id != chosen_id:
                            yield Give(CONTROLLER, card_id)


class WW_0700:
    """孤胆游侠雷诺 - Reno, Lone Ranger
    [x]Battlecry: If your deck started with no duplicates, remove all enemy minions from the game.
    战吼：如果你的套牌里没有相同的牌，将所有敌方随从移出对战。
    """
    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK)

    def play(self):
        if self.powered_up:
            # 将所有敌方随从移出对战（设置为 REMOVEDFROMGAME 区域）
            for minion in self.controller.opponent.field:
                minion.zone = Zone.REMOVEDFROMGAME


class WW_359:
    """桶沿警长 - Sheriff Barrelbrim
    Battlecry: If you have 20 or less Health, open the Badlands Jail.
    战吼：如果你的生命值小于或等于20点，开启荒芜之地监狱。
    """
    def play(self):
        # 检查生命值是否小于或等于20点
        if self.controller.hero.health <= 20:
            # 开启荒芜之地监狱（召唤监狱地标）
            # 荒芜之地监狱：地标，耐久度3，使一个随从休眠3回合
            yield Summon(CONTROLLER, "WW_359t")


class WW_379:
    """弗林特·枪臂 - Flint Firearm
    [x]Battlecry: Get a random Quickdraw card. If you play it this turn, repeat this.
    战吼：随机获取一张快枪牌。如果你在本回合使用获取的牌，重复此效果。
    """
    def play(self):
        # 从卡牌数据库中获取所有快枪牌
        from fireplace.cards import db
        quickdraw_cards = [
            card_id for card_id in db.keys()
            if db[card_id].tags.get(GameTag.QUICKDRAW, False) and db[card_id].collectible
        ]
        
        if quickdraw_cards:
            # 随机选择一张快枪牌
            import random
            card_id = random.choice(quickdraw_cards)
            
            # 给予玩家这张牌
            cards = yield Give(CONTROLLER, card_id)
            
            # 给获取的牌添加追踪 Buff，实现连锁效果
            if cards:
                for card in cards:
                    yield Buff(card, "WW_379e")


class WW_379e:
    """弗林特·枪臂追踪增益 - 标记这张牌是弗林特给的"""
    # 当这张特定的牌被使用时，重复弗林特的效果
    def handle_play(self, source, player, card, *args):
        """处理卡牌使用事件"""
        # 获取所有快枪牌
        from fireplace.cards import db
        quickdraw_cards = [
            card_id for card_id in db.keys()
            if db[card_id].tags.get(GameTag.QUICKDRAW, False) and db[card_id].collectible
        ]
        
        if quickdraw_cards:
            # 随机选择一张快枪牌
            import random
            card_id = random.choice(quickdraw_cards)
            
            # 给予玩家这张牌
            new_cards = yield Give(CONTROLLER, card_id)
            
            # 给新获取的牌也施加追踪增益，实现连锁效果
            if new_cards:
                for new_card in new_cards:
                    yield Buff(new_card, "WW_379e")
    
    events = Play(CONTROLLER, SELF).after(handle_play)


class WW_421:
    """帮派头领普德 - Kingpin Pud
    Battlecry: Resurrect your Ogre-Gang. Give them Windfury.
    战吼：复活你的食人魔帮众，使其获得风怒。
    """
    def play(self):
        # 复活食人魔帮众（从墓地复活所有食人魔随从）
        # 先给英雄施加一个临时增益，用于追踪即将召唤的食人魔
        yield Buff(FRIENDLY_HERO, "WW_421t")

        # 复活墓地中的所有食人魔
        yield Summon(CONTROLLER, Copy(FRIENDLY_GRAVEYARD + MINION + OGRE))


class WW_421t:
    """帮派头领普德临时追踪增益"""
    # 当召唤食人魔时，给予风怒
    events = Summon(CONTROLLER, MINION + OGRE).after(
        (Buff(Summon.CARD, "WW_421e"), Destroy(SELF))
    )



class WW_421e:
    """帮派头领普德增益 - 风怒"""
    tags = {
        GameTag.WINDFURY: True,
    }


class WW_440:
    """奔雷骏马 - Thunderbringer
    [x]Taunt Deathrattle: Summon an Elemental and Beast from your deck.
    嘲讽 亡语：从你的牌库中召唤一个元素和一只野兽。
    """
    # 亡语：从牌库中召唤一个元素和一只野兽
    deathrattle = (Recruit(ELEMENTAL), Recruit(BEAST))


