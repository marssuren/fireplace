"""
决战荒芜之地 - WARLOCK
"""
from ..utils import *


# ========== TOKEN CARDS ==========

class WW_044t:
    """淤泥桶 - Barrel of Sludge
    造成$3点伤害。
    Deal $3 damage.
    """
    # Type: SPELL | Cost: 3 | Rarity: COMMON | School: FEL
    # Token卡牌，由多张术士卡牌生成
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    play = Hit(TARGET, 3)


# ========== COMMON CARDS ==========

class DEEP_031:
    """混乱化形 - Chaos Creation
    造成$6点伤害。随机召唤一个法力值消耗为（6）的随从。摧毁你牌库底的6张牌。
    Deal $6 damage. Summon a random 6-Cost minion. Destroy the bottom 6 cards of your deck.
    """
    # Type: SPELL | Cost: 6 | Rarity: COMMON | School: FEL
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    
    def play(self):
        # 造成6点伤害
        yield Hit(TARGET, 6)
        # 随机召唤一个6费随从
        yield Summon(CONTROLLER, RandomMinion(cost=6))
        # 摧毁牌库底的6张牌
        for _ in range(6):
            if self.controller.deck:
                yield Destroy(self.controller.deck[-1])


class WW_041:
    """排污助理 - Disposal Assistant
    战吼，亡语：将一桶淤泥置于你的牌库底部。
    Battlecry and Deathrattle: Put a Barrel of Sludge on the bottom of your deck.
    """
    # Type: MINION | Cost: 2 | Rarity: COMMON | Stats: 3/2
    # 战吼和亡语都是将淤泥桶放到牌库底部
    play = ShuffleIntoDeck(CONTROLLER, "WW_044t", position='bottom')
    deathrattle = ShuffleIntoDeck(CONTROLLER, "WW_044t", position='bottom')


class WW_042:
    """废物清理工 - Waste Remover
    在你的回合结束时，摧毁你牌库底的3张牌。
    At the end of your turn, destroy the bottom 3 cards of your deck.
    """
    # Type: MINION | Cost: 4 | Rarity: COMMON | Stats: 7/7
    # 在回合结束时摧毁牌库底的3张牌
    # 注意：这里不能使用lambda，因为需要在事件触发时动态获取牌库状态
    def events(self):
        # 定义一个内部函数来处理摧毁逻辑
        def destroy_bottom_three():
            """在回合结束时摧毁牌库底的3张牌"""
            for _ in range(min(3, len(self.controller.deck))):
                if self.controller.deck:
                    yield Destroy(self.controller.deck[-1])
        
        return OWN_TURN_END.on(destroy_bottom_three)



class WW_441:
    """锅炉燃料 / Furnace Fuel
    当本牌被使用、弃掉或摧毁时，抽两张牌。
    When this is played, discarded, or destroyed, draw 2 cards."""
    # Type: SPELL | Cost: 3 | Rarity: COMMON
    # 使用时抽牌
    def play(self):
        yield Draw(CONTROLLER) * 2
    
    # 被弃掉或从手牌摧毁时抽牌
    # 需要处理两种情况：弃掉(Discard)、手牌摧毁(Destroy)
    # 监听 Destroy 事件，检查卡牌是否在手牌区域
    events = [
        Discard(CONTROLLER, SELF).after(Draw(CONTROLLER) * 2),
        # 监听这张牌被摧毁，如果在手牌中则抽牌
        lambda self: Destroy(SELF).on(
            lambda *args: Draw(CONTROLLER) * 2 if self.zone == Zone.HAND else None
        )
    ]


# ========== RARE CARDS ==========

class DEEP_030:
    """源质晶簇 - Elementium Geode
    战吼，亡语：抽一张牌，并对你的英雄造成2点伤害。
    Battlecry and Deathrattle: Draw a card. Deal 2 damage to your hero.
    """
    # Type: MINION | Cost: 2 | Rarity: RARE | Stats: 2/1 | Race: ELEMENTAL
    # 战吼和亡语效果相同
    def play(self):
        yield Draw(CONTROLLER)
        yield Hit(FRIENDLY_HERO, 2)
    
    def deathrattle(self):
        yield Draw(CONTROLLER)
        yield Hit(FRIENDLY_HERO, 2)


class DEEP_032:
    """灵魂冻结 - Soulfreeze
    冻结一个随从及其相邻随从，对你的英雄造成等同于所冻结随从数量的伤害。
    Freeze a minion and its neighbors. Deal damage to your hero equal to the number Frozen.
    """
    # Type: SPELL | Cost: 1 | Rarity: RARE | School: FROST
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        # 收集目标：主目标及其相邻随从
        targets_to_freeze = [self.target]
        if self.target and hasattr(self.target, 'adjacent_minions'):
            targets_to_freeze.extend(self.target.adjacent_minions)
        
        # 冻结所有目标并计数
        for target in targets_to_freeze:
            if target and target.zone == Zone.PLAY:
                yield Freeze(target)
        
        # 计算实际冻结的数量（检查FROZEN标签）
        frozen_count = sum(1 for t in targets_to_freeze if t and t.zone == Zone.PLAY and t.frozen)
        
        # 对自己的英雄造成等同于冻结数量的伤害
        if frozen_count > 0:
            yield Hit(FRIENDLY_HERO, frozen_count)


