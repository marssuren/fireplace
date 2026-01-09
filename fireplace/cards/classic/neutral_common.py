from ..utils import *


##
# Free basic minions


class CS2_122:
    """Raid Leader / 团队领袖
    你的其他随从拥有+1攻击力。"""

    update = Refresh(FRIENDLY_MINIONS - SELF, buff="CS2_122e")


CS2_122e = buff(atk=1)


class CS2_222:
    """Stormwind Champion / 暴风城勇士
    你的其他随从拥有+1/+1。"""

    update = Refresh(FRIENDLY_MINIONS - SELF, buff="CS2_222o")


CS2_222o = buff(+1, +1)


class CS2_226:
    """Frostwolf Warlord / 霜狼督军
    战吼：战场上每有一个其他友方随从，便获得+1/+1。"""

    play = Buff(SELF, "CS2_226e") * Count(FRIENDLY_MINIONS - SELF)


CS2_226e = buff(+1, +1)


class EX1_011:
    """Voodoo Doctor / 巫医
    战吼： 恢复#2点生命值。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Heal(TARGET, 2)


class EX1_015:
    """Novice Engineer / 工程师学徒
    战吼：抽一张牌。"""

    play = Draw(CONTROLLER)


class EX1_082:
    """Mad Bomber / 疯狂投弹者
    战吼：造成3点伤害，随机分配到所有其他角色身上。"""

    play = Hit(RANDOM_OTHER_CHARACTER, 1) * 3


class EX1_102:
    """Demolisher / 攻城车
    在你的回合开始时，随机对一个敌人造成2点伤害。"""

    events = OWN_TURN_BEGIN.on(Hit(RANDOM_ENEMY_CHARACTER, 2))


class EX1_162:
    """Dire Wolf Alpha / 恐狼前锋
    相邻的随从拥有+1攻击力。"""

    update = Refresh(SELF_ADJACENT, buff="EX1_162o")


EX1_162o = buff(atk=1)


class EX1_399:
    """Gurubashi Berserker / 古拉巴什狂暴者
    每当本随从受到伤害，获得+3攻击力。"""

    events = SELF_DAMAGE.on(Buff(SELF, "EX1_399e"))


EX1_399e = buff(atk=3)


class EX1_508:
    """Grimscale Oracle / 暗鳞先知
    你的其他鱼人拥有+1攻击力。"""

    update = Refresh(FRIENDLY_MINIONS + MURLOC - SELF, buff="EX1_508o")


EX1_508o = buff(atk=1)


class EX1_593:
    """Nightblade / 夜刃刺客
    战吼：对敌方英雄造成3点伤害。"""

    play = Hit(ENEMY_HERO, 3)


class EX1_595:
    """Cult Master / 诅咒教派领袖
    在一个友方随从死亡后，抽一张牌。"""

    events = Death(FRIENDLY + MINION).on(Draw(CONTROLLER))


##
# Common basic minions


class CS2_117:
    """Earthen Ring Farseer / 大地之环先知
    战吼： 恢复#3点生命值。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Heal(TARGET, 3)


class CS2_141:
    """Ironforge Rifleman / 铁炉堡火枪手
    战吼：造成1点伤害。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 1)


class CS2_146:
    """Southsea Deckhand / 南海船工
    如果你装备着武器，本随从拥有 冲锋。"""

    update = Find(FRIENDLY_WEAPON) & Refresh(SELF, {GameTag.CHARGE: True})


class CS2_147:
    """Gnomish Inventor / 侏儒发明家
    战吼：抽一张牌。"""

    play = Draw(CONTROLLER)


class CS2_150:
    """Stormpike Commando / 雷矛特种兵
    战吼：造成2点伤害。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 2)


class CS2_151:
    """Silver Hand Knight / 白银之手骑士
    战吼：召唤一个2/2的侍从。"""

    play = Summon(CONTROLLER, "CS2_152")


class CS2_189:
    """Elven Archer / 精灵弓箭手
    战吼：造成1点伤害。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 1)


class CS2_188:
    """Abusive Sergeant / 叫嚣的中士
    战吼：在本回合中，使一个随从获得+2攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Buff(TARGET, "CS2_188o")


CS2_188o = buff(atk=2)


class CS2_196:
    """Razorfen Hunter / 剃刀猎手
    战吼：召唤一个1/1的野猪。"""

    play = Summon(CONTROLLER, "CS2_boar")


