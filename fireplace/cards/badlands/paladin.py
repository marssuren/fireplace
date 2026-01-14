"""
决战荒芜之地 - PALADIN
"""
from ..utils import *


# COMMON

class DEEP_018:
    """魔菇采掘 - Shroomscavate
    使一个随从获得圣盾。发掘一个宝藏。
    Give a minion Divine Shield. Excavate a treasure.
    """
    # Type: SPELL | Cost: 2 | Rarity: COMMON | Mechanics: EXCAVATE
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        yield GiveDivineShield(TARGET)
        yield Excavate(CONTROLLER)


class WW_335:
    """神圣牛仔 - Holy Cowboy
    战吼：你的下一张神圣法术牌法力值消耗减少（2）点。
    Battlecry: Your next Holy spell costs (2) less.
    """
    # Type: MINION | Cost: 3 | Rarity: COMMON | Stats: 4/3 | Mechanics: BATTLECRY
    def play(self):
        # 给控制者添加一个buff，下一张神圣法术减2费
        yield Buff(CONTROLLER, "WW_335e")


class WW_335e:
    """下一张神圣法术减2费"""
    class Hand:
        # 减少手牌中神圣法术的费用
        update = Refresh(FRIENDLY_HAND + SPELL + HOLY, {GameTag.COST: -2})
    
    # 当施放神圣法术后移除此buff
    events = Play(CONTROLLER, SPELL + HOLY).after(Destroy(SELF))


class WW_336:
    """棱彩光束 - Prismatic Beam
    对所有敌人造成$3点伤害。你每有一个敌方随从，本牌的法力值消耗便减少（1）点。
    [x]Deal $3 damage to all  enemies. Costs (1) less for each enemy minion.
    """
    # Type: SPELL | Cost: 7 | Rarity: COMMON
    # 费用减免通过Aura实现
    class Hand:
        # 每个敌方随从减1费
        update = Refresh(SELF, {GameTag.COST: -Count(ENEMY_MINIONS)})
    
    play = Hit(ENEMY_CHARACTERS, 3)


class WW_342:
    """长臂执法者 - Lawful Longarm
    突袭，吸血。战吼：你手牌中每有一张牌，便获得+1攻击力。
    [x]Rush, Lifesteal Battlecry: Gain +1 Attack for each card in your hand.
    """
    # Type: MINION | Cost: 5 | Rarity: COMMON | Stats: 1/5 | Mechanics: BATTLECRY, LIFESTEAL, RUSH
    rush = True
    lifesteal = True
    
    def play(self):
        # 手牌数量
        hand_count = len(self.controller.hand)
        if hand_count > 0:
            yield Buff(SELF, "WW_342e") * hand_count


class WW_342e:
    """+1攻击"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


# RARE

class DEEP_033:
    """化石水晶龙 - Fossilized Kaleidosaur
    战吼：随机获得两项额外效果。发掘一个宝藏。
    Battlecry: Gain two random Bonus Effects. Excavate a treasure.
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 3/4 | Mechanics: BATTLECRY, EXCAVATE
    def play(self):
        # 随机获得2个额外效果（Bonus Effects）
        # 额外效果包括：圣盾、嘲讽、突袭、吸血、剧毒、风怒等
        bonus_effects = [
            "DEEP_033e_divine_shield",  # 圣盾
            "DEEP_033e_taunt",          # 嘲讽
            "DEEP_033e_rush",           # 突袭
            "DEEP_033e_lifesteal",      # 吸血
            "DEEP_033e_poisonous",      # 剧毒
            "DEEP_033e_windfury",       # 风怒
        ]
        
        # 随机选择2个不同的效果
        chosen = self.game.random.sample(bonus_effects, 2)
        for effect in chosen:
            yield Buff(SELF, effect)
        
        # 发掘
        yield Excavate(CONTROLLER)


# 额外效果Buff定义
class DEEP_033e_divine_shield:
    """圣盾"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.DIVINE_SHIELD: True}


class DEEP_033e_taunt:
    """嘲讽"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.TAUNT: True}


class DEEP_033e_rush:
    """突袭"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.RUSH: True}


class DEEP_033e_lifesteal:
    """吸血"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.LIFESTEAL: True}


class DEEP_033e_poisonous:
    """剧毒"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.POISONOUS: True}


class DEEP_033e_windfury:
    """风怒"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT, GameTag.WINDFURY: True}


