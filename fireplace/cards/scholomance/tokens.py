from ..utils import *


##
# Demon Hunter & Warlock Tokens


class BT_496t:
    """Soul Fragment (灵魂碎片)
    Casts When Drawn: Restore 2 Health to your hero.
    抽到时施放：为你的英雄恢复2点生命值。
    """
    # 0费暗影法术 - Token
    # 来源：通灵学园扩展包
    # 由多张卡牌生成，包括：
    # - Luckysoul Hoarder (YOP_003) - 暗月马戏团
    # - 其他术士/恶魔猎手卡牌
    
    # Casts When Drawn 效果
    draw = Heal(FRIENDLY_HERO, 2)
