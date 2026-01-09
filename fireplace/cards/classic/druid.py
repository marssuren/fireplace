from ..utils import *


##
# Minions


class EX1_165:
    """Druid of the Claw / 利爪德鲁伊
    抉择：变形成为7/6并具有突袭；或者变形成为4/9并具有嘲讽。"""

    choose = ("EX1_165a", "EX1_165b")
    play = (ChooseBoth(CONTROLLER), Morph(SELF, "OG_044a"))


class EX1_165a:
    play = Morph(SELF, "EX1_165t1")


class EX1_165b:
    play = Morph(SELF, "EX1_165t2")


class EX1_166:
    """Keeper of the Grove / 丛林守护者
    抉择：造成2点伤害；或者沉默一个随从。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("EX1_166a", "EX1_166b")
    play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Silence(TARGET))


class EX1_166a:
    play = Hit(TARGET, 2)
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}


class EX1_166b:
    play = Silence(TARGET)
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}


class EX1_178:
    """Ancient of War / 战争古树
    抉择： +5攻击力；或者+5生命值并具有嘲讽。"""

    choose = ("EX1_178b", "EX1_178a")
    play = ChooseBoth(CONTROLLER) & (Buff(SELF, "EX1_178ae"), Buff(SELF, "EX1_178be"))


class EX1_178a:
    play = Buff(SELF, "EX1_178ae")


EX1_178ae = buff(health=5, taunt=True)


class EX1_178b:
    play = Buff(SELF, "EX1_178be")


EX1_178be = buff(atk=5)


class EX1_573:
    """Cenarius / 塞纳留斯
    抉择：使你的所有其他随从获得+2/+2；或者召唤两个2/2并具有嘲讽的树人。"""

    choose = ("EX1_573a", "EX1_573b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(FRIENDLY_MINIONS - SELF, "EX1_573ae"),
        Summon(CONTROLLER, "EX1_573t") * 2,
    )


class EX1_573a:
    play = Buff(FRIENDLY_MINIONS - SELF, "EX1_573ae")


EX1_573ae = buff(+2, +2)


class EX1_573b:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 2,
    }
    play = SummonBothSides(CONTROLLER, "EX1_573t") * 2


class NEW1_008:
    """Ancient of Lore / 知识古树
    抉择：抽两张牌；或者恢复#7点生命值。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("NEW1_008a", "NEW1_008b")
    play = ChooseBoth(CONTROLLER) & (Draw(CONTROLLER), Heal(TARGET, 5))


class NEW1_008a:
    play = Draw(CONTROLLER)


class NEW1_008b:
    play = Heal(TARGET, 5)
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}


##
# Spells


class CS2_005:
    """Claw / 爪击
    使你的英雄获得2点护甲值，并在本回合中获得 +2攻击力。"""

    play = Buff(FRIENDLY_HERO, "CS2_005o"), GainArmor(FRIENDLY_HERO, 2)


CS2_005o = buff(atk=2)


class CS2_007:
    """Healing Touch / 治疗之触
    恢复#8点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 8)


class CS2_008:
    """Moonfire / 月火术
    造成$1点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1)


class CS2_009:
    """Mark of the Wild / 野性印记
    使一个随从获得嘲讽和+2/+3。（+2攻击力/+3生命值）"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_009e")


CS2_009e = buff(+2, +2, taunt=True)


class CS2_011:
    """Savage Roar / 野蛮咆哮
    在本回合中，使你的所有角色获得+2攻击力。"""

    play = Buff(FRIENDLY_CHARACTERS, "CS2_011o")


CS2_011o = buff(atk=2)


class CS2_012:
    """Swipe / 横扫
    对一个敌人造成$4点伤害，并对所有其他敌人 造成$1点伤害。"""

    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4), Hit(ENEMY_CHARACTERS - TARGET, 1)


class CS2_013:
    """Wild Growth / 野性成长
    获得一个空的法力水晶。"""

    # 如果已达到最大法力值,给予超额法力牌,否则获得空法力水晶
    play = AT_MAX_MANA(CONTROLLER) & Give(CONTROLLER, "CS2_013t") | GainEmptyMana(
        CONTROLLER, 1
    )


class CS2_013t:
    play = Draw(CONTROLLER)


class EX1_154:
    """Wrath / 愤怒
    抉择： 对一个随从造成$3点伤害；或者造成$1点伤害并抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    choose = ("EX1_154a", "EX1_154b")
    play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 3), Hit(TARGET, 1), Draw(CONTROLLER))


