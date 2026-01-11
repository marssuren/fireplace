from ..utils import *


##
# Minions

class DMF_081:
    """K'thir Ritualist (克熙尔祭师)
    Taunt Battlecry: Add a random 4-Cost minion to your opponent's hand."""
    # 3费 2/3 嘲讽 - 战吼：将一张随机4费随从牌置入对手的手牌
    play = Give(OPPONENT, RandomCollectible(card_class=CardClass.NEUTRAL, type=CardType.MINION, cost=4))


class DMF_125:
    """Safety Inspector (安全检查员)
    Battlecry: Shuffle the lowest-Cost card from your hand into your deck. Draw a card."""
    # 1费 1/3 - 战吼：将你手牌中法力值消耗最低的卡牌洗入你的牌库。抽一张牌
    play = (Shuffle(CONTROLLER, LOWEST_COST(FRIENDLY_HAND)), Draw(CONTROLLER))


class DMF_202:
    """Derailed Coaster (脱轨过山车)
    Battlecry: Summon a 1/1 Rider with Rush for each minion in your hand."""
    # 5费 3/2 - 战吼：你的手牌中每有一张随从牌，便召唤一个1/1并具有突袭的游客
    play = Summon(CONTROLLER, "DMF_202t") * Count(FRIENDLY_HAND + MINION)


class DMF_202t:
    """Rider (游客)"""
    # 1/1 突袭 - Token随从
    pass


class YOP_003:
    """Luckysoul Hoarder (幸运之魂囤积者)
    Battlecry: Shuffle 2 Soul Fragments into your deck. Corrupt: Draw a card."""
    # 3费 3/3 - 战吼：将2个灵魂碎片洗入你的牌库。腐蚀：抽一张牌
    play = Shuffle(CONTROLLER, "SCH_307t") * 2
    corrupt = Draw(CONTROLLER)


class YOP_032:
    """Armor Vendor (护甲商贩)
    Battlecry: Give 4 Armor to each hero."""
    # 1费 1/3 - 战吼：使双方英雄获得4点护甲值
    play = GainArmor(ALL_HEROES, 4)


class YOP_034:
    """Runaway Blackwing (窜逃的黑翼龙)
    At the end of your turn, deal 10 damage to a random enemy minion."""
    # 10费 9/4 - 在你的回合结束时，对一个随机敌方随从造成10点伤害
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_MINION, 10))


##
# Spells

class YOP_006:
    """Hysteria (狂乱)
    Choose an enemy minion. It attacks random minions until it dies."""
    # 4费法术 - 选择一个敌方随从。使其攻击随机随从，直到它死亡
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 使目标随从持续攻击随机随从直到它死亡
        # 这需要一个循环逻辑，在fireplace中通过自定义Action实现
        yield HysteriaAttack(TARGET)


class HysteriaAttack(TargetedAction):
    """Hysteria attack loop - 狂乱攻击循环"""
    TARGET = ActionArg()
    
    def do(self, source, target):
        # 当目标还活着时,持续攻击
        while not target.dead and target.zone == Zone.PLAY:
            # 获取所有可攻击的随从(除了自己)
            valid_targets = [
                x for x in target.controller.game.board 
                if x != target and x.type == CardType.MINION and not x.dead
            ]
            
            if not valid_targets:
                break
            
            # 随机选择一个目标攻击
            attack_target = source.game.random.choice(valid_targets)
            
            # 执行攻击
            source.game.queue_actions(target, [Attack(attack_target)])
            source.game.process_deaths()
            
            # 如果攻击者死了，停止循环
            if target.dead or target.zone != Zone.PLAY:
                break


class YOP_009:
    """Rally! (开赛集结)
    Resurrect a friendly 1-Cost, 2-Cost, and 3-Cost minion."""
    # 4费法术 - 复活一个友方的1费、2费和3费随从
    def play(self):
        # 复活机制：从墓地召唤符合条件的随从
        actions = []
        
        # 复活1费随从
        dead_1_cost = [m for m in self.controller.graveyard 
                      if m.type == CardType.MINION and m.cost == 1]
        if dead_1_cost:
            minion = self.game.random.choice(dead_1_cost)
            actions.append(Summon(CONTROLLER, minion.id))
        
        # 复活2费随从
        dead_2_cost = [m for m in self.controller.graveyard 
                      if m.type == CardType.MINION and m.cost == 2]
        if dead_2_cost:
            minion = self.game.random.choice(dead_2_cost)
            actions.append(Summon(CONTROLLER, minion.id))
        
        # 复活3费随从
        dead_3_cost = [m for m in self.controller.graveyard 
                      if m.type == CardType.MINION and m.cost == 3]
        if dead_3_cost:
            minion = self.game.random.choice(dead_3_cost)
            actions.append(Summon(CONTROLLER, minion.id))
        
        return actions


class YOP_024:
    """Guidance (灵魂指引)
    Look at two spells. Add one to your hand or Overload: (1) to get both."""
    # 1费法术 - 检视两张法术牌。将其中一张置入你的手牌，或者过载：(1)以获取两张
    
    # 使用 Choose One 机制：定义两个选项
    choose = ("YOP_024a", "YOP_024b")
    
    def play(self):
        # 生成两张随机法术牌
        # 使用 RandomSpell() 选择器
        spell1 = self.controller.card(RandomSpell().evaluate(self), source=self)
        spell2 = self.controller.card(RandomSpell().evaluate(self), source=self)
        
        # 将法术存储到卡牌上，供选项使用
        self.stored_spells = [spell1, spell2]
        return []


class YOP_024a:
    """Choose One (选择一张)"""
    # 选项1：选择其中一张法术加入手牌
    
    def play(self):
        # 从父卡牌获取存储的法术
        parent = self.creator
        if hasattr(parent, 'stored_spells') and parent.stored_spells:
            # 让玩家选择一张法术
            choice = yield GenericChoice(self.controller, cards=parent.stored_spells)


class YOP_024b:
    """Overload for Both (过载获取全部)"""
    # 选项2：过载(1)，两张法术都加入手牌
    
    def play(self):
        # 从父卡牌获取存储的法术
        parent = self.creator
        if hasattr(parent, 'stored_spells'):
            spells = parent.stored_spells
            # 过载(1)并给予两张法术
            return (Overload(CONTROLLER, 1), Give(CONTROLLER, spells))
        return []
