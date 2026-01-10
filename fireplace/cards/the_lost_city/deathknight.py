"""
失落之城 - DEATH KNIGHT
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from .map_helpers import mark_map_discovered_card, check_is_map_discovered_card


# COMMON

class DINO_417:
    """安魂仪典 - Rite of Souls
    1费 法术 - 暗影学派
    使你的随从获得+1攻击力和<b>突袭</b>。它们会在你的回合结束时死亡。
    
    Give your minions +1 Attack and Rush. They die at the end of your turn.
    """
    requirements = {}
    
    def play(self):
        # 给所有友方随从+1攻击力和突袭
        for minion in self.controller.field:
            yield Buff(minion, "DINO_417e")


class DINO_417e:
    """安魂仪典增益 - Rite of Souls Buff
    
    +1攻击力和突袭，回合结束时死亡
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.ATK: 1,
    }
    
    # 回合结束时死亡
    events = OWN_TURN_END.on(
        lambda self: Destroy(SELF)
    )


class TLC_401:
    """寒骨剑龙 - Frostbone Stegosaurus
    6费 6/3 亡灵+野兽 - 冰霜符文x2
    <b>亡语：</b>随机对三个敌人造成6点伤害。
    
    Deathrattle: Deal 6 damage randomly split among enemy characters.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 6) * 3


class TLC_435:
    """地窟地图 - Catacombs Map
    1费 法术 - 冰霜符文x2
    <b>发现</b>一张冰霜符文牌，如果你在本回合中使用该牌，再从其余选项中选择一张。
    
    Discover a Frost rune card. If you play it this turn, pick from the other options.
    """
    requirements = {}
    
    def play(self):
        # 发现一张冰霜符文牌
        # 过滤条件：有冰霜符文消耗的卡牌
        def has_frost_rune(card):
            if hasattr(card, 'rune_cost'):
                return card.rune_cost.get('frost', 0) > 0
            return False
        
        # 使用 GenericChoice 进行发现
        cards = yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=has_frost_rune,
            count=3
        ))
        
        # 记录发现的卡牌和其他选项
        if cards:
            discovered_card = self.controller.hand[-1] if self.controller.hand else None
            
            if discovered_card:
                # 标记为地图发现的卡牌
                mark_map_discovered_card(self.controller, discovered_card.id)
                
                # 给玩家添加一个buff，监听本回合打出地图发现的卡牌
                yield Buff(CONTROLLER, "TLC_435e")


class TLC_435e:
    """地窟地图效果 - Catacombs Map Effect
    
    监听本回合打出地图发现的卡牌，如果打出则再次发现
    """
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    
    # 监听玩家打出卡牌事件
    events = Play(CONTROLLER).after(
        lambda self, source, card: (
            check_is_map_discovered_card(self.controller, card.id)
            and [
                # 再次发现一张冰霜符文牌（从剩余选项中）
                GenericChoice(CONTROLLER, cards=RandomCardGenerator(
                    CONTROLLER,
                    card_filter=lambda c: hasattr(c, 'rune_cost') and c.rune_cost.get('frost', 0) > 0,
                    count=3
                ))
            ]
        )
    )


class TLC_443:
    """不情愿的饲养员 - Reluctant Keeper
    3费 1/1 - 无符文
    <b>复生</b>。<b>亡语：</b>召唤一只2/2并具有<b>嘲讽</b>的亡灵野兽。
    
    Reborn. Deathrattle: Summon a 2/2 Undead Beast with Taunt.
    """
    tags = {
        GameTag.REBORN: True,
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "TLC_443t")


# RARE

class DINO_415:
    """安布拉的故事 - Ambra's Tale
    7费 法术 - 无符文（迷你包）
    <b>发现</b>一个法力值消耗大于或等于（5）点的<b>亡语</b>随从，召唤该随从并触发其<b>亡语</b>。
    
    Discover a Deathrattle minion that costs (5) or more. Summon it and trigger its Deathrattle.
    """
    requirements = {}
    
    def play(self):
        # 发现一个5费以上的亡语随从
        cards = yield DISCOVER(RandomCollectible(
            cost_min=5,
            type=CardType.MINION,
            deathrattle=True
        ))
        
        if cards:
            # 召唤发现的随从
            minion = yield Summon(CONTROLLER, cards[0])
            
            # 触发其亡语
            if minion:
                yield Deathrattle(minion[0])


class DINO_416:
    """空角恐角龙 - Hollow Ceratops
    5费 5/4 亡灵+野兽 - 无符文（迷你包）
    <b>突袭</b>。在一个友方随从死亡后，消耗3份<b>残骸</b>以获得<b>复生</b>。
    
    Rush. After a friendly minion dies, spend 3 Corpses to gain Reborn.
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    # 监听友方随从死亡事件
    events = Death(FRIENDLY + MINION).on(
        lambda self, source, target: (
            target != self  # 不是自己死亡
            and self.controller.corpses >= 3  # 有足够的残骸
            and not self.reborn  # 还没有复生
            and [
                # 消耗3残骸
                SpendCorpses(CONTROLLER, 3),
                # 获得复生
                Buff(SELF, "DINO_416e")
            ]
        )
    )


