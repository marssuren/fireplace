"""
威兹班的工坊 - ROGUE
"""
from ..utils import *


# COMMON

class TOY_505:
    """玩具船 - Toy Boat
    After you summon a Pirate, draw a card.
    在你召唤一个海盗后,抽一张牌。
    """
    # 2费 2/3 随从
    # 效果：召唤海盗后抽牌
    
    events = Summon(CONTROLLER, PIRATE).after(Draw(CONTROLLER))


class TOY_514:
    """菊花茶具 - Thistle Tea Set
    <b>Discover</b> a spell from another class. Get a copy of it.
    <b>发现</b>一张另一职业的法术牌，并获取一张它的复制。
    """
    # 2费法术
    # 效果：发现其他职业法术，获取复制
    
    def play(self):
        # 发现一张其他职业的法术牌
        # 排除盗贼和中立职业
        cards = yield DISCOVER(RandomCollectible(
            type=CardType.SPELL,
            card_class=~(CardClass.ROGUE | CardClass.NEUTRAL)
        ))
        
        if cards:
            # 获取发现的牌的复制
            yield Give(CONTROLLER, cards[0].id)


class TOY_516:
    """折价区海盗 - Bargain Bin Buccaneer
    <b>Rush</b>. <b>Combo:</b> Summon a copy of this.
    <b>突袭</b>。<b>连击：</b>召唤一个本随从的复制。
    """
    # 3费 3/2 海盗 突袭
    # 连击：召唤复制
    rush = True
    
    def play(self):
        if self.controller.cards_played_this_turn > 0:
            # 连击触发：召唤本随从的复制
            yield Summon(CONTROLLER, ExactCopy(SELF))


class MIS_903:
    """可疑交易 - Dubious Purchase
    Draw 3 cards. <b>Combo:</b> Destroy a random enemy minion.
    抽三张牌。<b>连击：</b>随机消灭一个敌方随从。
    """
    # 4费法术
    # 效果：抽3张牌，连击消灭随机敌方随从
    
    def play(self):
        # 抽3张牌
        yield Draw(CONTROLLER)
        yield Draw(CONTROLLER)
        yield Draw(CONTROLLER)
        
        # 连击：消灭随机敌方随从
        if self.controller.cards_played_this_turn > 0:
            enemy_minions = ENEMY_MINIONS.eval(self.game, self)
            if enemy_minions:
                target = self.game.random.choice(enemy_minions)
                yield Destroy(target)


# RARE

class MIS_708:
    """幻变的卡牌包 - Twisted Pack
    Add 5 random cards from other classes to your hand. They are <b>Temporary</b>.
    随机将五张其他职业的牌置入你的手牌。这些牌为<b>临时</b>牌。
    """
    # 1费法术
    # 效果：获取5张其他职业的随机牌，标记为临时牌
    
    def play(self):
        # 获取5张其他职业的随机牌
        for _ in range(5):
            # 随机获取非盗贼非中立的牌
            card = yield Give(CONTROLLER, RandomCollectible(
                card_class=~(CardClass.ROGUE | CardClass.NEUTRAL)
            ))
            
            if card:
                # 标记为临时牌（回合结束时弃掉）
                yield Buff(card[0], "MIS_708e")


class TOY_510:
    """挖掘宝藏 - Dig for Treasure
    Draw a minion. If it's a Pirate, get a Coin.
    抽一张随从牌。如果是海盗牌，获取一张幸运币。
    """
    # 1费法术
    # 效果：抽随从牌，如果是海盗则获取幸运币
    
    def play(self):
        # 抽一张随从牌
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
        
        if drawn:
            card = drawn[0]
            # 检查是否是海盗
            if hasattr(card, 'race') and card.race == Race.PIRATE:
                # 获取幸运币
                yield Give(CONTROLLER, "GAME_005")
            elif hasattr(card, 'races') and Race.PIRATE in card.races:
                # 检查多种族情况
                yield Give(CONTROLLER, "GAME_005")


