from ..utils import *


##
# Minions


class ICC_034:
    """Arrogant Crusader / 傲慢的十字军
    亡语：如果此时是你对手的回合，则召唤一个2/2的食尸鬼。"""

    deathrattle = (CurrentPlayer(OPPONENT), Summon(CONTROLLER, "ICC_900t"))


class ICC_245:
    """Blackguard / 黑色卫士
    每当你的英雄获得治疗时，便随机对一个敌方随从造成等量的 伤害。"""

    events = Heal(FRIENDLY_HERO).on(Hit(RANDOM_ENEMY_MINION, Heal.AMOUNT))


class ICC_801:
    """Howling Commander / 咆哮的指挥官
    战吼：从你的牌库中抽一张具有圣盾的随从牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + DIVINE_SHIELD))


class ICC_858:
    """Bolvar, Fireblood / 浴火者伯瓦尔
    圣盾 在一个友方随从失去圣盾后，获得+2攻击力。"""

    events = LosesDivineShield(FRIENDLY_MINIONS).after(Buff(SELF, "ICC_858e"))


ICC_858e = buff(atk=2)


##
# Spells


class ICC_039:
    """Dark Conviction / 黑暗裁决
    将一个随从的攻击力和生命值 变为3。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "ICC_039e")


class ICC_039e:
    atk = SET(3)
    max_health = SET(3)


class ICC_244:
    """Desperate Stand / 殊死一搏
    使一个随从获得“亡语：回到战场，并具有1点生命值。”"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_244e")


class ICC_244e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, Copy(OWNER)).then(SetCurrentHealth(Summon.CARD, 1))


##
# Weapons


class ICC_071:
    """Light's Sorrow / 光之悲恸
    在一个友方随从失去圣盾后，获得+1攻击力。"""

    events = LosesDivineShield(FRIENDLY_MINIONS).after(Buff(SELF, "ICC_071e"))


ICC_071e = buff(atk=1)


##
# Heros


class ICC_829:
    """Uther of the Ebon Blade / 黑锋骑士乌瑟尔
    战吼： 装备一把5/3并具有吸血的武器。"""

    play = Summon(CONTROLLER, "ICC_829t")


class ICC_829p:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = ["ICC_829t2", "ICC_829t3", "ICC_829t4", "ICC_829t5"]
    activate = Summon(CONTROLLER, RandomEntourage(exclude=FRIENDLY_MINIONS))
    update = FindAll(
        FRIENDLY_MINIONS + ID("ICC_829t2"),
        FRIENDLY_MINIONS + ID("ICC_829t3"),
        FRIENDLY_MINIONS + ID("ICC_829t4"),
        FRIENDLY_MINIONS + ID("ICC_829t5"),
    ) & Destroy(ENEMY_HERO)
