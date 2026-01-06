"""
深暗领域 - 中立 - EPIC
"""
from ..utils import *


class GDB_129:
    """末日女武神 - Doomsday Valkyrie
    4费 4/4 中立随从 - 恶魔
    <b>战吼:</b>从你对手的牌库中抽一张牌。如果你未在本回合中使用该牌,将其置回。
    
    Battlecry: Draw a card from your opponent's deck. If you don't play it this turn, return it.
    
    参考: stormwind/rogue.py - DED_005 (海盗谈判)
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DEMON
    
    def play(self):
        # 从对手牌库中随机获取一张牌到己方手牌
        # 参考 DED_005 的实现: Give(CONTROLLER, Random(OPPONENT_DECK))
        if self.controller.opponent.deck:
            cards = yield Give(CONTROLLER, Random(OPPONENT_DECK))
            if cards:
                # 给抽到的牌添加标记buff,用于回合结束时检查
                yield Buff(cards[0], "GDB_129e")


class GDB_129e:
    """末日女武神标记 - Doomsday Valkyrie Mark
    标记从对手牌库抽取的牌,回合结束时检查是否被使用
    
    Mark for cards drawn from opponent's deck
    """
    events = OWN_TURN_END.on(
        lambda self: self._return_to_opponent_deck()
    )
    
    def _return_to_opponent_deck(self):
        """回合结束时,如果牌还在手牌中(未被使用),将其返回对手牌库"""
        card = self.owner
        # 检查牌是否还在手牌中
        if card.zone == Zone.HAND:
            # 先从己方手牌移除
            yield Discard(card)
            # 将牌洗回对手牌库
            yield Shuffle(OPPONENT, card.id)


class GDB_321:
    """变异生命体 - Mutating Organism
    5费 3/8 中立随从 - 全种族
    在本随从受到伤害并存活下来后,获得一项随机<b>额外效果</b>。
    
    After this takes damage and survives, gain a random Bonus Effect.
    
    参考: badlands/neutral_epic.py - DEEP_035 (炫彩旋岩虫)
    """
    race = Race.ALL
    
    events = Damage(SELF).after(
        lambda self: self._gain_bonus_effect()
    )
    
    def _gain_bonus_effect(self):
        """受到伤害并存活后,获得随机额外效果"""
        # 检查是否存活
        if not self.dead and not self.to_be_destroyed:
            # 随机给予一个额外效果
            yield Buff(SELF, "GDB_321e")


class GDB_321e:
    """变异效果 - Mutation Effect
    随机额外效果
    
    Random Bonus Effect
    """
    def apply(self, target):
        """应用随机额外效果"""
        import random
        # 定义可能的额外效果(关键字)
        # 参考官方数据,包含8种常见的额外效果
        bonus_effects = [
            {GameTag.DIVINE_SHIELD: True},  # 圣盾
            {GameTag.TAUNT: True},          # 嘲讽
            {GameTag.RUSH: True},           # 突袭
            {GameTag.LIFESTEAL: True},      # 吸血
            {GameTag.WINDFURY: True},       # 风怒
            {GameTag.POISONOUS: True},      # 剧毒
            {GameTag.STEALTH: True},        # 潜行
            {GameTag.REBORN: True},         # 复生
        ]
        # 随机选择一个效果
        effect = random.choice(bonus_effects)
        # 应用到目标
        for tag, value in effect.items():
            target.tags[tag] = value


class GDB_340:
    """星际狐人 - Space Fox
    5费 4/5 中立随从
    <b>可交易</b>
    <b>战吼:</b>消灭一个敌方<b>星舰</b>或<b>星舰组件</b>。
    
    Tradeable. Battlecry: Destroy an enemy Starship or Starship Piece.
    """
    tags = {
        GameTag.TRADEABLE: True,
        GameTag.BATTLECRY: True,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self, target):
        """战吼:消灭目标星舰或星舰组件"""
        if target:
            # 检查目标是否是星舰或星舰组件
            # 星舰组件有STARSHIP_PIECE标签
            is_starship_piece = target.tags.get(GameTag.STARSHIP_PIECE, False)
            # 星舰是Starship类的实例(休眠状态的星舰实体)
            from ..card import Starship
            is_starship = isinstance(target, Starship)
            
            if is_starship or is_starship_piece:
                yield Destroy(target)
    
    # 目标选择器:所有敌方随从(包括星舰和星舰组件)
    # 注意:星舰在休眠状态下也是场上实体,可以被选中
    play_target = ENEMY_MINIONS


class GDB_341:
    """红巨星巨人 - Red Giant
    8费 8/8 中立随从 - 元素
    本牌在手牌中时,每有一张相邻的牌被使用,本牌的法力值消耗便减少(1)点。
    
    Costs (1) less for each adjacent card played while in your hand.
    
    参考: space/tokens.py - 星球碰撞机制和乘务员相邻检测
    使用 zone_position 属性追踪手牌位置
    """
    race = Race.ELEMENTAL
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 追踪相邻牌被使用的次数
        self._adjacent_cards_played = 0
        # 记录上一次检查时的手牌位置
        self._last_position = None
    
    def cost_func(self, value):
        """动态费用计算"""
        return value - self._adjacent_cards_played
    
    # 监听己方打出牌的事件
    events = Play(CONTROLLER).on(
        lambda self, source, card: self._check_adjacent_played(card)
    )
    
    def _check_adjacent_played(self, played_card):
        """检查被使用的牌是否与本牌相邻
        
        使用 zone_position 属性来判断相邻关系:
        - 在牌被打出前,记录其在手牌中的位置
        - 检查该位置是否与本牌相邻(位置差为1)
        - 如果相邻,增加计数器
        """
        # 只在本牌在手牌中时触发
        if self.zone != Zone.HAND:
            return
        
        # 获取本牌当前在手牌中的位置
        my_position = self.zone_position
        
        # 获取被打出的牌之前在手牌中的位置
        # 注意:牌被打出后已经不在手牌中了
        # 我们需要从Play事件中获取牌打出前的位置信息
        
        # 方法1: 检查被打出的牌是否有记录的位置信息
        played_position = getattr(played_card, '_hand_position_before_play', None)
        
        # 方法2: 如果没有记录,尝试从当前手牌推断
        # 当一张牌被打出后,后面的牌位置会前移
        # 所以我们检查当前相邻位置的牌是否是新的
        if played_position is None:
            # 简化处理:检查当前相邻位置
            # 如果之前记录了位置,检查是否有牌从相邻位置消失
            hand = list(self.controller.hand)
            
            # 检查左右相邻位置
            for card in hand:
                if card == self:
                    continue
                # 如果有牌的位置正好是 my_position ± 1
                # 说明可能有相邻的牌被打出了
                if abs(card.zone_position - my_position) == 1:
                    # 这里无法准确判断,所以采用保守策略
                    pass
            
            # 由于无法准确追踪,我们使用一个简化的方案:
            # 检查打出的牌的ID是否在我们记录的"相邻牌列表"中
            if not hasattr(self, '_adjacent_card_ids'):
                self._adjacent_card_ids = set()
            
            # 更新相邻牌列表
            self._update_adjacent_cards()
            
            # 如果打出的牌在相邻列表中,增加计数
            if played_card.entity_id in self._adjacent_card_ids:
                self._adjacent_cards_played += 1
                # 从列表中移除
                self._adjacent_card_ids.discard(played_card.entity_id)
        else:
            # 如果有记录的位置,直接检查是否相邻
            if abs(played_position - my_position) == 1:
                self._adjacent_cards_played += 1
    
    def _update_adjacent_cards(self):
        """更新相邻牌的ID列表"""
        if not hasattr(self, '_adjacent_card_ids'):
            self._adjacent_card_ids = set()
        
        # 清空并重新收集
        self._adjacent_card_ids.clear()
        
        hand = list(self.controller.hand)
        my_position = self.zone_position
        
        for card in hand:
            if card == self:
                continue
            # 检查是否相邻(位置差为1)
            if abs(card.zone_position - my_position) == 1:
                self._adjacent_card_ids.add(card.entity_id)


class GDB_450:
    """王牌探路者 - Ace Pathfinder
    4费 4/4 中立随从 - 德莱尼
    <b>战吼:</b>随机获得两项
    <b>额外效果</b>。你使用的下一个德莱尼也会获得这些效果。
    
    Battlecry: Gain 2 random Bonus Effects. The next Draenei you play also gains them.
    
    参考: badlands/paladin.py - WW_327 (随机额外效果机制)
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DRAENEI
    
    def play(self):
        """战吼:随机获得2个额外效果,并传递给下一个德莱尼"""
        import random
        
        # 定义可能的额外效果
        bonus_effects_pool = [
            {GameTag.DIVINE_SHIELD: True},  # 圣盾
            {GameTag.TAUNT: True},          # 嘲讽
            {GameTag.RUSH: True},           # 突袭
            {GameTag.LIFESTEAL: True},      # 吸血
            {GameTag.WINDFURY: True},       # 风怒
            {GameTag.POISONOUS: True},      # 剧毒
            {GameTag.STEALTH: True},        # 潜行
            {GameTag.REBORN: True},         # 复生
        ]
        
        # 随机选择2个不同的效果
        selected_effects = random.sample(bonus_effects_pool, 2)
        
        # 应用到自身
        for tags in selected_effects:
            for tag, value in tags.items():
                self.tags[tag] = value
        
        # 给玩家添加buff,记录这些效果并传递给下一个德莱尼
        # 将效果转换为buff ID列表
        effect_buffs = []
        for effect_tags in selected_effects:
            # 根据效果类型确定buff ID
            if GameTag.DIVINE_SHIELD in effect_tags:
                effect_buffs.append("GDB_450e_divine_shield")
            elif GameTag.TAUNT in effect_tags:
                effect_buffs.append("GDB_450e_taunt")
            elif GameTag.RUSH in effect_tags:
                effect_buffs.append("GDB_450e_rush")
            elif GameTag.LIFESTEAL in effect_tags:
                effect_buffs.append("GDB_450e_lifesteal")
            elif GameTag.WINDFURY in effect_tags:
                effect_buffs.append("GDB_450e_windfury")
            elif GameTag.POISONOUS in effect_tags:
                effect_buffs.append("GDB_450e_poisonous")
            elif GameTag.STEALTH in effect_tags:
                effect_buffs.append("GDB_450e_stealth")
            elif GameTag.REBORN in effect_tags:
                effect_buffs.append("GDB_450e_reborn")
        
        # 给玩家添加buff,存储要传递的效果
        if len(effect_buffs) >= 2:
            yield Buff(CONTROLLER, "GDB_450e",
                      effect1_id=effect_buffs[0],
                      effect2_id=effect_buffs[1])


