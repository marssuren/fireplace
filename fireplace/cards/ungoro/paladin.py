from ..utils import *


##
# Minions


class UNG_011:
    """Hydrologist / 水文学家
    战吼：发现并施放一个奥秘。"""

    play = WITH_SECRECTS & (DISCOVER(RandomSpell(secret=True))) | (
        DISCOVER(RandomSpell(secret=True, card_class=CardClass.PALADIN))
    )


class UNG_015:
    """Sunkeeper Tarim / 守日者塔林姆
    嘲讽，战吼：将所有其他随从的攻击力和生命值变为3。"""

    play = Buff(ALL_MINIONS - SELF, "UNG_015e")


class UNG_015e:
    atk = SET(3)
    max_health = SET(3)


class UNG_953:
    """Primalfin Champion / 蛮鱼勇士
    亡语：将你施放在本随从身上的所有法术移回你的手牌。"""

    events = Play(CONTROLLER, SPELL, SELF).on(StoringBuff(SELF, "UNG_953e", Play.CARD))


class UNG_953e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, Copy(STORE_CARD))


class UNG_962:
    """Lightfused Stegodon / 光注剑龙
    战吼：进化你的白银之手新兵。"""

    play = Adapt(FRIENDLY_MINIONS + ID("CS2_101t"))


##
# Spells


class UNG_004:
    """Dinosize / 巨化术
    将一个随从的属性值变为7/14。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "UNG_004e")


class UNG_004e:
    atk = SET(10)
    max_health = SET(10)


class UNG_952:
    """Spikeridged Steed / 剑龙骑术
    使一个随从获得+2/+6和嘲讽。当该随从死亡时，召唤一只剑龙。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "UNG_952e")


class UNG_952e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 6,
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
    }

    deathrattle = Summon(CONTROLLER, "UNG_810")


class UNG_954:
    """The Last Kaleidosaur / 最后的水晶龙
    任务：对你的随从施放5个法术。 奖励：嘉沃顿。"""

    progress_total = 6
    quest = Play(CONTROLLER, SPELL, FRIENDLY_MINIONS).after(
        AddProgress(SELF, Play.CARD)
    )
    reward = Give(CONTROLLER, "UNG_954t1")


class UNG_954t1:
    play = Adapt(SELF) * 5


class UNG_960:
    """Lost in the Jungle / 迷失丛林
    召唤两个1/1的白银之手新兵。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "CS2_101t") * 2


class UNG_961:
    """Adaptation / 适者生存
    进化一个友方随从。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Adapt(TARGET)


##
# Weapons


class UNG_950:
    """Vinecleaver / 斩棘刀
    在你的英雄攻击后，召唤两个1/1的白银之手 新兵。"""

    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "CS2_101t") * 2)
