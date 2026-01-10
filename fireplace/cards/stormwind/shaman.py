# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 萨满
"""

from ..utils import *

class DED_509:
    """艳丽的金刚鹦鹉 / Brilliant Macaw
    战吼：重复你上一个战吼。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    def play(self):
        """重复上一个战吼"""
        # 获取上一个战吼
        last_battlecry = getattr(self.controller, 'last_battlecry', None)
        
        if last_battlecry and hasattr(last_battlecry, 'play'):
            # 重复战吼效果
            # 注意：需要在正确的上下文中执行
            try:
                # 执行上一个战吼的 play 方法
                yield from last_battlecry.play()
            except:
                # 如果执行失败，忽略
                pass



class DED_511:
    """吸盘钩手 / Suckerhook
    在你的回合结束时，将你的武器变形为一把法力值消耗高（1）点的武器。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 2,
        GameTag.COST: 2,
    }
    
    # 回合结束时变形武器
    events = OWN_TURN_END.on(
        lambda self: self._transform_weapon()
    )
    
    def _transform_weapon(self):
        """将玩家装备的武器变形为费用+1的武器"""
        # 检查玩家是否装备了武器
        if not self.controller.weapon:
            return
        
        # 获取当前武器的费用
        current_cost = self.controller.weapon.cost
        target_cost = current_cost + 1
        
        # 变形为费用+1的萨满或中立武器
        # 使用 RandomCollectible 获取目标费用的武器
        try:
            # 变形玩家装备的武器
            yield Morph(
                FRIENDLY_WEAPON, 
                RandomCollectible(
                    type=CardType.WEAPON,
                    cost=target_cost,
                    card_class=CardClass.SHAMAN
                )
            )
        except:
            # 如果没有找到合适的武器，保持当前武器不变
            pass



class DED_522:
    """厨师曲奇 / Cookie the Cook
    吸血 亡语：装备一把2/3并具有吸血的搅拌棒。"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        GameTag.LIFESTEAL: True,
    }
    
    deathrattle = Equip(CONTROLLER, "DED_522t")


class DED_522t:
    """搅拌棒 / Stirring Rod"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 3,
        GameTag.COST: 3,
        GameTag.LIFESTEAL: True,
    }


class SW_025:
    """拍卖行木槌 / Auctionhouse Gavel
    在你的英雄攻击后，使你手牌中一张战吼随从牌的法力值消耗减少（1）点。"""
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.ATK: 2,
        GameTag.DURABILITY: 3,
        GameTag.COST: 2,
    }
    
    events = Attack(FRIENDLY_HERO).after(
        Find(FRIENDLY_HAND + MINION + BATTLECRY) & 
        Buff(RANDOM(FRIENDLY_HAND + MINION + BATTLECRY), "SW_025e")
    )


class SW_025e:
    """拍卖行木槌减费"""
    cost = -1


class SW_026:
    """幽灵狼前锋 / Spirit Alpha
    在你打出一张过载牌后，召唤一个2/3并具有嘲讽的幽灵狼。"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.COST: 4,
    }
    
    # 监听打出过载牌
    events = Play(CONTROLLER).after(
        lambda self: Summon(CONTROLLER, "SW_026t") 
        if hasattr(Play.CARD, 'overload') and Play.CARD.overload > 0 else None
    )


class SW_026t:
    """幽灵狼 / Spirit Wolf"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 2,
        GameTag.TAUNT: True,
    }


class SW_031:
    """号令元素 / Command the Elements
    任务线：打出3张过载牌。奖励：解锁你的过载法力水晶。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.QUEST: True,
    }
    
    # 任务线要求：三个阶段，每个阶段打出3张过载牌
    questline_requirements = [3, 3, 3]
    
    def play(self):
        """打出任务线"""
        from ..enums import QUESTLINE_STAGE, QUESTLINE_PROGRESS
        
        self.tags[QUESTLINE_STAGE] = 1
        self.tags[QUESTLINE_PROGRESS] = 0
        self.zone = Zone.SECRET
        
        yield Buff(CONTROLLER, "SW_031e")
    
    def questline_reward_1(self):
        """阶段1奖励：解锁过载"""
        return [UnlockOverload(CONTROLLER)]
    
    def questline_reward_2(self):
        """阶段2奖励：解锁过载"""
        return [UnlockOverload(CONTROLLER)]
    
    def questline_reward_3(self):
        """阶段3奖励：解锁过载"""
        return [UnlockOverload(CONTROLLER)]


