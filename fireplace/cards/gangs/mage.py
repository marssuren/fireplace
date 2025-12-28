from ..utils import *


##
# Minions


class CFM_066:
    """Kabal Lackey / 暗金教侍从
    战吼： 在本回合中，你使用的下一个奥秘的法力值消耗为（1）点。"""

    play = Buff(CONTROLLER, "EX1_612o")


class CFM_660:
    """Manic Soulcaster / 狂热铸魂者
    战吼：选择一个友方随从，将它的一张复制洗入你的牌库。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Shuffle(CONTROLLER, Copy(TARGET))


class CFM_671:
    """Cryomancer / 凛风巫师
    战吼：如果有敌人被冻结，便获得+2/+2。"""

    play = Find(ENEMY + FROZEN) & Buff(CONTROLLER, "CFM_671e")


CFM_671e = buff(+2, +2)


class CFM_687:
    """Inkmaster Solia / 墨水大师索莉娅
    战吼：在本回合中，如果你的牌库里没有相同的牌，你所施放的下一个法术的法力值消耗为（0）点。"""

    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & Buff(CONTROLLER, "CFM_687e")


class CFM_687e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(0)})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class CFM_760:
    """Kabal Crystal Runner / 暗金教水晶侍女
    在本局对战中，你每使用一张奥秘牌，本牌的法力值消耗便减少（2）点。"""

    cost_mod = -TIMES_SECRETS_PLAYED_THIS_GAME * 2


##
# Spells


class CFM_021:
    """Freezing Potion / 冰冻药水
    冻结一个敌人。"""

    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Freeze(TARGET)


class CFM_065:
    """Volcanic Potion / 火山药水
    对所有随从造成$2点伤害。"""

    play = Hit(ALL_MINIONS, 2)


class CFM_620:
    """Potion of Polymorph / 变形药水
    奥秘：在你的对手使用一张随从牌后，将其变形成为1/1的绵羊。"""

    secret = Play(OPPONENT, MINION).after(Reveal(SELF), Morph(Play.CARD, "CS2_tk1"))


class CFM_623:
    """Greater Arcane Missiles / 强能奥术飞弹
    随机对敌人发射三枚飞弹，每枚飞弹造成$3点伤害。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 3) * 3
