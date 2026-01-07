"""
失落之城 - PRIEST
"""
from ..utils import *
from hearthstone.enums import CardType, SpellSchool
from .kindred_helpers import check_kindred_active


# COMMON

class DINO_426:
	"""生命仪式 - Life Ritual
	<b>发现</b>一张法力值消耗为（3）的随从牌，召唤一个它的2/3的复制。
	
	2费 神圣法术
	Discover a 3-Cost minion. Summon a 2/3 copy of it.
	"""
	requirements = {}
	
	def play(self):
		# 发现一张3费随从牌
		cards = yield DISCOVER(RandomCollectible(type=CardType.MINION, cost=3))
		
		if cards:
			# 召唤发现的随从并设置为2/3
			yield Summon(CONTROLLER, cards[0]).then(Buff(Summon.CARD, "DINO_426e"))


class DINO_426e:
	"""生命仪式增益 - Life Ritual Buff"""
	atk = SET(2)
	max_health = SET(3)


class DINO_431:
	"""擎天雷龙 - Titanic Brontosaurus
	<b>嘲讽</b>。<b>亡语：</b>随机召唤一个法力值消耗大于或等于（5）点的<b>嘲讽</b>随从。
	
	8费 5/10 野兽
	Taunt. Deathrattle: Summon a random minion with Taunt that costs (5) or more.
	"""
	tags = {
		GameTag.TAUNT: True,
		GameTag.DEATHRATTLE: True,
	}
	
	deathrattle = Summon(CONTROLLER, RandomCollectible(
		type=CardType.MINION,
		min_cost=5,
		card_filter=lambda c: GameTag.TAUNT in c.tags
	))


class TLC_814:
	"""暮光治愈者 - Twilight Healer
	<b>亡语：</b>随机获取神圣和暗影法术牌各一张。
	
	3费 3/4 随从
	Deathrattle: Get a random Holy and Shadow spell.
	"""
	tags = {
		GameTag.DEATHRATTLE: True,
	}
	
	def deathrattle(self):
		# 获取一张随机神圣法术
		yield Give(CONTROLLER, RandomCollectible(
			type=CardType.SPELL,
			spell_school=SpellSchool.HOLY
		))
		# 获取一张随机暗影法术
		yield Give(CONTROLLER, RandomCollectible(
			type=CardType.SPELL,
			spell_school=SpellSchool.SHADOW
		))


class TLC_816:
	"""墓晨太阳花 - Gravebloom Sunflower
	抽两张牌。<b>延系：</b>本牌法力值消耗减少（2）点。
	
	4费 神圣法术
	Draw 2 cards. Kindred: This costs (2) less.
	
	实现说明:
	- 使用 Hand Aura 检查延系条件并动态调整费用
	- 延系条件:上回合打出过神圣法术
	"""
	requirements = {}
	
	def play(self):
		# 抽两张牌
		yield Draw(CONTROLLER) * 2
	
	class Hand:
		"""手牌光环:延系减费"""
		def _update_cost(self):
			# 检查延系是否激活(上回合打出过神圣法术)
			if check_kindred_active(
				self.owner.controller,
				card_type=CardType.SPELL,
				spell_school=SpellSchool.HOLY
			):
				# 减少2费
				self.owner.cost -= 2
			else:
				# 恢复原始费用
				self.owner.cost = self.owner.data.cost
		
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self._update_cost()
		
		events = (
			OWN_TURN_BEGIN.on(lambda self: self._update_cost()),
			AFTER_PLAY.on(lambda self, *args: self._update_cost()),
		)


class TLC_835:
	"""阿玛拉的故事 - Amara's Story
	将你英雄的生命值变为40。
	
	10费 法术
	Set your hero's Health to 40.
	
	任务奖励卡牌 from TLC_817 (寻求平衡)
	
	实现说明:
	- 参考 UNG_940t8 (希望守护者阿玛拉)
	- 设置英雄最大生命值为40
	"""
	requirements = {}
	
	play = Buff(FRIENDLY_HERO, "TLC_835e")


class TLC_835e:
	"""阿玛拉的故事增益 - Amara's Story Buff"""
	max_health = SET(40)


# RARE

class DINO_428:
	"""巨鳗面具 - Giant Eel Mask
	将一个随从的属性值变为8/10并使其获得<b>吸血</b>。随机迫使一个敌方随从攻击该随从。
	
	7费 法术
	Set a minion's stats to 8/10 and give it Lifesteal. Force a random enemy minion to attack it.
	"""
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	
	def play(self):
		# 将目标随从的属性值设置为8/10并给予吸血
		yield Buff(TARGET, "DINO_428e")
		
		# 随机选择一个敌方随从攻击目标
		enemy_minions = self.game.query(ENEMY_MINIONS)
		if enemy_minions and TARGET:
			import random
			attacker = random.choice(enemy_minions)
			# 迫使攻击
			yield Attack(attacker, TARGET)


