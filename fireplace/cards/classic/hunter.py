from ..utils import *


##
# Minions


class CS2_237:
    """Starving Buzzard / 饥饿的秃鹫
    每当你召唤一个野兽，抽一张牌。"""

    events = Summon(CONTROLLER, BEAST).on(Draw(CONTROLLER))


class DS1_070:
    """Houndmaster / 驯兽师
    战吼：使一个友方野兽获得+2/+2和嘲讽。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    powered_up = Find(FRIENDLY_MINIONS + BEAST)
    play = Buff(TARGET, "DS1_070o")


DS1_070o = buff(+2, +2, taunt=True)


class DS1_175:
    """Timber Wolf / 森林狼
    你的其他野兽拥有+1攻击力。"""

    update = Refresh(FRIENDLY_MINIONS + BEAST - SELF, buff="DS1_175o")


DS1_175o = buff(atk=1)


class DS1_178:
    """Tundra Rhino / 苔原犀牛
    你的野兽拥有冲锋。"""

    update = Refresh(FRIENDLY_MINIONS + BEAST, buff="DS1_178e")


DS1_178e = buff(charge=True)


class EX1_531:
    """Scavenging Hyena / 食腐土狼
    每当一个友方野兽死亡，便获得+2/+1。"""

    events = Death(FRIENDLY + BEAST).on(Buff(SELF, "EX1_531e"))


EX1_531e = buff(+2, +1)


class EX1_534:
    """Savannah Highmane / 长鬃草原狮
    亡语：召唤两只2/2的土狼。"""

    deathrattle = Summon(CONTROLLER, "EX1_534t") * 2


class NEW1_033:
    """Leokk / 雷欧克
    你的其他随从拥有+1攻击力。"""

    update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")


NEW1_033o = buff(atk=1)


##
# Spells


class CS2_084:
    """Hunter's Mark / 猎人印记
    使一个随从的生命值变为1。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_084e")


class CS2_084e:
    max_health = SET(1)


class DS1_183:
    """Multi-Shot / 多重射击
    随机对两个敌方随从造成$3点 伤害。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION * 2, 3)


class DS1_184:
    """Tracking / 追踪术
    从你的牌库中发现一张牌。"""

    play = GenericChoice(CONTROLLER, FRIENDLY_DECK[-3:])


class DS1_185:
    """Arcane Shot / 奥术射击
    造成$2点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2)


class EX1_537:
    """Explosive Shot / 爆炸射击
    对一个随从造成$5点伤害，并对其相邻的随从造成 $2点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 5), Hit(TARGET_ADJACENT, 2)


class EX1_538:
    """Unleash the Hounds / 关门放狗
    战场上每有一个敌方随从，便召唤一个 1/1并具有冲锋的猎犬。"""

    requirements = {
        PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "EX1_538t") * Count(ENEMY_MINIONS)


class EX1_539:
    """Kill Command / 杀戮命令
    造成$3点伤害。如果你控制一个野兽，则改为造成 $5点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    powered_up = Find(FRIENDLY_MINIONS + BEAST)
    play = powered_up & Hit(TARGET, 5) | Hit(TARGET, 3)


class EX1_544:
    """Flare / 照明弹
    所有随从失去潜行，摧毁所有敌方奥秘，抽一张牌。"""

    play = (
        Unstealth(ALL_MINIONS),
        Destroy(ENEMY_SECRETS),
        Draw(CONTROLLER),
    )


class EX1_549:
    """Bestial Wrath / 狂野怒火
    在本回合中，使一只友方野兽获得+2攻击力和免疫。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Buff(TARGET, "EX1_549o")


EX1_549o = buff(atk=2, immune=True)


class EX1_617:
    """Deadly Shot / 致命射击
    随机消灭一个敌方随从。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Destroy(RANDOM_ENEMY_MINION)


class NEW1_031:
    """Animal Companion / 动物伙伴
    随机召唤一个野兽伙伴。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]
    play = Summon(CONTROLLER, RandomEntourage())


##
# Secrets


class EX1_533:
    """Misdirection / 误导
    奥秘：当一个敌人攻击你的英雄时，改为该敌人随机攻击另一个角色。"""

    secret = Attack(ALL_CHARACTERS, FRIENDLY_HERO).on(
        Reveal(SELF),
        Retarget(
            Attack.ATTACKER, RANDOM(ALL_CHARACTERS - FRIENDLY_HERO - Attack.ATTACKER)
        ),
    )


class EX1_554:
    """Snake Trap / 毒蛇陷阱
    奥秘：当你的随从受到攻击时，召唤三条1/1的蛇。"""

    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "EX1_554t") * 3)
    )


class EX1_609:
    """Snipe / 狙击
    奥秘：在你的对手使用一张随从牌后，对该随从造成$6点伤害。"""

    secret = Play(OPPONENT, MINION).after(Reveal(SELF), Hit(Play.CARD, 4))


class EX1_610:
    """Explosive Trap / 爆炸陷阱
    奥秘：当你的英雄受到攻击，对所有敌人造成$2点伤害。"""

    secret = Attack(ENEMY_CHARACTERS, FRIENDLY_HERO).on(
        Reveal(SELF), Hit(ENEMY_CHARACTERS, 2)
    )


class EX1_611:
    """Freezing Trap / 冰冻陷阱
    奥秘：当一个敌方随从攻击时，将其移回拥有者的手牌，并且法力值消耗增加（2）点。"""

    secret = Attack(ENEMY_MINIONS).on(
        Reveal(SELF), Bounce(Attack.ATTACKER), Buff(Attack.ATTACKER, "EX1_611e")
    )


class EX1_611e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: +2}


##
# Weapons


class DS1_188:
    """Gladiator's Longbow / 角斗士的长弓
    你的英雄在攻击时免疫。"""

    update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class EX1_536:
    """Eaglehorn Bow / 鹰角弓
    每当一个友方奥秘被揭示时，便获得+1耐久度。"""

    events = Reveal(FRIENDLY_SECRETS).on(Buff(SELF, "EX1_536e"))


EX1_536e = buff(health=1)
