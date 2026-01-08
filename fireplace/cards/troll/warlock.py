from ..utils import *


##
# Minions


class TRL_247:
    """Soulwarden / 护魂者
    战吼：随机将三张你在本局对战中弃掉的牌置入你的手牌。"""

    # <b>Battlecry:</b> Add 3 random cards you discarded this game to your hand.
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY + DISCARDED) * 3))


class TRL_251:
    """Spirit of the Bat / 蝙蝠之灵
    潜行一回合。在一个友方随从死亡后，使你手牌中的一张随从牌获得+1/+1。"""

    # <b>Stealth</b> for 1 turn. After a friendly minion dies, give a minion in your hand
    # +1/+1.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Death(FRIENDLY_MINIONS).on(Buff(RANDOM(FRIENDLY_HAND + MINION), "TRL_251e")),
    )


TRL_251e = buff(+1, +1)


class TRL_252:
    """High Priestess Jeklik / 高阶祭司耶克里克
    嘲讽，吸血 当你弃掉这张牌时，将这张牌的两张复制置入你的手牌。"""

    # [x]<b>Taunt</b>, <b>Lifesteal</b> When you discard this, add 2 copies of it to your
    # hand.
    discard = Give(CONTROLLER, Copy(SELF)) * 2


class TRL_253:
    """Hir'eek, the Bat / 希里克，蝙蝠之神
    战吼：用本随从的复制填满你的面板。"""

    # <b>Battlecry:</b> Fill your board with copies of this minion.
    play = SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 7


class TRL_257:
    """Blood Troll Sapper / 鲜血巨魔工兵
    在一个友方随从 死亡后，对敌方英雄造成2点伤害。"""

    # After a friendly minion dies, deal 2 damage to the enemy hero.
    events = Death(FRIENDLY_MINIONS).on(Hit(ENEMY_HERO, 2))


class TRL_551:
    """Reckless Diretroll / 粗暴的恐怖巨魔
    嘲讽，战吼：弃掉你手牌中法力值消耗最低的牌。"""

    # <b>Taunt</b> <b>Battlecry:</b> Discard your lowest Cost card.
    play = Discard(LOWEST_COST(FRIENDLY_HAND))


##
# Spells


class TRL_245:
    """Shriek / 尖啸
    弃掉你手牌中法力值消耗最低的牌。对所有随从造成$2点 伤害。"""

    # Discard your lowest Cost card. Deal $2 damage to all minions.
    play = (Discard(LOWEST_COST(FRIENDLY_HAND)), Hit(ALL_MINIONS, 2))


class TRL_246:
    """Void Contract / 虚空契约
    摧毁双方牌库中一半的牌。"""

    # Destroy half of each player's deck.
    play = (
        Destroy(RANDOM(FRIENDLY_DECK)) * (Count(FRIENDLY_DECK) / 2),
        Destroy(RANDOM(ENEMY_DECK)) * (Count(ENEMY_DECK) / 2),
    )


class TRL_249:
    """Grim Rally / 残酷集结
    消灭一个友方随从。使你的所有随从获得+1/+1。"""

    # Destroy a friendly minion. Give your minions +1/+1.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET), Buff(FRIENDLY_MINIONS, "TRL_249e")


TRL_249e = buff(+1, +1)


class TRL_555:
    """Demonbolt / 恶魔之箭
    消灭一个随从。你每控制一个随从，本牌的法力值消耗便减少（1）点。"""

    # Destroy a minion. Costs (1) less for each minion you control.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    cost_mod = -Count(FRIENDLY_MINIONS)
    play = Destroy(TARGET)
