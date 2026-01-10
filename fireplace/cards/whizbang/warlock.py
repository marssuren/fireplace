"""
威兹班的工坊 - WARLOCK
"""
from ..utils import *


# COMMON

class MIS_707:
    """批量生产 - Mass Production
    Draw 2 cards. Deal $3 damage to your hero. Shuffle 2 copies of this into your deck.
    抽两张牌。对你的英雄造成$3点伤害。将两张本牌的复制洗入你的牌库。
    """
    # 1费法术
    # 效果：抽2张牌，对自己造成3点伤害，洗入2张复制
    # 迷你包卡牌
    
    def play(self):
        # 抽两张牌
        yield Draw(CONTROLLER) * 2
        
        # 对自己的英雄造成3点伤害
        yield Hit(FRIENDLY_HERO, 3)
        
        # 将两张本牌的复制洗入牌库
        yield Shuffle(CONTROLLER, ExactCopy(SELF))
        yield Shuffle(CONTROLLER, ExactCopy(SELF))


class TOY_883:
    """掀桌子 - Table Flip
    Deal $3 damage to all enemy minions. Costs (1) less for each other card in your hand.
    对所有敌方随从造成$3点伤害。你每有一张其他手牌，本牌的法力值消耗便减少（1）点。
    """
    # 10费暗影法术
    # 效果：对所有敌方随从造成3点伤害
    # 费用减少：每有一张其他手牌减少1费
    
    play = Hit(ENEMY_MINIONS, 3)
    
    # 费用减少机制
    # 计算手牌数量（不包括本牌自己）
    class Hand:
        """动态费用减少 Aura"""
        def apply(self, target):
            # 计算手牌数量（不包括本牌）
            hand_count = len(target.controller.hand) - 1
            # 每张其他手牌减少1费
            target.cost -= hand_count
    
    update = Hand()


class TOY_914:
    """邪鬼皇后 - Wretched Queen
    <b>Taunt</b>
    <b>Deathrattle:</b> Summon two 4/6 Knights with <b>Taunt</b>.
    <b>嘲讽</b>
    <b>亡语：</b>召唤两个4/6并具有<b>嘲讽</b>的骑士。
    """
    # 8费 4/4 恶魔 嘲讽
    # 亡语：召唤两个4/6嘲讽骑士
    taunt = True
    deathrattle = Summon(CONTROLLER, "TOY_914t") * 2


class TOY_915:
    """桌游角色扮演玩家 - Tabletop Roleplayer
    <b>Miniaturize</b>
    <b>Battlecry:</b> Give a friendly Demon +2 Attack and <b>Immune</b> this turn.
    <b>微缩</b>
    <b>战吼：</b>在本回合中，使一个友方恶魔获得+2攻击力和<b>免疫</b>。
    """
    # 4费 4/3 微缩
    # 战吼：使一个友方恶魔+2攻击力和免疫（本回合）
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON}
    
    def play(self):
        if TARGET:
            # +2攻击力（本回合）
            yield Buff(TARGET, "TOY_915e")


# RARE

class MIS_027:
    """多米诺效应 - Domino Effect
    Deal $2 damage to a minion. Repeat to the left or right, dealing 1 more damage each time.
    对一个随从造成$2点伤害。向左侧或右侧重复此效果，每次伤害增加1点。
    """
    # 4费法术
    # 效果：对目标造成2点伤害，然后向左或右重复，每次+1伤害
    # 不受法术伤害加成影响
    # 迷你包卡牌
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        """
        多米诺效应实现
        从目标开始，向左或右侧连锁伤害
        每次伤害增加1点
        """
        target = self.target
        if not target:
            return
        
        # 对初始目标造成2点伤害
        yield Hit(target, 2)
        
        # 获取目标所在位置
        zone = target.zone
        if not zone or zone != Zone.PLAY:
            return
        
        # 获取目标在战场上的位置
        try:
            target_index = target.zone_position
        except:
            return
        
        # 随机选择方向（左或右）
        import random
        go_left = random.choice([True, False])
        
        # 当前伤害值（下一次是3点）
        damage = 3
        
        # 向选定方向连锁
        if go_left:
            # 向左侧（索引递减）
            for i in range(target_index - 1, -1, -1):
                minions = target.controller.field if target.controller == self.controller else target.controller.opponent.field
                if i < len(minions):
                    next_target = minions[i]
                    yield Hit(next_target, damage)
                    damage += 1
        else:
            # 向右侧（索引递增）
            minions = target.controller.field if target.controller == self.controller else target.controller.opponent.field
            for i in range(target_index + 1, len(minions)):
                next_target = minions[i]
                yield Hit(next_target, damage)
                damage += 1


