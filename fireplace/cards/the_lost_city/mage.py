"""
失落之城 - MAGE
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from hearthstone.enums import Race, SpellSchool


# COMMON

class DINO_414:
    """祭礼之舞 - Ritual Dance
    5费 法术
    选择一个随从，将其变形成为你另选的一个不同的随从。
    
    Choose a minion. Transform it into a different minion you choose.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 第一次选择：选择要变形的随从（已通过 TARGET 完成）
        # 第二次选择：发现一个随从进行变形
        cards = yield DISCOVER(RandomCollectible(type=CardType.MINION))
        
        if cards:
            # 将目标随从变形为发现的随从
            yield Morph(TARGET, cards[0])


class TLC_220:
    """扫页疾风 - Page Gust
    4费 4/5 元素
    在你召唤一个元素后，随机对一个敌人造成3点伤害。
    
    After you summon an Elemental, deal 3 damage to a random enemy.
    """
    # 监听召唤元素事件
    events = Summon(CONTROLLER, ELEMENTAL).after(
        lambda self, source, target: (
            target != self  # 不是自己被召唤
            and Hit(RANDOM_ENEMY_CHARACTER, 3)
        )
    )


class TLC_461:
    """拾荒清道夫 - Scavenging Scavenger
    1费 1/1
    <b>战吼：</b><b>发现</b>一张法力值消耗等同于你剩余法力水晶数量的卡牌。
    
    Battlecry: Discover a card that costs the same as your remaining Mana.
    """
    def play(self):
        # 获取剩余法力值
        remaining_mana = self.controller.mana
        
        # 发现一张法力值等于剩余法力的卡牌
        yield DISCOVER(RandomCollectible(cost=remaining_mana))


class TLC_483:
    """宝库闯入者 - Vault Raider
    3费 2/4
    在你<b>发现</b>一张卡牌后，使其法力值消耗减少（1）点。
    
    After you Discover a card, reduce its Cost by (1).
    """
    # 监听发现事件
    # 注意：这需要监听 GenericChoice 事件，当选择完成后触发
    events = GenericChoice(CONTROLLER).after(
        lambda self, source: (
            # 检查手牌中最后一张卡牌（刚发现的）
            self.controller.hand
            and Buff(self.controller.hand[-1], "TLC_483e")
        )
    )


class TLC_483e:
    """宝库闯入者减费 - Vault Raider Cost Reduction"""
    tags = {GameTag.COST: -1}


# RARE

class DINO_409:
    """科技恐龙 - Tech Dinosaur
    7费 3/6 机械+野兽
    <b>嘲讽</b>。在本局对战中，你每使用一张你的套牌之外的卡牌，本牌的法力值消耗便减少（1）点。
    
    Taunt. Costs (1) less for each card you've played that didn't start in your deck this game.
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    
    cost_mod = lambda self, i: -len(getattr(self.controller, 'cards_not_started_in_deck_played', []))


class DINO_429:
    """绵羊面具 - Sheep Mask
    4费 法术
    将一个随从的属性值变为1/1并使其获得"<b>亡语：</b>对所有随从造成2点伤害。"
    
    Transform a minion into a 1/1 that has "Deathrattle: Deal 2 damage to all minions."
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 将目标随从变为1/1
        yield SetTags(TARGET, {GameTag.ATK: 1, GameTag.HEALTH: 1})
        
        # 添加亡语：对所有随从造成2点伤害
        yield Buff(TARGET, "DINO_429e")


class DINO_429e:
    """绵羊面具亡语 - Sheep Mask Deathrattle"""
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Hit(ALL_MINIONS, 2)


class TLC_334:
    """列王遗宝 - Regal Relics
    7费 法术
    <b>发现</b>一张法力值消耗大于或等于（8）点的任意职业法术牌，其法力值消耗为（1）点。
    
    Discover a spell from any class that costs (8) or more. It costs (1).
    """
    requirements = {}
    
    def play(self):
        # 发现一张8费以上的任意职业法术
        cards = yield DISCOVER(RandomCollectible(
            type=CardType.SPELL,
            cost_min=8
        ))
        
        if cards:
            # 使发现的卡牌费用变为1
            discovered_card = self.controller.hand[-1] if self.controller.hand else None
            if discovered_card:
                yield Buff(discovered_card, "TLC_334e")


class TLC_334e:
    """列王遗宝费用 - Regal Relics Cost"""
    cost = SET(1)


