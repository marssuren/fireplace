# ========================================
# Hunter Tokens (Sidequest Rewards)
# ========================================


class DRG_251t:
    """Gryphon / 狮鹫
    4/4 并具有突袭的狮鹫（Clear the Way 的奖励）"""

    # 4/4 Gryphon with Rush (Reward from Clear the Way)
    pass


class DRG_255t:
    """Leper Gnome / 麻风侏儒
    2/1 的麻风侏儒（Toxic Reinforcements 的奖励）
    亡语：对敌方英雄造成2点伤害"""

    # 2/1 Leper Gnome (Reward from Toxic Reinforcements)
    # Deathrattle: Deal 2 damage to the enemy hero
    deathrattle = Hit(ENEMY_HERO, 2)
