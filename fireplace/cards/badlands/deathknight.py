"""
决战荒芜之地 - DEATHKNIGHT
"""
from ..utils import *


# COMMON

class DEEP_016:
    """石英碎击槌 - Quartzite Crusher
    吸血。冻结任何受到你的英雄伤害的角色。
    """
    # 武器: 4费 3/3 (耐久度实际为0,需要查看数据)
    # 符文消耗: Blood=1, Frost=1
    lifesteal = True
    # 当英雄攻击时,冻结被攻击的角色
    events = Attack(FRIENDLY_HERO).after(Freeze(Attack.DEFENDER))


class DEEP_017:
    """采矿事故 - Mining Casualties
    召唤两个1/1并具有"亡语:召唤一个1/1的脆弱的食尸鬼"的白银之手新兵。
    """
    # 法术: 2费
    # 召唤两个特殊的白银之手新兵(带亡语效果)
    play = Summon(CONTROLLER, "DEEP_017t") * 2


class DEEP_017t:
    """白银之手新兵 - Silver Hand Recruit (Mining Casualties)"""
    # 1/1 随从,带亡语
    atk = 1
    health = 1
    deathrattle = Summon(CONTROLLER, "DEEP_017t2")


class DEEP_017t2:
    """脆弱的食尸鬼 - Frail Ghoul"""
    # 1/1 亡灵
    atk = 1
    health = 1
    race = Race.UNDEAD


class WW_352:
    """自埋自收 - Reap What You Sow
    造成$3点伤害。发掘一个宝藏。
    """
    # 法术: 3费
    # 符文消耗: Frost=1
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    play = Hit(TARGET, 3), Excavate(CONTROLLER)


class WW_354:
    """残骸遍野 - Fistful of Corpses
    对一个随从造成等同于你残骸数量的伤害。
    """
    # 法术: 1费
    # 符文消耗: Blood=1, Unholy=1
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: True,
        PlayReq.REQ_MINION_TARGET: True
    }
    
    def play(self):
        damage = self.controller.corpses
        yield Hit(self.target, damage)


class WW_358:
    """农场小助手 - Farm Hand
    战吼:发现一张亡灵牌。快枪:其法力值消耗减少(2)点。
    """
    # 随从: 3费 4/3 亡灵
    # 符文消耗: Unholy=2
    # TODO: 快枪机制需要核心支持
    # 目前先实现基础战吼效果
    def play(self):
        # 发现一张亡灵牌(任何职业)
        yield Discover(CONTROLLER, RandomCollectible(race=Race.UNDEAD))
        # 快枪效果: 如果是从牌库顶抽到的,则减少(2)费
        # 这需要核心支持 QUICKDRAW 机制,暂时无法实现


# RARE

class DEEP_015:
    """义肢假手 - Prosthetic Hand
    磁力。复生。可以磁力吸附在机械或亡灵上。
    """
    # 随从: 3费 3/1 机械
    # 符文消耗: 无(迷你包卡牌)
    magnetic = True
    reborn = True
    # 特殊: 可以吸附在机械或亡灵上
    # 这需要扩展磁力机制,暂时使用标准磁力


class WW_322:
    """骷髅矿工 - Skeleton Crew
    战吼:发掘一个宝藏。其法力值消耗为(0)点。
    """
    # 随从: 4费 3/3 亡灵
    # 符文消耗: Frost=1
    def play(self):
        # 发掘一个宝藏
        yield Excavate(CONTROLLER)
        # 使获得的宝藏法力值消耗为(0)
        # 这需要在 Excavate 动作后获取生成的卡牌并修改其费用
        # 暂时使用简化实现: 给予下一张手牌 buff
        # TODO: 需要扩展 Excavate 动作以返回生成的卡牌


class WW_324:
    """白骨堆 - Pile of Bones
    亡语:下次你发掘时,重新召唤本随从。
    """
    # 随从: 2费 2/1 亡灵
    # 符文消耗: Frost=1, Unholy=1
    def deathrattle(self):
        # 设置标记: 下次发掘时重新召唤
        yield SetTag(CONTROLLER, "WW_324_RESUMMON", 1)
    
    # 监听发掘事件
    # TODO: 需要在 Excavate 动作中添加事件触发


