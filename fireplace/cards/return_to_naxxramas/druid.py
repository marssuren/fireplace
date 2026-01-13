from ..utils import *

class NX2_010:
    """死亡甲虫 (Death Beetle)
    嘲讽。法力渴求（11）：获得+4/+4和冲锋。
    机制: MANATHIRST, TAUNT
    [迷你扩展包]
    """
    tags = {GameTag.TAUNT: True}
    
    def play(self):
        # 法力渴求（11）：获得+4/+4和冲锋
        if self.controller.max_mana >= 11:
            yield Buff(SELF, "NX2_010e")



class NX2_010e:
    """死亡甲虫增益 (Death Beetle Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 4,
        GameTag.CHARGE: True,
    }
    health = 4



class NX2_011:
    """死中新生 (Life from Death)
    抽三张牌。注能（6）：法力值消耗为（1）点。
    机制: INFUSE
    [迷你扩展包]
    """
    infuse = 6  # 注能阈值
    play = Draw(CONTROLLER) * 3
    
    class Hand:
        # 如果已注能，费用变为1
        cost_mod = lambda self, i: -(self.cost - 1) if self.infused else 0
class NX2_012:
    """斜掠 (Rake)
    在本回合中，使你的英雄获得+2攻击力。对一个随从造成等同于你的英雄攻击力的伤害。
    机制: AFFECTED_BY_SPELL_POWER
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 使英雄获得+2攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "NX2_012e")
        # 对目标造成等同于英雄攻击力的伤害
        yield Hit(TARGET, ATK(FRIENDLY_HERO))



class NX2_012e:
    """斜掠增益 (Rake Buff)"""
    tags = {GameTag.ATK: 2}
    # 回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))



