"""
深暗领域 - 中立 - RARE
"""
from ..utils import *


class GDB_100:
    """阿肯尼特防护水晶 - Arkonite Defense Crystal
    Deathrattle: Gain 4 Armor. Starship Piece

    5费 4/5 中立随从 - 星舰组件
    <b>亡语：</b>获得4点护甲值。
    <b>星舰组件</b>
    """
    # 亡语：获得4点护甲值
    deathrattle = Armor(CONTROLLER, 4)


class GDB_132:
    """躁动的愤怒卫士 - Relentless Wrathguard
    3费 4/2 中立随从 - 恶魔
    <b>战吼：</b>对一个敌方随从造成2点伤害。如果其死亡，则<b>发现</b>一张恶魔牌。
    
    Battlecry: Deal 2 damage to an enemy minion. If it dies, Discover a Demon.
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DEMON
    
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self, target):
        """战吼：对敌方随从造成2点伤害，如果其死亡则发现恶魔"""
        if target:
            # 造成2点伤害
            yield Hit(target, 2)
            # 检查目标是否死亡
            if target.dead or target.to_be_destroyed:
                # 发现一张恶魔牌
                yield Discover(CONTROLLER, RandomMinion(race=Race.DEMON))


class GDB_331:
    """分裂星岩 - Splitting Spacerock
    8费 8/8 中立随从 - 元素
    <b>亡语：</b>召唤两个4/4的分裂巨石。
    
    Deathrattle: Summon two 4/4 Splitting Boulders.
    """
    race = Race.ELEMENTAL
    
    # 亡语：召唤两个4/4的分裂巨石
    deathrattle = Summon(CONTROLLER, "GDB_331t") * 2


class GDB_343:
    """混蒙畸体 - Perplexing Anomaly
    3费 2/5 中立随从 - 元素
    <b>突袭</b>，<b>嘲讽</b>
    <b>……<b>潜行</b>？</b>
    
    Rush, Taunt, ...Stealth?
    
    实现说明：
    - 这张卡同时拥有突袭、嘲讽和潜行三个关键字
    - 这是一个幽默的设计：潜行和嘲讽通常是矛盾的
    - 潜行状态下无法被攻击，但嘲讽要求必须被攻击
    - 一旦使用突袭攻击，潜行就会失效
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
        GameTag.STEALTH: True,
    }
    race = Race.ELEMENTAL


class GDB_862:
    """星系远征军 - Galactic Crusader
    7费 3/9 中立随从 - 德莱尼
    <b>嘲讽</b>
    <b>亡语：</b>随机获得两张圣光法术牌，其法力值消耗减少(3)点。
    
    Taunt. Deathrattle: Get two random Holy spells. They cost (3) less.
    """
    tags = {
        GameTag.TAUNT: True,
    }
    race = Race.DRAENEI
    
    def deathrattle(self):
        """亡语：获得两张随机圣光法术，减3费"""
        # 获得两张随机圣光法术
        for _ in range(2):
            cards = yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.HOLY))
            # 给获得的法术减3费
            if cards:
                for card in cards:
                    if card:
                        yield Buff(card, "GDB_862e")


class SC_010:
    """跳虫 - Zergling
    1费 1/1 中立随从（多职业：死亡骑士/恶魔猎手/猎人/术士）
    <b>战吼：</b>召唤一个1/1的跳虫。
    
    Battlecry: Summon a 1/1 Zergling.
    
    参考：Heroes of StarCraft 迷你包
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        """战吼：召唤一个1/1的跳虫"""
        # 召唤一个跳虫Token
        yield Summon(CONTROLLER, "SC_010t")


class SC_401:
    """SCV - SCV
    1费 1/3 中立随从 - 机械（多职业：圣骑士/萨满/战士）
    <b>战吼：</b>你的下一次<b>星舰</b>发射的法力值消耗减少(2)点。
    
    Battlecry: Your next Starship launch costs (2) less.
    
    参考：Heroes of StarCraft 迷你包
    实现说明：
    - 给玩家添加buff，追踪下一次星舰发射减费
    - 在LaunchStarship action中检查并应用减费
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.MECHANICAL
    
    def play(self):
        """战吼：下一次星舰发射减2费"""
        # 给控制者添加buff，使下一次星舰发射减2费
        yield Buff(CONTROLLER, "SC_401e")


class SC_783:
    """虚空辉光舰 - Void Ray
    3费 3/2 中立随从 - 机械（多职业：德鲁伊/法师/牧师/潜行者）
    <b>突袭</b>，<b>圣盾</b>
    <b>战吼：</b>如果本牌的法力值消耗为(0)点，则获得+2/+2。
    
    Rush, Divine Shield. Battlecry: If this costs (0), gain +2/+2.
    
    参考：Heroes of StarCraft 迷你包
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.DIVINE_SHIELD: True,
        GameTag.BATTLECRY: True,
    }
    race = Race.MECHANICAL
    
    def play(self):
        """战吼：如果本牌费用为0，则获得+2/+2"""
        # 检查本牌当前费用是否为0
        if self.cost == 0:
            # 给自己+2/+2
            yield Buff(SELF, "SC_783e")


