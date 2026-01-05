"""
决战荒芜之地 - DEATHKNIGHT
"""
from ..utils import *


# COMMON

class DEEP_016:
    """石英碎击槌 - Quartz Crusher
    <b>吸血</b>。<b>冻结</b>任何受到你的英雄伤害的角色。
    """
    # Type: WEAPON | Cost: 4 | Rarity: COMMON | Stats: 3/0 | Mechanics: FREEZE, LIFESTEAL | Runes: B1F1U0
    # 武器攻击后冻结被攻击的目标
    events = Attack(FRIENDLY_HERO).after(Freeze(Attack.DEFENDER))


class DEEP_017:
    """采矿事故 - Mining Mishap
    召唤两个1/1并具有"<b>亡语:</b>召唤一个1/1的脆弱的食尸鬼"的白银之手新兵。
    """
    # Type: SPELL | Cost: 2 | Rarity: COMMON
    # 召唤两个特殊的白银之手新兵
    play = Summon(CONTROLLER, "DEEP_017t") * 2


class DEEP_017t:
    """白银之手新兵 - Silver Hand Recruit
    1/1 带有亡语：召唤一个1/1的脆弱的食尸鬼
    """
    atk = 1
    health = 1
    deathrattle = Summon(CONTROLLER, "DEEP_017t2")


class DEEP_017t2:
    """脆弱的食尸鬼 - Brittle Ghoul
    1/1 亡灵
    """
    atk = 1
    health = 1
    race = Race.UNDEAD


class WW_352:
    """自埋自收 - Bury and Borrow
    造成$3点伤害。<b>发掘</b>一个宝藏。
    """
    # Type: SPELL | Cost: 3 | Rarity: COMMON | Mechanics: EXCAVATE | Runes: B0F1U0
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    play = Hit(TARGET, 3), Excavate(CONTROLLER)


class WW_354:
    """残骸遍野 - Corpse Farm
    对一个随从造成等同于你的<b>残骸</b>数量的伤害。
    """
    # Type: SPELL | Cost: 1 | Rarity: COMMON | Runes: B1F0U1
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        damage = self.controller.corpses
        yield Hit(self.target, damage)


class WW_358:
    """农场小助手 - Farmhand
    <b>战吼:</b><b>发现</b>一张亡灵牌。<b>快枪:</b>其法力值消耗减少(2)点。
    """
    # Type: MINION | Cost: 3 | Rarity: COMMON | Stats: 4/3 | Race: UNDEAD | Mechanics: BATTLECRY, DISCOVER, QUICKDRAW | Runes: B0F0U2
    
    def play(self):
        # 检查是否触发快枪：本回合获得并立即使用
        if self.drawn_this_turn:
            # 快枪：发现的卡牌减少(2)费
            yield Discover(CONTROLLER, RANDOM(FRIENDLY_DECK + UNDEAD)).then(
                Buff(Give.CARD, "WW_358e")
            )
        else:
            # 普通：发现亡灵牌
            yield Discover(CONTROLLER, RANDOM(FRIENDLY_DECK + UNDEAD))


class WW_358e:
    """减费buff"""
    tags = {GameTag.COST: -2}


# RARE

class DEEP_015:
    """义肢假手 - Prosthetic Hand
    <b>磁力</b>。<b>复生</b>
    可以<b>磁力吸附</b>在机械或亡灵上。
    """
    # Type: MINION | Cost: 3 | Rarity: RARE | Stats: 3/1 | Race: MECHANICAL | Mechanics: MAGNETIC, REBORN
    # 参考 TTN_087 (吸附寄生体) 的实现，使用 MAGNETIC_TARGET_RACES 标签
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置可以吸附的目标种族：机械和亡灵
        from ...enums import MAGNETIC_TARGET_RACES
        self.tags[MAGNETIC_TARGET_RACES] = [Race.MECHANICAL, Race.UNDEAD]
    
    # 使用标准磁力函数，会自动读取 MAGNETIC_TARGET_RACES 标签
    magnetic = MAGNETIC("DEEP_015e")


class DEEP_015e:
    """义肢假手附魔"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.MAGNETIC: True,
        GameTag.REBORN: True,
    }


class WW_322:
    """骷髅矿工 - Skeleton Crew
    <b>战吼:</b><b>发掘</b>一个宝藏，其法力值消耗为(0)点。
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 3/3 | Race: UNDEAD | Mechanics: BATTLECRY, EXCAVATE | Runes: B0F1U0
    
    def play(self):
        # 发掘一个宝藏，并使其法力值消耗为0
        yield Excavate(CONTROLLER).then(
            SetTag(Give.CARD, GameTag.COST, 0)
        )