class WW_043:
    """轮式淤泥怪 - Sludge on Wheels
    突袭。每当本随从受到伤害时，获取一桶淤泥并将一桶淤泥置于你的牌库底部。
    Rush. Whenever this takes damage, get a Barrel of Sludge and add one to the bottom of your deck.
    """
    # Type: MINION | Cost: 3 | Rarity: RARE | Stats: 2/5
    rush = True
    
    # 每当受到伤害时触发
    events = Damage(SELF).on(
        Give(CONTROLLER, "WW_044t"),  # 获取一桶淤泥到手牌
        ShuffleIntoDeck(CONTROLLER, "WW_044t", position='bottom')  # 将一桶淤泥放到牌库底
    )


class WW_092:
    """液力压裂 - Fracking
    查看你牌库底的3张牌。抽一张牌并摧毁其他牌。
    Look at the bottom 3 cards of your deck. Draw one and destroy the others.
    """
    # Type: SPELL | Cost: 1 | Rarity: RARE
    # 使用Choice让玩家从牌库底3张牌中选择一张抽取，摧毁其他
    def play(self):
        deck = self.controller.deck
        if not deck:
            return
        
        # 获取牌库底的最多3张牌
        num_cards = min(3, len(deck))
        bottom_cards = deck[-num_cards:]
        
        if len(bottom_cards) == 0:
            return
        
        # 保存牌库底的牌列表，用于后续摧毁
        cards_to_check = list(bottom_cards)
        
        # 让玩家从牌库底的牌中选择一张
        chosen = yield Choice(CONTROLLER, bottom_cards)
        
        if chosen:
            # 抽取选中的牌
            yield ForceDraw(chosen)
            
            # 摧毁其他牌
            for card in cards_to_check:
                if card != chosen and card.zone == Zone.DECK:
                    yield Destroy(card)



class WW_442:
    """钻拳莫尔葛 - Mo'arg Drillfist
    嘲讽。亡语：发掘一个宝藏。
    Taunt. Deathrattle: Excavate a treasure.
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 4/5
    taunt = True
    deathrattle = Excavate(CONTROLLER)


# ========== EPIC CARDS ==========

class WW_378:
    """列车烟囱 - Smokestack
    对一个随从造成$1点伤害。如果它死亡，发掘一个宝藏。
    Deal $1 damage to a minion. If it dies, Excavate a treasure.
    """
    # Type: SPELL | Cost: 1 | Rarity: EPIC
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        # 造成1点伤害
        yield Hit(TARGET, 1)
        
        # 检查目标是否死亡
        if self.target and self.target.dead:
            # 发掘一个宝藏
            yield Excavate(CONTROLLER)


class WW_436:
    """列车难题 - Trolley Problem
    弃掉你法力值消耗最低的法术牌。召唤两个3/3并具有突袭的电车。快枪：不弃牌。
    Discard your lowest Cost spell. Summon two 3/3 Tram Cars with Rush. Quickdraw: Don't discard.
    """
    # Type: SPELL | Cost: 3 | Rarity: EPIC | Mechanics: QUICKDRAW
    
    def play(self):
        # 快枪：本回合获得并立即使用时，跳过弃牌
        if not self.drawn_this_turn:
            # 普通：弃掉法力值消耗最低的法术牌
            spells = [c for c in self.controller.hand if c.type == CardType.SPELL and c != self]
            if spells:
                # 找到费用最低的法术
                lowest_cost_spell = min(spells, key=lambda c: c.cost)
                yield Discard(lowest_cost_spell)
        
        # 召唤两个3/3突袭电车
        yield Summon(CONTROLLER, "WW_436t") * 2


class WW_436t:
    """电车 - Tram Car"""
    # Type: MINION | Stats: 3/3 | Mechanics: RUSH
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.RUSH: True,
    }


# ========== LEGENDARY CARDS ==========

class WW_091:
    """腐臭淤泥波普加 - Pop'gar the Putrid
    你的邪能法术法力值消耗减少（2）点并具有吸血。战吼：获取两桶淤泥。
    Your Fel spells cost (2) less and have Lifesteal. Battlecry: Get two Barrels of Sludge.
    """
    # Type: MINION | Cost: 4 | Rarity: LEGENDARY | Stats: 2/6
    
    # 战吼：获取两桶淤泥
    play = Give(CONTROLLER, "WW_044t") * 2
    
    # 光环：邪能法术费用减少2点并具有吸血
    update = (
        # 减少邪能法术的费用
        Refresh(FRIENDLY_HAND + SPELL + SPELL_SCHOOL(SpellSchool.FEL), {
            GameTag.COST: -2
        }),
        # 给邪能法术添加吸血
        Refresh(FRIENDLY_HAND + SPELL + SPELL_SCHOOL(SpellSchool.FEL), {
            GameTag.LIFESTEAL: True
        })
    )


class WW_437:
    """列车司机杰里 - Tram Conductor Gerry
    战吼：如果你已经发掘过两次，召唤六个3/3并具有突袭的电车。
    Battlecry: If you've Excavated twice, summon six 3/3 Tram Cars with Rush.
    """
    # Type: MINION | Cost: 7 | Rarity: LEGENDARY | Stats: 4/4
    
    def play(self):
        # 检查是否已经发掘过至少2次
        # 使用Player类中定义的times_excavated属性（player.py第34行）
        if self.controller.times_excavated >= 2:
            # 召唤6个3/3突袭电车
            yield Summon(CONTROLLER, "WW_436t") * 6


