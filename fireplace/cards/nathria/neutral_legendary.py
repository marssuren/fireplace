"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_033:
    """Sylvanas, the Accused - 被告希尔瓦娜斯
    [x]<b>Battlecry:</b> Destroy
an enemy minion.
<b>Infuse (7):</b> Take control
of it instead.
    <b>战吼：</b>消灭一个敌方随从。<b>注能(7)：</b>改为控制它。
    """
    infuse = 7
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        if self.infused:
            # 注能后：控制目标随从
            yield Steal(TARGET)
        else:
            # 未注能：消灭目标随从
            yield Destroy(TARGET)


class MAW_034:
    """The Jailer - 典狱长
    <b>Battlecry:</b> Destroy your deck. This minion
gains <b>Immune</b>.
    <b>战吼：</b>摧毁你的牌库。本随从获得<b>免疫</b>。
    """
    def play(self):
        # 摧毁牌库中的所有卡牌
        yield Destroy(FRIENDLY_DECK)
        # 获得免疫
        yield Buff(SELF, "MAW_034e")


class MAW_034e:
    """The Jailer Buff - 典狱长增益"""
    tags = {GameTag.IMMUNE: True}


class REV_018:
    """Prince Renathal - 雷纳索尔王子
    Your deck size and
starting Health are 40.
    你的牌库容量和起始生命值为40点。
    """
    # 这是一个特殊的卡牌，需要在构建套牌时生效
    # 在 fireplace 中，这种效果通常在游戏开始前处理
    # 这里我们提供一个占位实现，实际效果需要在套牌构建器中处理
    # 
    # 正确的实现方式：
    # 1. 在套牌构建时检查是否包含此卡
    # 2. 如果包含，允许套牌最多40张卡（而非30张）
    # 3. 游戏开始时，英雄生命值设为40（而非30）
    #
    # 由于这是构建时效果，在游戏中打出此卡不会有任何效果
    pass


class REV_021:
    """Kael'thas Sinstrider - 逐罪者凯尔萨斯
    Every third minion you play each turn costs (0).
    你每回合打出的第三个随从的法力值消耗为(0)点。
    """
    # 光环效果：检查本回合打出的随从数量
    # 如果下一个随从是第三个，则费用为0
    class Hand:
        def cost_mod(self, source, game):
            # 获取控制者本回合已打出的随从数量
            controller = source.controller
            minions_played = controller.minions_played_this_turn
            
            # 如果下一个是第三个随从（已打出2个）
            if minions_played == 2:
                return -source.cost
            
            # 如果下一个是第六个随从（已打出5个）
            if minions_played == 5:
                return -source.cost
            
            # 如果下一个是第九个随从（已打出8个）
            if minions_played == 8:
                return -source.cost
            
            return 0


