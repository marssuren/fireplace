"""
失落之城 - DRUID
"""
from ..utils import *
from .kindred_helpers import check_kindred_active


# COMMON

class DINO_130:
    """长颈龙蛋 - Longneck Egg
    2费 0/2 随从 - 迷你包
    <b>亡语:</b>召唤一只3/3的野兽。使你的随从获得+1/+1。
    
    Deathrattle: Summon a 3/3 Beast. Give your minions +1/+1.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = [
        # 召唤一只3/3的野兽
        Summon(CONTROLLER, "DINO_130t"),
        # 使所有友方随从获得+1/+1
        Buff(FRIENDLY_MINIONS, "DINO_130e")
    ]


class DINO_130e:
    """长颈龙蛋增益 - Longneck Egg Buff
    
    +1/+1
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class TLC_230:
    """树群来袭 - Treant Swarm
    5费 法术 - 自然学派
    选择一个随从。召唤四个2/2的树人攻击该随从。
    
    Choose a minion. Summon four 2/2 Treants that attack it.
    
    参考实现：ULD_212 (Wild Bloodstinger) 和 MIS_714 (Funhouse Mirror)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 召唤四个2/2树人并让它们攻击目标
        # 参考 ULD_212: Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION)).then(Attack(SELF, Summon.CARD))
        for _ in range(4):
            treant = yield Summon(CONTROLLER, "TLC_230t")
            # 使树人攻击目标（参考 whizbang/priest.py MIS_714）
            if treant and len(treant) > 0:
                yield Attack(treant[0], TARGET)


class TLC_231:
    """班纳布斯的故事 - Banabus's Tale
    2费 法术
    抽一张随从牌。如果其攻击力大于或等于5点，使其获得+5生命值并获得5点护甲值。
    
    Draw a minion. If it has 5 or more Attack, give it +5 Health and gain 5 Armor.
    """
    requirements = {}
    
    def play(self):
        # 抽一张随从牌
        drawn_card = yield ForceDraw(CONTROLLER, lambda c: c.type == CardType.MINION)
        
        # 检查抽到的牌是否攻击力>=5
        if drawn_card and len(drawn_card) > 0:
            card = drawn_card[0]
            if hasattr(card, 'atk') and card.atk >= 5:
                # 给予+5生命值
                yield Buff(card, "TLC_231e")
                # 获得5点护甲值
                yield GainArmor(FRIENDLY_HERO, 5)


class TLC_231e:
    """班纳布斯的故事增益 - Banabus's Tale Buff
    
    +5生命值
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.HEALTH: 5,
    }


class TLC_237:
    """啸天龙蛋 - Screechling Egg
    3费 0/2 随从
    <b>亡语:</b>召唤四只2/1的啸天龙宝宝。
    
    Deathrattle: Summon four 2/1 Screechlings.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "TLC_237t") * 4


# RARE

class DINO_421:
    """震地雷龙 - Earthshaker Brontosaurus
    9费 9/9 野兽 - 迷你包
    <b>嘲讽</b>。<b>扰魔</b>
    <b>亡语:</b>使你的手牌和牌库里的所有随从牌获得+3/+3。
    
    Taunt. Elusive. Deathrattle: Give all minions in your hand and deck +3/+3.
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.ELUSIVE: True,
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = [
        # 手牌中的随从+3/+3
        Buff(FRIENDLY_HAND + MINION, "DINO_421e"),
        # 牌库中的随从+3/+3
        Buff(FRIENDLY_DECK + MINION, "DINO_421e")
    ]


class DINO_421e:
    """震地雷龙增益 - Earthshaker Brontosaurus Buff
    
    +3/+3
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class DINO_432:
    """奔行豹面具 - Prowling Panther Mask
    4费 法术 - 迷你包
    将一个随从的属性值变为5/4并使其获得<b>潜行</b>。抽两张牌。
    
    Transform a minion into a 5/4 with Stealth. Draw 2 cards.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 将目标随从变为5/4并获得潜行
        yield Buff(TARGET, "DINO_432e")
        # 抽两张牌
        yield Draw(CONTROLLER) * 2


class DINO_432e:
    """奔行豹面具增益 - Prowling Panther Mask Buff
    
    属性变为5/4，获得潜行
    """
    atk = SET(5)
    max_health = SET(4)
    tags = {
        GameTag.STEALTH: True,
    }


class TLC_232:
    """待哺群雏 - Waiting Brood
    2费 法术
    在你的下个回合开始时，召唤三只2/1的啸天龙宝宝。
    
    At the start of your next turn, summon three 2/1 Screechlings.
    """
    requirements = {}
    
    def play(self):
        # 给玩家添加一个buff，在下回合开始时触发
        yield Buff(CONTROLLER, "TLC_232e")


class TLC_232e:
    """待哺群雏效果 - Waiting Brood Effect
    
    下回合开始时召唤三只2/1啸天龙宝宝
    """
    # 监听下回合开始事件
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 召唤三只2/1啸天龙宝宝
            Summon(CONTROLLER, "TLC_237t") * 3,
            # 移除此buff
            Destroy(SELF)
        ]
    )


