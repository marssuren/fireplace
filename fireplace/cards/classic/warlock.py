from ..utils import *


##
# Minions


class CS2_059:
    """Blood Imp / 鲜血小鬼
    潜行 在你的回合结束时，随机使另一个友方随从获得+1生命值。"""

    events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "CS2_059o"))


CS2_059o = buff(health=1)


class CS2_064:
    """Dread Infernal / 恐惧地狱火
    战吼：对所有其他角色造成1点伤害。"""

    play = Hit(ALL_CHARACTERS - SELF, 1)


class EX1_301:
    """Felguard / 恶魔卫士
    嘲讽，战吼：摧毁你的一个法力水晶。"""

    play = GainEmptyMana(CONTROLLER, -1)


class EX1_304:
    """Void Terror / 虚空恐魔
    战吼：消灭两侧相邻的随从，并获得他们的攻击力和生命值。"""

    play = (
        Buff(
            SELF,
            "EX1_304e",
            atk=ATK(SELF_ADJACENT),
            max_health=CURRENT_HEALTH(SELF_ADJACENT),
        ),
        Destroy(SELF_ADJACENT),
    )


class EX1_306:
    """Felstalker / 魔犬
    战吼： 随机弃一张牌。"""

    play = Discard(RANDOM(FRIENDLY_HAND))


class EX1_310:
    """Doomguard / 末日守卫
    冲锋，战吼：随机弃两张牌。"""

    play = Discard(RANDOM(FRIENDLY_HAND) * 2)


class EX1_313:
    """Pit Lord / 深渊领主
    战吼：对你的英雄造成5点伤害。"""

    play = Hit(FRIENDLY_HERO, 5)


class EX1_315:
    """Summoning Portal / 召唤传送门
    你的随从牌的法力值消耗减少（2）点，但不能少于（1）点。"""

    update = Refresh(
        FRIENDLY_HAND + MINION, {GameTag.COST: lambda self, i: min(i, max(1, i - 2))}
    )


class EX1_319:
    """Flame Imp / 烈焰小鬼
    战吼：对你的英雄造成3点伤害。"""

    play = Hit(FRIENDLY_HERO, 3)


class EX1_323:
    """Lord Jaraxxus / 加拉克苏斯大王
    战吼：装备一把3/8的血怒。"""

    play = (
        Summon(CONTROLLER, "EX1_323h").then(Morph(SELF, Summon.CARD)),
        Summon(CONTROLLER, "EX1_323w"),
    )


class EX1_tk33:
    """INFERNO!"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "EX1_tk34")


##
# Spells


class CS2_061:
    """Drain Life / 吸取生命
    造成$2点伤害，为你的英雄恢复#2点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), Heal(FRIENDLY_HERO, 2)


class CS2_062:
    """Hellfire / 地狱烈焰
    对所有角色造成$3点伤害。"""

    play = Hit(ALL_CHARACTERS, 3)


class CS2_063:
    """Corruption / 腐蚀术
    选择一个敌方随从，在你的回合开始时，消灭该随从。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "CS2_063e")


class CS2_063e:
    events = OWN_TURN_BEGIN.on(Destroy(OWNER))


class CS2_057:
    """Shadow Bolt / 暗影箭
    对一个随从造成$4点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4)


class EX1_302:
    """Mortal Coil / 死亡缠绕
    对一个随从造成$1点伤害。如果消灭该随从，抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1), Dead(TARGET) & Draw(CONTROLLER)


class EX1_303:
    """Shadowflame / 暗影烈焰
    消灭一个友方随从，对所有敌方随从造成等同于其攻击力的伤害。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(ENEMY_MINIONS, ATK(TARGET)), Destroy(TARGET)


class EX1_308:
    """Soulfire / 灵魂之火
    造成$4点伤害，随机弃一 张牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4), Discard(RANDOM(FRIENDLY_HAND))


class EX1_309:
    """Siphon Soul / 灵魂虹吸
    消灭一个随从，为你的英雄恢复#3点生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), Heal(FRIENDLY_HERO, 3)


class EX1_312:
    """Twisting Nether / 扭曲虚空
    消灭所有随从和地标。"""

    play = Destroy(ALL_MINIONS)


class EX1_316:
    """Power Overwhelming / 力量的代价
    使一个友方随从获得+4/+4，该随从会在回合结束时死亡。死得很惨。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "EX1_316e")


class EX1_316e:
    events = TURN_END.on(Destroy(OWNER))
    tags = {
        GameTag.ATK: +4,
        GameTag.HEALTH: +4,
    }


class EX1_317:
    """Sense Demons / 感知恶魔
    从你的牌库中抽两张恶魔牌。"""

    play = (
        Find(FRIENDLY_DECK + DEMON) & ForceDraw(RANDOM(FRIENDLY_DECK + DEMON))
        | Give(CONTROLLER, "EX1_317t"),
    ) * 2


class EX1_320:
    """Bane of Doom / 末日灾祸
    对一个角色造成$3点伤害。如果消灭该角色，随机召唤一个恶魔。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), Dead(TARGET) & Summon(
        CONTROLLER, RandomMinion(race=Race.DEMON)
    )


class EX1_596:
    """Demonfire / 恶魔之火
    对一个随从造成$2点伤害，如果该随从是友方恶魔，则改为使其获得+2/+2。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Find(TARGET + FRIENDLY + DEMON) & Buff(TARGET, "EX1_596e") | Hit(TARGET, 2)


EX1_596e = buff(+2, +2)


class NEW1_003:
    """Sacrificial Pact / 牺牲契约
    消灭一个友方恶魔，为你的英雄恢复#5点生命值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 15,
    }
    play = Destroy(TARGET), Heal(FRIENDLY_HERO, 5)


class EX1_181:
    """Call of the Void / 虚空召唤
    随机将一张恶魔牌置入你的 手牌。"""

    # Add a random Demon to your hand.
    play = Give(CONTROLLER, RandomDemon())


class EX1_185:
    """Siegebreaker / 攻城恶魔
    嘲讽 你的其他恶魔拥有+1攻击力。"""

    # <b>Taunt</b> Your other Demons have +1 Attack.
    update = Refresh(FRIENDLY_MINIONS - SELF + DEMON, {GameTag.ATK: 1})