class MIS_706:
    """滚灰兔 - Dust Bunny
    <b>Battlecry</b> and <b>Deathrattle:</b> Add a random piece of junk to your hand <i>(a Coin, Rock, Banana, or Knife)</i>.
    <b>战吼，亡语：</b>将一件垃圾置入你的手牌<i>（幸运币，石头，香蕉或短刀）</i>。
    """
    # 3费 3/2 野兽
    # 战吼和亡语：获取随机垃圾
    
    # 垃圾卡牌列表
    JUNK_CARDS = [
        "GAME_005",  # 幸运币 (The Coin)
        "MIS_706t1", # 石头 (Rock)
        "EX1_014t",  # 香蕉 (Banana)
        "MIS_706t2", # 短刀 (Knife)
    ]
    
    def play(self):
        # 战吼：获取随机垃圾
        junk = self.game.random.choice(self.JUNK_CARDS)
        yield Give(CONTROLLER, junk)
    
    def deathrattle(self):
        # 亡语：获取随机垃圾
        junk = self.game.random.choice(self.JUNK_CARDS)
        yield Give(CONTROLLER, junk)


class TOY_512:
    """水晶海湾 - The Crystal Cove
    The next minion you summon this turn has its stats set to 4/4.
    在本回合中，你召唤的下一个随从的属性值变为4/4。
    """
    # 3费地标 3耐久
    # 效果：下一个召唤的随从变为4/4
    
    def activate(self):
        # 给控制者添加一个临时效果
        # 使用 Buff 标记下一个召唤的随从
        yield Buff(CONTROLLER, "TOY_512e")


class TOY_521:
    """沙箱恶霸 - Sandbox Scoundrel
    <b>Miniaturize</b>
    <b>Battlecry:</b> Your next card this turn costs (2) less.
    <b>微缩</b>
    <b>战吼：</b>在本回合中，你的下一张牌法力值消耗减少（2）点。
    """
    # 5费 4/3 海盗 微缩
    # 战吼：下一张牌费用减少2
    
    def play(self):
        # 给控制者添加临时效果：下一张牌费用减少2
        yield Buff(CONTROLLER, "TOY_521e")


# EPIC

class TOY_522:
    """水弹枪 - Watercannon
    After your hero attacks, summon a 1/1 Pirate that attacks a random enemy.
    在你的英雄攻击后，召唤一个1/1的海盗，并使其随机攻击一个敌人。
    """
    # 4费武器 3/3
    # 官方数据：3 Attack, 3 Durability
    # 效果：英雄攻击后召唤1/1海盗并攻击随机敌人
    
    events = Attack(FRIENDLY_HERO).after(
        lambda self, card: self._summon_and_attack()
    )
    
    def _summon_and_attack(self):
        """召唤海盗并让其攻击随机敌人"""
        # 召唤1/1海盗
        pirate = yield Summon(CONTROLLER, "TOY_522t")
        
        if pirate:
            pirate_minion = pirate[0]
            
            # 获取所有可攻击的敌人（随从+英雄）
            enemies = list(self.controller.opponent.field) + [self.controller.opponent.hero]
            valid_enemies = [e for e in enemies if e.can_be_attacked_by(pirate_minion)]
            
            if valid_enemies:
                target = self.game.random.choice(valid_enemies)
                yield Attack(pirate_minion, target)


class TOY_519:
    """一件不留 - Everything Must Go!
    Summon two random 4-Cost minions. Costs (1) less for each card you've drawn this turn.
    随机召唤两个法力值消耗为（4）的随从。在本回合中你每抽过一张牌，本牌的法力值消耗便减少（1）点。
    """
    # 9费法术
    # 效果：召唤两个随机4费随从，本回合每抽一张牌费用减少1
    
    cost_mod = lambda self, i: -self.controller.cards_drawn_this_turn
    
    def play(self):
        # 召唤两个随机4费随从
        for _ in range(2):
            minion_id = yield RandomCollectible(type=CardType.MINION, cost=4)
            if minion_id:
                yield Summon(CONTROLLER, minion_id)


# LEGENDARY

