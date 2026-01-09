from ..utils import *


##
# Minions


class EX1_398:
    """Arathi Weaponsmith / 阿拉希武器匠
    战吼：装备一把2/2的武器。"""

    play = Summon(CONTROLLER, "EX1_398t")


class EX1_402:
    """Armorsmith / 铸甲师
    每当一个友方随从受到伤害，便获得1点护甲值。"""

    events = Damage(FRIENDLY_MINIONS).on(GainArmor(FRIENDLY_HERO, 1))


class EX1_414:
    """Grommash Hellscream / 格罗玛什·地狱咆哮
    冲锋 受伤时拥有+6攻 击力。"""

    enrage = Refresh(SELF, buff="EX1_414e")


EX1_414e = buff(atk=6)


class EX1_603:
    """Cruel Taskmaster / 严酷的监工
    战吼：对一个随从造成1点伤害，并使其获得+2攻击力。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "EX1_603e"), Hit(TARGET, 1)


EX1_603e = buff(atk=2)


class EX1_604:
    """Frothing Berserker / 暴乱狂战士
    每当一个随从 受到伤害，便获得+1攻击力。"""

    events = Damage(ALL_MINIONS).on(Buff(SELF, "EX1_604o"))


EX1_604o = buff(atk=1)


##
# Spells


class CS2_103:
    """Charge / 冲锋
    使一个友方随从获得+2攻击力和冲锋。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "CS2_103e"), Buff(TARGET, "CS2_103e2")


@custom_card
class CS2_103e:
    tags = {
        GameTag.CARDNAME: "Charge",
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.CANNOT_ATTACK_HEROES: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


CS2_103e2 = buff(charge=True)


class CS2_104:
    """Rampage / 狂暴
    使一个受伤的随从获得+3/+3。"""

    requirements = {
        PlayReq.REQ_DAMAGED_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "CS2_104e")


CS2_104e = buff(+3, +3)


class CS2_105:
    """Heroic Strike / 英勇打击
    在本回合中，使你的英雄获得+4攻击力。"""

    play = Buff(FRIENDLY_HERO, "CS2_105e")


CS2_105e = buff(atk=4)


class CS2_108:
    """Execute / 斩杀
    消灭一个受伤的敌方随从。"""

    requirements = {
        PlayReq.REQ_DAMAGED_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET)


class CS2_114:
    """Cleave / 顺劈斩
    随机对两个敌方随从造成 $2点伤害。"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION * 2, 2)


class EX1_391:
    """Slam / 猛击
    对一个随从造成$2点伤害，如果 它依然存活，则抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), Dead(TARGET) | Draw(CONTROLLER)


class EX1_392:
    """Battle Rage / 战斗怒火
    每有一个受伤的友方角色，便抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0}
    play = Draw(CONTROLLER) * Count(FRIENDLY_CHARACTERS + DAMAGED)


class EX1_400:
    """Whirlwind / 旋风斩
    对所有随从造成$1点伤害。"""

    play = Hit(ALL_MINIONS, 1)


class EX1_407:
    """Brawl / 绝命乱斗
    随机选择一个随从，消灭除了该随从外的所有其他随从。"""

    requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 2}
    # 如果有必胜随从,保留它并消灭其他所有随从,否则随机保留一个
    play = Find(ALL_MINIONS + ALWAYS_WINS_BRAWLS) & Destroy(
        ALL_MINIONS - RANDOM(ALL_MINIONS + ALWAYS_WINS_BRAWLS)
    ) | Destroy(ALL_MINIONS - RANDOM_MINION)


class EX1_408:
    """Mortal Strike / 致死打击
    造成$4点伤害；如果你的生命值小于或等于12点，则改为造成$6点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    powered_up = CURRENT_HEALTH(FRIENDLY_HERO) <= 12
    play = powered_up & Hit(TARGET, 6) | Hit(TARGET, 4)


class EX1_409:
    """Upgrade! / 升级
    如果你装备着武器，使其获得+1/+1。否则装备一把1/3的武器。"""

    # 如果装备着武器,使其获得+1/+1,否则装备一把1/3的武器
    play = Find(FRIENDLY_WEAPON) & Buff(FRIENDLY_WEAPON, "EX1_409e") | Summon(
        CONTROLLER, "EX1_409t"
    )


EX1_409e = buff(+1, +1)


class EX1_410:
    """Shield Slam / 盾牌猛击
    你每有1点护甲值，便对一个随从造成1点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, ARMOR(FRIENDLY_HERO))


class EX1_606:
    """Shield Block / 盾牌格挡
    获得5点护甲值。抽一张牌。"""

    play = GainArmor(FRIENDLY_HERO, 5), Draw(CONTROLLER)


class EX1_607:
    """Inner Rage / 怒火中烧
    对一个随从造成$1点伤害，并使其获得+2攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "EX1_607e"), Hit(TARGET, 1)


EX1_607e = buff(atk=2)


class NEW1_036:
    """Commanding Shout / 命令怒吼
    在本回合中，你的随从的生命值无法被降到1点以下。抽一张牌。"""

    play = Buff(FRIENDLY_MINIONS, "NEW1_036e"), Buff(CONTROLLER, "NEW1_036e2")


class NEW1_036e2:
    events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "NEW1_036e"))


NEW1_036e = buff(health_minimum=1)


class EX1_084:
    """Warsong Commander / 战歌指挥官
    每当你召唤一个攻击力小于或等于3的随从，使其获得冲锋。"""

    update = Refresh(FRIENDLY_MINIONS + CHARGE, buff="EX1_084e")


EX1_084e = buff(atk=1)


##
# Weapons


class EX1_411:
    """Gorehowl / 血吼
    攻击随从不会消耗耐久度，改为降低1点攻击力。"""

    update = Attacking(FRIENDLY_HERO, MINION) & Refresh(SELF, buff="EX1_411e")
    events = Attack(FRIENDLY_HERO, MINION).after(Buff(SELF, "EX1_411e2"))


EX1_411e = buff(immune=True)
EX1_411e2 = buff(atk=-1)
