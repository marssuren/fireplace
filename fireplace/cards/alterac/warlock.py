# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 术士
"""

from ..utils import *


class AV_277:
    """毁灭之种 / Seeds of Destruction
    将四张"裂隙"洗入你的牌库。抽到裂隙时，召唤一只3/3的恐惧小鬼。"""
    play = Shuffle(CONTROLLER, "AV_277t") * 4


class AV_277t:
    """裂隙 / Rift
    抽到时：召唤一只3/3的恐惧小鬼。"""
    # 抽牌时触发效果
    draw = Summon(CONTROLLER, "AV_277t2")


class AV_277t2:
    """恐惧小鬼 / Dread Imp
    3/3 恶魔"""
    # 在 CardDefs.xml 中定义


class AV_281:
    """邪火爆弹 / Felfire in the Hole!
    抽一张法术牌，对所有敌人造成$2点伤害。如果抽到的是邪能法术牌，则额外造成$1点。"""
    def play(self):
        """抽法术牌并造成伤害"""
        # 抽一张法术牌
        spells = self.controller.deck.filter(type=CardType.SPELL)
        if spells:
            drawn_card = self.game.random.choice(spells)
            yield Draw(CONTROLLER, drawn_card)

            # 基础伤害2点
            yield Hit(ALL_ENEMIES, 2)

            # 如果是邪能法术，额外造成1点伤害
            if drawn_card.spell_school == SpellSchool.FEL:
                yield Hit(ALL_ENEMIES, 1)


class AV_285:
    """邪能狂潮 / Full-Blown Evil
    造成$5点伤害，随机分配到所有敌方随从身上。在本回合可重复使用。"""
    play = Hit(RANDOM_ENEMY_MINION * 5, 1), Give(CONTROLLER, "AV_285t")


class AV_285t:
    """邪能狂潮（可重复） / Full-Blown Evil (Repeatable)
    造成$5点伤害，随机分配到所有敌方随从身上。在本回合可重复使用。"""
    play = Hit(RANDOM_ENEMY_MINION * 5, 1), Give(CONTROLLER, "AV_285t")
    events = OwnTurnEnds(CONTROLLER).on(Destroy(SELF))


class AV_286:
    """邪行者 / Felwalker
    嘲讽。战吼：从你的手牌中施放法力值消耗最高的邪能法术。"""
    def play(self):
        """施放手牌中费用最高的邪能法术"""
        fel_spells = [c for c in self.controller.hand
                      if c.type == CardType.SPELL and c.spell_school == SpellSchool.FEL]

        if fel_spells:
            # 找到费用最高的邪能法术
            highest_cost_spell = max(fel_spells, key=lambda c: c.cost)
            # 施放该法术
            yield CastSpell(highest_cost_spell)


class AV_308:
    """墓地污染者 / Grave Defiler
    战吼：复制你手牌中的一张邪能法术牌。"""
    def play(self):
        """复制手牌中的邪能法术"""
        fel_spells = [c for c in self.controller.hand
                      if c.type == CardType.SPELL and c.spell_school == SpellSchool.FEL]

        if fel_spells:
            # 随机选择一张邪能法术
            spell_to_copy = self.game.random.choice(fel_spells)
            # 复制到手牌
            yield Give(CONTROLLER, Copy(spell_to_copy))


class AV_312:
    """祭祀召唤师 / Sacrificial Summoner
    战吼：消灭一个友方随从。从你的牌库中召唤一个法力值消耗多(1)点的随从。"""
    play = (
        Destroy(TARGET) &
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == Cost(TARGET) + 1)))
    )


class AV_313:
    """空洞的憎恶 / Hollow Abomination
    战吼：对所有敌方随从造成1点伤害。荣誉消灭：获得该随从的攻击力。"""
    play = Hit(ENEMY_MINIONS, 1)
    honorable_kill = Buff(SELF, "AV_313e", atk=ATK(KILLED))


class AV_313e:
    """空洞的憎恶增益"""
    # 动态攻击力增益
    tags = {GameTag.ATK: lambda self, i: self.atk}


class AV_316:
    """恐惧巫妖塔姆辛 / Dreadlich Tamsin
    战吼：对所有随从造成3点伤害。将3张"裂隙"洗入你的牌库。抽3张牌。"""
    play = (
        Hit(ALL_MINIONS, 3) &
        Shuffle(CONTROLLER, "AV_277t") * 3 &
        Draw(CONTROLLER) * 3
    )


class AV_317:
    """塔姆辛的魂匣 / Tamsin's Phylactery
    发现一个在本局对战中死亡的友方亡语随从。使你的随从获得其亡语。"""
    requirements = {
        PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
    }

    def play(self):
        """发现死亡的亡语随从并复制其亡语到所有友方随从"""
        # 使用 GenericChoice 从死亡的亡语随从中选择一个
        choice = yield GenericChoice(
            CONTROLLER,
            RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 3
        )

        if choice:
            # 给所有友方随从添加选中随从的亡语
            for minion in self.controller.field:
                yield CopyDeathrattleBuff(minion, "AV_317e", source=choice)


class AV_657:
    """被亵渎的墓园 / Desecrated Graveyard
    在你的回合结束时，消灭你攻击力最低的随从，召唤一个4/4的阴影魔。持续3回合。"""
    # 前地标时代的伪地标设计
    # 使用 PseudoSecret 核心类实现

    # 设置持续时间
    duration = 3

    # 伪奥秘事件：每回合结束时消灭最低攻击力随从并召唤阴影魔
    # 使用内联 lambda 处理复杂逻辑（查找最低攻击力随从）
    pseudo_secret = [
        OwnTurnEnds(CONTROLLER).on(
            lambda self: [
                # 如果场上有随从，消灭攻击力最低的随从
                Destroy(min(self.controller.field, key=lambda m: m.atk))
            ] if self.controller.field else []
        ).then(
            # 召唤阴影魔
            Summon(CONTROLLER, "AV_657t")
        ).then(
            # 递减持续时间
            lambda self: self.decrement_duration()
        )
    ]


class AV_657t:
    """阴影魔 / Shade
    4/4 恶魔"""
    # 在 CardDefs.xml 中定义


class ONY_033:
    """小鬼侵染 / Impfestation
    每有一个敌方随从，就召唤一只3/3的恐惧小鬼使其攻击对应敌方随从。"""
    def play(self):
        """为每个敌方随从召唤小鬼并攻击"""
        enemy_minions = list(self.game.opponent.field)

        for enemy in enemy_minions:
            # 召唤小鬼
            imp = yield Summon(CONTROLLER, "AV_277t2")
            # 使小鬼攻击对应的敌方随从
            if imp:
                yield Attack(imp, enemy)


class ONY_034:
    """痛苦诅咒 / Curse of Agony
    将三张"痛苦"洗入对手的牌库。抽到痛苦时，受到疲劳伤害。"""
    play = Shuffle(OPPONENT, "ONY_034t") * 3


class ONY_034t:
    """痛苦 / Agony
    抽到时：受到疲劳伤害。"""
    # 抽牌时触发疲劳伤害
    def draw(self):
        """造成等同于疲劳计数器的伤害"""
        # 疲劳伤害 = 当前疲劳计数器 + 1
        fatigue_damage = self.controller.fatigue_counter + 1
        yield Hit(FRIENDLY_HERO, fatigue_damage)
        # 增加疲劳计数器（模拟疲劳效果）
        self.controller.fatigue_counter += 1


class ONY_035:
    """死亡之翼的后裔 / Spawn of Deathwing
    战吼：消灭一个随机敌方随从。弃一张随机手牌。"""
    play = (
        Destroy(RANDOM_ENEMY_MINION) &
        Discard(RANDOM(FRIENDLY_HAND))
    )
