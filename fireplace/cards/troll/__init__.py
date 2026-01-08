"""
拉斯塔哈的大乱斗 (Rastakhan's Rumble)
发布时间: 2018-12-04

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: TROLL (Rastakhan's Rumble)
- 版本: 渡鸦年 (Year of the Raven)

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
- 狂怒 (Overkill) - 造成超量伤害时触发
- 洛阿神灵 (Loa) - 每职业1张传说随从
- 精灵 (Spirit) - 每职业1张稀有随从
- 巨魔主题

【著名卡牌】
- TRL_541: 苏拉玛尔 (Shirvallah, the Tiger) - 圣骑士法术
- TRL_092: 祖尔金 (Zul'jin) - 猎人英雄
- TRL_360: 祖达克 (Zul'Drak Ritualist) - 中立随从
- TRL_318: 格罗尔 (Gral, the Shark) - 盗贼洛阿
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
