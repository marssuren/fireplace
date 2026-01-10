"""
穿越时间流 - DEMONHUNTER
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_441:
    """永世裂痕 - Aeon Rend
    4费 法术 - 邪能学派
    <b>回溯</b>。随机对两个敌人造成$4点伤害。

    Rewind. Deal 4 damage to two random enemies.
    """
    requirements = {}

    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 随机对两个敌人造成4点伤害
            # 注意：可能对同一个敌人造成两次伤害
            for _ in range(2):
                yield Hit(RANDOM_ENEMY_CHARACTER, 4)

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_444:
    """迷时战刃 - Time-Lost Glaive
    1费 2/2 武器
    <b>亡语：</b>随机获取一张来自过去的恶魔牌。
    
    Deathrattle: Get a random Demon from the past.
    """
    deathrattle = Give(CONTROLLER, RandomDemon())


class TIME_448:
    """命源 - Solitude
    2费 法术
    <b>发现</b>2张随从牌。如果你的牌库中没有随从，使你手牌中的随从牌的法力值消耗减少（2）点。
    
    Discover 2 minions. If your deck has no minions, reduce the Cost of any in your hand by (2).
    """
    requirements = {}
    
    def play(self):
        # 发现第一张随从牌
        yield Discover(CONTROLLER, RandomMinion())
        
        # 发现第二张随从牌
        yield Discover(CONTROLLER, RandomMinion())
        
        # 检查牌库中是否有随从
        has_minions_in_deck = any(
            card.type == CardType.MINION 
            for card in self.controller.deck
        )
        
        # 如果牌库中没有随从，减少手牌中随从的费用
        if not has_minions_in_deck:
            yield Buff(FRIENDLY_HAND + MINION, "TIME_448e")


class TIME_448e:
    """命源减费 - Solitude Cost Reduction"""
    cost = -2


# RARE

class TIME_022:
    """累世巨蛇 - Perennial Serpent
    8费 7/9 野兽
    <b>突袭</b>。如果有<b>休眠</b>的随从，本牌的法力值消耗减少（4）点。
    
    Rush. Costs (4) less if a minion is Dormant.
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    
    cost_mod = lambda self, i: -4 if any(minion.dormant for minion in self.game.board) else 0


class TIME_443:
    """怒火狱犬 - Hounds of Fury
    4费 法术
    召唤两只3/3的恶魔。如果你的牌库中没有随从，使其攻击生命值最低的敌人。
    
    Summon two 3/3 Demons. If your deck has no minions, they attack the lowest Health enemy.
    """
    requirements = {}
    
    def play(self):
        # 检查牌库中是否有随从
        has_minions_in_deck = any(
            card.type == CardType.MINION 
            for card in self.controller.deck
        )
        
        # 召唤两只3/3恶魔
        hounds = []
        for _ in range(2):
            hound = yield Summon(CONTROLLER, "TIME_443t")
            if hound:
                hounds.extend(hound)
        
        # 如果牌库中没有随从，使恶魔攻击生命值最低的敌人
        if not has_minions_in_deck and hounds:
            # 找到生命值最低的敌人
            enemies = list(self.controller.opponent.characters)
            if enemies:
                lowest_health_enemy = min(enemies, key=lambda e: e.health)
                
                # 让每只恶魔攻击（给予临时突袭）
                for hound in hounds:
                    # 给恶魔临时突袭以允许立即攻击
                    yield Buff(hound, "TIME_443e")
                    yield Attack(hound, lowest_health_enemy)


class TIME_443e:
    """怒火狱犬 - 临时突袭"""
    tags = {
        GameTag.RUSH: True,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }


