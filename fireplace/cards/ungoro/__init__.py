"""
勇闯安戈洛 (Journey to Un'Goro)
发布时间: 2017-04-06

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: UNGORO (Un'Goro)
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
- adapt_buff.py: 适应 (Adapt) 机制

【核心机制】
- 任务 (Quest) - 1费传说法术，完成后获得奖励
- 适应 (Adapt) - 发现3选1的随从增益
- 元素 (Elemental) 种族
- 恐龙 (Beast) 主题

【著名卡牌】
- UNG_116: 丛林巨兽 (Jungle Giants) - 德鲁伊任务
- UNG_028: 开启传送门 (Open the Waygate) - 法师任务
- UNG_067: 最后的卡利多斯 (The Last Kaleidosaur) - 圣骑士任务
- UNG_829: 始生幼龙 (Primordial Drake) - 史诗随从
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
from .adapt_buff import *
