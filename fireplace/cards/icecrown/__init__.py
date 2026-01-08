"""
冰冠堡垒的骑士 (Knights of the Frozen Throne)
发布时间: 2017-08-10

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: ICECROWN (Frozen Throne)
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
- 死亡骑士英雄卡 (Death Knight Hero Cards) - 每职业1张传说英雄
- 生命偷取 (Lifesteal)
- 冰冻 (Freeze) 主题

【著名卡牌】
- ICC_314: 玛法里奥的化身 (Malfurion the Pestilent) - 德鲁伊英雄
- ICC_481: 德雷克塔尔 (Deathstalker Rexxar) - 猎人英雄
- ICC_829: 冰霜巫妖吉安娜 (Frost Lich Jaina) - 法师英雄
- ICC_832: 巫妖王 (The Lich King) - 传说随从
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
