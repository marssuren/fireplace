"""
决斗模式 - 顶级宝藏卡牌 (Part 1)
Duels Mode - Top Tier Treasures
"""
from ..utils import *


class PVPDR_Boombox:
    """砰砰博士的音箱 / Dr. Boom's Boombox
    4费法术 - 召唤7个1/1并具有"亡语：对一个随机敌人造成1-4点伤害"的爆破机器人。"""

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }

    def play(self):
        """召唤7个爆破机器人"""
        slots_available = 7 - len(self.controller.field)
        for _ in range(min(7, slots_available + len(self.controller.field))):
            if len(self.controller.field) < 7:
                yield Summon(CONTROLLER, "PVPDR_Boombox_Token")


class PVPDR_Boombox_Token:
    """爆破机器人 / Boom Bot
    1/1 机械 - 亡语：对一个随机敌人造成1-4点伤害。"""

    tags = {
        GameTag.CARDRACE: Race.MECHANICAL,
    }
    atk = 1
    max_health = 1
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, RandomNumber(1, 4))


class PVPDR_PureCold:
    """纯粹寒冷 / Pure Cold
    5费法术 - 造成8点伤害。冻结目标。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 8), Freeze(TARGET)


class PVPDR_WandOfDisintegration:
    """瓦解之杖 / Wand of Disintegration
    10费法术 - 消灭所有敌方随从。"""

    play = Destroy(ENEMY_MINIONS)


class PVPDR_EmbersOfRagnaros:
    """拉格纳罗斯的余烬 / Embers of Ragnaros
    6费法术 - 对两个随机敌方随从造成8点伤害。"""

    def play(self):
        """对两个随机敌方随从造成8点伤害"""
        targets = self.controller.opponent.field
        if targets:
            target1 = self.game.random.choice(targets)
            yield Hit(target1, 8)

        # 第二次选择（可能是同一个目标）
        targets = self.controller.opponent.field
        if targets:
            target2 = self.game.random.choice(targets)
            yield Hit(target2, 8)


class PVPDR_LoomingPresence:
    """迫近的存在 / Looming Presence
    5费法术 - 抽两张牌。获得4点护甲值。"""

    play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


class PVPDR_WaxRager:
    """蜡质暴怒者 / Wax Rager
    3费 5/1 随从 - 亡语：将此随从移回你的手牌。"""

    atk = 5
    max_health = 1
    deathrattle = Bounce(SELF)


class PVPDR_CanopicJars:
    """卡诺匹克罐 / Canopic Jars
    2费法术 - 使你的所有随从获得"亡语：召唤一个1/1的骷髅"。"""

    play = Buff(FRIENDLY_MINIONS, "PVPDR_CanopicJars_Buff")


class PVPDR_CanopicJars_Buff:
    """卡诺匹克罐增益"""
    deathrattle = Summon(CONTROLLER, "PVPDR_Skeleton_Token")


class PVPDR_Skeleton_Token:
    """骷髅 / Skeleton
    1/1 随从"""
    atk = 1
    max_health = 1


class PVPDR_StaffOfScales:
    """鳞片法杖 / Staff of Scales
    3费法术 - 消灭一个随从。召唤一个随机的传说随从。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    play = Destroy(TARGET), Summon(CONTROLLER, RandomLegendaryMinion())


class PVPDR_AnnoyoHorn:
    """烦人的号角 / Annoy-o Horn
    6费法术 - 召唤7个1/2并具有圣盾和嘲讽的随从。"""

    def play(self):
        """召唤满场圣盾嘲讽随从"""
        for _ in range(7):
            if len(self.controller.field) < 7:
                yield Summon(CONTROLLER, "PVPDR_AnnoyoHorn_Token")


class PVPDR_AnnoyoHorn_Token:
    """烦人机器人 / Annoy-o-Tron
    1/2 机械 - 圣盾，嘲讽"""

    tags = {
        GameTag.CARDRACE: Race.MECHANICAL,
        GameTag.DIVINE_SHIELD: True,
        GameTag.TAUNT: True,
    }
    atk = 1
    max_health = 2


class PVPDR_BookOfTheDead:
    """亡者之书 / Book of the Dead
    5费法术 - 对所有敌人造成7点伤害。"""

    play = Hit(ENEMY_CHARACTERS, 7)


class PVPDR_AncientReflections:
    """远古倒影 / Ancient Reflections
    4费法术 - 选择一个随从。召唤它的7个复制。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        """召唤目标随从的7个复制"""
        for _ in range(7):
            if len(self.controller.field) < 7:
                yield Summon(CONTROLLER, ExactCopy(TARGET))

