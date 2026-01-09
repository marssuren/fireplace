"""
失落之城 - PALADIN
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from .map_helpers import mark_map_discovered_card, check_is_map_discovered_card


# COMMON

class DINO_404:
    """火鳃鱼人 - Firegill Murloc
    3费 3/2 元素+鱼人
    <b>延系：</b>使你的其他随从获得<b>突袭</b>。
    
    Kindred: Give your other minions Rush.
    
    官方验证：Hearthstone Wiki
    """
    requirements = {}
    
    def play(self):
        # 检查 Kindred 是否激活（上回合打出过元素或鱼人）
        kindred_active = (
            check_kindred_active(self.controller, CardType.MINION, Race.ELEMENTAL) or
            check_kindred_active(self.controller, CardType.MINION, Race.MURLOC)
        )
        
        if kindred_active:
            # 给所有其他友方随从获得突袭
            yield Buff(FRIENDLY_MINIONS - SELF, "DINO_404e")


class DINO_404e:
    """突袭"""
    tags = {GameTag.RUSH: True}


class DINO_405:
    """孵化仪典 - Hatching Ritual
    3费 神圣法术
    在你的下个回合结束时，使你的随从获得+2/+2。
    
    At the end of your next turn, give your minions +2/+2.
    
    官方验证：Hearthstone Wiki
    实现说明：给玩家添加一个buff，在下个回合结束时触发
    """
    requirements = {}
    
    def play(self):
        # 给玩家添加一个buff，在下个回合结束时触发
        yield Buff(CONTROLLER, "DINO_405e")


class DINO_405e:
    """孵化仪典效果 - Hatching Ritual Effect
    在下个回合结束时给所有随从+2/+2
    """
    # 监听己方回合结束事件
    events = OWN_TURN_END.on(
        # 给所有友方随从+2/+2
        Buff(FRIENDLY_MINIONS, "DINO_405e2"),
        # 移除此buff
        Destroy(SELF)
    )


class DINO_405e2:
    """+2/+2"""
    atk = 2
    max_health = 2


class TLC_428:
    """温泉踏浪鱼人 - Hot Spring Strider
    3费 2/4 鱼人
    <b>战吼：</b>你的下一张鱼人牌的法力值消耗减少（1）点。<b>延系：</b>且会获得<b>圣盾</b>。
    
    Battlecry: Your next Murloc costs (1) less. Kindred: It also gains Divine Shield.
    
    官方验证：Hearthstone Wiki
    """
    requirements = {}
    
    def play(self):
        # 检查 Kindred 是否激活（上回合打出过鱼人）
        kindred_active = check_kindred_active(self.controller, CardType.MINION, Race.MURLOC)
        
        # 给玩家添加buff，下一张鱼人减1费
        if kindred_active:
            yield Buff(CONTROLLER, "TLC_428e_kindred")
        else:
            yield Buff(CONTROLLER, "TLC_428e")


class TLC_428e:
    """下一张鱼人减1费"""
    class Hand:
        # 减少手牌中鱼人的费用
        update = Refresh(FRIENDLY_HAND + MINION + MURLOC, {GameTag.COST: -1})
    
    # 当打出鱼人后移除此buff
    events = Play(CONTROLLER, MINION + MURLOC).after(Destroy(SELF))


class TLC_428e_kindred:
    """下一张鱼人减1费并获得圣盾（Kindred版本）"""
    class Hand:
        # 减少手牌中鱼人的费用
        update = Refresh(FRIENDLY_HAND + MINION + MURLOC, {GameTag.COST: -1})
    
    # 当打出鱼人后给予圣盾并移除此buff
    events = Play(CONTROLLER, MINION + MURLOC).after(
        lambda self, source, card: [
            Buff(card, "TLC_428e_divine_shield"),
            Destroy(SELF)
        ]
    )


class TLC_428e_divine_shield:
    """圣盾"""
    tags = {GameTag.DIVINE_SHIELD: True}


class TLC_441:
    """整备团队 - Rally the Troops
    3费 神圣法术
    使一个友方随从和具有相同类型的其他友方随从获得+1/+2。
    
    Give a friendly minion and other friendly minions of the same type +1/+2.
    
    官方验证：Hearthstone Wiki
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        # 给目标随从+1/+2
        yield Buff(TARGET, "TLC_441e")
        
        # 获取目标随从的种族
        target_races = getattr(TARGET, 'races', [])
        if not target_races and hasattr(TARGET, 'race'):
            target_races = [TARGET.race]
        
        # 给所有其他相同种族的友方随从+1/+2
        if target_races:
            for minion in self.controller.field:
                if minion == TARGET:
                    continue
                
                # 检查是否有相同种族
                minion_races = getattr(minion, 'races', [])
                if not minion_races and hasattr(minion, 'race'):
                    minion_races = [minion.race]
                
                # 如果有任何相同种族，给予buff
                if any(race in target_races for race in minion_races):
                    yield Buff(minion, "TLC_441e")


