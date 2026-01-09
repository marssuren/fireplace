# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 战士
"""

from ..utils import *

class DED_518:
    """操纵火炮 / Man the Cannons
    对一个随从造成$3点伤害，并对所有其他随从造成$1点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    play = (Hit(TARGET, 3), Hit(ALL_MINIONS - TARGET, 1))


class DED_519:
    """迪菲亚炮手 / Defias Cannoneer
    在你的英雄攻击后，随机对一个敌人造成2点伤害，共两次。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    events = Attack(FRIENDLY_HERO).after(
        Hit(RANDOM_ENEMY_CHARACTER, 2) * 2
    )


class DED_527:
    """铁匠锤 / Blacksmithing Hammer
    可交易 在你交易此牌后，获得+2点耐久度。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 2,
        GameTag.COST: 2,
    }
    
    # 交易后增加耐久度
    trade = Buff(SELF, "DED_527e")


class DED_527e:
    """铁匠锤耐久度增益"""
    durability = 2


class SW_021:
    """怯懦的步兵 / Cowardly Grunt
    亡语：从你的牌库中召唤一个随从。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    deathrattle = Summon(CONTROLLER, Random(FRIENDLY_DECK + MINION))


class SW_023:
    """挑衅 / Provoke
    可交易 选择一个友方随从。敌方随从攻击它。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    # 给予嘲讽（强制敌方随从攻击它）
    play = SetTag(TARGET, {GameTag.TAUNT: True})


class SW_024:
    """洛萨 / Lothar
    在你的回合结束时，攻击一个随机敌方随从。如果它死亡，获得+3/+3。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
    }
    
    # 回合结束时自动攻击
    events = OWN_TURN_END.on(
        lambda self: self._auto_attack()
    )
    
    def _auto_attack(self):
        """自动攻击随机敌方随从"""
        # 获取所有敌方随从
        enemy_minions = [m for m in self.controller.opponent.field]
        
        if enemy_minions and self.zone == Zone.PLAY:
            # 随机选择一个目标
            import random
            target = random.choice(enemy_minions)
            
            # 记录目标的生命值
            target_health_before = target.health
            
            # 执行攻击
            yield Attack(self, target)
            
            # 检查目标是否死亡
            if target.zone == Zone.GRAVEYARD or target.health <= 0:
                # 获得+3/+3
                yield Buff(SELF, "SW_024e")


class SW_024e:
    """洛萨增益"""
    atk = 3
    max_health = 3


class SW_027:
    """海上威胁 / Shiver Their Timbers!
    对一个随从造成$2点伤害。如果你控制一个海盗，改为造成$5点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        """根据是否有海盗造成不同伤害"""
        has_pirate = any(m.race == Race.PIRATE for m in self.controller.field)
        damage = 5 if has_pirate else 2
        yield Hit(TARGET, damage)


class SW_028:
    """开进码头 / Raid the Docks
    任务线：打出3个海盗。奖励：抽一把武器。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    questline_requirements = [3, 3, 3]
    
    def play(self):
        """打出任务线"""
        from ..enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_028e")
    
    def questline_reward_1(self):
        """阶段1奖励：抽一把武器"""
        return [ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)]
    
    def questline_reward_2(self):
        """阶段2奖励：抽一把武器"""
        return [ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)]
    
    def questline_reward_3(self):
        """阶段3奖励：抽一把武器"""
        return [ForceDraw(CONTROLLER, FRIENDLY_DECK + WEAPON)]


class SW_028e:
    """开进码头追踪器"""
    # 监听打出海盗
    events = Play(CONTROLLER, MINION + PIRATE).after(
        Find(FRIENDLY_SECRETS + ID("SW_028")) &
        QuestlineProgress(FRIENDLY_SECRETS + ID("SW_028"), 3)
    )


class SW_029:
    """港口匪徒 / Harbor Scamp
    战吼：抽一张海盗牌。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + PIRATE)


class SW_030:
    """货物保镖 / Cargo Guard
    在你的回合结束时，获得3点护甲值。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 3,
    }
    
    events = OWN_TURN_END.on(GainArmor(FRIENDLY_HERO, 3))


class SW_093:
    """暴风城海盗 / Stormwind Freebooter
    战吼：在本回合中，使你的英雄获得+2攻击力。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.PIRATE,
    }
    
    play = Buff(FRIENDLY_HERO, "SW_093e")


class SW_093e:
    """暴风城海盗增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.ONE_TURN_EFFECT: True,
    }


class SW_094:
    """厚重板甲 / Heavy Plate
    可交易 获得8点护甲值。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    play = GainArmor(FRIENDLY_HERO, 8)


class SW_097:
    """遥控傀儡 / Remote-Controlled Golem
    在本随从受到伤害后，将两个傀儡零件洗入你的牌库。抽到时，召唤一个2/1的机械。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    
    events = Damage(SELF).after(
        Shuffle(CONTROLLER, "SW_097t") * 2
    )


class SW_097t:
    """傀儡零件 / Golem Part"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    # 抽到时召唤2/1机械
    draw = Summon(CONTROLLER, "SW_097t2")


class SW_097t2:
    """傀儡 / Golem"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.MECHANICAL,
    }
