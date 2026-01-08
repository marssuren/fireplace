"""
失落之城 - TOKENS

所有职业共享的 Token 卡牌定义
包括：随从 Token、法术 Token、Enchantment 等
"""
from ..utils import *
from ...enums import HEALTH_COST


# ========================================
# Death Knight Tokens
# ========================================

class TLC_443t:
    """不情愿的宠物 - Reluctant Pet
    2/2 亡灵+野兽 - 嘲讽
    
    Token from TLC_443 (不情愿的饲养员)
    """
    tags = {
        GameTag.TAUNT: True,
    }


class TLC_433t:
    """泰拉克斯，魔骸暴龙 - Terrax, the Bone Tyrant
    10费 10/10 亡灵+野兽
    <b>突袭</b>。<b>亡语：</b>召唤一个它的复制。
    
    Rush. Deathrattle: Summon a copy of this.
    
    任务奖励 Token from TLC_433 (恐怖再起)
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "TLC_433t")


# ========================================
# Demon Hunter Tokens
# ========================================

class DINO_136t:
    """贪婪的迅猛龙 - Greedy Raptor
    2费 2/1 野兽
    <b>突袭</b>
    
    Token from DINO_136 (盛宴之角)
    """
    tags = {
        GameTag.RUSH: True,
    }


class TLC_833t:
    """异种虫幼体 - Silithid Hatchling
    2费 2/1 随从
    <b>突袭</b>
    
    Token from TLC_833 (昆虫利爪) and TLC_902 (虫害侵扰)
    """
    tags = {
        GameTag.RUSH: True,
    }


class TLC_902t:
    """格里什毒刺虫 - Qiraji Stinger
    1费 法术
    造成$2点伤害并召唤一只2/1具有<b>突袭</b>的异种虫幼体。
    
    Token from TLC_902 (虫害侵扰) and TLC_630 (格里什异种虫)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)
        # 召唤一只2/1突袭异种虫幼体
        yield Summon(CONTROLLER, "TLC_833t")


class TLC_631t:
    """格里什巨虫 - Qiraji Colossus
    10费 10/10 随从
    <b>突袭</b>。<b>嘲讽</b>
    
    Quest reward from TLC_631 (放出巨虫)
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
    }


class TLC_841t:
    """标本罐 - Specimen Jar
    1费 0/1 随从
    <b>亡语：</b>召唤罐子中的随从。
    
    Token from TLC_841 (昆虫学家托鲁)
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    # 亡语由 TLC_841e 动态提供


# ========================================
# Druid Tokens
# ========================================

class DINO_130t:
    """长颈龙幼体 - Longneck Hatchling
    3费 3/3 野兽
    
    Token from DINO_130 (长颈龙蛋)
    """
    # 基础属性由 cards.json 定义


class TLC_230t:
    """树人 - Treant
    2费 2/2 随从
    
    Token from TLC_230 (树群来袭)
    """
    # 基础属性由 cards.json 定义


class TLC_237t:
    """啸天龙宝宝 - Screechling
    1费 2/1 野兽
    
    Token from TLC_237 (啸天龙蛋), TLC_232 (待哺群雏)
    """
    # 基础属性由 cards.json 定义


class TLC_234t:
    """永生花芽 - Everlasting Bud
    0费 0/1 随从
    <b>亡语:</b>召唤一个永生血瓣花。
    
    Token from TLC_234 (永生血瓣花)
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "TLC_234")


class TLC_239t:
    """永茂之花 - Everbloom
    5费 地标 - 3耐久度
    召唤一个法力值消耗为（5）的随从。
    
    Quest reward from TLC_239 (治愈荒野)
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 5,
        GameTag.HEALTH: 3,
    }
    
    def activate(self):
        # 召唤一个5费随从
        yield Summon(CONTROLLER, RandomMinion(cost=5))



# ========================================
# Hunter Tokens
# ========================================

