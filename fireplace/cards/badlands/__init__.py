"""
决战荒芜之地 (Showdown in the Badlands)
发布时间: 2023-11-14

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: WILD_WEST (Showdown in the Badlands)
- 版本: 独狼年 (Year of the Wolf)

【卡牌统计】
可收集卡牌: 183张
├── 职业卡牌: 133张 (每职业11张 + 死亡骑士11张)
└── 中立卡牌: 50张

【文件结构】
- 职业文件: deathknight.py, demonhunter.py, druid.py 等 (11个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- excavate.py: 挖掘 (Excavate) 机制

【核心机制】
- 挖掘 (Excavate) - 发现宝藏
- 快速拔枪 (Quickdraw) - 抽到时触发
- 西部主题

【著名卡牌】
- DEEP_001: 挖掘系列
- DEEP_020: 快速拔枪系列
- DEEP_999: 宝藏卡牌
- WW_001: 西部传奇
"""

from .deathknight import *
from .demonhunter import *
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
from .excavate import *
from .tokens import *
