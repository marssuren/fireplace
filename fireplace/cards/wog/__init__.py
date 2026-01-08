"""
上古之神的低语 (Whispers of the Old Gods)
发布时间: 2016-04-26

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: WOG (Whispers of the Old Gods)
- 版本: 海怪年 (Year of the Kraken)

【卡牌统计】
可收集卡牌: 134张
├── 职业卡牌: 83张 (每职业9张)
└── 中立卡牌: 51张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- toxins.py: 毒药系统

【核心机制】
- 古神 (Old Gods) - 4张传说古神
- 克苏恩 (C'Thun) 系统
- 腐蚀 (Corruption) 主题

【著名卡牌】
- OG_042: 克苏恩 (C'Thun) - 中立传说随从
- OG_134: 尤格-萨隆 (Yogg-Saron) - 中立传说随从
- OG_280: 恩佐斯 (N'Zoth) - 中立传说随从
- OG_334: 亚煞极 (Y'Shaarj) - 中立传说随从
"""

from .druid import *
from .hunter import *
from .mage import *
from .paladin import *
from .priest import *
from .rogue import *
from .shaman import *
from .warlock import *
from .warrior import *
from .neutral_common import *
from .neutral_rare import *
from .neutral_epic import *
from .neutral_legendary import *
from .toxins import *
