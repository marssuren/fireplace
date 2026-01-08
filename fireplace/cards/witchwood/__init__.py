"""
女巫森林 (The Witchwood)
发布时间: 2018-04-12

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: WITCHWOOD (The Witchwood)
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
- echo_buff.py: 回响 (Echo) 机制

【核心机制】
- 回响 (Echo) - 本回合可重复使用
- 突袭 (Rush) - 首次关键词引入
- 偶数/奇数套牌 (Even/Odd Decks)

【著名卡牌】
- GIL_826: 巴库 (Baku the Mooneater) - 传说随从 (奇数套牌)
- GIL_692: 格恩·格雷迈恩 (Genn Greymane) - 传说随从 (偶数套牌)
- GIL_558: 沙德沃克 (Shudderwock) - 传说随从
- GIL_800: 黑森林女巫 (Witchwood Grizzly) - 稀有随从
"""

from .echo_buff import *
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
