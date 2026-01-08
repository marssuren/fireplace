"""
穿越时间流 - DEATH KNIGHT
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


# COMMON

class TIME_613:
    """时空冰封勇士 - Cryofrozen Champion
    1费 2/1 亡灵 - 冰霜符文x1
    **亡语：**获得一张随机**传说**随从。其法力值消耗减少（1）点。
    
    Deathrattle: Get a random Legendary minion. Reduce its Cost by (1).
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    deathrattle = [
        Give(CONTROLLER, RandomCollectible(type=CardType.MINION, rarity=Rarity.LEGENDARY)),
        Find(FRIENDLY_HAND + LAST_DRAWN) & Buff(FRIENDLY_HAND + LAST_DRAWN, "TIME_613e")
    ]


class TIME_613e:
    """时空冰封勇士减费 - Cryofrozen Champion Cost Reduction"""
    cost = -1


class TIME_611:
    """时间停滞 - Timestop
    2费 法术 - 冰霜学派 - 冰霜符文x2
    造成$3点伤害。**冻结**两个随机敌方随从。
    
    Deal $3 damage. Freeze two random enemy minions.
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 对目标造成3点伤害
        yield Hit(TARGET, 3)
        
        # 冻结两个随机敌方随从
        yield Freeze(RandomMinion(ENEMY_MINIONS))
        yield Freeze(RandomMinion(ENEMY_MINIONS))


class TIME_612:
    """赤红汲取 - Blood Draw
    3费 法术 - 暗影学派 - 鲜血符文x1
    **发现**一张法术。其消耗生命值而非法力值。
    
    Discover a spell. This costs Health instead of Mana.
    """
    requirements = {}
    
    def play(self):
        # 发现一张法术
        cards = yield DISCOVER(RandomCollectible(type=CardType.SPELL))
        
        # 给发现的法术添加"消耗生命值而非法力值"的buff
        # 发现的卡牌会被添加到手牌末尾
        if cards and self.controller.hand:
            # 找到刚发现的卡牌（手牌中最后一张）
            discovered_card = self.controller.hand[-1]
            yield Buff(discovered_card, "TIME_612e")


class TIME_612e:
    """赤红汲取效果 - Blood Draw Effect
    
    此卡牌消耗生命值而非法力值
    """
    # 标记此卡牌消耗生命值而非法力值
    # 核心引擎会在打出时检查此属性
    costs_health_instead_of_mana = True


# RARE

class TIME_610:
    """昨日之影 - Shadows of Yesterday
    6费 法术 - 暗影学派 - 亡灵符文x2
    **回溯**。召唤四个3/2暗影。它们每个分别获得两个随机**奖励效果**。

    Rewind. Summon four 3/2 Shades. They each gain two random Bonus Effects.
    """
    requirements = {}

    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 召唤四个3/2暗影
            for _ in range(4):
                minion = yield Summon(CONTROLLER, "TIME_610t")

                # 每个暗影获得两个随机奖励效果
                if minion:
                    # 随机选择2个不同的奖励效果
                    bonus_effects = self.game.random.sample([
                        "TIME_610e1",  # +2/+2
                        "TIME_610e2",  # 突袭
                        "TIME_610e3",  # 嘲讽
                        "TIME_610e4",  # 圣盾
                        "TIME_610e5",  # 吸血
                    ], 2)

                    for buff_id in bonus_effects:
                        yield Buff(minion[0], buff_id)

        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)


class TIME_614:
    """生命撕裂者 - Liferender
    3费 3/4 亡灵
    **战吼：**如果你的英雄在本回合中生命值发生了变化，对一个敌方随从造成6点伤害。
    
    Battlecry: If your hero's Health changed this turn, deal 6 damage to an enemy minion.
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        # 检查英雄生命值是否在本回合发生变化
        # 使用核心引擎已有的追踪机制：
        # - player.damage_taken_this_turn: 本回合英雄受到的伤害总量
        # - hero.healed_this_turn: 本回合英雄受到的治疗总量
        hero = self.controller.hero
        
        # 检查本回合是否有伤害或治疗
        health_changed = (
            self.controller.damage_taken_this_turn > 0 or  # 本回合受到过伤害
            hero.healed_this_turn > 0  # 本回合受到过治疗
        )
        
        if health_changed and self.target:
            yield Hit(TARGET, 6)


