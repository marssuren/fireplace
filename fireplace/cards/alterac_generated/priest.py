"""
奥特兰克的决裂 - 牧师
Fractured in Alterac Valley - Priest
"""
from ..utils import *


##
# 英雄卡 / Hero Cards

class AV_207:
    """虔诚祭司泽瑞拉 / Xyrella, the Devout
    8费传说英雄卡 - 战吼：触发本局对战中每个死亡的友方随从的亡语。"""

    def play(self):
        """触发所有死亡友方随从的亡语"""
        # 获取墓地中所有有亡语的友方随从
        for card in self.controller.graveyard:
            if hasattr(card, 'deathrattle') and card.type == CardType.MINION:
                # 触发亡语效果
                yield card.deathrattle


##
# 法术 / Spells

class AV_315:
    """超脱 / Bless
    2费法术 - 对一个随从造成3点伤害。荣誉消灭：召唤该随从的一个3/3复制。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Hit(TARGET, 3)


class AV_324:
    """暗言术：噬 / Shadow Word: Devour
    2费法术 - 选择一个随从，使其从所有其他随从处各偷取1点生命值。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        """目标随从从所有其他随从处偷取1点生命值"""
        all_minions = self.controller.field + self.controller.opponent.field
        other_minions = [m for m in all_minions if m != self.target]

        for minion in other_minions:
            yield Hit(minion, 1)
            yield Heal(TARGET, 1)


##
# 随从 / Minions

class AV_325:
    """不死信徒 / Undying Disciple
    3费 3/3 稀有随从 - 嘲讽。亡语：对所有敌方随从造成等同于本随从攻击力的伤害。"""

    atk = 3
    max_health = 3
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDRACE: Race.UNDEAD,
    }

    def deathrattle(self):
        """对所有敌方随从造成等同于攻击力的伤害"""
        damage = self.atk
        yield Hit(ENEMY_MINIONS, damage)


class AV_326:
    """光辉晶簇 / Luminous Geode
    2费 2/4 普通元素 - 在一个友方随从受到治疗后，使其获得+2攻击力。"""

    atk = 2
    max_health = 4
    tags = {
        GameTag.CARDRACE: Race.ELEMENTAL,
    }

    events = Heal(FRIENDLY_MINIONS).after(Buff(Heal.TARGET, "AV_326e"))


class AV_326e:
    """光辉晶簇增益"""
    atk = 2


class AV_328:
    """灵魂向导 / Spirit Guide
    3费 1/6 普通亡灵 - 嘲讽，亡语：抽一张神圣法术牌和一张暗影法术牌。"""

    atk = 1
    max_health = 6
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDRACE: Race.UNDEAD,
    }

    deathrattle = (
        ForceDraw(CONTROLLER, SPELL + HOLY),
        ForceDraw(CONTROLLER, SPELL + SHADOW)
    )


class AV_329:
    """祝福 / Bless
    2费法术 - 使一个随从获得+2生命值，然后使其攻击力等同于其生命值。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Buff(TARGET, "AV_329e")


class AV_329e:
    """祝福增益"""
    max_health = 2

    def apply(self, target):
        """使攻击力等同于生命值"""
        target.atk = target.health


class AV_330:
    """纳鲁的赐福 / Gift of the Naaru
    3费法术 - 为所有角色恢复3点生命值。如果有角色仍处于受伤状态，抽一张牌。"""

    def play(self):
        """治疗所有角色，如果有受伤的则抽牌"""
        yield Heal(ALL_CHARACTERS, 3)

        # 检查是否有受伤的角色
        all_chars = list(self.controller.field) + [self.controller.hero] + \
                    list(self.controller.opponent.field) + [self.controller.opponent.hero]

        for char in all_chars:
            if char.health < char.max_health:
                yield Draw(CONTROLLER)
                break


class AV_331:
    """纳亚克·海克森 / Najak Hexxen
    5费 1/4 传说随从 - 战吼：夺取一个敌方随从的控制权。亡语：归还控制的随从。"""

    atk = 1
    max_health = 4

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    play = Steal(TARGET)
    deathrattle = GiveControl(TARGET, OPPONENT)


class AV_664:
    """雷矛救援站 / Stormpike Aid Station
    3费法术 - 在你的回合结束时，使你的随从获得+2生命值。持续3回合。"""

    play = Buff(FRIENDLY_HERO, "AV_664e")


class AV_664e:
    """雷矛救援站增益"""
    tags = {
        GameTag.TRIGGER_VISUAL: True,
    }
    max_turns = 3
    events = OWN_TURN_END.on(Buff(FRIENDLY_MINIONS, "AV_664e2"))


class AV_664e2:
    """雷矛救援站生命值增益"""
    max_health = 2
