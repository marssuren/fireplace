"""
通灵学园 (Scholomance Academy)
发布时间: 2020-08-06

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: SCHOLOMANCE (Scholomance Academy)
- 版本: 凤凰年 (Year of the Phoenix)

【卡牌统计】
可收集卡牌: 135张
├── 职业卡牌: 90张 (每职业9张)
└── 中立卡牌: 45张

【文件结构】
- 职业文件: demonhunter.py, druid.py, hunter.py 等 (10个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- transfer_student.py: 转校生特殊实现

【核心机制】
- 双职业卡牌 (Dual-Class Cards) - 可用于2个职业
- 法术伤害 (Spell Damage) 主题
- 学习 (Studies) - 发现并减费
- 学园主题

【著名卡牌】
- SCH_142: 转校生 (Transfer Student) - 中立随从
- SCH_312: 教头拉兹 (Instructor Fireheart) - 萨满传说随从
- SCH_600: 大法师克尔苏加德 (Kel'Thuzad) - 法师传说随从
- SCH_537: 古神克苏恩 (C'Thun, the Shattered) - 中立传说随从
"""

from .transfer_student import *
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
from .tokens import *