class TLC_364:
    """时空之门的故事 - Tale of the Timeways
    2费 法术
    使你手牌中套牌之外的牌的法力值消耗减少（1）点。
    
    Reduce the Cost of cards in your hand that didn't start in your deck by (1).
    """
    requirements = {}
    
    def play(self):
        # 遍历手牌，给所有套牌外卡牌减费
        for card in self.controller.hand:
            # 检查卡牌是否为套牌外卡牌
            if hasattr(card, 'started_in_deck') and not card.started_in_deck:
                yield Buff(card, "TLC_364e")


class TLC_364e:
    """时空之门的故事减费 - Tale of the Timeways Cost Reduction"""
    tags = {GameTag.COST: -1}


class TLC_365:
    """乱翻库存 - Rummaging Around
    3费 法术 - 奥术学派
    对一个随从造成$3点伤害。如果你在本回合中<b>发现</b>过，则本牌的法力值消耗为（0）点。
    
    Deal $3 damage to a minion. Costs (0) if you've Discovered this turn.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    
    cost_mod = lambda self, i: -self.cost if (hasattr(self.controller, 'cards_discovered_this_turn') and self.controller.cards_discovered_this_turn > 0) else 0
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)


# EPIC

class TLC_226:
    """咒术图书管理员 - Arcane Librarian
    3费 2/2 元素
    <b>亡语：</b>抽一张法术牌。<b>延系：</b>召唤一个本随从的复制。
    
    Deathrattle: Draw a spell. Kindred: Summon a copy of this.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    def play(self):
        # 检查延系是否激活（上回合打出过元素）
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.ELEMENTAL):
            # 召唤一个本随从的复制
            yield Summon(CONTROLLER, ExactCopy(SELF))
    
    deathrattle = ForceDraw(CONTROLLER, lambda c: c.type == CardType.SPELL)


class TLC_462:
    """出土神器 - Unearthed Artifact
    2费 法术
    随机召唤一个法力值消耗为（2）的随从。如果你在本回合中<b><b>发现</b>过</b>，改为随机召唤一个法力值消耗为（4）的随从。
    
    Summon a random (2)-Cost minion. If you've Discovered this turn, summon a (4)-Cost one instead.
    """
    requirements = {}
    
    def play(self):
        # 检查本回合是否发现过
        if hasattr(self.controller, 'cards_discovered_this_turn') and self.controller.cards_discovered_this_turn > 0:
            # 召唤一个4费随从
            yield Summon(CONTROLLER, RandomMinion(cost=4))
        else:
            # 召唤一个2费随从
            yield Summon(CONTROLLER, RandomMinion(cost=2))


# LEGENDARY

class TLC_452:
    """泰坦考据学家欧斯克 - Oskar, Titan Archaeologist
    6费 6/6 传说随从
    在你的手牌中时，随机获得一项<b>泰坦</b>技能。该技能每回合都会改变。
    
    While in your hand, gain a random Titan ability. It changes each turn.
    """
    # 基础版本（无泰坦技能）
    # 在手牌中时，每回合开始会变形为带有泰坦技能的版本之一
    
    class Hand:
        """手牌触发器：回合开始时随机变形为带有泰坦技能的版本"""
        events = OWN_TURN_BEGIN.on(
            # 随机选择一个泰坦技能版本
            # 使用 Morph 变形为 TLC_452a/b/c/d 之一
            lambda self, source: (
                # 随机选择一个版本（4个泰坦技能）
                Morph(SELF, self.game.random.choice([
                    "TLC_452a",  # 版本A：造成伤害
                    "TLC_452b",  # 版本B：抽牌
                    "TLC_452c",  # 版本C：召唤随从
                    "TLC_452d",  # 版本D：发现法术
                ]))
            )
        )


# 泰坦技能版本A：造成伤害
class TLC_452a:
    """泰坦考据学家欧斯克 - 版本A
    6费 6/6 传说随从
    <b>泰坦</b>：对所有敌方随从造成2点伤害。
    """
    tags = {
        GameTag.TITAN: True,
    }
    
    # 泰坦技能1：对所有敌方随从造成2点伤害
    def titan_ability_1(self):
        yield Hit(ENEMY_MINIONS, 2)
    
    class Hand:
        """手牌触发器：回合开始时随机变形为其他版本"""
        events = OWN_TURN_BEGIN.on(
            lambda self, source: (
                Morph(SELF, self.game.random.choice([
                    "TLC_452",   # 基础版本
                    "TLC_452b",  # 版本B
                    "TLC_452c",  # 版本C
                    "TLC_452d",  # 版本D
                ]))
            )
        )


