"""
冠军的试炼 (The Grand Tournament)
发布时间: 2015-08-24

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: TGT (The Grand Tournament)
- 版本: 经典扩展

【卡牌统计】
可收集卡牌: 132张
├── 职业卡牌: 82张
│   ├── Druid (德鲁伊): 9张
│   ├── Hunter (猎人): 10张
│   ├── Mage (法师): 9张
│   ├── Paladin (圣骑士): 9张
│   ├── Priest (牧师): 9张
│   ├── Rogue (潜行者): 9张
│   ├── Shaman (萨满): 9张
│   ├── Warlock (术士): 9张
│   └── Warrior (战士): 9张
└── 中立卡牌: 50张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 激励 (Inspire) - 使用英雄技能后触发
- 骑术 (Joust) - 双方牌库随从比较费用

【著名卡牌】
- AT_132: 穆克拉的冠军 (Mukla's Champion) - 普通随从
- AT_017: 暮光守护者 (Twilight Guardian) - 史诗随从
- AT_063: 神秘挑战者 (Mysterious Challenger) - 史诗随从
- AT_123: 银色神官帕尔崔丝 (Confessor Paletress) - 传说随从
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
