"""
穿越时间流 - WARRIOR
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_715:
    """为了荣耀！ - For Glory!
    5费 法术
    抽两张牌。你的对手每控制一个随从，本牌的法力值消耗便减少（1）点。
    
    Draw 2 cards. Costs (1) less for each minion your opponent controls.
    
    动态费用减免机制，对手随从越多，这张牌越便宜。
    """
    # 使用 Aura 实现动态费用减免
    class Hand:
        """在手牌时的费用减免光环"""
        # 每个敌方随从减少1费
        cost_mod = lambda self, i: -len(self.controller.opponent.field)
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 抽两张牌
            yield Draw(self.controller)
            yield Draw(self.controller)
        
        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_750:
    """先行打击 - Precursory Strike
    2费 法术
    造成$3点伤害。如果你的手牌中有法力值消耗大于或等于（5）点的随从牌，抽一张随从牌。
    
    Deal $3 damage. If you're holding a minion that costs (5) or more, draw a minion.
    
    单体伤害法术，如果手牌中有高费随从还能抽牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)
        
        # 检查手牌中是否有5费或以上的随从
        has_big_minion = False
        for card in self.controller.hand:
            if card.type == CardType.MINION and card.cost >= 5:
                has_big_minion = True
                break
        
        # 如果有，抽一张随从牌
        if has_big_minion:
            yield Draw(self.controller, RandomMinion(FRIENDLY_DECK))


class TIME_873:
    """放出鳄鱼 - Unleash the Crocolisks
    1费 法术
    获得10点护甲值。为你的对手召唤两只2/3的鳄鱼。
    
    Gain 10 Armor. Summon two 2/3 Beasts for your opponent.
    
    给自己10护甲，但为对手召唤两个2/3野兽。
    适合控制战士使用，护甲收益大于对手获得的场面。
    """
    def play(self):
        # 获得10点护甲
        yield GainArmor(self.controller.hero, 10)
        
        # 为对手召唤两只2/3鳄鱼（Token: TIME_873t）
        yield Summon(self.controller.opponent, "TIME_873t")
        yield Summon(self.controller.opponent, "TIME_873t")


# RARE

