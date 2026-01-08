"""
狗头人与地下世界 (Kobolds and Catacombs)
发布时间: 2017-12-07

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: KOBOLDS (Kobolds and Catacombs)
- 版本: 猛犸年 (Year of the Mammoth)

【卡牌统计】
可收集卡牌: 135张
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
└── 中立卡牌: 45张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 法术石 (Spellstones) - 可升级的法术
- 传说武器 (Legendary Weapons) - 每职业1把
- 招募 (Recruit) - 从牌库直接召唤随从
- 地下城跑 (Dungeon Run) 模式

【著名卡牌】
- LOOT_503: 小型法术翡翠石 (Lesser Jasper Spellstone) - 德鲁伊法术
- LOOT_412: 颅骨之王 (Skull of the Man'ari) - 术士武器
- LOOT_214: 虚空领主 (Voidlord) - 术士随从
- LOOT_541: 召唤传送门 (Call to Arms) - 圣骑士法术
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
