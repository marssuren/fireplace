from ..utils import *


##
# Minions

class SCH_236:
    """Diligent Notetaker / 勤奋的记录员
    Spellburst: Return the spell to your hand.
    法术迸发：将该法术返回你的手牌。"""

    # 2费 2/3 法术迸发：将该法术返回你的手牌
    # TODO: 需要追踪触发Spellburst的法术并返回手牌
    # 目前先留空，等待后续实现
    pass


class SCH_507:
    """Instructor Fireheart / 导师炎心
    Battlecry: Discover a spell that costs (1) or more. If you play it this turn, repeat this effect.
    战吼：发现一张法力值消耗大于或等于1的法术牌。如果你在本回合使用它，重复此效果。"""

    # 3费 3/3 传说 战吼：发现一张法力值消耗大于或等于1的法术牌
    # TODO: 实现"如果你在本回合使用它，重复此效果"的复杂逻辑
    # 目前先实现基础的发现效果
    play = Discover(CONTROLLER, RandomSpell(cost=1))


class SCH_615:
    """Totem Goliath / 图腾巨像
    Deathrattle: Summon all four basic Totems. Overload: (1)
    亡语：召唤全部四个基础图腾。过载：（1）"""

    # 5费 5/5 亡语：召唤全部四个基础图腾。过载：（1）
    # 四个基础图腾：治疗图腾、灼热图腾、石爪图腾、空气之怒图腾
    deathrattle = (
        Summon(CONTROLLER, "NEW1_009") +  # 治疗图腾
        Summon(CONTROLLER, "NEW1_010") +  # 灼热图腾
        Summon(CONTROLLER, "CS2_052") +   # 石爪图腾
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
    # TODO: 需要根据实际造成的伤害召唤元素
    # 目前先实现简单版本：造成2点伤害，召唤2个1/1元素
    play = Hit(TARGET, 2), Summon(CONTROLLER, "SCH_271t") * 2


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

