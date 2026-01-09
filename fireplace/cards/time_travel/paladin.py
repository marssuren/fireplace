"""
穿越时间流 - PALADIN
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_015:
    """强光护卫 - Hardlight Protector
    圣盾。战吼：为你的英雄恢复#3点生命值并使其获得圣盾。
    
    Divine Shield. Battlecry: Restore 3 Health to your hero and give them Divine Shield.
    """
    # Mechanics: BATTLECRY, DIVINE_SHIELD
    # 圣盾在卡牌定义中通过标签实现
    requirements = {}
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 为英雄恢复3点生命值
            yield Heal(FRIENDLY_HERO, 3)
            
            # 给英雄圣盾
            yield Buff(FRIENDLY_HERO, "divine_shield")


class TIME_017:
    """坦克机械师 - Tankgineer
    圣盾。亡语：召唤一辆7/7并具有圣盾的坦克。
    
    Divine Shield. Deathrattle: Summon a 7/7 Tank with Divine Shield.
    """
    # Mechanics: DEATHRATTLE, DIVINE_SHIELD
    # 圣盾在卡牌定义中通过标签实现
    deathrattle = Summon(CONTROLLER, "TIME_017t")


class TIME_700:
    """时序光环 - Chronological Aura
    在你的回合结束时，召唤一个3/5并具有嘲讽的龙。持续3个回合。
    
    At the end of your turn, summon a 3/5 Dragon with Taunt. Lasts 3 turns.
    """
    # 这是一个地标（Location）卡牌，持续3回合
    # 每回合结束时触发效果
    events = OWN_TURN_END.on(Summon(CONTROLLER, "TIME_700t"))


# RARE

class TIME_016:
    """耀眼创意 - Neon Innovation
    发现一张来自过去的圣骑士机械牌。使其获得+5/+5。
    
    Discover a Paladin Mech from the past. Give it +5/+5.
    """
    # Mechanics: DISCOVER, GEARS
    requirements = {}
    
    def play(self):
        # 发现一张圣骑士机械牌
        # 参考 mage.py 的 Discover 实现
        card = yield Discover(
            self.controller,
            RandomCollectible(card_class=CardClass.PALADIN, race=Race.MECHANICAL)
        )
        
        # 给发现的卡牌+5/+5
        if card:
            yield Buff(card, "TIME_016e")


class TIME_016e:
    """耀眼创意 - +5/+5"""
    atk = 5
    max_health = 5


class TIME_019:
    """时间流具象 - Manifested Timeways
    战吼：如果你控制着光环，对所有敌人造成3点伤害。
    
    Battlecry: If you control an Aura, deal 3 damage to all enemies.
    """
    # Mechanics: BATTLECRY
    requirements = {}
    
    def play(self):
        # 检查是否控制光环（地标）
        # 光环是 Location 类型的卡牌
        has_aura = False
        for entity in self.controller.live_entities:
            if entity.type == CardType.LOCATION:
                has_aura = True
                break
        
        # 如果控制光环，对所有敌人造成3点伤害
        if has_aura:
            yield Hit(ENEMY_CHARACTERS, 3)


class TIME_043:
    """无穷永动机 - PMM Infinitizer
    战吼：将一个友方随从的攻击力和生命值变为8。本回合中，该随从无法攻击英雄。
    
    Battlecry: Set a friendly minion's Attack and Health to 8. It can't attack heroes this turn.
    """
    # Mechanics: BATTLECRY
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        if self.target:
            # 将攻击力和生命值设置为8
            # 参考 mage.py 的 SetAtk/SetHealth 实现
            yield SetAtk(self.target, 8)
            yield SetHealth(self.target, 8)
            
            # 本回合无法攻击英雄
            yield Buff(self.target, "TIME_043e")


class TIME_043e:
    """无穷永动机 - 无法攻击英雄"""
    tags = {
        GameTag.CANNOT_ATTACK_HEROES: True,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }


# EPIC

class TIME_018:
    """修补时间线 - Mend the Timeline
    回溯。随机获取2张神圣法术牌，为你的英雄恢复等同于其法力值消耗的生命值。
    
    Rewind. Get 2 random Holy spells. Restore Health to your hero equal to their Costs.
    """
    requirements = {}
    
    def play(self):
        
        # 随机获取2张神圣法术牌并累计法力值消耗
        total_cost = 0
        for _ in range(2):
            # Give action 返回的是一个列表
            cards = yield Give(
                self.controller,
                RandomSpell(spell_school=SpellSchool.HOLY)
            )
            
            # 累计法力值消耗
            if cards:
                # cards 是一个列表，取第一个元素
                card = cards[0] if isinstance(cards, list) else cards
                total_cost += card.cost
        
        # 为英雄恢复等同于法力值消耗的生命值
        if total_cost > 0:
            yield Heal(FRIENDLY_HERO, total_cost)


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_044:
    """过去的诺莫瑞根 - Past Gnomeregan
    使一个随从获得+2/+1。进入现在！
    
    Give a minion +2/+1. Advance to the present!
    
    注：这是一个地标（Location）卡牌，有3个阶段：
    - 过去：+2/+1
    - 现在：+2/+1 + 亡语：对敌方英雄造成2点伤害
    - 未来：+2/+1 + 圣盾 + 亡语：对敌方英雄造成2点伤害
    """
    # 这是一个地标卡牌，每次激活时升级
    # 第一阶段：过去的诺莫瑞根
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def activate(self):
        # 给目标随从+2/+1
        yield Buff(TARGET, "TIME_044e")


class TIME_044e:
    """过去的诺莫瑞根 - +2/+1"""
    atk = 2
    max_health = 1


# LEGENDARY

class TIME_009:
    """明日巨匠格尔宾 - Gelbin of Tomorrow
    奇闻。战吼：将每种不同的光环从你的牌库中置入战场。
    
    Fabled. Battlecry: Put one of each Aura from your deck into the battlefield.
    """
    # Mechanics: BATTLECRY, FABLED
    # Fabled 机制在套牌构建时处理
    requirements = {}
    
    def play(self):
        # 从牌库中找出所有不同的光环（Location）卡牌
        # 并将它们置入战场
        found_auras = set()
        
        for card in list(self.controller.deck):
            # 检查是否为地标卡牌（光环）
            if card.type == CardType.LOCATION:
                # 检查是否已经找过这种光环
                if card.id not in found_auras:
                    found_auras.add(card.id)
                    # 将光环从牌库移到战场
                    yield Play(self.controller, card)


class TIME_706:
    """超时空鳍侠 - The Fins Beyond Time
    战吼：将你的手牌替换为起始手牌。在你的回合结束时换回。
    
    Battlecry: Replace your hand with your starting hand. Swap back at the end of your turn.
    
    实现说明：
    - 参考 Secret Passage (SCH_305) 的实现
    - 使用 Setaside 暂存当前手牌
    - 从 starting_hand 获取起始手牌
    - 回合结束时换回
    """
    # Mechanics: BATTLECRY
    requirements = {}
    
    def play(self):
        # 1. 将当前手牌移到暂存区（参考 Secret Passage）
        yield Setaside(FRIENDLY_HAND)
        
        # 2. 从起始手牌中给予卡牌
        # starting_hand 是一个 CardList，包含游戏开始时的手牌
        if hasattr(self.controller, 'starting_hand'):
            for card in self.controller.starting_hand:
                # 给予起始手牌的复制
                yield Give(self.controller, card.id)
        
        # 3. 添加追踪buff，在回合结束时换回手牌
        yield Buff(self.controller, "TIME_706e")


class TIME_706e:
    """超时空鳍侠 - 回合结束时换回手牌
    
    参考 Secret Passage 的追踪器实现
    在回合结束时：
    1. 将当前手牌（起始手牌）洗回牌库
    2. 从暂存区恢复原来的手牌
    3. 销毁这个buff
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 监听回合结束事件（参考 SCH_305_tracker）
    events = OWN_TURN_END.on(
        # 1. 将当前手牌洗回牌库
        Shuffle(CONTROLLER, FRIENDLY_HAND),
        # 2. 从暂存区取回原来的手牌
        Give(CONTROLLER, FRIENDLY_SETASIDE),
        # 3. 销毁这个buff
        Destroy(SELF)
    )



