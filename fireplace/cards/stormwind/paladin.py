# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 圣骑士
"""

from ..utils import *

class DED_500:
    """分赃专员 / Wealth Redistributor
    嘲讽 战吼：交换攻击力最高和最低的随从的攻击力。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.TAUNT: True,
    }
    
    def play(self):
        """交换攻击力最高和最低的随从的攻击力"""
        # 获取所有随从
        all_minions = list(self.game.board)
        
        if len(all_minions) >= 2:
            # 找到攻击力最高和最低的随从
            highest_atk_minion = max(all_minions, key=lambda m: m.atk)
            lowest_atk_minion = min(all_minions, key=lambda m: m.atk)
            
            # 交换攻击力
            if highest_atk_minion != lowest_atk_minion:
                high_atk = highest_atk_minion.atk
                low_atk = lowest_atk_minion.atk
                
                # 设置新的攻击力
                yield Buff(highest_atk_minion, "DED_500e_low", atk_value=low_atk - high_atk)
                yield Buff(lowest_atk_minion, "DED_500e_high", atk_value=high_atk - low_atk)


class DED_500e_low:
    """分赃专员攻击力调整（降低）"""
    def __init__(self, atk_value):
        self.atk = atk_value


class DED_500e_high:
    """分赃专员攻击力调整（提高）"""
    def __init__(self, atk_value):
        self.atk = atk_value


class DED_501:
    """金翼鹦鹉 / Sunwing Squawker
    战吼：对本随从重复施放你上一个对友方随从施放的法术。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    def play(self):
        """重复上一个对友方随从施放的法术"""
        # 获取上一个对友方随从施放的法术
        last_spell = getattr(self.controller, 'last_spell_on_friendly_minion', None)
        
        if last_spell:
            # 对自己施放该法术
            # 创建法术的副本并对自己施放
            spell_copy = self.controller.card(last_spell.id, source=self)
            spell_copy.target = self
            yield CastSpell(CONTROLLER, spell_copy)



class DED_502:
    """正义防御 / Righteous Defense
    将一个随从的攻击力和生命值设为1。将其损失的属性给予你手牌中的一个随从。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        """
        将目标随从设为1/1
        将损失的属性给予手牌中的随从
        """
        # 计算损失的属性
        atk_lost = TARGET.atk - 1
        health_lost = TARGET.health - 1
        
        # 将目标设为1/1
        yield SetTag(TARGET, {
            GameTag.ATK: 1,
            GameTag.HEALTH: 1,
        })
        
        # 如果有损失的属性，给予手牌中的随从
        if atk_lost > 0 or health_lost > 0:
            yield Find(FRIENDLY_HAND + MINION) & Buff(RANDOM(FRIENDLY_HAND + MINION), "DED_502e", 
                                                       atk_bonus=atk_lost, health_bonus=health_lost)


class DED_502e:
    """正义防御增益"""
    def __init__(self, atk_bonus, health_bonus):
        self.atk = atk_bonus
        self.max_health = health_bonus


class SW_046:
    """城建税 / City Tax
    可交易 吸血 对所有敌方随从造成$1点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.LIFESTEAL: True,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Hit(ENEMY_MINIONS, 1)

class SW_047:
    """大领主弗塔根 / Highlord Fordragon
    圣盾 在一个友方随从失去圣盾后，使你手牌中的一个随从获得+5/+5。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
        GameTag.DIVINE_SHIELD: True,
    }
    
    # 监听友方随从失去圣盾
    events = LosesDivineShield(FRIENDLY + MINION).on(
        Find(FRIENDLY_HAND + MINION) & Buff(RANDOM(FRIENDLY_HAND + MINION), "SW_047e")
    )


class SW_047e:
    """大领主弗塔根增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }


class SW_048:
    """棱彩珠宝工具 / Prismatic Jewel Kit
    在一个友方随从失去圣盾后，使你手牌中的随从获得+1/+1。失去1点耐久度。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 4,
        GameTag.COST: 3,
    }
    
    # 监听友方随从失去圣盾
    events = LosesDivineShield(FRIENDLY + MINION).on(
        (Buff(FRIENDLY_HAND + MINION, "SW_048e"), Hit(SELF, 1))
    )


