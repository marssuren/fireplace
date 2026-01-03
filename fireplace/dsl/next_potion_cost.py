"""
通用的"下一份药剂减费" buff
用于支持食尸鬼炼金师等卡牌
"""
from ..utils import *


class NextPotionCostZero:
    """
    通用的"下一份药剂减费到0" buff
    
    使用方法:
        yield Buff(FRIENDLY_HERO, "NextPotionCostZero")
    """
    # 药剂列表
    POTIONS = [
        "CFM_021", "CFM_065", "CFM_620", "CFM_603", "CFM_604",
        "CFM_661", "CFM_662", "CFM_094", "CFM_608", "CFM_611"
    ]
    
    def apply(self, target):
        """应用到玩家英雄上"""
        # 设置标记
        target.controller.next_potion_cost_zero = True
    
    # 监听打出卡牌，如果是药剂则消耗标记并移除自己
    def _consume_reduction(self, source, player, card):
        if player == self.controller and self.controller.next_potion_cost_zero:
            # 检查是否为药剂
            if card.id in self.POTIONS:
                # 重置标记
                self.controller.next_potion_cost_zero = False
                # 移除此buff
                yield Destroy(SELF)
    
    events = Play(CONTROLLER).after(_consume_reduction)
    
    # 给手牌中的药剂减费
    class Hand:
        def cost_mod(self, card, game):
            # 检查是否为药剂且玩家有标记
            if card.controller.next_potion_cost_zero and card.id in NextPotionCostZero.POTIONS:
                # 返回负的费用，使其变为0
                return -card.cost
            return 0