class TLC_441e:
    """+1/+2"""
    atk = 1
    max_health = 2


class TLC_442:
    """淹没的地图 - Submerged Map
    1费 法术
    <b>发现</b>一张鱼人牌，如果你在本回合中使用该牌，再从其余选项中选择一张。
    
    Discover a Murloc. If you play it this turn, Discover again from the other options.
    
    官方验证：Hearthstone Wiki
    实现说明：使用地图卡牌机制
    """
    requirements = {}
    
    def play(self):
        # 发现一张鱼人牌
        cards = yield GenericChoice(
            CONTROLLER,
            cards=RandomCardGenerator(
                CONTROLLER,
                card_filter=lambda c: c.type == CardType.MINION and Race.MURLOC in getattr(c, 'races', [getattr(c, 'race', None)]),
                count=3
            )
        )
        
        if cards:
            discovered_card = cards[0]
            # 标记为地图发现的卡牌
            mark_map_discovered_card(self.controller, discovered_card.id)
            
            # 给玩家添加buff，监听该卡牌的使用
            yield Buff(CONTROLLER, "TLC_442e", 
                      discovered_card_id=discovered_card.id,
                      remaining_options=cards[1:] if len(cards) > 1 else [])


class TLC_442e:
    """淹没的地图效果 - Submerged Map Effect
    监听地图发现的卡牌是否被使用
    """
    def __init__(self, discovered_card_id='', remaining_options=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discovered_card_id = discovered_card_id
        self.remaining_options = remaining_options or []
    
    def _check_and_discover_again(self, played_card):
        """检查打出的卡牌是否是地图发现的，如果是则再次发现"""
        # 检查是否是本回合从地图发现的卡牌
        if check_is_map_discovered_card(self.controller, played_card.id):
            # 从剩余选项中再次选择
            if self.remaining_options:
                yield GenericChoice(CONTROLLER, cards=self.remaining_options)
            # 移除此buff
            yield Destroy(SELF)
    
    # 合并事件：监听打出卡牌和回合结束
    events = (
        Play(CONTROLLER).on(
            lambda self, source, card: self._check_and_discover_again(card)
        ),
        OWN_TURN_END.on(Destroy(SELF))
    )


# RARE

class DINO_424:
    """英雄欢迎仪式 - Hero's Welcome
    8费 神圣法术
    <b>发现</b>并召唤一个<b>传说</b>随从，将其属性值变为10/10。
    
    Discover and summon a Legendary minion. Set its stats to 10/10.
    
    官方验证：Hearthstone Wiki
    """
    requirements = {}
    
    def play(self):
        # 发现一个传说随从
        cards = yield GenericChoice(
            CONTROLLER,
            cards=RandomCardGenerator(
                CONTROLLER,
                card_filter=lambda c: c.type == CardType.MINION and c.rarity == Rarity.LEGENDARY,
                count=3
            )
        )
        
        if cards:
            # 召唤发现的随从
            summoned = yield Summon(CONTROLLER, cards[0].id)
            
            if summoned:
                # 将属性值设为10/10
                yield Buff(summoned[0], "DINO_424e")


class DINO_424e:
    """属性值设为10/10"""
    def apply(self, target):
        target.atk = 10
        target.max_health = 10
        target.damage = 0


class TLC_240:
    """填鳃暴龙 - Gillsaurus
    4费 3/3 野兽
    <b>突袭</b>。<b>亡语：</b> 召唤三个2/1的鱼人，使其各获得一项随机<b>额外效果</b>。
    
    Rush. Deathrattle: Summon three 2/1 Murlocs with a random Bonus Effect each.
    
    官方验证：Hearthstone Wiki
    参考：badlands/paladin.py - 随机额外效果机制
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.DEATHRATTLE: True,
    }
    
    @property
    def deathrattle(self):
        """亡语：召唤三个2/1鱼人，各有随机额外效果"""
        actions = []
        
        # 定义可能的额外效果
        bonus_effects = [
            "TLC_240e_divine_shield",  # 圣盾
            "TLC_240e_taunt",          # 嘲讽
            "TLC_240e_rush",           # 突袭
            "TLC_240e_lifesteal",      # 吸血
            "TLC_240e_poisonous",      # 剧毒
            "TLC_240e_windfury",       # 风怒
        ]
        
        # 召唤3个鱼人，每个都有随机效果
        for _ in range(3):
            # 召唤2/1鱼人
            summon_action = Summon(CONTROLLER, "TLC_240t")
            actions.append(summon_action)
            
            # 随机选择一个效果
            effect = self.game.random.choice(bonus_effects)
            # 给刚召唤的鱼人添加效果
            actions.append(Buff(Find(CONTROLLER_FIELD + FRIENDLY + LAST_SUMMONED), effect))
        
        return actions


# 额外效果Buff定义
class TLC_240e_divine_shield:
    """圣盾"""
    tags = {GameTag.DIVINE_SHIELD: True}


class TLC_240e_taunt:
    """嘲讽"""
    tags = {GameTag.TAUNT: True}


class TLC_240e_rush:
    """突袭"""
    tags = {GameTag.RUSH: True}


class TLC_240e_lifesteal:
    """吸血"""
    tags = {GameTag.LIFESTEAL: True}


class TLC_240e_poisonous:
    """剧毒"""
    tags = {GameTag.POISONOUS: True}


class TLC_240e_windfury:
    """风怒"""
    tags = {GameTag.WINDFURY: True}


class TLC_438:
    """紫色珍鳃鱼人 - Purple Pearlgill
    2费 1/2 鱼人
    <b>战吼：</b>从你的牌库中随机施放一个法力值消耗小于或等于（2）点的法术<i>（尽可能以本随从为目标）</i>。
    
    Battlecry: Cast a random spell from your deck that costs (2) or less (targets this if possible).
    
    官方验证：Hearthstone Wiki
    """
    requirements = {}
    
    def play(self):
        # 从牌库中找到所有2费或更低的法术
        eligible_spells = [
            card for card in self.controller.deck
            if card.type == CardType.SPELL and card.cost <= 2
        ]
        
        if eligible_spells:
            # 随机选择一个法术
            spell = self.game.random.choice(eligible_spells)
            
            # 施放法术（尽可能以本随从为目标）
            # 如果法术需要目标且本随从是合法目标，则以本随从为目标
            if spell.requirements.get(PlayReq.REQ_TARGET_TO_PLAY):
                # 检查本随从是否是合法目标
                if spell.requirements.get(PlayReq.REQ_MINION_TARGET):
                    # 以本随从为目标施放
                    yield Play(spell, target=SELF)
                else:
                    # 随机选择目标
                    yield Play(spell)
            else:
                # 不需要目标，直接施放
                yield Play(spell)


class TLC_444:
    """嘉沃顿的故事 - Gavotte's Tale
    2费 神圣法术
    使一个随从获得三项随机<b>额外效果</b>。
    
    Give a minion 3 random Bonus Effects.
    
    官方验证：Hearthstone Wiki
    参考：badlands/paladin.py - DEEP_033 (随机额外效果)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 定义可能的额外效果
        bonus_effects = [
            "TLC_444e_divine_shield",  # 圣盾
            "TLC_444e_taunt",          # 嘲讽
            "TLC_444e_rush",           # 突袭
            "TLC_444e_lifesteal",      # 吸血
            "TLC_444e_poisonous",      # 剧毒
            "TLC_444e_windfury",       # 风怒
            "TLC_444e_stealth",        # 潜行
            "TLC_444e_reborn",         # 复生
        ]
        
        # 随机选择3个不同的效果
        chosen = self.game.random.sample(bonus_effects, min(3, len(bonus_effects)))
        for effect in chosen:
            yield Buff(TARGET, effect)


# 额外效果Buff定义
class TLC_444e_divine_shield:
    """圣盾"""
    tags = {GameTag.DIVINE_SHIELD: True}


class TLC_444e_taunt:
    """嘲讽"""
    tags = {GameTag.TAUNT: True}


class TLC_444e_rush:
    """突袭"""
    tags = {GameTag.RUSH: True}


class TLC_444e_lifesteal:
    """吸血"""
    tags = {GameTag.LIFESTEAL: True}


class TLC_444e_poisonous:
    """剧毒"""
    tags = {GameTag.POISONOUS: True}


class TLC_444e_windfury:
    """风怒"""
    tags = {GameTag.WINDFURY: True}


class TLC_444e_stealth:
    """潜行"""
    tags = {GameTag.STEALTH: True}


class TLC_444e_reborn:
    """复生"""
    tags = {GameTag.REBORN: True}


# EPIC

class TLC_430:
    """圣窟生物 - Grotto Dweller
    4费 2/5 野兽
    在你的回合结束时，再次施放本回合中你施放过的一个随机神圣法术<i>（尽可能以本随从为目标）</i>。
    
    At the end of your turn, recast a random Holy spell you cast this turn (targets this if possible).
    
    官方验证：Hearthstone Wiki
    """
    # 监听己方回合结束事件
    events = OWN_TURN_END.on(
        lambda self: self._recast_holy_spell()
    )
    
    def _recast_holy_spell(self):
        """回合结束时重新施放一个随机神圣法术"""
        # 获取本回合施放过的神圣法术
        # 使用 cards_played_this_turn_ids 而非 cards_played_this_turn（后者是数字）
        holy_spells_played = [
            card_id for card_id in getattr(self.controller, 'cards_played_this_turn_ids', [])
            if self._is_holy_spell(card_id)
        ]
        
        if holy_spells_played:
            # 随机选择一个神圣法术
            spell_id = self.game.random.choice(holy_spells_played)
            
            # 创建法术实例
            spell = self.controller.card(spell_id, source=self)
            
            # 施放法术（尽可能以本随从为目标）
            if spell.requirements.get(PlayReq.REQ_TARGET_TO_PLAY):
                # 检查本随从是否是合法目标
                if spell.requirements.get(PlayReq.REQ_MINION_TARGET):
                    # 以本随从为目标施放
                    yield Play(spell, target=SELF)
                else:
                    # 随机选择目标
                    yield Play(spell)
            else:
                # 不需要目标，直接施放
                yield Play(spell)
    
    def _is_holy_spell(self, card_id):
        """检查卡牌是否是神圣法术"""
        try:
            from .. import db
            card_data = db[card_id]
            return (card_data.type == CardType.SPELL and 
                   getattr(card_data, 'spell_school', None) == SpellSchool.HOLY)
        except:
            return False


class TLC_477:
    """蛇颈龙骑手的祝福 - Plesiosaur Rider's Blessing
    5费 神圣法术
    使一个友方随从获得+4/+4和"<b>亡语：</b>随机召唤一个法力值消耗为（4）的随从。"
    
    Give a friendly minion +4/+4 and "Deathrattle: Summon a random 4-Cost minion."
    
    官方验证：Hearthstone Wiki
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        # 给目标随从+4/+4和亡语
        yield Buff(TARGET, "TLC_477e")


class TLC_477e:
    """+4/+4和亡语"""
    atk = 4
    max_health = 4
    tags = {GameTag.DEATHRATTLE: True}
    
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=4))


# LEGENDARY

class TLC_241:
    """蛇颈龙群的伊度 - Idu of the Plesiosaurs
    4费 2/7 传说随从
    当本随从存活时，你获取一张法力值消耗为（2）的神圣法术牌，该牌可以使一个随从获得+2/+2和<b>圣盾</b>。
    
    While this is alive, you have a 2-Cost Holy spell that gives a minion +2/+2 and Divine Shield.
    
    官方验证：Hearthstone Wiki
    实现说明：光环效果，持续给予玩家一张特殊法术
    """
    # 光环效果：当本随从在场时，持续给予玩家一张特殊法术
    update = (
        # 检查玩家手牌中是否已有此法术
        -Find(FRIENDLY_HAND + ID("TLC_241t")) & Give(CONTROLLER, "TLC_241t")
    )


class TLC_426:
    """潜入葛拉卡 - Dive into Grakka
    1费 传说任务
    <b>可重复任务：</b>召唤6个鱼人。<b>奖励：</b>你召唤的鱼人获得+1/+1。
    
    Repeatable Quest: Summon 6 Murlocs. Reward: Your Murlocs have +1/+1.
    
    官方验证：Hearthstone Wiki
    参考：the_lost_city/deathknight.py - TLC_433 任务系统
    
    实现说明：
    - 使用完整的任务系统实现
    - 监听召唤鱼人事件增加进度
    - 完成后给予永久光环buff
    - 可重复任务：完成后重置进度并保留任务
    """
    tags = {
        GameTag.QUEST: True,
        GameTag.QUEST_PROGRESS_TOTAL: 6,
        GameTag.QUEST_REWARD_DATABASE_ID: 0,  # 可重复任务
    }
    
    def play(self):
        """打出任务"""
        # 初始化任务进度
        self.controller.quest_progress = 0
        self.controller.quest_target = 6
        
        # 将任务放入秘密区
        self.zone = Zone.SECRET
        
        # 给玩家添加追踪器buff
        yield Buff(CONTROLLER, "TLC_426_tracker")
    
    def quest_reward(self):
        """任务完成奖励"""
        # 给玩家添加永久光环
        return [Buff(CONTROLLER, "TLC_426e")]


class TLC_426_tracker:
    """潜入葛拉卡追踪器 - Dive into Grakka Tracker
    
    监听召唤鱼人事件，更新任务进度
    """
    # 监听召唤鱼人事件
    events = Summon(CONTROLLER, MINION + MURLOC).after(
        lambda self, source, target: [
            # 更新任务进度
            SetTag(CONTROLLER, {GameTag.QUEST_PROGRESS: min(self.controller.quest_progress + 1, self.controller.quest_target})),
            
            # 检查是否完成任务
            (self.controller.quest_progress + 1 >= self.controller.quest_target) and [
                # 完成任务，给予奖励
                Buff(CONTROLLER, "TLC_426e"),
                # 重置任务进度（可重复任务）
                SetTag(CONTROLLER, {GameTag.QUEST_PROGRESS: 0})
            ]
        ]
    )


class TLC_426e:
    """鱼人光环 - Murloc Aura
    所有鱼人+1/+1
    
    这是一个永久光环，每次完成任务都会叠加一层
    """
    update = Refresh(FRIENDLY_MINIONS + MURLOC, {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    })

