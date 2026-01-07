"""
穿越时间流 - TOKENS
"""
from ..utils import *


# ========================================
# Druid Tokens
# ========================================

class TIME_704t:
    """小学生 - Pupil
    2/2 随从
    
    由"上层精灵教师"生成的Token
    亡语：施放教会的法术
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    @property
    def deathrattle(self):
        """动态亡语：施放教会的法术"""
        # 从buff中获取存储的法术ID
        spell_id = None
        for buff in self.buffs:
            if buff.id == "TIME_704e" and hasattr(buff, 'spell_id'):
                spell_id = buff.spell_id
                break
        
        if spell_id:
            # 施放该法术
            return CastSpell(spell_id)
        return []


class TIME_704e:
    """小学生 - 存储法术ID的buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    def __init__(self, *args, spell_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id


class TIME_211t1:
    """辛艾萨莉 - Zin-Azshari
    10费 地标
    
    由"艾萨拉女士"的Fabled机制添加到套牌中
    每回合开始时，随机施放一个自然法术
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.HEALTH: 3,
    }
    
    def activate(self):
        """激活效果：随机施放一个自然法术"""
        yield CastSpell(RandomSpell(spell_school=SpellSchool.NATURE))


class TIME_211t2:
    """永恒之井 - The Well of Eternity
    5费 法术
    
    由"艾萨拉女士"的Fabled机制添加到套牌中
    抽五张牌，其法力值消耗减少（2）点
    """
    requirements = {}
    
    def play(self):
        # 抽五张牌
        drawn_cards = []
        for _ in range(5):
            cards = yield Draw(self.controller)
            if cards:
                drawn_cards.extend(cards)
        
        # 给抽到的牌减少2费
        for card in drawn_cards:
            if card.zone == Zone.HAND:
                yield Buff(card, "TIME_211t2e")


class TIME_211t2e:
    """永恒之井 - 减少2费"""
    cost = -2


class TIME_025t:
	"""时空撕裂 - Time Tear
	Casts When Drawn. Deal 3 damage to your hero.
	"""
	# Mechanics: CASTS_WHEN_DRAWN
	def play(self):
		yield Hit(self.controller.hero, 3)
		yield Draw(self.controller)


# ========================================
# Death Knight Tokens
# ========================================

class TIME_610t:
	"""暗影 - Shade
	3/2 亡灵
	
	由"昨日之影"召唤的Token
	"""
	pass


class TIME_610e1:
	"""奖励效果：+2/+2"""
	atk = 2
	health = 2


class TIME_610e2:
	"""奖励效果：突袭"""
	tags = {
		GameTag.RUSH: True,
	}


class TIME_610e3:
	"""奖励效果：嘲讽"""
	tags = {
		GameTag.TAUNT: True,
	}


class TIME_610e4:
	"""奖励效果：圣盾"""
	tags = {
		GameTag.DIVINE_SHIELD: True,
	}


class TIME_610e5:
	"""奖励效果：吸血"""
	tags = {
		GameTag.LIFESTEAL: True,
	}


class TIME_619t:
	"""Bwonsamdi - 邦桑迪
	6费 6/6 亡灵
	**亡语：**召唤一个随机的法力值消耗为（4）点的随从。（给予邦桑迪的任何祝福都会传递给召唤的随从。）
	
	Deathrattle: Summon a random 4-Cost minion. (Any Boons given to Bwonsamdi carry over.)
	
	由Talanji of the Graves的Fabled机制添加到套牌中
	"""
	tags = {
		GameTag.DEATHRATTLE: True,
	}
	
	@property
	def deathrattle(self):
		"""
		动态亡语：召唤一个随机4费随从，并将Bwonsamdi的祝福buff传递给它
		"""
		# 召唤一个随机4费随从
		minion = Summon(CONTROLLER, RandomCollectible(type=CardType.MINION, cost=4))
		
		# 检查Bwonsamdi是否有祝福buff
		# 祝福buff的ID：TIME_619t2e (长寿), TIME_619t3e (力量), TIME_619t4e (速度)
		boon_buffs = []
		for buff in self.buffs:
			if buff.id in ["TIME_619t2e", "TIME_619t3e", "TIME_619t4e"]:
				boon_buffs.append(buff.id)
		
		# 将祝福传递给召唤的随从
		actions = [minion]
		if boon_buffs:
			for boon_id in boon_buffs:
				actions.append(Buff(minion, boon_id))
		
		return actions


class TIME_619t2:
	"""长寿祝福 - Longevity Boon (选项卡牌)
	选择此祝福会给Bwonsamdi添加吸血
	"""
	pass


class TIME_619t2e:
	"""长寿祝福效果 - Longevity Boon Effect
	吸血，并使亡语召唤的随从费用+2
	"""
	tags = {
		GameTag.LIFESTEAL: True,
	}
	
	# 修改亡语召唤的随从费用
	# 这需要在亡语逻辑中处理


class TIME_619t3:
	"""力量祝福 - Power Boon (选项卡牌)
	选择此祝福会给Bwonsamdi添加嘲讽
	"""
	pass


class TIME_619t3e:
	"""力量祝福效果 - Power Boon Effect
	嘲讽，并使亡语召唤的随从费用+2
	"""
	tags = {
		GameTag.TAUNT: True,
	}


class TIME_619t4:
	"""速度祝福 - Speed Boon (选项卡牌)
	选择此祝福会给Bwonsamdi添加突袭
	"""
	pass


class TIME_619t4e:
	"""速度祝福效果 - Speed Boon Effect
	突袭，并使亡语召唤的随从费用+2
	"""
	tags = {
		GameTag.RUSH: True,
	}


class TIME_619t5:
	"""赞达拉的遭遇 - What Befell Zandalar
	3费 法术
	对所有敌人造成$2点伤害。选择一个祝福给予邦桑迪。（祝福还会使邦桑迪的**亡语**召唤的随从法力值消耗增加（2）点。）
	
	Deal $2 damage to all enemies. Choose a Boon to give to Bwonsamdi. (Boons also make minions summoned by Bwonsamdi's Deathrattle cost (2) more.)
	
	由Talanji of the Graves的Fabled机制添加到套牌中
	"""
	requirements = {}
	
	def play(self):
		# 对所有敌人造成2点伤害
		yield Hit(ENEMY_CHARACTERS, 2)
		
		# 选择一个祝福给Bwonsamdi
		choice = yield GenericChoice(CONTROLLER, cards=[
			"TIME_619t2",  # 长寿祝福
			"TIME_619t3",  # 力量祝福
			"TIME_619t4",  # 速度祝福
		])
		
		# 找到Bwonsamdi（可能在手牌、场上或牌库中）
		bwonsamdi = None
		for card in self.controller.hand:
			if card.id == "TIME_619t":
				bwonsamdi = card
				break
		
		if not bwonsamdi:
			for minion in self.controller.field:
				if minion.id == "TIME_619t":
					bwonsamdi = minion
					break
		
		if not bwonsamdi:
			for card in self.controller.deck:
				if card.id == "TIME_619t":
					bwonsamdi = card
					break
		
		# 给Bwonsamdi添加祝福
		if bwonsamdi and choice:
			# 根据选择添加对应的buff
			if choice[0] == "TIME_619t2":
				yield Buff(bwonsamdi, "TIME_619t2e")
			elif choice[0] == "TIME_619t3":
				yield Buff(bwonsamdi, "TIME_619t3e")
			elif choice[0] == "TIME_619t4":
				yield Buff(bwonsamdi, "TIME_619t4e")


# ========================================
# Demon Hunter Tokens
# ========================================

class TIME_443t:
	"""怒火狱犬 - Hound of Fury
	3/3 恶魔
	
	由"怒火狱犬"召唤的Token
	"""
	tags = {
		GameTag.RUSH: True,
	}


class TIME_020t1:
	"""安尼赫兰 - Annihilan
	5费 6/8 恶魔
	<b>嘲讽</b>
	
	布洛克斯加的Fabled附带卡牌之一（阿古斯恶魔）
	"""
	tags = {
		GameTag.TAUNT: True,
	}


class TIME_020t2:
	"""末日守卫 - Doomguard
	5费 5/7 恶魔
	<b>冲锋</b>
	
	布洛克斯加的Fabled附带卡牌之一（阿古斯恶魔）
	"""
	tags = {
		GameTag.CHARGE: True,
	}


class TIME_020t3:
	"""恐惧魔王 - Dreadlord
	5费 7/5 恶魔
	<b>吸血</b>
	
	布洛克斯加的Fabled附带卡牌之一（阿古斯恶魔）
	"""
	tags = {
		GameTag.LIFESTEAL: True,
	}


class TIME_020t4:
	"""深渊领主 - Pit Lord
	5费 8/6 恶魔
	<b>战吼：</b>对你的英雄造成5点伤害。
	
	布洛克斯加的Fabled附带卡牌之一（阿古斯恶魔）
	"""
	def play(self):
		yield Hit(FRIENDLY_HERO, 5)


# ========================================
# Mage Tokens
# ========================================

class TIME_006t:
	"""镜像 - Mirror Image
	0/4 随从，嘲讽
	
	由"镜像维度"召唤的Token
	"""
	tags = {
		GameTag.TAUNT: True,
	}


# ========================================
# Hunter Tokens
# ========================================

class TIME_042t:
	"""无穷香蕉 - Infinite Banana
	1费 法术
	使一个随从获得+2/+2。将本牌的一张复制置入你的手牌。
	
	Give a minion +2/+2. Add a copy of this to your hand.
	
	由穆拉克（King Maluk）生成的Token
	"""
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def play(self):
		# 给目标随从+2/+2
		yield Buff(TARGET, "TIME_042te")
		
		# 将本牌的复制置入手牌
		yield Give(self.controller, "TIME_042t")


class TIME_042te:
	"""无穷香蕉增益 - Infinite Banana Buff"""
	atk = 2
	max_health = 2


class TIME_609t1:
	"""奥蕾莉亚 - Alleria Windrunner
	3费 3/3
	**战吼：**本回合中，你的英雄技能造成的伤害+1。
	
	Battlecry: Your Hero Power deals +1 damage this turn.
	
	由游侠将军希尔瓦娜斯的Fabled机制添加到套牌中
	"""
	tags = {
		GameTag.BATTLECRY: True,
	}
	
	def play(self):
		# 给玩家添加buff，本回合英雄技能伤害+1
		yield Buff(self.controller, "TIME_609t1e")


class TIME_609t1e:
	"""奥蕾莉亚效果 - Alleria Effect
	
	本回合英雄技能伤害+1
	"""
	tags = {
		GameTag.TAG_ONE_TURN_EFFECT: True,
	}
	
	# 这个效果需要在英雄技能造成伤害时增加1点
	# 通常通过修改 SPELLPOWER 或者监听 Hit 事件实现
	# 简化实现：给玩家+1法术伤害
	update = lambda self, entity: (
		entity == self.controller.hero.power and
		[Buff(entity, "TIME_609t1e2")]
	)


class TIME_609t1e2:
	"""奥蕾莉亚伤害增益"""
	tags = {
		GameTag.SPELLPOWER: 1,
	}


class TIME_609t2:
	"""温蕾萨 - Vereesa Windrunner
	3费 3/3
	**战吼：**装备一把2/2的武器。
	
	Battlecry: Equip a 2/2 weapon.
	
	由游侠将军希尔瓦娜斯的Fabled机制添加到套牌中
	"""
	tags = {
		GameTag.BATTLECRY: True,
	}
	
	def play(self):
		# 装备一把2/2武器
		yield Equip(self.controller, "TIME_609t2t")




class TIME_609t2t:
	"""温蕾萨的弓 - Vereesa's Bow
	2/2 武器
	
	由温蕾萨生成的Token武器
	"""
	pass


# ========================================
# Rogue Tokens
# ========================================

class TIME_713t:
	"""永恒宝箱 - Timeless Chest
	3费 0/8 随从
	**亡语：**用硬币填满你对手的手牌。
	
	Deathrattle: Fill your opponent's hand with Coins.
	
	由时空上将钩尾召唤的Token
	"""
	tags = {
		GameTag.DEATHRATTLE: True,
	}
	
	deathrattle = Give(OPPONENT, "GAME_005") * 10  # 硬币的ID是 GAME_005


class TIME_875t:
	"""莱恩国王 - King Llane
	3费 3/3 随从
	**游戏开始时：**躲避迦罗娜，藏在敌方牌库中。**战吼：**抽一张牌。将本牌洗回你的牌库。
	
	Start of Game: Hide from Garona in the enemy's deck. Battlecry: Draw a card. Shuffle this back into your deck.
	
	由半兽人迦罗娜的Fabled机制添加到对手套牌中
	
	实现说明：
	- 游戏开始时，莱恩国王会从玩家牌库移动到对手牌库
	- 这是通过 start_of_game 方法实现的
	- 参考 TIME_020 (布洛克斯加) 的实现
	"""
	tags = {
		GameTag.BATTLECRY: True,
		GameTag.START_OF_GAME: True,
	}
	
	def start_of_game(self):
		"""游戏开始时：从己方牌库移动到对手牌库"""
		# 莱恩国王最初在玩家牌库中（因为是 Fabled 套餐的一部分）
		# 游戏开始时，需要将其移动到对手牌库
		if self.zone == Zone.DECK:
			# 从己方牌库移除
			yield Destroy(SELF)
			# 洗入对手牌库
			yield Shuffle(OPPONENT, ExactCopy(SELF))
	
	def play(self):
		# 抽一张牌
		yield Draw(self.controller)
		
		# 将本牌洗回牌库
		yield Shuffle(self.controller, ExactCopy(SELF))


class TIME_875t2:
	"""弑君者 - The Kingslayers
	2费 3/2 武器
	在你的英雄攻击后，双方各抽一张传说卡牌。
	
	After your hero attacks, both players draw a Legendary card.
	
	由半兽人迦罗娜的Fabled机制添加到套牌中
	"""
	# 监听英雄攻击事件
	events = Attack(FRIENDLY_HERO).after(
		lambda self, source, target: [
			# 双方各抽一张传说卡牌
			ForceDraw(RANDOM(FRIENDLY_DECK + LEGENDARY)),
			ForceDraw(RANDOM(ENEMY_DECK + LEGENDARY)),
		]
	)


class TIME_036t1:
	"""获取复制 - Get a Copy (选项卡牌)
	
	王室线人的选项之一：获取对手手牌最右边卡牌的复制
	"""
	pass


class TIME_036t2:
	"""增加费用 - Increase Cost (选项卡牌)
	
	王室线人的选项之一：使对手手牌最右边的卡牌费用增加2点
	"""
	pass


# ========================================
# Shaman Tokens
# ========================================

class TIME_209t:
	"""高山之王的战锤 - High King's Hammer
	6费 3/4 武器，风怒
	亡语：将本武器洗入你的牌库，并永久获得+2攻击力。
	
	Deathrattle: Shuffle this into your deck with +2 Attack permanently.
	
	由高山之王穆拉丁的Fabled机制添加到套牌中
	
	完整实现：
	- 亡语触发时，先给自己添加 +2 攻击力的永久buff
	- 然后将带有buff的自己洗入牌库
	- 这样每次触发亡语都会累积攻击力
	"""
	tags = {
		GameTag.WINDFURY: True,
		GameTag.DEATHRATTLE: True,
	}
	
	def deathrattle(self):
		"""动态亡语：给自己加buff然后洗入牌库"""
		# 给自己添加 +2 攻击力的永久buff
		yield Buff(SELF, "TIME_209te")
		# 将自己洗入牌库（此时已经有了buff）
		yield Shuffle(CONTROLLER, ExactCopy(SELF))


class TIME_209te:
	"""高山之王的战锤 - 永久+2攻击力"""
	atk = 2


# ========================================
# Paladin Tokens
# ========================================

class TIME_017t:
	"""坦克 - Tank
	7/7 机械，圣盾
	
	由坦克机械师的亡语召唤的Token
	"""
	tags = {
		GameTag.DIVINE_SHIELD: True,
	}


class TIME_700t:
	"""时序龙 - Temporal Dragon
	3/5 龙，嘲讽
	
	由时序光环召唤的Token
	"""
	tags = {
		GameTag.TAUNT: True,
	}



# ========================================
# Priest Tokens
# ========================================

class TIME_890t:
	"""卡拉赞 - Karazhan
	3费 地标
	
	由圣者麦迪文的Fabled机制添加到套牌中
	每回合结束时，随机对一个敌人造成3点伤害。
	
	Karazhan is a Location added to your deck by Medivh the Hallowed's Fabled effect.
	At the end of your turn, deal 3 damage to a random enemy.
	"""
	tags = {
		GameTag.CARDTYPE: CardType.LOCATION,
		GameTag.HEALTH: 3,
	}
	
	# 每回合结束时触发效果
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 3))


# ========================================
# Neutral Tokens
# ========================================

class TIME_059t:
	"""悖论活体 - Living Paradox (Token)
	2/1 随从，扰魔
	
	由悖论活体召唤的Token
	"""
	tags = {
		GameTag.ELUSIVE: True,
	}


class TIME_434t:
	"""暗影 - Shadow
	4/1 随从
	
	由时空旅行者召唤的Token
	"""
	pass


# ========================================
# Warrior Tokens
# ========================================

class TIME_873t:
	"""鳄鱼 - Crocolisk
	2/3 野兽
	
	由"放出鳄鱼"为对手召唤的Token
	"""
	pass


class TIME_870t:
	"""老虎 - Tiger
	5/5 野兽，潜行
	
	由"角斗开战"为对手召唤的Token
	"""
	tags = {
		GameTag.STEALTH: True,
	}


class TIME_850t:
	"""血斗士 - Blood Fighter
	3费 3/3 随从
	
	由血斗士洛戈什的Fabled机制添加到套牌中
	这是一个基础随从，会被洛戈什的亡语召唤并强化
	"""
	pass