class TLC_826t:
    """卡纳莎的迅猛龙 - Carnassa's Raptor
    1费 3/2 野兽
    <b>战吼：</b>抽一张牌。
    
    Token from TLC_826 (卡纳莎的故事)
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 战吼：抽一张牌
        yield Draw(CONTROLLER)


class TLC_830t:
    """绍克 - Shok
    10费 10/10 野兽
    <b>突袭</b>。<b>嘲讽</b>
    
    Quest reward from TLC_830 (食物链)
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
    }


# ========================================
# Mage Tokens
# ========================================

class TLC_460t:
    """源生之石 - Primordial Stone
    10费 地标 - 3耐久度
    <b>发现</b>一张法术牌并施放它。
    
    Quest reward from TLC_460 (禁忌序列)
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 10,
        GameTag.HEALTH: 3,
    }
    
    def activate(self):
        # 发现一张法术牌
        cards = yield DISCOVER(RandomCollectible(type=CardType.SPELL))
        
        if cards:
            # 施放发现的法术
            # 使用 CastSpell action 会自动处理目标选择（随机目标）
            # 参考 whizbang/tokens.py 的 LOOT_506 实现
            yield CastSpell(cards[0])


class TLC_452t:
    """考古发现 - Archaeological Discovery
    2费 2/2 随从
    
    Token from TLC_452c (泰坦考据学家欧斯克 - 版本C)
    """
    # 基础属性由 cards.json 定义


# ========================================
# Paladin Tokens
# ========================================

class TLC_240t:
    """鱼人 - Murloc
    2费 2/1 鱼人
    
    Token from TLC_240 (填鳃暴龙)
    """
    # 基础属性由 cards.json 定义


class TLC_241t:
    """伊度的祝福 - Idu's Blessing
    2费 神圣法术
    使一个随从获得+2/+2和<b>圣盾</b>。
    
    Give a minion +2/+2 and Divine Shield.
    
    Token from TLC_241 (蛇颈龙群的伊度)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 给目标随从+2/+2和圣盾
        yield Buff(TARGET, "TLC_241t_buff")


class TLC_241t_buff:
    """+2/+2和圣盾"""
    atk = 2
    max_health = 2
    tags = {GameTag.DIVINE_SHIELD: True}


# ========================================
# Priest Tokens
# ========================================

class TLC_817t1:
	"""生命之息 - Breath of Life
	5费 4/4 元素
	<b>嘲讽</b>。<b>战吼:</b>召唤一个它的复制。<i>(阿玛拉在此,拼合!)</i>
	
	Quest reward from TLC_817 (寻求平衡) - 神圣任务奖励
	"""
	tags = {
		GameTag.TAUNT: True,
		GameTag.BATTLECRY: True,
	}
	
	def play(self):
		# 战吼:召唤一个自己的复制
		yield Summon(CONTROLLER, "TLC_817t3")


class TLC_817t2:
	"""死亡之触 - Touch of Death
	5费 4/4 元素
	<b>复生</b>。<b>亡语:</b>对一个随从造成5点伤害。<i>(阿玛拉在此,拼合!)</i>
	
	Quest reward from TLC_817 (寻求平衡) - 暗影任务奖励
	"""
	tags = {
		GameTag.REBORN: True,
		GameTag.DEATHRATTLE: True,
	}
	
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS: 1,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def deathrattle(self):
		# 亡语:对一个随从造成5点伤害
		# 需要目标选择
		if TARGET:
			yield Hit(TARGET, 5)


class TLC_817t3:
	"""阿玛拉之息 - Amara's Breath
	5费 4/4 元素
	<b>嘲讽</b>。<b>战吼:</b>召唤一个它的复制。
	
	Token from TLC_817t1 (生命之息)
	"""
	tags = {
		GameTag.TAUNT: True,
		GameTag.BATTLECRY: True,
	}
	
	def play(self):
		# 战吼:召唤一个自己的复制
		yield Summon(CONTROLLER, "TLC_817t4")


