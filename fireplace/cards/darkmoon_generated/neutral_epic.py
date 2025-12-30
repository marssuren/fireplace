from ..utils import *


##
# Minions

class DMF_070:
    """暗月兔子 - Darkmoon Rabbit
    突袭，剧毒。同时对其攻击目标相邻的随从造成伤害。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 10,
        GameTag.RUSH: True,
        GameTag.POISONOUS: True,
    }
    events = Attack(SELF).on(CLEAVE)


class DMF_124:
    """Horrendous Growth (恐怖增生体)
    Corrupt: Gain +1/+1. Can be Corrupted endlessly."""
    # 2费 2/2 - 腐蚀：获得+1/+1。可以无限次腐蚀
    # 特殊：每次腐蚀都会触发，不会失效
    
    def corrupt(self):
        # 每次腐蚀都给予 +1/+1
        # 注意：不设置 corrupted 标志，所以可以重复腐蚀
        return Buff(SELF, "DMF_124e")


class DMF_124e:
    """Corrupted (已腐蚀)"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class DMF_163:
    """Carnival Clown (狂欢小丑)
    Taunt Battlecry: Summon 2 copies of this. Corrupt: Fill your board with copies."""
    # 9费 4/4 嘲讽 - 战吼：召唤2个本随从的复制。腐蚀：用复制填满你的战场
    
    def play(self):
        # 检查是否已腐蚀
        if hasattr(self, 'corrupted') and self.corrupted:
            # 已腐蚀：填满战场（最多7个随从）
            available_slots = 7 - len(self.controller.field)
            return Summon(CONTROLLER, ExactCopy(SELF)) * available_slots
        else:
            # 未腐蚀：召唤2个复制
            return Summon(CONTROLLER, ExactCopy(SELF)) * 2
    
    # 腐蚀效果：标记为已腐蚀
    corrupt = Buff(SELF, "DMF_163e")


class DMF_163e:
    """Corrupted (已腐蚀)"""
    def apply(self, target):
        target.corrupted = True


class YOP_012:
    """Deathwarden (死亡守望者)
    Deathrattles can't trigger."""
    # 3费 2/5 - 亡语无法触发
    # 根据 actions.py 第345行，亡语触发条件是 target.has_deathrattle
    # 所以我们需要禁用所有随从的 has_deathrattle 属性
    
    # 使用 Refresh 光环持续禁用亡语
    update = Refresh(ALL_MINIONS, {
        GameTag.DEATHRATTLE: 0  # 禁用亡语标签
    })
