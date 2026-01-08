"""
黑石山的火焰 (Blackrock Mountain)
发布时间: 2015-04-02

【扩展包信息】
- 类型: 冒险模式 (Adventure)
- 代码: BRM (Blackrock Mountain)
- 版本: 经典扩展

【卡牌统计】
可收集卡牌: 31张
├── 职业卡牌: 18张 (每职业2张)
│   ├── Druid (德鲁伊): 2张
│   ├── Hunter (猎人): 2张
│   ├── Mage (法师): 2张
│   ├── Paladin (圣骑士): 2张
│   ├── Priest (牧师): 2张
│   ├── Rogue (潜行者): 2张
│   ├── Shaman (萨满): 2张
│   ├── Warlock (术士): 2张
│   └── Warrior (战士): 2张
└── 中立卡牌: 13张

Token/衍生物: ~10个
冒险模式卡牌: ~99个 (Boss技能、随从、法术等)
乱斗模式卡牌: ~23个

【文件结构】
- collectible.py: 可收集卡牌 + Token/Buff (41个类)
- adventure.py: 冒险模式专属卡牌 (99个类)
- brawl.py: 乱斗模式专属卡牌 (23个类)

【核心机制】
- 龙族协同 (Dragon Synergy)
- 本回合随从死亡计数 (Minions died this turn)
- 手牌龙牌检测 (Holding Dragon)

【著名卡牌】
- BRM_028: 索瑞森大帝 (Emperor Thaurissan) - 传说随从
- BRM_027: 管理者埃克索图斯 (Majordomo Executus) - 传说随从
- BRM_031: 克洛玛古斯 (Chromaggus) - 传说随从
- BRM_030: 奈法利安 (Nefarian) - 传说随从
- BRM_002: 火妖 (Flamewaker) - 稀有随从
- BRM_019: 恐怖的奴隶主 (Grim Patron) - 稀有随从
"""

from .adventure import *
from .brawl import *
from .collectible import *