class MIS_703:
    """地狱火！ - INFERNAL!
    <b>Taunt</b>. <b>Battlecry:</b> Set your hero's remaining Health to 15.
    <b>嘲讽</b>。<b>战吼：</b>将你的英雄的剩余生命值变为15。
    """
    # 4费 6/6 恶魔 嘲讽
    # 战吼：将英雄生命值设置为15
    # 迷你包卡牌
    taunt = True
    
    def play(self):
        # 将英雄生命值设置为15
        # 使用 SetCurrentHealth action
        yield SetCurrentHealth(FRIENDLY_HERO, 15)


class TOY_884:
    """抓娃娃 - Crane Game
    Summon copies of two Demons in your deck.
    召唤你牌库中两个恶魔的各一个复制。
    """
    # 8费法术
    # 效果：召唤牌库中两个恶魔的复制
    
    def play(self):
        # 从牌库中随机选择两个恶魔
        # 召唤它们的复制
        for _ in range(2):
            # 随机选择牌库中的一个恶魔
            demon = yield RandomCard(FRIENDLY_DECK + MINION + RACE(Race.DEMON))
            if demon:
                # 召唤复制
                yield Summon(CONTROLLER, Copy(demon))


class TOY_886:
    """决胜时刻 - Endgame
    Resurrect your last Demon that died.
    复活上一个死亡的你的恶魔。
    """
    # 2费暗影法术
    # 效果：复活最后一个死亡的恶魔
    
    def play(self):
        # 获取墓地中最后一个恶魔
        # 使用 FRIENDLY_GRAVEYARD 获取墓地
        graveyard = self.controller.graveyard
        
        # 从后向前查找最后一个恶魔
        for card in reversed(graveyard):
            if card.type == CardType.MINION and Race.DEMON in card.races:
                # 复活这个恶魔
                yield Summon(CONTROLLER, Copy(card))
                break


class TOY_916:
    """速写美术家 - Sketch Artist
    <b>Battlecry:</b> Draw a Shadow spell. Get a <b>Temporary</b> copy of it.
    <b>战吼：</b>抽一张暗影法术牌，获取一张它的<b>临时</b>复制。
    """
    # 3费 3/3
    # 战吼：抽一张暗影法术，获取临时复制
    
    def play(self):
        # 抽一张暗影法术牌
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL + SPELL_SCHOOL(SpellSchool.SHADOW))
        
        if drawn:
            spell = drawn[0]
            # 获取一张临时复制
            # 临时卡牌会在回合结束时消失
            copy = yield Give(CONTROLLER, Copy(spell))
            if copy:
                # 标记为临时卡牌
                yield Buff(copy[0], "TOY_916e")


# EPIC

class TOY_526:
    """凶魔城堡 - Malefic Rook
    <b>Battlecry:</b> Attack <b>YOUR</b> hero.
    <b>战吼：</b>攻击<b>你的</b>英雄。
    """
    # 3费 5/6 恶魔
    # 战吼：攻击自己的英雄
    
    def play(self):
        # 攻击自己的英雄
        # 使用 Attack action
        yield Attack(SELF, FRIENDLY_HERO)


class TOY_527:
    """诅咒之旅 - Cursed Campaign
    Give a friendly minion "<b>Deathrattle:</b> Summon two copies of this minion that are <b>Dormant</b> for 2 turns."
    使一个友方随从获得"<b>亡语：</b>召唤本随从的两个<b>休眠</b>2回合的复制。"
    """
    # 4费暗影法术
    # 效果：给友方随从添加亡语（召唤2个休眠2回合的复制）
    # 参考：TOY_644 (Red Card) 的 SetDormant 实现
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 给目标添加亡语 Buff
            yield Buff(TARGET, "TOY_527e")


# LEGENDARY

