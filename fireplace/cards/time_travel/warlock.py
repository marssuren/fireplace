"""
穿越时间流 - WARLOCK
"""
from ..utils import *
from .rewind_helpers import create_rewind_point


# COMMON

class TIME_025:
	"""暮光时空跃迁者 - Twilight Timehopper
	2费 4/4 龙
	**战吼：**将2张时空撕裂洗入你的牌库。抽到时空撕裂时会对你的英雄造成3点伤害。
	
	Battlecry: Shuffle 2 Shreds of Time into your deck. When drawn, deal 3 damage to your hero.
	
	时空撕裂是 Warlock 的核心机制，是一张"抽到时施放"的法术，会对英雄造成3点伤害并抽一张牌。
	"""
	requirements = {}
	
	def play(self):
		# 战吼：将2张时空撕裂洗入牌库
		yield Shuffle(self.controller, "TIME_025t")
		yield Shuffle(self.controller, "TIME_025t")


class TIME_027:
	"""超光子弹幕 - Tachyon Barrage
	2费 法术
	造成$6点伤害，随机分配到所有敌人身上。将2张时空撕裂洗入你的牌库。
	
	Deal $6 damage split among all enemies. Shuffle 2 Shreds of Time into your deck.
	
	这是一张AOE伤害法术，同时会洗入时空撕裂。
	注意：ImmuneToSpellpower 标签表示不受法术伤害加成影响。
	
	"split among" 效果的实现：
	- 随机分配6点伤害到所有敌人身上
	- 每次随机选择一个敌人造成1点伤害，重复6次
	"""
	requirements = {}
	
	def play(self):
		# 造成6点伤害，随机分配到所有敌人身上
		# 参考 kobolds/neutral_common.py 和其他 "split among" 实现
		for _ in range(6):
			yield Hit(RANDOM(ENEMY_CHARACTERS), 1)
		
		# 将2张时空撕裂洗入牌库
		yield Shuffle(self.controller, "TIME_025t")
		yield Shuffle(self.controller, "TIME_025t")


class TIME_029:
	"""灾毁迅疾幼龙 - Ruinous Velocidrake
	5费 5/5 龙
	**突袭。战吼：**从你的牌库中施放一张时空撕裂以召唤一个本随从的复制。
	
	Rush. Battlecry: Cast a Shred of Time from your deck to summon a copy of this.
	
	这张卡的效果是：
	1. 从牌库中找到时空撕裂并施放（造成3点伤害并抽牌）
	2. 如果成功施放，召唤一个自身的复制
	"""
	requirements = {}
	
	def play(self):
		# 从牌库中找到时空撕裂
		shred = None
		for card in self.controller.deck:
			if card.id == "TIME_025t":
				shred = card
				break
		
		if shred:
			# 施放时空撕裂（从牌库中）
			# 时空撕裂的效果：对英雄造成3点伤害，抽一张牌
			yield Hit(self.controller.hero, 3)
			yield Draw(self.controller)
			
			# 从牌库中移除时空撕裂
			yield Destroy(shred)
			
			# 召唤一个本随从的复制
			yield Summon(self.controller, ExactCopy(SELF))


# RARE

class TIME_026:
	"""续连熵能 - Entropic Continuity
	1费 法术
	使你的随从获得+1/+1。将2张时空撕裂洗入你的牌库。
	
	Give your minions +1/+1. Shuffle 2 Shreds of Time into your deck.
	
	简单的buff法术，同时洗入时空撕裂。
	"""
	requirements = {}
	
	def play(self):
		# 给所有友方随从+1/+1
		yield Buff(FRIENDLY_MINIONS, "TIME_026e")
		
		# 将2张时空撕裂洗入牌库
		yield Shuffle(self.controller, "TIME_025t")
		yield Shuffle(self.controller, "TIME_025t")


class TIME_026e:
	"""续连熵能 - +1/+1"""
	atk = 1
	max_health = 1


