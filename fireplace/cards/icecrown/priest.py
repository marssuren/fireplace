from ..utils import *


##
# Minions


class ICC_210:
    """Shadow Ascendant / 暗影升腾者
    在你的回合结束时，随机使另一个友方随从获得+1/+1。"""

    events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_MINIONS - SELF), "ICC_210e"))


ICC_210e = buff(+1, +1)


class ICC_214:
    """Obsidian Statue / 黑曜石雕像
    嘲讽，吸血 亡语：随机消灭一个敌方随从。"""

    deathrattle = Destroy(RANDOM_ENEMY_MINION)


class ICC_215:
    """Archbishop Benedictus / 大主教本尼迪塔斯
    战吼：复制你对手的牌库，并洗入你的 牌库。"""

    play = Shuffle(CONTROLLER, ExactCopy(ENEMY_DECK))


##
# Spells


class ICC_207:
    """Devour Mind / 吞噬意志
    复制你对手的牌库中的三张牌，并将其置入你的手牌。"""

    play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK) * 3))


class ICC_213:
    """Eternal Servitude / 永恒奴役
    发现一个在本局对战中死亡的友方随从，并召唤该随从。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Choice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 3)
    ).then(Summon(CONTROLLER, Choice.CARD))


class ICC_235:
    """Shadow Essence / 暗影精华
    随机挑选你牌库里的一个随从，召唤一个5/5的复制。"""

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
        Buff(Summon.CARD, "ICC_235e")
    )


class ICC_235e:
    atk = SET(5)
    max_health = SET(5)


class ICC_802:
    """Spirit Lash / 灵魂鞭笞
    吸血 对所有随从造成 $1点伤害。"""

    play = Hit(ALL_MINIONS, 1)


class ICC_849:
    """Embrace Darkness / 黑暗之拥
    选择一个敌方随从。在你的回合开始时，获得该随从的 控制权。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_849e")


class ICC_849e:
    events = OWN_TURN_BEGIN.on(Steal(OWNER), Destroy(SELF))


##
# Heros


class ICC_830:
    """Shadowreaper Anduin / 暗影收割者安度因
    战吼：消灭所有攻击力大于或等于5的随从。"""

    play = Destroy(ALL_MINIONS + (ATK >= 5))


class ICC_830p:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Hit(TARGET, 2)
    events = Play(CONTROLLER).after(RefreshHeroPower(SELF))
