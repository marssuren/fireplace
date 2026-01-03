from ..utils import *

class NX2_024:
    """蹒跚的肉用僵尸 (Shambling Chow)
    突袭。亡语：对你的英雄造成4点伤害。
    机制: DEATHRATTLE, RUSH
    [迷你扩展包]
    """
    tags = {GameTag.RUSH: True}
    deathrattle = Hit(FRIENDLY_HERO, 4)



class NX2_025:
    """灾难之握 (Calamity's Grasp)
    亡语：随机将一张流放牌置入你的
手牌。
    机制: DEATHRATTLE
    [迷你扩展包]
    """
    deathrattle = Give(CONTROLLER, RandomCard(outcast=True))



class NX2_026:
    """邪鳞唤醒师 (Felscale Evoker)
    战吼：如果你在本牌在你手中时施放过三个法术，从你的牌库中召唤一个不同的恶魔。@（还剩{0}个！）@（已经就绪！）
    机制: BATTLECRY
    [迷你扩展包]
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    
    def play(self):
        # 检查是否施放过三个法术（NAGA机制）
        if self.spells_cast_while_in_hand >= 3:
            # 从牌库中召唤一个不同的恶魔（排除同名卡牌）
            yield Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + DEMON - ID(SELF.id)))



