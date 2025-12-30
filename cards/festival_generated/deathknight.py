# -*- coding: utf-8 -*-
"""
传奇音乐节（Festival of Legends）- DEATHKNIGHT 
"""

from ..utils import *

class JAM_007:
    """酷炫的食尸鬼 / Cool Ghoul
    <b>圣盾</b>，<b>复生</b>"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 1,
        GameTag.COST: 4,
        GameTag.DIVINE_SHIELD: True,
        GameTag.REBORN: True,
    }


class ETC_209:
    """硬核信徒 / Hardcore Cultist
    <b>战吼：</b>造成2点伤害。<b>压轴：</b>改为对所有敌人。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 3,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 2)
    finale = Hit(ENEMY_CHARACTERS, 2)


class ETC_427:
    """悦耳金属 / Harmonic Metal
    随机使你手牌中的4张随从牌获得+2/+2。<i>（每回合切换。）</i>"""
    tags = {
        GameTag.COST: 3,
    }
    play = Buff(RANDOM(FRIENDLY_HAND + MINION) * 4, "ETC_427e")


class ETC_427e:
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2}


class ETC_533:
    """狂欢舞台 / Mosh Pit
    消耗3份<b>残骸</b>，使一个友方随从获得<b>复生</b>。"""
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_CORPSE_COUNT: 3,
    }
    activate = SetTag(TARGET, {GameTag.REBORN: True})


class ETC_423:
    """奥金利斧 / Arcanite Ripper
    <b>亡语：</b>召唤一个1/1并具有<b>吸血</b>的亡灵。<i>（装备期间，在你的回合中使你的生命值发生变化以提升此效果！）</i>"""
    tags = {
        GameTag.ATK: 5,
        GameTag.DURABILITY: 2,
        GameTag.COST: 3,
    }
    deathrattle = Summon(CONTROLLER, "ETC_423t")


class ETC_423t:
    """亡灵 / Undead"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.LIFESTEAL: True,
    }


class JAM_006:
    """冻感舞步 / Cold Feet
    下个回合，敌方随从牌的法力值消耗增加（5）点。"""
    tags = {
        GameTag.COST: 2,
    }
    play = Buff(OPPONENT, "JAM_006e")


class JAM_006e:
    """下回合敌方随从增加5费"""
    update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: 5})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class JAM_008:
    """直播事故 / Dead Air
    消灭你的亡灵。再次召唤它们。"""
    tags = {
        GameTag.COST: 2,
    }
    play = (
        Destroy(FRIENDLY_MINIONS + UNDEAD) &
        Summon(CONTROLLER, Copy(FRIENDLY_MINIONS + UNDEAD + KILLED_THIS_TURN))
    )
class ETC_424:
    """死亡嘶吼 / Death Growl
    选择一个随从。将其<b>亡语</b>传播到相邻随从上。"""
    tags = {
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = CopyDeathrattles(TARGET, TARGET_ADJACENT)
class ETC_523:
    """死亡金属骑士 / Death Metal Knight
    <b>嘲讽</b>。在本回合中，如果你的英雄受到治疗，本牌改为消耗生命值而非法力值。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
        GameTag.TAUNT: True,
    }
    cost_health = FRIENDLY_HERO_HEALED_THIS_TURN
class JAM_005:
    """约德尔狂吼歌手 / Yelling Yodeler
    <b>战吼：</b>触发一个友方随从的<b>亡语</b>，触发两次。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Deathrattle(TARGET) * 2
class ETC_428:
    """碎骨速弹吉他手 / Boneshredder
    <b>战吼：</b>消耗5份<b>残骸</b>，触发并获得一个在本局对战中死亡的友方随从的<b>亡语</b>。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    requirements = {
        PlayReq.REQ_CORPSE_COUNT: 5,
    }
    play = (
        SpendCorpses(5) &
        CopyDeathrattle(SELF, RANDOM(FRIENDLY_MINIONS + KILLED_THIS_GAME)) &
        Deathrattle(RANDOM(FRIENDLY_MINIONS + KILLED_THIS_GAME))
    )
class ETC_522:
    """尖叫女妖 / Screaming Banshee
    <b>吸血</b>。在你的英雄获得生命值后，召唤一个具有等量攻击力与生命值的灵魂。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.COST: 5,
        GameTag.LIFESTEAL: True,
    }
    events = FRIENDLY_HERO_HEAL.on(
        Summon(CONTROLLER, "ETC_522t").then(
            SetAtk(Summon.CARD, Heal.AMOUNT),
            SetHealth(Summon.CARD, Heal.AMOUNT)
        )
    )


class ETC_522t:
    """灵魂 / Soul"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }
class ETC_526:
    """凯吉·海德 / Cage Head
    <b>亡语：</b>召唤一只9/9并具有<b>冲锋</b>和<b>嘲讽</b>的凋零野猪。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 1,
        GameTag.COST: 8,
    }
    deathrattle = Summon(CONTROLLER, "ETC_526t")


class ETC_526t:
    """凋零野猪 / Blight Boar"""
    tags = {
        GameTag.ATK: 9,
        GameTag.HEALTH: 9,
        GameTag.CHARGE: True,
        GameTag.TAUNT: True,
    }
class ETC_210:
    """通灵最强音 / Climactic Necrotic Explosion
    <b>吸血</b>。造成${0}点伤害。召唤{1}个{2}/{3}的灵魂。<i>（随你消耗过的<b>残骸</b>数量随机提升）</i>"""
    tags = {
        GameTag.COST: 10,
        GameTag.LIFESTEAL: True,
    }
    # Base effect: Deal 5 damage to all enemies, summon 2 3/3 Souls
    # This is a simplified implementation - the actual random improvement based on corpses
    # would require custom logic that tracks corpses spent throughout the game
    play = Hit(ENEMY_CHARACTERS, 5) & Summon(CONTROLLER, "ETC_210t") * 2


class ETC_210t:
    """灵魂 / Soul"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }
