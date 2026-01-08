"""
威兹班的工坊 (Whizbang's Workshop)
发布时间: 2024-03-19

【扩展包信息】
- 类型: 扩展包 (Expansion)
- 代码: WHIZBANG (Whizbang's Workshop)
- 版本: 天马年 (Year of the Pegasus)

【卡牌统计】
可收集卡牌: 183张
├── 职业卡牌: 133张 (每职业11张 + 死亡骑士11张)
└── 中立卡牌: 50张

【文件结构】
- 职业文件: deathknight.py 等 (11个)
- tokens.py: Miniaturize, Gigantify 等 Token 卡牌

【核心机制】
- 微缩 (Miniaturize) - 生成1费1/1版本
- 巨大化 (Gigantify) - 生成8费8/8版本
- 工坊主题

【著名卡牌】
- TOY_700: 精彩绝伦的威兹班 (Splendiferous Whizbang) - 中立传说随从
- TOY_500: 微缩系列
- TOY_600: 巨大化系列
"""
from .deathknight import *  # noqa
from .tokens import *  # noqa - Miniaturize, Gigantify 等 Token 卡牌