class DINO_416e:
    """空角恐角龙复生 - Hollow Ceratops Reborn Buff"""
    tags = {
        GameTag.REBORN: True,
    }


class TLC_432:
    """恐惧迅猛龙 - Dread Raptor
    4费 3/4 亡灵+野兽 - 冰霜符文x1 + 亡灵符文x1
    <b>战吼：</b>抽一张法力值消耗小于或等于（3）点的<b>亡语</b>随从牌。<b>延系：</b>其法力值消耗变为（0）点。
    
    Battlecry: Draw a Deathrattle minion that costs (3) or less. Kindred: It costs (0).
    """
    def play(self):
        # 抽一张3费以下的亡语随从
        drawn_card = yield ForceDraw(CONTROLLER, lambda c: (
            c.type == CardType.MINION 
            and c.cost <= 3 
            and (hasattr(c, 'deathrattles') and c.deathrattles or GameTag.DEATHRATTLE in c.tags)
        ))
        
        # 检查延系是否激活（上回合打出过亡灵野兽）
        from hearthstone.enums import Race
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.UNDEAD) or \
           check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST):
            # 使抽到的牌变为0费
            if drawn_card:
                yield Buff(drawn_card[0], "TLC_432e")


class TLC_432e:
    """恐惧迅猛龙减费 - Dread Raptor Cost Reduction"""
    cost = SET(0)


class TLC_434:
    """古生物秘术 - Paleontology
    3费 法术 - 暗影学派 - 亡灵符文x1
    <b>发现</b>一张亡灵牌。消耗5份<b>残骸</b>，改为保留全部三张牌。
    
    Discover an Undead card. Spend 5 Corpses to keep all 3.
    """
    requirements = {}
    
    def play(self):
        # 检查是否有5份残骸
        from hearthstone.enums import Race
        
        # 定义亡灵牌过滤器
        def is_undead(card):
            if card.type == CardType.MINION and hasattr(card, 'race'):
                races = getattr(card, 'races', [card.race])
                return Race.UNDEAD in races
            return False
        
        # 如果有5份残骸，保留全部三张（参考 BOT_299 的实现）
        if self.controller.corpses >= 5:
            # 消耗5份残骸
            yield SpendCorpses(CONTROLLER, 5)
            
            # 保留全部三张
            yield Give(CONTROLLER, RandomCollectible(card_filter=is_undead)) * 3
        else:
            # 正常发现一张亡灵牌
            yield DISCOVER(RandomCollectible(card_filter=is_undead))


class TLC_440:
    """封冻沉眠 - Frozen Slumber
    4费 法术 - 冰霜学派 - 冰霜符文x2
    造成$4点伤害并抽一张牌。<b>延系：</b>再抽一张。
    
    Deal $4 damage and draw a card. Kindred: Draw another.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 造成4点伤害
        yield Hit(TARGET, 4)
        
        # 抽一张牌
        yield Draw(CONTROLLER)
        
        # 检查延系是否激活（上回合打出过冰霜法术）
        from hearthstone.enums import SpellSchool
        if check_kindred_active(self.controller, card_type=CardType.SPELL, spell_school=SpellSchool.FROST):
            # 再抽一张牌
            yield Draw(CONTROLLER)


# EPIC

class TLC_436:
    """重生的翼手龙 - Reanimated Pterrordax
    5费 4/3 亡灵+野兽 - 无符文
    <b><b>突袭</b>。吸血</b>
    消耗<b>残骸</b>而非法力值。
    
    Rush, Lifesteal. Costs Corpses instead of Mana.
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.LIFESTEAL: True,
    }
    
    # 消耗残骸而非法力值
    # 使用 cost_mod 实现动态费用计算（参考 TTN_459）
    
    cost_mod = lambda self, i: -self.cost if self.controller.corpses >= self.cost else 0
    
    # 标记此卡牌消耗残骸而非法力值
    # 核心引擎会在打出时检查此属性
    costs_corpses_instead_of_mana = True


