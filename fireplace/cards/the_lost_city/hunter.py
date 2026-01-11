"""
失落之城 - HUNTER
"""
from ..utils import *
from .kindred_helpers import check_kindred_active
from .map_helpers import mark_map_discovered_card, check_is_map_discovered_card


# COMMON

class DINO_403:
    """魔暴龙面具 - T-Rex Mask
    8费 法术
    将一个随从的属性值变为8/8。使其获得<b>冲锋</b>。
    
    Transform a minion into an 8/8 with Charge.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 将目标随从变为8/8并获得冲锋
        yield Morph(TARGET, "DINO_403e")


class DINO_403e:
    """魔暴龙面具变形 - T-Rex Mask Transformation
    
    8/8 冲锋
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.CHARGE: True,
    }


class DINO_434:
    """迅猛龙巢护工 - Raptor Nest Keeper
    1费 1/1
    <b>战吼：</b>随机获取一张法力值消耗为（1）的随从牌。<b>亡语：</b>随机获取一张法力值消耗为（1）的法术牌。
    
    Battlecry: Randomly get a (1)-Cost minion card. Deathrattle: Randomly get a (1)-Cost spell card.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    def play(self):
        # 战吼：随机获取一张1费随从牌
        yield Give(CONTROLLER, RandomCollectible(
            cost=1,
            type=CardType.MINION
        ))
    
    deathrattle = Give(CONTROLLER, RandomCollectible(
        cost=1,
        type=CardType.SPELL
    ))


class TLC_822:
    """恐龙保育师 - Dino Caretaker
    2费 2/3
    在你的回合结束时，随机使你手牌中一张野兽牌的法力值消耗减少（1）点。
    
    At the end of your turn, reduce the Cost of a random Beast in your hand by (1).
    """
    events = OWN_TURN_END.on(
        lambda self: [
            # 找到手牌中的所有野兽牌
            Find(FRIENDLY_HAND + MINION + BEAST) & [
                # 随机选择一张，减少1费
                Buff(RANDOM(FRIENDLY_HAND + MINION + BEAST), "TLC_822e")
            ]
        ]
    )


class TLC_822e:
    """恐龙保育师减费 - Dino Caretaker Cost Reduction"""
    tags = {GameTag.COST: -1}


class TLC_823:
    """恐惧畏缩 - Fearful Flinch
    2费 法术
    对一个随从造成$3点伤害。在本回合中，你使用的下一张野兽牌法力值消耗减少（2）点。
    
    Deal $3 damage to a minion. The next Beast you play this turn costs (2) less.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)
        
        # 给玩家添加buff，下一张野兽牌-2费
        yield Buff(CONTROLLER, "TLC_823e")


class TLC_823e:
    """恐惧畏缩效果 - Fearful Flinch Effect
    
    监听打出野兽牌，第一张野兽牌-2费
    """
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    
    class Hand:
        """手牌中的野兽牌-2费"""
        def cost(self, i):
            if self.owner.type == CardType.MINION and self.owner.race == Race.BEAST:
                return i - 2
            return i
    
    # 监听打出野兽牌后移除buff
    events = Play(CONTROLLER, MINION + BEAST).after(
        lambda self, source, card: Destroy(SELF)
    )


class TLC_824:
    """奇异的地图 - Odd Map
    1费 法术
    <b>发现</b>一张攻击力为奇数的野兽牌，如果你在本回合中使用该牌，再从其余选项中选择一张。
    
    Discover a Beast with odd Attack. If you play it this turn, pick from the other options.
    """
    requirements = {}
    
    def play(self):
        # 发现一张攻击力为奇数的野兽牌
        def is_odd_attack_beast(card):
            return (card.type == CardType.MINION and 
                    card.race == Race.BEAST and 
                    hasattr(card, 'atk') and 
                    card.atk % 2 == 1)
        
        # 使用 GenericChoice 进行发现
        cards = yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=is_odd_attack_beast,
            count=3
        ))
        
        # 记录发现的卡牌
        if cards:
            discovered_card = self.controller.hand[-1] if self.controller.hand else None
            
            if discovered_card:
                # 标记为地图发现的卡牌
                mark_map_discovered_card(self.controller, discovered_card.id)
                
                # 给玩家添加一个buff，监听本回合打出地图发现的卡牌
                yield Buff(CONTROLLER, "TLC_824e")


class TLC_824e:
    """奇异的地图效果 - Odd Map Effect
    
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
                # 再次发现一张攻击力为奇数的野兽牌（从剩余选项中）
                GenericChoice(CONTROLLER, cards=RandomCardGenerator(
                    CONTROLLER,
                    card_filter=lambda c: (c.type == CardType.MINION and 
                                          c.race == Race.BEAST and 
                                          hasattr(c, 'atk') and 
                                          c.atk % 2 == 1),
                    count=3
                ))
            ]
        )
    )


# RARE

class DINO_422:
    """甲龙 - Ankylodon
    6费 7/5 野兽
    <b>嘲讽</b>。<b>亡语：</b>随机召唤两只法力值消耗为（3）的野兽，并使其攻击随机敌人。
    
    Taunt. Deathrattle: Summon two random (3)-Cost Beasts and make them attack random enemies.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
    }
    
    def deathrattle(self):
        # 召唤两只3费野兽
        for _ in range(2):
            # 召唤一只3费野兽
            minion = yield Summon(CONTROLLER, RandomMinion(
                cost=3,
                race=Race.BEAST
            ))
            
            # 使其攻击随机敌人
            if minion and ENEMY_CHARACTERS:
                yield Attack(minion[0], RANDOM(ENEMY_CHARACTERS))


