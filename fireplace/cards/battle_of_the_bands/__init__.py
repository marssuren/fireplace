"""
传奇音乐节 (Festival of Legends)
发布时间: 2023-04-11

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: BATTLE_OF_THE_BANDS (Festival of Legends)
- 版本: 独狼年 (Year of the Wolf)

【卡牌统计】
可收集卡牌: 183张
├── 职业卡牌: 133张 (每职业11张 + 死亡骑士11张)
└── 中立卡牌: 50张

【文件结构】
- 职业文件: deathknight.py, demonhunter.py, druid.py 等 (11个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py

【核心机制】
- 传奇法术 (Legendary Spells)
- 合音 (Harmonize) - 打出法术后触发
- 独奏 (Solo) - 只有1张卡时增强
- 音乐节主题

【著名卡牌】
- ETC_083: 精灵传奇摇滚乐队 (E.T.C., Band Manager) - 中立传说随从
- ETC_333: 合音系列
- ETC_210: 独奏卡牌
- ETC_515: 传奇法术
"""

from .deathknight import *
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
