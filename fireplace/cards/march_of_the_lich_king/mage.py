"""巫妖王的进军 - 法师 (March of the Lich King - Mage)"""
from ..utils import *


class RLK_541:
    """维萨鲁斯 (Vexallus)
    你的奥术法术会施放两次。
    机制: AURA
    """
    update = Refresh(FRIENDLY_HAND + FRIENDLY_DECK + SPELL + ARCANE, {
        GameTag.SPELL_DOUBLE_CAST: True
    })


class RLK_542:
    """奥能散射机 (Arcsplitter)
    亡语：将2张奥术箭置入你的手牌。
    机制: DEATHRATTLE
    """
    deathrattle = Give(CONTROLLER, "RLK_843") * 2


class RLK_543:
    """魔导师学徒 (Magister's Apprentice)
    你的奥术法术的法力值消耗减少（1）点。
    机制: AURA
    """
    update = Refresh(FRIENDLY_HAND + SPELL + ARCANE, {
        GameTag.COST: -1
    })


class RLK_544:
    """奥术防御者 (Arcane Defenders)
    召唤两个5/6并具有嘲讽和扰魔的魔像。
    """
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_544t") * 2


class RLK_544t:
    """奥术魔像 (Arcane Golem)
    5/6 嘲讽，扰魔
    """
    # Token 卡牌，属性在 CardDefs.xml 中定义
    pass


class RLK_545:
    """能量塑形师 (Energy Shaper)
    战吼：将你手牌中的所有法术牌变形成为法力值消耗增加（3）点的法术牌。（保留其原始法力值消耗。）
    机制: BATTLECRY
    """
    def play(self):
        # 将手牌中所有法术牌变形为费用+3的版本
        for card in list(self.controller.hand):
            if card.type == CardType.SPELL and card != self:
                # 发现一张费用为原费用+3的法术牌
                new_cost = card.cost + 3
                discovered = yield GenericChoice(CONTROLLER, RandomSpell(cost=new_cost) * 3)
                if discovered:
                    # 移除原卡牌并给予新卡牌
                    card.destroy()
                    yield Give(CONTROLLER, discovered)


class RLK_546:
    """广阔智慧 (Vast Wisdom)
    发现两张法力值消耗小于或等于（3）点的法术牌。交换其法力值消耗。
    """
    def play(self):
        # 第一步：发现一张费用<=3的法术牌
        first_spell = yield GenericChoice(CONTROLLER, RandomSpell(cost_max=3) * 3)
        if not first_spell:
            return

        # 第二步：发现另一张费用<=3的法术牌
        second_spell = yield GenericChoice(CONTROLLER, RandomSpell(cost_max=3) * 3)
        if not second_spell:
            return

        # 交换两张法术的费用
        first_cost = first_spell.cost
        second_cost = second_spell.cost

        # 给予两张法术牌并交换费用
        first_card = yield Give(CONTROLLER, Copy(first_spell))
        second_card = yield Give(CONTROLLER, Copy(second_spell))

        if first_card and second_card:
            # 使用 Buff action 而不是直接调用方法
            yield Buff(first_card, "RLK_546e", cost=second_cost - first_cost)
            yield Buff(second_card, "RLK_546e", cost=first_cost - second_cost)


class RLK_546e:
    """费用交换 (Cost Swap)"""
    def apply(self, target):
        # Buff 会自动应用 cost 参数
        pass


class RLK_547:
    """棱光元素 (Prismatic Elemental)
    战吼：发现一张任意职业的法术牌，其法力值消耗减少（1）点。
    机制: BATTLECRY, DISCOVER
    """
    def play(self):
        # 发现一张任意职业的法术牌
        discovered = yield GenericChoice(CONTROLLER, RandomSpell() * 3)
        if discovered:
            # 给予法术牌并减少1费
            card = yield Give(CONTROLLER, Copy(discovered))
            if card:
                # 使用 Buff action 而不是直接调用方法
                yield Buff(card, "RLK_547e")


class RLK_547e:
    """棱光增益 (Prismatic Buff)
    法力值消耗减少（1）点
    """
    tags = {GameTag.COST: -1}


class RLK_548:
    """奥术浮龙 (Arcane Wyrm)
    战吼：将一张奥术箭置入你的手牌。
    机制: BATTLECRY
    """
    play = Give(CONTROLLER, "RLK_843")


class RLK_803:
    """大法师罗曼斯 (Grand Magister Rommath)
    战吼：再次施放你在本局对战中施放的每个套牌之外的法术。
    机制: BATTLECRY
    """
    def play(self):
        # 获取本局对战中施放的所有套牌之外的法术
        spells_to_cast = list(self.controller.spells_cast_not_from_deck)

        # 再次施放这些法术
        for spell_id in spells_to_cast:
            yield CastSpell(spell_id)


class RLK_843:
    """奥术箭 (Arcane Bolt)
    造成$2点伤害。法力渴求（8）：改为造成$3点伤害。
    机制: MANATHIRST
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self, target):
        # 基础伤害2点，法力渴求（8）改为3点
        damage = 3 if self.controller.max_mana >= 8 else 2
        yield Hit(target, damage)