class TLC_233:
    """孵化辅助师 - Hatching Assistant
    3费 2/3 随从
    <b>战吼:</b>使你的其他攻击力小于或等于2的随从获得+1/+2和<b>嘲讽</b>。
    
    Battlecry: Give your other minions with 2 or less Attack +1/+2 and Taunt.
    """
    def play(self):
        # 给所有其他攻击力<=2的友方随从+1/+2和嘲讽
        for minion in self.controller.field:
            if minion != self and minion.atk <= 2:
                yield Buff(minion, "TLC_233e")


class TLC_233e:
    """孵化辅助师增益 - Hatching Assistant Buff
    
    +1/+2和嘲讽
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class TLC_236:
    """杂交育种 - Hybrid Breeding
    5费 法术 - 自然学派
    抽取法力值消耗为（1），（2），（3），（4）的随从牌各一张。<b>延系:</b>其法力值消耗减少（1）点。
    
    Draw a (1), (2), (3), and (4)-Cost minion. Kindred: They cost (1) less.
    """
    requirements = {}
    
    def play(self):
        # 检查延系是否激活（上回合打出过野兽）
        from hearthstone.enums import Race
        kindred_active = check_kindred_active(self.controller, card_type=CardType.MINION, race=Race.BEAST)
        
        # 抽取1费、2费、3费、4费随从各一张
        for cost in [1, 2, 3, 4]:
            drawn_card = yield ForceDraw(CONTROLLER, lambda c, cost=cost: (
                c.type == CardType.MINION and c.cost == cost
            ))
            
            # 如果延系激活，减少1费
            if kindred_active and drawn_card:
                yield Buff(drawn_card[0], "TLC_236e")


class TLC_236e:
    """杂交育种减费 - Hybrid Breeding Cost Reduction
    
    法力值消耗减少（1）点
    """
    tags = {GameTag.COST: -1}


# EPIC

class TLC_234:
    """永生血瓣花 - Everlasting Bloodpetal
    4费 5/1 随从
    <b>亡语:</b>召唤一个0/1的永生花芽。
    
    Deathrattle: Summon a 0/1 Everlasting Bud.
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = Summon(CONTROLLER, "TLC_234t")


class TLC_235:
    """生命循环 - Circle of Life
    1费 法术 - 自然学派
    消灭一个随从，随机召唤一个法力值消耗相同的随从来替换它。
    
    Destroy a minion. Summon a random minion with the same Cost to replace it.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 记录目标随从的费用和控制者
        target_cost = TARGET.cost
        target_controller = TARGET.controller
        
        # 消灭目标随从
        yield Destroy(TARGET)
        
        # 召唤一个相同费用的随机随从（给目标的控制者）
        yield Summon(target_controller, RandomMinion(cost=target_cost))


# LEGENDARY

class TLC_239:
    """治愈荒野 - Heal the Wilds
    1费 法术 - 任务
    <b>任务:</b>填满你的面板，总计3回合。<b>奖励:</b>永茂之花。
    
    Quest: Fill your board 3 times. Reward: Everbloom.
    
    参考实现：UNG_116 (Jungle Giants) 和 ULD_155 (Unseal the Vault)
    使用标准的 progress_total、quest 和 reward 属性
    """
    tags = {
        GameTag.QUEST: True,
    }
    
    # 任务目标：填满面板3次
    progress_total = 3
    
    # 任务追踪：回合结束时检查场上是否有7个随从
    # 使用自定义事件监听，因为需要在回合结束时检查而不是触发时
    # 参考 deathknight.py TLC_433 的实现模式
    quest = OWN_TURN_END.on(
        Find(lambda self: len(self.controller.field) == 7) & AddProgress(SELF, 1)
    )
    
    # 任务奖励：给予永茂之花
    reward = Give(CONTROLLER, "TLC_239t")


class TLC_257:
    """洛，在世传奇 - Loh, Living Legend
    9费 5/5 随从 - 传说
    <b>战吼:</b>在本局对战中，你的随从牌的法力值消耗为（5）点。
    
    Battlecry: For the rest of the game, your minion cards cost (5).
    """
    def play(self):
        # 给玩家添加一个永久buff，使所有随从牌变为5费
        yield Buff(CONTROLLER, "TLC_257e")


class TLC_257e:
    """洛，在世传奇效果 - Loh, Living Legend Effect
    
    所有随从牌费用变为5费
    """
    class Hand:
        """手牌中的随从牌费用变为5费"""
        def cost(self, i):
            if self.owner.type == CardType.MINION:
                return 5
            return i
    
    class Deck:
        """牌库中的随从牌费用变为5费（显示用）"""
        def cost(self, i):
            if self.owner.type == CardType.MINION:
                return 5
            return i


# Token 定义已移至 tokens.py 文件
# 包括：
# - DINO_130t (长颈龙幼体 - 3/3野兽)
# - TLC_230t (树人 - 2/2)
# - TLC_237t (啸天龙宝宝 - 2/1野兽)
# - TLC_234t (永生花芽 - 0/1，亡语：召唤永生血瓣花)
# - TLC_239t (永茂之花 - 任务奖励地标)
