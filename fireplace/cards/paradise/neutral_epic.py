"""
胜地历险记 - 中立 - EPIC
"""
from ..utils import *


class VAC_439:
    """海滨巨人 - Seaside Giant
    在本局对战中，你每使用过一次地标效果，本牌的法力值消耗便减少（1）点。
    Costs (1) less for each time you've used a location this game.
    """
    # 9费 8/8
    class Hand:
        def cost(self, i):
            # 每使用一次地标，减少1费
            return i - self.controller.locations_used_this_game


class VAC_447:
    """恐惧的逃亡者 - Dread Deserter
    如果本随从不在你的套牌中，则拥有冲锋。
    Has Charge if this didn't start in your deck.
    """
    # 6费 6/6 海盗
    race = Race.PIRATE
    
    @property
    def charge(self):
        # 检查卡牌是否在起始套牌中
        # 如果不在起始套牌中（生成的卡、发现的卡等），则拥有冲锋
        if hasattr(self.controller, 'starting_deck'):
            # 检查起始套牌中是否有这张卡
            for card in self.controller.starting_deck:
                if card.id == self.id:
                    return False  # 在起始套牌中，没有冲锋
        # 不在起始套牌中，拥有冲锋
        return True


class VAC_523:
    """混调师 - Mixologist
    战吼：制造一张法力值消耗为（1）的自定义药水牌。
    Battlecry: Craft a custom 1-Cost Potion.
    
    官方效果：玩家可以从9个效果中选择2个，组合成一个1费药水
    效果选项：
    1. 召唤一个2/2的恶魔
    2. 召唤一个本局对战中死亡的友方随从
    3. 使你的随从获得+2生命值
    4. 冻结一个随机的敌方随从
    5. 造成3点伤害
    6. 对所有随从造成2点伤害
    7. 获得4点护甲
    8. 抽一张牌
    9. 将一张随机恶魔牌置入你的手牌
    """
    # 3费 2/3
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 类似 Kazakus 的自定义药水机制
        # 生成 Mixologist's Special Token，让玩家选择两个效果
        yield Give(CONTROLLER, "VAC_523t")


class VAC_935:
    """随行肉虫 - Carry-On Grub
    战吼：获取一张法力值消耗为（1）的手提箱，将你牌库顶的2张牌装入其中。
    Battlecry: Get a 1-Cost Suitcase. Pack the top 2 cards of your deck into it.
    """
    # 4费 5/4 野兽
    mechanics = [GameTag.BATTLECRY]
    race = Race.BEAST
    
    def play(self):
        # 创建手提箱Token
        suitcase = self.controller.card("VAC_935t", source=self)
        suitcase.packed_cards = []
        
        # 将牌库顶的2张牌装入手提箱（如果有的话）
        cards_to_pack = min(2, len(self.controller.deck))
        for _ in range(cards_to_pack):
            if self.controller.deck:
                card = self.controller.deck[-1]
                suitcase.packed_cards.append(card.id)
                card.zone = Zone.SETASIDE
        
        # 将手提箱加入手牌
        yield Give(CONTROLLER, suitcase)


class VAC_958:
    """进化融合怪 - Adaptive Amalgam
    本随从拥有全部随从类型。亡语：将本随从洗入你的牌库。保留所有附加效果。
    This has all minion types. Deathrattle: Shuffle this into your deck. It keeps any enchantments.
    """
    # 1费 1/2 全种族
    mechanics = [GameTag.DEATHRATTLE]
    race = Race.ALL
    
    def deathrattle(self):
        # 创建一个新的复制，保留所有 buffs
        new_card = self.controller.card(self.id, source=self)
        
        # 复制所有附加效果（buffs/enchantments）
        for buff in self.buffs:
            # 复制 buff 到新卡
            new_buff = self.controller.card(buff.id, source=buff.source)
            
            # 复制所有 buff 的属性
            # 包括：atk, max_health, taunt, divine_shield, windfury 等
            for attr in ['atk', 'max_health', 'taunt', 'divine_shield', 'windfury', 
                        'charge', 'stealth', 'poisonous', 'lifesteal', 'rush']:
                if hasattr(buff, attr):
                    setattr(new_buff, attr, getattr(buff, attr))
            
            # 应用 buff 到新卡
            new_buff.apply(new_card)
        
        # 将新卡洗入牌库
        new_card.zone = Zone.DECK
        yield Shuffle(CONTROLLER, new_card)


class WORK_042:
    """食肉格块 - Carnivorous Cubicle
    战吼：消灭一个友方随从。在你的回合结束时，召唤一个它的复制。
    Battlecry: Destroy a friendly minion. Summon a copy of it at the end of your turns.
    """
    # 5费 4/6
    mechanics = [GameTag.BATTLECRY]
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        if TARGET:
            # 记录被消灭的随从ID
            minion_id = TARGET.id
            
            # 消灭目标
            yield Destroy(TARGET)
            
            # 给自己添加一个buff，存储随从ID
            # 使用 kwargs 传递自定义属性
            yield Buff(SELF, "WORK_042e", stored_minion_id=minion_id)
    
    # 回合结束时召唤复制
    events = OWN_TURN_END.on(
        lambda self: Summon(CONTROLLER, self.buffs[0].stored_minion_id) if self.buffs and hasattr(self.buffs[0], 'stored_minion_id') else []
    )


class WORK_042e:
    """食肉格块存储效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # stored_minion_id 将在运行时通过 kwargs 设置
