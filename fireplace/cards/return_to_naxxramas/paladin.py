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
            # 根据官方机制：双类型随从只满足其中一个类型要求
            drawn_races = set()
            for card in list(self.controller.deck):  # 使用list避免迭代时修改
                if card.type == CardType.MINION:
                    # 获取该随从的所有种族
                    card_races = getattr(card, 'races', [])
                    if not card_races or Race.INVALID in card_races:
                        continue
                    
                    # 检查该随从是否有我们还未抽取的种族
                    # 双类型随从只满足其中一个类型（取第一个未抽取的）
                    for race in card_races:
                        if race != Race.INVALID and race not in drawn_races:
                            yield ForceDraw(card)
                            drawn_races.add(race)
                            break  # 该随从只满足一个类型要求



