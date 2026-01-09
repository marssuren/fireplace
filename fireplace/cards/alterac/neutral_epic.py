# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 中立史诗
"""

from ..utils import *


class AV_102:
    """冷饮制冰机 / Popsicooler
    亡语：冻结两个随机敌方随从。"""
    deathrattle = Freeze(RANDOM(ENEMY_MINIONS) * 2)


class AV_128:
    """冰封猛犸 / Frozen Mammoth
    该随从被冻结，直到你施放一个火焰法术。"""
    events = [
        # 进入战场时冻结自己
        Play(CONTROLLER, SELF).after(Freeze(SELF)),
        # 施放火焰法术时解冻
        Play(CONTROLLER, SPELL + FIRE).after(Unfreeze(SELF))
    ]


class AV_138:
    """恐怖图腾赏金猎人 / Grimtotem Bounty Hunter
    战吼：消灭一个敌方传说随从。"""
    play = Destroy(TARGET)


class AV_139:
    """憎恶军官 / Abominable Lieutenant
    在你的回合结束时，吞食一个随机敌方随从并获得其属性值。"""
    events = OWN_TURN_END.on(
        Find(ENEMY_MINIONS) & (
            Buff(SELF, "AV_139e", atk=ATK(RANDOM_ENEMY_MINION), health=CURRENT_HEALTH(RANDOM_ENEMY_MINION)),
            Destroy(RANDOM_ENEMY_MINION)
        )
    )


class AV_139e:
    """憎恶军官增益"""
    # 动态设置属性值


class AV_222:
    """话痨奥术师 / Spammy Arcanist
    战吼：对所有其他随从造成1点伤害。如果有随从死亡，重复此效果。"""
    def play(self, source, target):
        """递归AOE伤害"""
        from fireplace.actions import Hit, Destroy
        from fireplace.enums import Zone
        
        while True:
            # 对所有其他随从造成1点伤害
            other_minions = [m for m in source.game.board if m != source and m.zone == Zone.PLAY]
            if not other_minions:
                break
            
            any_died = False
            for minion in other_minions:
                source.game.queue_actions(source, [Hit(minion, 1)])
                if minion.zone == Zone.GRAVEYARD or minion.to_be_destroyed:
                    any_died = True
            
            # 如果没有随从死亡，停止循环
            if not any_died:
                break


class ONY_003:
    """雏龙狂魔 / Whelp Bonker
    暴怒和荣誉击杀：抽一张牌。"""
    frenzy = Draw(CONTROLLER)
    honorable_kill = Draw(CONTROLLER)