class TLC_817t4:
	"""阿玛拉之触 - Amara's Touch
	5费 4/4 元素
	<b>复生</b>。<b>亡语:</b>对一个随从造成5点伤害。
	
	Token from TLC_817t2 (死亡之触)
	"""
	tags = {
		GameTag.REBORN: True,
		GameTag.DEATHRATTLE: True,
	}
	
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS: 1,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def deathrattle(self):
		# 亡语:对一个随从造成5点伤害
		if TARGET:
			yield Hit(TARGET, 5)


class TLC_817t5:
	"""阿玛拉循环 - Amara's Cycle
	5费 8/8 元素
	<b>嘲讽</b>。<b>复生</b>。<b>战吼:</b>召唤一个它的复制。<b>亡语:</b>对一个随从造成5点伤害。
	
	Final form - 当两个任务都完成后的最终形态
	"""
	tags = {
		GameTag.TAUNT: True,
		GameTag.REBORN: True,
		GameTag.BATTLECRY: True,
		GameTag.DEATHRATTLE: True,
	}
	
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS: 1,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def play(self):
		# 战吼:召唤一个自己的复制
		yield Summon(CONTROLLER, "TLC_817t5")
	
	def deathrattle(self):
		# 亡语:对一个随从造成5点伤害
		if TARGET:
			yield Hit(TARGET, 5)


class TLC_820t:
	"""林地祝福/诅咒 - Woodland Blessing/Curse
	1费 神圣法术
	<b>抉择:</b>使一个随从获得+2生命值;或使一个随从获得-2生命值。
	
	Token from TLC_820 (林地生态学者)
	"""
	tags = {
		GameTag.CHOOSE_ONE: True,
	}
	choose = ["TLC_820ta", "TLC_820tb"]


class TLC_820ta:
	"""林地祝福 - Woodland Blessing
	使一个随从获得+2生命值。
	
	Choose One option A from TLC_820t
	"""
	tags = {GameTag.CARDTYPE: CardType.SPELL}
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def play(self):
		# 给予+2生命值
		yield Buff(TARGET, "TLC_820tae")


class TLC_820tae:
	"""+2生命值"""
	max_health = 2


class TLC_820tb:
	"""林地诅咒 - Woodland Curse
	使一个随从获得-2生命值。
	
	Choose One option B from TLC_820t
	"""
	tags = {GameTag.CARDTYPE: CardType.SPELL}
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def play(self):
		# 给予-2生命值
		yield Buff(TARGET, "TLC_820tbe")


class TLC_820tbe:
	"""-2生命值"""
	max_health = -2



# ========================================
# Rogue Tokens
# ========================================

class TLC_518t:
    """忍者 - Ninja
    3费 3/3 随从
    潜行。抽到时召唤。
    
    Stealth. Cast When Drawn.
    
    Token from TLC_518 (审讯)
    """
    tags = {
        GameTag.STEALTH: True,
        GameTag.CAST_WHEN_DRAWN: True,
    }
    
    # 抽到时召唤自己
    def drawn(self):
        yield Summon(CONTROLLER, SELF)


class TLC_519t:
    """喷毒龙 - Venomspitter
    1费 1/1 野兽
    潜行。剧毒。
    
    Stealth. Poisonous.
    
    Token from TLC_519 (潜踪掠食)
    """
    tags = {
        GameTag.STEALTH: True,
        GameTag.POISONOUS: True,
    }


class TLC_513t:
    """暮影大师 - Shadowmaster
    5费 5/5 随从
    战吼:你的随从获得+2/+2和潜行。
    
    Battlecry: Give your minions +2/+2 and Stealth.
    
    Quest reward from TLC_513 (暗中设伏)
    """
    def play(self):
        # 给予所有友方随从+2/+2和潜行
        for minion in self.controller.field:
            yield Buff(minion, "TLC_513te")


class TLC_513te:
    """+2/+2和潜行 - Shadowmaster Buff"""
    atk = 2
    max_health = 2
    tags = {GameTag.STEALTH: True}


# ========================================
# Shaman Tokens
# ========================================

