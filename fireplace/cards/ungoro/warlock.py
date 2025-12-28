from ..utils import *


##
# Minions


class UNG_047:
    """Ravenous Pterrordax / 饥饿的翼手龙
    战吼： 消灭一个友方随从，并连续进化两次。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Destroy(TARGET), Adapt(SELF) * 2


class UNG_049:
    """Tar Lurker / 焦油潜伏者
    嘲讽 在你对手的回合拥有+3攻击力。"""

    update = CurrentPlayer(OPPONENT) & Refresh(SELF, {GameTag.ATK: +3})


class UNG_830:
    """Cruel Dinomancer / 残暴的恐龙统领
    亡语：随机召唤一个你在本局对战中弃掉的随从。"""

    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY + DISCARDED + MINION))


class UNG_833:
    """Lakkari Felhound / 拉卡利地狱犬
    嘲讽，战吼：弃掉你手牌中法力值消耗最低的两张牌。"""

    play = Discard(RANDOM(FRIENDLY_HAND) * 2)


class UNG_835:
    """Chittering Tunneler / 聒噪的挖掘者
    战吼： 发现一张法术牌。对你的英雄造成等同于其法力值消耗的伤害。"""

    play = Discover(CONTROLLER, RandomSpell()).then(
        Give(CONTROLLER, Discover.CARD), Hit(FRIENDLY_HERO, COST(Discover.CARD))
    )


class UNG_836:
    """Clutchmother Zavas / 萨瓦丝女王
    每当你弃掉这张牌时，使其获得+2/+2，并将其移回你的手牌。"""

    discard = Give(CONTROLLER, SELF), Buff(SELF, "UNG_836e")


UNG_836e = buff(+2, +2)


##
# Spells


class UNG_829:
    """Lakkari Sacrifice / 拉卡利献祭
    任务：弃掉六张牌。 奖励：虚空传送门。"""

    progress_total = 6
    quest = Discard(FRIENDLY).after(AddProgress(SELF, Discard.TARGET))
    reward = Give(CONTROLLER, "UNG_829t1")


class UNG_829t1:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "UNG_829t2")


class UNG_829t2:
    tags = {GameTag.DORMANT: True}
    dormant_events = OWN_TURN_END.on(SummonBothSides(CONTROLLER, "UNG_829t3") * 2)


class UNG_831:
    """Corrupting Mist / 腐化迷雾
    诅咒所有随从，在你的下个回合开始时将其消灭。"""

    play = Buff(ALL_MINIONS, "UNG_831e")


class UNG_831e:
    events = OWN_TURN_BEGIN.on(Destroy(OWNER))


class UNG_832:
    """Bloodbloom / 血色绽放
    在本回合中，你施放的下一个法术不再消耗法力值，转而消耗生命值。"""

    play = Buff(CONTROLLER, "UNG_832e")


class UNG_832e:
    events = OWN_SPELL_PLAY.on(Destroy(SELF))
    update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class UNG_834:
    """Feeding Time / 喂食时间
    对一个随从造成$3点伤害。召唤三只1/1的翼手龙并使其进化。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Summon(CONTROLLER, "UNG_834t1") * 3
