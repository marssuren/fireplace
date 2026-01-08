"""
砰砰计划 (The Boomsday Project)
发布时间: 2018-08-07

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: BOOMSDAY (The Boomsday Project)
- 版本: 渡鸦年 (Year of the Raven)

【卡牌统计】
可收集卡牌: 136张
├── 职业卡牌: 90张 (每职业10张)
│   ├── Druid (德鲁伊): 10张
│   ├── Hunter (猎人): 10张
│   ├── Mage (法师): 10张
│   ├── Paladin (圣骑士): 10张
│   ├── Priest (牧师): 10张
│   ├── Rogue (潜行者): 10张
│   ├── Shaman (萨满): 10张
│   ├── Warlock (术士): 10张
│   └── Warrior (战士): 10张
└── 中立卡牌: 46张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 磁力 (Magnetic) - 机械随从合体
- 炸弹 (Bombs) - 洗入对手牌库
- 科学计划 (Science Projects)
- 欧米茄卡牌 (Omega Cards) - 10费时增强

【著名卡牌】
- BOT_424: 米米尔隆的头部 (Mecha'thun) - 传说随从
- BOT_573: 星界秘法师 (Astromancer) - 史诗随从
- BOT_436: 砰砰博士 (Dr. Boom, Mad Genius) - 战士英雄
- BOT_914: 惠斯班 (Whizbang the Wonderful) - 传说随从
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
