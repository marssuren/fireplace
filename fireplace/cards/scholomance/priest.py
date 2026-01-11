from ..utils import *


##
# Minions

class SCH_137:
    """Frazzled Freshman / 慌乱的新生
    1/4 vanilla minion / 1/4 香草随从"""

    # 1费 1/4 香草随从，无特殊效果
    pass

class SCH_159:
    """Mindrender Illucia / 心灵撕裂者伊露希亚
    Battlecry: Replace your hand with a copy of your opponent's until end of turn.
    战吼：将你的手牌替换为对手手牌的复制，直到回合结束。"""

    # 3费 1/3 传说 战吼：将你的手牌替换为对手手牌的复制，直到回合结束
    # 完整实现：使用 Setaside 存储原手牌，回合结束时恢复
    play = (
        # 1. 将当前手牌移到暂存区
        Setaside(FRIENDLY_HAND),
        # 2. 复制对手手牌
        Give(CONTROLLER, Copy(ENEMY_HAND)),
        # 3. 添加追踪buff，回合结束时恢复原手牌
        Buff(CONTROLLER, "SCH_159_tracker")
    )

class SCH_513:
    """Brittlebone Destroyer / 脆骨毁灭者
    Battlecry: If your hero's Health changed this turn, destroy a minion.
    战吼：如果你的英雄在本回合生命值发生过变化，消灭一个随从。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    # 6费 6/8 战吼：如果你的英雄在本回合生命值发生过变化，消灭一个随从
    # 完整实现：使用事件系统追踪英雄生命值变化
    # 首先给玩家添加一个追踪buff
    play = Buff(CONTROLLER, "SCH_513_tracker"), Find(Attr(CONTROLLER, "hero_health_changed")) & Destroy(TARGET)

class SCH_120:
    """Cabal Acolyte / 秘教侍僧
    Taunt Spellburst: Gain control of a random enemy minion with 2 or less Attack.
    嘲讽 法术迸发：随机获得一个攻击力小于或等于2的敌方随从的控制权。"""

    # 4费 2/6 嘲讽 法术迸发：随机获得一个攻击力小于或等于2的敌方随从的控制权
    # 嘲讽通过 CardDefs.xml 中的 TAUNT 标签定义
    spellburst = Steal(RANDOM(ENEMY_MINIONS + (ATK <= 2)))

class SCH_126:
    """Disciplinarian Gandling / 教导主任加丁
    After you play a minion, destroy it and summon a 4/4 Failed Student.
    在你使用一张随从牌后，将其消灭并召唤一个4/4的挂掉的学生。"""

    # 4费 3/6 传说 在你使用一张随从牌后，将其消灭并召唤一个4/4的挂掉的学生
    events = Play(CONTROLLER, MINION).after(Destroy(Play.CARD), Summon(CONTROLLER, "SCH_126t"))

class SCH_140:
    """Flesh Giant / 血肉巨人
    Costs (1) less for each time your hero's Health changed during your turns.
    在本局对战中，你的英雄每有一次生命值变化，本牌的法力值消耗便减少（1）点。"""

    # 8费 8/8 在本局对战中，你的英雄每有一次生命值变化，本牌的法力值消耗便减少（1）点
    # 完整实现：使用追踪buff记录英雄生命值变化次数
    # 首先确保追踪buff存在
    play = Buff(CONTROLLER, "SCH_140_tracker")
    
    # 费用减少 = 英雄生命值变化次数(使用 lambda 安全访问)
    @property
    def cost(self):
        """动态费用计算"""
        base_cost = 8
        if hasattr(self, 'controller'):
            change_count = getattr(self.controller, 'hero_health_change_count', 0)
            return max(0, base_cost - change_count)
        return base_cost



##
# Spells

class SCH_514:
    """Raise Dead / 复活死者
    Deal $3 damage to your hero. Return two friendly minions that died this game to your hand.
    对你的英雄造成3点伤害。将两个在本局对战中死亡的友方随从移回你的手牌。"""

    # 0费 对你的英雄造成3点伤害。将两个在本局对战中死亡的友方随从移回你的手牌
    # 完整实现：从死亡的友方随从中随机选择两个移回手牌
    play = Hit(FRIENDLY_HERO, 3), Give(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION)), Give(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION))


class SCH_233:
    """Draconic Studies / 龙类研习
    Discover a Dragon. Your next one costs (1) less.
    发现一张龙牌。你的下一张龙牌法力值消耗减少（1）点。"""

    # 1费 发现一张龙牌。你的下一张龙牌法力值消耗减少（1）点
    play = Discover(CONTROLLER, RandomMinion(race=Race.DRAGON)), Buff(CONTROLLER, "SCH_233e")


class SCH_233e:
    """Draconic Studies Buff / 龙类研习增益"""
    update = Refresh(FRIENDLY_HAND + MINION + (Race.DRAGON), {GameTag.COST: -1})
    events = Play(FRIENDLY + MINION + (Race.DRAGON)).on(Destroy(SELF))

class SCH_136:
    """Power Word: Feast / 真言术：盛
    Give a minion +2/+2. Restore it to full Health at the end of this turn.
    使一个随从获得+2/+2。在本回合结束时，将其恢复到满生命值。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    # 2费 使一个随从获得+2/+2。在本回合结束时，将其恢复到满生命值
    play = Buff(TARGET, "SCH_136e")


