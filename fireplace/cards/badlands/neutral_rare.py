"""
决战荒芜之地 - 中立 - RARE
"""
from ..utils import *


class DEEP_034:
    """页岩蛛 - Shale Spider
    战吼：如果你在上个回合使用过元素牌，抽一张牌。
    Battlecry: If you played an Elemental last turn, draw a card.
    """
    # Type: MINION | Cost: 2 | Rarity: RARE | Stats: 3/2
    # 战吼：如果上回合使用过元素牌，抽一张牌
    def play(self):
        if self.controller.elemental_played_last_turn > 0:
            yield Draw(CONTROLLER)


class WW_002:
    """破地钻机 - Burrow Buster
    突袭。战吼：发掘一个宝藏。
    Rush. Battlecry: Excavate a treasure.
    """
    # Type: MINION | Cost: 5 | Rarity: RARE | Stats: 6/5
    # 突袭，战吼：发掘一个宝藏
    rush = True
    play = Excavate(CONTROLLER)


class WW_003:
    """悬赏公告栏 / Bounty Board
    你的发掘，快枪，可交易和传说牌的法力值消耗减少（1）点。
    Your Excavate, Quickdraw, Tradeable, and Legendary cards cost (1) less."""
    # Type: MINION | Cost: 3 | Rarity: RARE | Stats: 0/5
    # 光环：发掘、快枪、可交易和传说牌费用-1
    
    # 使用 update 属性实现光环效果
    update = Refresh(
        FRIENDLY_HAND + (
            # 发掘牌（拥有 EXCAVATE 标签）
            FuncSelector(lambda entities, src: [e for e in entities if getattr(e, 'excavate', False)]) |
            # 快枪牌（拥有 QUICKDRAW 标签）
            FuncSelector(lambda entities, src: [e for e in entities if e.tags.get(GameTag.QUICKDRAW, False)]) |
            # 可交易牌（拥有 TRADEABLE 标签）
            FuncSelector(lambda entities, src: [e for e in entities if e.tags.get(GameTag.TRADEABLE, False)]) |
            # 传说牌（稀有度为 LEGENDARY）
            LEGENDARY
        ),
        {GameTag.COST: -1}
    )


class WW_332:
    """蛇油商人 - Snake Oil Seller
    亡语：将2张可交易的蛇油洗入你的对手的牌库。
    Deathrattle: Shuffle 2 Tradeable Snake Oils into your opponent's deck.
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 4/5
    # 亡语：将2张可交易的蛇油洗入对手牌库
    deathrattle = Shuffle(OPPONENT, "WW_331t") * 2


class WW_360:
    """艾泽里特苦囚 - Azerite Chain Gang
    嘲讽。战吼和快枪：召唤一个本随从的复制。
    Taunt. Battlecry and Quickdraw: Summon a copy of this minion.
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 2/3
    # 嘲讽，战吼+快枪：召唤复制
    taunt = True
    
    def play(self):
        # 战吼：召唤一个复制
        yield Summon(CONTROLLER, ExactCopy(SELF))
        
        # 快枪：本回合获得并立即使用时，额外召唤一个复制
        if self.drawn_this_turn:
            yield Summon(CONTROLLER, ExactCopy(SELF))


class WW_419:
    """食人魔帮骑手 - Ogre-Gang Rider
    突袭。50%概率使你的英雄在本回合中获得+3攻击力，而不是攻击。
    Rush. 50% chance to give your hero +3 Attack this turn instead of attacking.
    """
    # Type: MINION | Cost: 4 | Rarity: RARE | Stats: 3/6
    # 突袭，50%概率给英雄+3攻击而不是攻击
    rush = True
    
    # 使用事件系统：在攻击前50%概率改为给英雄+3攻击
    events = Attack(SELF).on(
        COINFLIP & (
            Buff(FRIENDLY_HERO, "WW_419e"),  # 给英雄+3攻击（本回合）
            Retarget(SELF, None)  # 取消攻击
        )
    )



class WW_419e:
    """+3攻击（本回合）"""
    tags = {
        GameTag.ATK: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    # 回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


