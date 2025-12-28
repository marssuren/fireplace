from ..utils import *


##
# Minions


class DAL_163:
    """Messenger Raven / 渡鸦信使
    战吼：发现一张法师随从牌。"""

    # <b>Battlecry:</b> <b>Discover</b> a Mage minion.
    play = DISCOVER(RandomMinion(card_class=CardClass.MAGE))


class DAL_182:
    """Magic Dart Frog / 魔法蓝蛙
    在你施放一个法术后，随机对一个敌方随从造成1点伤害。"""

    # After you cast a spell, deal 1 damage to a random enemy minion.
    events = OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1))


class DAL_575:
    """Khadgar / 卡德加
    你的召唤随从的卡牌召唤数量翻倍。"""

    # Your cards that summon minions summon twice_as_many.
    events = Summon(CONTROLLER, MINION, source=FRIENDLY - PLAYER - ID("DAL_575")).after(
        Summon(CONTROLLER, ExactCopy(Summon.CARD))
    )


class DAL_576:
    """Kirin Tor Tricaster / 肯瑞托三修法师
    法术伤害+3 你的法术牌法力值消耗增加（1）点。"""

    # <b>Spell Damage +3</b> Your spells cost (1) more.
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: 1})


class DAL_603:
    """Mana Cyclone / 法力飓风
    战吼：你在本回合中每施放过一个法术，便随机将一张法师法术牌置入你的手牌。"""

    # [x]<b>Battlecry:</b> For each spell you've cast this turn, add a random Mage spell to
    # your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * Count(
        CARDS_PLAYED_THIS_TURN + SPELL
    )


class DAL_609:
    """Kalecgos / 卡雷苟斯
    你每个回合使用的第一张法术牌的法力值消耗为（0）点。战吼：发现一张法术牌。"""

    # Your first spell each turn costs (0). <b>Battlecry:</b> <b>Discover</b> a spell.
    update = (Count(CARDS_PLAYED_THIS_TURN + SPELL) == 0) & Refresh(
        FRIENDLY_HAND + SPELL, buff="DAL_609e"
    )
    play = DISCOVER(RandomSpell())


class DAL_609e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


##
# Spells


class DAL_177:
    """Conjurer's Calling / 咒术师的召唤
    双生法术 消灭一个随从。召唤两个法力值消耗相同的随从来替换它。"""

    # <b>Twinspell</b> Destroy a minion. Summon 2 minions of the same Cost to replace it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Summon(CONTROLLER, RandomMinion(cost=COST(TARGET))) * 2


class DAL_177ts(DAL_177):
    pass


class DAL_577:
    """Ray of Frost / 霜冻射线
    双生法术 冻结一个随从。如果该随从已被冻结，则对其造成$2点伤害。"""

    # <b>Twinspell</b> <b>Freeze</b> a minion. If it's already <b>Frozen</b>, deal $2
    # damage to it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Find(TARGET + FROZEN) & Hit(TARGET, 2) | Freeze(TARGET)


class DAL_577ts(DAL_577):
    pass


class DAL_578:
    """Power of Creation / 创世之力
    发现一张法力值消耗为（6）的随从牌。召唤两个它的 复制。"""

    # <b>Discover</b> a 6-Cost minion. Summon two copies of it.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Discover(CONTROLLER, RandomMinion(cost=6)).then(
        Summon(CONTROLLER, Copy(Discover.CARD)) * 2
    )


class DAL_608:
    """Magic Trick / 魔术戏法
    发现一张法力值消耗小于或等于（3）点的法术牌。"""

    # <b>Discover</b> a spell that costs (3) or less.
    play = DISCOVER(RandomSpell(cost=list(range(0, 4))))
