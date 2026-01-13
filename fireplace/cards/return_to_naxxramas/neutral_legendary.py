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
    events = OWN_TURN_BEGIN.on(
        SetAttr(SELF, "thaddius_odd_mode", lambda self, player: not getattr(entity, "thaddius_odd_mode", True))
    )

    # 根据当前模式决定减费哪些卡牌
    # 使用 Refresh 动态更新手牌费用
    # 在 Hand 类中定义 cost 修改器
    class Hand:
        def cost(self, i):
            # 获取 Thaddius 实体
            thaddius_list = [m for m in self.controller.field if m.id == "NX2_033"]
            if not thaddius_list:
                return i
            
            thaddius = thaddius_list[0]
            is_odd_mode = getattr(thaddius, "thaddius_odd_mode", True)
            
            # 检查当前卡牌费用是否符合减费条件
            if is_odd_mode and i % 2 == 1:  # 奇数模式减费奇数卡
                return i - 2
            elif not is_odd_mode and i % 2 == 0:  # 偶数模式减费偶数卡
                return i - 2
            return i



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