class TIME_034:
    """现场播报员 - Stadium Announcer
    4费 3/3 龙
    **回溯。战吼：**双方玩家各随机装备一把武器，使你的武器获得+1/+1。
    
    Rewind. Battlecry: Both players equip a random weapon. Give yours +1/+1.
    
    回溯机制允许玩家对随机武器不满意时重新来过。
    双方都装备随机武器，但你的武器会获得+1/+1加成。
    """
    def play(self):
        
        # 双方玩家各装备一把随机武器
        # 为己方装备随机武器
        yield Equip(self.controller, RandomWeapon())
        
        # 为对手装备随机武器
        yield Equip(self.controller.opponent, RandomWeapon())
        
        # 给己方武器+1/+1
        if self.controller.hero.weapon:
            yield Buff(self.controller.hero.weapon, "TIME_034e")


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_034e:
    """现场播报员 - 武器+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.DURABILITY: 1,
    }


class TIME_716:
    """慢动作 - Slow Motion
    2费 法术
    下个回合，你的对手卡牌的法力值消耗增加（1）点。
    
    Your opponent's cards cost (1) more next turn.
    
    延缓对手节奏的控制法术。
    """
    def play(self):
        # 给对手施加一个持续到下回合结束的费用增加效果
        # 使用 Buff 给对手英雄施加效果
        yield Buff(self.controller.opponent.hero, "TIME_716e")


class TIME_716e:
    """慢动作 - 对手卡牌+1费
    
    参考 Loatheb (FP1_030e) 的实现：
    - 使用 CurrentPlayer(OWNER) 确保只在对手回合生效
    - 使用 Refresh 动态更新手牌费用
    - 在对手回合开始时自动移除
    """
    # 在对手回合时，对手手牌费用+1
    update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND, {GameTag.COST: +1})
    # 在对手回合开始时移除此效果（效果持续一个回合）
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class TIME_872:
    """不败冠军 - Undefeated Champion
    8费 13/13 随从
    **突袭。战吼：**用随机的法力值消耗为（1）的随从填满你对手的面板。
    
    Rush. Battlecry: Fill your opponent's board with random 1-Cost minions.
    
    强力的身材和突袭能力，战吼为对手填满场面（但都是1费小随从）。
    可以配合 AOE 清场或者利用对手场面满来阻止其召唤。
    """
    def play(self):
        # 为对手召唤1费随从直到场面满（7个）
        while len(self.controller.opponent.field) < 7:
            yield Summon(
                self.controller.opponent,
                RandomCollectible(
                    card_type=CardType.MINION,
                    cost=1
                )
            )


# EPIC

class TIME_870:
    """角斗开战 - Gladiatorial Combat
    5费 法术
    从你的牌库中随机召唤一个随从。为你的对手召唤一只5/5并具有**潜行**的老虎。
    
    Summon a random minion from your deck. Summon a 5/5 Tiger with Stealth for your opponent.
    
    从牌库中拉随从上场，但为对手召唤一只5/5潜行老虎。
    适合拉高费随从的套牌使用。
    """
    def play(self):
        # 从牌库中随机召唤一个随从
        yield Summon(self.controller, RandomMinion(FRIENDLY_DECK))
        
        # 为对手召唤一只5/5潜行老虎（Token: TIME_870t）
        yield Summon(self.controller.opponent, "TIME_870t")


class TIME_871:
    """后世之嗣 - Heir of Hereafter
    5费 2/6 龙
    **嘲讽。战吼：**每有一个受伤的随从，便获得+2/+2。
    
    Taunt. Battlecry: Gain +2/+2 for each damaged minion.
    
    嘲讽随从，根据场上受伤随从的数量获得大量属性加成。
    """
    def play(self):
        # 计算场上受伤的随从数量
        damaged_count = 0
        for minion in ALL_MINIONS.eval(self.game, self):
            if minion.damage > 0:
                damaged_count += 1
        
        # 每个受伤随从给予+2/+2
        if damaged_count > 0:
            for _ in range(damaged_count):
                yield Buff(SELF, "TIME_871e")


class TIME_871e:
    """后世之嗣 - +2/+2"""
    atk = 2
    max_health = 2


# LEGENDARY

class TIME_714:
    """时光领主埃博克 - Chrono-Lord Epoch
    6费 7/5 龙
    **战吼：**消灭你的对手上回合使用的所有随从。
    
    Battlecry: Destroy all minions that your opponent played last turn.
    
    强力的场面清理效果，消灭对手上回合打出的所有随从。
    
    完整实现：
    - 使用 Player 类的 cards_played_last_turn 属性（存储卡牌ID列表）
    - 遍历对手场上的随从，检查其ID是否在上回合打出的列表中
    - 由于同ID卡牌可能有多张，需要追踪已消灭的数量
    - 参考 VAC_415 (Sasquawk) 的实现模式
    """
    def play(self):
        # 获取对手上回合打出的卡牌ID列表
        if hasattr(self.controller.opponent, 'cards_played_last_turn'):
            # 统计每个卡牌ID在上回合打出的次数
            from collections import Counter
            played_counts = Counter(self.controller.opponent.cards_played_last_turn)
            
            # 遍历对手场上的随从，消灭上回合打出的
            for minion in list(self.controller.opponent.field):
                if minion.type == CardType.MINION and minion.id in played_counts:
                    # 检查是否还有配额可以消灭
                    if played_counts[minion.id] > 0:
                        yield Destroy(minion)
                        played_counts[minion.id] -= 1



class TIME_850:
    """血斗士洛戈什 - Lo'Gosh, Blood Fighter
    7费 7/7 传说随从
    **奇闻，突袭。亡语：**从你的手牌中召唤一位血斗士，使其获得+5/+5并随机攻击一个敌人。
    
    Fabled, Rush. Deathrattle: Summon a Blood Fighter from your hand. It gains +5/+5 and attacks a random enemy.
    
    Fabled 机制：套牌中包含特殊的附带卡牌（血斗士 Token）。
    亡语：从手牌中召唤一个血斗士，给予+5/+5并立即攻击。
    
    完整实现：
    - Fabled 机制在 fabled_helpers.py 中定义附带卡牌
    - 亡语：搜索手牌中的血斗士 Token 并召唤
    - 给予+5/+5 buff
    - 立即攻击随机敌人
    """
    def deathrattle(self):
        # 从手牌中找到血斗士 Token（TIME_850t）
        blood_fighter = None
        for card in list(self.controller.hand):
            if card.id == "TIME_850t":
                blood_fighter = card
                break
        
        if blood_fighter:
            # 召唤血斗士
            summoned = yield Summon(self.controller, blood_fighter)
            
            if summoned and len(summoned) > 0:
                fighter = summoned[0]
                
                # 给予+5/+5
                yield Buff(fighter, "TIME_850e")
                
                # 立即攻击随机敌人
                # 召唤的随从默认有召唤病（不能攻击），需要移除
                # 但由于这是亡语触发，我们可以直接让它攻击
                enemies = list(ENEMY_CHARACTERS.eval(self.game, self))
                if enemies:
                    target = self.game.random.choice(enemies)
                    # 临时允许攻击（移除召唤病）
                    fighter.exhausted = False
                    fighter.num_attacks = 0
                    yield Attack(fighter, target)


class TIME_850e:
    """血斗士洛戈什 - +5/+5"""
    atk = 5
    max_health = 5