class TLC_229t:
    """阿沙隆 - Ashalon
    10费 10/10 野兽
    <b>突袭</b>。<b>嘲讽</b>

    Quest reward from TLC_229 (群山之灵)
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
    }


# ========================================
# Warlock Tokens
# ========================================

class DINO_402e:
    """蝙蝠面具附魔 - Bat Mask Enchantment
    1/1。

    实现说明:
    - 将随从的攻击力和生命值设置为1/1
    - 使用 lambda 设置固定值
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }

    # 设置固定属性值
    atk = lambda self, i: 1
    max_health = lambda self, i: 1


class DINO_131e:
    """吸血附魔 - Lifesteal Enchantment
    使随从获得吸血。
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.LIFESTEAL: True,
    }


class TLC_450e:
    """洞穴专家玩家附加效果 - Cave Expert Player Enchantment
    你的下一张<b>临时</b>牌的法力值消耗减少（2）点。

    实现说明:
    - 使用 Hand 光环在手牌中就生效
    - 监听打出临时牌的事件，使用后移除自身
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }

    class Hand:
        """手牌光环：临时牌减费(2)"""
        def apply(self, target):
            # 检查是否为临时牌
            if target.tags.get(GameTag.TEMPORARY, False):
                target.cost -= 2

    # 监听打出临时牌的事件，使用后移除自身
    events = Play(CONTROLLER, FRIENDLY + TEMPORARY).on(
        Destroy(SELF)
    )


class TLC_466e:
    """拉卡利的故事附魔 - Lakkari's Tale Enchantment
    在你的回合结束时，弃一张牌并用3/2的小鬼填满你的面板。持续3回合。

    实现说明:
    - 使用 TAG_SCRIPT_DATA_NUM_1 追踪剩余回合数
    - 每回合结束时触发效果并减少计数
    - 计数归零时移除自身
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 剩余回合数
    }

    events = OWN_TURN_END.on(
        lambda self, entity: TLC_466e._trigger_effect(entity.owner)
    )

    @staticmethod
    def _trigger_effect(buff):
        """回合结束时触发效果"""
        controller = buff.controller

        # 弃一张随机手牌
        if controller.hand:
            yield Discard(RANDOM(FRIENDLY_HAND))

        # 计算剩余空位并召唤小鬼
        available_space = 7 - len(controller.field)
        if available_space > 0:
            yield Summon(controller, "TLC_466t") * available_space

        # 减少剩余回合数
        buff.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] -= 1

        # 如果回合数用完，移除buff
        if buff.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] <= 0:
            yield Destroy(buff)


class TLC_467e:
    """石之低语附魔 - Whispering Stone Enchantment
    消耗生命值，而非法力值。

    实现说明:
    - 使用 HEALTH_COST 标记法术消耗生命值而非法力值
    - 核心系统会在打出时扣除生命值
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        HEALTH_COST: True,
    }


class TLC_466t:
    """小鬼 Token - Imp Token
    3/2 小鬼
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 1,
        GameTag.CARDTYPE: CardType.MINION,
    }
    race = Race.DEMON


class TLC_446t:
    """邪能地窟裂隙 - Fel Grotto Rift (Spell)
    5费 法术
    打开一道邪能地窟裂隙。向其中投入一张卡牌以随机召唤2只邪能野兽。（每回合一次。）

    实现说明:
    - 召唤一个特殊的地窟裂隙随从（TLC_446t1）
    """
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }

    def play(self):
        # 召唤邪能地窟裂隙随从
        yield Summon(CONTROLLER, "TLC_446t1")


class TLC_446t1:
    """邪能地窟裂隙 - Fel Grotto Rift (Minion)
    5费 0/1 特殊随从
    选择裂隙即可激活。向其中投入一张卡牌以随机召唤2只邪能野兽。（每回合一次。）

    实现说明:
    - 不可被攻击（UNTOUCHABLE）
    - 每回合可激活一次
    - 激活时：弃掉一张手牌，召唤2只随机邪能野兽
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 1,
        GameTag.COST: 5,
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.UNTOUCHABLE: True,
    }

    def activate(self):
        """激活裂隙：弃一张手牌，召唤2只邪能野兽"""
        if self.controller.hand:
            # 弃掉一张随机手牌
            yield Discard(RANDOM(FRIENDLY_HAND))
            # 随机召唤2只邪能野兽
            import random
            fel_beasts = ["TLC_446t2", "TLC_446t3", "TLC_446t4"]
            for _ in range(2):
                beast_id = random.choice(fel_beasts)
                yield Summon(CONTROLLER, beast_id)