class TIME_449:
    """绵延传承 - Lasting Legacy
    3费 法术
    在本回合中，使你的英雄获得+4攻击力。如果你的牌库中没有随从，使你手牌中的随从牌获得+4攻击力。
    
    Give your hero +4 Attack this turn. If your deck has no minions, give a minion in your hand +4 Attack.
    """
    requirements = {}
    
    def play(self):
        # 给英雄+4攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "TIME_449e")
        
        # 检查牌库中是否有随从
        has_minions_in_deck = any(
            card.type == CardType.MINION 
            for card in self.controller.deck
        )
        
        # 如果牌库中没有随从，给手牌中的随从+4攻击力
        if not has_minions_in_deck:
            yield Buff(FRIENDLY_HAND + MINION, "TIME_449e2")


class TIME_449e:
    """绵延传承 - 英雄攻击力增益"""
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.ATK: 4,
    }


class TIME_449e2:
    """绵延传承 - 手牌随从攻击力增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 4,
    }
    events = REMOVED_IN_PLAY


# EPIC

class TIME_021:
    """末日准备狂 - Doomsday Prepper
    5费 5/4 随从
    <b>流放：</b>直到你的下个回合，你的英雄<b>免疫</b>。
    
    Outcast: Your hero is Immune until your next turn.
    """
    def play(self):
        # 检查是否为流放
        if self.outcast:
            # 给英雄免疫buff（持续到下个回合）
            yield Buff(FRIENDLY_HERO, "TIME_021e")


class TIME_021e:
    """末日准备狂 - 英雄免疫"""
    tags = {
        GameTag.IMMUNE: True,
    }
    
    # 在下个回合开始时移除
    events = OWN_TURN_BEGIN


class TIME_442:
    """时间流守望者 - Timeway Warden
    4费 2/6 随从
    <b>战吼：</b>监禁一个敌方随从。使其<b>休眠</b>10,000个回合。<b>亡语：</b>唤醒它。
    
    Battlecry: Imprison an enemy minion. It goes Dormant for 10,000 turns. Deathrattle: Awaken it.
    
    实现说明：
    - 使用 SetTag 设置 DORMANT 为 10000（参考 space/hunter.py 的实现）
    - 保存目标引用用于亡语
    - 亡语时将 DORMANT 设置为 0 来唤醒
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        if TARGET:
            # 使目标休眠10000回合
            # 参考 space/hunter.py - GDB_450 的实现
            yield SetTag(TARGET, {GameTag.DORMANT: 10000})
            
            # 记录被监禁的随从ID（而不是引用，因为引用可能失效）
            self._imprisoned_minion_id = id(TARGET)
            self._imprisoned_minion_ref = TARGET
    
    @property
    def deathrattle(self):
        """亡语：唤醒被监禁的随从"""
        if hasattr(self, '_imprisoned_minion_ref') and self._imprisoned_minion_ref:
            target = self._imprisoned_minion_ref
            # 检查目标是否仍在场上且处于休眠状态
            if target.zone == Zone.PLAY and target.dormant:
                # 唤醒随从（设置 DORMANT 为 0）
                # 参考 the_lost_city/neutral_common.py - TLC_246 的实现
                return [SetTag(target, {GameTag.DORMANT: 0})]
        return []


# LEGENDARY

class TIME_020:
    """布洛克斯加 - Broxigar
    2费 12/12 随从
    <b>奇闻</b>
    <b>冲锋</b>。<b>对战开始时：</b>消失。
    消灭全部4个来自阿古斯的恶魔以重新出现在手牌中。
    
    Fabled, Charge
    Start of Game: Disappear.
    Kill all 4 Demons from Argus to reappear in hand.
    
    阿古斯的4个恶魔：
    - 安尼赫兰 (Annihilan)
    - 末日守卫 (Doomguard)
    - 恐惧魔王 (Dreadlord)
    - 深渊领主 (Pit Lord)
    """
    tags = {
        GameTag.CHARGE: True,
        GameTag.START_OF_GAME: True,
        GameTag.FABLED: True,
    }
    
    # Fabled附带卡牌（4个阿古斯恶魔）
    # 这些卡牌会在组牌时自动添加到套牌中
    fabled_package = ["TIME_020t1", "TIME_020t2", "TIME_020t3", "TIME_020t4"]
    
    def start_of_game(self):
        """对战开始时：从手牌和牌库中移除布洛克斯加"""
        # 初始化追踪计数器
        self.controller.broxigar_demons_killed = 0
        
        # 从手牌或牌库中移除自己
        if self.zone == Zone.HAND:
            yield Destroy(SELF)
        elif self.zone == Zone.DECK:
            yield Destroy(SELF)
        
        # 给玩家添加追踪buff
        yield Buff(CONTROLLER, "TIME_020e")


