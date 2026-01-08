"""
纳克萨玛斯的诅咒 (Curse of Naxxramas)
发布时间: 2014-07-22

【扩展包信息】
- 类型: 冒险模式 (Adventure)
- 代码: NAXX (Naxxramas)
- 版本: 经典扩展
- 特点: 炉石传说第一个冒险模式

【卡牌统计】
可收集卡牌: 30张
├── 职业卡牌: 9张 (每职业1张)
│   ├── Druid (德鲁伊): 1张
│   ├── Hunter (猎人): 1张
│   ├── Mage (法师): 1张
│   ├── Paladin (圣骑士): 1张
│   ├── Priest (牧师): 1张
│   ├── Rogue (潜行者): 1张
│   ├── Shaman (萨满): 1张
│   ├── Warlock (术士): 1张
│   └── Warrior (战士): 1张
└── 中立卡牌: 21张

【文件结构】
- collectible.py: 可收集卡牌 + Token/Buff
- adventure.py: 冒险模式专属卡牌 (Boss技能、随从、法术等)

【核心机制】
- 亡语 (Deathrattle) - 主题机制
- 随从复活/召唤

【著名卡牌】
- NAXX1_01: 洛欧塞布 (Loatheb) - 传说随从
- FP1_012: 肯瑞托·克苏恩 (Kel'Thuzad) - 传说随从
- FP1_002: 疯狂的科学家 (Mad Scientist) - 普通随从
- FP1_004: 幽灵爬行者 (Haunted Creeper) - 普通随从
- FP1_007: 蛛魔之卵 (Nerubian Egg) - 稀有随从
- FP1_031: 死亡领主 (Sludge Belcher) - 稀有随从
"""

from .adventure import *
from .collectible import *