class TLC_446t2:
    """邪能啸天龙 - Fel Howler
    5费 5/3 恶魔+野兽
    <b>突袭</b>。<b>吸血</b>
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 3,
        GameTag.COST: 5,
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.RUSH: True,
        GameTag.LIFESTEAL: True,
    }
    races = [Race.DEMON, Race.BEAST]


class TLC_446t3:
    """邪能迅猛龙 - Fel Raptor
    5费 4/4 恶魔+野兽
    <b>冲锋</b>。<b>扰魔</b>
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CHARGE: True,
        GameTag.CANT_BE_TARGETED_BY_SPELLS: True,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
    }
    races = [Race.DEMON, Race.BEAST]


class TLC_446t4:
    """邪能恐角龙 - Fel Terrorhorn
    5费 3/5 恶魔+野兽
    <b>嘲讽</b>。<b>复生</b>
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
        GameTag.COST: 5,
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.TAUNT: True,
        GameTag.REBORN: True,
    }
    races = [Race.DEMON, Race.BEAST]


# ========================================
# Warrior Tokens
# ========================================

class TLC_632t2:
    """怒火（两次）
    随机对一个敌人造成$8点伤害。<i>（还能使用两次。）</i>
    """
    # Type: HERO_POWER | Cost: 2
    activate = Hit(RANDOM_ENEMY_CHARACTER, 8)

    events = Activate(SELF).after(
        # 使用后替换为只能使用一次的版本
        Summon(CONTROLLER, "TLC_632t"),
        Destroy(SELF)
    )


class TLC_632t:
    """怒火（一次）
    随机对一个敌人造成$8点伤害。<i>（还能使用一次。）</i>
    """
    # Type: HERO_POWER | Cost: 2

    def activate(self):
        # 造成8点伤害
        yield Hit(RANDOM_ENEMY_CHARACTER, 8)

        # 恢复原始英雄技能
        if hasattr(self.controller, 'tlc632_original_power'):
            original_id = self.controller.tlc632_original_power
            yield Summon(CONTROLLER, original_id)
        else:
            # 默认战士英雄技能
            yield Summon(CONTROLLER, "CS2_102")

        # 销毁当前英雄技能
        yield Destroy(SELF)


# ========================================
# Neutral Tokens
# ========================================

class TLC_252t:
    """骸骨 - Bone
    1费 法术
    使一个随从获得被消灭随从的攻击力和生命值。
    
    Token from TLC_252 (蚀解软泥怪)
    
    官方说明：
    - 动态法术牌，属性值存储在 TLC_252e buff 中
    - 给目标随从增加被消灭随从的攻击力和生命值
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 从自己的 buff 中获取存储的属性值
        stored_atk = 0
        stored_health = 0
        
        # 查找 TLC_252e buff
        for buff in self.buffs:
            if buff.id == "TLC_252e":
                stored_atk = getattr(buff, '_stored_atk', 0)
                stored_health = getattr(buff, '_stored_health', 0)
                break
        
        # 给目标随从增加属性值
        if TARGET and (stored_atk > 0 or stored_health > 0):
            yield Buff(TARGET, "TLC_252t_buff", atk=stored_atk, max_health=stored_health)


class TLC_252t_buff:
    """骸骨增益 - Bone Buff
    
    给目标随从增加属性值
    """
    def apply(self, target):
        # 从 buff 参数中获取属性值并保存
        self._xatk = self.atk
        self._xhealth = self.max_health
    
    # 使用 lambda 动态返回属性值
    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


