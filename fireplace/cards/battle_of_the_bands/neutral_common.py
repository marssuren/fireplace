# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- 中立 普通
"""

from ..utils import *

class ETC_102:
    """空气吉他手 / Air Guitarist
    <b>战吼：</b>使你的武器获得+1耐久度。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    play = Buff(FRIENDLY_WEAPON, "ETC_102e")


class ETC_102e:
    tags = {GameTag.DURABILITY: 1}


class ETC_086:
    """强音雷象 / Amplified Elekk
    <b>嘲讽</b>。<b>亡语：</b>对所有敌方随从造成3点伤害。"""
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 12,
        GameTag.COST: 10,
        GameTag.TAUNT: True,
    }
    deathrattle = Hit(ENEMY_MINIONS, 3)


class ETC_109:
    """吵吵歌迷 / Annoying Fan
    <b>战吼：</b>选择一个随从。当本随从存活时，选中的随从无法攻击。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "ETC_109e")


class ETC_109e:
    """无法攻击"""
    tags = {GameTag.CANT_ATTACK: True}


class ETC_325:
    """音乐治疗师 / Audio Medic
    <b>突袭</b>。<b>压轴：</b>获得<b>吸血</b>。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.RUSH: True,
    }
    finale = Buff(SELF, "ETC_325e")


class ETC_325e:
    tags = {GameTag.LIFESTEAL: True}


class ETC_543:
    """举烛观众 / Candleraiser
    <b>圣盾</b>。<b>压轴：</b>使相邻的随从获得<b>圣盾</b>。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        GameTag.DIVINE_SHIELD: True,
    }
    finale = SetTag(SELF_ADJACENT, {GameTag.DIVINE_SHIELD: True})


class ETC_099:
    """公演增强幼龙 / Concert Promo-Drake
    <b>可交易</b>
<b>压轴：</b>消灭一个敌方随从。"""
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 8,
        GameTag.TRADEABLE: True,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    finale = Destroy(TARGET)


class ETC_101:
    """牛铃独演者 / Cowbell Soloist
    <b>战吼：</b>如果你没有控制其他随从，造成2点伤害。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Find(FRIENDLY_MINIONS - SELF) | Hit(TARGET, 2)


class ETC_106:
    """频率振荡机 / Frequency Oscillator
    <b>战吼：</b>你的下一张机械牌的法力值消耗减少（1）点。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    play = Buff(CONTROLLER, "ETC_106e")


class ETC_106e:
    """下一张机械牌减费"""
    update = Refresh(FRIENDLY_HAND + MECH, {GameTag.COST: -1})
    events = Play(CONTROLLER, MECH).on(Destroy(SELF))


class ETC_088:
    """幽灵写手 / Ghost Writer
    <b>战吼：</b><b>发现</b>一张法术牌。<b>压轴：</b>再<b>发现</b>一张。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    play = GenericChoice(CONTROLLER, DISCOVER(SPELL))
    finale = GenericChoice(CONTROLLER, DISCOVER(SPELL))
class ETC_103:
    """风潮浪客 / Hipster
    <b>战吼：</b><b>发现</b>一张不在对手牌库中的对手职业的法术牌。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    play = GenericChoice(CONTROLLER, DISCOVER(SPELL + (CARD_CLASS == OPPONENT_CLASS) - IN_ENEMY_DECK))
class ETC_418:
    """乐器技师 / Instrument Tech
    <b>战吼：</b>抽一张武器牌。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)
class ETC_111:
    """商品卖家 / Merch Seller
    在你的回合结束时，随机将一张法术牌置于你对手的牌库顶。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    events = OWN_TURN_END.on(Shuffle(OPPONENT, RandomSpell(), TOPDECK))
class ETC_108:
    """痴醉歌迷 / Obsessive Fan
    <b>战吼：</b>选择一个随从。当本随从存活时，选中的随从拥有<b>潜行</b>。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 6,
        GameTag.COST: 4,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "ETC_108e")


class ETC_108e:
    """潜行"""
    tags = {GameTag.STEALTH: True}
class ETC_420:
    """服装裁缝 / Outfit Tailor
    <b>战吼：</b>使一个友方随从获得等同于本随从的攻击力和生命值。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0}
    play = Buff(TARGET, "ETC_420e")


class ETC_420e:
    """获得攻击力和生命值"""
    atk = lambda self, i: ATK(OWNER(SELF))
    max_health = lambda self, i: CURRENT_HEALTH(OWNER(SELF))
class ETC_326:
    """狗仔队 / Paparazzi
    <b>战吼：</b><b>发现</b>一张<b>传说</b>随从牌。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    play = GenericChoice(CONTROLLER, DISCOVER(MINION + LEGENDARY))
class ETC_350:
    """派对动物 / Party Animal
    <b>战吼：</b>使你手牌中每个不同类型的各一张随从牌获得+1/+1。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    play = Buff(FRIENDLY_HAND + MINION + UNIQUE_RACE, "ETC_350e")


class ETC_350e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}
class ETC_540:
    """烟火技师 / Pyrotechnician
    在你施放一个法术后，随机将一张火焰法术牌置入你的手牌。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    events = Play(CONTROLLER, SPELL).after(Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.FIRE)))
class JAM_033:
    """混搭乐师 / Remixed Musician
    <b>突袭</b>。在你的手牌中时会获得一项额外效果，该效果每回合都会改变。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.RUSH: True,
    }
    # Remixed 机制：在手牌中每回合改变效果，这是一个复杂的机制
    # 需要在 CardDefs.xml 中定义具体的效果变化
    pass
class ETC_742:
    """摇滚巨石 / Rolling Stone
    <b>突袭</b>。<b>战吼：</b>如果你使用的上一张牌法力值消耗为（1）点，便获得+1/+1。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.RUSH: True,
    }
    play = Find(FRIENDLY_CONTROLLER + LAST_CARD_PLAYED + (COST == 1)) & Buff(SELF, "ETC_742e")


class ETC_742e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}
class ETC_107:
    """喧哗歌迷 / Rowdy Fan
    <b>战吼：</b>选择一个随从。当本随从存活时，选中的随从拥有+4攻击力。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "ETC_107e")


class ETC_107e:
    """获得+4攻击力"""
    tags = {GameTag.ATK: 4}
class ETC_105:
    """立体声图腾 / Stereo Totem
    在你的回合结束时，随机使你手牌中的一张随从牌获得+2/+2。"""
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_HAND + MINION), "ETC_105e"))


class ETC_105e:
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2}
