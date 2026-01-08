"""
贫瘠之地的锤炼 (Forged in the Barrens)
发布时间: 2021-03-30

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: BARRENS (Forged in the Barrens)
- 版本: 狮鹫年 (Year of the Gryphon)

【卡牌统计】
可收集卡牌: 170张
├── 职业卡牌: 110张 (每职业11张)
└── 中立卡牌: 60张

【文件结构】
- 职业文件: demonhunter.py, druid.py, hunter.py 等 (10个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 狂乱 (Frenzy) - 首次受伤后触发
- 等级法术 (Ranked Spells) - 根据法力水晶数量升级
- 任务线 (Questlines) - 多阶段任务
- 部落主题

【著名卡牌】
- BAR_891: 古夫·符文图腾 (Guff Runetotem) - 德鲁伊传说随从
- BAR_720: 德卡·雷霆拳 (Deckhand Swabbie) - 中立随从
- BAR_876: 守望者 (Watchpost) 系列
- BAR_329: 任务线卡牌
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
