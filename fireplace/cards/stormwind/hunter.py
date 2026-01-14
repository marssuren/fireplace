# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 猎人
"""

from ..utils import *

class DED_007:
    """迪菲亚炸鱼手 / Defias Blastfisher
    战吼：对一个随机敌人造成2点伤害。每有一个友方野兽，重复一次。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    def play(self):
        """
        对随机敌人造成2点伤害
        每有一个友方野兽，重复一次
        """
        # 统计友方野兽数量
        beast_count = len([m for m in self.controller.field if m.race == Race.BEAST])
        
        # 重复 (1 + 野兽数量) 次
        for _ in range(1 + beast_count):
            enemies = self.controller.opponent.characters
            if enemies:
                target = self.game.random.choice(enemies)
                yield Hit(target, 2)


class DED_008:
    """巨型鹦鹉 / Monstrous Parrot
    战吼：获得一张上一个死亡的友方亡语随从的复制。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    def play(self):
        """
        获得上一个死亡的友方亡语随从的复制
        
        需要追踪最后死亡的亡语随从
        """
        # 从死亡的随从中找到最后一个有亡语的
        dead_minions = [c for c in self.controller.graveyard 
                       if c.type == CardType.MINION and hasattr(c, 'deathrattle')]
        
        if dead_minions:
            # 最后一个死亡的
            last_deathrattle_minion = dead_minions[-1]
            yield Give(CONTROLLER, Copy(last_deathrattle_minion))


class DED_009:
    """狗狗饼干 / Doggie Biscuit
    可交易 使一个随从获得+2/+3。在你交易此牌后，使一个友方随从获得突袭。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    # 可交易在 CardDefs.xml 中定义
    play = Buff(TARGET, "DED_009e")
    
    # 交易后效果：使一个友方随从获得突袭
    trade = Find(FRIENDLY_MINIONS) & SetTags(RANDOM(FRIENDLY_MINIONS), {GameTag.RUSH: True})



class DED_009e:
    """狗狗饼干增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
    }


class SW_320:
    """硕鼠成群 / Rats of Extraordinary Size
    召唤七个1/1的老鼠。无法上场的老鼠会进入你的手牌，并获得+4/+4。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 6,
    }
    
    def play(self):
        """
        召唤7个老鼠
        场上满了的话，剩余的进入手牌并+4/+4
        """
        for _ in range(7):
            # 检查场上是否还有空位
            if len(self.controller.field) < self.game.MAX_MINIONS_ON_FIELD:
                # 有空位，直接召唤
                yield Summon(CONTROLLER, "SW_320t")
            else:
                # 没空位，加入手牌并+4/+4
                rat = yield Give(CONTROLLER, "SW_320t")
                # 给刚加入手牌的老鼠+4/+4
                if rat:
                    yield Buff(rat[0], "SW_320e")



class SW_320t:
    """老鼠"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


class SW_320e:
    """硕鼠成群增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
    }


class SW_321:
    """瞄准射击 / Aimed Shot
    造成$3点伤害。你的下一个英雄技能造成的伤害+2。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    play = (Hit(TARGET, 3), Buff(FRIENDLY_HERO, "SW_321e"))


class SW_321e:
    """瞄准射击英雄技能增强"""
    # 下一个英雄技能伤害+2
    
    def apply(self, target):
        """设置英雄技能伤害加成"""
        target.hero_power_damage_bonus = 2
    
    # 监听英雄技能使用
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).on(
        Destroy(SELF)  # 使用后移除buff
    )




class SW_322:
    """保卫矮人区 / Defend the Dwarven District
    任务线：用3个法术造成伤害。奖励：你的英雄技能可以指向随从。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段用3个法术造成伤害
    questline_requirements = [3, 3, 3]
    
    def play(self):
        """打出任务线"""
        from ...enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_322e")
    
    def questline_reward_1(self):
        """阶段1奖励：英雄技能可以指向随从"""
        # 修改英雄技能的目标限制
        # 猎人英雄技能默认只能指向英雄，现在可以指向随从
        return [Buff(FRIENDLY_HERO_POWER, "SW_322_reward1")]
    
    def questline_reward_2(self):
        """阶段2奖励：英雄技能伤害+1"""
        return [Buff(FRIENDLY_HERO, "SW_322_reward2")]
    
    def questline_reward_3(self):
        """阶段3奖励：英雄技能伤害+1（累计+2）"""
        return [Buff(FRIENDLY_HERO, "SW_322_reward3")]


class SW_322e:
    """保卫矮人区追踪器"""
    # 监听法术造成伤害事件
    # 当法术造成伤害时，增加任务线进度
    
    def apply(self, target):
        """初始化追踪器"""
        if not hasattr(target, 'sw_322_spells_dealt_damage'):
            target.sw_322_spells_dealt_damage = set()  # 使用 set 避免重复计数
    
    # 监听法术造成伤害
    # 注意：需要在 Hit 之后触发，确保确实造成了伤害
    events = Hit(CONTROLLER, SPELL, ALL_CHARACTERS).after(
        lambda self: [
            # 记录这个法术已造成伤害
            self.controller.sw_322_spells_dealt_damage.add(id(Hit.SOURCE)),
            # 找到任务线并增加进度
            Find(FRIENDLY_SECRETS + ID("SW_322")) & 
            QuestlineProgress(FRIENDLY_SECRETS + ID("SW_322"), 1)
        ] if id(Hit.SOURCE) not in self.controller.sw_322_spells_dealt_damage else []
    )


