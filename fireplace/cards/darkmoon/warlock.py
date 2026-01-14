"""
暗月马戏团 - 术士
"""
from ..utils import *


##
# Minions

class DMF_110:
    """吐火艺人 - Fire Breather
    战吼：对所有非恶魔随从造成2点伤害。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
    }
    play = Hit(ALL_MINIONS - DEMON, 2)



class DMF_111:
    """摇滚堕落者 - Wriggling Horror
    战吼：在本回合中，使一个友方恶魔获得+3攻击力和吸血。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 4,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON,
    }
    play = Buff(TARGET, "DMF_111e")


class DMF_111e:
    """本回合+3攻击力和吸血"""
    tags = {
        GameTag.ATK: 3,
        GameTag.LIFESTEAL: True,
    }
    events = OWN_TURN_END.on(Destroy(SELF))


class DMF_114:
    """癫狂的游客 - Midway Maniac
    嘲讽
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 5,
        GameTag.COST: 2,
        GameTag.TAUNT: True,
    }


class DMF_115:
    """怨灵捣蛋鬼 - Revenant Rascal
    战吼：摧毁每个玩家的一个法力水晶。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
    }
    play = (
        GainMana(CONTROLLER, -1),
        GainMana(OPPONENT, -1),
    )


class DMF_118:
    """提克特斯 - Tickatus
    战吼：移除你的牌库顶的五张牌。腐蚀：改为对手的牌库。
    """
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 6,
    }
    play = Mill(CONTROLLER) * 5
    corrupt = Mill(OPPONENT) * 5


class DMF_533:
    """火圈鬼母 - Ring Matron
    嘲讽，亡语：召唤两个3/2的小鬼。
    """
    tags = {
        GameTag.ATK: 6,
        GameTag.HEALTH: 4,
        GameTag.COST: 6,
        GameTag.TAUNT: True,
    }
    deathrattle = Summon(CONTROLLER, "DMF_533t") * 2


class DMF_533t:
    """小鬼"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
        GameTag.CARDRACE: Race.DEMON,
    }


##
# Spells

class DMF_113:
    """免票入场 - Free Admission
    抽两张随从牌。如果两张都是恶魔牌，使其法力值消耗减少（2）点。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 抽两张随从牌
        drawn_cards = []
        for _ in range(2):
            cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
            if cards:
                drawn_cards.extend(cards)
        
        # 检查是否两张都是恶魔
        if len(drawn_cards) == 2:
            if all(Race.DEMON in card.races for card in drawn_cards):
                # 两张都是恶魔，减少法力值消耗
                for card in drawn_cards:
                    yield Buff(card, "DMF_113e")


class DMF_113e:
    """减少法力值消耗（2）点"""
    tags = {
        GameTag.COST: -2,
    }


class DMF_117:
    """连环灾难 - Cascading Disaster
    随机消灭一个敌方随从。腐蚀：消灭两个。再次腐蚀：消灭三个。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = Destroy(RANDOM(ENEMY_MINIONS))
    corrupt = Destroy(RANDOM(ENEMY_MINIONS)) * 2
    
    # 再次腐蚀：消灭3个随机敌方随从
    # Second corruption: Destroy 3 random enemy minions
    corrupt2 = Destroy(RANDOM(ENEMY_MINIONS)) * 3
    


class DMF_119:
    """邪恶低语 - Wicked Whispers
    弃掉你手牌中法力值消耗最低的牌。使你的所有随从获得+1/+1。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 1,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    play = (
        Discard(LOWEST_COST(FRIENDLY_HAND)),
        Buff(FRIENDLY_MINIONS, "DMF_119e"),
    )


class DMF_119e:
    """+1/+1"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class DMF_534:
    """混乱套牌 - Deck of Chaos
    使你牌库中所有随从牌的法力值消耗和攻击力互换。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.SHADOW,
    }
    
    def play(self):
        """
        交换牌库中所有随从牌的法力值消耗和攻击力
        Swap the Cost and Attack of all minions in your deck
        """
        # 遍历牌库中的所有随从牌
        for card in self.controller.deck:
            if card.type == CardType.MINION:
                # 为每张随从牌添加一个 buff 来交换费用和攻击力
                yield Buff(card, "DMF_534e")


class DMF_534e:
    """混乱套牌效果 - 交换费用和攻击力"""
    
    def apply(self, target):
        """
        应用 buff 时，保存原始的费用和攻击力
        然后交换它们
        """
        # 保存原始值
        original_cost = target.cost
        original_atk = target.atk
        
        # 存储交换后的值
        self._swap_cost = original_atk
        self._swap_atk = original_cost
    
    # 重写 cost 属性，返回交换后的值（原攻击力）
    cost = lambda self, i: self._swap_cost
    
    # 重写 atk 属性，返回交换后的值（原费用）
    atk = lambda self, i: self._swap_atk
