"""
巨龙降临 (Descent of Dragons)
发布时间: 2019-12-10

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: DRAGONS (Descent of Dragons)
- 版本: 巨龙年 (Year of the Dragon)

【卡牌统计】
可收集卡牌: 140张
├── 职业卡牌: 90张 (每职业10张)
└── 中立卡牌: 50张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- adventure.py: 冒险模式卡牌 (迦拉克隆的觉醒)

【核心机制】
- 迦拉克隆 (Galakrond) - 5个职业专属英雄卡
- 祈求 (Invoke) - 升级迦拉克隆
- 侧翼打击 (Sidequest) - 小型任务
- 龙族主题

【著名卡牌】
- DRG_238: 迦拉克隆 (Galakrond, the Unspeakable) - 牧师英雄
- DRG_403: 死亡之翼 (Deathwing, Mad Aspect) - 传说随从
- DRG_090: 奈萨里奥 (Necrium Apothecary) - 盗贼随从
- DRG_242: 堕落的守护者 (Dragonqueen Alexstrasza) - 传说随从
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
from .adventure import *
