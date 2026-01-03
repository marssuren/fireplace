"""
通用的"下一张卡减费" buff
用于支持锯齿骨刺、装填弹膛等卡牌
"""
from ..utils import *


class NextCardCostReduction:
    """
    通用的"下一张卡减费" buff
    
    使用方法:
        yield Buff(FRIENDLY_HERO, NextCardCostReduction(amount=2))
    
    参数:
        amount: 减费数量（正数）
    """
    def __init__(self, amount=0):
        self.cost_reduction = amount
    
    def apply(self, target):
        """应用到玩家英雄上"""
        # 增加玩家的下一张卡减费
        target.controller.next_card_cost_reduction += self.cost_reduction
    
    # 监听打出卡牌，消耗减费并移除自己
    def _consume_reduction(self, source, player, card):
        if player == self.controller and self.controller.next_card_cost_reduction > 0:
            # 重置减费
            self.controller.next_card_cost_reduction = 0
            # 移除此buff
            yield Destroy(SELF)
    
    events = Play(CONTROLLER).after(_consume_reduction)
    
    # 给手牌减费
    class Hand:
        def cost_mod(self, card, game):
            # 返回玩家的下一张卡减费
            if card.controller.next_card_cost_reduction > 0:
                return -card.controller.next_card_cost_reduction
            return 0


def ReduceNextCardCost(amount):
    """
    便捷函数：创建一个"下一张卡减费"的buff
    
    使用方法:
        yield Buff(FRIENDLY_HERO, ReduceNextCardCost(2))
    
    参数:
        amount: 减费数量（正数）
    """
    return lambda: NextCardCostReduction(amount=amount)
