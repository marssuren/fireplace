from ..utils import *


##
# Minions


class ICC_068:
    """Ice Walker / 寒冰行者
    你的英雄技能还会 冻结目标。"""

    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(Freeze(Activate.TARGET))


class ICC_069:
    """Ghastly Conjurer / 鬼影巫师
    战吼：将一张“镜像”法术牌置入你的手牌。"""

    play = Give(CONTROLLER, "CS2_027")


class ICC_083:
    """Doomed Apprentice / 末日学徒
    你对手法术的法力值消耗增加（1）点。"""

    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: 1})


class ICC_252:
    """Coldwraith / 冰冷鬼魂
    战吼：如果有敌人被冻结，抽一张牌。"""

    requirements = {
        PlayReq.REQ_FROZEN_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (Find(ENEMY + FROZEN), Draw(CONTROLLER))


class ICC_838:
    """Sindragosa / 辛达苟萨
    战吼：召唤两个0/1的被冰封的勇士。"""

    play = SummonBothSides(CONTROLLER, "ICC_838t") * 2


class ICC_838t:
    deathrattle = Give(CONTROLLER, RandomLegendaryMinion())


##
# Spells


class ICC_082:
    """Frozen Clone / 寒冰克隆
    奥秘：在你的对手使用一张随从牌后，将两张该随从的复制置入你的手牌。"""

    secret = Play(OPPONENT, MINION).after(
        Reveal(SELF), Give(CONTROLLER, Copy(Play.CARD)) * 2
    )


class ICC_086:
    """Glacial Mysteries / 冰封秘典
    将每种不同的奥秘从你的牌库中置入战场。"""

    requirements = {
        PlayReq.REQ_SECRET_ZONE_CAP_FOR_NON_SECRET: 0,
    }
    play = Summon(CONTROLLER, FRIENDLY_DECK + SECRET)


class ICC_823:
    """Simulacrum / 模拟幻影
    复制你手牌中法力值消耗最低的随从牌。"""

    play = Give(CONTROLLER, ExactCopy(LOWEST_COST(FRIENDLY_HAND)))


class ICC_836:
    """Breath of Sindragosa / 冰龙吐息
    随机对一个敌方随从造成$2点伤害，并使其冻结。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION, 2).then(Freeze(Hit.TARGET))


##
# Heros


class ICC_833:
    """Frost Lich Jaina / 冰霜女巫吉安娜
    战吼：召唤一个3/6的水元素。在本局对战中，你的所有元素拥有吸血。"""

    play = (Summon(CONTROLLER, "ICC_833t"), Buff(CONTROLLER, "ICC_833e"))


class ICC_833h:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Hit(TARGET, 1).then(Dead(TARGET) & Summon(CONTROLLER, "ICC_833t"))


class ICC_833t:
    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class ICC_833e:
    update = Refresh(FRIENDLY_MINIONS + ELEMENTAL, {GameTag.LIFESTEAL: True})
