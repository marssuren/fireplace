# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 术士
"""

from ..utils import *

class DED_503:
    """暗影之刃飞刀手 / Shadowblade Slinger
    战吼：如果你在本回合受到过伤害，对一个敌方随从造成等量的伤害。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        """如果本回合受到过伤害，造成等量伤害"""
        # 使用本回合受到的伤害
        damage_taken = getattr(self.controller, 'damage_taken_this_turn', 0)
        if damage_taken > 0 and TARGET:
            yield Hit(TARGET, damage_taken)


class DED_504:
    """邪恶船运 / Wicked Shipment
    可交易 召唤两个1/1的小鬼。（交易时升级2点！）"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        """召唤小鬼，数量取决于升级次数"""
        # 检查升级次数
        upgrade_level = 0
        for buff in self.buffs:
            if buff.id == "DED_504e":
                upgrade_level += 1
        
        # 基础2个，每次升级+2
        imp_count = 2 + (upgrade_level * 2)
        
        for _ in range(imp_count):
            yield Summon(CONTROLLER, "DED_504t")
    
    # 交易后升级
    trade = Buff(SELF, "DED_504e")


class DED_504e:
    """邪恶船运升级标记"""
    pass


class DED_504t:
    """小鬼 / Imp"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.DEMON,
    }


class DED_505:
    """碎舰恶魔 / Hullbreaker
    战吼和亡语：抽一张法术牌。你的英雄受到等同于其法力值消耗的伤害。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 4,
    }
    
    def play(self):
        """抽法术并受伤"""
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
        if drawn:
            yield Hit(FRIENDLY_HERO, drawn.cost)
    
    def deathrattle(self):
        """抽法术并受伤"""
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
        if drawn:
            yield Hit(FRIENDLY_HERO, drawn.cost)


class SW_003:
    """符文秘银杖 / Runed Mithril Rod
    在你抽4张牌后，使你手牌中的牌的法力值消耗减少（1）点。失去1点耐久度。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 3,
        GameTag.COST: 3,
    }
    
    def play(self):
        """装备时添加追踪器"""
        yield Buff(SELF, "SW_003e")


class SW_003e:
    """符文秘银杖追踪器"""
    def apply(self, target):
        """初始化抽牌计数"""
        if not hasattr(target, 'sw_003_cards_drawn'):
            target.sw_003_cards_drawn = 0
    
    # 监听抽牌
    events = Draw(CONTROLLER).after(
        lambda self: self._on_draw()
    )
    
    def _on_draw(self):
        """抽牌时增加计数"""
        # 增加计数
        self.owner.sw_003_cards_drawn += 1
        
        # 检查是否达到4张
        if self.owner.sw_003_cards_drawn >= 4:
            # 重置计数
            self.owner.sw_003_cards_drawn = 0
            
            # 减少手牌费用
            yield Buff(FRIENDLY_HAND, "SW_003_cost")
            
            # 失去1点耐久度
            yield Hit(self.owner, 1)


class SW_003_cost:
    """符文秘银杖减费"""
    cost = -1


class SW_084:
    """血缚小鬼 / Bloodbound Imp
    每当本随从攻击时，对你的英雄造成2点伤害。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 5,
        GameTag.COST: 2,
    }
    
    events = Attack(SELF).on(Hit(FRIENDLY_HERO, 2))


class SW_085:
    """暗巷契约 / Dark Alley Pact
    召唤一个恶魔，其属性等同于你的手牌数量，并具有嘲讽。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        """召唤恶魔，属性=手牌数"""
        hand_size = len(self.controller.hand)
        minion = yield Summon(CONTROLLER, "SW_085t")
        if minion:
            yield SetTag(minion, {
                GameTag.ATK: hand_size,
                GameTag.HEALTH: hand_size,
            })


class SW_085t:
    """恶魔 / Fiend"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 3,
        GameTag.CARDRACE: Race.DEMON,
        GameTag.TAUNT: True,
    }


class SW_086:
    """阴暗的酒保 / Shady Bartender
    可交易 战吼：使你的恶魔获得+2/+2。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
    }
    
    play = Buff(FRIENDLY_MINIONS + DEMON, "SW_086e")


class SW_086e:
    """阴暗的酒保增益"""
    atk = 2
    max_health = 2


class SW_087:
    """恐惧坐骑 / Dreaded Mount
    使一个随从获得+1/+1。当其死亡时，召唤一匹无尽的恐惧战马。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    play = Buff(TARGET, "SW_087e")


class SW_087e:
    """恐惧坐骑增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }
    deathrattle = Summon(CONTROLLER, "SW_087t")


class SW_087t:
    """恐惧战马 / Dreadsteed"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 4,
        GameTag.CARDRACE: Race.DEMON,
    }
    # 无尽：死亡时召唤自己
    deathrattle = Summon(CONTROLLER, "SW_087t")


class SW_088:
    """恶魔来袭 / Demonic Assault
    造成$3点伤害。召唤两个1/3并具有嘲讽的虚空行者。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    play = (Hit(TARGET, 3), Summon(CONTROLLER, "SW_088t") * 2)


