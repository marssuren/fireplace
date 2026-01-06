"""
深暗领域 - 星舰定义 (Starships)

星舰是通过星舰组件死亡累积而成的特殊随从。
每个职业有自己的星舰，或使用中立星舰。

星舰特性：
- 初始为休眠状态，占据场地位置
- 累积所有死亡的星舰组件的属性和效果
- 玩家可以花费5点法力值发射星舰
- 发射后成为活跃随从，拥有所有累积的属性
"""
from ..utils import *


# ========================================
# 专属星舰 (Class-Specific Starships)
# ========================================

class GDB_STARSHIP_DEATHKNIGHT:
    """死亡骑士星舰 - The Necropolis (亡灵要塞)

    这是死亡骑士的专属星舰。
    通过死亡骑士的星舰组件构筑。
    """
    # 星舰基础属性由组件累积，这里只定义卡牌框架
    pass


class GDB_STARSHIP_DEMONHUNTER:
    """恶魔猎手星舰 - The Fel Hammer (邪能战锤)

    这是恶魔猎手的专属星舰。
    通过恶魔猎手的星舰组件构筑。
    """
    pass


class GDB_STARSHIP_DRUID:
    """德鲁伊星舰 - The Exodar (埃索达)

    这是德鲁伊的专属星舰。
    通过德鲁伊的星舰组件构筑。
    """
    pass


class GDB_STARSHIP_HUNTER:
    """猎人星舰 - The Reaver (掠夺者)

    这是猎人的专属星舰。
    通过猎人的星舰组件构筑。
    """
    pass


class GDB_STARSHIP_ROGUE:
    """潜行者星舰 - The Defiant (反抗者)

    这是潜行者的专属星舰。
    通过潜行者的星舰组件构筑。
    """
    pass


class GDB_STARSHIP_WARLOCK:
    """术士星舰 - The Burning Legion Ship (燃烧军团战舰)

    这是术士的专属星舰。
    通过术士的星舰组件构筑。
    """
    pass


# ========================================
# 中立星舰 (Neutral Starships)
# ========================================

class GDB_STARSHIP_BATTLECRUISER:
    """战列巡洋舰 - Battlecruiser

    中立星舰，供以下职业使用：
    - 圣骑士 (Paladin)
    - 萨满祭司 (Shaman)
    - 战士 (Warrior)
    """
    pass


class GDB_STARSHIP_EXILES_HOPE:
    """流亡者之希望 - The Exile's Hope

    中立星舰，供以下职业使用：
    - 法师 (Mage)
    - 牧师 (Priest)
    """
    pass
