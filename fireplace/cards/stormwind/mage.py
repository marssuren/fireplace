# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 法师
"""

from ..utils import *

class DED_515:
    """灰贤鹦鹉 / Grey Sage Parrot
    战吼：重复施放你上一个施放的法力值消耗大于或等于（6）点的法术。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.COST: 6,
    }
    
    def play(self):
        """
        重复施放上一个6费以上的法术
        
        需要追踪施放过的法术
        """
        # 从施放过的法术中找到最后一个6费以上的
        expensive_spells = [
            card for card in self.controller.cards_played_this_game
            if card.type == CardType.SPELL and card.cost >= 6
        ]
        
        if expensive_spells:
            last_expensive_spell = expensive_spells[-1]
            # 重新施放该法术
            yield CastSpell(CONTROLLER, Copy(last_expensive_spell))

class DED_516:
    """深水唤醒师 / Deepwater Evoker
    战吼：抽一张法术牌。获得等同于其法力值消耗的护甲值。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    def play(self):
        """
        抽一张法术牌
        获得等于其费用的护甲值
        """
        # 从牌库中找到一张法术牌
        spell_cards = [c for c in self.controller.deck if c.type == CardType.SPELL]
        
        if spell_cards:
            # 抽第一张法术牌
            card = spell_cards[0]
            yield Draw(CONTROLLER, card)
            
            # 获得等于其费用的护甲值
            armor_amount = card.cost
            if armor_amount > 0:
                yield GainArmor(FRIENDLY_HERO, armor_amount)



class DED_517:
    """奥术溢爆 / Arcane Overflow
    对一个敌方随从造成$8点伤害。召唤一个属性等同于超量伤害的残影。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        """
        造成8点伤害
        召唤一个属性等于超量伤害的残影
        """
        # 造成8点伤害并获取超量伤害
        excess_damage = yield HitExcessDamage(TARGET, 8)
        
        # 如果有超量伤害，召唤残影
        if excess_damage > 0:
            # 召唤残影
            yield Summon(CONTROLLER, "DED_517t")
            # 给残影设置属性
            # CARD 是召唤的残影
            yield Buff(CARD, "DED_517e", atk=excess_damage, max_health=excess_damage)


class DED_517t:
    """残影"""
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 0,
        GameTag.COST: 0,
    }


class DED_517e:
    """奥术溢爆增益"""
    # 动态设置攻击力和生命值
    pass


class SW_001:
    """星空墨水套装 / Celestial Ink Set
    在你的法术牌上花费5点法力值后，使你手牌中的一张法术牌法力值消耗减少（5）点。失去1点耐久度。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 1,
        GameTag.DURABILITY: 3,
        GameTag.COST: 2,
    }
    
    def apply(self, target):
        """初始化法力值计数器"""
        if not hasattr(target, 'sw_001_mana_spent_on_spells'):
            target.sw_001_mana_spent_on_spells = 0
    
    # 监听施放法术
    events = CastSpell(CONTROLLER, SPELL).after(
        lambda self: [
            # 增加花费的法力值
            setattr(self.controller, 'sw_001_mana_spent_on_spells',
                   self.controller.sw_001_mana_spent_on_spells + CastSpell.CARD.cost),
            # 如果达到5点，触发效果
            (
                Find(FRIENDLY_HAND + SPELL) &
                Buff(RANDOM(FRIENDLY_HAND + SPELL), "SW_001e") &
                Hit(SELF, 1) &  # 失去1点耐久度
                # 重置计数
                setattr(self.controller, 'sw_001_mana_spent_on_spells', 0)
            ) if self.controller.sw_001_mana_spent_on_spells >= 5 else None
        ]
    )


class SW_001e:
    """星空墨水套装减费"""
    cost = -5


class SW_107:
    """火热促销 / Fire Sale
    可交易 对所有随从造成$3点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Hit(ALL_MINIONS, 3)


class SW_108:
    """初始之火 / First Flame
    对一个随从造成$2点伤害。将一张次级之火置入你的手牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    play = (Hit(TARGET, 2), Give(CONTROLLER, "SW_108t"))


class SW_108t:
    """次级之火 / Second Flame"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    play = Hit(TARGET, 3)


class SW_109:
    """笨拙的信使 / Clumsy Courier
    战吼：施放你手牌中法力值消耗最高的法术。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
    }
    
    def play(self):
        """
        施放手牌中费用最高的法术
        """
        # 找到手牌中的所有法术
        hand_spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        
        if hand_spells:
            # 找到费用最高的法术
            highest_cost_spell = max(hand_spells, key=lambda x: x.cost)
            # 施放它
            yield CastSpell(CONTROLLER, highest_cost_spell)


class SW_110:
    """点燃 / Ignite
    造成$2点伤害。将一张点燃洗入你的牌库，其伤害+1。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.FIRE,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        """
        造成伤害（默认2点，或当前存储的伤害值）
        洗入一张伤害+1的点燃
        """
        # 获取当前伤害值（从buff中读取，默认2点）
        current_damage = 2
        for buff in self.buffs:
            if hasattr(buff, 'ignite_damage'):
                current_damage = buff.ignite_damage
                break
        
        # 造成当前伤害
        yield Hit(TARGET, current_damage)
        
        # 创建一张新的点燃并洗入牌库
        yield Shuffle(CONTROLLER, "SW_110")
        
        # 给洗入的点燃添加伤害buff（伤害+1）
        # 需要找到刚洗入的卡牌
        # 使用一个特殊的buff来存储伤害值
        new_damage = current_damage + 1
        
        # 给牌库中最后一张点燃添加伤害buff
        for card in reversed(self.controller.deck):
            if card.id == "SW_110":
                # 创建并应用伤害buff
                buff = self.controller.card("SW_110e", source=self)
                buff.ignite_damage = new_damage
                buff.apply(card)
                break


