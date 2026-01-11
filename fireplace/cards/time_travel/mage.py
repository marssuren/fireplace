"""
穿越时间流 - MAGE
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_006:
    """镜像维度 - Mirror Dimension
    召唤一个0/4并具有嘲讽的随从。如果你的手牌中有龙牌，再召唤一个。
    
    Summon a 0/4 minion with Taunt. If you are holding a Dragon, summon another.
    """
    requirements = {}
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 召唤第一个0/4嘲讽随从
            yield Summon(self.controller, "TIME_006t")

            # 检查手牌中是否有龙
            has_dragon = False
            for card in self.controller.hand:
                if hasattr(card, 'race') and card.race == Race.DRAGON:
                    has_dragon = True
                    break

            # 如果有龙，再召唤一个
            if has_dragon:
                yield Summon(self.controller, "TIME_006t")

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_855:
    """奥术弹幕 - Arcane Barrage
    对一个敌人造成$3点伤害，并随机对两个其他敌人造成$2点伤害。
    
    Deal $3 damage to an enemy and $2 damage to two other random ones.
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0}
    
    def play(self):
        # 对目标造成3点伤害
        yield Hit(TARGET, 3)
        
        # 对两个其他随机敌人造成2点伤害
        # 使用 fireplace 的 RANDOM 选择器
        yield Hit(RANDOM(ENEMY_CHARACTERS - TARGET), 2)
        yield Hit(RANDOM(ENEMY_CHARACTERS - TARGET), 2)


class TIME_856:
    """艾杰斯亚导师 - Algeth'ar Instructor
    法术伤害+2
    
    Spell Damage +2
    """
    # 法术伤害在卡牌定义中通过 spellDamage 标签实现
    # 这里不需要额外的脚本
    pass


# RARE

class TIME_000:
    """半稳定的传送门 - Semi-Stable Portal
    回溯。随机将一张随从牌置入你的手牌。该牌的法力值消耗减少（3）点。
    
    Rewind. Add a random minion to your hand. It costs (3) less.
    """
    requirements = {}
    
    def play(self):
        # 随机获取一张随从牌并减少3费
        card = yield Give(self.controller, RandomMinion())
        if card:
            yield Buff(card, "TIME_000e")

class TIME_000e:
    """半稳定的传送门 - 减少3费"""
    cost = -3


class TIME_857:
    """操控时间 - Alter Time
    发现两张来自过去的奥术法术牌，其法力值消耗减少（2）点。
    
    Discover two Arcane spells from the past. They cost (2) less.
    """
    requirements = {}
    
    def play(self):
        # 发现第一张奥术法术
        card1 = yield Discover(self.controller, RandomSpell(spell_school=SpellSchool.ARCANE))
        if card1:
            yield Buff(card1, "TIME_857e")
        
        # 发现第二张奥术法术
        card2 = yield Discover(self.controller, RandomSpell(spell_school=SpellSchool.ARCANE))
        if card2:
            yield Buff(card2, "TIME_857e")


class TIME_857e:
    """操控时间 - 减少2费"""
    cost = -2


