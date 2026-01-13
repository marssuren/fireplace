from ..utils import *

class NX2_004:
    """洗劫 (Ransack)
    对一个随从造成$1点伤害。在本回合中，如果你使用过另一职业的卡牌，改为造成$4点。
    [迷你扩展包]
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 检查本回合是否使用过其他职业的卡牌
        used_other_class = False
        # cards_played_this_turn 是整数，应该使用 cards_played_this_turn_with_position
        for card_info in self.controller.cards_played_this_turn_with_position:
            card = card_info[0] if isinstance(card_info, tuple) else card_info
            # 检查卡牌是否为其他职业（非中立且非本职业）
            if hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL and card.card_class != self.controller.hero.card_class:
                used_other_class = True
                break
        
        # 根据条件造成不同伤害
        damage = 4 if used_other_class else 1
        yield Hit(TARGET, damage)



class NX2_005:
    """缝合造物 (Stitched Creation)
    连击：获得+2/+2。注能（{0}）：获得+3/+3。法力渴求（{1}）：获得+4/+4。
    机制: COMBO, INFUSE, MANATHIRST
    [迷你扩展包]
    """
    infuse = 3  # 注能阈值
    
    def play(self):
        # 连击：获得+2/+2
        if self.controller.combo:
            yield Buff(SELF, "NX2_005e1")
        
        # 注能（3）：获得+3/+3
        if self.infused:
            yield Buff(SELF, "NX2_005e2")
        
        # 法力渴求（7）：获得+4/+4
        if self.controller.max_mana >= 7:
            yield Buff(SELF, "NX2_005e3")



class NX2_005e1:
    """连击增益 (Combo Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
    }
    health = 2



class NX2_005e2:
    """注能增益 (Infused Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }
    health = 3



class NX2_005e3:
    """法力渴求增益 (Manathirst Buff)"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 4,
    }
    health = 4



class NX2_005e_combo:
    atk = 2
    health = 2


class NX2_005e_infuse:
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }
    health = 3
    

class NX2_005e_mana:
    atk = 4
    health = 4

class NX2_006:
    """旗标骷髅 (Jolly Roger)
    在你的英雄攻击后，召唤一个1/1的亡灵海盗。
    机制: TRIGGER_VISUAL
    [迷你扩展包]
    """
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "NX2_006t"))



class NX2_006t:
    """亡灵海盗 (Undead Pirate)
    1/1 亡灵海盗
    """
    # Token 卡牌
    pass



