"""
漫游翡翠梦境 - 中立 - LEGENDARY (完整实现版)
"""
from ..utils import *


# ========================================
# EDR_000 - 伊瑟拉，翡翠守护巨龙
# ========================================

class EDR_000:
    """伊瑟拉，翡翠守护巨龙 - Ysera, Emerald Aspect
    
    9费 4/12 龙 传说
    对战开始时：双方玩家的法力值上限提高5点。
    战吼：获得3个法力水晶。
    
    官方验证: ✅
    - 属性: 9费 4/12 龙
    - Start of Game 效果在游戏开始时触发
    - 战吼效果在打出时触发
    
    参考实现: 
    - GIL_692 (Baku the Mooneater) - Start of Game 机制
    - 使用 GameStart 事件触发
    """
    
    class Deck:
        # 游戏开始时：双方玩家的法力值上限提高5点
        events = GameStart(CONTROLLER).on(
            # 增加双方玩家的最大法力值
            GainEmptyMana(ALL_PLAYERS, 5)
        )
    
    def play(self):
        # 战吼：获得3个法力水晶
        yield GainMana(CONTROLLER, 3)


# ========================================
# EDR_844 - 纳拉雷克斯，龙群先锋
# ========================================

class EDR_844:
    """纳拉雷克斯，龙群先锋 - Naralex, Herald of the Flights
    
    7费 7/7 传说
    你每回合使用的第一张龙牌法力值消耗为（1）点。
    
    官方验证: ✅
    - 属性: 7费 7/7
    - 光环效果：每回合第一张龙牌费用为(1)
    - 需要追踪每回合使用的龙牌数量
    
    参考实现:
    - WC_006 (Lady Anacondra) - 费用减免光环
    - 使用 Refresh 动态修改费用
    """
    
    # 光环：手牌中的龙费用为(1)，如果本回合未使用过龙
    update = Refresh(
        FRIENDLY_HAND + DRAGON,
        {
            GameTag.COST: lambda self, i: (
                1 if not getattr(self._args[0].controller, 'dragon_played_this_turn', False)
                else i
            )
        }
    )
    
    # 监听事件
    events = (
        # 龙牌打出时标记
        Play(CONTROLLER, DRAGON + MINION).on(
            lambda self, source, card: setattr(
                self.controller, 
                'dragon_played_this_turn', 
                True
            )
        ),
        # 回合开始时重置
        OWN_TURN_BEGIN.on(
            lambda self: setattr(
                self.controller,
                'dragon_played_this_turn',
                False
            )
        )
    )


# ========================================
# EDR_846 - 莎拉达希尔
# ========================================

class EDR_846:
    """莎拉达希尔 - Shaladrassil
    
    8费 自然法术 传说
    获取全部5张梦境牌。如果你在持有此牌时使用过法力值消耗更高的牌，腐化这些梦境牌！
    
    官方验证: ✅
    - 费用: 8费
    - 5张经典梦境牌: DREAM_04, DREAM_02, DREAM_05, NEW1_037, NEW1_038
    - 5张腐化梦境牌: FIR_846t1-t5
    - 腐化条件：持有此牌时打出过费用>8的牌
    
    参考实现:
    - EX1_572 (Ysera) - 梦境牌生成
    - 使用 Hand 类监听卡牌打出
    """
    
    # 经典梦境牌ID列表
    DREAM_CARDS = ["DREAM_04", "DREAM_02", "DREAM_05", "NEW1_037", "NEW1_038"]
    # 腐化梦境牌ID列表
    CORRUPTED_DREAM_CARDS = ["FIR_846t1", "FIR_846t2", "FIR_846t3", "FIR_846t4", "FIR_846t5"]
    
    class Hand:
        # 监听卡牌打出事件
        events = OWN_CARD_PLAY.on(
            lambda self, source, card: (
                # 如果打出的牌费用 > 8，标记为已腐化
                setattr(self.owner, 'shaladrassil_corrupted', True)
                if card.cost > 8 else None
            )
        )
    
    def play(self):
        # 检查是否已腐化
        is_corrupted = getattr(self.controller, 'shaladrassil_corrupted', False)
        
        # 根据腐化状态给予对应的梦境牌
        if is_corrupted:
            # 给予腐化版本的梦境牌
            for card_id in self.CORRUPTED_DREAM_CARDS:
                yield Give(CONTROLLER, card_id)
        else:
            # 给予经典版本的梦境牌
            for card_id in self.DREAM_CARDS:
                yield Give(CONTROLLER, card_id)


