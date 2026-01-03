from ..utils import *

class NX2_001:
    """撕裂现实 (Tear Reality)
    随机将2张来自过去的法师法术牌置入你的手牌，其法力值消耗减少（2）点。
    [迷你扩展包]
    """
    def play(self):
        # 从狂野法师法术中随机选择2张
        for i in range(2):
            card = yield RandomSpell(card_class=CardClass.MAGE)
            if card:
                # 置入手牌并减少2费
                yield Give(CONTROLLER, card)
                yield Buff(card, "NX2_001e")



class NX2_001e:
    """撕裂现实增益 (Tear Reality Buff)"""
    tags = {GameTag.COST: -2}



class NX2_002:
    """鬼灵学徒 (Spectral Trainee)
    在你施放一个法术后，对所有敌方随从造成1点伤害。
    机制: TRIGGER_VISUAL
    [迷你扩展包]
    """
    events = OWN_SPELL_PLAY.after(Hit(ENEMY_MINIONS, 1))



class NX2_003:
    """织漩者 (Whirlweaver)
    战吼：如果你在上回合施放过法术，发现一张元素牌。
    机制: BATTLECRY, DISCOVER
    [迷你扩展包]
    """
    def play(self):
        # 检查上回合是否施放过法术
        last_turn = self.game.turn - 1
        cast_spell_last_turn = any(
            card.type == CardType.SPELL and card.turn_played == last_turn
            for card in self.controller.cards_played_this_game
        )

        if cast_spell_last_turn:
            # 发现一张元素牌
            yield GenericChoice(CONTROLLER, RandomMinion(race=Race.ELEMENTAL) * 3)