class SW_048e:
    """棱彩珠宝工具增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_049:
    """受祝福的货物 / Blessed Goods
    发现一张奥秘、武器或圣盾随从。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    def play(self):
        """发现一张奥秘、武器或圣盾随从"""
        # 创建选项池：奥秘、武器、圣盾随从
        options = []
        
        # 添加奥秘
        secrets = RandomCollectible(type=CardType.SPELL, secret=True)
        options.append(secrets)
        
        # 添加武器
        weapons = RandomCollectible(type=CardType.WEAPON)
        options.append(weapons)
        
        # 添加圣盾随从
        divine_shield_minions = RandomCollectible(type=CardType.MINION, divine_shield=True)
        options.append(divine_shield_minions)
        
        # 发现
        yield Discover(CONTROLLER, options)


class SW_305:
    """乌瑞恩首席剑士 / First Blade of Wrynn
    圣盾 战吼：如果本随从的攻击力至少为4点，获得突袭。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.DIVINE_SHIELD: True,
    }
    
    def play(self):
        """如果攻击力>=4，获得突袭"""
        if self.atk >= 4:
            yield SetTags(SELF, {GameTag.RUSH: True})


class SW_313:
    """挺身而出 / Rise to the Occasion
    任务线：打出3张不同的1费牌。奖励：装备一把1/4的光明正义。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段打出3张不同的1费牌
    questline_requirements = [3, 3, 3]
    
    def play(self):
        """打出任务线"""
        from ...enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_313e")
    
    def questline_reward_1(self):
        """阶段1奖励：装备1/4光明正义"""
        return [Equip(CONTROLLER, "SW_313t")]
    
    def questline_reward_2(self):
        """阶段2奖励：装备2/4光明正义"""
        return [Equip(CONTROLLER, "SW_313t2")]
    
    def questline_reward_3(self):
        """阶段3奖励：装备3/4光明正义"""
        return [Equip(CONTROLLER, "SW_313t3")]


class SW_313e:
    """挺身而出追踪器"""
    def apply(self, target):
        """初始化追踪器"""
        if not hasattr(target, 'sw_313_one_cost_cards_played'):
            target.sw_313_one_cost_cards_played = set()
    
    # 监听打出1费牌
    # Play().after() 传递参数: player, played_card, target
    events = Play(CONTROLLER).after(
        lambda self, player, played_card, target: (
            # 记录打出的1费牌(如果是1费)
            self.controller.sw_313_one_cost_cards_played.add(played_card.id) if played_card.cost == 1 else None,
            # 检查是否达到3张不同的1费牌
            (
                Find(FRIENDLY_SECRETS + ID("SW_313")) &
                QuestlineProgress(FRIENDLY_SECRETS + ID("SW_313"), 3)
            ) if len(getattr(self.controller, 'sw_313_one_cost_cards_played', set())) >= 3 else None
        ) or []
    )


class SW_313t:
    """光明正义 / Light's Justice"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 1,
        GameTag.DURABILITY: 4,
        GameTag.COST: 1,
    }


class SW_313t2:
    """光明正义（强化）"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 4,
        GameTag.COST: 1,
    }


class SW_313t3:
    """光明正义（完全强化）"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 4,
        GameTag.COST: 1,
    }


class SW_314:
    """光明使者之锤 / Lightbringer's Hammer
    吸血 不能攻击英雄。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 2,
        GameTag.COST: 3,
        GameTag.LIFESTEAL: True,
        GameTag.CANNOT_ATTACK_HEROES: True,
    }


class SW_315:
    """联盟旗手 / Alliance Bannerman
    战吼：抽一张随从牌。使你手牌中的随从获得+1/+1。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    play = (ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION), Buff(FRIENDLY_HAND + MINION, "SW_315e"))


class SW_315e:
    """联盟旗手增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_316:
    """神圣坐骑 / Noble Mount
    使一个随从获得+1/+1和圣盾。当其死亡时，召唤一匹战马。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    play = Buff(TARGET, "SW_316e")


class SW_316e:
    """神圣坐骑增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.DIVINE_SHIELD: True,
    }
    
    # 死亡时召唤战马
    deathrattle = Summon(CONTROLLER, "SW_316t")


class SW_316t:
    """战马 / Warhorse"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


class SW_317:
    """古墓卫士 / Catacomb Guard
    吸血 战吼：对一个敌方随从造成等同于本随从攻击力的伤害。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
        GameTag.LIFESTEAL: True,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    play = Hit(TARGET, ATK(SELF))

