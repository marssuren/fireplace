from ..utils import *


##
# Minions


class GVG_074:
    """Kezan Mystic / 科赞秘术师
    战吼：随机夺取一个敌方奥秘的控制权。"""

    play = Steal(RANDOM(ENEMY_SECRETS))


class GVG_089:
    """Illuminator / 明光祭司
    如果在你的回合结束时，你控制一个奥秘，则为你的英雄恢复#4点生命值。"""

    events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Heal(FRIENDLY_HERO, 4))


class GVG_094:
    """Jeeves / 基维斯
    在每个玩家的回合结束时，该玩家抽若干牌，直至其手牌数量达到3张。"""

    events = EndTurn().on(DrawUntil(EndTurn.PLAYER, 3))


class GVG_095:
    """Goblin Sapper / 地精工兵
    如果你对手的手牌数量大于或等于6张，便拥有+4攻击力。"""

    update = (Count(ENEMY_HAND) >= 6) & Refresh(SELF, {GameTag.ATK: +4})


class GVG_097:
    """Lil' Exorcist / 小个子驱魔者
    嘲讽，战吼：每有一个具有亡语的敌方随从，便获得+1/+1。"""

    # The Enchantment ID is correct
    play = Buff(SELF, "GVG_101e") * Count(ENEMY_MINIONS + DEATHRATTLE)


GVG_101e = buff(+1, +1)


class GVG_099:
    """Bomb Lobber / 榴弹投手
    战吼：随机对一个敌方随从造成4点伤害。"""

    play = Hit(RANDOM_ENEMY_MINION, 4)