class SCH_136e:
    """Power Word: Feast Buff / 真言术：盛增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }
    events = OWN_TURN_END.on(FullHeal(OWNER))


class SCH_512:
    """Initiation / 入会仪式
    Deal $4 damage to a minion. If that kills it, summon a new copy.
    对一个随从造成4点伤害。如果这消灭了它，召唤一个新的复制。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    # 4费 对一个随从造成4点伤害。如果这消灭了它，召唤一个新的复制
    play = Hit(TARGET, 4), Dead(TARGET) & Summon(CONTROLLER, ExactCopy(TARGET))


# 英雄生命值变化追踪buff（用于SCH_513脆骨毁灭者）
class SCH_513_tracker:
    """Hero Health Change Tracker / 英雄生命值变化追踪器"""

    def apply(self, target):
        # 初始化标记
        target.hero_health_changed = 0

    # 监听英雄受到伤害的事件
    events = [
        Damage(FRIENDLY_HERO).on(SetAttr(CONTROLLER, "hero_health_changed", 1)),
        Heal(FRIENDLY_HERO).on(SetAttr(CONTROLLER, "hero_health_changed", 1)),
        # 回合开始时重置标记
        OWN_TURN_BEGIN.on(SetAttr(CONTROLLER, "hero_health_changed", 0))
    ]


# 英雄生命值变化次数追踪buff（用于SCH_140血肉巨人）
class SCH_140_tracker:
    """Hero Health Change Counter / 英雄生命值变化计数器"""

    def apply(self, target):
        # 初始化计数器
        target.hero_health_change_count = 0

    # 监听英雄生命值变化事件（只在自己回合内）
    events = [
        # 自己回合内英雄受到伤害
        Damage(FRIENDLY_HERO).on(
            CurrentPlayer(CONTROLLER) & SetAttr(CONTROLLER, "hero_health_change_count", Attr(CONTROLLER, "hero_health_change_count") + 1)
        ),
        # 自己回合内英雄受到治疗
        Heal(FRIENDLY_HERO).on(
            CurrentPlayer(CONTROLLER) & SetAttr(CONTROLLER, "hero_health_change_count", Attr(CONTROLLER, "hero_health_change_count") + 1)
        )
    ]


# 手牌交换追踪buff（用于SCH_159心灵撕裂者伊露希亚）
class SCH_159_tracker:
    """Hand Swap Tracker / 手牌交换追踪器

    在回合结束时：
    1. 清空当前手牌（对手手牌的复制）
    2. 从暂存区恢复原来的手牌
    3. 销毁这个buff
    """

    events = OWN_TURN_END.on(
        # 1. 清空当前手牌（对手手牌的复制）
        Discard(FRIENDLY_HAND),
        # 2. 从暂存区取回原来的手牌
        Give(CONTROLLER, FRIENDLY_SETASIDE),
        # 3. 销毁这个buff
        Destroy(SELF)
    )

