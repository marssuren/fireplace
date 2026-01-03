from ..utils import *

class NX2_021:
    """亡者骑士 (Knight of the Dead)
    战吼：对你的英雄造成5点伤害。法力渴求（7）：改为为你的英雄恢复5点生命值。
    机制: BATTLECRY, MANATHIRST
    [迷你扩展包]
    """
    def play(self):
        # 法力渴求（7）：恢复生命值
        if self.controller.max_mana >= 7:
            yield Heal(FRIENDLY_HERO, 5)
        else:
            # 否则造成伤害
            yield Hit(FRIENDLY_HERO, 5)



class NX2_022:
    """金翼巨龙 (Goldwing)
    突袭。战吼：如果你的手牌中有机械牌，便获得风怒。
    机制: BATTLECRY, RUSH
    [迷你扩展包]
    """
    tags = {GameTag.RUSH: True}
    
    def play(self):
        # 检查手牌中是否有机械牌
        if self.controller.hand.filter(race=Race.MECHANICAL):
            # 获得风怒
            yield Buff(SELF, "NX2_022e")



class NX2_022e:
    """金翼巨龙增益 (Goldwing Buff)"""
    tags = {GameTag.WINDFURY: True}



class NX2_023:
    """纯净馆长 (The Purator)
    嘲讽。战吼：如果你的牌库中没有中立卡牌，抽取每个随从类型的随从牌各一张。
    机制: BATTLECRY, TAUNT
    [迷你扩展包]
    """
    tags = {GameTag.TAUNT: True}
    
    def play(self):
        # 检查牌库中是否有中立卡牌
        has_neutral = any(card.card_class == CardClass.NEUTRAL for card in self.controller.deck)
        
        if not has_neutral:
            # 抽取每个随从类型（种族）的随从牌各一张
            # 统计牌库中所有不同的种族
            drawn_races = set()
            for card in list(self.controller.deck):  # 使用list避免迭代时修改
                if card.type == CardType.MINION and card.race != Race.INVALID and card.race not in drawn_races:
                    yield ForceDraw(card)
                    drawn_races.add(card.race)
                    # 炉石传说中有14个种族，但牌库中不一定都有
                    if len(drawn_races) >= 14:  # 所有可能的种族
                        break



