"""
地精大战侏儒 (Goblins vs Gnomes)
发布时间: 2014-12-08

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: GVG (Goblins vs Gnomes)
- 版本: 经典扩展
- 特点: 炉石传说第一个大型扩展包

【卡牌统计】
可收集卡牌: 123张
├── 职业卡牌: 72张 (每职业8张)
│   ├── Druid (德鲁伊): 8张
│   ├── Hunter (猎人): 8张
│   ├── Mage (法师): 8张
│   ├── Paladin (圣骑士): 8张
│   ├── Priest (牧师): 8张
│   ├── Rogue (潜行者): 8张
│   ├── Shaman (萨满): 8张
│   ├── Warlock (术士): 8张
│   └── Warrior (战士): 8张
└── 中立卡牌: 51张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- spare_parts.py: 零件卡牌 (机械主题)

【核心机制】
- 机械 (Mech) 种族
- 零件 (Spare Parts) - 1费法术
- 随机效果 (RNG)

【著名卡牌】
- GVG_096: 机械跃迁者 (Mechwarper) - 稀有随从
- GVG_006: 机械雪人 (Piloted Shredder) - 普通随从
- GVG_110: 博士的爆破机器人 (Dr. Boom) - 传说随从
- GVG_117: 加兹鲁维 (Gazlowe) - 传说随从
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
from .spare_parts import *
