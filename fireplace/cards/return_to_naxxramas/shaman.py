from ..utils import *

class NX2_007:
    """霜鳍咀嚼者 (Frostfin Chomper)
    战吼：
如果你在上个回合使用过元素牌，则召唤三个1/1的鱼人。
    机制: BATTLECRY
    [迷你扩展包]
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 检查上回合是否使用过元素牌
        if self.controller.elemental_played_last_turn:
            # 召唤3个1/1的鱼人
            yield Summon(CONTROLLER, "CS2_173") * 3  # Murloc Raider



class NX2_007t:
    """僵尸鱼人 (Zombie Murloc)?"""
    race = Race.MURLOC

class NX2_008:
    """炽焰变幻 (Blazing Transmutation)
    选择一个随从，将其变形成为你发现的法力值消耗增加（1）点的随从。
    机制: DISCOVER
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 获取目标随从的费用
        target_cost = TARGET.cost + 1
        # 发现一个相同费用的随从
        discovered = yield GenericChoice(CONTROLLER, RandomMinion(cost=target_cost) * 3)
        if discovered:
            # 将目标变形为发现的随从
            yield Morph(TARGET, discovered)



class NX2_009:
    """冰冷贮藏 (Cold Storage)
    冻结一个随从，将一张它的复制置入你的手牌。
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    play = (
        Freeze(TARGET),
        Give(CONTROLLER, ExactCopy(TARGET))
    )