class REV_022:
    """Murloc Holmes - 摩洛克·福尔摩斯
    [x]<b>Battlecry:</b> Solve 3 Clues 
about your opponent's cards 
to get copies of them.
    <b>战吼：</b>解开3个关于对手卡牌的线索，获得它们的复制。
    """
    # 正确机制（基于搜索结果）：
    # 线索1：哪张卡在对手的起始手牌中？
    # 线索2：哪张卡当前在对手手牌中？
    # 线索3：哪张卡在对手的牌库中？
    # 
    # 规则：
    # - 每个线索给出3个选项，玩家选择1个
    # - 如果猜错任何一个，战吼立即结束，不获得任何卡牌
    # - 必须全部猜对才能获得3张卡的复制
    # - 没有对手猜测机制
    
    def play(self):
        opponent = self.controller.opponent
        
        # 定义创建选项的辅助函数
        def create_options(target, pool):
            """创建3个选项：1个正确答案 + 2个干扰项"""
            options = [target]
            
            # 从池中选择干扰项
            other_cards = [c for c in pool if c != target]
            if len(other_cards) >= 2:
                decoys = self.game.random.sample(other_cards, 2)
                options.extend(decoys)
            elif len(other_cards) == 1:
                options.append(other_cards[0])
                # 如果只有1张其他卡，重复使用
                options.append(self.game.random.choice(pool))
            else:
                # 如果没有其他卡，重复使用目标卡
                options.extend([target, target])
            
            # 打乱顺序
            self.game.random.shuffle(options)
            return options
        
        # 线索1：起始手牌（mulligan后的手牌）
        # 使用 opponent.starting_hand 获取对手真实的起始手牌
        starting_hand_pool = list(opponent.starting_hand) if hasattr(opponent, 'starting_hand') and opponent.starting_hand else []
        
        # 如果没有起始手牌记录（可能是测试环境），回退到当前手牌
        if not starting_hand_pool:
            starting_hand_pool = list(opponent.hand)
        
        if not starting_hand_pool:
            return  # 没有可选项，结束
        
        # 创建线索1的选项
        clue1_target = self.game.random.choice(starting_hand_pool)
        clue1_options = create_options(clue1_target, starting_hand_pool)
        
        # 玩家猜测线索1
        choice1 = yield GenericChoice(CONTROLLER, clue1_options)
        if not choice1 or choice1[0] != clue1_target:
            return  # 猜错了，战吼结束
        
        # 线索2：当前手牌
        if not opponent.hand:
            return  # 没有手牌，结束
        
        clue2_target = self.game.random.choice(list(opponent.hand))
        clue2_options = create_options(clue2_target, list(opponent.hand))
        
        # 玩家猜测线索2
        choice2 = yield GenericChoice(CONTROLLER, clue2_options)
        if not choice2 or choice2[0] != clue2_target:
            return  # 猜错了，战吼结束
        
        # 线索3：牌库
        if not opponent.deck:
            return  # 没有牌库，结束
        
        clue3_target = self.game.random.choice(list(opponent.deck))
        clue3_options = create_options(clue3_target, list(opponent.deck))
        
        # 玩家猜测线索3
        choice3 = yield GenericChoice(CONTROLLER, clue3_options)
        if not choice3 or choice3[0] != clue3_target:
            return  # 猜错了，战吼结束
        
        # 全部猜对！给予3张卡的复制
        yield Give(CONTROLLER, Copy(clue1_target))
        yield Give(CONTROLLER, Copy(clue2_target))
        yield Give(CONTROLLER, Copy(clue3_target))
    
class REV_238:
    """Theotar, the Mad Duke - 癫狂公爵西塔尔
    <b>Battlecry:</b> <b>Discover</b> a
card in each player's hand and swap them.
    <b>战吼：</b>从双方手牌中各<b>发现</b>一张卡牌并交换它们。
    """
    def play(self):
        # 这需要两次选择：
        # 1. 从己方手牌中选择一张
        # 2. 从对手手牌中选择一张
        # 3. 交换它们
        
        my_hand = [c for c in self.controller.hand if c != self]
        enemy_hand = list(self.controller.opponent.hand)
        
        if my_hand and enemy_hand:
            # 使用 GenericChoice 让AI选择
            # 这样AI可以学习选择策略
            # 第一步：从己方手牌中选择（最多3个选项）
            my_choice = yield GenericChoice(CONTROLLER, my_hand[:3] if len(my_hand) > 3 else my_hand)
            
            # 第二步：从对手手牌中选择（最多3个选项）
            enemy_choice = yield GenericChoice(CONTROLLER, enemy_hand[:3] if len(enemy_hand) > 3 else enemy_hand)
            
            # 交换选中的卡牌
            if my_choice and enemy_choice:
                yield Steal(my_choice[0], OPPONENT)
                yield Steal(enemy_choice[0], CONTROLLER)


class REV_906:
    """Sire Denathrius - 德纳修斯大帝
    <b><b>Lifesteal</b>.</b> <b>Battlecry:</b> Deal 5 damage amongst enemies. <b>Endlessly Infuse (2):</b> Deal 1 more.
    <b>吸血，战吼：</b>对敌方随机分配5点伤害。<b>无尽注能(2)：</b>多造成1点伤害。
    """
    tags = {GameTag.LIFESTEAL: True}
    infuse = 2  # 每2个友方随从死亡增加1点伤害
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 显式初始化 infuse_counter
        # 这个卡牌的特殊之处在于"无尽注能"：没有上限
        self.infuse_counter = 0
        # 标记为无尽注能，核心不会锁定计数器
        self.endless_infuse = True
    
    def play(self):
        # 基础伤害5点
        base_damage = 5
        
        # 计算额外伤害：每注能2次增加1点
        # infuse_counter 由核心的 Death action 自动维护
        # 由于 endless_infuse=True，计数器不会被锁定
        extra_damage = self.infuse_counter // 2
        
        total_damage = base_damage + extra_damage
        
        # 对敌方随机分配伤害
        # 使用 Hit 多次，每次1点伤害，随机目标
        for i in range(total_damage):
            yield Hit(RANDOM_ENEMY_CHARACTER, 1)


