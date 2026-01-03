from ..utils import *

class NX2_032:
    """沉沦的大主教 (Lost Exarch)
    亡语：消耗你所有的法力值，召唤相同数量的2/2的并具有突袭的僵尸。
    机制: DEATHRATTLE
    [迷你扩展包]
    """
    def deathrattle(self, card):
        # 获取当前法力值
        mana = self.controller.mana
        # 消耗所有法力值
        yield SpendMana(CONTROLLER, mana)
        # 召唤相同数量的2/2僵尸
        for i in range(mana):
            yield Summon(CONTROLLER, "NX2_032t")



class NX2_032t:
    """僵尸 (Zombie)
    2/2 突袭
    """
    tags = {GameTag.RUSH: True}



