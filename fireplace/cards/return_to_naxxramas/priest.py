from ..utils import *

class NX2_018:
    """腐烂通灵师 (Rotting Necromancer)
    战吼：探底。如果选中的是亡灵牌，对敌方英雄造成5点伤害。
    机制: BATTLECRY, DREDGE
    [迷你扩展包]
    """
    def play(self):
        # 探底：查看牌库底部的3张牌，将其中一张置于牌库顶部
        if len(self.controller.deck) > 0:
            # 使用Dredge action
            yield Dredge(CONTROLLER)
            # 检查顶部的牌是否是亡灵
            if len(self.controller.deck) > 0:
                top_card = self.controller.deck[0]
                if top_card.race == Race.UNDEAD:
                    yield Hit(ENEMY_HERO, 5)



class NX2_019:
    """精神灼烧 (Mind Sear)
    对一个随从造成$2点伤害。如果该随从死亡，则对敌方英雄造成$3点伤害。
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 对目标造成2点伤害
        yield Hit(TARGET, 2)
        # 如果目标死亡，对敌方英雄造成3点伤害
        if TARGET.dead:
            yield Hit(ENEMY_HERO, 3)



class NX2_020:
    """野蛮残食 (Cannibalize)
    消灭一个随从。为所有友方角色恢复生命值，数值相当于该随从的生命值。
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 获取目标的生命值
        heal_amount = TARGET.health
        # 消灭目标
        yield Destroy(TARGET)
        # 为所有友方角色恢复生命值
        yield Heal(FRIENDLY_CHARACTERS, heal_amount)



