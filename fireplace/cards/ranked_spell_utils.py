"""
等级法术（Ranked Spells）机制实现

等级法术是《贫瘠之地的试炼》扩展包引入的新机制。
这些法术会在玩家达到特定法力水晶数量时自动升级：
- Rank 1 (初始): 基础版本
- Rank 2 (5费时): 第一次升级
- Rank 3 (10费时): 最终升级

实现原理：
在每个回合开始时检查玩家的最大法力水晶，如果达到阈值则自动升级

使用方法：
    class BAR_891:  # Fury (Rank 1)
        '''怒火（等级1）'''
        # 定义 Rank 1 的效果
        play = GainArmor(FRIENDLY_HERO, 2)
        
        # 在手牌中监听升级
        class Hand:
            events = (
                OWN_TURN_BEGIN.on(
                    Find(SELF) & (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_891t")
                ),
            )
    
    class BAR_891t:  # Fury (Rank 2)
        '''怒火（等级2）'''
        play = GainArmor(FRIENDLY_HERO, 4)
        
        class Hand:
            events = (
                OWN_TURN_BEGIN.on(
                    Find(SELF) & (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_891t2")
                ),
            )
    
    class BAR_891t2:  # Fury (Rank 3)
        '''怒火（等级3）'''
        play = GainArmor(FRIENDLY_HERO, 6)
"""

# 注意：等级法术的升级逻辑直接在各个卡牌类中实现
# 每个 Rank 1 和 Rank 2 的卡牌都有一个 Hand.events 来监听回合开始并检查是否需要升级
# 这种方式更简洁，不需要额外的工具类
