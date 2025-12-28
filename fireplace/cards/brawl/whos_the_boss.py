"""
Who's the Boss Now?
"""

from ..utils import *


class BRMA01_2H_2_TB:
    """Pile On!!! / 干杯！
    从双方的牌库中各将一个随从置入战场。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
        Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION)),
    )


class BRMA02_2_2_TB:
    """Jeering Crowd / 强势围观
    召唤一个1/1并具有嘲讽的观众。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA02_2t")


class BRMA02_2_2c_TB:
    """Jeering Crowd (Unused)"""

    play = Summon(CONTROLLER, "BRMA02_2t")


class BRMA06_2H_TB:
    """The Majordomo / 火妖管理者
    召唤一个3/3的火妖卫士。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA06_4H")


class BRMA07_2_2_TB:
    """ME SMASH / 猛砸
    随机消灭一个敌方随从。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Destroy(RANDOM_ENEMY_MINION)


class BRMA07_2_2c_TB:
    """ME SMASH (Unused)"""

    play = Destroy(RANDOM_ENEMY_MINION)


class BRMA09_2_TB:
    """Open the Gates / 打开大门
    召唤三条1/1的雏龙。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA09_2t") * 3


class BRMA14_10H_TB:
    """Activate! / 激活！
    随机激活一个金刚。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["BRMA14_3", "BRMA14_5", "BRMA14_7", "BRMA14_9"]
    Summon(CONTROLLER, RandomEntourage())


class BRMA13_4_2_TB:
    """Wild Magic / 狂野魔法
    随机将一张你对手职业的法术牌置入你的手牌。"""

    activate = Give(CONTROLLER, RandomSpell(card_class=Attr(ENEMY_HERO, GameTag.CLASS)))


class BRMA17_5_TB:
    """Bone Minions / 白骨爪牙
    召唤两个2/1的白骨结构体。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "BRMA17_6") * 2


class NAX3_02_TB:
    """Web Wrap / 裹体之网
    随机将一个敌方随从移回对手的 手牌。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Bounce(RANDOM_ENEMY_MINION)


class NAX8_02H_TB:
    """Harvest / 收割
    抽一张牌。获得一个法力水晶。"""

    activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1)


class NAX11_02H_2_TB:
    """Poison Cloud / 毒云
    对所有敌方随从造成1点伤害。每死亡一个随从，召唤一个泥浆怪。"""

    activate = Hit(ENEMY_MINIONS, 1).then(
        Dead(Hit.TARGET) & Summon(CONTROLLER, "NAX11_03")
    )


class NAX12_02H_2_TB:
    """Decimate / 残杀
    将所有敌方随从的生命值变为1。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    activate = Buff(ENEMY_MINIONS, "NAX12_02e")


class NAX12_02H_2c_TB:
    """Decimate (Unused)"""

    play = Buff(ENEMY_MINIONS, "NAX12_02e")
