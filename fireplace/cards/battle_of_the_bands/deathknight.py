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
    """Mosh Pit - 狂欢舞台
    2费 地标
    消耗3份残骸,使一个友方随从获得复生。

    官方数据确认：2费，2耐久度
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 2,
        GameTag.HEALTH: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINIMUM_CORPSES: 3,  # 需要至少3份残骸
    }
    # 地标激活效果:消耗3份残骸,使目标获得复生
    def activate(self):
        yield SpendCorpses(CONTROLLER, 3)
        yield SetTags(TARGET, {GameTag.REBORN: True})


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
        Destroy(FRIENDLY_MINIONS + UNDEAD),
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
    play = CopyDeathrattleBuff(TARGET, TARGET_ADJACENT)
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
        PlayReq.REQ_MINIMUM_CORPSES: 5,
    }
    play = (
        SpendCorpses(CONTROLLER, 5),
        CopyDeathrattleBuff(SELF, RANDOM(FRIENDLY_MINIONS + KILLED)),
        Deathrattle(RANDOM(FRIENDLY_MINIONS + KILLED))
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
    events = Heal(FRIENDLY_HERO).on(
        Summon(CONTROLLER, "ETC_522t").then(
            Buff(Summon.CARD, "ETC_522e", atk=Heal.AMOUNT, max_health=Heal.AMOUNT)
        )
    )


class ETC_522t:
    """灵魂 / Soul"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }

class ETC_522e:
    """灵魂属性增益"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

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
    
    def play(self):
        """
        打出效果：造成伤害并召唤灵魂
        
        基础效果：造成6点伤害，召唤3个2/2灵魂
        动态提升：每消耗1个残骸，随机提升以下参数之一：
        - 伤害值（初始6）
        - 召唤数量（初始3，上限7）
        - 灵魂攻击力（初始2）
        - 灵魂生命值（初始2）
        
        提升机制：基于 player.total_corpses_spent（本局对战中累积消耗的残骸总数）
        """
        # 基础数值
        base_damage = 6
        base_soul_count = 3
        base_soul_atk = 2
        base_soul_health = 2
        
        # 根据消耗的残骸总数进行随机提升
        total_spent = self.controller.total_corpses_spent
        
        # 初始化提升值
        damage_bonus = 0
        soul_count_bonus = 0
        soul_atk_bonus = 0
        soul_health_bonus = 0
        
        # 每消耗1个残骸，随机提升一个参数
        for _ in range(total_spent):
            stat = self.game.random.choice(['damage', 'count', 'atk', 'health'])
            if stat == 'damage':
                damage_bonus += 1
            elif stat == 'count':
                # 召唤数量上限为7
                if base_soul_count + soul_count_bonus < 7:
                    soul_count_bonus += 1
            elif stat == 'atk':
                soul_atk_bonus += 1
            elif stat == 'health':
                soul_health_bonus += 1
        
        # 计算最终数值
        final_damage = base_damage + damage_bonus
        final_soul_count = base_soul_count + soul_count_bonus
        final_soul_atk = base_soul_atk + soul_atk_bonus
        final_soul_health = base_soul_health + soul_health_bonus
        
        # 造成伤害（吸血效果由 LIFESTEAL 标签自动处理）
        yield Hit(ENEMY_CHARACTERS, final_damage)
        
        # 召唤灵魂
        for _ in range(final_soul_count):
            soul = yield Summon(CONTROLLER, "ETC_210t")
            if soul:
                # 设置灵魂的攻击力和生命值
                yield Buff(soul[0], "ETC_210e", atk=final_soul_atk - 1, max_health=final_soul_health - 1)


class ETC_210e:
    """通灵最强音灵魂增益 / Climactic Necrotic Explosion Soul Buff
    
    动态增益：根据消耗的残骸数量提升灵魂属性
    """
    # 基础属性由 Buff action 的 atk 和 max_health 参数动态设置
    pass


class ETC_210t:
    """灵魂 / Soul"""
    tags = {
        GameTag.ATK: 1,  # 基础1攻（会被 buff 提升到实际值）
        GameTag.HEALTH: 1,  # 基础1血（会被 buff 提升到实际值）
    }