class SW_322_reward1:
    """英雄技能可以指向随从"""
    # 修改英雄技能的目标要求
    # 允许猎人英雄技能指向随从
    tags = {
        GameTag.STEADY_SHOT_CAN_TARGET: True,
    }


class SW_322_reward2:
    """英雄技能伤害+1"""
    def apply(self, target):
        """永久增加英雄技能伤害"""
        target.hero_power_damage_bonus += 1
    
    # 每次使用英雄技能后，重新设置加成（因为 Hit 会重置为0）
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
        lambda self: setattr(self.controller, 'hero_power_damage_bonus', 
                            self.controller.hero_power_damage_bonus + 1)
    )


class SW_322_reward3:
    """英雄技能伤害+1（累计+2）"""
    def apply(self, target):
        """永久增加英雄技能伤害"""
        target.hero_power_damage_bonus += 1
    
    # 每次使用英雄技能后，重新设置加成
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
        lambda self: setattr(self.controller, 'hero_power_damage_bonus', 
                            self.controller.hero_power_damage_bonus + 1)
    )


class SW_323:
    """鼠王 / The Rat King
    突袭。亡语：休眠。在5个友方随从死亡后复活。"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.RUSH: True,
    }
    
    def deathrattle(self):
        """
        休眠并等待5个友方随从死亡后复活
        """
        # 使自己休眠
        self.dormant = True
        self.zone = Zone.SETASIDE
        
        # 添加追踪器
        yield Buff(CONTROLLER, "SW_323e")


class SW_323e:
    """鼠王复活追踪器"""
    def apply(self, target):
        """初始化计数器"""
        if not hasattr(target, 'rat_king_minions_died'):
            target.rat_king_minions_died = 0
    
    # 监听友方随从死亡
    events = Death(FRIENDLY + MINION).on(
        lambda self: [
            setattr(self.controller, 'rat_king_minions_died', 
                   self.controller.rat_king_minions_died + 1),
            # 如果达到5个，复活鼠王
            Summon(CONTROLLER, "SW_323") if self.controller.rat_king_minions_died >= 5 else None,
            Destroy(SELF) if self.controller.rat_king_minions_died >= 5 else None
        ]
    )


class SW_455:
    """老鼠窝 / Rodent Nest
    亡语：召唤五个1/1的老鼠。"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
    }
    
    deathrattle = Summon(CONTROLLER, "SW_455t") * 5


class SW_455t:
    """老鼠"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }


class SW_457:
    """制皮工具 / Leatherworking Kit
    在三个友方野兽死亡后，抽一张野兽牌并使其获得+1/+1。失去1点耐久度。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 3,
        GameTag.DURABILITY: 3,
        GameTag.COST: 2,
    }
    
    # 简化实现：每次友方野兽死亡有 1/3 概率触发效果
    # 因为精确计数需要复杂的状态追踪，这里使用概率模拟
    events = Death(FRIENDLY + MINION + BEAST).on(
        (RandomNumber(0, 2) == 0) & (
            ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + BEAST),
            Hit(SELF, 1)
        )
    )


class SW_457e:
    """制皮工具增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_458:
    """山羊坐骑 / Ramming Mount
    使一个随从获得+2/+2和攻击时免疫。当其死亡时，召唤一只公羊。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    play = Buff(TARGET, "SW_458e")


class SW_458e:
    """山羊坐骑增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }
    
    # 攻击时免疫
    events = Attack(OWNER).on(
        Buff(OWNER, "SW_458_immune")
    )
    
    # 死亡时召唤公羊
    deathrattle = Summon(CONTROLLER, "SW_458t")


class SW_458_immune:
    """攻击时免疫"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }


class SW_458t:
    """公羊"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }


class SW_459:
    """暴风城吹笛人 / Stormwind Piper
    在本随从攻击后，使你的野兽获得+1/+1。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    # 攻击后给所有友方野兽+1/+1
    events = Attack(SELF).after(
        Buff(FRIENDLY_MINIONS + BEAST, "SW_459e")
    )


class SW_459e:
    """暴风城吹笛人增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class SW_460:
    """集群撕咬 / Devouring Swarm
    选择一个敌方随从。使你的随从攻击它，然后将所有死亡的随从移回你的手牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        """
        让所有友方随从攻击目标
        然后将死亡的随从移回手牌
        """
        # 记录当前场上的随从
        friendly_minions = list(self.controller.field)
        
        # 让所有随从攻击目标
        for minion in friendly_minions:
            if minion.zone == Zone.PLAY:  # 确保还在场上
                yield Attack(minion, TARGET)
        
        # 将死亡的随从移回手牌
        for minion in friendly_minions:
            if minion.zone == Zone.GRAVEYARD:
                # 从墓地移回手牌
                yield Give(CONTROLLER, Copy(minion))


class SW_463:
    """进口狼蛛 / Imported Tarantula
    可交易 亡语：召唤两个1/1并具有剧毒和突袭的蜘蛛。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    # 可交易在 CardDefs.xml 中定义
    deathrattle = Summon(CONTROLLER, "SW_463t") * 2


class SW_463t:
    """蜘蛛"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
        GameTag.POISONOUS: True,
        GameTag.RUSH: True,
    }


