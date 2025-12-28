from ..utils import *


##
# Minions


class EX1_131:
    """Defias Ringleader / 迪菲亚头目
    连击：召唤一个2/1的迪菲亚强盗。"""

    combo = Summon(CONTROLLER, "EX1_131t")


class EX1_134:
    """SI:7 Agent / 军情七处特工
    连击：造成3点伤害。"""

    requirements = {PlayReq.REQ_TARGET_FOR_COMBO: 0}
    combo = Hit(TARGET, 2)


class EX1_613:
    """Edwin VanCleef / 艾德温·范克里夫
    连击：在本回合中，你每使用一张其他牌，便获得+2/+2。"""

    combo = Buff(SELF, "EX1_613e") * NUM_CARDS_PLAYED_THIS_TURN


EX1_613e = buff(+2, +2)


class NEW1_005:
    """Kidnapper / 劫持者
    连击：将一个随从移回其拥有者的手牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_FOR_COMBO: 0}
    combo = Bounce(TARGET)


class NEW1_014:
    """Master of Disguise / 伪装大师
    战吼：直到你的下个回合，使一个友方随从获得潜行。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET - STEALTH, "NEW1_014e")


class NEW1_014e:
    """Disguised"""

    tags = {GameTag.STEALTH: True}
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


##
# Spells


class CS2_072:
    """Backstab / 背刺
    对一个未受伤的随从造成$2点 伤害。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class CS2_073:
    """Cold Blood / 冷血
    使一个随从获得+2攻击力；连击：改为获得+4攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_073e")
    combo = Buff(TARGET, "CS2_073e2")


CS2_073e = buff(atk=2)
CS2_073e2 = buff(atk=4)


class CS2_074:
    """Deadly Poison / 致命药膏
    使你的武器获得+2攻击力。"""

    requirements = {PlayReq.REQ_WEAPON_EQUIPPED: 0}
    play = Buff(FRIENDLY_WEAPON, "CS2_074e")


CS2_074e = buff(atk=2)


class CS2_075:
    """Sinister Strike / 影袭
    对敌方英雄造成$3点伤害。"""

    play = Hit(ENEMY_HERO, 3)


class CS2_076:
    """Assassinate / 刺杀
    消灭一个敌方随从。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET)


class CS2_077:
    """Sprint / 疾跑
    抽四张牌。"""

    play = Draw(CONTROLLER) * 4


class CS2_233:
    """Blade Flurry / 剑刃乱舞
    摧毁你的武器，对所有敌方随从 造成等同于其攻击力的伤害。"""

    requirements = {PlayReq.REQ_WEAPON_EQUIPPED: 0}
    play = Hit(ENEMY_MINIONS, ATK(FRIENDLY_WEAPON)), Destroy(FRIENDLY_WEAPON)


class EX1_124:
    """Eviscerate / 刺骨
    造成$2点伤害；连击：改为造成$4点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2)
    combo = Hit(TARGET, 4)


class EX1_126:
    """Betrayal / 背叛
    使一个敌方随从对其相邻的随从 造成等同于其攻击力的伤害。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(SELF_ADJACENT, ATK(SELF), source=TARGET)


class EX1_128:
    """Conceal / 隐藏
    直到你的下个回合，使所有友方随从获得潜行。"""

    play = (
        Buff(FRIENDLY_MINIONS - STEALTH, "EX1_128e"),
        Stealth(FRIENDLY_MINIONS),
    )


class EX1_128e:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class EX1_129:
    """Fan of Knives / 刀扇
    对所有敌方随从造成$1点伤害，抽一张牌。"""

    play = Hit(ENEMY_MINIONS, 1), Draw(CONTROLLER)


class EX1_137:
    """Headcrack / 裂颅之击
    对敌方英雄造成$2点伤害；连击：在下个回合将其移回你的手牌。"""

    play = Hit(ENEMY_HERO, 2)
    combo = (play, TURN_END.on(Give(CONTROLLER, "EX1_137")))


class EX1_144:
    """Shadowstep / 暗影步
    将一个友方随从移回你的手牌，它的法力值消耗减少 （2）点。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Bounce(TARGET), Buff(TARGET, "EX1_144e")


@custom_card
class EX1_144e:
    tags = {
        GameTag.CARDNAME: "Shadowstep Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -2,
    }
    events = REMOVED_IN_PLAY


class EX1_145:
    """Preparation / 伺机待发
    在本回合中，你所施放的下一个法术的法力值消耗减少（2）点。"""

    play = Buff(CONTROLLER, "EX1_145o")


class EX1_145o:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -2})
    events = OWN_SPELL_PLAY.on(Destroy(SELF))


class EX1_278:
    """Shiv / 毒刃
    造成$1点伤害，抽一张牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1), Draw(CONTROLLER)


class EX1_581:
    """Sap / 闷棍
    将一个敌方随从移回你对手的 手牌。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Bounce(TARGET)


class NEW1_004:
    """Vanish / 消失
    将所有随从移回其拥有者的 手牌。"""

    play = Bounce(ALL_MINIONS)


##
# Weapons


class EX1_133:
    """Perdition's Blade / 毁灭之刃
    战吼：造成1点伤害。连击：改为造成2点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 1)
    combo = Hit(TARGET, 2)


class EX1_182:
    """Pilfer / 窃取
    随机将一张另一职业的卡牌置入你的手牌。"""

    # Add a random card from another class to_your hand.</i>.
    play = Give(CONTROLLER, RandomCollectible(card_class=ANOTHER_CLASS))


class EX1_191:
    """Plaguebringer / 瘟疫使者
    战吼：使一个友方随从获得剧毒。"""

    # <b>Battlecry:</b> Give a friendly minion <b>Poisonous</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = GivePoisonous(TARGET)
