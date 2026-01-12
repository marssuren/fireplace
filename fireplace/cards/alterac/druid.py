# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 德鲁伊
"""

from ..utils import *


class AV_205:
    """森林之王的古树 / Guff Runetotem
    战吼：你的法力值上限变为20点。获得一个空的法力水晶。"""
    play = (
        SetTags(CONTROLLER, {GameTag.RESOURCES: 20}),
        GainMana(CONTROLLER, 1)
    )


class AV_210:
    """开路者 / Pathmaker
    战吼：施放你的上一个抉择法术的另一个选项。"""
    def play(self):
        """施放上一个抉择法术的另一个选项"""
        # 使用核心追踪的抉择信息
        if not hasattr(self.controller, 'last_choose_one_card'):
            return
        
        last_card = self.controller.last_choose_one_card
        last_choice = self.controller.last_choose_one_choice
        
        if not last_card or not last_choice:
            return
        
        # 找到另一个选项
        for choice_card in last_card.choose_cards:
            if choice_card != last_choice:
                # 施放另一个选项
                actions = choice_card.get_actions("play")
                if actions:
                    yield actions
                break


class AV_211:
    """凶恶霜狼 / Frostsaber Matriarch
    潜行，亡语：召唤一只2/2并具有潜行的狼。"""
    deathrattle = Summon(CONTROLLER, "AV_211t")


class AV_211t:
    """霜狼幼崽 / Frostwolf Cub
    2/2 潜行 野兽"""
    # 在 CardDefs.xml 中定义


class AV_291:
    """霜刃豹头领 / Frostsaber Matriarch
    嘲讽 在本局对战中，你每召唤一只野兽，本牌的法力值消耗便减少（1）点。"""
    # 追踪召唤的野兽数量
    cost_mod = lambda self, i: -self.controller.beasts_summoned_this_game


class AV_292:
    """野性之心 / Heart of the Wild
    使一个随从获得+2/+2，然后使你的野兽获得+1/+1。"""
    play = (Buff(TARGET, "AV_292e"), Buff(FRIENDLY_MINIONS + BEAST, "AV_292e2"))


class AV_292e:
    """野性之心增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


class AV_292e2:
    """野性之心野兽增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class AV_293:
    """空军指挥官穆维里克 / Wing Commander Mulverick
    突袭。你的随从拥有"荣誉消灭：召唤一只2/2并具有突袭的双足飞龙。"""
    # 给所有友方随从添加荣誉消灭效果
    update = Refresh(FRIENDLY_MINIONS, {
        HONORABLE_KILL: lambda self: Summon(CONTROLLER, "AV_293t")
    })


class AV_293t:
    """双足飞龙 / Wyvern
    2/2 突袭 野兽"""
    # 在 CardDefs.xml 中定义


class AV_294:
    """怒爪精锐 / Dire Frostwolf
    战吼：在本回合中，使所有其他友方角色获得+1攻击力。"""
    play = Buff(FRIENDLY_CHARACTERS - SELF, "AV_294e")


class AV_294e:
    """怒爪精锐增益"""
    tags = {GameTag.ATK: 1}
    events = OWN_TURN_END.on(Destroy(SELF))


class AV_295:
    """占领冷齿矿洞 / Capture Coldtooth Mine
    抉择：抽取你法力值消耗最低的牌；或者抽取你法力值消耗最高的牌。"""
    choose = ["AV_295a", "AV_295b"]


class AV_295a:
    """抽取最低费用牌"""
    play = lambda self: [
        Draw(CONTROLLER, min(self.controller.deck, key=lambda c: c.cost))
    ] if self.controller.deck else []


class AV_295b:
    """抽取最高费用牌"""
    play = lambda self: [
        Draw(CONTROLLER, max(self.controller.deck, key=lambda c: c.cost))
    ] if self.controller.deck else []


class AV_296:
    """傲狮猎手 / Pride Seeker
    战吼：你的下一张抉择牌法力值消耗减少（2）点。"""
    play = Buff(CONTROLLER, "AV_296e")


class AV_296e:
    """傲狮猎手效果"""
    # 下一张抉择牌减费
    update = Refresh(FRIENDLY_HAND + CHOOSE_ONE, {
        GameTag.COST: lambda self, i: max(0, self.cost - 2)
    })
    events = Play(CONTROLLER, CHOOSE_ONE).after(Destroy(SELF))


class AV_360:
    """霜狼巢穴 / Frostwolf Kennels
    在你的回合结束时，召唤一只2/2并具有潜行的狼。持续3回合。"""
    # 前地标时代的伪地标设计
    # 使用 PseudoSecret 核心类实现
    
    # 设置持续时间
    duration = 3
    
    # 伪奥秘事件：每回合结束时召唤狼
    pseudo_secret = [
        OWN_TURN_END.on(
            Summon(CONTROLLER, "AV_211t")
        ).then(
            lambda self: self.decrement_duration()
        )
    ]


class ONY_018:
    """鳞片守护者 / Scale of Onyxia
    抉择：为你的英雄恢复8点生命值；或者造成4点伤害。"""
    choose = ["ONY_018a", "ONY_018b"]


class ONY_018a:
    """恢复生命值"""
    play = Heal(FRIENDLY_HERO, 8)


class ONY_018b:
    """造成伤害"""
    play = Hit(TARGET, 4)


class ONY_019:
    """奥妮克希亚协调员 / Onyxian Warder
    战吼：发现一张抉择牌，使其同时拥有两个效果。"""
    play = Discover(
        CONTROLLER,
        lambda card: card.has_choose_one
    ).then(
        lambda card: Buff(card, "ONY_019e")
    )


class ONY_019e:
    """协调员增益 - 同时拥有两个效果"""
    # 使抉择牌同时拥有两个效果
    tags = {
        GameTag.CHOOSE_BOTH: True
    }


class ONY_021:
    """奥妮克希亚的鳞片 / Onyxian Scales
    召唤七只2/1并具有突袭的雏龙。"""
    play = Summon(CONTROLLER, "ONY_021t") * 7


class ONY_021t:
    """奥妮克希亚雏龙 / Onyxian Whelp
    2/1 突袭 龙"""
    # 在 CardDefs.xml 中定义
