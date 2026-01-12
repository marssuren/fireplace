# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立传说
"""

from ..utils import *


class DED_006:
    """重拳先生 / Mr. Smite
    你的海盗具有冲锋。"""
    update = Refresh(FRIENDLY_MINIONS + PIRATE, {GameTag.CHARGE: True})


class DED_525:
    """哥利亚，斯尼德的杰作 / Goliath, Sneed's Masterpiece
    战吼：向敌方随从发射五枚火箭，每枚造成2点伤害。（你来选择目标！）"""
    # 玩家选择5次目标，每次造成2点伤害
    play = (
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2)
    )


class SW_045:
    """拍卖师亚克森 / Auctioneer Jaxon
    每当你交易时，从你的牌库中发现一张牌来抽取。"""
    events = Trade(CONTROLLER).on(
        Discover(CONTROLLER, FRIENDLY_DECK)
    )


class SW_078:
    """普瑞斯托女士 / Lady Prestor
    战吼：将你牌库中的随从变形为随机龙。（它们保持原始属性和法力值消耗。）"""
    
    def play(self):
        """将牌库中的所有随从变形为随机龙，保持原始属性和费用"""
        for minion in list(self.controller.deck):
            if minion.type == CardType.MINION:
                # 保存原始属性
                original_cost = minion.cost
                original_atk = minion.atk
                original_health = minion.max_health
                
                # 变形为随机龙
                morphed = yield Morph(minion, RandomDragon())
                
                # 如果变形成功，添加buff来恢复原始属性
                if morphed:
                    yield Buff(morphed, "SW_078e", 
                              original_cost=original_cost,
                              original_atk=original_atk, 
                              original_health=original_health)


class SW_078e:
    """普瑞斯托女士的属性保持buff"""
    def apply(self, target):
        """应用原始属性"""
        # 设置原始费用
        if hasattr(self, 'original_cost'):
            target._sw_078_cost = self.original_cost
        
        # 设置原始攻击力和生命值
        if hasattr(self, 'original_atk'):
            target._sw_078_atk = self.original_atk
        if hasattr(self, 'original_health'):
            target._sw_078_health = self.original_health
    
    # 费用修改器
    cost = lambda self, i: getattr(self.owner, '_sw_078_cost', i) if hasattr(self, 'original_cost') else i
    
    # 攻击力修改器
    atk = lambda self, i: getattr(self.owner, '_sw_078_atk', i) if hasattr(self, 'original_atk') else i
    
    # 生命值修改器  
    max_health = lambda self, i: getattr(self.owner, '_sw_078_health', i) if hasattr(self, 'original_health') else i


class SW_079:
    """飞行管理员杜加尔 / Flightmaster Dungar
    战吼：选择一条飞行路线并休眠。完成后带着奖励苏醒！"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    
    # 选择飞行路线：短途、中途、长途
    def play(self):
        """选择飞行路线并休眠"""
        # 使自己休眠
        self.dormant = True
        
        # 创建选择卡牌对象
        choices = [
            self.controller.card("SW_079a", self),  # 短途：2回合后苏醒，抽1张牌
            self.controller.card("SW_079b", self),  # 中途：3回合后苏醒，抽2张牌
            self.controller.card("SW_079c", self),  # 长途：4回合后苏醒，抽3张牌
        ]
        
        # 让玩家选择飞行路线
        yield GenericChoice(CONTROLLER, choices)


class SW_079a:
    """短途飞行 / Short Flight"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    def play(self):
        """2回合后苏醒，抽1张牌"""
        # 找到杜加尔并添加苏醒追踪器
        dungars = [m for m in self.controller.field if m.id == "SW_079"]
        if dungars:
            dungar = dungars[0]
            yield Buff(dungar, "SW_079a_tracker", turns_to_wait=2, cards_to_draw=1)


class SW_079b:
    """中途飞行 / Medium Flight"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    def play(self):
        """3回合后苏醒，抽2张牌"""
        dungars = [m for m in self.controller.field if m.id == "SW_079"]
        if dungars:
            dungar = dungars[0]
            yield Buff(dungar, "SW_079b_tracker", turns_to_wait=3, cards_to_draw=2)


class SW_079c:
    """长途飞行 / Long Flight"""
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 0,
    }
    
    def play(self):
        """4回合后苏醒，抽3张牌"""
        dungars = [m for m in self.controller.field if m.id == "SW_079"]
        if dungars:
            dungar = dungars[0]
            yield Buff(dungar, "SW_079c_tracker", turns_to_wait=4, cards_to_draw=3)


class SW_079a_tracker:
    """短途飞行追踪器"""
    def apply(self, target):
        """初始化回合计数"""
        target.dungar_turns_remaining = 2
        target.dungar_cards_to_draw = 1
    
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 减少回合计数
            setattr(self.owner, 'dungar_turns_remaining', self.owner.dungar_turns_remaining - 1),
            # 如果到达时间,苏醒并抽牌
            (
                Awaken(self.owner),
                Draw(CONTROLLER) * self.owner.dungar_cards_to_draw,
                Destroy(SELF)
            ) if self.owner.dungar_turns_remaining <= 0 else None
        ]
    )


class SW_079b_tracker:
    """中途飞行追踪器"""
    def apply(self, target):
        target.dungar_turns_remaining = 3
        target.dungar_cards_to_draw = 2
    
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            setattr(self.owner, 'dungar_turns_remaining', self.owner.dungar_turns_remaining - 1),
            (
                Awaken(self.owner),
                Draw(CONTROLLER) * self.owner.dungar_cards_to_draw,
                Destroy(SELF)
            ) if self.owner.dungar_turns_remaining <= 0 else None
        ]
    )


class SW_079c_tracker:
    """长途飞行追踪器"""
    def apply(self, target):
        target.dungar_turns_remaining = 4
        target.dungar_cards_to_draw = 3
    
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            setattr(self.owner, 'dungar_turns_remaining', self.owner.dungar_turns_remaining - 1),
            (
                Awaken(self.owner),
                Draw(CONTROLLER) * self.owner.dungar_cards_to_draw,
                Destroy(SELF)
            ) if self.owner.dungar_turns_remaining <= 0 else None
        ]
    )



class SW_080:
    """考内留斯·罗姆 / Cornelius Roame
    在每个玩家回合的开始和结束时，抽一张牌。"""
    events = [
        OWN_TURN_BEGIN.on(Draw(CONTROLLER)),
        OWN_TURN_END.on(Draw(CONTROLLER)),
        BeginTurn(OPPONENT).on(Draw(CONTROLLER)),
        EndTurn(OPPONENT).on(Draw(CONTROLLER))
    ]


class SW_081:
    """瓦里安，暴风城国王 / Varian, King of Stormwind
    战吼：抽一张突袭随从以获得突袭。对嘲讽和圣盾重复此过程。"""
    play = (
        # 抽一张突袭随从，获得突袭
        Find(FRIENDLY_DECK + MINION + RUSH) & (
            (Draw(CONTROLLER, TARGET), SetTags(SELF, {GameTag.RUSH: True}))
        ) &
        # 抽一张嘲讽随从，获得嘲讽
        Find(FRIENDLY_DECK + MINION + TAUNT) & (
            (Draw(CONTROLLER, TARGET), SetTags(SELF, {GameTag.TAUNT: True}))
        ) &
        # 抽一张圣盾随从，获得圣盾
        Find(FRIENDLY_DECK + MINION + DIVINE_SHIELD) & (
            (Draw(CONTROLLER, TARGET), SetTags(SELF, {GameTag.DIVINE_SHIELD: True}))
        )
    )