class SW_088t:
    """虚空行者 / Voidwalker"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 1,
        GameTag.CARDRACE: Race.DEMON,
        GameTag.TAUNT: True,
    }


class SW_089:
    """资深顾客 / Entitled Customer
    战吼：对所有其他随从造成等同于你手牌数量的伤害。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    
    def play(self):
        """对所有其他随从造成伤害"""
        hand_size = len(self.controller.hand)
        yield Hit(ALL_MINIONS - SELF, hand_size)


class SW_090:
    """纳斯雷兹姆之触 / Touch of the Nathrezim
    对一个随从造成$2点伤害。如果它死亡，为你的英雄恢复3点生命值。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        """造成伤害，如果目标死亡则恢复生命"""
        target = TARGET
        target_health_before = target.health
        
        yield Hit(TARGET, 2)
        
        # 检查目标是否死亡
        if target.zone == Zone.GRAVEYARD or target.health <= 0:
            yield Heal(FRIENDLY_HERO, 3)


class SW_091:
    """恶魔之种 / The Demon Seed
    任务线：在你的回合受到12点伤害。奖励：吸血。对敌方英雄造成$3点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段在自己回合受到特定伤害
    questline_requirements = [6, 7, 8]  # 阶段1: 6点，阶段2: 7点，阶段3: 8点
    
    def play(self):
        """打出任务线"""
        from ..enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_091e")
    
    def questline_reward_1(self):
        """阶段1奖励：吸血，造成3点伤害"""
        return [
            Buff(FRIENDLY_HERO, "SW_091_lifesteal"),
            Hit(ENEMY_HERO, 3)
        ]
    
    def questline_reward_2(self):
        """阶段2奖励：吸血，造成3点伤害"""
        return [
            Buff(FRIENDLY_HERO, "SW_091_lifesteal"),
            Hit(ENEMY_HERO, 3)
        ]
    
    def questline_reward_3(self):
        """阶段3奖励：吸血，造成3点伤害，替换英雄技能"""
        # 替换英雄技能
        controller = self.controller
        
        # 保存原始英雄技能
        if not hasattr(controller, 'original_hero_power'):
            controller.original_hero_power = controller.hero.power
        
        # 创建新的英雄技能
        new_power = controller.card("SW_091t", source=controller.hero)
        controller.hero.power = new_power
        new_power.controller = controller
        new_power.zone = Zone.PLAY
        
        return [
            Buff(FRIENDLY_HERO, "SW_091_lifesteal"),
            Hit(ENEMY_HERO, 3),
        ]


class SW_091e:
    """恶魔之种追踪器"""
    def apply(self, target):
        """初始化追踪"""
        if not hasattr(target, 'sw_091_damage_this_turn'):
            target.sw_091_damage_this_turn = 0
    
    # 监听回合开始，重置计数
    events_turn_start = OWN_TURN_BEGIN.on(
        lambda self: setattr(self.controller, 'sw_091_damage_this_turn', 0)
    )
    
    # 监听受到伤害（使用已有的 damage_taken_this_turn）
    events_turn_end = OWN_TURN_END.on(
        lambda self: self._check_damage()
    )
    
    def _check_damage(self):
        """回合结束时检查受到的伤害"""
        damage = getattr(self.controller, 'damage_taken_this_turn', 0)
        
        # 获取当前任务线阶段
        quest = None
        for secret in self.controller.secrets:
            if secret.id == "SW_091":
                quest = secret
                break
        
        if quest and damage > 0:
            # 增加任务线进度
            current_stage = quest.tags.get(QUESTLINE_STAGE, 1)
            required_damage = [6, 7, 8][current_stage - 1] if current_stage <= 3 else 0
            
            if damage >= required_damage:
                yield QuestlineProgress(quest, required_damage)


class SW_091_lifesteal:
    """恶魔之种吸血"""
    # 给英雄添加吸血光环
    # 所有造成的伤害都会恢复生命
    events = Damage(ALL_CHARACTERS).after(
        lambda self: Heal(FRIENDLY_HERO, Damage.AMOUNT) 
        if Damage.SOURCE.controller == self.controller else None
    )


class SW_091t:
    """完成仪式 / Complete the Ritual"""
    tags = {
        GameTag.CARDTYPE: CardType.HERO_POWER,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    # 对目标造成5点伤害
    activate = Hit(TARGET, 5)


class SW_092:
    """安纳塞隆 / Anetheron
    如果你的手牌已满，法力值消耗为（1）点。"""
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 6,
        GameTag.COST: 8,
        GameTag.CARDRACE: Race.DEMON,
    }
    
    @property
    def cost(self):
        """如果手牌已满，费用为1"""
        if hasattr(self, 'controller') and len(self.controller.hand) >= 10:
            return 1
        return 8
