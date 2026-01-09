"""
穿越时间流 - SHAMAN
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_212:
    """引雷针 - Lightning Rod
    Deal $2 damage to a friendly minion to deal $4 damage to a random enemy minion.
    
    1费 自然法术
    对一个友方随从造成$2点伤害，对一个随机敌方随从造成$4点伤害。
    
    这张卡是自然法术伤害协同的关键卡牌，可以触发 Flux Revenant 和 Stormrook 的效果。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 对友方随从造成2点伤害
            yield Hit(TARGET, 2)
            
            # 对随机敌方随从造成4点伤害
            yield Hit(RANDOM_ENEMY_MINION, 4)
        
        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_213:
    """始源监督者 - Primordial Overseer
    [x]Battlecry: If you've cast a Nature spell while holding this, gain +1/+1 and draw a card.
    
    2费 2/3 随从
    战吼：如果你在本牌在你手中时施放过自然法术，获得+1/+1并抽一张牌。
    
    如果触发，这是一个2费3/4抽牌的强力效果。
    """
    requirements = {}
    
    # powered_up 用于UI显示（高亮效果）
    powered_up = lambda self: getattr(self, '_cast_nature_while_holding', False)
    
    def play(self):
        # 检查是否在手牌中时施放过自然法术
        if getattr(self, '_cast_nature_while_holding', False):
            # 获得 +1/+1
            yield Buff(SELF, "TIME_213e")
            # 抽一张牌
            yield Draw(self.controller)
    
    class Hand:
        # 监听自然法术施放事件
        events = OWN_SPELL_PLAY.on(
            lambda self, player, card, *args: (
                card.spell_school == SpellSchool.NATURE and
                setattr(self.owner, '_cast_nature_while_holding', True)
            )
        )


class TIME_213e:
    """始源监督者 - +1/+1"""
    atk = 1
    max_health = 1


class TIME_218:
    """静电震击 - Static Shock
    Deal $1 damage to a minion. Give your hero +1 Attack this turn.
    
    0费 自然法术
    对一个随从造成$1点伤害。使你的英雄在本回合中获得+1攻击力。
    
    非常便宜的自然法术，可以触发协同效果，并提供英雄攻击力。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 对随从造成1点伤害
        yield Hit(TARGET, 1)
        
        # 给英雄+1攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "TIME_218e")


class TIME_218e:
    """静电震击 - 英雄+1攻击"""
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    atk = 1


# RARE

class TIME_214:
    """时流亡魂 - Flux Revenant
    [x]Taunt Whenever you would damage this with a Nature spell, it gains +2/+1 instead.
    
    2费 1/4 元素
    嘲讽。每当你使用自然法术对本随从造成伤害时，改为使其获得+2/+1。
    
    自然法术协同的核心随从，可以通过友方自然法术快速成长。
    
    完整实现：
    - 使用 Predamage 事件在伤害应用前拦截
    - 检查伤害来源是否为友方自然法术
    - 如果是，将伤害设置为0并给予 +2/+1 buff
    """
    requirements = {}
    
    # 监听即将受到伤害的事件（PREDAMAGE）
    events = Predamage(SELF).on(
        lambda self, source, target, amount: (
            # 检查伤害来源是否为友方自然法术
            hasattr(source, 'spell_school') and
            source.spell_school == SpellSchool.NATURE and
            source.controller == self.controller and
            [
                # 将伤害设置为0（取消伤害）
                Predamage(target, 0),
                # 给予 +2/+1
                Buff(SELF, "TIME_214e")
            ]
        )
    )


class TIME_214e:
    """时流亡魂 - +2/+1"""
    atk = 2
    max_health = 1


class TIME_215:
    """雷霆动地 - Thunderquake
    [x]Deal $1 damage to all minions. Get a Static Shock.
    
    2费 自然法术
    对所有随从造成$1点伤害。获取一张静电震击。
    
    AOE清场并生成一张0费自然法术。
    """
    requirements = {}
    
    def play(self):
        # 对所有随从造成1点伤害
        yield Hit(ALL_MINIONS, 1)
        
        # 获取一张静电震击
        yield Give(self.controller, "TIME_218")


class TIME_216:
    """新生闪电 - Nascent Bolt
    Deal $5 damage to a minion. If it survives, draw 2 cards.
    
    3费 自然法术
    对一个随从造成$5点伤害。如果该随从存活，抽两张牌。
    
    高伤害单体法术，如果目标存活还能抽牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 对目标造成5点伤害
        yield Hit(TARGET, 5)
        
        # 检查目标是否存活
        # 需要在伤害结算后检查，所以使用 to_be_destroyed 和 zone
        if TARGET.to_be_destroyed == False and TARGET.zone == Zone.PLAY:
            # 抽两张牌
            yield Draw(self.controller)
            yield Draw(self.controller)


# EPIC

