from ..utils import *


##
# Minions


class AT_070:
    """Skycap'n Kragg / 天空上尉库拉格
    冲冲冲冲锋 每有一个友方海盗，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Count(FRIENDLY_MINIONS + PIRATE)


class AT_122:
    """Gormok the Impaler / 穿刺者戈莫克
    战吼：如果你拥有至少四个其他随从，则造成4点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS: 4}
    play = (Count(FRIENDLY_MINIONS) >= 4) & Hit(TARGET, 4)


class AT_123:
    """Chillmaw / 冰喉
    嘲讽，亡语： 如果你的手牌中有龙牌，则对所有随从造成3点伤害。"""

    deathrattle = HOLDING_DRAGON & Hit(ALL_MINIONS, 3)


class AT_124:
    """Bolf Ramshield / 博尔夫·碎盾
    每当你的英雄受到伤害，改为由本随从承担。"""

    events = Predamage(FRIENDLY_HERO).on(
        Predamage(FRIENDLY_HERO, 0), Hit(SELF, Predamage.AMOUNT)
    )


class AT_125:
    """Icehowl / 冰吼
    冲锋 无法攻击英雄。"""

    tags = {GameTag.CANNOT_ATTACK_HEROES: True}


class AT_127:
    """Nexus-Champion Saraad / 虚灵勇士萨兰德
    激励：随机将一张法术牌置入你的手牌。"""

    inspire = Give(CONTROLLER, RandomSpell())


class AT_128:
    """The Skeleton Knight / 骷髅骑士
    亡语：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，则将骷髅骑士移回你的手牌。"""

    deathrattle = JOUST & Bounce(SELF)


class AT_129:
    """Fjola Lightbane / 光明邪使菲奥拉
    每当你以本随从为目标施放一个法术时，获得圣盾。"""

    events = Play(CONTROLLER, SPELL, SELF).on(GiveDivineShield(SELF))


class AT_131:
    """Eydis Darkbane / 黑暗邪使艾蒂丝
    每当你以本随从为目标施放一个法术时，随机对一个敌人造成3点伤害。"""

    events = Play(CONTROLLER, SPELL, SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class AT_132:
    """Justicar Trueheart / 裁决者图哈特
    战吼：以更强的英雄技能来替换你的初始英雄技能。"""

    play = UPGRADE_HERO_POWER
