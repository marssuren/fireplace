from ..utils import *

class NX2_033:
    """巨怪塔迪乌斯 (Thaddius, Monstrosity)
    嘲讽。你的法力值消耗为奇数的牌的法力值消耗减少（2）点。（每回合切换极性！）
    机制: AURA, TAUNT, TRIGGER_VISUAL
    [迷你扩展包]
    """
    tags = {GameTag.TAUNT: True}

    # 打出时初始化为奇数减费模式
    play = SetAttr(SELF, "thaddius_odd_mode", True)

    # 回合开始时切换极性
    events = OwnTurnBegin(CONTROLLER).on(
        SetAttr(SELF, "thaddius_odd_mode", lambda self, entity: not getattr(entity, "thaddius_odd_mode", True))
    )

    # 根据当前模式决定减费哪些卡牌
    # 如果是奇数模式，减费奇数卡牌；否则减费偶数卡牌
    def update(self, entity):
        is_odd_mode = getattr(entity, "thaddius_odd_mode", True)
        if is_odd_mode:
            return Find(FRIENDLY_HAND + ODD_COST) | Buff("NX2_033e")
        else:
            return Find(FRIENDLY_HAND + EVEN_COST) | Buff("NX2_033e")



class NX2_033e:
    """巨怪塔迪乌斯增益 (Thaddius Buff)"""
    tags = {GameTag.COST: -2}



class NX2_034:
    """战争之骑士瑞文戴尔 (Rivendare, Warrider)
    亡语：将其他3位骑士洗入你的牌库。
    机制: DEATHRATTLE
    [迷你扩展包]
    """
    deathrattle = (
        Shuffle(CONTROLLER, "NX2_034t"),  # 饥荒之骑士
        Shuffle(CONTROLLER, "NX2_034t2"), # 死亡之骑士
        Shuffle(CONTROLLER, "NX2_034t3")  # 瀟疫之骑士
    )



class NX2_034t:
    """饥荒之骑士 (Famine)"""
    # Token 卡牌
    pass



class NX2_034t2:
    """死亡之骑士 (Death)"""
    # Token 卡牌
    pass



class NX2_034t3:
    """瀟疫之骑士 (Pestilence)"""
    # Token 卡牌
    pass



