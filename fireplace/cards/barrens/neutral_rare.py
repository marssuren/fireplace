"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_071:
    """Taurajo Brave - 陶拉祖武士
    Frenzy: Destroy a random enemy minion.
    暴怒：摧毁一个随机敌方随从。
    """
    frenzy = Destroy(RANDOM_ENEMY_MINION)


class BAR_072:
    """Burning Blade Acolyte - 火刃侍僧
    Deathrattle: Summon a 5/8 Demonspawn with Taunt.
    亡语：召唤一个5/8并具有嘲讽的恶魔后裔。
    """
    deathrattle = Summon(CONTROLLER, "BAR_072t")


class BAR_076:
    """Mor'shan Watch Post - 莫尔杉哨所
    Can't attack. After your opponent plays a minion, summon a 2/2 Grunt.
    无法攻击。在你的对手打出一个随从后，召唤一个2/2的步兵。
    """
    events = Play(OPPONENT, MINION).after(
        Summon(CONTROLLER, "BAR_076t")
    )


class BAR_430:
    """Horde Operative - 部落特工
    Battlecry: Copy your opponent's Secrets and put them into play.
    战吼：复制你对手的奥秘并使其进入战场。
    """
    play = Summon(CONTROLLER, Copy(ENEMY_SECRETS))


class BAR_745:
    """Hecklefang Hyena - 乱齿土狼
    Battlecry: Deal 3 damage to your hero.
    战吼：对你的英雄造成3点伤害。
    """
    play = Hit(FRIENDLY_HERO, 3)