class TIME_014:
    """瞬时多重宇宙 - Instant Multiverse
    Rewind Summon 12 Mana worth of random minions. Overload: (3)
    
    6费 法术
    回溯。随机召唤消耗总计12点法力值的随从。过载：（3）
    
    回溯机制允许玩家对随机结果不满意时重新来过。
    
    完整实现：
    - 创建回溯点
    - 循环召唤随从直到达到12费或场上满7个
    - 过载3点
    """
    requirements = {}
    
    def play(self):
        
        # 随机召唤总计12费的随从
        remaining_mana = 12
        
        while remaining_mana > 0 and len(self.controller.field) < 7:
            # 随机选择一个费用不超过剩余法力值的随从
            # 限制最大费用为剩余法力值和10之间的较小值
            max_cost = min(remaining_mana, 10)
            
            # 如果剩余法力值为0，退出
            if max_cost <= 0:
                break
            
            # 随机召唤一个随从
            minions = yield Summon(
                self.controller,
                RandomCollectible(
                    card_type=CardType.MINION,
                    max_cost=max_cost,
                    min_cost=0
                )
            )
            
            # 减少剩余法力值
            if minions and len(minions) > 0:
                minion_cost = minions[0].cost
                remaining_mana -= minion_cost
            else:
                # 如果无法召唤，退出循环
                break
        
        # 过载3点
        yield Overload(self.controller, 3)


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_217:
    """雷鸫 - Stormrook
    [x]Whenever you would damage this with a Nature spell, summon a random 5-Cost minion instead.
    
    5费 5/5 野兽/元素
    每当你使用自然法术对本随从造成伤害时，改为召唤一个随机的法力值消耗为（5）点的随从。
    
    自然法术协同的强力随从，可以通过友方自然法术快速铺场。
    
    完整实现：
    - 使用 Predamage 事件在伤害应用前拦截
    - 检查伤害来源是否为友方自然法术
    - 如果是，将伤害设置为0并召唤5费随从
    """
    requirements = {}
    
    # 监听即将受到伤害的事件（PREDAMAGE）
    events = Predamage(SELF).on(
        lambda self, source, target, amount: (
            # 检查伤害来源是否为友方自然法术
            hasattr(source, 'spell_school') and
            source.spell_school == SpellSchool.NATURE and
            source.controller == self.controller and
            [
                # 将伤害设置为0（取消伤害）
                Predamage(target, 0),
                # 召唤一个随机5费随从
                Summon(CONTROLLER, RandomCollectible(card_type=CardType.MINION, cost=5))
            ]
        )
    )


# LEGENDARY

class TIME_013:
    """先知者沃 - Farseer Wo
    [x]Elusive After you cast a spell, Discover a Nature spell from the past.
    
    4费 2/6 传说随从
    扰魔。在你施放一个法术后，发现一张来自过去的自然法术牌。
    
    强力的法术生成引擎，每次施放法术都能发现自然法术。
    """
    requirements = {}
    
    # 添加 ELUSIVE 标签
    tags = {
        GameTag.ELUSIVE: True,
    }
    
    # 在施放法术后触发
    events = OWN_SPELL_PLAY.after(
        lambda self, player, card, *args: (
            Discover(
                self.controller,
                RandomCollectible(
                    card_type=CardType.SPELL,
                    spell_school=SpellSchool.NATURE
                )
            )
        )
    )


class TIME_209:
    """高山之王穆拉丁 - Muradin, High King
    [x]Fabled, Rush. Battlecry: Bring the High King's Hammer to ME! Deathrattle: Add it to your hand.
    
    5费 3/2 传说随从
    奇闻，突袭。战吼：将高山之王的战锤带到我这里！亡语：将其加入你的手牌。
    
    Fabled 机制：套牌中包含特殊的附带卡牌（高山之王的战锤）。
    战吼：从牌库中抽取高山之王的战锤。
    亡语：将高山之王的战锤加入手牌。
    
    完整实现：
    - 战吼：搜索牌库中的战锤并抽到手牌
    - 亡语：检查战锤的位置，将其加入手牌
      - 如果战锤在场上（装备中），将其加入手牌
      - 如果战锤在牌库中，将其抽到手牌
      - 如果战锤在墓地或其他位置，生成一张新的
    """
    requirements = {}
    
    # 添加 RUSH 标签
    tags = {
        GameTag.RUSH: True,
    }
    
    def play(self):
        # 战吼：从牌库中抽取高山之王的战锤
        # 搜索牌库中的 TIME_209t（高山之王的战锤）
        hammer = None
        for card in list(self.controller.deck):
            if card.id == "TIME_209t":
                hammer = card
                break
        
        if hammer:
            # 将战锤抽到手牌（使用 ForceDraw 确保抽到指定卡牌）
            yield ForceDraw(hammer)
    
    def deathrattle(self):
        # 亡语：将高山之王的战锤加入手牌
        # 需要检查战锤的当前位置
        
        # 1. 检查战锤是否装备在英雄上
        if self.controller.hero.weapon and self.controller.hero.weapon.id == "TIME_209t":
            # 将装备的战锤移到手牌
            hammer = self.controller.hero.weapon
            hammer.zone = Zone.HAND
            yield Give(self.controller, hammer)
            return
        
        # 2. 检查战锤是否在牌库中
        for card in list(self.controller.deck):
            if card.id == "TIME_209t":
                # 将战锤从牌库移到手牌
                yield ForceDraw(card)
                return
        
        # 3. 检查战锤是否在墓地
        for card in list(self.controller.graveyard):
            if card.id == "TIME_209t":
                # 将战锤从墓地移到手牌
                card.zone = Zone.HAND
                yield Give(self.controller, card)
                return
        
        # 4. 如果战锤不在任何位置（被消灭或变形等），生成一张新的
        yield Give(self.controller, "TIME_209t")


