"""
决斗模式 - 其他宝藏卡牌 (Part 1)
Duels Mode - Other Treasures
"""
from ..utils import *


class PVPDR_Hyperblaster:
    """超级爆破枪 / Hyperblaster
    3费武器 3/2 - 剧毒"""

    tags = {
        GameTag.POISONOUS: True,
    }
    atk = 3
    durability = 2


class PVPDR_GnomishArmyKnife:
    """侏儒军刀 / Gnomish Army Knife
    1费法术 - 使一个随从获得+1/+1，突袭，风怒，圣盾，吸血，剧毒，嘲讽和潜行。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Buff(TARGET, "PVPDR_GnomishArmyKnife_Buff")


class PVPDR_GnomishArmyKnife_Buff:
    """侏儒军刀增益"""
    tags = {
        GameTag.RUSH: True,
        GameTag.WINDFURY: True,
        GameTag.DIVINE_SHIELD: True,
        GameTag.LIFESTEAL: True,
        GameTag.POISONOUS: True,
        GameTag.TAUNT: True,
        GameTag.STEALTH: True,
    }
    atk = 1
    max_health = 1


class PVPDR_CrustyTheCrustacean:
    """硬壳蟹人 / Crusty the Crustacean
    5费 5/5 随从 - 战吼：消灭一个随从。"""

    atk = 5
    max_health = 5

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Destroy(TARGET)


class PVPDR_BananaSplit:
    """香蕉船 / Banana Split
    4费法术 - 选择一个随从。召唤它的3个复制。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        """召唤目标随从的3个复制"""
        for _ in range(3):
            if len(self.controller.field) < 7:
                yield Summon(CONTROLLER, ExactCopy(TARGET))


class PVPDR_Bubba:
    """布巴 / Bubba
    6费 6/6 随从 - 战吼：消灭一个随机敌方随从。"""

    atk = 6
    max_health = 6

    def play(self):
        """消灭一个随机敌方随从"""
        targets = self.controller.opponent.field
        if targets:
            target = self.game.random.choice(targets)
            yield Destroy(target)


class PVPDR_ClockworkAssistant:
    """发条助手 / Clockwork Assistant
    1费 1/1 随从 - 每当你施放一个法术，获得+1/+1。"""

    atk = 1
    max_health = 1

    events = Play(CONTROLLER, SPELL).after(Buff(SELF, "PVPDR_ClockworkAssistant_Buff"))


class PVPDR_ClockworkAssistant_Buff:
    """发条助手增益"""
    atk = 1
    max_health = 1


class PVPDR_PuzzleBox:
    """谜题盒 / Puzzle Box
    1费法术 - 如果你的场上有3个或更多随从，抽3张牌。"""

    def play(self):
        """如果场上有3个或更多随从，抽3张牌"""
        if len(self.controller.field) >= 3:
            yield Draw(CONTROLLER) * 3


class PVPDR_BladeOfQuelDelar:
    """奎尔德拉之刃 / Blade of Quel'Delar
    4费武器 6/3"""

    atk = 6
    durability = 3


class PVPDR_HiltOfQuelDelar:
    """奎尔德拉剑柄 / Hilt of Quel'Delar
    1费武器 1/3"""

    atk = 1
    durability = 3


class PVPDR_VampiricFangs:
    """吸血獠牙 / Vampiric Fangs
    3费法术 - 消灭一个随从。为你的英雄恢复5点生命值。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Destroy(TARGET), Heal(FRIENDLY_HERO, 5)


class PVPDR_TheExorcisor:
    """驱魔者 / The Exorcisor
    3费武器 3/2 - 每当此武器攻击时，沉默被攻击的随从。"""

    atk = 3
    durability = 2
    events = Attack(SELF, MINION).after(Silence(Attack.DEFENDER))


class PVPDR_HolyBook:
    """圣书 / Holy Book
    2费法术 - 消灭一个随从。召唤一个8/8的天使。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Destroy(TARGET), Summon(CONTROLLER, "PVPDR_HolyBook_Token")


class PVPDR_HolyBook_Token:
    """天使 / Angel
    8/8 随从"""
    atk = 8
    max_health = 8


class PVPDR_MutatingInjection:
    """变异注射 / Mutating Injection
    1费法术 - 使一个随从获得+4/+4和嘲讽。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Buff(TARGET, "PVPDR_MutatingInjection_Buff")


class PVPDR_MutatingInjection_Buff:
    """变异注射增益"""
    tags = {
        GameTag.TAUNT: True,
    }
    atk = 4
    max_health = 4


class PVPDR_Spyglass:
    """望远镜 / Spyglass
    1费法术 - 发现对手手牌中的一张牌。"""

    def play(self):
        """发现对手手牌中的一张牌"""
        opponent_hand = list(self.controller.opponent.hand)
        if opponent_hand:
            yield Discover(CONTROLLER, cards=[card.id for card in opponent_hand])


class PVPDR_NecroticPoison:
    """死灵毒药 / Necrotic Poison
    1费法术 - 消灭一个随从。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Destroy(TARGET)


class PVPDR_BeastlyBeauty:
    """野兽美人 / Beastly Beauty
    4费法术 - 消灭一个随从。召唤一个8/8的野兽。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Destroy(TARGET), Summon(CONTROLLER, "PVPDR_BeastlyBeauty_Token")


class PVPDR_BeastlyBeauty_Token:
    """野兽 / Beast
    8/8 野兽"""
    tags = {
        GameTag.CARDRACE: Race.BEAST,
    }
    atk = 8
    max_health = 8


class PVPDR_GrimmerPatron:
    """更暗的顾客 / Grimmer Patron
    4费 3/3 随从 - 每当此随从受到伤害并存活时，召唤一个更暗的顾客。"""

    atk = 3
    max_health = 3

    events = Damage(SELF).after(
        Find(SELF) & (CURRENT_HEALTH(SELF) > 0) & Summon(CONTROLLER, "PVPDR_GrimmerPatron")
    )