class TLC_427t:
    """石头 - Stone
    1费 法术
    造成$3点伤害。
    
    Token from TLC_427 (抛石鱼人)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)


class TLC_429t:
    """鱼人 - Murloc
    1费 1/1 鱼人
    <b>突袭</b>
    
    Token from TLC_429 (蒸鳍偷蛋贼)
    """
    tags = {
        GameTag.RUSH: True,
    }


class TLC_468t1:
    """剧毒黏团 - Poisonous Blob
    1费 1/2
    <b>剧毒</b>
    
    Token from TLC_468 (黏团焦油)
    """
    tags = {
        GameTag.POISONOUS: True,
    }


class TLC_468t2:
    """嘲讽黏团 - Taunt Blob
    1费 1/2
    <b>嘲讽</b>
    
    Token from TLC_468 (黏团焦油)
    """
    tags = {
        GameTag.TAUNT: True,
    }


class TLC_831t:
    """翼手龙 - Pterrordax
    3费 3/3 野兽
    <b>战吼：</b>从所有其他随从处偷取1点生命值。
    
    Token from TLC_831 (翼手龙蛋)
    """
    def play(self):
        # 从所有其他随从处偷取1点生命值
        other_minions = self.game.query(ALL_MINIONS - SELF)
        for minion in other_minions:
            # 对每个随从造成1点伤害
            yield Hit(minion, 1)
            # 治疗自己1点
            yield Heal(SELF, 1)


class TLC_245t:
    """植物 - Plant
    1费 1/1 随从
    
    Token from TLC_245c (远古迅猛龙 - 选项3)
    """
    # 基础属性由 cards.json 定义
    # 1费 1/1 普通随从


# ========================================
# 凯洛斯的蛋系列 Token (DINO_410)
# ========================================

class DINO_410t1:
    """轻微开裂的蛋 - Slightly Cracked Egg
    3费 0/3
    <b>亡语：</b>召唤一枚开裂的蛋。
    
    Token from DINO_410 (凯洛斯的蛋) - 阶段1
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "DINO_410t2")


class DINO_410t2:
    """开裂的蛋 - Cracked Egg
    3费 0/3
    <b>亡语：</b>召唤一枚严重开裂的蛋。
    
    Token from DINO_410t1 - 阶段2
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "DINO_410t3")


class DINO_410t3:
    """严重开裂的蛋 - Heavily Cracked Egg
    3费 0/3
    <b>亡语：</b>召唤一枚即将孵化的蛋。
    
    Token from DINO_410t2 - 阶段3
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "DINO_410t4")


class DINO_410t4:
    """即将孵化的蛋 - Nearly Hatched Egg
    3费 0/3
    <b>亡语：</b>召唤凯洛斯。
    
    Token from DINO_410t3 - 阶段4
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "DINO_410t5")


class DINO_410t5:
    """凯洛斯 - Kairos
    10费 20/20 野兽
    <b>嘲讽</b>
    
    Token from DINO_410t4 - 最终形态
    """
    tags = {
        GameTag.TAUNT: True,
    }


# ========================================
# 导航员伊莉斯地标 Token (TLC_100)
# ========================================

class TLC_100t:
    """安戈洛宝箱 - Un'Goro Pack
    5费 地标 - 3耐久度
    <b>发现</b>一张牌。
    
    Token from TLC_100 (导航员伊莉斯)
    
    官方说明:
    - 自定义地标，每次使用时发现一张牌
    - 3次使用机会
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 5,
        GameTag.HEALTH: 3,
    }
    
    def activate(self):
        # 发现一张牌（任意可收集卡牌）
        yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.collectible,
            count=3
        ))


# ========================================
# Shared Tokens (跨职业共享)
# ========================================

# 当前版本没有跨职业共享的 Token
# 所有 Token 都已在各自的职业文件或 tokens.py 的对应职业部分定义
