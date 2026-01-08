"""
奥丹姆奇兵 (Saviors of Uldum)
发布时间: 2019-08-06

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: ULDUM (Saviors of Uldum)
- 版本: 巨龙年 (Year of the Dragon)

【卡牌统计】
可收集卡牌: 135张
├── 职业卡牌: 90张 (每职业10张)
└── 中立卡牌: 45张

【文件结构】
- 职业文件: druid.py, hunter.py, mage.py 等 (9个)
- 中立文件: neutral_common.py, neutral_rare.py, neutral_epic.py, neutral_legendary.py
- zephrys_the_great.py: 泽菲里斯特殊实现

【核心机制】
- 重生 (Reborn) - 死亡后复活为1生命
- 任务 (Quest) 回归 - 1费传说法术
- 瘟疫 (Plague) 系列法术
- 探险者联盟主题

【著名卡牌】
- ULD_003: 泽菲里斯 (Zephrys the Great) - 传说随从
- ULD_431: 任务德鲁伊 (Untapped Potential) - 德鲁伊任务
- ULD_155: 任务猎人 (Unseal the Vault) - 猎人任务
- ULD_326: 沙漠野兔 (Desert Hare) - 普通随从
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
from .zephrys_the_great import *