class DINO_428e:
	"""巨鳗面具增益 - Giant Eel Mask Buff"""
	atk = SET(8)
	max_health = SET(10)
	tags = {GameTag.LIFESTEAL: True}


class TLC_815:
	"""墓晨虚空芽 - Gravebloom Void Bud
	随机召唤一个法力值消耗为（4）的随从并使其获得<b>嘲讽</b>。<b>延系：</b>重复一次。
	
	4费 暗影法术
	Summon a random 4-Cost minion with Taunt. Kindred: Do it again.
	
	实现说明:
	- 延系条件:上回合打出过暗影法术
	- 如果延系激活,召唤两次
	"""
	requirements = {}
	
	def play(self):
		# 检查延系是否激活
		kindred_count = check_kindred_active(
			self.controller,
			card_type=CardType.SPELL,
			spell_school=SpellSchool.SHADOW
		)
		
		# 召唤次数:基础1次 + 延系激活时额外1次
		summon_count = 1 + kindred_count
		
		for _ in range(summon_count):
			# 召唤一个4费随从并给予嘲讽
			yield Summon(CONTROLLER, RandomMinion(cost=4)).then(
				Buff(Summon.CARD, "TLC_815e")
			)


class TLC_815e:
	"""墓晨虚空芽增益 - Gravebloom Void Bud Buff"""
	tags = {GameTag.TAUNT: True}


class TLC_820:
	"""林地生态学者 - Woodland Ecologist
	<b>亡语：</b>获取一张法力值消耗为（1）的神圣法术牌，该牌可以使一个随从获得+2或-2生命值。
	
	1费 2/1 随从
	Deathrattle: Get a 1-Cost Holy spell that gives a minion +2 or -2 Health.
	
	实现说明:
	- 亡语获取 TLC_820t (林地祝福/诅咒)
	- 该法术是抉择牌:+2生命值 或 -2生命值
	"""
	tags = {
		GameTag.DEATHRATTLE: True,
	}
	
	deathrattle = Give(CONTROLLER, "TLC_820t")


class TLC_821:
	"""枯萎之影 - Withering Shadow
	<b>吸血</b>。每当你治疗一个敌人，本随从攻击该敌人。
	
	7费 6/7 元素
	Lifesteal. Whenever you heal an enemy, this attacks it.
	
	实现说明:
	- 监听治疗事件
	- 如果治疗目标是敌方角色,则攻击该目标
	- 参考 badlands/neutral_legendary.py - WW_819 (治疗触发攻击)
	"""
	tags = {
		GameTag.LIFESTEAL: True,
	}
	
	# 监听治疗事件
	events = Heal.on(
		lambda self, source, target, amount: (
			# 检查是否是己方治疗敌方
			Attack(SELF, target)
			if source.controller == self.controller and target.controller != self.controller
			else None
		)
	)


# EPIC

class TLC_818:
	"""轮回转生 - Reincarnation Cycle
	复活法力值消耗为1，2，3的随从各一个，使其获得<b>复生</b>。
	
	6费 暗影法术
	Resurrect a 1, 2, and 3-Cost minion. Give them Reborn.
	
	实现说明:
	- 从墓地中分别复活1费、2费、3费的随从各一个
	- 给予复生效果
	- 参考 stormwind/priest.py - SW_316 (复活指定费用随从)
	"""
	requirements = {}
	
	def play(self):
		# 复活1费、2费、3费随从各一个
		for cost in [1, 2, 3]:
			# 从墓地中筛选对应费用的随从
			dead_minions = [
				card for card in self.controller.graveyard
				if card.type == CardType.MINION and card.cost == cost
			]
			
			if dead_minions:
				# 随机选择一个复活
				import random
				chosen = random.choice(dead_minions)
				# 召唤复制并给予复生
				yield Summon(CONTROLLER, chosen.id).then(
					Buff(Summon.CARD, "TLC_818e")
				)


class TLC_818e:
	"""轮回转生增益 - Reincarnation Cycle Buff"""
	tags = {GameTag.REBORN: True}