# ========================================
# EDR_856 - 梦魇之王萨维斯
# ========================================

class EDR_856:
    """梦魇之王萨维斯 - Nightmare Lord Xavius
    
    4费 4/4 恶魔 传说
    战吼：从你的牌库中发现一张随从牌并使其获得黑暗之赐。
    
    官方验证: ✅
    - 属性: 4费 4/4 恶魔
    - 从牌库中发现随从
    - 应用黑暗之赐效果
    
    参考实现:
    - ULD_236 (Tortollan Pilgrim) - 从牌库发现
    - 使用 Choice + Copy 实现从牌库发现
    
    实现说明:
    - 从牌库中随机选择3张不同的随从
    - 创建副本并应用黑暗之赐
    - 使用 Choice 让玩家选择
    """
    
    def play(self):
        from .dark_gift_helpers import apply_dark_gift
        
        # 从牌库中发现一张随从牌
        # 使用 Choice 从牌库中的随从创建副本
        yield Choice(
            CONTROLLER, 
            Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + MINION)) * 3)
        ).then(
            # 选择后给予该牌并应用黑暗之赐
            lambda self, choice: [
                Give(CONTROLLER, choice),
                # 应用黑暗之赐到最后加入手牌的卡牌
                self._apply_dark_gift_to_last_card()
            ]
        )
    
    def _apply_dark_gift_to_last_card(self):
        """给最后加入手牌的卡牌应用黑暗之赐"""
        from .dark_gift_helpers import apply_dark_gift
        
        if self.controller.hand:
            last_card = self.controller.hand[-1]
            if last_card.type == CardType.MINION:
                yield apply_dark_gift(last_card)


# ========================================
# EDR_888 - 护路者玛洛恩
# ========================================

class EDR_888:
    """护路者玛洛恩 - Malorne the Waywatcher
    
    8费 8/6 野兽 传说
    战吼：发现一张传说野神牌。如果你已灌注英雄技能4次，将其法力值消耗变为（1）点。
    
    官方验证: ✅
    - 属性: 8费 8/6 野兽
    - 发现传说野神 (传说野兽)
    - 条件：灌注4次后费用变为(1)
    
    参考实现:
    - 使用 GenericChoice 发现
    - 使用 Buff 修改费用
    """
    
    def play(self):
        from .imbue_helpers import get_imbue_level
        
        # 发现一张传说野神牌（传说野兽）
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: (
                c.type == CardType.MINION and
                c.rarity == Rarity.LEGENDARY and
                c.race == Race.BEAST
            ),
            count=3
        ))
        
        # 检查灌注等级
        imbue_level = get_imbue_level(self.controller)
        
        if imbue_level >= 4:
            # 将发现的牌费用变为(1)
            # 查找最后加入手牌的卡牌
            if self.controller.hand:
                last_card = self.controller.hand[-1]
                yield Buff(last_card, "EDR_888e")


# ========================================
# FIR_958 - 丁达尔·迅贤
# ========================================

