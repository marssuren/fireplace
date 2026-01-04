# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 猎人
"""

from ..utils import *


class AV_113:
    """兽王塔维什 / Beaststalker Tavish
    战吼：发现并施放2个强化奥秘。"""
    # 英雄牌 - 战吼：发现并施放2个强化奥秘
    def play(self):
        """发现并施放2个强化奥秘"""
        # 发现第一个奥秘
        discovered1 = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, FRIENDLY_CLASS + SECRET)
        )
        if discovered1:
            # 施放第一个奥秘（强化版本 - 费用为0）
            yield CastSpell(discovered1)

        # 发现第二个奥秘
        discovered2 = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, FRIENDLY_CLASS + SECRET)
        )
        if discovered2:
            # 施放第二个奥秘（强化版本 - 费用为0）
            yield CastSpell(discovered2)


class AV_147:
    """丹巴达堡垒 / Dun Baldar Bunker
    在你的回合结束时，抽一张奥秘牌，并使其法力值消耗变为（1）点。持续3回合。"""
    # 前地标时代的伪地标设计
    # 使用 PseudoSecret 核心类实现

    # 设置持续时间
    duration = 3

    # 伪奥秘事件：每回合结束时抽奥秘并减费
    pseudo_secret = [
        OwnTurnEnds(CONTROLLER).on(
            Find(FRIENDLY_DECK + SECRET) &
            Draw(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET)).then(
                lambda card: Buff(card, "AV_147e")
            )
        ).then(
            lambda self: self.decrement_duration()
        )
    ]


class AV_147e:
    """丹巴达堡垒效果 - 奥秘费用变为1"""
    tags = {
        GameTag.COST: 1
    }


class AV_224:
    """触发陷阱 / Spring the Trap
    对一个随从造成3点伤害，并从你的牌库中施放一张奥秘牌。荣誉消灭：施放2张。"""
    play = Hit(TARGET, 3)

    # 荣誉消灭：施放2张奥秘
    honorable_kill = (
        Find(FRIENDLY_DECK + SECRET) &
        CastSpell(RANDOM(FRIENDLY_DECK + SECRET)) &
        Find(FRIENDLY_DECK + SECRET) &
        CastSpell(RANDOM(FRIENDLY_DECK + SECRET))
    )

    # 普通情况：施放1张奥秘
    play = (
        Hit(TARGET, 3) &
        Find(FRIENDLY_DECK + SECRET) &
        CastSpell(RANDOM(FRIENDLY_DECK + SECRET))
    )


class AV_226:
    """冰霜陷阱 / Ice Trap
    奥秘：当你的对手施放一个法术时，将其移回他的手牌。该牌的法力值消耗增加（1）点。"""
    secret = (
        Play(OPPONENT, SPELL).on(
            Bounce(Play.CARD) &
            Buff(Play.CARD, "AV_226e")
        )
    )


class AV_226e:
    """冰霜陷阱效果 - 增加1费"""
    tags = {
        GameTag.COST: lambda self, i: self.cost + 1
    }


class AV_244:
    """嗜血者 / Bloodseeker
    荣誉消灭：获得+1/+1。"""
    honorable_kill = Buff(FRIENDLY_WEAPON, "AV_244e")


class AV_244e:
    """嗜血者增益"""
    atk = 1
    max_health = 1


class AV_333:
    """复活宠物 / Revive Pet
    发现一只在本局对战中死亡的友方野兽。召唤它。"""
    play = GenericChoice(
        CONTROLLER,
        Discover(CONTROLLER, FRIENDLY + KILLED + BEAST)
    ).then(
        lambda card: Summon(CONTROLLER, ExactCopy(card))
    )


class AV_334:
    """暴风城战羊 / Stormpike Battle Ram
    突袭 亡语：你的下一只野兽的法力值消耗减少（2）点。"""
    deathrattle = Buff(CONTROLLER, "AV_334e")


class AV_334e:
    """暴风城战羊效果 - 下一只野兽减2费"""
    update = Refresh(FRIENDLY_HAND + BEAST, {
        GameTag.COST: lambda self, i: max(0, self.cost - 2)
    })
    events = Play(CONTROLLER, BEAST).after(Destroy(SELF))


class AV_335:
    """驯羊师 / Ram Tamer
    战吼：如果你控制一张奥秘牌，便获得+1/+1和潜行。"""
    powered_up = Find(FRIENDLY_SECRET)
    play = powered_up & Buff(SELF, "AV_335e")


class AV_335e:
    """驯羊师增益"""
    atk = 1
    max_health = 1
    tags = {GameTag.STEALTH: True}


class AV_336:
    """空军指挥官艾奇曼 / Wing Commander Ichman
    战吼：从你的牌库中召唤一只野兽，并使其获得突袭。如果它在本回合中消灭了一个随从，重复此效果。"""
    def play(self):
        """召唤野兽并给予突袭"""
        # 从牌库中查找野兽
        beasts = [c for c in self.controller.deck
                 if c.type == CardType.MINION and Race.BEAST in c.races]
        if not beasts:
            return

        # 召唤野兽
        beast = random.choice(beasts)
        yield Summon(CONTROLLER, beast)

        # 给予突袭和追踪buff
        yield Buff(beast, "AV_336e")

        # 给控制器添加追踪buff（用于触发重复召唤）
        yield Buff(CONTROLLER, "AV_336_tracker")


class AV_336e:
    """空军指挥官艾奇曼效果 - 突袭"""
    tags = {GameTag.RUSH: True}


class AV_336_tracker:
    """空军指挥官艾奇曼追踪器 - 监听野兽消灭随从"""
    def apply(self, target):
        """初始化追踪器"""
        target.av_336_last_summoned = None

    # 当友方野兽攻击并消灭敌方随从时触发
    events = [
        # 监听攻击事件
        Attack(FRIENDLY + MINION + BEAST).after(
            lambda self, source, attacker, target: (
                # 检查目标是否是随从且已死亡
                self._trigger_summon(attacker.controller)
                if (target.type == CardType.MINION and
                    target.zone == Zone.GRAVEYARD)
                else None
            )
        ),
        # 回合结束时移除追踪器
        OwnTurnEnds(CONTROLLER).on(Destroy(SELF))
    ]

    def _trigger_summon(self, controller):
        """触发召唤新野兽"""
        # 从牌库中查找野兽
        beasts = [c for c in controller.deck
                 if c.type == CardType.MINION and Race.BEAST in c.races]
        if beasts:
            beast = random.choice(beasts)
            controller.game.queue_actions(controller, [
                Summon(controller, beast),
                Buff(beast, "AV_336e")
            ])


class AV_337:
    """山地野熊 / Mountain Bear
    嘲讽 亡语：召唤两只2/4并具有嘲讽的幼熊。"""
    deathrattle = Summon(CONTROLLER, "AV_337t") * 2


class AV_337t:
    """幼熊 / Bear Cub
    2/4 嘲讽 野兽"""
    # 在 CardDefs.xml 中定义


class ONY_008:
    """狂怒之嚎 / Furious Howl
    抽一张牌。重复此效果直到你至少有3张手牌。"""
    def play(self):
        """抽牌直到至少有3张手牌"""
        while len(self.controller.hand) < 3:
            if not self.controller.deck:
                break
            yield Draw(CONTROLLER)


class ONY_009:
    """宠物收藏家 / Pet Collector
    战吼：从你的牌库中召唤一只法力值消耗小于或等于（5）点的野兽。"""
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST <= 5)))


class ONY_010:
    """屠龙射击 / Dragonbane Shot
    造成2点伤害。荣誉消灭：将一张屠龙射击牌置入你的手牌。"""
    play = Hit(TARGET, 2)
    honorable_kill = Give(CONTROLLER, "ONY_010")
