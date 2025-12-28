from ..utils import *


##
# Hero Powers


class TBA01_5:
    """Wild Magic / 狂野魔法
    随机将一张职业法术卡牌置入你的手牌。它的法力值消耗变为（0）点。"""

    activate = Buff(Give(CONTROLLER, RandomSpell()), "TBA01_5e")


@custom_card
class TBA01_5e:
    tags = {
        GameTag.CARDNAME: "Wild Magic Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    cost = SET(0)
    events = REMOVED_IN_PLAY


class TBA01_6:
    """Molten Rage / 熔岩暴怒
    召唤一个5/1的岩浆暴怒者。"""

    activate = Summon(CONTROLLER, "CS2_118")


##
# Minions


class BRMC_84:
    """Dragonkin Spellcaster / 龙人施法者
    战吼：召唤两条2/2的雏龙。"""

    play = SummonBothSides(CONTROLLER, "BRMA09_2Ht") * 2


class BRMC_85:
    """Lucifron / 鲁西弗隆
    战吼：对所有其他随从施放腐蚀术。"""

    play = Buff(ALL_MINIONS - SELF, "CS2_063e")


class BRMC_86:
    """Atramedes / 艾卓曼德斯
    每当你的对手使用一张牌时，便获得+2攻击力。"""

    events = Play(OPPONENT).on(Buff(SELF, "BRMC_86e"))


BRMC_86e = buff(atk=2)


class BRMC_87:
    """Moira Bronzebeard / 茉艾拉·铜须
    亡语：召唤索瑞森大帝。"""

    deathrattle = Summon(CONTROLLER, "BRM_028")


class BRMC_88:
    """Drakonid Slayer / 龙人杀戮者
    同时对其攻击目标相邻的随从造成伤害。"""

    events = Attack(SELF).on(CLEAVE)


class BRMC_91:
    """Son of the Flame / 烈焰之子
    战吼：造成6点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 6)


class BRMC_92:
    """Coren Direbrew / 科林·烈酒
    总会赢得绝命乱斗的胜利。 战吼：将一张绝命乱斗置入你的手牌。"""

    play = Give(CONTROLLER, "EX1_407")
    tags = {
        enums.ALWAYS_WINS_BRAWLS: True,
    }


class BRMC_95:
    """Golemagg / 古雷曼格
    你的英雄每受到1点伤害，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -DAMAGE(FRIENDLY_HERO)


class BRMC_96:
    """High Justice Grimstone / 裁决者格里斯通
    在你的回合开始时，召唤一个传说随从。"""

    events = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))
    )


class BRMC_97:
    """Vaelastrasz / 瓦拉斯塔兹
    你的卡牌法力值消耗减少（3）点。"""

    update = Refresh(FRIENDLY_HAND, {GameTag.COST: -3})


# Burning Adrenaline (Unused)
class BRMC_97e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -2}


class BRMC_98:
    """Razorgore / 拉佐格尔
    在你的回合开始时，使你的所有随从获得+3攻击力。"""

    events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_MINIONS, "BRMC_98e"))


BRMC_98e = buff(atk=3)


class BRMC_99:
    """Garr / 加尔
    每当本随从受到伤害，召唤一个2/3并具有嘲讽的元素。"""

    events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRMC_99e"))


##
# Spells


class BRMC_83:
    """Open the Gates / 打开大门
    用2/2的雏龙填满你的面板。"""

    play = Summon(CONTROLLER, "BRMA09_2Ht") * 7


class BRMC_93:
    """Omnotron Defense System / 全能金刚防御系统
    随机召唤一个金刚。"""

    entourage = ["BRMA14_3", "BRMA14_5", "BRMA14_7", "BRMA14_9"]
    play = Summon(CONTROLLER, RandomEntourage())


class BRMC_95h:
    """Core Hound Puppies"""

    play = Summon(CONTROLLER, "BRMC_95he") * 2


class BRMC_95he:
    events = TURN_END.on(Summon(CONTROLLER, Copy(ID("BRMC_95he") + KILLED_THIS_TURN)))


class BRMC_100:
    """Living Bomb / 活体炸弹
    选择一个敌方随从。在你的下个回合开始时，如果该随从依然存活，则对所有敌人造成$5点伤害。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "BRMC_100e")


class BRMC_100e:
    events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_MINIONS, 5))


##
# Weapons


class BRMC_94:
    """Sulfuras / 萨弗拉斯
    亡语：你的英雄技能变为“随机对一个敌人造成8点伤害”。"""

    deathrattle = Summon(CONTROLLER, "BRM_027p")
