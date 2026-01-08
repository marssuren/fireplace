"""
外域的灰烬 (Ashes of Outland)
发布时间: 2020-04-07

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: OUTLANDS (Ashes of Outland)
- 版本: 凤凰年 (Year of the Phoenix)
- 特点: 恶魔猎手 (Demon Hunter) 职业首次登场！

【卡牌统计】
可收集卡牌: 135张
├── 职业卡牌: 90张 (10个职业，每职业9张)
│   ├── Demon Hunter (恶魔猎手): 15张 (新职业)
│   └── 其他9个职业: 各9张
└── 中立卡牌: 45张

【文件结构】
- 职业文件: demonhunter.py, druid.py, hunter.py 等 (10个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 恶魔猎手职业 - 全新职业
- 禁锢 (Imprisoned) - 休眠2回合
- 外域 (Outcast) - 在手牌最左或最右时触发
- 恶魔主题

【著名卡牌】
- BT_187: 伊利丹·怒风 (Metamorphosis) - 恶魔猎手英雄
- BT_429: 监禁的安东尼达斯 (Imprisoned Antaen) - 恶魔猎手随从
- BT_801: 卡加斯·刃拳 (Kayn Sunfury) - 恶魔猎手传说随从
- BT_355: 监禁的观察者 (Imprisoned Observer) - 恶魔猎手随从
"""

from .demonhunter import *
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