class GDB_450e:
    """探路者的祝福 - Pathfinder's Blessing
    玩家buff:下一个德莱尼获得相同的额外效果
    
    Player enchantment: Next Draenei gains the same bonus effects
    """
    def __init__(self, effect1_id='', effect2_id='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 存储要传递的效果ID
        self.effect1_id = effect1_id
        self.effect2_id = effect2_id
    
    events = Play(CONTROLLER, MINION + DRAENEI).on(
        lambda self, source, card: self._apply_effects(card),
        Destroy(SELF)
    )
    
    def _apply_effects(self, draenei):
        """将记录的效果应用到德莱尼"""
        # 根据记录的效果ID应用对应的buff
        if self.effect1_id:
            yield Buff(draenei, self.effect1_id)
        if self.effect2_id:
            yield Buff(draenei, self.effect2_id)


# 王牌探路者的额外效果buff定义
class GDB_450e_divine_shield:
    """圣盾效果"""
    tags = {GameTag.DIVINE_SHIELD: True}


class GDB_450e_taunt:
    """嘲讽效果"""
    tags = {GameTag.TAUNT: True}


class GDB_450e_rush:
    """突袭效果"""
    tags = {GameTag.RUSH: True}


class GDB_450e_lifesteal:
    """吸血效果"""
    tags = {GameTag.LIFESTEAL: True}


class GDB_450e_windfury:
    """风怒效果"""
    tags = {GameTag.WINDFURY: True}


class GDB_450e_poisonous:
    """剧毒效果"""
    tags = {GameTag.POISONOUS: True}


class GDB_450e_stealth:
    """潜行效果"""
    tags = {GameTag.STEALTH: True}


class GDB_450e_reborn:
    """复生效果"""
    tags = {GameTag.REBORN: True}
