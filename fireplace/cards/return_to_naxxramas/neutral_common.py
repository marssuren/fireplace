from ..utils import *

class NX2_051:
    """黑暗堕落者影兵 (Darkfallen Shadow)
    突袭。法力渴求（6）：获得复生。
    机制: MANATHIRST, RUSH
    [迷你扩展包]
    """
    tags = {GameTag.RUSH: True}

    def play(self):
        # 法力渴求（6）：获得复生
        if self.controller.max_mana >= 6:
            yield Buff(SELF, "NX2_051e")



class NX2_051e:
    """黑暗堕落者影兵增益 (Darkfallen Shadow Buff)"""
    tags = {GameTag.REBORN: True}



