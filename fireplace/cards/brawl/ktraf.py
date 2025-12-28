"""
An Evil Exchange
"""

from ..utils import *


class TB_KTRAF_HP_KT_3:
    """Necromancy / 亡灵巫术
    随机将一张“纳克萨玛斯”的随从牌置入你的手牌。"""

    activate = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))


class TB_KTRAF_1:
    """Anub'Rekhan / 阿努布雷坎
    在你的回合结束时，召唤一个3/1的蛛魔。"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "NAX1_03"))


class TB_KTRAF_2:
    """Lady Blaumeux / 女公爵布劳缪克丝
    战吼：召唤一个禁卫骑兵。"""

    play = Summon(CONTROLLER, "TB_KTRAF_2s")


class TB_KTRAF_2s:
    """Sir Zeliek"""

    update = Refresh(ALL_MINIONS + ID("TB_KTRAF_2"), {GameTag.CANT_BE_DAMAGED: True})


class TB_KTRAF_3:
    """Gluth / 格拉斯
    在你的回合结束时，随机召唤一个亡灵。"""

    entourage = [
        "FP1_001",
        "AT_030",
        "LOE_019",
        "EX1_012",
        "EX1_059",
        "FP1_004",
        "EX1_616",
        "FP1_024",
        "tt_004",
    ]
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage()))


class TB_KTRAF_4:
    """Gothik the Harvester / 收割者戈提克
    亡语：为你的对手召唤一个鬼灵戈提克。"""

    deathrattle = Summon(OPPONENT, "TB_KTRAF_4m")


class TB_KTRAF_4m:
    events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 4))


class TB_KTRAF_5:
    """Grand Widow Faerlina / 黑女巫法琳娜
    你的对手 每有一张手牌，拥有+1攻击力。"""

    update = Refresh(SELF, {GameTag.ATK: lambda self, i: self.health})


class TB_KTRAF_6:
    """Grobbulus / 格罗布鲁斯
    每当格罗布鲁斯消灭一个随从，便召唤一个2/2并具有剧毒的辐射泥浆怪。"""

    events = Death(ENEMY + MINION, source=SELF).on(Summon(CONTROLLER, "TB_KTRAF_6m"))


class TB_KTRAF_7:
    """Heigan the Unclean / 肮脏的希尔盖
    在你的回合结束时，随机对一个敌人造成4点伤害。"""

    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 4))


class TB_KTRAF_8:
    """Instructor Razuvious / 教官拉苏维奥斯
    战吼：装备一把5/2的符文巨剑。"""

    play = Summon(CONTROLLER, "TB_KTRAF_08w")


class TB_KTRAF_08w:
    """Massive Runeblade"""

    update = Attacking(FRIENDLY_HERO, HERO) & Refresh(SELF, {GameTag.ATK: +5})


class TB_KTRAF_10:
    """Noth the Plaguebringer / 瘟疫使者诺斯
    每当一个敌方随从死亡，召唤一个1/1的骷髅，并使你的其他随从获得+1/+1。"""

    events = Death(ENEMY + MINION).on(
        Summon(CONTROLLER, "NAX4_03"), Buff(FRIENDLY_MINIONS - SELF, "TB_KTRAF_10e")
    )


TB_KTRAF_10e = buff(+1, +1)


class TB_KTRAF_11:
    """Sapphiron / 萨菲隆
    在你的回合开始时，随机冻结一个 敌方随从。"""

    events = OWN_TURN_BEGIN.on(Freeze(RANDOM_ENEMY_MINION))


class TB_KTRAF_12:
    """Patchwerk / 帕奇维克
    战吼：随机消灭一个敌方随从。"""

    play = Destroy(RANDOM_ENEMY_MINION)


class TB_KTRAF_101:
    """Darkness Calls / 黑暗召唤
    随机召唤两个纳克萨玛斯的首领，并触发其战吼效果。"""

    entourage = [
        "TB_KTRAF_1",
        "TB_KTRAF_3",
        "TB_KTRAF_4",
        "TB_KTRAF_5",
        "TB_KTRAF_6",
        "TB_KTRAF_7",
        "TB_KTRAF_8",
        "TB_KTRAF_2",
        "TB_KTRAF_10",
        "TB_KTRAF_12",
        "TB_KTRAF_11",
    ]
    play = Summon(CONTROLLER, RandomEntourage()).then(Battlecry(Summon.CARD)) * 2


class TB_KTRAF_104:
    """Uncover Staff Piece / 发现法杖组件
    为你的英雄技能添加另一块 组件。"""

    play = Switch(
        FRIENDLY_HERO_POWER,
        {
            "TB_KTRAF_HP_RAF3": Summon(CONTROLLER, "TB_KTRAF_HP_RAF4"),
            "TB_KTRAF_HP_RAF4": Summon(CONTROLLER, "TB_KTRAF_HP_RAF5"),
        },
    )
