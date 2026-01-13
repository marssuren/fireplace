"""
深暗领域 - WARLOCK
"""
from ..utils import *


# COMMON

class GDB_109:
    """军团之心 - Heart of the Legion
    Lifesteal Starship Piece

    2费 3/2 术士随从 - 星舰组件
    <b>吸血</b>
    <b>星舰组件</b>
    """
    tags = {
        GameTag.LIFESTEAL: True,
    }


class GDB_121:
    """恶兆邪火 - Foreboding Flame
    Battlecry: Demons that didn't start in your deck cost (1) less this game.

    2费 2/3 元素
    战吼：在本局对战中，你套牌之外的恶魔的法力值消耗减少（1）点。
    """
    requirements = {}

    def play(self):
        # 为控制者添加光环效果，使套牌外的恶魔减费
        yield Buff(CONTROLLER, "GDB_121e")


class GDB_123:
    """挟持射线 - Abduction Ray
    Get a random Demon. Reduce its Cost by (2). Repeatable this turn.

    2费 暗影法术
    随机获取一张恶魔牌，其法力值消耗减少（2）点。在本回合可以重复使用。

    实现说明：
    - 使用后生成一个 Token 副本（GDB_123t）到手牌
    - Token 在回合结束时自动销毁
    - 参考 LOOT_504 (Unstable Evolution) 的实现模式
    """
    requirements = {}

    def play(self):
        # 随机获取一张恶魔牌
        yield RandomCard(CONTROLLER, race=Race.DEMON)
        # 减少2费 - 对刚获取的恶魔牌
        yield Buff(Find(CONTROLLER_HAND + FRIENDLY + LAST_CARD_PLAYED), "GDB_123e")
        # 生成可重复使用的 Token
        yield Give(CONTROLLER, "GDB_123t")


class SC_019:
    """雷兽窟 - Ultralisk Cavern
    Deal 1 damage to all enemies. Deathrattle: Summon an 8/8 Ultralisk with Rush.

    4费 地标 3耐久
    对所有敌人造成1点伤害。亡语：召唤一只8/8并具有突袭的雷兽。
    """
    requirements = {}

    def activate(self):
        # 地标激活时，对所有敌人造成1点伤害
        yield Hit(ENEMY_CHARACTERS, 1)

    deathrattle = Summon(CONTROLLER, "SC_019t")


class SC_023:
    """脊针爬虫 - Spine Crawler
    Taunt. Can't attack. Has +3 Attack if you control a location.

    2费 1/6 嘲讽
    嘲讽。无法攻击。如果你控制着地标，则拥有+3攻击力。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.CANT_ATTACK: True,
    }

    # 条件攻击力加成
    class Hand:
        """如果控制地标，获得+3攻击力"""
        def apply(self, target):
            # 检查是否控制地标
            if target.controller.locations:
                target.atk += 3

    update = Hand()


# RARE

class GDB_104:
    """邪火推进器 - Felfire Thrusters
    [x]Spellburst: Deal this minion's Attack damage to 2 random enemy minions. Starship Piece

    3费 2/4 术士随从 - 星舰组件
    <b>法术迸发：</b>对2个随机敌方随从各造成等同于本随从攻击力的伤害。
    <b>星舰组件</b>
    """
    # 法术迸发：对2个随机敌方随从各造成等同于本随从攻击力的伤害
    events = Spellburst(CONTROLLER, Hit(RANDOM_ENEMY_MINION * 2, ATK(SELF)))


class GDB_122:
    """狱火邪谋 - Infernal Stratagem
    Give a minion +3/+3. If it's a Demon, your next one costs (2) less.

    3费 邪能法术
    使一个随从获得+3/+3。如果该随从是恶魔，你的下一张恶魔牌法力值消耗减少（2）点。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        # 给予目标+3/+3
        yield Buff(TARGET, "GDB_122e")

        # 如果目标是恶魔，下一张恶魔牌减费
        if TARGET and TARGET.race == Race.DEMON:
            yield Buff(CONTROLLER, "GDB_122e2")


