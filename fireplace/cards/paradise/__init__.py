"""
胜地历险记 (Perils in Paradise)
发布时间: 2024-07-23

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: PARADISE (Perils in Paradise)
- 版本: 天马年 (Year of the Pegasus)

【卡牌统计】
可收集卡牌: 183张
├── 职业卡牌: 133张 (每职业11张 + 死亡骑士11张)
└── 中立卡牌: 50张

【文件结构】
- 职业文件: deathknight.py, demonhunter.py, druid.py 等 (11个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- tokens.py: Token 卡牌

【核心机制】
- 游客 (Tourist) - 可使用其他职业卡牌
- 度假胜地主题

【著名卡牌】
- WORK_001: 游客系列
- WORK_100: 度假胜地卡牌
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
from .tokens import *
