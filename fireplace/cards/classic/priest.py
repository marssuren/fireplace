from ..utils import *


##
# Minions


class CS2_235:
    """Northshire Cleric / 北郡牧师
    每当一个随从获得治疗时，抽一张牌。"""

    events = Heal(ALL_MINIONS).on(Draw(CONTROLLER))


class EX1_091:
    """Cabal Shadow Priest / 秘教暗影祭司
    战吼：夺取一个攻击力小于或等于2的敌方随从的控制权。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_MAX_ATTACK: 2,
    }
    play = Steal(TARGET)


class EX1_335:
    """Lightspawn / 光耀之子
    本随从的攻击力始终等同于其生命值。"""

    update = Refresh(SELF, {GameTag.ATK: lambda self, i: self.health}, priority=100)


class EX1_341:
    """Lightwell / 光明之泉
    在你的回合开始时，随机为一个受伤的 友方角色恢复#3点生命值。"""

    events = OWN_TURN_BEGIN.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 3))


class EX1_350:
    """Prophet Velen / 先知维伦
    使你的法术和英雄技能的伤害和治疗效果翻倍。"""

    update = Refresh(
        CONTROLLER,
        {
            GameTag.HEALING_DOUBLE: 1,
            GameTag.SPELLPOWER_DOUBLE: 1,
            GameTag.HERO_POWER_DOUBLE: 1,
        },
    )


class EX1_591:
    """Auchenai Soulpriest / 奥金尼灵魂祭司
    你的恢复生命值的牌和技能改为造成等量的伤害。"""

    update = Refresh(
        CONTROLLER,
        {
            GameTag.EMBRACE_THE_SHADOW: True,
        },
    )


class EX1_623:
    """Temple Enforcer / 圣殿执行者
    战吼：使一个友方随从获得+3生命值。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "EX1_623e")


EX1_623e = buff(health=3)


class EX1_193:
    """Psychic Conjurer / 心灵咒术师
    战吼：复制你对手的牌库中的一张牌，并将其置入你的手牌。"""

    # <b>Battlecry:</b> Copy a card in your opponent’s deck and add it to your
    # hand.
    play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class EX1_195:
    """Kul Tiran Chaplain / 库尔提拉斯教士
    战吼：使一个友方随从获得+2生命值。"""

    # <b>Battlecry:</b> Give a friendly minion +2 Health.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "EX1_195e")


EX1_195e = buff(health=2)


class EX1_196:
    """Scarlet Subjugator / 血色征服者
    战吼：直到你的下个回合，使一个敌方随从获得-2攻击力。"""

    # <b>Battlecry:</b> Give an enemy minion -2 Attack until your_next turn.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "EX1_196e")


class EX1_196e:
    tags = {GameTag.ATK: -2}
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class EX1_198:
    """Natalie Seline / 娜塔莉·塞林
    战吼：消灭一个随从并获得其生命值。"""

    # <b>Battlecry:</b> Destroy a minion and gain its Health.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = (Buff(SELF, "EX1_198e", max_health=CURRENT_HEALTH(TARGET)), Destroy(TARGET))


##
# Spells


class CS2_004:
    """Power Word: Shield / 真言术：盾
    使一个随从获得+2生命值。 抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_004e")


CS2_004e = buff(health=2)


class CS1_112:
    """Holy Nova / 神圣新星
    对所有敌方随从造成$2点伤害，为所有友方角色恢复#2点 生命值。"""

    play = Hit(ENEMY_MINIONS, 2), Heal(FRIENDLY_CHARACTERS, 2)


class CS1_113:
    """Mind Control / 精神控制
    夺取一个敌方随从的控制权。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Steal(TARGET)


class CS1_129:
    """Inner Fire / 心灵之火
    使一个随从的攻击力等同于其生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS1_129e")


class CS1_129e:
    atk = lambda self, i: self._xatk

    def apply(self, target):
        self._xatk = target.health


