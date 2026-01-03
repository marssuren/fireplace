from ..utils import *

class NX2_016:
    """鳍形鬼状 (Nofin's Imp-ossible)
    使所有友方恶魔和鱼人获得“亡语：召唤一个2/2的小鬼鱼人。”
    [迷你扩展包]
    """
    def play(self):
        # 为所有友方恶魔和鱼人添加亡语
        targets = FRIENDLY_MINIONS.filter(lambda m: Race.DEMON in m.races or Race.MURLOC in m.races)
        for target in targets:
            yield Buff(target, "NX2_016e")



class NX2_016e:
    """鳍形鬼状增益 (Nofin's Imp-ossible Buff)"""
    deathrattle = Summon(CONTROLLER, "NX2_016t")



class NX2_016t:
    """小鬼鱼人 (Imp Murloc)
    2/2 恶魔鱼人
    """
    # Token 卡牌
    pass



class NX2_017:
    """瘟疫爆发 (Plague Eruption)
    对所有随从造成$2点伤害。如果你在本局对战中弃过牌，再造成$1点。
    [迷你扩展包]
    """
    def play(self):
        # 基础伤害
        damage = 2
        # 检查是否弃过牌（简化实现：检查弃牌堆）
        if len(self.controller.graveyard.filter(discarded=True)) > 0:
            damage += 1
        yield Hit(ALL_MINIONS, damage)



class NX2_044:
    """可疑的摊贩 (Suspicious Peddler)
    战吼：发现一张法力值消耗为（1）的卡牌。你的对手如果猜中了你的选择，即可获取一张复制。
    机制: BATTLECRY, DISCOVER
    [迷你扩展包]
    """
    # 使用 DiscoverWithPendingGuess 实现"猜牌"机制
    # 发现一张1费卡牌 (自动遵循发现规则：本职业或中立)
    play = DiscoverWithPendingGuess(CONTROLLER, RandomCollectible(cost=1))



