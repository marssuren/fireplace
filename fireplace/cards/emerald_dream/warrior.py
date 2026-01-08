"""
深入翡翠梦境 - WARRIOR
"""
from ..utils import *
from .dark_gift_helpers import apply_dark_gift, has_dark_gift


# COMMON

class EDR_457:
    """龙巢守护者 - Brood Keeper
    Battlecry: If you're holding a Dragon, equip a 2/2 Sword.

    3费 3/3 随从
    战吼：如果你的手牌中有龙牌，装备一把2/2的剑。
    """
    def play(self):
        # 检查手牌中是否有龙
        has_dragon = any(
            Race.DRAGON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False
            for c in self.controller.hand
        )

        if has_dragon:
            # 装备一把2/2的剑
            yield Equip(CONTROLLER, "EDR_457t")


class EDR_468:
    """捣蛋狂魔 - Eggbasher
    Battlecry: Deal 1 damage to a minion and give it +4 Attack.

    2费 2/3 随从
    战吼：对一个随从造成1点伤害，并使其获得+4攻击力。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        # 造成1点伤害
        yield Hit(TARGET, 1)
        # 给予+4攻击力
        yield Buff(TARGET, "EDR_468e")


class EDR_570:
    """凶险梦魇 - Ominous Nightmares
    [x]Choose One - Deal $1 damage to all minions; or Give a damaged minion +2/+2.

    3费 法术
    抉择：对所有随从造成1点伤害；或者使一个受伤的随从获得+2/+2。
    """
    choose = ["EDR_570a", "EDR_570b"]


class EDR_570a:
    """凶险梦魇（选项1）- Ominous Nightmares (Option 1)
    Deal $1 damage to all minions.

    对所有随从造成1点伤害。
    """
    requirements = {}

    def play(self):
        yield Hit(ALL_MINIONS, 1)


class EDR_570b:
    """凶险梦魇（选项2）- Ominous Nightmares (Option 2)
    Give a damaged minion +2/+2.

    使一个受伤的随从获得+2/+2。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }

    def play(self):
        yield Buff(TARGET, "EDR_570be")


class FIR_939:
    """影焰晕染 - Shadowflame Suffusion
    [x]Deal $2 damage. Discover a Warrior minion with a Dark Gift.

    2费 法术 - 暗影学派
    造成2点伤害。发现一张具有黑暗之赐的战士随从牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)

        # 发现一张战士随从牌
        yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: (
                c.type == CardType.MINION and
                c.card_class == CardClass.WARRIOR
            ),
            count=3
        ))

        # 给予黑暗之赐
        if self.controller.hand:
            discovered_card = self.controller.hand[-1]
            yield apply_dark_gift(discovered_card)


# RARE

class EDR_455:
    """屈从疯狂 - Succumb to Madness
    Discover a friendly Dragon that died this game. Resummon it.

    5费 法术
    发现一条在本局对战中死亡的友方龙。重新召唤它。
    """
    requirements = {}

    def play(self):
        # 获取本局对战中死亡的友方龙
        dead_dragons = [
            c for c in self.controller.graveyard
            if c.type == CardType.MINION and
            Race.DRAGON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False
        ]

        if dead_dragons:
            # 发现一条龙
            import random
            choices = random.sample(dead_dragons, min(3, len(dead_dragons)))
            yield GenericChoice(CONTROLLER, cards=[c.id for c in choices])

            # 重新召唤它
            if self.controller.hand:
                dragon_card = self.controller.hand[-1]
                # 将卡牌从手牌移除并召唤到场上
                yield Summon(CONTROLLER, dragon_card.id)
                yield Destroy(dragon_card)


class EDR_456:
    """黑暗的龙骑士 - Darkrider
    Battlecry: If you're holding a Dragon, Discover a Dragon with a Dark Gift.

    4费 4/4 随从
    战吼：如果你的手牌中有龙牌，发现一张具有黑暗之赐的龙牌。
    """
    def play(self):
        # 检查手牌中是否有龙
        has_dragon = any(
            Race.DRAGON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False
            for c in self.controller.hand
        )

        if has_dragon:
            # 发现一张龙牌
            yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
                CONTROLLER,
                card_filter=lambda c: (
                    c.type == CardType.MINION and
                    Race.DRAGON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False
                ),
                count=3
            ))

            # 给予黑暗之赐
            if self.controller.hand:
                discovered_card = self.controller.hand[-1]
                yield apply_dark_gift(discovered_card)


class EDR_531:
    """虹吸生长 - Siphoning Growth
    Destroy a friendly minion to gain 8 Armor.

    2费 法术 - 自然学派
    消灭一个友方随从，获得8点护甲值。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }

    def play(self):
        # 消灭目标随从
        yield Destroy(TARGET)
        # 获得8点护甲值
        yield GainArmor(FRIENDLY_HERO, 8)