class TIME_020e:
    """布洛克斯加追踪 - Broxigar Tracker
    
    追踪消灭阿古斯恶魔的数量
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化计数器
        if not hasattr(self.controller, 'broxigar_demons_killed'):
            self.controller.broxigar_demons_killed = 0
    
    # 监听敌方随从死亡事件
    events = Death(ENEMY_MINIONS).on(
        lambda self, entity: (
            # 检查是否是阿古斯恶魔
            entity.id in ["TIME_020t1", "TIME_020t2", "TIME_020t3", "TIME_020t4"]
        ),
        lambda self, entity: self._on_argus_demon_killed()
    )
    
    def _on_argus_demon_killed(self):
        """处理阿古斯恶魔被消灭"""
        # 增加计数
        self.controller.broxigar_demons_killed += 1
        
        # 检查是否消灭了全部4个恶魔
        if self.controller.broxigar_demons_killed >= 4:
            # 将布洛克斯加加入手牌
            yield Give(CONTROLLER, "TIME_020")
            # 移除追踪buff
            yield Destroy(SELF)


class TIME_446:
    """永时坚垒 - The Eternal Hold
    6费 地标 - 3次使用
    <b>发现</b>一张法力值消耗为（5）或更高的恶魔牌。如果你的牌库中没有随从，你的下一张恶魔牌的法力值消耗变为（0）点。
    
    Discover any Demon that costs (5) or more. If your deck has no minions, your next one costs (0).
    
    实现说明：
    - 地标使用 activate 方法（而非 lambda 列表）
    - 费用修正使用 Aura 的 Hand.cost_mod 方法
    - 参考 stormwind/warlock.py 的地标实现
    """
    def activate(self):
        """地标激活效果"""
        # 发现一张5费+的恶魔
        yield Discover(CONTROLLER, RandomDemon(cost__ge=5))
        
        # 检查牌库中是否有随从
        has_minions_in_deck = any(
            card.type == CardType.MINION 
            for card in self.controller.deck
        )
        
        # 如果牌库中没有随从，添加减费buff
        if not has_minions_in_deck:
            yield Buff(CONTROLLER, "TIME_446e")


class TIME_446e:
    """永时坚垒 - 下一张恶魔0费
    
    使用 Aura 的 Hand.cost_mod 方法来正确修改手牌费用
    参考 badlands/neutral_legendary.py - WW_819e 的实现
    """
    # 辅助函数：检查是否是手牌中的第一张恶魔
    @staticmethod
    def _is_first_demon(card):
        if card.type != CardType.MINION or not hasattr(card, 'race') or card.race != Race.DEMON:
            return False
        # 找到手牌中第一张恶魔
        first_demon = next((c for c in card.controller.hand 
                           if c.type == CardType.MINION and hasattr(c, 'race') and c.race == Race.DEMON), None)
        return card == first_demon
    
    # 使用 Aura 给手牌中的恶魔减费
    class Hand:
        """手牌光环：给第一张恶魔减费到0"""
        cost_mod = lambda self, i: -self.cost if TIME_446e._is_first_demon(self) else 0
    
    # 监听打出恶魔事件，移除buff
    events = Play(CONTROLLER, MINION).after(
        lambda self, source, card: (
            # 检查是否是恶魔
            hasattr(card, 'race') and card.race == Race.DEMON
        ),
        lambda self, source, card: Destroy(SELF)  # 移除buff
    )