class SW_110e:
    """点燃伤害存储"""
    # 用于存储递增的伤害值
    # ignite_damage 属性会在运行时设置
    pass



class SW_111:
    """圣殿蜡烛商 / Sanctum Chandler
    在你施放火焰法术后，抽一张法术牌。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    # 监听施放火焰法术
    events = CastSpell(CONTROLLER, SPELL + FIRE).after(
        ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
    )


class SW_112:
    """普瑞斯托的炎术师 / Prestor's Pyromancer
    战吼：你的下一个火焰法术获得法术伤害+2。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 3,
    }
    
    play = Buff(CONTROLLER, "SW_112e")


class SW_112e:
    """普瑞斯托的炎术师效果"""
    # 下一个火焰法术获得法术伤害+2
    # 使用法术学派伤害加成机制（核心扩展）
    
    def apply(self, target):
        """设置火焰法术伤害加成"""
        # 设置法术学派伤害加成字典
        self.spell_school_damage_bonus = {
            SpellSchool.FIRE: 2  # 火焰法术+2伤害
        }
    
    # 监听施放火焰法术后移除
    events = CastSpell(CONTROLLER, SPELL + FIRE).after(
        Destroy(SELF)
    )



class SW_113:
    """首席法师安东尼达斯 / Grand Magus Antonidas
    战吼：如果你在过去三个回合都施放过火焰法术，则对随机敌人施放3个火球术。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 7,
        GameTag.COST: 7,
    }
    
    def play(self):
        """
        检查过去三个回合是否每个回合都施放过火焰法术
        如果是，施放3个火球术
        """
        current_turn = self.game.turn
        
        # 检查过去三个回合（当前回合和之前两个回合）
        turns_to_check = [current_turn, current_turn - 1, current_turn - 2]
        
        # 检查每个回合是否都施放过火焰法术
        all_turns_have_fire_spell = True
        for turn in turns_to_check:
            if turn < 1:  # 游戏开始前的回合
                all_turns_have_fire_spell = False
                break
            
            # 获取该回合施放的法术
            spells_in_turn = self.controller.spells_by_turn.get(turn, [])
            
            # 检查是否有火焰法术
            has_fire_spell = any(
                spell.spell_school == SpellSchool.FIRE
                for spell in spells_in_turn
            )
            
            if not has_fire_spell:
                all_turns_have_fire_spell = False
                break
        
        # 如果过去三个回合都有火焰法术，施放3个火球术
        if all_turns_have_fire_spell:
            for _ in range(3):
                enemies = self.game.opponent.characters
                if enemies:
                    target = self.game.random.choice(enemies)
                    yield Hit(target, 6)  # 火球术造成6点伤害


class SW_450:
    """巫师的计策 / Sorcerer's Gambit
    任务线：施放一个火焰、冰霜和奥术法术。奖励：抽一张法术牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段施放火焰、冰霜、奥术各一个
    questline_requirements = [3, 3, 3]
    
    def play(self):
        """打出任务线"""
        from ...enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_450e")
    
    def questline_reward_1(self):
        """阶段1奖励：抽一张法术牌"""
        return [ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)]
    
    def questline_reward_2(self):
        """阶段2奖励：抽一张法术牌"""
        return [ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)]
    
    def questline_reward_3(self):
        """阶段3奖励：抽一张法术牌"""
        return [ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)]


class SW_450e:
    """巫师的计策追踪器"""
    def apply(self, target):
        """初始化追踪器"""
        if not hasattr(target, 'sw_450_schools_this_stage'):
            target.sw_450_schools_this_stage = set()
    
    # 监听施放法术
    events = CastSpell(CONTROLLER, SPELL).after(
        lambda self: [
            # 记录施放的法术学派
            self.controller.sw_450_schools_this_stage.add(CastSpell.CARD.spell_school)
            if CastSpell.CARD.spell_school in [SpellSchool.FIRE, SpellSchool.FROST, SpellSchool.ARCANE]
            else None,
            # 检查是否完成（火焰、冰霜、奥术各一个）
            (
                Find(FRIENDLY_SECRETS + ID("SW_450")) &
                QuestlineProgress(FRIENDLY_SECRETS + ID("SW_450"), 3) &
                # 重置学派追踪
                setattr(self.controller, 'sw_450_schools_this_stage', set())
            ) if len(self.controller.sw_450_schools_this_stage) >= 3 else None
        ]
    )


class SW_462:
    """炽热连击 / Hot Streak
    你在本回合的下一个火焰法术法力值消耗减少（2）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    play = Buff(CONTROLLER, "SW_462e")


class SW_462e:
    """炽热连击效果"""
    # 下一个火焰法术减2费
    # 给手牌中的火焰法术减费
    events = [
        # 给手牌中的火焰法术减费
        lambda self: Buff(FRIENDLY_HAND + SPELL + FIRE, "SW_462_cost"),
        # 监听施放火焰法术后移除
        CastSpell(CONTROLLER, SPELL + FIRE).on(Destroy(SELF)),
        # 回合结束时移除
        OWN_TURN_END.on(Destroy(SELF)),
    ]


class SW_462_cost:
    """炽热连击减费"""
    cost = -2