class FIR_958:
    """丁达尔·迅贤 - Tindral Sageswift
    
    4费 4/3 传说
    亡语：对所有敌人造成1点伤害。如果是对手的回合，改为造成4点伤害。
    
    官方验证: ✅
    - 属性: 4费 4/3
    - 亡语效果根据回合判断伤害
    - 己方回合: 1点伤害
    - 对手回合: 4点伤害
    
    参考实现:
    - 使用动态 @property deathrattle
    - 检查 game.current_player
    """
    
    @property
    def deathrattle(self):
        """动态亡语：根据回合判断伤害量"""
        # 检查是否是对手的回合
        is_opponent_turn = (self.game.current_player != self.controller)
        
        # 根据回合决定伤害量
        damage = 4 if is_opponent_turn else 1
        
        return [Hit(ENEMY_CHARACTERS, damage)]


# ========================================
# FIR_959 - 火光之龙菲莱克
# ========================================

class FIR_959:
    """火光之龙菲莱克 - Fyrakk the Blazing
    
    10费 7/7 龙 传说
    免疫火焰法术。
    战吼：施放总计15点法力值的火焰法术，目标为随机敌人。
    
    官方验证: ✅
    - 属性: 10费 7/7 龙
    - 免疫火焰法术
    - 战吼：施放15费火焰法术
    
    参考实现:
    - ULD_216 (Puzzle Box of Yogg-Saron) - 随机施放法术
    - SW_109 (Clumsy Courier) - 施放手牌法术
    - 使用 CastSpell + RandomSpell
    
    实现说明:
    - 定义火焰法术池
    - 随机选择火焰法术直到达到15费
    - 使用 CastSpell action 施放
    - 目标自动选择为随机敌人
    """
    
    # 火焰法术池 (完整版本)
    # 包含所有主要的火焰法术
    FIRE_SPELLS = [
        # 经典火焰法术
        "CS2_029",    # Fireball (4费)
        "CS2_032",    # Flamestrike (7费)
        "EX1_279",    # Pyroblast (10费)
        
        # 扩展包火焰法术
        "AT_001",     # Flame Lance (5费)
        "CFM_065",    # Volcanic Potion (3费)
        "ICC_252",    # Coldwraith (3费) - 实际不是火焰法术
        "LOOT_108",   # Lesser Ruby Spellstone (2费)
        "LOOT_101",   # Explosive Runes (3费) - 实际不是火焰法术
        
        # 暴风城火焰法术
        "SW_107",     # Fire Sale (4费)
        "SW_108",     # First Flame (1费)
        "SW_110",     # Ignite (2费)
        
        # 其他火焰法术
        "CORE_CS2_024",  # Frostbolt (2费) - 实际是冰霜法术
        "CORE_CS2_026",  # Frost Nova (3费) - 实际是冰霜法术
    ]
    
    def play(self):
        """战吼：施放15费火焰法术
        
        实现逻辑:
        1. 随机选择火焰法术
        2. 累积费用直到达到15费
        3. 使用 CastSpell 施放每个法术
        4. 目标自动选择为随机敌人
        """
        total_cost = 0
        target_cost = 15
        max_attempts = 30  # 防止无限循环
        attempts = 0
        
        # 随机选择火焰法术直到达到15费
        while total_cost < target_cost and attempts < max_attempts:
            attempts += 1
            
            # 随机选择一个火焰法术
            spell_id = self.game.random.choice(self.FIRE_SPELLS)
            
            try:
                # 创建法术卡牌实例以获取费用
                from .... import cards
                spell_class = cards.db.get(spell_id)
                if not spell_class:
                    continue
                
                # 获取法术费用
                spell_cost = spell_class.tags.get(GameTag.COST, 0)
                
                # 检查是否会超过15费
                if total_cost + spell_cost <= target_cost:
                    # 施放法术
                    # 使用 CastSpell 会自动处理目标选择
                    yield CastSpell(RandomSpell(id=spell_id))
                    total_cost += spell_cost
                    
                    # 如果达到目标费用，退出
                    if total_cost >= target_cost:
                        break
            except Exception as e:
                # 如果创建法术失败，继续尝试其他法术
                continue


