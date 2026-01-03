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



class CastTrainingSession(TargetedAction):
    def do(self, source, target):
        # 创建并施放"训练课程"的复制
        # 需使用 SETASIDE 区域创建，避免进入手牌
        card = source.controller.card("NX2_029", zone=Zone.SETASIDE)
        source.game.queue_actions(source, [CastSpell(card)])


class NX2_029e:
    """训练课程增益 (Training Session Buff)"""
    # [x]本回合内
    tags = {GameTag.ONE_TURN_EFFECT: True}
    # 如果你在本回合使用发现的牌，重复此效果
    events = Play(CONTROLLER, OWNER).after(CastTrainingSession(CONTROLLER, None))


class NX2_029:
    """训练课程 (Training Session)
    发现一张嘲讽随从牌。如果你在本回合使用发现的牌，重复此效果。
    机制: DISCOVER
    [迷你扩展包]
    """
    # 发现一张嘲讽随从，给予玩家，并添加监控Buff
    play = Discover(CONTROLLER, RandomMinion(taunt=True)).then(
        Give(CONTROLLER, Discover.CARD),
        Buff(Discover.CARD, "NX2_029e")
    )



