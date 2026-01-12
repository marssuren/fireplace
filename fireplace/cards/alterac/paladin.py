"""
奥特兰克的决裂 - 圣骑士
Fractured in Alterac Valley - Paladin
"""
from ..utils import *


##
# 英雄卡 / Hero Cards

class AV_206:
    """光铸卡瑞尔 / Lightforged Cariel
    8费传说英雄卡 - 战吼：对所有敌人造成2点伤害。装备一把2/5的不动之物武器。"""

    # 战吼：对所有敌人造成2点伤害，装备武器
    def play(self):
        yield Hit(ENEMY_CHARACTERS, 2)
        yield Summon(CONTROLLER, "AV_206t")


class AV_206t:
    """不动之物 / Immovable Object
    2/5武器 - 你的英雄受到的伤害减半（向上取整）。此武器不会失去耐久度。"""

    atk = 2
    durability = 5

    # 武器不会失去耐久度
    tags = {
        GameTag.IMMUNE_WHILE_ATTACKING: True,
    }

    # 英雄受到的伤害减半
    events = Predamage(FRIENDLY_HERO).on(
        lambda self, source, target, amount, *args: [amount // 2 + (amount % 2)]
    )


##
# 随从 / Minions

class AV_340:
    """亮铜之翼 / Brasswing
    8费 9/7 史诗龙 - 在你的回合结束时，对所有敌人造成2点伤害。荣誉击杀：为你的英雄恢复4点生命值。"""

    atk = 9
    max_health = 7
    tags = {
        GameTag.CARDRACE: Race.DRAGON,
    }

    # 回合结束时对所有敌人造成2点伤害
    events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 2))


class AV_339:
    """圣殿骑兵队长 / Templar Captain
    8费 6/6 随从 - 突袭。在攻击一个随从后，召唤一个5/5并具有嘲讽的防御者。"""

    atk = 6
    max_health = 6
    tags = {
        GameTag.RUSH: True,
    }

    # 攻击随从后召唤防御者
    events = Attack(SELF, MINION).after(Summon(CONTROLLER, "AV_339t"))


class AV_339t:
    """防御者 / Defender
    5/5 随从 - 嘲讽"""

    atk = 5
    max_health = 5
    tags = {
        GameTag.TAUNT: True,
    }


##
# 法术 / Spells

class AV_343:
    """保护无辜者 / Protect the Innocent
    1费法术 - 为你的英雄恢复3点生命值。抽一张牌。"""

    play = Heal(FRIENDLY_HERO, 3), Draw(CONTROLLER)


class AV_344:
    """活力涌动 / Vitality Surge
    2费法术 - 为一个随从恢复8点生命值。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Heal(TARGET, 8)


##
# 武器 / Weapons

class AV_345:
    """骑兵号角 / Cavalry Horn
    3费 2/2 武器 - 在你的英雄攻击后，召唤一个1/1的银色之手新兵。"""

    atk = 2
    durability = 2

    # 攻击后召唤银色之手新兵
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "CS2_101t"))