class EX1_154a:
    """Wrath (3 Damage)"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)


class EX1_154b:
    """Wrath (1 Damage)"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1), Draw(CONTROLLER)


class EX1_155:
    """Mark of Nature / 自然印记
    抉择： 使一个随从获得+4攻击力；或者+4生命值和嘲讽。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    choose = ("EX1_155a", "EX1_155b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(TARGET, "EX1_155ae"),
        Buff(TARGET, "EX1_155be"),
    )


class EX1_155a:
    play = Buff(TARGET, "EX1_155ae")
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}


EX1_155ae = buff(atk=4)


class EX1_155b:
    play = Buff(TARGET, "EX1_155be")
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}


EX1_155be = buff(health=4, taunt=True)


class EX1_158:
    """Soul of the Forest / 丛林之魂
    使你的所有随从获得“亡语：召唤一个2/2的树人”。"""

    play = Buff(FRIENDLY_MINIONS, "EX1_158e")


class EX1_158e:
    deathrattle = Summon(CONTROLLER, "EX1_158t")
    tags = {GameTag.DEATHRATTLE: True}


class EX1_160:
    """Power of the Wild / 野性之力
    抉择：使你的所有随从获得+1/+1；或者召唤一只3/2的 猎豹。"""

    choose = ("EX1_160a", "EX1_160b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(FRIENDLY_MINIONS, "EX1_160be"),
        Summon(CONTROLLER, "EX1_160t"),
    )


class EX1_160a:
    play = Summon(CONTROLLER, "EX1_160t")
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}


class EX1_160b:
    play = Buff(FRIENDLY_MINIONS, "EX1_160be")


EX1_160be = buff(+1, +1)


class EX1_161:
    """Naturalize / 自然平衡
    消灭一个随从，你的对手抽两张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), Draw(OPPONENT) * 2


class EX1_164:
    """Nourish / 滋养
    抉择：获得两个法力水晶；或者抽三张牌。"""

    choose = ("EX1_164a", "EX1_164b")
    play = ChooseBoth(CONTROLLER) & (GainMana(CONTROLLER, 2), Draw(CONTROLLER) * 3)


class EX1_164a:
    play = GainMana(CONTROLLER, 2)


class EX1_164b:
    play = Draw(CONTROLLER) * 3


class EX1_169:
    """Innervate / 激活
    在本回合中，获得一个 法力水晶。"""

    play = ManaThisTurn(CONTROLLER, 1)


class EX1_173:
    """Starfire / 星火术
    造成$5点伤害。抽一张牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 5), Draw(CONTROLLER)


class EX1_570:
    """Bite / 撕咬
    使你的英雄获得4点护甲值，并在本回合中获得 +4攻击力。"""

    play = Buff(FRIENDLY_HERO, "EX1_570e"), GainArmor(FRIENDLY_HERO, 4)


EX1_570e = buff(atk=4)


class EX1_571:
    """Force of Nature / 自然之力
    召唤三个2/2的树人。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "EX1_tk9") * 3


class EX1_578:
    """Savagery / 野蛮之击
    对一个随从造成等同于你的英雄攻击力的伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, ATK(FRIENDLY_HERO))


class NEW1_007:
    """Starfall / 星辰坠落
    抉择：对一个随从造成$5点伤害；或者对所有敌方随从造成$2点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("NEW1_007a", "NEW1_007b")
    play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 5), Hit(ENEMY_MINIONS, 2))


class NEW1_007a:
    play = Hit(ENEMY_MINIONS, 2)


class NEW1_007b:
    play = Hit(TARGET, 5)
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}


class EX1_183:
    """Gift of the Wild / 野性赐福
    使你的所有随从获得+2/+2和 嘲讽。"""

    # Give your minions +2/+2 and <b>Taunt</b>.
    play = Buff(FRIENDLY_MINIONS, "EX1_183e")


EX1_183e = buff(+2, +2, taunt=True)
