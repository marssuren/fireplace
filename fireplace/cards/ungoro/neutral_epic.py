from ..utils import *


##
# Minions


class UNG_085:
    """Emerald Hive Queen / 翡翠蜂后
    你的随从的法力值消耗增加（2）点。"""

    update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: +2})


class UNG_087:
    """Bittertide Hydra / 苦潮多头蛇
    每当本随从受到伤害，对你的英雄造成 3点伤害。"""

    events = Damage(SELF).on(Hit(FRIENDLY_HERO, 3))


class UNG_088:
    """Tortollan Primalist / 始祖龟预言者
    战吼： 发现一张法术牌，并向随机目标施放。"""

    play = Discover(CONTROLLER, RandomSpell()).then(CastSpell(Discover.CARD))


class UNG_089:
    """Gentle Megasaur / 温顺的巨壳龙
    战吼：进化你所有的鱼人。"""

    play = Adapt(FRIENDLY_MINIONS + MURLOC)


class UNG_099:
    """Charged Devilsaur / 狂奔的魔暴龙
    冲锋，战吼：在本回合中无法攻击英雄。"""

    play = Buff(SELF, "UNG_099e")


@custom_card
class UNG_099e:
    tags = {
        GameTag.CARDNAME: "Can't attack heroes this turn",
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.CANNOT_ATTACK_HEROES: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class UNG_113:
    """Bright-Eyed Scout / 热情的探险家
    战吼：抽一张牌，使其法力值消耗变为（5）点。"""

    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "UNG_113e"))


class UNG_113e:
    cost = SET(5)
    events = REMOVED_IN_PLAY


class UNG_847:
    """Blazecaller / 火焰使者
    战吼：如果你在上个回合使用过元素牌，则造成5点伤害。"""

    requirements = {
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABE_AND_ELEMENTAL_PLAYED_LAST_TURN: 0,
    }
    play = Hit(TARGET, 5)


class UNG_848:
    """Primordial Drake / 始生幼龙
    嘲讽，战吼： 对所有其他随从造成2点伤害。"""

    play = Hit(ALL_MINIONS, 2)


class UNG_946:
    """Gluttonous Ooze / 贪食软泥怪
    战吼：摧毁对手的武器，并获得等同于其攻击力的护甲值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Destroy(ENEMY_WEAPON).then(GainArmor(FRIENDLY_HERO, ATK(Destroy.TARGET)))
