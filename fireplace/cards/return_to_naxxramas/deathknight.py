from ..utils import *

class NX2_035:
    """霜鳞海妖 (Rimescale Siren)
    战吼：如果你在本牌在你手中时施放过三个法术，随机冻结3个敌方随从。@（还剩{0}个！）@（已经就绪！）
    机制: BATTLECRY
    [迷你扩展包]
    """
    def play(self):
        # 检查是否施放过三个法术（NAGA机制）
        if self.spells_cast_while_in_hand >= 3:
            # 随机冻结3个敌方随从
            yield Freeze(RANDOM(ENEMY_MINIONS) * 3)



class NX2_036:
    """构造区 (Construct Quarter)
    消灭一个友方随从，召唤一个4/5并具有突袭的亡灵。
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    play = (
        Destroy(TARGET),
        Summon(CONTROLLER, "NX2_036t")
    )



class NX2_036t:
    """亡灵构造体 (Undead Construct)
    4/5 突袭亡灵
    """
    # Token 卡牌
    pass



class NX2_037:
    """冰霜女王辛达苟萨 (Frost Queen Sindragosa)
    巨型+2
在一个敌方随从被冻结后，将其消灭。
    机制: COLOSSAL, TRIGGER_VISUAL
    [迷你扩展包]
    """
    # 巨型+2：召唤2个附件
    play = (
        Summon(CONTROLLER, "NX2_037t"),  # 附件1
        Summon(CONTROLLER, "NX2_037t2")  # 附件2
    )

    # 在敌方随从被冻结后，消灭它
    events = SetTags(ENEMY_MINIONS, (GameTag.FROZEN,)).after(
        Destroy(SetTags.TARGET)
    )



class NX2_037t:
    """辛达苟萨的冰霜之翼 (Sindragosa's Frost Wing)
    巨型附件1
    """
    # Token 卡牌
    pass



class NX2_037t2:
    """辛达苟萨的冰霜之翼 (Sindragosa's Frost Wing)
    巨型附件2
    """
    # Token 卡牌
    pass



