from ..utils import *


##
# Minions


class AT_046:
    """Tuskarr Totemic / 海象人图腾师
    战吼：随机召唤一个基础图腾。"""

    play = Summon(CONTROLLER, RandomBasicTotem())


class AT_047:
    """Draenei Totemcarver / 德莱尼图腾师
    战吼：每有一个友方图腾，便获得+1/+1。"""

    play = Buff(SELF, "AT_047e") * Count(FRIENDLY_MINIONS + TOTEM)


AT_047e = buff(+1, +1)


class AT_049:
    """Thunder Bluff Valiant / 雷霆崖勇士
    战吼，激励：使你的图腾获得+2攻击力。"""

    inspire = Buff(FRIENDLY_MINIONS + TOTEM, "AT_049e")


AT_049e = buff(atk=2)


class AT_054:
    """The Mistcaller / 唤雾者伊戈瓦尔
    战吼：使你的手牌和牌库里的所有随从牌获得+1/+1。"""

    # The Enchantment ID is correct
    play = Buff(FRIENDLY_HAND | FRIENDLY_DECK, "AT_045e")


AT_045e = buff(+1, +1)


##
# Spells


class AT_048:
    """Healing Wave / 治疗波
    恢复#8点生命值。揭示双方牌库里的一张随从牌。如果你的牌法力值 消耗较大，改为恢复#16点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = JOUST & Heal(TARGET, 14) | Heal(TARGET, 7)


class AT_051:
    """Elemental Destruction / 元素毁灭
    对所有随从造成$4到$5点伤害。过载：（2）"""

    play = Hit(ALL_MINIONS, RandomNumber(4, 5))


class AT_053:
    """Ancestral Knowledge / 先祖知识
    抽两张牌。过载：（1）"""

    play = Draw(CONTROLLER) * 2


##
# Weapons


class AT_050:
    """Charged Hammer / 灌魔之锤
    亡语：你的英雄技能改为“造成 2点伤害”。"""

    deathrattle = Summon(CONTROLLER, "AT_050t")


class AT_050t:
    activate = Hit(TARGET, 2)
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