class TIME_858:
    """时空构造体 - Temporal Construct
    战吼：对一个敌方随从造成5点伤害，然后抽牌，数量等同于超过目标生命值的伤害。
    
    Battlecry: Deal 5 damage to an enemy minion. Draw cards equal to the excess damage.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        if self.target:
            # 记录目标当前生命值
            target_health = self.target.health
            
            # 造成5点伤害
            yield Hit(self.target, 5)
            
            # 计算超出伤害（5 - 目标生命值）
            excess_damage = max(0, 5 - target_health)
            
            # 抽取等量的牌
            for _ in range(excess_damage):
                yield Draw(self.controller)


# EPIC

class TIME_859:
    """异化 - Anomalize
    随机召唤法力值消耗为（10）和（1）的随从各一个，打乱其属性值。
    
    Summon a random 10 and 1-Cost minion. Scramble their stats.
    """
    requirements = {}
    
    def play(self):
        # 召唤一个10费随从
        minion_10 = yield Summon(self.controller, RandomMinion(cost=10))
        
        # 召唤一个1费随从
        minion_1 = yield Summon(self.controller, RandomMinion(cost=1))
        
        # 打乱属性值:根据炉石的"Scramble"机制,交换两个随从的攻击力和生命值
        if minion_10 and minion_1:
            # 获取原始属性
            atk_10 = minion_10[0].atk if isinstance(minion_10, list) else minion_10.atk
            health_10 = minion_10[0].health if isinstance(minion_10, list) else minion_10.health
            atk_1 = minion_1[0].atk if isinstance(minion_1, list) else minion_1.atk
            health_1 = minion_1[0].health if isinstance(minion_1, list) else minion_1.health
            
            m10 = minion_10[0] if isinstance(minion_10, list) else minion_10
            m1 = minion_1[0] if isinstance(minion_1, list) else minion_1
            
            # 交换属性:将10费随从设置为1费随从的属性,反之亦然
            yield SetTag(m10, {GameTag.ATK: atk_1, GameTag.HEALTH: health_1})
            yield SetTag(m1, {GameTag.ATK: atk_10, GameTag.HEALTH: health_10})


class TIME_860:
    """神秘无面者 - Faceless Enigma
    战吼：检视2个随机奥秘，选择其中一个为你自己施放，另一个为你的对手施放。
    
    Battlecry: Look at 2 random Secrets. Pick one to cast for yourself. The other casts for your opponent.
    """
    requirements = {}
    
    def play(self):
        # 生成两个随机奥秘供选择
        # 使用 RandomSecret 获取奥秘牌
        
        # 生成两个随机奥秘ID
        secret_1 = RandomSecret()
        secret_2 = RandomSecret()
        
        # 让玩家选择一个
        choice = yield GenericChoice(
            self.controller,
            cards=[secret_1, secret_2]
        )
        
        if choice:
            # 获取选择的奥秘ID
            chosen_secret_id = choice[0]
            
            # 确定另一个奥秘ID
            other_secret_id = secret_2 if chosen_secret_id == secret_1 else secret_1
            
            # 为自己施放选择的奥秘
            # 参考 nathria/mage.py 的 CastSpell 实现
            yield Play(self.controller, chosen_secret_id)
            
            # 为对手施放另一个奥秘
            yield Play(self.controller.opponent, other_secret_id)


# LEGENDARY

class TIME_852:
    """碧蓝女王辛达苟萨 - Azure Queen Sindragosa
    奇闻。如果你控制着其他龙，你的奥术法术的法力值消耗减少（2）点。
    
    Fabled. If you control another Dragon, your Arcane spells cost (2) less.
    """
    # Fabled 机制在套牌构建时处理
    # 光环效果：如果控制其他龙，奥术法术减2费
    # 参考 the_lost_city/mage.py 的 cost_mod 实现
    
    # 使用 Aura 实现光环效果
    # 当场上有其他龙时，给手牌中的奥术法术减2费
    update = Refresh(FRIENDLY_HAND + SPELL, {
        GameTag.COST: lambda self, i: (
            -2 if (
                # 检查是否有其他龙在场
                any(m.race == Race.DRAGON and m != self.owner for m in self.owner.controller.field)
                # 检查是否为奥术法术
                and hasattr(i, 'spell_school') and i.spell_school == SpellSchool.ARCANE
            ) else 0
        )
    })


class TIME_861:
    """时光循环者托奇 - Timelooper Toki
    战吼：随机获取3张来自过去的法术牌。当你使用了全部3张法术牌，再获取一张时光循环者托奇。
    
    Battlecry: Get 3 random spells from the past. When you play ALL 3, get another Timelooper Toki.
    """
    requirements = {}
    
    def play(self):
        # 随机获取3张法术牌
        # 给这些法术添加标记，用于追踪
        for _ in range(3):
            card = yield Give(self.controller, RandomSpell())
            
            # 给这些法术添加标记buff
            if card:
                yield Buff(card, "TIME_861e")
        
        # 初始化追踪计数器
        # 在玩家对象上存储追踪信息
        if not hasattr(self.controller, 'toki_spells_remaining'):
            self.controller.toki_spells_remaining = 0
        
        # 增加需要打出的法术数量
        self.controller.toki_spells_remaining += 3


class TIME_861e:
    """时光循环者托奇 - 法术标记"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 监听法术打出事件
    # 当这张法术被打出时，减少计数器
    events = Play(OWNER).on(
        lambda self, source: self._on_spell_played()
    )
    
    def _on_spell_played(self):
        """当标记的法术被打出时触发"""
        actions = []
        
        # 减少计数器
        if hasattr(self.controller, 'toki_spells_remaining'):
            self.controller.toki_spells_remaining = max(0, self.controller.toki_spells_remaining - 1)
            
            # 检查是否所有法术都已打出
            if self.controller.toki_spells_remaining == 0:
                # 给予一张新的托奇
                actions.append(Give(self.controller, "TIME_861"))
                # 重置计数器
                self.controller.toki_spells_remaining = 0
        
        # 移除这个buff（法术已经打出）
        actions.append(Destroy(self))
        
        return actions
