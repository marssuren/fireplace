"""
暗月马戏团的疯狂 (Madness at the Darkmoon Faire)
发布时间: 2020-11-17

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: DARKMOON (Darkmoon Faire)
- 版本: 凤凰年 (Year of the Phoenix)

【卡牌统计】
可收集卡牌: 170张
├── 职业卡牌: 110张 (每职业11张)
└── 中立卡牌: 60张

【文件结构】
- 职业文件: demonhunter.py, druid.py, hunter.py 等 (10个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 腐蚀 (Corrupt) - 打出更高费卡牌后升级
- 古神 (Old Gods) 回归
- 马戏团主题
- 游戏小游戏

【著名卡牌】
- DMF_078: 古神尤格-萨隆 (Yogg-Saron, Master of Fate) - 传说随从
- DMF_235: 古神恩佐斯 (N'Zoth, God of the Deep) - 传说随从
- DMF_174: 古神克苏恩 (C'Thun, the Shattered) - 传说随从
- DMF_120: 古神亚煞极 (Y'Shaarj, the Defiler) - 传说随从
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