class WW_341:
    """警务光环 - Deputization Aura
    你最左边的随从获得+1攻击力和吸血。持续3回合。
    Your left-most minion has +1 Attack and Lifesteal. Lasts 3 turns.
    """
    # Type: SPELL | Cost: 3 | Rarity: RARE
    # 这是一个持续3回合的光环法术
    # 通过给英雄施加一个持续3回合的buff来实现光环效果
    def play(self):
        yield Buff(FRIENDLY_HERO, "WW_341e")


class WW_341e:
    """警务光环效果"""
    # 使用标准的Update机制给最左边的随从施加buff
    update = (
        # 移除之前的buff
        Destroy(FRIENDLY_MINIONS + ID("WW_341e2")),
        # 给最左边的随从施加新buff
        Find(FRIENDLY_MINIONS) & Buff((FRIENDLY_MINIONS)[:1], "WW_341e2")
    )
    
    # 在己方回合开始时减少计数，3回合后移除
    events = OWN_TURN_BEGIN.on(
        AddProgress(SELF, SELF, -1),
        (Count(SELF) <= -3) & Destroy(SELF)
    )


class WW_341e2:
    """+1攻击和吸血"""
    tags = {
        GameTag.ATK: 1,
        GameTag.LIFESTEAL: True
    }


class WW_344:
    """威猛银翼巨龙 - Hi Ho Silverwing
    圣盾。亡语：抽一张神圣法术牌。
    Divine Shield Deathrattle: Draw a Holy spell.
    """
    # Type: MINION | Cost: 2 | Rarity: RARE | Stats: 2/1 | Mechanics: DEATHRATTLE, DIVINE_SHIELD
    divine_shield = True
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + HOLY))


class WW_365:
    """不许乱动 - Lay Down the Law
    可交易。将一个随从的攻击力和生命值变为1。快枪：然后对其造成$1点伤害。
    """
    # Type: SPELL | Cost: 2 | Rarity: RARE | Mechanics: QUICKDRAW, TRADEABLE
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    tradeable = True
    
    def play(self):
        # 将随从属性变为1/1
        yield Buff(TARGET, "WW_365e")
        
        # 快枪：本回合获得并立即使用时触发，造成1点伤害
        if self.drawn_this_turn:
            yield Hit(TARGET, 1)


class WW_365e:
    """属性设置为1/1"""
    def apply(self, target):
        target.atk = 1
        target.max_health = 1
        target.damage = 0


# EPIC

class WW_051:
    """决战！ - Showdown!
    双方玩家各召唤三个3/3的亡命徒。使你召唤的随从获得突袭。
    Both players summon three 3/3 Outlaws. Give yours Rush.
    """
    # Type: SPELL | Cost: 2 | Rarity: EPIC
    def play(self):
        # 双方各召唤3个3/3亡命徒
        # 己方的获得突袭
        for _ in range(3):
            minion = yield Summon(CONTROLLER, "WW_051t")
            if minion:
                yield Buff(minion, "WW_051e")
        
        # 对手召唤3个
        for _ in range(3):
            yield Summon(OPPONENT, "WW_051t")


class WW_051t:
    """亡命徒 - Outlaw
    3/3 随从
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.MINION
    }


class WW_051e:
    """突袭"""
    tags = {GameTag.RUSH: True}


class WW_366:
    """活体天光 - Living Horizon
    嘲讽，圣盾。你手牌中每有一张其他牌，本牌的法力值消耗便减少（1）点。
    [x]Taunt, Divine Shield Costs (1) less for each other card in your hand.
    """
    # Type: MINION | Cost: 10 | Rarity: EPIC | Stats: 4/6 | Mechanics: DIVINE_SHIELD, TAUNT
    taunt = True
    divine_shield = True
    
    class Hand:
        # 手牌中每有一张其他牌减1费（不包括自己）
        update = Refresh(SELF, {GameTag.COST: -Count(FRIENDLY_HAND - SELF)})


# LEGENDARY

class DEEP_007:
    """无畏爵士芬利 - Sir Finley, the Intrepid
    战吼：如果你已经发掘过两次，将所有敌方随从变形成为1/1的鱼人。
    [x]Battlecry: If you've Excavated twice, transform all enemy minions into 1/1 Murlocs.
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 2/3 | Mechanics: BATTLECRY, EXCAVATE
    def play(self):
        # 检查是否已发掘2次
        if self.controller.excavate_tier >= 2:
            # 将所有敌方随从变形为1/1鱼人
            yield Morph(ENEMY_MINIONS, "DEEP_007t")


