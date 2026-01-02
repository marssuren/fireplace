# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 牧师
"""

from ..utils import *

class DED_512:
    """不朽护符 / Amulet of Undying
    可交易 复活1个友方亡语随从。（交易时升级！）"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    
    def play(self):
        """复活亡语随从，数量取决于升级次数"""
        # 检查升级次数
        upgrade_level = 0
        for buff in self.buffs:
            if buff.id == "DED_512e":
                upgrade_level += 1
        
        # 复活数量：基础1个，每次升级+1
        resurrect_count = 1 + upgrade_level
        
        # 从墓地中找到亡语随从
        deathrattle_minions = [
            minion for minion in self.controller.graveyard
            if minion.type == CardType.MINION and hasattr(minion, 'deathrattle')
        ]
        
        if deathrattle_minions:
            # 复活最后N个死亡的亡语随从
            targets = deathrattle_minions[-resurrect_count:]
            for target in targets:
                yield Summon(CONTROLLER, Copy(target))
    
    # 交易后升级
    trade = Buff(SELF, "DED_512e")


class DED_512e:
    """不朽护符升级标记"""
    # 每次交易添加一个标记，用于计数升级次数
    pass


class DED_513:
    """迪菲亚麻风侏儒 / Defias Leper
    战吼：如果你手牌中有暗影法术，造成2点伤害。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    
    def play(self):
        """如果手牌中有暗影法术，造成2点伤害"""
        # 检查手牌中是否有暗影法术
        has_shadow_spell = any(
            card.type == CardType.SPELL and card.spell_school == SpellSchool.SHADOW
            for card in self.controller.hand
        )
        
        if has_shadow_spell and TARGET:
            yield Hit(TARGET, 2)


class DED_514:
    """仿冒猫猫 / Copycat
    战吼：将你对手打出的下一张牌的复制置入你的手牌。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    play = Buff(CONTROLLER, "DED_514e")


class DED_514e:
    """仿冒猫猫效果"""
    # 监听对手打出卡牌
    events = Play(OPPONENT).on(
        Give(CONTROLLER, Copy(Play.CARD)) & Destroy(SELF)
    )


class SW_012:
    """暗影布缝针 / Shadowcloth Needle
    在你施放暗影法术后，对所有敌人造成1点伤害。失去1点耐久度。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 3,
        GameTag.COST: 2,
    }
    
    # 监听施放暗影法术
    events = CastSpell(CONTROLLER, SPELL + SHADOW).after(
        Hit(ENEMY_CHARACTERS, 1) & Hit(SELF, 1)
    )


class SW_433:
    """寻求指引 / Seek Guidance
    任务线：打出一张2费、3费和4费牌。奖励：从你的牌库中发现一张牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段打出2费、3费、4费牌
    questline_requirements = [3, 3, 3]
    
    def play(self):
        """打出任务线"""
        from ..enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_433e")
    
    def questline_reward_1(self):
        """阶段1奖励：从牌库中发现一张牌"""
        return [GenericChoice(CONTROLLER, Discover(CONTROLLER, FRIENDLY_DECK))]
    
    def questline_reward_2(self):
        """阶段2奖励：从牌库中发现一张牌"""
        return [GenericChoice(CONTROLLER, Discover(CONTROLLER, FRIENDLY_DECK))]
    
    def questline_reward_3(self):
        """阶段3奖励：从牌库中发现一张牌"""
        return [GenericChoice(CONTROLLER, Discover(CONTROLLER, FRIENDLY_DECK))]


class SW_433e:
    """寻求指引追踪器"""
    def apply(self, target):
        """初始化追踪器"""
        if not hasattr(target, 'sw_433_costs_played'):
            target.sw_433_costs_played = set()
    
    # 监听打出2/3/4费牌
    events = Play(CONTROLLER).after(
        lambda self: [
            # 记录打出的费用
            self.controller.sw_433_costs_played.add(Play.CARD.cost)
            if Play.CARD.cost in [2, 3, 4] else None,
            # 检查是否完成（2费、3费、4费各一张）
            (
                Find(FRIENDLY_SECRETS + ID("SW_433")) &
                QuestlineProgress(FRIENDLY_SECRETS + ID("SW_433"), 3) &
                # 重置计数
                setattr(self.controller, 'sw_433_costs_played', set())
            ) if len(self.controller.sw_433_costs_played) >= 3 else None
        ]
    )


