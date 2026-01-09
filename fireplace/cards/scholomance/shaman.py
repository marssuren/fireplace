from ..utils import *


##
# Minions

class SCH_236:
    """Diligent Notetaker / 勤奋的记录员
    Spellburst: Return the spell to your hand.
    法术迸发：将该法术返回你的手牌。"""

    # 2费 2/3 法术迸发：将该法术返回你的手牌
    # 完整实现：使用 SPELLBURST_SPELL 选择器获取触发的法术
    spellburst = Give(CONTROLLER, Copy(SPELLBURST_SPELL))


class SCH_507:
    """Instructor Fireheart / 导师炎心
    Battlecry: Discover a spell that costs (1) or more. If you play it this turn, repeat this effect.
    战吼：发现一张法力值消耗大于或等于1的法术牌。如果你在本回合使用它，重复此效果。"""

    # 3费 3/3 传说 战吼：发现一张法力值消耗大于或等于1的法术牌
    # 完整实现：发现法术后添加追踪buff，如果本回合使用则重复效果
    play = (
        Discover(CONTROLLER, RandomSpell(cost=1)),
        Buff(CONTROLLER, "SCH_507_tracker")
    )


class SCH_615:
    """Totem Goliath / 图腾巨像
    Deathrattle: Summon all four basic Totems. Overload: (1)
    亡语：召唤全部四个基础图腾。过载：（1）"""

    # 5费 5/5 亡语：召唤全部四个基础图腾。过载：（1）
    # 四个基础图腾：治疗图腾、灼热图腾、石爪图腾、空气之怒图腾
    deathrattle = (
        Summon(CONTROLLER, "NEW1_009"),  # 治疗图腾
        Summon(CONTROLLER, "NEW1_010"),  # 灼热图腾
        Summon(CONTROLLER, "CS2_052"),   # 石爪图腾
        Summon(CONTROLLER, "CS2_050")     # 空气之怒图腾
    )


##
# Spells

class SCH_271:
    """Molten Blast / 熔岩爆裂
    Deal $2 damage. Summon that many 1/1 Elementals.
    造成2点伤害。召唤等量的1/1元素。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    # 3费 造成2点伤害。召唤等量的1/1元素
    # 完整实现：根据实际造成的伤害召唤元素
    def play(self):
        target = self.target
        # Hit Action 返回实际造成的伤害值
        damage = yield Hit(target, 2)
        # 根据实际伤害召唤元素
        for _ in range(damage):
            yield Summon(self.controller, "SCH_271t")


class SCH_535:
    """Tidal Wave / 潮汐波涛
    Lifesteal Deal $3 damage to all minions.
    吸血 对所有随从造成3点伤害。"""

    # 8费 吸血 对所有随从造成3点伤害
    # 吸血通过 CardDefs.xml 中的 LIFESTEAL 标签定义
    play = Hit(ALL_MINIONS, 3)


##
# Weapons

class SCH_301:
    """Rune Dagger / 符文匕首
    After your hero attacks, gain Spell Damage +1 this turn.
    在你的英雄攻击后，本回合获得法术伤害+1。"""

    # 2费 1/3 武器 在你的英雄攻击后，本回合获得法术伤害+1
    events = Attack(FRIENDLY_HERO).after(Buff(FRIENDLY_HERO, "SCH_301e"))


SCH_301e = buff(spellpower=1)


# 导师炎心追踪buff（用于SCH_507导师炎心）
class SCH_507_tracker:
    """Instructor Fireheart Tracker / 导师炎心追踪器

    追踪发现的法术，如果本回合使用则重复发现效果
    """

    def apply(self, target):
        # 初始化存储：记录发现的法术ID
        if not hasattr(target, 'fireheart_discovered_spell'):
            target.fireheart_discovered_spell = None

    # 监听发现事件和法术使用事件
    events = [
        # 当玩家通过发现获得卡牌时，记录该卡牌
        # 注意：这里使用 Give 事件来捕获发现后加入手牌的法术
        Give(CONTROLLER, SPELL).after(
            Buff(SELF, "SCH_507_store", spell_to_store=Give.CARD)
        ),

        # 当玩家使用法术时，检查是否是记录的法术
        Play(CONTROLLER, SPELL).after(
            Buff(SELF, "SCH_507_check", played_spell=Play.CARD)
        ),

        # 回合结束时清除追踪
        OWN_TURN_END.on(Destroy(SELF))
    ]


# 导师炎心存储buff（用于存储发现的法术）
class SCH_507_store:
    """Store discovered spell for Instructor Fireheart"""

    def apply(self, target):
        # 记录发现的法术ID
        if hasattr(self, 'spell_to_store'):
            target.fireheart_discovered_spell = self.spell_to_store.id


# 导师炎心检查buff（用于检查是否使用了发现的法术）
class SCH_507_check:
    """Check if discovered spell was played"""

    def apply(self, target):
        # 检查使用的法术是否是发现的法术
        if hasattr(self, 'played_spell') and hasattr(target, 'fireheart_discovered_spell'):
            if self.played_spell.id == target.fireheart_discovered_spell:
                # 如果是，重复发现效果
                target.game.queue_actions(target, [
                    Discover(target, RandomSpell(cost=1)),
                    Buff(target, "SCH_507_tracker")
                ])
                # 清除记录
                target.fireheart_discovered_spell = None