class DEEP_007t:
    """鱼人 - Murloc"""
    # 1/1鱼人
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDRACE: Race.MURLOC
    }


class WW_337:
    """荒芜之地的精魂 - Spirit of the Badlands
    战吼：如果你的套牌里没有相同的牌，则获取一张永久的幻象牌。
    [x]Battlecry: If your deck started with no duplicates, get  a <i>permanent</i>  Mirage.
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 3/4 | Mechanics: BATTLECRY
    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    
    def play(self):
        # 检查起始套牌是否无重复
        if self.powered_up:
            # 获取永久幻象
            yield Give(CONTROLLER, "WW_337t")


class WW_337t:
    """幻象 - Mirage"""
    # 永久幻象牌（0费法术）
    # 效果：在你的回合开始时，变形成为你牌库中的一个随从的复制。（这张牌保留在你的手牌中。）
    # At the start of your turn, transform into a copy of a minion in your deck. (This stays in your hand.)
    tags = {
        GameTag.COST: 0,
        GameTag.CARDTYPE: CardType.SPELL
    }
    
    # 在回合开始时，变形成牌库中的随从
    events = OWN_TURN_BEGIN.on(
        # 如果牌库中有随从
        Find(FRIENDLY_DECK + MINION) & (
            # 变形成牌库中随机一个随从的复制
            Morph(SELF, Copy(RANDOM(FRIENDLY_DECK + MINION))),
            # 给变形后的卡牌添加一个标记，使其在使用后返回幻象
            Buff(SELF, "WW_337t_tracker")
        )
    )


class WW_337t_tracker:
    """幻象追踪标记"""
    # 当这张从幻象变来的卡牌被使用后，重新给予一张幻象
    events = Play(CONTROLLER, SELF).after(
        Give(CONTROLLER, "WW_337t")
    )


class WW_345:
    """荒芜之地劫掠者 - The Badlands Bandits
    获取八个3/2并具有额外效果的强盗。无法置入你手牌的强盗会被直接召唤。
    [x]Get eight 3/2 Bandits with Bonus Effects. Any that can't fit in your hand are summoned instead.
    """
    # Type: SPELL | Cost: 6 | Rarity: LEGENDARY
    def play(self):
        # 生成8个3/2强盗，每个都有随机额外效果
        # 官方有8种额外效果：风怒、复生、吸血、潜行、剧毒、突袭、圣盾、嘲讽
        for _ in range(8):
            # 随机选择一个额外效果的强盗
            bandit_variants = [
                "WW_345t",   # 突袭 (Rush)
                "WW_345t2",  # 圣盾 (Divine Shield)
                "WW_345t3",  # 吸血 (Lifesteal)
                "WW_345t4",  # 嘲讽 (Taunt)
                "WW_345t5",  # 风怒 (Windfury)
                "WW_345t6",  # 复生 (Reborn)
                "WW_345t7",  # 潜行 (Stealth)
                "WW_345t8",  # 剧毒 (Poisonous)
            ]
            bandit_id = self.game.random.choice(bandit_variants)
            
            # 检查手牌是否已满
            if len(self.controller.hand) < self.controller.max_hand_size:
                # 置入手牌
                yield Give(CONTROLLER, bandit_id)
            else:
                # 直接召唤
                yield Summon(CONTROLLER, bandit_id)


class WW_345t:
    """强盗 - Bandit (突袭)"""
    # 3/2随从，突袭
    tags = {GameTag.RUSH: True}


class WW_345t2:
    """强盗 - Bandit (圣盾)"""
    # 3/2随从，圣盾
    tags = {GameTag.DIVINE_SHIELD: True}


class WW_345t3:
    """强盗 - Bandit (吸血)"""
    # 3/2随从，吸血
    tags = {GameTag.LIFESTEAL: True}


class WW_345t4:
    """强盗 - Bandit (嘲讽)"""
    # 3/2随从，嘲讽
    tags = {GameTag.TAUNT: True}


class WW_345t5:
    """强盗 - Bandit (风怒)"""
    # 3/2随从，风怒
    tags = {GameTag.WINDFURY: True}


class WW_345t6:
    """强盗 - Bandit (复生)"""
    # 3/2随从，复生
    tags = {GameTag.REBORN: True}


class WW_345t7:
    """强盗 - Bandit (潜行)"""
    # 3/2随从，潜行
    tags = {GameTag.STEALTH: True}


class WW_345t8:
    """强盗 - Bandit (剧毒)"""
    # 3/2随从，剧毒
    tags = {GameTag.POISONOUS: True}