class SW_031e:
    """号令元素追踪器"""
    # 监听打出过载牌
    events = Play(CONTROLLER).after(
        lambda self: [
            Find(FRIENDLY_SECRETS + ID("SW_031")) &
            QuestlineProgress(FRIENDLY_SECRETS + ID("SW_031"), 3)
        ] if hasattr(Play.CARD, 'overload') and Play.CARD.overload > 0 else None
    )


class UnlockOverload:
    """解锁过载 Action"""
    def __init__(self, player):
        self.player = player
    
    def do(self):
        """解锁所有过载的法力水晶"""
        self.player.overloaded = 0


class SW_032:
    """花岗岩熔铸体 / Granite Forgeborn
    战吼：使你手牌和牌库中的元素牌的法力值消耗减少（1）点。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    
    play = (Buff(FRIENDLY_HAND + ELEMENTAL, "SW_032e"), Buff(FRIENDLY_DECK + ELEMENTAL, "SW_032e"))


class SW_032e:
    """花岗岩熔铸体减费"""
    cost = -1


class SW_033:
    """运河慢步者 / Canal Slogger
    突袭，吸血 过载：（1）"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 4,
        GameTag.COST: 5,
        GameTag.RUSH: True,
        GameTag.LIFESTEAL: True,
        GameTag.OVERLOAD: 1,
    }


class SW_034:
    """小巧玩具 / Tiny Toys
    召唤四个随机的5费随从。使它们变为2/2。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 7,
    }
    
    def play(self):
        """召唤4个5费随从并变为2/2"""
        for _ in range(4):
            minion = yield Summon(CONTROLLER, RandomMinion(cost=5))
            if minion:
                yield SetTag(minion, {GameTag.ATK: 2, GameTag.HEALTH: 2})


class SW_035:
    """充能召唤 / Charged Call
    发现一张1费随从牌并召唤它。（你每在本局游戏中打出一张过载牌，便升级一次！）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        """发现并召唤随从，根据过载牌数量升级"""
        # 统计本局游戏打出的过载牌数量
        overload_cards_played = sum(
            1 for card in self.controller.cards_played_this_game
            if hasattr(card, 'overload') and card.overload > 0
        )
        
        # 根据过载牌数量决定召唤的费用
        # 0-2张：1费，3-5张：2费，6+张：3费
        if overload_cards_played >= 6:
            minion_cost = 3
        elif overload_cards_played >= 3:
            minion_cost = 2
        else:
            minion_cost = 1
        
        # 发现并召唤
        discovered = yield GenericChoice(
            CONTROLLER, 
            Discover(CONTROLLER, RandomMinion(cost=minion_cost))
        )
        if discovered:
            yield Summon(CONTROLLER, discovered)



class SW_095:
    """投资良机 / Investment Opportunity
    抽一张过载牌。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + OVERLOAD)


class SW_114:
    """强行透支 / Overdraft
    可交易 解锁你的过载法力水晶以造成等量的伤害。"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
    }
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        """解锁过载并造成伤害"""
        overloaded = self.controller.overloaded
        if overloaded > 0:
            # 解锁过载
            self.controller.overloaded = 0
            # 造成伤害
            yield Hit(TARGET, overloaded)


class SW_115:
    """伯尔纳·锤喙 / Bolner Hammerbeak
    在你打出一张战吼随从后，重复本回合打出的第一个战吼。"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    def play(self):
        """添加追踪器"""
        yield Buff(CONTROLLER, "SW_115e")


class SW_115e:
    """伯尔纳·锤喙追踪器"""
    def apply(self, target):
        """初始化追踪"""
        if not hasattr(target, 'bolner_first_battlecry_this_turn'):
            target.bolner_first_battlecry_this_turn = None
    
    # 监听打出战吼随从
    events = Play(CONTROLLER, MINION).after(
        lambda self: self._on_battlecry_played()
    )
    
    def _on_battlecry_played(self):
        """当打出战吼随从时"""
        played_card = Play.CARD
        
        # 检查是否有战吼
        if hasattr(played_card, 'play') and callable(played_card.play):
            # 如果是本回合第一个战吼，记录它
            if self.controller.bolner_first_battlecry_this_turn is None:
                self.controller.bolner_first_battlecry_this_turn = played_card
            else:
                # 不是第一个，重复第一个战吼
                first_battlecry = self.controller.bolner_first_battlecry_this_turn
                if first_battlecry and hasattr(first_battlecry, 'play'):
                    try:
                        yield from first_battlecry.play()
                    except:
                        pass
    
    # 回合结束时重置
    events_turn_end = OWN_TURN_END.on(
        lambda self: setattr(self.controller, 'bolner_first_battlecry_this_turn', None)
    )