class TIME_616:
    """悼念成真 - Memoriam Manifest
    4费 法术 - 暗影学派
    召唤本局游戏中死亡的法力值消耗最高的友方亡灵。
    
    Summon the highest Cost friendly Undead that died this game.
    """
    requirements = {}
    
    def play(self):
        # 从墓地中找到费用最高的友方亡灵随从
        from hearthstone.enums import Race
        
        undead_graveyard = [
            card for card in self.controller.graveyard
            if card.type == CardType.MINION 
            and hasattr(card, 'races') 
            and Race.UNDEAD in card.races
        ]
        
        if undead_graveyard:
            # 找到费用最高的
            highest_cost_undead = max(undead_graveyard, key=lambda c: c.cost)
            
            # 召唤它
            yield Summon(CONTROLLER, highest_cost_undead.id)


# EPIC

class TIME_615:
    """遗忘纪元 - Forgotten Millennium
    8费 法术 - 鲜血符文x1 + 亡灵符文x1
    用随机亡灵填满你的手牌。在本回合中，这些卡牌消耗生命值而非法力值。
    
    Fill your hand with random Undead. They cost Health instead of Mana this turn.
    """
    requirements = {}
    
    def play(self):
        from hearthstone.enums import Race
        
        # 定义亡灵牌过滤器
        def is_undead(card):
            if card.type == CardType.MINION and hasattr(card, 'races'):
                return Race.UNDEAD in card.races
            return False
        
        # 计算需要填充的手牌数量
        cards_to_give = 10 - len(self.controller.hand)
        
        # 填满手牌
        for _ in range(cards_to_give):
            card = yield Give(CONTROLLER, RandomCollectible(card_filter=is_undead))
            
            # 给每张卡添加"本回合消耗生命值而非法力值"的buff
            if card:
                yield Buff(card[0], "TIME_615e")