class WW_368:
    """耕地轮作 - Crop Rotation
    召唤四个1/1并具有突袭的亡灵,它们在回合结束时死亡。
    """
    # 法术: 3费
    # 符文消耗: Unholy=1
    def play(self):
        # 召唤四个1/1亡灵,带突袭
        for _ in range(4):
            yield Summon(CONTROLLER, "WW_368t")


class WW_368t:
    """亡灵 - Undead (Crop Rotation)"""
    # 1/1 亡灵,突袭,回合结束时死亡
    atk = 1
    health = 1
    race = Race.UNDEAD
    rush = True
    # 回合结束时死亡
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))


# EPIC

class WW_356:
    """泥犁耕牛 - Harrowing Ox
    嘲讽。战吼:如果你已经发掘过两次,你本回合的下一张牌法力值消耗减少(7)点。
    """
    # 随从: 7费 7/7 亡灵/野兽
    # 符文消耗: Frost=1
    taunt = True
    
    def play(self):
        # 检查是否已经发掘过至少2次
        if self.controller.times_excavated >= 2:
            # 给予控制者一个buff: 下一张牌减少(7)费
            yield Buff(CONTROLLER, "WW_356e")


class WW_356e:
    """泥犁耕牛效果 - Harrowing Ox Effect"""
    # 下一张打出的牌减少(7)费
    # 这需要一个特殊的 buff 机制
    # 暂时使用简化实现
    pass


class WW_374:
    """凉心农场 - Corpse Farm
    消耗至多8份残骸,召唤一个法力值消耗等同于此的随从。
    """
    # 法术: 3费
    # 符文消耗: Unholy=1
    def play(self):
        # 消耗至多8份残骸
        corpses_to_spend = min(self.controller.corpses, 8)
        if corpses_to_spend > 0:
            yield SpendCorpses(CONTROLLER, corpses_to_spend)
            # 召唤一个法力值消耗等同于残骸数量的随从
            yield Summon(CONTROLLER, RandomMinion(cost=corpses_to_spend))


# LEGENDARY

class WW_357:
    """老腐和老墓 - Maw and Paw
    在你的回合结束时,获得5份残骸。在你的回合开始时,消耗5份残骸,使你的英雄获得+5点生命值。
    """
    # 随从: 4费 2/8 亡灵
    # 符文消耗: Blood=1, Unholy=1
    # 回合结束时获得5份残骸
    events = [
        OwnTurnEnd(CONTROLLER).on(GainCorpses(CONTROLLER, 5)),
        # 回合开始时消耗5份残骸,给英雄+5生命值
        OwnTurnBegin(CONTROLLER).on(
            If(Attr(CONTROLLER, GameTag.CORPSES) >= 5,
               SpendCorpses(CONTROLLER, 5) & Buff(FRIENDLY_HERO, "WW_357e")
            )
        )
    ]


class WW_357e:
    """老腐和老墓效果 - Maw and Paw Effect"""
    # +5 最大生命值
    max_health = 5


class WW_373:
    """矿坑老板雷斯卡 - Reska, the Pit Boss
    突袭。在本局对战中每有一个随从死亡,本牌的法力值消耗便减少(1)点。亡语:夺取一个随机敌方随从的控制权。
    """
    # 随从: 20费 6/3 亡灵
    # 符文消耗: Frost=1, Unholy=1
    rush = True
    
    # 费用减免: 每有一个随从死亡减少(1)费
    @property
    def cost_mod(self):
        # 需要追踪本局对战中死亡的随从数量
        # 这需要在 Player 或 Game 中添加计数器
        return -getattr(self.game, 'minions_died_this_game', 0)
    
    # 亡语: 夺取一个随机敌方随从的控制权
    deathrattle = Steal(RANDOM(ENEMY_MINIONS))


