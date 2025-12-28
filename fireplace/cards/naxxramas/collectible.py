from ..utils import *


##
# Minions


class FP1_001:
    """Zombie Chow / 肉用僵尸
    亡语：为敌方英雄恢复#5点生命值。"""

    deathrattle = Heal(ENEMY_HERO, 5)


class FP1_002:
    """Haunted Creeper / 鬼灵爬行者
    亡语：召唤两只1/1的鬼灵蜘蛛。"""

    deathrattle = Summon(CONTROLLER, "FP1_002t") * 2


class FP1_003:
    """Echoing Ooze / 分裂软泥怪
    战吼： 在回合结束时召唤一个本随从的复制。"""

    play = OWN_TURN_END.on(Summon(CONTROLLER, ExactCopy(SELF)))


class FP1_004:
    """Mad Scientist / 疯狂的科学家
    亡语： 将一个奥秘从你的牌库中置入战场。"""

    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class FP1_005:
    """Shade of Naxxramas / 纳克萨玛斯之影
    潜行。在你的回合开始时，获得+1/+1。"""

    events = OWN_TURN_BEGIN.on(Buff(SELF, "FP1_005e"))


FP1_005e = buff(+1, +1)


class FP1_007:
    """Nerubian Egg / 蛛魔之卵
    亡语：召唤一个4/4的蛛魔。"""

    deathrattle = Summon(CONTROLLER, "FP1_007t")


class FP1_009:
    """Deathlord / 死亡领主
    嘲讽，亡语：你的对手将一个随从从其牌库置入战场。"""

    deathrattle = Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))


class FP1_011:
    """Webspinner / 结网蛛
    亡语：随机获取一张野兽牌。"""

    deathrattle = Give(CONTROLLER, RandomBeast())


class FP1_012:
    """Sludge Belcher / 淤泥喷射者
    嘲讽，亡语：召唤一个1/2并具有嘲讽的泥浆怪。"""

    deathrattle = Summon(CONTROLLER, "FP1_012t")


class FP1_013:
    """Kel'Thuzad / 克尔苏加德
    在每个回合结束时，召唤所有在本回合中死亡的友方随从。"""

    events = TURN_END.on(Summon(CONTROLLER, Copy(FRIENDLY + MINION + KILLED_THIS_TURN)))


class FP1_014:
    """Stalagg / 斯塔拉格
    亡语：如果费尔根也在本局对战中死亡，召唤塔迪乌斯。"""

    deathrattle = Find(KILLED + ID("FP1_015")) & Summon(CONTROLLER, "FP1_014t")


class FP1_015:
    """Feugen / 费尔根
    亡语：如果斯塔拉格也在本局对战中死亡，召唤塔迪乌斯。"""

    deathrattle = Find(KILLED + ID("FP1_014")) & Summon(CONTROLLER, "FP1_014t")


class FP1_016:
    """Wailing Soul / 哀嚎的灵魂
    战吼：沉默你的其他随从。"""

    play = Silence(FRIENDLY_MINIONS)


class FP1_017:
    """Nerub'ar Weblord / 尼鲁巴蛛网领主
    具有战吼的随从法力值消耗增加（2）点。"""

    update = Refresh(IN_HAND + MINION + BATTLECRY, {GameTag.COST: +2})


class FP1_022:
    """Voidcaller / 空灵召唤者
    亡语： 随机将一张恶魔牌从你的手牌置入战场。"""

    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON))


class FP1_023:
    """Dark Cultist / 黑暗教徒
    亡语： 随机使一个友方随从获得+3生命值。"""

    deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "FP1_023e")


FP1_023e = buff(health=3)


class FP1_024:
    """Unstable Ghoul / 蹒跚的食尸鬼
    嘲讽，亡语：对所有随从造成1点伤害。"""

    deathrattle = Hit(ALL_MINIONS, 1)


class FP1_026:
    """Anub'ar Ambusher / 阿努巴尔伏击者
    亡语： 随机将一个友方随从移回你的手牌。"""

    deathrattle = Bounce(RANDOM_FRIENDLY_MINION)


class FP1_027:
    """Stoneskin Gargoyle / 岩肤石像鬼
    在你的回合开始时，为本随从恢复所有生命值。"""

    events = OWN_TURN_BEGIN.on(Heal(SELF, DAMAGE(SELF)))


class FP1_028:
    """Undertaker / 送葬者
    每当你召唤一个具有亡语的随从，便获得+1/+1。"""

    events = Summon(CONTROLLER, MINION + DEATHRATTLE).on(Buff(SELF, "FP1_028e"))


FP1_028e = buff(atk=1)


class FP1_029:
    """Dancing Swords / 舞动之剑
    亡语：你的对手抽一张牌。"""

    deathrattle = Draw(OPPONENT)


class FP1_030:
    """Loatheb / 洛欧塞布
    战吼：下个回合敌方法术的法力值消耗增加（5）点。"""

    play = Buff(OPPONENT, "FP1_030e")


class FP1_030e:
    update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +5})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class FP1_031:
    """Baron Rivendare / 瑞文戴尔男爵
    你的随从的亡语将触发两次。"""

    update = Refresh(CONTROLLER, {GameTag.EXTRA_DEATHRATTLES: True})


##
# Spells


class FP1_019:
    """Poison Seeds / 剧毒之种
    消灭所有随从，并召唤等量的2/2树人代替他们。"""

    def play(self):
        friendly_count = Count(FRIENDLY_MINIONS).evaluate(self)
        enemy_count = Count(ENEMY_MINIONS).evaluate(self)
        yield Destroy(ALL_MINIONS)
        yield Deaths()
        yield Summon(CONTROLLER, "FP1_019t") * friendly_count
        yield Summon(OPPONENT, "FP1_019t") * enemy_count


class FP1_025:
    """Reincarnate / 转生
    消灭一个随从，然后将其复活，并具有所有生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), Deaths(), Summon(CONTROLLER, Copy(TARGET))


##
# Secrets


class FP1_018:
    """Duplicate / 复制
    奥秘：当一个友方随从死亡时，将两张该随从的复制置入你的手牌。"""

    secret = Death(FRIENDLY + MINION).on(
        FULL_HAND | (Reveal(SELF), Give(CONTROLLER, Copy(Death.ENTITY)) * 2)
    )


class FP1_020:
    """Avenge / 复仇
    奥秘：当你的随从死亡时，随机使一个友方随从获得+3/+2。"""

    secret = Death(FRIENDLY + MINION).on(
        (Count(FRIENDLY_MINIONS - TO_BE_DESTROYED) == 0)
        | (Reveal(SELF), Buff(RANDOM(FRIENDLY_MINIONS - TO_BE_DESTROYED), "FP1_020e"))
    )


FP1_020e = buff(+3, +2)


##
# Weapons


class FP1_021:
    """Death's Bite / 死亡之咬
    亡语：对所有随从造成1点伤害。"""

    deathrattle = Hit(ALL_MINIONS, 1)
