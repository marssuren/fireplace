from ..utils import *


##
# Minions


class ICC_075:
    """Despicable Dreadlord / 卑鄙的恐惧魔王
    在你的回合结束时，对所有敌方随从造成1点伤害。"""

    events = OWN_TURN_END.on(Hit(ENEMY_MINIONS, 1))


class ICC_218:
    """Howlfiend / 咆哮魔
    每当本随从受到伤害，随机弃掉 一张牌。"""

    events = SELF_DAMAGE.on(Discard(RANDOM(FRIENDLY_HAND)))


class ICC_407:
    """Gnomeferatu / 侏儒吸血鬼
    战吼：移除你对手的牌库顶的一张牌。"""

    play = Mill(OPPONENT)


class ICC_841:
    """Blood-Queen Lana'thel / 鲜血女王兰娜瑟尔
    吸血 在本局对战中，你每弃掉一张牌，便拥有+1攻击力。"""

    update = Refresh(SELF, {GameTag.ATK: Count(FRIENDLY + DISCARDED)})


class ICC_903:
    """Sanguine Reveler / 血色狂欢者
    战吼：消灭一个友方随从，并获得+2/+2。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Buff(SELF, "ICC_903t")


ICC_903t = buff(+2, +2)


##
# Spells


class ICC_041:
    """Defile / 亵渎
    对所有随从造成$1点伤害，如果有随从死亡，则再次施放该法术。"""

    def play(self):
        yield Hit(ALL_MINIONS, 1)
        for _ in range(13):
            if Dead(ALL_MINIONS).check(self):
                yield Deaths()
                yield Hit(ALL_MINIONS, 1)
            else:
                break


class ICC_055:
    """Drain Soul / 吸取灵魂
    吸血 对一个随从造成 $3点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2)


class ICC_206:
    """Treachery / 变节
    选择一个友方随从，交给你的 对手。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Steal(TARGET, OPPONENT)


class ICC_469:
    """Unwilling Sacrifice / 强制牺牲
    选择一个友方随从，消灭该随从和一个随机敌方随从。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Destroy(RANDOM_ENEMY_MINION)


##
# Heros


class ICC_831:
    """Bloodreaver Gul'dan / 鲜血掠夺者古尔丹
    战吼：召唤所有在本局对战中死亡的友方恶魔。"""

    play = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + DEMON))


class ICC_831p:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Hit(TARGET, 3)
