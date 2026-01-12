from ..utils import *


##
# Minions


class ICC_047:
    """Fatespinner / 命运织网蛛
    秘密亡语： 抉择：对所有随从造成3点伤害；或者使所有随从获得+2/+2。"""

    choose = ("ICC_047a", "ICC_047b")
    player = ChooseBoth(CONTROLLER) & Morph(SELF, "ICC_047t2")


class ICC_047a:
    def play(self):
        morphed = yield Morph(SELF, "ICC_047t")
        if morphed:
            yield SetTags(morphed, {GameTag.SECRET_DEATHRATTLE: 1})


class ICC_047b:
    def play(self):
        morphed = yield Morph(SELF, "ICC_047t")
        if morphed:
            yield SetTags(morphed, {GameTag.SECRET_DEATHRATTLE: 2})


class ICC_047t:
    secret_deathrattles = (Buff(ALL_MINIONS, "ICC_047e"), Hit(ALL_MINIONS, 3))


ICC_047e = buff(+2, +2)


class ICC_047t2:
    deathrattle = Buff(ALL_MINIONS, "ICC_047e"), Hit(ALL_MINIONS, 3)
    play = (ChooseBoth(CONTROLLER), Morph(SELF, "ICC_051t3"))


class ICC_051:
    """Druid of the Swarm / 虫群德鲁伊
    抉择：变形成为1/2并具有剧毒；或者变形成为1/5并具有嘲讽。"""

    choose = ("ICC_051a", "ICC_051b")


class ICC_051a:
    play = Morph(SELF, "ICC_051t")


class ICC_051b:
    play = Morph(SELF, "ICC_051t2")


class ICC_807:
    """Strongshell Scavenger / 硬壳清道夫
    战吼：使你具有嘲讽的随从获得+2/+2。"""

    play = Buff(FRIENDLY_MINIONS + TAUNT, "ICC_807e")


ICC_807e = buff(+2, +2)


class ICC_808:
    """Crypt Lord / 地穴领主
    嘲讽 在你召唤一个随从后，获得+1生命值。"""

    events = Summon(CONTROLLER, TAUNT).after(Buff(SELF, "ICC_808e"))


ICC_808e = buff(health=1)


class ICC_835:
    """Hadronox / 哈多诺克斯
    亡语：召唤所有你在本局对战中死亡的，并具有嘲讽的随从。"""

    deathrattle = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + TAUNT))


##
# Spells


class ICC_050:
    """Webweave / 蛛网
    召唤两只1/2并具有剧毒的 蜘蛛。"""

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "ICC_832t3") * 2


class ICC_054:
    """Spreading Plague / 传播瘟疫
    召唤一只1/5并具有嘲讽的甲虫。如果你的对手拥有的随从更多，则再次施放该法术。"""

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "ICC_832t4").then(
        (Count(FRIENDLY_MINIONS) < Count(ENEMY_MINIONS)) & CastSpell("ICC_054")
    )


class ICC_079:
    """Gnash / 铁齿铜牙
    使你的英雄获得3点护甲值，并在本回合中获得 +3攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    play = GainArmor(FRIENDLY_HERO, 3), Buff(FRIENDLY_HERO, "ICC_079e")


ICC_079e = buff(atk=3)


class ICC_085:
    """Ultimate Infestation / 终极感染
    造成$5点伤害。抽五张牌。获得5点护甲值。召唤一个5/5的食尸鬼。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = (
        Hit(TARGET, 5),
        Draw(CONTROLLER) * 5,
        GainArmor(FRIENDLY_HERO, 5),
        Summon(CONTROLLER, "ICC_085t"),
    )


##
# Heros


class ICC_832:
    """Malfurion the Pestilent / 污染者玛法里奥
    抉择：召唤两只具有剧毒的蜘蛛；或者召唤两只具有嘲讽的甲虫。"""

    choose = ("ICC_832a", "ICC_832b")
    play = ChooseBoth(CONTROLLER) & (
        Summon(CONTROLLER, "ICC_832t4") * 2,
        Summon(CONTROLLER, "ICC_832t3") * 2,
    )


class ICC_832a:
    play = Summon(CONTROLLER, "ICC_832t4") * 2


class ICC_832b:
    play = Summon(CONTROLLER, "ICC_832t3") * 2


class ICC_832p:
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    choose = ("ICC_832pa", "ICC_832pb")
    activate = ChooseBoth(CONTROLLER) & (
        GainArmor(FRIENDLY_HERO, 3),
        Buff(FRIENDLY_HERO, "ICC_832e"),
    )


class ICC_832pa:
    activate = GainArmor(FRIENDLY_HERO, 3)


class ICC_832pb:
    activate = Buff(FRIENDLY_HERO, "ICC_832e")


ICC_832e = buff(atk=3)
