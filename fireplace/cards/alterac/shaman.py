# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 萨满
"""

from ..utils import *


# ========== 1费法术 ==========

class AV_266:
    """寒风 / Windchill
    冻结一个随从。抽一张牌。"""
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Freeze(TARGET) + Draw(CONTROLLER)


# ========== 2费法术 ==========

class ONY_013:
    """凛冽寒冷 / Bracing Cold
    为你的英雄恢复5点生命值。使你手牌中一张随机法术牌的法力值消耗减少（2）点。"""
    play = Heal(FRIENDLY_HERO, 5) + Buff(RANDOM(FRIENDLY_HAND + SPELL), "ONY_013e")


class ONY_013e:
    """凛冽寒冷增益"""
    cost = -2


class AV_259:
    """冰霜刺咬 / Frostbite
    造成3点伤害。荣誉消灭：你的对手的下一个法术的法力值消耗增加（2）点。"""
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)
    honorable_kill = Buff(ENEMY_HERO, "AV_259e")


class AV_259e:
    """冰霜刺咬效果 - 下一个法术+2费"""
    events = Play(OPPONENT, SPELL).on(
        Buff(Play.CARD, "AV_259e2") & Destroy(SELF)
    )


class AV_259e2:
    """冰霜刺咬 - 法术增加费用"""
    cost = 2


class ONY_012:
    """灵魂坐骑 / Spirit Mount
    使一个随从获得+1/+2和法术伤害+1。当它死亡时，召唤一只灵魂迅猛龙。"""
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "ONY_012e")


class ONY_012e:
    """灵魂坐骑增益"""
    atk = 1
    max_health = 2
    spellpower = 1
    deathrattle = Summon(CONTROLLER, "ONY_012t")


class ONY_012t:
    """灵魂迅猛龙 / Spirit Raptor
    1/1 野兽"""
    # 在 CardDefs.xml 中定义


# ========== 3费法术 ==========

class AV_250:
    """雪球大战 / Snowball Fight!
    对一个随从造成1点伤害并冻结它。如果它存活，对另一个随从重复此效果！"""
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        """循环对随从造成伤害并冻结，直到目标死亡或没有其他目标"""
        target = self.target
        hit_targets = []

        while target and target.zone == Zone.PLAY:
            # 对当前目标造成伤害并冻结
            yield Hit(target, 1)
            yield Freeze(target)
            hit_targets.append(target)

            # 检查目标是否存活
            if target.zone != Zone.PLAY or target.health <= 0:
                break

            # 获取其他可选目标（排除已经被击中的目标）
            other_minions = [m for m in self.game.board if m not in hit_targets and m.zone == Zone.PLAY]
            if not other_minions:
                break

            # 随机选择下一个目标
            target = self.game.random.choice(other_minions)


# ========== 4费法术 ==========

class AV_268:
    """野爪洞穴 / Wildpaw Cavern
    在你的回合结束时，召唤一个3/4并会冻结的元素。持续3个回合。"""
    play = Summon(CONTROLLER, "AV_268ps")


class AV_268ps:
    """野爪洞穴（伪奥秘）- 持续3回合
    使用PseudoSecret机制，占用奥秘槽位但具有持续时间"""
    # 设置持续时间（PseudoSecret会自动读取）
    duration = 3

    # 伪奥秘事件：每回合结束时召唤元素并递减持续时间
    pseudo_secret = [
        OwnTurnEnds(CONTROLLER).on(
            Summon(CONTROLLER, "AV_268t")
        ).then(
            lambda self: self.decrement_duration()
        )
    ]


class AV_268t:
    """冰霜元素 / Frost Elemental
    3/4 元素，攻击时冻结目标"""
    # 在 CardDefs.xml 中定义


# ========== 5费法术 ==========

class ONY_011:
    """别站在火里！ / Don't Stand in the Fire!
    随机对所有敌方随从造成共10点伤害。过载：（1）"""
    play = Hit(RANDOM_ENEMY_MINION * 10, 1)


# ========== 6费法术 ==========

class AV_107:
    """冰川化 / Glaciate
    发现一张法力值消耗为（8）的随从牌。召唤它并使其冻结。"""
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion(cost=8))) + (
        Summon(CONTROLLER, Copy(GenericChoice.CARD)) + Freeze(Summon.CARD)
    )


# ========== 随从卡牌 ==========

class AV_260:
    """碎冰元素 / Sleetbreaker
    战吼：将一张寒风牌置入你的手牌。"""
    play = Give(CONTROLLER, "AV_266")


class AV_251:
    """狡诈的雪怪哥布林 / Cheaty Snobold
    在一个敌人被冻结后，对其造成3点伤害。"""
    events = Freeze(ENEMY).after(
        Hit(Freeze.TARGET, 3)
    )


class AV_255:
    """雪崩守护者 / Snowfall Guardian
    战吼：冻结所有其他随从。"""
    play = Freeze(ALL_MINIONS - SELF)


class AV_257:
    """熊人格拉希尔 / Bearon Gla'shear
    战吼：在本局对战中，你每施放一个冰霜法术，便召唤一个3/4并会冻结的元素。"""
    def play(self):
        """根据施放的冰霜法术数量召唤元素"""
        # 计算施放的冰霜法术数量
        frost_spells_count = getattr(self.controller, 'frost_spells_cast', 0)

        # 召唤对应数量的冰霜元素
        for _ in range(frost_spells_count):
            yield Summon(CONTROLLER, "AV_268t")


# ========== 英雄卡 ==========

class AV_258:
    """元素使者布鲁坎 / Bru'kan of the Elements
    战吼：召唤两个元素之力！"""
    def play(self):
        """让玩家选择两个元素召唤"""
        # 第一次选择
        first_choice = yield GenericChoice(CONTROLLER, [
            "AV_258t",   # 火焰元素
            "AV_258t2",  # 冰霜元素
            "AV_258t3",  # 自然元素
            "AV_258t4",  # 闪电元素
        ])
        
        if not first_choice:
            return

        # 召唤第一个选择的元素
        first_card = first_choice[0] if isinstance(first_choice, list) else first_choice
        yield Summon(CONTROLLER, first_card)
        
        # 第二次选择（排除第一次选择的元素）
        all_elements = ["AV_258t", "AV_258t2", "AV_258t3", "AV_258t4"]
        first_id = first_card.id if hasattr(first_card, 'id') else first_card
        remaining_elements = [e for e in all_elements if e != first_id]
        
        second_choice = yield GenericChoice(CONTROLLER, remaining_elements)
        
        if not second_choice:
            return
        
        # 召唤第二个选择的元素
        second_card = second_choice[0] if isinstance(second_choice, list) else second_choice
        yield Summon(CONTROLLER, second_card)


class AV_258t:
    """火焰元素 / Fire Elemental
    6/6 元素"""
    # 在 CardDefs.xml 中定义


class AV_258t2:
    """冰霜元素 / Frost Elemental
    6/6 元素"""
    # 在 CardDefs.xml 中定义


class AV_258t3:
    """自然元素 / Nature Elemental
    6/6 元素"""
    # 在 CardDefs.xml 中定义


class AV_258t4:
    """闪电元素 / Lightning Elemental
    6/6 元素"""
    # 在 CardDefs.xml 中定义