class CS1_130:
    """Holy Smite / 神圣惩击
    对一个随从造成$3点伤害。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3)


class CS2_003:
    """Mind Vision / 心灵视界
    随机复制对手手牌中的一张牌，将其置入你的手牌。"""

    play = Give(CONTROLLER, Copy(RANDOM(ENEMY_HAND)))


class CS2_234:
    """Shadow Word: Pain / 暗言术：痛
    消灭一个攻击力小于或等于3的随从。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_MAX_ATTACK: 3,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET)


class CS2_236:
    """Divine Spirit / 神圣之灵
    使一个随从的生命值翻倍。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_236e", max_health=CURRENT_HEALTH(TARGET))


class DS1_233:
    """Mind Blast / 心灵震爆
    对敌方英雄造成$5点伤害。"""

    play = Hit(ENEMY_HERO, 5)


class EX1_332:
    """Silence / 沉默
    沉默一个随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Silence(TARGET)


class EX1_334:
    """Shadow Madness / 暗影狂乱
    直到回合结束，获得一个攻击力小于或等于3的敌方随从的控制权。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_TARGET_MAX_ATTACK: 3,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Steal(TARGET), Buff(TARGET, "EX1_334e")


class EX1_334e:
    events = [
        TURN_END.on(Destroy(SELF), Steal(OWNER, OPPONENT)),
        Silence(OWNER).on(Steal(OWNER, OPPONENT)),
    ]
    tags = {GameTag.CHARGE: True}


class EX1_339:
    """Thoughtsteal / 思维窃取
    复制你对手的牌库中的两张牌，并将其置入你的手牌。"""

    play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK) * 2))


class EX1_345:
    """Mindgames / 控心术
    随机将你对手的牌库中的一张随从牌的复制置入战场。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Find(ENEMY_DECK + MINION) & Summon(
        CONTROLLER, Copy(RANDOM(ENEMY_DECK + MINION))
    ) | Summon(CONTROLLER, "EX1_345t")


class EX1_621:
    """Circle of Healing / 治疗之环
    为所有随从恢复#4点生命值。"""

    play = Heal(ALL_MINIONS, 4)


class EX1_622:
    """Shadow Word: Death / 暗言术：灭
    消灭一个攻击力大于或等于5的随从。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_MIN_ATTACK: 5,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET)


class EX1_624:
    """Holy Fire / 神圣之火
    造成$5点伤害。为你的英雄恢复#5点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 5), Heal(FRIENDLY_HERO, 5)


class EX1_625:
    """Shadowform / 暗影形态
    你的英雄技能变为“造成2点伤害”。"""

    play = Switch(
        FRIENDLY_HERO_POWER,
        {
            "EX1_625t": Summon(CONTROLLER, "EX1_625t2"),
            "EX1_625t2": (),
            None: Summon(CONTROLLER, "EX1_625t"),
        },
    )


class EX1_625t:
    """Mind Spike"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 2)
    update = Refresh(CONTROLLER, {GameTag.SHADOWFORM: True})


class EX1_625t2:
    """Mind Shatter"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 3)
    update = Refresh(CONTROLLER, {GameTag.SHADOWFORM: True})


class EX1_626:
    """Mass Dispel / 群体驱散
    沉默所有敌方随从，抽一张牌。"""

    play = Silence(ENEMY_MINIONS), Draw(CONTROLLER)


class EX1_192:
    """Radiance / 圣光闪耀
    为你的英雄恢复#5点生命值。"""

    # Restore #5 Health to your hero.
    play = Heal(FRIENDLY_HERO, 5)


class EX1_194:
    """Power Infusion / 能量灌注
    使一个随从获得+2/+6。"""

    # Give a minion +2/+6.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "EX1_194e")


EX1_194e = buff(+2, +2)


class EX1_197:
    """Shadow Word: Ruin / 暗言术：毁
    消灭所有攻击力大于或等于5的随从。"""

    # Destroy all minions with 5 or more Attack.
    play = Destroy(ALL_MINIONS + (ATK >= 5))