class FIR_928:
    """烈焰守护者 - Keeper of Flame
    [x]Battlecry: Give all minions in your hand +3/+3. They are destroyed in 3 turns.

    6费 5/5 随从
    战吼：使你手牌中的所有随从牌获得+3/+3。它们会在3个回合后被消灭。
    """
    def play(self):
        # 给予手牌中所有随从 +3/+3
        for card in self.controller.hand:
            if card.type == CardType.MINION:
                yield Buff(card, "FIR_928e")


class FIR_956:
    """龙龟 - Dragon Turtle
    [x]Battlecry: If you're holding a minion with a Dark Gift, give your hero +3 Attack this turn and 6 Armor.

    5费 5/7 野兽
    战吼：如果你的手牌中有具有黑暗之赐的随从牌，在本回合中使你的英雄获得+3攻击力并获得6点护甲值。
    """
    def play(self):
        # 检查手牌中是否有具有黑暗之赐的随从
        has_dark_gift_minion = any(
            has_dark_gift(c) and c.type == CardType.MINION
            for c in self.controller.hand
        )

        if has_dark_gift_minion:
            # 给予英雄+3攻击力（本回合）
            yield Buff(FRIENDLY_HERO, "FIR_956e")
            # 获得6点护甲值
            yield GainArmor(FRIENDLY_HERO, 6)


# EPIC

class EDR_454:
    """腐蚀之巢 - Clutch of Corruption
    [x]Choose a friendly Dragon. Summon a 0/2 Egg that hatches into a copy of it.

    3费 法术
    选择一条友方龙。召唤一个0/2的蛋，它会孵化成该龙的一个复制。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DRAGON,
    }

    def play(self):
        # 记录目标龙的ID
        target_dragon_id = TARGET.id

        # 召唤一个0/2的蛋
        yield Summon(CONTROLLER, "EDR_454t")

        # 给蛋添加亡语：孵化成目标龙的复制
        if self.controller.field:
            egg = self.controller.field[-1]
            # 使用buff存储龙的ID
            yield Buff(egg, "EDR_454e", dragon_id=target_dragon_id)


class EDR_459:
    """受难的毁灭者 - Afflicted Devastator
    [x]Battlecry: Deal 3 damage to all other friendly minions. Deathrattle: Deal 3 damage to all enemy minions.

    7费 6/6 随从
    战吼：对所有其他友方随从造成3点伤害。亡语：对所有敌方随从造成3点伤害。
    """
    def play(self):
        # 对所有其他友方随从造成3点伤害
        yield Hit(FRIENDLY_MINIONS - SELF, 3)

    deathrattle = Deathrattle("EDR_459d")


# LEGENDARY

class EDR_465:
    """伊森德雷 - Ysondre
    [x]Taunt. Deathrattle: Summon a random Dragon for each time Ysondre has died this game.

    8费 4/12 龙
    嘲讽。亡语：每当伊森德雷在本局对战中死亡一次，随机召唤一条龙。

    实现说明:
    - 需要追踪伊森德雷在本局对战中死亡的次数
    - 使用 Player 属性存储死亡计数
    - 亡语时根据死亡次数召唤随机龙
    """
    tags = {
        GameTag.TAUNT: True,
    }

    deathrattle = Deathrattle("EDR_465d")


class EDR_471:
    """托尔托拉 - Tortolla
    [x]Taunt, Elusive After this takes damage, gain 1 Armor and give this minion +1 Attack.

    7费 2/10 龙
    嘲讽，扰魔。在该随从受到伤害后，获得1点护甲值并使该随从获得+1攻击力。

    实现说明:
    - 监听受到伤害事件
    - 触发时给予控制者1点护甲值
    - 给予自身+1攻击力
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.ELUSIVE: True,
    }

    # 受到伤害后触发
    events = Damage(SELF).after(
        lambda self: [
            GainArmor(FRIENDLY_HERO, 1),
            Buff(SELF, "EDR_471e")
        ]
    )


