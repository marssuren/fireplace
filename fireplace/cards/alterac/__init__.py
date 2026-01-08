"""
奥特兰克的决裂 (Fractured in Alterac Valley)
发布时间: 2021-12-07

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: ALTERAC (Fractured in Alterac Valley)
- 版本: 狮鹫年 (Year of the Gryphon)

【卡牌统计】
可收集卡牌: 170张
├── 职业卡牌: 110张 (每职业11张)
└── 中立卡牌: 60张

【文件结构】
- 职业文件: demonhunter.py, druid.py, hunter.py 等 (10个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 荣誉击杀 (Honorable Kill) - 精确击杀触发
- 目标 (Objectives) - 战场目标
- 联盟 vs 部落主题

【著名卡牌】
- AV_100: 范达尔·鹿盔 (Vanndar Stormpike) - 中立传说随从
- AV_101: 德雷克塔尔 (Drek'Thar) - 中立传说随从
- AV_200: 荣誉击杀系列
- AV_711: 目标卡牌
"""

from .demonhunter import *
from .druid import *
from .hunter import *
from .mage import *
from .neutral_common import *
from .neutral_epic import *
from .neutral_legendary import *
from .neutral_rare import *
from .paladin import *
from .priest import *
from .rogue import *
from .shaman import *
from .warlock import *
from .warrior import *