class GDB_124:
    """恶兆 - Bad Omen
    In 2 turns, summon two 6/6 Demons with Taunt. If you're building a Starship, summon them now.

    6费 邪能法术
    2回合后，召唤两个6/6并具有嘲讽的恶魔。如果你正在构筑星舰，改为现在召唤。
    """
    requirements = {}

    def play(self):
        # 检查是否正在构筑星舰
        if self.controller.starship_in_progress:
            # 立即召唤
            yield Summon(CONTROLLER, "GDB_124t") * 2
        else:
            # 2回合后召唤
            # 使用延迟召唤机制
            yield Buff(CONTROLLER, "GDB_124e")


class SC_020:
    """吞噬 - Consume
    Remove 1 Durability from a friendly location to restore #8 Health to your hero.

    1费 法术
    移除一个友方地标的1点耐久度，为你的英雄恢复8点生命值。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_CARDTYPE: CardType.LOCATION,
    }

    def play(self):
        # 移除目标地标的1点耐久度
        if TARGET:
            TARGET.damage += 1
            # 为英雄恢复8点生命值
            yield Heal(FRIENDLY_HERO, 8)


# EPIC

class GDB_125:
    """治疗石 - Healthstone
    Tradeable. Restore all damage your hero has taken this turn.

    0费 邪能法术 可交易
    可交易。恢复你的英雄在本回合中受到的所有伤害。
    """
    requirements = {}

    def play(self):
        # 获取本回合英雄受到的伤害
        damage_taken = getattr(self.controller, 'damage_taken_this_turn', 0)

        if damage_taken > 0:
            # 恢复等量生命值
            yield Heal(FRIENDLY_HERO, damage_taken)


class GDB_126:
    """黑洞 - Black Hole
    Destroy all minions except Demons.

    8费 暗影法术
    消灭所有非恶魔随从。
    """
    requirements = {}

    def play(self):
        # 消灭所有非恶魔随从
        # 使用选择器：所有随从 - 恶魔随从
        yield Destroy(ALL_MINIONS - DEMON)


# LEGENDARY

class GDB_127:
    """卡拉，黑暗之星 - K'ara, the Dark Star
    Spellburst: Steal 2 Health from a random enemy. (Shadow spells don't remove this Spellburst.)

    3费 3/3 传奇随从
    法术迸发：随机从一个敌人处偷取2点生命值。（暗影法术不会移除此法术迸发。）
    """
    requirements = {}

    # 特殊的法术迸发：暗影法术不会移除
    # 需要自定义事件监听
    events = [
        OWN_SPELL_PLAY.on(lambda self, card: self._trigger_spellburst(source))
    ]

    def _trigger_spellburst(self, spell):
        """触发法术迸发效果"""
        # 随机选择一个敌人
        target = self.game.random.choice(self.controller.opponent.characters)
        if target:
            # 偷取2点生命值（造成伤害并治疗自己）
            yield Hit(target, 2)
            yield Heal(FRIENDLY_HERO, 2)

        # 如果不是暗影法术，移除法术迸发
        if spell.spell_school != SpellSchool.SHADOW:
            # 移除法术迸发标记
            self.spellburst_active = False


class GDB_128:
    """阿克蒙德 - Archimonde
    Battlecry: Summon every Demon you played this game that didn't start in your deck.

    7费 7/7 恶魔 传奇
    战吼：召唤你在本局对战中使用过的你套牌之外的所有恶魔。
    """
    requirements = {}

    def play(self):
        # 获取本局对战中使用过的套牌外恶魔
        # 需要从 Player 对象中追踪的列表获取
        demons_played = getattr(self.controller, 'demons_not_started_in_deck_played', [])

        # 召唤所有这些恶魔
        for demon_id in demons_played:
            yield Summon(CONTROLLER, demon_id)