class SW_440:
    """墓园召唤 / Call of the Grave
    发现一张亡语随从牌。如果你有足够的法力值来使用它，触发其亡语。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        """发现亡语随从，如果有足够法力则触发亡语"""
        # 发现亡语随从
        discovered = yield GenericChoice(CONTROLLER, 
                                        Discover(CONTROLLER, RandomCollectible(deathrattle=True)))
        
        if discovered and self.controller.mana >= discovered.cost:
            # 有足够法力，触发亡语
            if hasattr(discovered, 'deathrattle'):
                # 执行亡语效果
                yield discovered.deathrattle


class SW_441:
    """纳鲁碎片 / Shard of the Naaru
    可交易 沉默所有敌方随从。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Silence(ENEMY_MINIONS)


class SW_442:
    """虚空碎片 / Void Shard
    吸血 造成$4点伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.LIFESTEAL: True,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    play = Hit(TARGET, 4)


class SW_443:
    """雷象坐骑 / Elekk Mount
    使一个随从获得+4/+7和嘲讽。当其死亡时，召唤一头雷象。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    play = Buff(TARGET, "SW_443e")


class SW_443e:
    """雷象坐骑增益"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 7,
        GameTag.TAUNT: True,
    }
    deathrattle = Summon(CONTROLLER, "SW_443t")


class SW_443t:
    """雷象 / Elekk"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 7,
        GameTag.COST: 7,
        GameTag.RACE: Race.BEAST,
    }


class SW_444:
    """暮光欺诈者 / Twilight Deceptor
    战吼：如果本回合有任意英雄受到过伤害，抽一张暗影法术牌。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    
    def play(self):
        """如果本回合有英雄受伤，抽暗影法术"""
        # 简化实现：检查英雄生命值是否低于最大值
        if (self.controller.hero.damage > 0 or 
            self.controller.opponent.hero.damage > 0):
            yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL + SHADOW)


class SW_445:
    """灵能魔 / Psyfiend
    在你施放暗影法术后，对双方英雄造成2点伤害。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 1,
        GameTag.COST: 2,
    }
    
    events = CastSpell(CONTROLLER, SPELL + SHADOW).after(
        Hit(ALL_HEROES, 2)
    )


class SW_446:
    """虚触侍从 / Voidtouched Attendant
    双方英雄受到的所有伤害+1。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    # 监听对英雄的伤害，增加1点额外伤害
    # 使用 Damage 事件的 after 钩子来追加伤害
    events = Damage(ALL_HEROES).after(
        lambda self: Hit(Damage.TARGET, 1) if Damage.TARGET.type == CardType.HERO else None
    )


class SW_448:
    """黑暗主教本尼迪塔斯 / Darkbishop Benedictus
    游戏开始时：如果你牌库中的法术全是暗影法术，进入暗影形态。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 6,
        GameTag.COST: 7,
    }
    
    # 游戏开始时检查
    # 使用 mulligan 阶段后的事件
    def play(self):
        """打出时检查是否应该进入暗影形态"""
        # 检查牌库中的法术是否全是暗影法术
        deck_spells = [
            card for card in self.controller.deck
            if card.type == CardType.SPELL
        ]
        
        if deck_spells:
            all_shadow = all(
                card.spell_school == SpellSchool.SHADOW
                for card in deck_spells
            )
            
            if all_shadow:
                # 进入暗影形态
                yield Buff(FRIENDLY_HERO, "SW_448e")


class SW_448e:
    """暗影形态"""
    # 暗影形态效果：英雄技能变为"造成2点伤害"
    
    def apply(self, target):
        """进入暗影形态，替换英雄技能"""
        # 保存原始英雄技能
        if not hasattr(target, 'original_hero_power'):
            target.original_hero_power = target.hero.power
        
        # 替换为暗影形态技能
        # 创建新的英雄技能
        shadowform_power = target.card("SW_448t", source=target.hero)
        target.hero.power = shadowform_power
        shadowform_power.controller = target
        shadowform_power.zone = Zone.PLAY
    
    def destroy(self):
        """离开暗影形态，恢复原技能"""
        target = self.owner
        if hasattr(target, 'original_hero_power'):
            target.hero.power = target.original_hero_power
            delattr(target, 'original_hero_power')


class SW_448t:
    """暗影形态技能 / Shadowform Hero Power"""
    tags = {
        GameTag.CARDTYPE: CardType.HERO_POWER,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    # 造成2点伤害
    activate = Hit(TARGET, 2)


