from ..utils import *


##
# Minions


class CS2_042:
    """Fire Elemental / 火元素
    战吼：造成4点伤害。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 3)


class EX1_258:
    """Unbound Elemental / 无羁元素
    在你使用一张具有过载的牌后，便获得+1/+1。"""

    events = Play(CONTROLLER, OVERLOAD).on(Buff(SELF, "EX1_258e"))


EX1_258e = buff(+1, +1)


class EX1_565:
    """Flametongue Totem / 火舌图腾
    相邻的随从拥有+2攻击力。"""

    update = Refresh(SELF_ADJACENT, buff="EX1_565o")


EX1_565o = buff(atk=2)


class EX1_575:
    """Mana Tide Totem / 法力之潮图腾
    在你的回合结束时，抽一张牌。"""

    events = OWN_TURN_END.on(Draw(CONTROLLER))


class EX1_587:
    """Windspeaker / 风语者
    战吼：使一个友方随从获得风怒。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = GiveWindfury(TARGET - WINDFURY)


##
# Spells


class CS2_037:
    """Frost Shock / 冰霜震击
    对一个敌方角色造成$1点伤害，并使其冻结。"""

    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1), Freeze(TARGET)


class CS2_038:
    """Ancestral Spirit / 先祖之魂
    使一个随从获得“亡语：再次召唤本随从。”"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_038e")


class CS2_038e:
    deathrattle = Summon(CONTROLLER, Copy(OWNER))
    tags = {GameTag.DEATHRATTLE: True}


class CS2_039:
    """Windfury / 风怒
    使一个随从获得风怒。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = GiveWindfury(TARGET - WINDFURY)


class CS2_041:
    """Ancestral Healing / 先祖治疗
    为一个随从恢复所有生命值并使其获得嘲讽。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = FullHeal(TARGET), Buff(TARGET, "CS2_041e")


CS2_041e = buff(taunt=True)


class CS2_045:
    """Rockbiter Weapon / 石化武器
    在本回合中，使一个友方角色获得+3攻击力。"""

    requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_045e")


CS2_045e = buff(atk=3)


class CS2_046:
    """Bloodlust / 嗜血
    在本回合中，使你的所有随从获得+3攻击力。"""

    play = Buff(FRIENDLY_MINIONS, "CS2_046e")


CS2_046e = buff(atk=3)


class CS2_053:
    """Far Sight / 视界术
    抽一张牌，该牌的法力值消耗减少（3）点。"""

    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "CS2_053e"))


class CS2_053e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -3}


class EX1_238:
    """Lightning Bolt / 闪电箭
    造成$3点伤害，过载：（1）"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)


class EX1_241:
    """Lava Burst / 熔岩爆裂
    造成$5点伤害，过载：（2）"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 5)


class EX1_244:
    """Totemic Might / 图腾之力
    使你的图腾获得+2生命值。"""

    play = Buff(FRIENDLY_MINIONS + TOTEM, "EX1_244e")


EX1_244e = buff(health=2)


class EX1_246:
    """Hex / 妖术
    使一个随从变形成为一只0/1并具有嘲讽的青蛙。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Morph(TARGET, "hexfrog")


class EX1_248:
    """Feral Spirit / 野性狼魂
    召唤两只2/3并具有嘲讽的幽灵狼。过载：（1）"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "EX1_tk11") * 2


class EX1_251:
    """Forked Lightning / 叉状闪电
    随机对两个敌方随从造成$2点伤害，过载：（2）"""

    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION * 2, 2)


class EX1_245:
    """Earth Shock / 大地震击
    沉默一个随从，然后对其造成$1点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Silence(TARGET), Hit(TARGET, 1)


class EX1_259:
    """Lightning Storm / 闪电风暴
    对所有敌方随从造成$3点伤害，过载：（1）"""

    play = Hit(ENEMY_MINIONS, RandomNumber(2, 3))