class TIME_028:
	"""破命之龙 - Fatebreaker
	4费 4/4 龙
	**吸血。战吼：**从你的牌库中施放一张时空撕裂以获得+3/+3。
	
	Lifesteal. Battlecry: Cast a Shred of Time from your deck to gain +3/+3.
	
	类似于 TIME_029，但效果是获得+3/+3而不是召唤复制。
	"""
	requirements = {}
	
	def play(self):
		# 从牌库中找到时空撕裂
		shred = None
		for card in self.controller.deck:
			if card.id == "TIME_025t":
				shred = card
				break
		
		if shred:
			# 施放时空撕裂（从牌库中）
			yield Hit(self.controller.hero, 3)
			yield Draw(self.controller)
			
			# 从牌库中移除时空撕裂
			yield Destroy(shred)
			
			# 获得+3/+3
			yield Buff(SELF, "TIME_028e")


class TIME_028e:
	"""破命之龙 - +3/+3"""
	atk = 3
	max_health = 3


class TIME_031:
	"""拉法姆人梯 - RAFAAM LADDER!!
	4费 法术
	抽三张法力值消耗不同的牌。
	
	Draw 3 cards of different Costs.
	
	这张卡的效果是抽3张费用各不相同的牌。
	实现方式：
	1. 从牌库中找到所有费用不同的牌
	2. 随机选择3张费用不同的牌抽取
	
	参考实现：whizbang/priest.py 中的类似逻辑
	"""
	requirements = {}
	
	def play(self):
		# 获取牌库中所有卡牌
		deck_cards = list(self.controller.deck)
		
		if not deck_cards:
			return
		
		# 按费用分组
		cards_by_cost = {}
		for card in deck_cards:
			cost = card.cost
			if cost not in cards_by_cost:
				cards_by_cost[cost] = []
			cards_by_cost[cost].append(card)
		
		# 随机选择3个不同费用的组
		import random
		available_costs = list(cards_by_cost.keys())
		
		if len(available_costs) == 0:
			return
		
		# 最多抽3张
		num_to_draw = min(3, len(available_costs))
		selected_costs = random.sample(available_costs, num_to_draw)
		
		# 从每个费用组中随机选择一张牌抽取
		for cost in selected_costs:
			cards_in_cost = cards_by_cost[cost]
			card_to_draw = random.choice(cards_in_cost)
			# 使用标准的 Draw action，直接传入卡牌实例
			yield Draw(self.controller, card_to_draw)


# EPIC

class TIME_008:
	"""过去的末日宣言者 - Bygone Doomspeaker
	3费 3/3 随从
	**回溯。战吼：**双方玩家各随机弃一张牌。
	
	Rewind. Battlecry: Both players discard a random card.
	
	回溯机制允许玩家对随机结果不满意时重新来过。
	"""
	requirements = {}
	
	def play(self):
		# 1. 创建回溯点
		create_rewind_point(self.game)
		
		# 2. 双方各随机弃一张牌
		# 己方弃牌
		if self.controller.hand:
			yield Discard(RANDOM(FRIENDLY_HAND))
		
		# 对手弃牌
		if self.controller.opponent.hand:
			yield Discard(RANDOM(ENEMY_HAND))


class TIME_030:
	"""裂解术 - Divergence
	5费 暗影法术
	随机将你手牌中的一张随从牌拆成两半。
	
	Split a random minion in your hand into two halves.
	
	这张卡的效果是将一张随从拆成两个较小的随从。
	实现方式：
	1. 随机选择手牌中的一张随从
	2. 将其属性（攻击力和生命值）分成两半
	3. 生成两张新的随从卡牌
	
	实现说明：
	- 原随从的属性减半
	- 复制一张相同的随从（也是减半后的属性）
	- 使用负值 buff 来减少属性
	"""
	requirements = {}
	
	def play(self):
		# 获取手牌中的所有随从
		minions_in_hand = [
			card for card in self.controller.hand
			if card.type == CardType.MINION
		]
		
		if not minions_in_hand:
			return
		
		# 随机选择一张随从
		import random
		target_minion = random.choice(minions_in_hand)
		
		# 获取原始属性
		original_atk = target_minion.atk
		original_health = target_minion.health
		
		# 计算分割后的属性（向下取整）
		half_atk = original_atk // 2
		half_health = original_health // 2
		
		# 确保至少为1
		half_atk = max(1, half_atk)
		half_health = max(1, half_health)
		
		# 计算需要减少的数值
		atk_reduction = original_atk - half_atk
		health_reduction = original_health - half_health
		
		# 给原随从添加负值buff来减少属性
		# 使用标准的 buff 系统
		if atk_reduction > 0 or health_reduction > 0:
			# 创建一个临时的 buff 类来存储减少的数值
			# 由于 fireplace 的限制，我们直接使用固定的 buff
			# 然后在 buff 中动态计算
			yield Buff(target_minion, "TIME_030e")
			# 手动设置 buff 的属性（这是一个 workaround）
			if target_minion.buffs:
				last_buff = target_minion.buffs[-1]
				last_buff.atk = -atk_reduction
				last_buff.max_health = -health_reduction
		
		# 复制一张相同的随从（也是一半属性）
		yield Give(self.controller, ExactCopy(target_minion))


