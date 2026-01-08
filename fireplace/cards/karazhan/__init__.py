"""
卡拉赞之夜 (One Night in Karazhan)
发布时间: 2016-08-11

【扩展包信息】
- 类型: 冒险模式 (Adventure)
- 代码: KARA (Karazhan)
- 版本: 经典扩展

【卡牌统计】
可收集卡牌: 45张
├── 职业卡牌: 27张 (每职业3张)
│   ├── Druid (德鲁伊): 3张
│   ├── Hunter (猎人): 3张
│   ├── Mage (法师): 3张
│   ├── Paladin (圣骑士): 3张
│   ├── Priest (牧师): 3张
│   ├── Rogue (潜行者): 3张
│   ├── Shaman (萨满): 3张
│   ├── Warlock (术士): 3张
│   └── Warrior (战士): 3张
└── 中立卡牌: 18张

【文件结构】
- collectible.py: 所有可收集卡牌 + Token/Buff

【核心机制】
- 传送门 (Portals) - 召唤随机随从并减费
- 派对主题卡牌

【著名卡牌】
- KAR_025: 巴内斯 (Barnes) - 传说随从
- KAR_036: 以太传送门 (Ethereal Peddler) - 稀有随从
- KAR_094: 火妖之书 (The Curator) - 传说随从
- KAR_061: 魔力之书 (Book Wyrm) - 稀有随从
"""

from .collectible import *