class TLC_366:
    """掠食飞翼龙 - Predatory Pterrordax
    6费 7/5 野兽
    <b>突袭</b>。<b>延系：</b>法力值消耗减少（2）点。
    
    Rush. Kindred: Costs (2) less.
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    cost_mod = lambda self, i: -2 if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST) else 0


class TLC_826:
    """卡纳莎的故事 - Carnassa's Tale
    2费 法术
    将十张法力值消耗为（1）的3/2的迅猛龙洗入你的牌库，这些迅猛龙具有"<b>战吼：</b>抽一张牌。"
    
    Shuffle ten 1-Cost 3/2 Raptors into your deck with "Battlecry: Draw a card."
    """
    requirements = {}
    
    def play(self):
        # 将10张卡纳莎的迅猛龙洗入牌库
        for _ in range(10):
            yield Shuffle(CONTROLLER, "TLC_826t")


class TLC_827:
    """食草剑龙 - Herbivore Stegosaurus
    3费 0/5 野兽
    在你的回合结束时，获得+1攻击力<i>（即便在手牌或牌库中）</i>。
    
    At the end of your turn, gain +1 Attack (wherever this is).
    """
    # 使用全局事件监听，无论在哪里都会触发
    events = OWN_TURN_END.on(
        lambda self: Buff(SELF, "TLC_827e")
    )


class TLC_827e:
    """食草剑龙增益 - Herbivore Stegosaurus Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


# EPIC

class TLC_825:
    """暴掠龙女王 - Ravenous Raptor Queen
    4费 5/4 野兽
    <b>延系：</b>对一个敌方随从造成等同于本随从攻击力的伤害。
    
    Kindred: Deal damage equal to this minion's Attack to an enemy minion.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        # 检查延系是否激活（上回合打出过野兽）
        if check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST):
            # 对目标造成等同于本随从攻击力的伤害
            if TARGET:
                yield Hit(TARGET, self.atk)


class TLC_828:
    """顶级恐龙学 - Top-Tier Dinosaurology
    5费 法术
    使你手牌，牌库和战场上的所有野兽获得+2/+2。
    
    Give all Beasts in your hand, deck, and battlefield +2/+2.
    """
    requirements = {}
    
    def play(self):
        # 给手牌、牌库和战场上的所有野兽+2/+2
        yield Buff(FRIENDLY_HAND + MINION + BEAST, "TLC_828e")
        yield Buff(FRIENDLY_DECK + MINION + BEAST, "TLC_828e")
        yield Buff(FRIENDLY + MINION + BEAST, "TLC_828e")


class TLC_828e:
    """顶级恐龙学增益 - Top-Tier Dinosaurology Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }


# LEGENDARY

class TLC_830:
    """食物链 - Food Chain
    1费 法术 - 任务
    <b>任务：</b>使用攻击力为1，3，5，7的野兽牌各一张。<b>奖励：</b>绍克。
    
    Quest: Play Beasts with 1, 3, 5, and 7 Attack. Reward: Shok.
    """
    tags = {
        GameTag.QUEST: True,
    }
    
    def play(self):
        """打出任务"""
        # 初始化任务进度追踪
        self.controller.quest_beasts_played = set()  # 记录已打出的攻击力
        self.controller.quest_target_attacks = {1, 3, 5, 7}  # 目标攻击力
        
        # 将任务放入秘密区
        self.zone = Zone.SECRET
        
        # 给玩家添加追踪器buff
        yield Buff(CONTROLLER, "TLC_830e")


class TLC_830e:
    """食物链追踪器 - Food Chain Tracker
    
    监听打出野兽牌，更新任务进度
    """
    # 监听打出野兽牌事件
    events = Play(CONTROLLER, MINION + BEAST).after(
        lambda self, source, card: (
            # 记录打出的野兽攻击力
            self.controller.quest_beasts_played.add(card.atk),
            
            # 检查是否完成任务（打出了1,3,5,7攻击力的野兽各一张）
            Find(self.controller.quest_beasts_played >= self.controller.quest_target_attacks) & [
                # 完成任务，给予奖励
                Give(CONTROLLER, "TLC_830t"),
                # 移除任务
                Destroy(Find(FRIENDLY_SECRETS + ID("TLC_830"))),
                # 移除追踪器
                Destroy(SELF)
            ]
        )
    )


class TLC_836:
    """环形山的尼利 - Nelly of the Crater
    3费 2/5 传说
    每当你使用一张法力值消耗为（1）的随从牌，使其属性值翻倍。每当你施放一个法力值消耗为（1）的法术，施放两次。
    
    Whenever you play a (1)-Cost minion, double its stats. Whenever you cast a (1)-Cost spell, cast it twice.
    """
    # 监听打出1费随从，使其属性值翻倍
    events = [
        Play(CONTROLLER, MINION + (COST == 1)).after(
            lambda self, source, card: Buff(card, "TLC_836e")
        ),
        # 监听施放1费法术，再次施放
        # CastSpell 会自动处理目标选择（随机目标）
        # 参考 titans/neutral_legendary.py 的 TTN_092 实现
        Play(CONTROLLER, SPELL + (COST == 1)).after(
            lambda self, source, card: [
                CastSpell(card)
            ]
        )
    ]


class TLC_836e:
    """环形山的尼利增益 - Nelly of the Crater Buff
    
    使随从属性值翻倍
    """
    # 使用动态属性计算（参考 GIL_128e）
    def apply(self, target):
        # 存储翻倍后的值
        self._xatk = target.atk * 2
        self._xhealth = target.max_health * 2
    
    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


# Token 定义已移至 tokens.py 文件
# 包括：TLC_826t (卡纳莎的迅猛龙), TLC_830t (绍克)