class TLC_439:
    """焦油狂潮 - Tar Surge
    4费 法术 - 冰霜符文x1 + 亡灵符文x1
    对所有敌方随从造成$2点伤害。下个回合，敌方随从牌的法力值消耗增加（2）点。
    
    Deal $2 damage to all enemy minions. Next turn, enemy minion cards cost (2) more.
    """
    requirements = {}
    
    def play(self):
        # 对所有敌方随从造成2点伤害
        yield Hit(ENEMY_MINIONS, 2)
        
        # 给对手添加一个buff，下回合敌方随从牌+2费
        yield Buff(OPPONENT, "TLC_439e")


class TLC_439e:
    """焦油狂潮效果 - Tar Surge Effect
    
    下回合敌方随从牌+2费
    """
    class Hand:
        """手牌中的随从牌+2费"""
        def cost(self, i):
            if self.owner.type == CardType.MINION:
                return i + 2
            return i
    
    # 在对手回合结束时移除此效果
    events = OWN_TURN_END.on(
        lambda self: Destroy(SELF)
    )


# LEGENDARY

class TLC_433:
    """恐怖再起 - Terror Rises
    1费 法术 - 任务 - 鲜血符文x1 + 亡灵符文x1
    <b>任务：</b>消耗15份<b>残骸</b>。<b>奖励：</b>泰拉克斯，魔骸暴龙。
    
    Quest: Spend 15 Corpses. Reward: Terrax, the Bone Tyrant.
    """
    tags = {
        GameTag.QUEST: True,
    }
    
    def play(self):
        """打出任务"""
        # 初始化任务进度
        self.controller.quest_progress = 0
        self.controller.quest_target = 15
        
        # 将任务放入秘密区
        self.zone = Zone.SECRET
        
        # 给玩家添加追踪器buff
        yield Buff(CONTROLLER, "TLC_433e")
    
    def quest_reward(self):
        """任务完成奖励"""
        # 给予泰拉克斯，魔骸暴龙
        return [Give(CONTROLLER, "TLC_433t")]


class TLC_433e:
    """恐怖再起追踪器 - Terror Rises Tracker
    
    监听残骸消耗事件，更新任务进度
    """
    # 监听残骸消耗事件（核心引擎已完整支持 SpendCorpses 事件）
    # SpendCorpses 在 actions.py 中实现，包括事件广播和追踪机制
    
    events = SpendCorpses(CONTROLLER).after(
        lambda self, source, amount: [
            # 更新任务进度
            SetTags(CONTROLLER, {GameTag.QUEST_PROGRESS: min(self.controller.quest_progress + amount, self.controller.quest_target})),
            
            # 检查是否完成任务
            Find(self.controller.quest_progress >= self.controller.quest_target) & [
                # 完成任务，给予奖励
                Give(CONTROLLER, "TLC_433t"),
                # 移除任务
                Destroy(Find(FRIENDLY_SECRETS + ID("TLC_433"))),
                # 移除追踪器
                Destroy(SELF)
            ]
        ]
    )


class TLC_810:
    """高阶教徒赫雷恩 - High Cultist Herenn
    7费 6/6 - 无符文（可能是Token或特殊卡牌）
    <b>战吼：</b>从你的牌库中召唤两个<b>亡语</b>随从，并使其互相攻击！
    
    Battlecry: Summon two Deathrattle minions from your deck and make them attack each other!
    """
    def play(self):
        # 从牌库中找到两个亡语随从
        deathrattle_minions = [
            card for card in self.controller.deck
            if card.type == CardType.MINION 
            and (hasattr(card, 'deathrattles') and card.deathrattles or GameTag.DEATHRATTLE in card.tags)
        ]
        
        if len(deathrattle_minions) >= 2:
            # 随机选择两个（使用 self.game.random）
            selected = self.game.random.sample(deathrattle_minions, 2)
            
            # 召唤第一个随从
            minion1 = yield Summon(CONTROLLER, selected[0])
            
            # 召唤第二个随从
            minion2 = yield Summon(CONTROLLER, selected[1])
            
            # 使它们互相攻击
            if minion1 and minion2:
                yield Attack(minion1[0], minion2[0])
        elif len(deathrattle_minions) == 1:
            # 只有一个亡语随从，只召唤它
            yield Summon(CONTROLLER, deathrattle_minions[0])


# Token 定义已移至 tokens.py 文件
# 包括：TLC_443t (不情愿的宠物), TLC_433t (泰拉克斯，魔骸暴龙)