class TIME_615e:
    """遗忘纪元效果 - Forgotten Millennium Effect
    
    本回合消耗生命值而非法力值
    """
    tags = {
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    
    # 标记此卡牌消耗生命值而非法力值
    costs_health_instead_of_mana = True


class TIME_617:
    """时空封冻者 - Chronochiller
    4费 8/7 亡灵 - 冰霜符文x1 + 亡灵符文x1
    你不再在你的回合开始时抽牌。
    
    You no longer draw a card at the start of your turn.
    """
    tags = {
        GameTag.TRIGGER_VISUAL: True,
        GameTag.AURA: True,  # 标记为光环效果
    }
    
    # 阻止回合开始抽牌的标记
    # 核心引擎在 game.py 的 _begin_turn 方法中会检查此属性
    # 如果场上有任何随从拥有此属性，则跳过回合开始抽牌
    blocks_turn_start_draw = True


# LEGENDARY

class TIME_618:
    """永时收割者哈斯克 - Husk, Eternal Reaper
    4费 5/3 亡灵
    **战吼：**使你的英雄获得"**亡语：**消耗至多20个**残骸**以该数值的生命值复活。"
    
    Battlecry: Give your hero "Deathrattle: Spend up to 20 Corpses to resurrect with that much Health."
    """
    def play(self):
        # 给英雄添加亡语buff
        yield Buff(FRIENDLY_HERO, "TIME_618e")


class TIME_618e:
    """永时收割者哈斯克效果 - Husk, Eternal Reaper Effect
    
    英雄亡语：消耗至多20个残骸以该数值的生命值复活
    
    实现方式：
    1. 消耗残骸
    2. 使用 SetCurrentHealth 将英雄生命值设置为残骸数量
    3. 这会将英雄从死亡状态救回（如果生命值 > 0，playstate 不会变为 LOSING）
    """
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    
    @property
    def deathrattle(self):
        """
        动态亡语：根据当前残骸数量决定复活生命值
        
        实现方式：
        1. 消耗残骸（最多20个）
        2. 使用 SetCurrentHealth 将英雄生命值设置为残骸数量
        3. 由于英雄生命值 > 0，playstate 不会被设置为 LOSING
        4. 游戏继续进行
        """
        # 计算可以消耗的残骸数量（最多20个）
        corpses_to_spend = min(self.owner.controller.corpses, 20)
        
        if corpses_to_spend > 0:
            return [
                # 消耗残骸
                SpendCorpses(CONTROLLER, corpses_to_spend),
                # 将英雄生命值设置为残骸数量
                # 这会将英雄从死亡状态救回（生命值从 <= 0 变为 > 0）
                SetCurrentHealth(FRIENDLY_HERO, corpses_to_spend),
            ]
        return []


class TIME_619:
    """墓地尊主塔兰吉 - Talanji of the Graves
    4费 4/5 亡灵
    **传奇套餐**。**战吼：**抽取Bwonsamdi*（如果他已经死亡则复活他）*。选择一个祝福给他。
    
    Fabled. Battlecry: Draw Bwonsamdi (or resurrect him if he has died). Choose a Boon to give him.
    """
    tags = {
        GameTag.FABLED: True,
    }
    
    def play(self):
        # 检查Bwonsamdi是否在牌库中
        bwonsamdi_in_deck = False
        for card in self.controller.deck:
            if card.id == "TIME_619t":  # Bwonsamdi的ID
                bwonsamdi_in_deck = True
                break
        
        # 检查Bwonsamdi是否已经死亡（在墓地中）
        bwonsamdi_in_graveyard = False
        for card in self.controller.graveyard:
            if card.id == "TIME_619t":
                bwonsamdi_in_graveyard = True
                break
        
        if bwonsamdi_in_deck:
            # 从牌库中抽取Bwonsamdi（使用 ForceDraw）
            drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + ID("TIME_619t"))
        elif bwonsamdi_in_graveyard:
            # 复活Bwonsamdi（召唤到场上）
            yield Summon(CONTROLLER, "TIME_619t")
        
        # 选择一个祝福给Bwonsamdi
        # 祝福选项：
        # 1. 长寿 (Longevity) - 吸血
        # 2. 力量 (Power) - 嘲讽
        # 3. 速度 (Speed) - 突袭
        # 同时使Bwonsamdi的亡语召唤的随从费用+2
        
        # 创建选项卡牌
        boon_options = [
            self.controller.card("TIME_619t2"),  # 长寿祝福
            self.controller.card("TIME_619t3"),  # 力量祝福
            self.controller.card("TIME_619t4"),  # 速度祝福
        ]
        
        # 使用 GenericChoice 让玩家选择祝福
        choice = yield GenericChoice(CONTROLLER, cards=boon_options)
        
        # 根据选择给Bwonsamdi添加对应的buff
        # 找到Bwonsamdi（可能在手牌或场上）
        bwonsamdi = None
        for card in self.controller.hand:
            if card.id == "TIME_619t":
                bwonsamdi = card
                break
        
        if not bwonsamdi:
            for minion in self.controller.field:
                if minion.id == "TIME_619t":
                    bwonsamdi = minion
                    break
        
        # 根据选择的卡牌ID添加对应的buff
        if bwonsamdi:
            # choice 返回的是选中的卡牌，我们需要根据其ID添加对应的buff
            # 选项卡牌的ID对应buff的ID（去掉最后的数字，加上'e'）
            for opt in boon_options:
                if opt.zone == Zone.HAND or opt.zone == Zone.PLAY:
                    # 这是被选中的卡牌
                    buff_id = opt.id + "e"  # TIME_619t2 -> TIME_619t2e
                    yield Buff(bwonsamdi, buff_id)
                    break


