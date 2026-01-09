"""
穿越时间流 - 中立 - RARE
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


class TIME_003:
    """传送门卫士 - Portal Vanguard
    回溯。战吼：随机抽一张随从牌，使其获得+2/+2。
    
    Rewind. Battlecry: Draw a random minion. Give it +2/+2.
    
    实现说明：
    - 创建回溯点
    - 从牌库中抽一张随机随从牌
    - 给抽到的随从牌+2/+2
    """
    requirements = {}
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 抽一张牌
            drawn_cards = yield Draw(self.controller)
            
            # 如果抽到了牌且是随从牌，给予+2/+2
            if drawn_cards:
                for card in drawn_cards:
                    if card.zone == Zone.HAND and card.type == CardType.MINION:
                        yield Buff(card, "TIME_003e")


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_003e:
    """传送门卫士 - +2/+2增益"""
    atk = 2
    max_health = 2


class TIME_051:
    """永恒龙士兵 - Soldier of the Infinite
    突袭。战吼：本随从的攻击力翻倍。
    
    Rush. Battlecry: Double this minion's Attack.
    
    实现说明：
    - 获取当前攻击力
    - 给予等同于当前攻击力的buff（实现翻倍效果）
    """
    requirements = {}
    
    def play(self):
        # 获取当前攻击力
        current_atk = self.atk
        
        # 给予等同于当前攻击力的攻击力buff（实现翻倍）
        if current_atk > 0:
            yield Buff(self, "TIME_051e", atk=current_atk)


class TIME_051e:
    """永恒龙士兵 - 攻击力翻倍"""
    # 动态攻击力buff，通过参数传递
    pass


class TIME_055:
    """未知旅客 - Unknown Voyager
    在本随从受到伤害并存活下来后，随机变形成为一个法力值消耗为（7）的随从。
    
    After this survives damage, transform into a random 7-Cost minion.
    
    实现说明：
    - 监听伤害事件
    - 确保随从存活（health > 0）
    - 变形为随机7费随从
    """
    events = [
        Damage(SELF).after(
            lambda self, source, target, amount: (
                self.zone == Zone.PLAY and
                self.health > 0 and
                [Morph(self, RandomMinion(cost=7))]
            )
        )
    ]


class TIME_058:
    """渺小的振翅蝶 - Paltry Flutterwing
    亡语：随机召唤一个法力值消耗为（2）并休眠2回合的随从。
    
    Deathrattle: Summon a random 2-Cost minion that is Dormant for 2 turns.
    
    实现说明：
    - 召唤随机2费随从
    - 使其休眠2回合
    - 使用SetTag设置DORMANT为2（参考TIME_063和TIME_442的实现）
    """
    def deathrattle(self):
        """动态亡语：召唤休眠的2费随从"""
        # 召唤随机2费随从
        minion = yield Summon(CONTROLLER, RandomMinion(cost=2))
        
        # 如果成功召唤，使其休眠2回合
        if minion:
            # 设置休眠回合数为2
            # 参考 TIME_063 (DORMANT: 5) 和 TIME_442 (DORMANT: 10000) 的实现
            yield SetTag(minion, {GameTag.DORMANT: 2})


class TIME_720:
    """青铜龙士兵 - Soldier of the Bronze
    嘲讽。战吼：本随从的生命值翻倍。
    
    Taunt. Battlecry: Double this minion's Health.
    
    实现说明：
    - 获取当前生命值
    - 给予等同于当前生命值的buff（实现翻倍效果）
    """
    requirements = {}
    
    def play(self):
        # 获取当前生命值
        current_health = self.health
        
        # 给予等同于当前生命值的生命值buff（实现翻倍）
        if current_health > 0:
            yield Buff(self, "TIME_720e", max_health=current_health)


class TIME_720e:
    """青铜龙士兵 - 生命值翻倍"""
    # 动态生命值buff，通过参数传递
    pass


