"""
探险者协会 (The League of Explorers)
发布时间: 2015-11-12

【扩展包信息】
- 类型: 冒险模式 (Adventure)
- 代码: LEAGUE (The League of Explorers)
- 版本: 经典扩展

【卡牌统计】
可收集卡牌: 45张
├── 职业卡牌: 27张 (每职业3张)
└── 中立卡牌: 18张

【文件结构】
- collectible.py: 可收集卡牌 + Token/Buff
- adventure.py: 冒险模式专属卡牌 (Boss技能、随从、法术等)

【核心机制】
- 发现 (Discover) - 首次引入！
- 探险者主题
- 雷诺·杰克逊 (Reno Jackson) 系统

【著名卡牌】
- LOE_011: 雷诺·杰克逊 (Reno Jackson) - 传说随从
- LOE_019: 芬利·莫格顿爵士 (Sir Finley Mrrgglton) - 传说随从
- LOE_077: 布莱恩·铜须 (Brann Bronzebeard) - 传说随从
- LOE_104: 伊莉斯·逐星 (Elise Starseeker) - 传说随从
"""

from .adventure import *
from .collectible import *