class WW_324:
    """白骨堆 - Pile of Bones
    <b>亡语:</b>在你下次<b>发掘</b>时，再次召唤本随从。
    """
    # Type: MINION | Cost: 2 | Rarity: RARE | Stats: 2/1 | Race: UNDEAD | Mechanics: DEATHRATTLE | Runes: B0F1U1
    
    def deathrattle(self):
        # 给玩家添加一个 buff，在下次发掘时触发召唤
        yield Buff(CONTROLLER, "WW_324e")


class WW_324e:
    """白骨堆待定召唤 buff
    在下次发掘时召唤白骨堆，然后移除自身
    """
    events = Excavate(CONTROLLER).after(
        Summon(CONTROLLER, "WW_324"),
        Destroy(SELF)
    )


class WW_368:
    """耕地轮作 - Crop Rotation
    召唤四个1/1并具有<b>突袭</b>且会在回合结束时死亡的亡灵。
    """
    # Type: SPELL | Cost: 3 | Rarity: RARE | Runes: B0F0U1
    play = Summon(CONTROLLER, "WW_368t") * 4


class WW_368t:
    """临时工 - Temp
    1/1 亡灵，突袭，回合结束时死亡
    """
    atk = 1
    health = 1
    race = Race.UNDEAD
    tags = {GameTag.RUSH: True}
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))


# EPIC

class WW_356:
    """泥犁耕牛 - Plow Ox
    <b>嘲讽</b>。<b>战吼:</b>如果你已经<b>发掘</b>过两次，在本回合中你的下一张牌法力值消耗减少(7)点。
    """
    # Type: MINION | Cost: 7 | Rarity: EPIC | Stats: 7/7 | Race: UNDEAD | Mechanics: BATTLECRY, TAUNT | Runes: B0F1U0
    
    def play(self):
        # 检查是否发掘过两次
        if self.controller.excavate_tier >= 2:
            # 给下一张打出的牌减少(7)费
            yield Buff(CONTROLLER, "WW_356e")


class WW_356e:
    """下一张牌减费"""
    events = Play(CONTROLLER).on(
        Buff(Play.CARD, "WW_356e2"),
        Destroy(SELF)
    )


class WW_356e2:
    """减费7点"""
    tags = {GameTag.COST: -7}


class WW_374:
    """凉心农场 - Chillfallen Farm
    消耗最多8份<b>残骸</b>，随机召唤一个法力值消耗相同的随从。
    """
    # Type: SPELL | Cost: 3 | Rarity: EPIC | Runes: B0F0U1
    
    def play(self):
        # 消耗最多8份残骸
        corpses_to_spend = min(self.controller.corpses, 8)
        if corpses_to_spend > 0:
            yield SpendCorpses(CONTROLLER, corpses_to_spend)
            # 召唤一个法力值消耗相同的随从
            yield Summon(CONTROLLER, RandomMinion(cost=corpses_to_spend))


# LEGENDARY

class WW_357:
    """老腐和老墓 - Maw and Paw
    在你的回合结束时，获得5份<b>残骸</b>。在你的回合开始时，消耗5份<b>残骸</b>，使你的英雄获得+5生命值。
    """
    # Type: MINION | Cost: 4 | Rarity: LEGENDARY | Stats: 2/8 | Race: UNDEAD | Mechanics: TRIGGER_VISUAL | Runes: B1F0U1
    
    events = [
        # 回合结束时获得5份残骸
        OwnTurnEnd(CONTROLLER).on(GainCorpses(CONTROLLER, 5)),
        # 回合开始时消耗5份残骸，英雄获得+5生命值
        OwnTurnBegin(CONTROLLER).on(
            Find(Attr(CONTROLLER, GameTag.CORPSES) >= 5) &
            SpendCorpses(CONTROLLER, 5) &
            Buff(FRIENDLY_HERO, "WW_357e")
        )
    ]


class WW_357e:
    """生命值+5"""
    tags = {GameTag.HEALTH: 5}


class WW_373:
    """矿坑老板雷斯卡 - Reska, the Pit Boss
    <b>突袭</b>。在本局对战中每有一个随从死亡，本牌的法力值消耗便减少(1)点。<b>亡语:</b>随机夺取一个敌方随从的控制权。
    """
    # Type: MINION | Cost: 20 | Rarity: LEGENDARY | Stats: 6/3 | Race: UNDEAD | Mechanics: DEATHRATTLE, RUSH | Runes: B0F1U1
    # 参考 AV_265 (乌祖尔巨兽) 的实现
    
    # 减费机制：每有一个随从死亡减少(1)费
    cost_mod = lambda self, i: -self.controller.minions_killed_this_game
    
    deathrattle = Give(CONTROLLER, RANDOM(ENEMY_MINIONS))