# 泰坦技能版本B：抽牌
class TLC_452b:
    """泰坦考据学家欧斯克 - 版本B
    6费 6/6 传说随从
    <b>泰坦</b>：抽两张牌。
    """
    tags = {
        GameTag.TITAN: True,
    }
    
    # 泰坦技能1：抽两张牌
    def titan_ability_1(self):
        yield Draw(CONTROLLER) * 2
    
    class Hand:
        """手牌触发器：回合开始时随机变形为其他版本"""
        events = OWN_TURN_BEGIN.on(
            lambda self, source: (
                Morph(SELF, self.game.random.choice([
                    "TLC_452",   # 基础版本
                    "TLC_452a",  # 版本A
                    "TLC_452c",  # 版本C
                    "TLC_452d",  # 版本D
                ]))
            )
        )


# 泰坦技能版本C：召唤随从
class TLC_452c:
    """泰坦考据学家欧斯克 - 版本C
    6费 6/6 传说随从
    <b>泰坦</b>：召唤两个2/2的随从。
    """
    tags = {
        GameTag.TITAN: True,
    }
    
    # 泰坦技能1：召唤两个2/2的随从
    def titan_ability_1(self):
        yield Summon(CONTROLLER, "TLC_452t") * 2
    
    class Hand:
        """手牌触发器：回合开始时随机变形为其他版本"""
        events = OWN_TURN_BEGIN.on(
            lambda self, source: (
                Morph(SELF, self.game.random.choice([
                    "TLC_452",   # 基础版本
                    "TLC_452a",  # 版本A
                    "TLC_452b",  # 版本B
                    "TLC_452d",  # 版本D
                ]))
            )
        )


# 泰坦技能版本D：发现法术
class TLC_452d:
    """泰坦考据学家欧斯克 - 版本D
    6费 6/6 传说随从
    <b>泰坦</b>：<b>发现</b>一张法术牌。
    """
    tags = {
        GameTag.TITAN: True,
    }
    
    # 泰坦技能1：发现一张法术牌
    def titan_ability_1(self):
        yield DISCOVER(RandomCollectible(type=CardType.SPELL))
    
    class Hand:
        """手牌触发器：回合开始时随机变形为其他版本"""
        events = OWN_TURN_BEGIN.on(
            lambda self, source: (
                Morph(SELF, self.game.random.choice([
                    "TLC_452",   # 基础版本
                    "TLC_452a",  # 版本A
                    "TLC_452b",  # 版本B
                    "TLC_452c",  # 版本C
                ]))
            )
        )


class TLC_460:
    """禁忌序列 - Forbidden Sequence
    1费 法术 - 任务
    <b>任务：</b><b>发现</b>7张牌。<b>奖励：</b>源生之石。
    
    Quest: Discover 7 cards. Reward: Primordial Stone.
    """
    tags = {
        GameTag.QUEST: True,
    }
    
    def play(self):
        """打出任务"""
        # 初始化任务进度
        self.controller.quest_progress = 0
        self.controller.quest_target = 7
        
        # 将任务放入秘密区
        self.zone = Zone.SECRET
        
        # 给玩家添加追踪器buff
        yield Buff(CONTROLLER, "TLC_460e")
    
    def quest_reward(self):
        """任务完成奖励"""
        # 给予源生之石
        return [Give(CONTROLLER, "TLC_460t")]


class TLC_460e:
    """禁忌序列追踪器 - Forbidden Sequence Tracker
    
    监听发现事件，更新任务进度
    """
    # 监听发现事件
    events = GenericChoice(CONTROLLER).after(
        lambda self, source: [
            # 更新任务进度
            SetTags(CONTROLLER, {GameTag.QUEST_PROGRESS: min(self.controller.quest_progress + 1, self.controller.quest_target)}),
            
            # 检查是否完成任务
            Find(self.controller.quest_progress >= self.controller.quest_target) & [
                # 完成任务，给予奖励
                Give(CONTROLLER, "TLC_460t"),
                # 移除任务
                Destroy(Find(FRIENDLY_SECRETS + ID("TLC_460"))),
                # 移除追踪器
                Destroy(SELF)
            ]
        ]
    )