class TOY_515:
    """水上舞者索尼娅 - Sonya Waterdancer
    After you play a 1-Cost minion, get a copy of it that costs (0).
    在你使用一张法力值消耗为（1）的随从牌后，获取一张它的法力值消耗为（0）点的复制。
    """
    # 4费 3/3 传说随从
    # 效果：打出1费随从后，获取0费复制
    
    events = Play(CONTROLLER, MINION + (COST(Play.CARD) == 1)).after(
        lambda self, player, played_card, target=None: self._give_copy(played_card)
    )
    
    def _give_copy(self, minion):
        """给予随从的0费复制"""
        # 获取复制
        copy = yield Give(CONTROLLER, ExactCopy(minion))
        
        if copy:
            # 设置费用为0
            yield Buff(copy[0], "TOY_515e")


class TOY_511:
    """大盗金胡子 - Shoplifter Goldbeard
    After you summon a Pirate, summon a copy of it that attacks a random enemy, then dies.
    在你召唤一个海盗后，召唤一个它的复制并使其攻击随机敌人然后死亡。
    """
    # 5费 5/5 海盗 传说随从
    # 效果：召唤海盗后，召唤复制并攻击随机敌人然后死亡
    
    events = Summon(CONTROLLER, PIRATE).after(
        lambda self, player, played_card, target=None: self._summon_and_attack(played_card)
    )
    
    def _summon_and_attack(self, pirate):
        """召唤海盗复制并攻击随机敌人然后死亡"""
        # 召唤复制
        copy = yield Summon(CONTROLLER, ExactCopy(pirate))
        
        if copy:
            pirate_copy = copy[0]
            
            # 获取所有可攻击的敌人
            enemies = list(self.controller.opponent.field) + [self.controller.opponent.hero]
            valid_enemies = [e for e in enemies if e.can_be_attacked_by(pirate_copy)]
            
            if valid_enemies:
                target = self.game.random.choice(valid_enemies)
                # 攻击随机敌人
                yield Attack(pirate_copy, target)
            
            # 然后死亡
            yield Destroy(pirate_copy)


# ========================================
# Buff 定义
# ========================================

class MIS_708e:
    """临时牌标记 - Temporary Card Buff
    Temporary. Discarded at end of turn.
    """
    # 临时牌标记
    # 回合结束时弃掉
    tags = {GameTag.GHOSTLY: True}


class TOY_512e:
    """水晶海湾增益 - Crystal Cove Buff
    Next minion summoned has 4/4 stats
    """
    # 控制者 Buff：下一个召唤的随从变为4/4
    # 参考 TOY_813 的实现，使用 Buff 设置属性
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True  # 本回合结束时移除
    }
    
    events = Summon(CONTROLLER, MINION).after(
        lambda self, player, played_card, target=None: self._set_stats(played_card)
    )
    
    def _set_stats(self, minion):
        """将召唤的随从属性设为4/4"""
        # 使用 Buff 设置属性（参考 TOY_813 的实现）
        yield Buff(minion, "TOY_512e2", atk=4, max_health=4)
        # 移除此 Buff（只对下一个随从生效）
        yield Destroy(SELF)


class TOY_512e2:
    """水晶海湾随从增益 - Crystal Cove Minion Buff
    Set to 4/4
    """
    # 这个 Buff 会在运行时动态设置 atk 和 max_health
    # 参数由 Buff action 传入
    pass


class TOY_521e:
    """沙箱恶霸增益 - Sandbox Scoundrel Buff
    Next card costs (2) less
    """
    # 控制者 Buff：下一张牌费用减少2
    # 参考 TOY_800e 的实现
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True  # 本回合结束时移除
    }
    
    # 使用 Aura 给手牌中的所有卡牌添加费用减少
    # 但只有第一张打出的牌会真正消耗这个效果
    update = Refresh(FRIENDLY_HAND, buff="TOY_521e2")
    
    # 监听卡牌打出，移除此 Buff
    events = Play(CONTROLLER).after(Destroy(SELF))


class TOY_521e2:
    """费用减少 Buff（应用到手牌）"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -2


class TOY_515e:
    """索尼娅增益 - Sonya Buff
    Costs (0)
    """
    # 费用变为0
    tags = {GameTag.COST: 0}