# ========================================
# TOKENS (衍生物)
# ========================================

class EDR_457t:
    """龙巢守护者的剑 - Brood Keeper's Sword
    2/2 武器
    """
    pass


class EDR_454t:
    """腐蚀之蛋 - Corrupted Egg
    0/2 随从
    亡语：孵化成一条龙的复制。

    实现说明:
    - 这个Token会通过buff获得亡语效果
    - buff中存储了要孵化的龙的ID
    """
    pass


# ========================================
# BUFFS (增益效果)
# ========================================

class EDR_468e:
    """捣蛋狂魔增益 - Eggbasher Buff
    +4 攻击力
    """
    atk = 4


class EDR_570be:
    """凶险梦魇增益 - Ominous Nightmares Buff
    +2/+2
    """
    atk = 2
    health = 2


class EDR_060e:
    """大地庇护增益 - Ward of Earth Buff
    嘲讽
    """
    tags = {GameTag.TAUNT: True}


class FIR_928e:
    """烈焰守护者增益 - Keeper of Flame Buff
    +3/+3，3回合后被消灭

    实现说明:
    - 给予随从+3/+3
    - 在3个回合后消灭该随从
    - 使用回合计数器追踪
    """
    atk = 3
    health = 3

    # 监听回合开始事件，计数3个回合后消灭（双方回合都计数）
    events = TURN_BEGIN.on(
        lambda self: FIR_928e._check_destroy(self.owner)
    )

    @staticmethod
    def _check_destroy(minion):
        """检查是否需要消灭随从"""
        # 获取buff的回合计数
        if not hasattr(minion, '_fir928_turn_count'):
            minion._fir928_turn_count = 0

        minion._fir928_turn_count += 1

        # 3个回合后消灭
        if minion._fir928_turn_count >= 3:
            return [Destroy(minion)]
        return []


class FIR_956e:
    """龙龟增益 - Dragon Turtle Buff
    本回合+3攻击力
    """
    atk = 3
    # 回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


class EDR_454e:
    """腐蚀之巢增益 - Clutch of Corruption Buff
    给予蛋亡语效果：孵化成指定龙的复制

    实现说明:
    - 这个buff存储了要孵化的龙的ID
    - 亡语时召唤该龙的复制
    - dragon_id 将在运行时通过 kwargs 设置
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # dragon_id 将在运行时通过 kwargs 设置

    @property
    def deathrattle(self):
        """动态生成亡语效果"""
        if hasattr(self, 'dragon_id'):
            dragon_id = self.dragon_id
            return lambda self: [Summon(CONTROLLER, dragon_id)]
        return lambda self: []


class EDR_471e:
    """托尔托拉增益 - Tortolla Buff
    +1 攻击力
    """
    atk = 1


# ========================================
# DEATHRATTLES (亡语效果)
# ========================================

class EDR_459d:
    """受难的毁灭者亡语 - Afflicted Devastator Deathrattle
    对所有敌方随从造成3点伤害
    """
    def deathrattle(self):
        yield Hit(ENEMY_MINIONS, 3)


class EDR_465d:
    """伊森德雷亡语 - Ysondre Deathrattle
    每当伊森德雷在本局对战中死亡一次，随机召唤一条龙

    实现说明:
    - 追踪伊森德雷的死亡次数
    - 使用 Player 属性存储计数
    """
    def deathrattle(self):
        # 初始化或增加死亡计数
        if not hasattr(self.controller, 'ysondre_death_count'):
            self.controller.ysondre_death_count = 0
        self.controller.ysondre_death_count += 1

        # 召唤随机龙
        for _ in range(self.controller.ysondre_death_count):
            yield Summon(CONTROLLER, RandomMinion(race=Race.DRAGON))