class TLC_819:
	"""林歌海妖 - Siren of the Woodsong
	<b>吸血</b>。如果你在本回合中使用过神圣和暗影法术牌，本牌的法力值消耗为（1）点。
	
	6费 4/7 娜迦
	Lifesteal. Costs (1) if you've cast a Holy and Shadow spell this turn.
	
	实现说明:
	- 使用 Hand Aura 检查本回合是否使用过神圣和暗影法术
	- 如果两种都使用过,费用变为1
	"""
	tags = {
		GameTag.LIFESTEAL: True,
	}
	
	class Hand:
		"""手牌光环:条件减费"""
		def _update_cost(self):
			# 检查本回合使用的法术
			# 需要检查是否使用过神圣法术和暗影法术
			has_holy = False
			has_shadow = False
			
			# 遍历本回合使用的卡牌
			for card_id in getattr(self.owner.controller, 'cards_played_this_turn', []):
				try:
					from .. import db
					card_data = db[card_id]
					
					# 检查是否是法术
					if card_data.type == CardType.SPELL:
						# 检查法术学派
						if hasattr(card_data, 'spell_school'):
							if card_data.spell_school == SpellSchool.HOLY:
								has_holy = True
							elif card_data.spell_school == SpellSchool.SHADOW:
								has_shadow = True
				except KeyError:
					continue
			
			# 如果两种法术都使用过,费用变为1
			if has_holy and has_shadow:
				self.owner.cost = 1
			else:
				# 恢复原始费用
				self.owner.cost = self.owner.data.cost
		
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self._update_cost()
		
		events = (
			OWN_SPELL_PLAY.after(lambda self, *args: self._update_cost()),
			OWN_TURN_BEGIN.on(lambda self: self._update_cost()),
		)


# LEGENDARY

class TLC_811:
	"""阿凯欧斯 - Akeos
	每当另一个友方随从攻击时，将其生命值变为与本随从相同。
	
	3费 1/6 野兽
	Whenever another friendly minion attacks, set its Health equal to this minion's.
	
	实现说明:
	- 监听友方随从攻击事件
	- 将攻击者的生命值设置为与本随从相同
	- 注意:是设置当前生命值,不是最大生命值
	"""
	# 监听友方随从攻击事件
	events = Attack.on(
		lambda self, source, target: (
			# 检查是否是其他友方随从攻击
			SetCurrentHealth(source, SELF.health)
			if source != SELF and source.controller == self.controller and source.type == CardType.MINION
			else None
		)
	)


class TLC_817:
	"""寻求平衡 - Seeking Balance
	<b>任务：</b>施放4个神圣法术。<b>奖励：</b>生命之息。<b>任务：</b>施放4个暗影法术。<b>奖励：</b>死亡之触。
	
	1费 传说法术 - 任务
	Quest: Cast 4 Holy spells. Reward: Breath of Life.
	Quest: Cast 4 Shadow spells. Reward: Touch of Death.
	
	实现说明:
	- 双任务系统:需要完成两个独立的任务
	- 任务1:施放4个神圣法术,奖励 TLC_817t1 (生命之息)
	- 任务2:施放4个暗影法术,奖励 TLC_817t2 (死亡之触)
	- 使用 Player buff 追踪进度
	- 参考 ungoro/priest.py - UNG_940 (任务系统)
	
	注意:
	- 这是一个特殊的双任务卡牌
	- 不能使用标准的 progress_total/quest/reward 属性
	- 需要手动实现双任务追踪
	"""
	tags = {
		GameTag.QUEST: True,
	}
	requirements = {}
	
	def play(self):
		# 给玩家添加任务追踪 buff
		yield Buff(CONTROLLER, "TLC_817e")


# ========================================
# Buff 和 Token 定义
# ========================================

class TLC_817e:
	"""寻求平衡任务追踪 - Seeking Balance Quest Tracker
	
	追踪两个任务的进度:
	- 神圣法术计数
	- 暗影法术计数
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 初始化计数器
		self.holy_count = 0
		self.shadow_count = 0
		self.holy_completed = False
		self.shadow_completed = False
	
	# 监听法术施放事件
	events = OWN_SPELL_PLAY.after(
		lambda self, player, card, *args: self._on_spell_play(card)
	)
	
	def _on_spell_play(self, card):
		"""法术施放时检查学派并更新计数"""
		# 检查法术学派
		if hasattr(card, 'spell_school'):
			if card.spell_school == SpellSchool.HOLY and not self.holy_completed:
				# 神圣法术计数+1
				self.holy_count += 1
				if self.holy_count >= 4:
					# 完成神圣任务,给予奖励
					self.holy_completed = True
					yield Give(CONTROLLER, "TLC_817t1")
			
			elif card.spell_school == SpellSchool.SHADOW and not self.shadow_completed:
				# 暗影法术计数+1
				self.shadow_count += 1
				if self.shadow_count >= 4:
					# 完成暗影任务,给予奖励
					self.shadow_completed = True
					yield Give(CONTROLLER, "TLC_817t2")
