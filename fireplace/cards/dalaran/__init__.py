"""
暗影崛起 (Rise of Shadows)
发布时间: 2019-04-09

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: DALARAN (Rise of Shadows)
- 版本: 巨龙年 (Year of the Dragon)

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
- lackey.py: 苦工 (Lackey) 系统

【核心机制】
- 苦工 (Lackey) - 1费随从Token
- 阴谋 (Scheme) - 每回合升级的法术
- 孪生法术 (Twinspell) - 复制到手牌的法术
- E.V.I.L. vs 探险者联盟主题

【著名卡牌】
- DAL_141: 大法师瓦格斯 (Archmage Vargoth) - 传说随从
- DAL_800: 拉法姆 (Rafaam) - 术士传说随从
- DAL_366: 卡德加 (Khadgar) - 法师传说随从
- DAL_077: 炸弹战士 (Wrenchcalibur) - 战士武器
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
from .lackey import *
