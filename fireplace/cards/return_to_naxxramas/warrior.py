from ..utils import *

class NX2_027:
    """血肉塑造者 (Fleshshaper)
    嘲讽。战吼：如果你的护甲值大于或等于5点，召唤一个本随从的复制。
    机制: BATTLECRY, TAUNT
    [迷你扩展包]
    """
    tags = {GameTag.TAUNT: True}
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 检查护甲值
        if self.controller.hero.armor >= 5:
            # 召唤一个复制
            yield Summon(CONTROLLER, ExactCopy(SELF))



class NX2_028:
    """钩拳-3000型 (Hookfist-3000)
    在你的英雄攻击后，获得4点护甲值并抽一张牌。
    机制: TRIGGER_VISUAL
    [迷你扩展包]
    """
    events = Attack(FRIENDLY_HERO).after(
        Armor(CONTROLLER, 4),
        Draw(CONTROLLER)
    )



class NX2_029:
    """训练课程 (Training Session)
    发现一张嘲讽随从牌。如果你在本回合使用发现的牌，重复此效果。
    机制: DISCOVER
    [迷你扩展包]
    """
    def play(self):
        # 发现一张嘲讽随从
        discovered = yield GenericChoice(CONTROLLER, RandomMinion(taunt=True) * 3)
        if discovered:
            # 简化实现：直接给予卡牌，不检查是否使用
            # 完整实现需要追踪发现的卡牌是否在本回合使用
            pass



