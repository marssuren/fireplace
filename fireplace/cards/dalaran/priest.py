from ..utils import *


##
# Minions


class DAL_030:
    """Shadowy Figure / 阴暗的人影
    战吼： 变形成为一个友方亡语随从的2/2复制。"""

    # <b>Battlecry:</b> Transform into a_2/2 copy of a friendly <b>Deathrattle</b> minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Morph(SELF, ExactCopy(TARGET)).then(Buff(Morph.CARD, "DAL_030e"))


class DAL_030e:
    atk = SET(2)
    max_health = SET(2)


class DAL_039:
    """Convincing Infiltrator / 无面渗透者
    嘲讽 亡语：随机消灭一个敌方随从。"""

    # [x]<b><b>Taunt</b></b> <b>Deathrattle:</b> Destroy a random enemy minion.
    deathrattle = Destroy(RANDOM(ENEMY_MINIONS))


class DAL_040:
    """Hench-Clan Shadequill / 荆棘帮箭猪
    亡语：为敌方英雄恢复5点生命值。"""

    # <b>Deathrattle:</b> Restore 5 Health to the enemy hero.
    deathrattle = Heal(ENEMY_HERO, 5)


class DAL_413:
    """EVIL Conscripter / 怪盗征募员
    亡语：将一张跟班牌置入你的手牌。"""

    # <b>Deathrattle:</b> Add a <b>Lackey</b> to your hand.
    deathrattle = Give(CONTROLLER, RandomLackey())


class DAL_721:
    """Catrina Muerte / 亡者卡特琳娜
    在你的回合结束时，复活另一个友方亡灵随从。"""

    # [x]At the end of your turn, summon a friendly minion that died this game.
    events = OWN_TURN_END.on(
        Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))
    )


class DAL_729:
    """Madame Lazul / 拉祖尔女士
    战吼：发现一张你的对手手牌的复制。"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a copy of a card in your opponent's hand.
    play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(ENEMY_HAND)) * 3))


##
# Spells


class DAL_011(SchemeUtils):
    """Lazul's Scheme"""

    # Reduce the Attack of an enemy minion by @ until your next turn. <i>(Upgrades each
    # turn!)</i>
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Buff(TARGET, "DAL_011e") * (Attr(SELF, GameTag.QUEST_PROGRESS) + 1)


class DAL_011e:
    tags = {GameTag.ATK: -1}
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class DAL_065:
    """Unsleeping Soul / 不眠之魂
    沉默一个友方随从，然后召唤一个它的复制。"""

    # <b>Silence</b> a friendly minion, then summon a copy of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Silence(TARGET), Summon(CONTROLLER, ExactCopy(TARGET))


class DAL_723:
    """Forbidden Words / 禁忌咒文
    消耗你所有的法力值。消灭一个攻击力小于或等于所消耗法力值的随从。"""

    # [x]Spend all your Mana. Destroy a minion with that much Attack or less.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_MINION_ATTACK_LESS_OR_EQUAL_MANA: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)), Destroy(TARGET)


class DAL_724:
    """Mass Resurrection / 群体复活
    召唤三个在本局对战中死亡的友方随从。"""

    # Summon 3 friendly minions that died this game.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
    }
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION) * 3))