class CS2_203:
    """Ironbeak Owl / 铁喙猫头鹰
    战吼： 沉默一个随从。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Silence(TARGET)


class CS2_221:
    """Spiteful Smith / 恶毒铁匠
    本随从受伤时，你的武器拥有+2攻击力。"""

    enrage = Refresh(FRIENDLY_WEAPON, buff="CS2_221e")


CS2_221e = buff(atk=2)


class CS2_227:
    """Venture Co. Mercenary / 风险投资公司雇佣兵
    你的随从牌的法力值消耗增加（3）点。"""

    update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: +3})


class DS1_055:
    """Darkscale Healer / 暗鳞治愈者
    战吼：为所有友方角色恢复#2点生命值。"""

    play = Heal(FRIENDLY_CHARACTERS, 2)


class EX1_007:
    """Acolyte of Pain / 苦痛侍僧
    每当本随从受到伤害，抽一张牌。"""

    events = SELF_DAMAGE.on(Draw(CONTROLLER))


class EX1_019:
    """Shattered Sun Cleric / 破碎残阳祭司
    战吼：使一个友方随从获得+1/+1。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "EX1_019e")


EX1_019e = buff(+1, +1)


class EX1_025:
    """Dragonling Mechanic / 机械幼龙技工
    战吼：召唤一个2/1的机械幼龙。"""

    play = Summon(CONTROLLER, "EX1_025t")


class EX1_029:
    """Leper Gnome / 麻风侏儒
    亡语：对敌方英雄造成2点伤害。"""

    deathrattle = Hit(ENEMY_HERO, 2)


class EX1_046:
    """Dark Iron Dwarf / 黑铁矮人
    战吼：在本回合中，使一个随从获得+2攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Buff(TARGET, "EX1_046e")


EX1_046e = buff(atk=2)


class EX1_048:
    """Spellbreaker / 破法者
    战吼： 沉默一个随从。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Silence(TARGET)


class EX1_049:
    """Youthful Brewmaster / 年轻的酒仙
    战吼：使一个友方随从从战场上移回你的手牌。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Bounce(TARGET)


class EX1_057:
    """Ancient Brewmaster / 年迈的酒仙
    战吼：使一个友方随从从战场上移回你的手牌。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Bounce(TARGET)


class EX1_066:
    """Acidic Swamp Ooze / 酸性沼泽软泥怪
    战吼： 摧毁对手的武器。"""

    play = Destroy(ENEMY_WEAPON)


class EX1_096:
    """Loot Hoarder / 战利品贮藏者
    亡语：抽一张牌。"""

    deathrattle = Draw(CONTROLLER)


class EX1_283:
    """Frost Elemental / 冰霜元素
    战吼： 冻结一个角色。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Freeze(TARGET)


class EX1_390:
    """Tauren Warrior / 牛头人战士
    嘲讽 受伤时拥有+3攻 击力。"""

    enrage = Refresh(SELF, buff="EX1_390e")


EX1_390e = buff(atk=3)


class EX1_393:
    """Amani Berserker / 阿曼尼狂战士
    受伤时拥有+3攻 击力。"""

    enrage = Refresh(SELF, buff="EX1_393e")


EX1_393e = buff(atk=3)


class EX1_412:
    """Raging Worgen / 暴怒的狼人
    受伤时拥有+1攻击力和风怒。"""

    enrage = Refresh(SELF, buff="EX1_412e")


EX1_412e = buff(atk=1, windfury=True)


class EX1_506:
    """Murloc Tidehunter / 鱼人猎潮者
    战吼：召唤一个1/1的鱼人斥候。"""

    play = Summon(CONTROLLER, "EX1_506a")


class EX1_556:
    """Harvest Golem / 麦田傀儡
    亡语：召唤一个2/1的损坏的傀儡。"""

    deathrattle = Summon(CONTROLLER, "skele21")


class EX1_583:
    """Priestess of Elune / 艾露恩的女祭司
    战吼：为你的英雄恢复#4点生命值。"""

    play = Heal(FRIENDLY_HERO, 4)


class NEW1_018:
    """Bloodsail Raider / 血帆袭击者
    战吼： 获得等同于你的武器攻击力的攻击力。"""

    play = (Find(FRIENDLY_WEAPON), Buff(SELF, "NEW1_018e", atk=ATK(FRIENDLY_WEAPON)))


class NEW1_022:
    """Dread Corsair / 恐怖海盗
    嘲讽 你的武器每有1点攻击力，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -ATK(FRIENDLY_WEAPON)


class tt_004:
    """Flesheating Ghoul"""

    events = Death(MINION).on(Buff(SELF, "tt_004o"))


tt_004o = buff(atk=1)


##
# Unused buffs

# Full Strength (Injured Blademaster)
CS2_181e = buff(atk=2)