class TIME_030e:
	"""裂解术 - 属性修改
	
	这个 buff 用于减少随从的属性。
	由于 fireplace 的 buff 系统限制，我们在应用后手动设置属性值。
	"""
	# 默认值为0，实际值在 play 方法中动态设置
	atk = 0
	max_health = 0


# LEGENDARY

class TIME_005:
	"""时空大盗拉法姆 - Timethief Rafaam
	10费 10/10 传说随从
	**奇闻+**
	你的套牌容量为40，但其中有10张拉法姆！**战吼：**如果你使用过其余拉法姆，消灭敌方英雄。
	
	Fabled+. Your deck size is 40, but has 10 Rafaams! Battlecry: If you played the rest, destroy the enemy hero.
	
	Fabled+ 机制说明：
	- 这是一个特殊的 Fabled 变体
	- 套牌容量扩展到40张
	- 其中包含10张拉法姆（TIME_005）
	- 战吼效果：如果已经打出了其他9张拉法姆，直接消灭敌方英雄
	
	实现说明：
	- 需要追踪已经打出的拉法姆数量
	- 使用 Player 的自定义属性来追踪
	"""
	requirements = {}
	
	def play(self):
		# 检查已经打出的拉法姆数量
		# 使用 controller 的自定义属性追踪
		if not hasattr(self.controller, 'rafaams_played'):
			self.controller.rafaams_played = 0
		
		# 增加已打出的拉法姆数量
		self.controller.rafaams_played += 1
		
		# 如果已经打出了10张拉法姆（包括当前这张）
		# 注意：题目说"如果你使用过其余拉法姆"，意思是其他9张
		# 所以当 rafaams_played == 10 时触发
		if self.controller.rafaams_played >= 10:
			# 消灭敌方英雄
			yield Destroy(ENEMY_HERO)


class TIME_032:
	"""克洛诺戈尔 - Chronogor
	6费 6/7 龙
	**战吼：**你抽取你法力值消耗最高的两张牌，你的对手抽取你法力值消耗最低的两张牌。
	
	Battlecry: You draw your 2 highest Cost cards. Your opponent draws your 2 lowest Cost cards.
	
	这是一个非常特殊的抽牌效果：
	1. 玩家抽取自己牌库中费用最高的2张牌
	2. 对手抽取玩家牌库中费用最低的2张牌
	
	注意：对手抽取的是"你的"牌库中的牌，所以需要从己方牌库移动到对手手牌。
	"""
	requirements = {}
	
	def play(self):
		# 获取牌库中的所有卡牌
		deck_cards = list(self.controller.deck)
		
		if not deck_cards:
			return
		
		# 按费用排序
		sorted_by_cost = sorted(deck_cards, key=lambda card: card.cost)
		
		# 玩家抽取费用最高的2张牌
		highest_cost_cards = sorted_by_cost[-2:] if len(sorted_by_cost) >= 2 else sorted_by_cost
		for card in reversed(highest_cost_cards):  # 从高到低抽取
			yield Draw(self.controller, card)
		
		# 对手抽取费用最低的2张牌
		# 注意：需要重新获取牌库（因为上面已经抽了牌）
		deck_cards = list(self.controller.deck)
		if deck_cards:
			sorted_by_cost = sorted(deck_cards, key=lambda card: card.cost)
			lowest_cost_cards = sorted_by_cost[:2] if len(sorted_by_cost) >= 2 else sorted_by_cost
			for card in lowest_cost_cards:
				# 将这些牌从己方牌库移到对手手牌
				# 使用 Give action 将牌给对手
				# 首先从牌库中移除
				yield Destroy(card)
				# 然后给对手一张复制
				yield Give(self.controller.opponent, ExactCopy(card))
