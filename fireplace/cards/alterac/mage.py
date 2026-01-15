# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 法师
"""

from ..utils import *


class AV_114:
    """颤抖的女术士 / Shivering Sorceress
    战吼：使你手牌中法力值消耗最高的法术的法力值消耗减少（1）点。"""
    def play(self):
        """减少手牌中最高费用法术的费用"""
        spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        if spells:
            # 找到费用最高的法术
            highest_cost_spell = max(spells, key=lambda c: c.cost)
            yield Buff(highest_cost_spell, "AV_114e")


class AV_114e:
    """颤抖的女术士效果 - 减1费"""
    # 使用参数 i 代表当前的 cost 值，避免无限递归
    tags = {
        GameTag.COST: lambda self, i: max(0, i - 1)
    }


class AV_115:
    """增幅雪暴 / Amplified Snowflurry
    战吼：你的下一个英雄技能的法力值消耗为（0）点，并冻结目标。"""
    play = Buff(CONTROLLER, "AV_115e")


class AV_115e:
    """增幅雪暴效果 - 英雄技能免费并冻结"""
    # 下一个英雄技能免费
    update = Refresh(FRIENDLY_HERO_POWER, {
        GameTag.COST: 0
    })
    # 使用英雄技能后冻结目标并移除buff
    events = [
        Inspire(CONTROLLER).on(
            Freeze(Inspire.TARGET) if Inspire.TARGET else None
        ),
        Inspire(CONTROLLER).after(Destroy(SELF))
    ]


class AV_116:
    """奥术光辉 / Arcane Brilliance
    将你牌库中一张法力值消耗为7、8、9和10点的法术的复制置入你的手牌。"""
    def play(self):
        """复制牌库中7、8、9、10费的法术"""
        for cost in [7, 8, 9, 10]:
            spells = [c for c in self.controller.deck
                     if c.type == CardType.SPELL and c.cost == cost]
            if spells:
                spell = self.game.random.choice(spells)
                yield Give(CONTROLLER, Copy(spell))


class AV_200:
    """执政官晨曦 / Magister Dawngrasp
    战吼：重新施放你在本局对战中施放过的每个法术学派的一个法术。"""
    def play(self):
        """重新施放每个法术学派的一个法术"""
        # 获取已施放过的法术学派
        if not hasattr(self.controller, 'spell_schools_played_this_game'):
            return

        schools = self.controller.spell_schools_played_this_game

        # 为每个学派重新施放一个法术
        for school in schools:
            # 查找该学派的法术（从墓地）
            spells = [c for c in self.controller.graveyard
                     if c.type == CardType.SPELL and
                     hasattr(c, 'spell_school') and c.spell_school == school]
            if spells:
                spell = self.game.random.choice(spells)
                yield CastSpell(Copy(spell))


class AV_212:
    """虹吸法力 / Siphon Mana
    使一个敌方随从的法力值消耗增加（2）点。"""
    play = Buff(TARGET, "AV_212e")


class AV_212e:
    """虹吸法力效果 - 增加2费"""
    # 使用参数 i 代表当前的 cost 值，避免无限递归
    tags = {
        GameTag.COST: lambda self, i: i + 2
    }


class AV_218:
    """群体变形术 / Mass Polymorph
    将所有敌方随从变形成为1/1的绵羊。"""
    play = Morph(ENEMY_MINIONS, "CS2_tk1")


class AV_282:
    """堆雪人 / Build a Snowman
    召唤两个2/3的雪人。冻结两个随机敌方随从。"""
    play = (
        Summon(CONTROLLER, "AV_282t") * 2,
        Freeze(RANDOM_ENEMY_MINION) * 2
    )


class AV_282t:
    """雪人 / Snowman
    2/3 元素"""
    # 在 CardDefs.xml 中定义


class AV_283:
    """大法师符文 / Rune of the Archmage
    施放10个随机法术（目标随机选择）。"""
    def play(self):
        """施放10个随机法术"""
        for _ in range(10):
            # 从所有可收集法术中随机选择
            yield CastSpell(RandomSpell())


class AV_284:
    """巴琳达·石炉 / Balinda Stonehearth
    战吼：如果你的手牌中有法术，使你牌库中的随从获得法术伤害。"""
    def play(self):
        """使牌库中的随从获得法术伤害"""
        # 检查手牌中是否有法术
        spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        if not spells:
            return

        # 计算法术伤害总和
        total_spell_damage = sum(c.spell_damage for c in spells if hasattr(c, 'spell_damage'))

        # 给牌库中的所有随从增加攻击力和生命值
        for minion in self.controller.deck:
            if minion.type == CardType.MINION:
                yield Buff(minion, "AV_284e", atk=total_spell_damage, health=total_spell_damage)


class AV_284e:
    """巴琳达·石炉效果"""
    # 动态增加攻击力和生命值
    # 使用初始化时传入的 atk 和 health 参数
    def __init__(self, atk=0, health=0, **kwargs):
        super().__init__(**kwargs)
        self._buff_atk = atk
        self._buff_health = health
    
    tags = {
        GameTag.ATK: lambda self, i: i + getattr(self, '_buff_atk', 0),
        GameTag.HEALTH: lambda self, i: i + getattr(self, '_buff_health', 0)
    }


class AV_290:
    """冰血塔楼 / Iceblood Tower
    在你的回合结束时，对所有敌方随从造成1点伤害。持续3回合。"""
    # 前地标时代的伪地标设计
    # 使用 PseudoSecret 核心类实现

    # 设置持续时间
    duration = 3

    # 伪奥秘事件：每回合结束时造成伤害
    pseudo_secret = [
        OWN_TURN_END.on(
            Hit(ENEMY_MINIONS, 1)
        ).then(
            lambda self: self.decrement_duration()
        )
    ]


class ONY_006:
    """深呼吸 / Deep Breath
    对所有随从造成1点伤害。如果有任何随从死亡，再次施放此法术。"""
    def play(self):
        """造成伤害并检查是否有随从死亡"""
        while True:
            # 记录当前场上随从数量
            minions_before = len(self.controller.opponent.field) + len(self.controller.field)

            # 对所有随从造成1点伤害
            yield Hit(ALL_MINIONS, 1)

            # 检查是否有随从死亡
            minions_after = len(self.controller.opponent.field) + len(self.controller.field)

            # 如果没有随从死亡，停止循环
            if minions_after >= minions_before:
                break


class ONY_007:
    """哈蕾，守护者族长 / Haleh, Matron Protectorate
    战吼：施放一个法术伤害等于你的法术伤害的奥术飞弹。"""
    def play(self):
        """施放法术伤害次数的奥术飞弹"""
        # 计算法术伤害 - 统计场上所有友方随从的法术伤害
        spell_damage = sum(
            getattr(minion, 'spell_damage', 0) 
            for minion in self.controller.field
        )

        # 施放奥术飞弹（每点法术伤害施放一次）
        for _ in range(spell_damage + 1):  # +1 因为基础伤害是1
            yield Hit(RANDOM_ENEMY_CHARACTER, 1)


class ONY_029:
    """龙火护符 / Drakefire Amulet
    你的下一个英雄技能可以使用三次。"""
    play = Buff(CONTROLLER, "ONY_029e")


class ONY_029e:
    """龙火护符效果 - 英雄技能可使用3次"""
    def apply(self, target):
        """初始化计数器"""
        target.ony_029_uses_remaining = 3

    # 使用英雄技能后递减计数器
    events = Inspire(CONTROLLER).after(
        lambda self, player: (
            setattr(source.controller, 'ony_029_uses_remaining',
                   source.controller.ony_029_uses_remaining - 1)
            if hasattr(source.controller, 'ony_029_uses_remaining') and
               source.controller.ony_029_uses_remaining > 1
            else Destroy(self)
        )
    )