class TOY_524:
    """游戏主持奈姆希 - Game Master Nemsy
    <b>Battlecry:</b> Draw a Demon. <b>Deathrattle:</b> Swap places with it.
    <b>战吼：</b>抽一张恶魔牌。<b>亡语：</b>与其交换位置。
    """
    # 5费 3/6 传说
    # 战吼：抽一张恶魔牌
    # 亡语：与抽到的恶魔交换位置
    # 
    # 【实现说明】
    # "交换位置" 意味着：
    # 1. 将手牌中的恶魔召唤到战场
    # 2. 将奈姆希放回手牌
    # 使用 Buff 存储恶魔引用，在亡语时触发
    
    def play(self):
        # 抽一张恶魔牌
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + RACE(Race.DEMON))
        
        if drawn:
            demon = drawn[0]
            # 给自己添加 Buff，存储恶魔引用
            buff = yield Buff(SELF, "TOY_524e")
            if buff:
                # 存储恶魔引用到 Buff 上
                buff[0].stored_demon = demon


class TOY_529:
    """死亡轮盘 - Wheel of DEATH!!!
    Destroy your deck. In 5 turns, destroy the enemy hero.
    摧毁你的牌库。5回合后，消灭敌方英雄。
    """
    # 8费暗影法术 传说
    # 效果：摧毁牌库，5回合后消灭敌方英雄
    
    def play(self):
        # 摧毁牌库中的所有卡牌
        for card in list(self.controller.deck):
            yield Destroy(card)
        
        # 给控制者添加一个 Buff，5回合后触发
        yield Buff(CONTROLLER, "TOY_529e")


# ========================================
# Buff 定义
# ========================================

class TOY_915e:
    """桌游角色扮演玩家增益 - Tabletop Roleplayer Buff
    +2 Attack and Immune this turn
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.IMMUNE: True,
        GameTag.ATK: 2,
    }


class TOY_916e:
    """临时卡牌标记 - Temporary Card Marker
    Discarded at end of turn
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.GHOSTLY: True  # 临时卡牌标记
    }


class TOY_524e:
    """游戏主持奈姆希增益 - Game Master Nemsy Buff
    Stores the demon reference for deathrattle
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    @property
    def deathrattle(self):
        """
        动态亡语：与抽到的恶魔交换位置
        """
        # 检查是否存储了恶魔引用
        if hasattr(self, 'stored_demon') and self.stored_demon:
            demon = self.stored_demon
            # 检查恶魔是否还在手牌中
            if demon.zone == Zone.HAND and demon.controller == self.owner.controller:
                # 交换位置：将恶魔召唤到战场，将奈姆希放回手牌
                return [
                    Summon(CONTROLLER, demon),
                    Give(CONTROLLER, Copy(self.owner))
                ]
        return []


class TOY_527e:
    """诅咒之旅增益 - Cursed Campaign Buff
    Deathrattle: Summon two Dormant copies
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    @property
    def deathrattle(self):
        """
        动态亡语：召唤两个休眠2回合的复制
        使用 SetDormant action 设置休眠状态
        """
        # 获取被 Buff 的随从
        minion = self.owner
        
        # 召唤两个复制，并设置为休眠2回合
        # 使用 Summon.then(SetDormant) 链式调用
        return [
            Summon(CONTROLLER, Copy(minion)).then(SetDormant(Summon.CARD, 2)),
            Summon(CONTROLLER, Copy(minion)).then(SetDormant(Summon.CARD, 2))
        ]


class TOY_529e:
    """死亡轮盘增益 - Wheel of DEATH!!! Buff
    Destroy enemy hero in 5 turns
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化剩余回合数（5回合后触发）
        self.turns_remaining = 5
    
    # 每回合开始时检查
    events = BeginTurn(CONTROLLER).on(
        lambda self, source: [
            # 减少剩余回合数并检查是否触发
            self._decrease_turns(),
        ]
    )
    
    def _decrease_turns(self):
        """减少剩余回合数，如果为0则消灭敌方英雄并移除自己"""
        self.turns_remaining -= 1
        if self.turns_remaining <= 0:
            # 消灭敌方英雄
            return [
                Destroy(ENEMY_HERO),
                Destroy(SELF)  # 移除自己
            ]
        return []
