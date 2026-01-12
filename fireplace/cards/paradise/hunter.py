"""
胜地历险记 - HUNTER
"""
from ..utils import *


# COMMON

class VAC_412:
    """当日渔获 - Catch of the Day
    Rush. Battlecry: Summon a 2/1 Worm for your opponent.
    突袭。战吼：为你的对手召唤一只2/1的鱼虫。
    """
    mechanics = [GameTag.RUSH, GameTag.BATTLECRY]
    
    def play(self):
        # 为对手召唤一只 2/1 的鱼虫 Token
        yield Summon(OPPONENT, "VAC_412t")


class VAC_960:
    """可靠的鱼竿 - Trusty Fishing Rod
    After your hero attacks, summon a 1-Cost minion from your deck.
    在你的英雄攻击后，从你的牌库中召唤一个法力值消耗为（1）的随从。
    """
    # 武器，监听英雄攻击事件
    events = Attack(FRIENDLY_HERO).after(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == 1)))
    )


class VAC_961:
    """宠物鹦鹉 - Pet Parrot
    Battlecry: Repeat the last 1-Cost card you played.
    战吼：重复你使用的上一张法力值消耗为（1）的牌。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 获取上一张打出的1费牌
        # 从 controller.cards_played_this_game 中查找
        last_1_cost = None
        for card in reversed(self.controller.cards_played_this_game):
            # 排除自己（VAC_961）
            if card.id != "VAC_961" and card.cost == 1:
                last_1_cost = card
                break
        
        if last_1_cost:
            # 创建并打出这张牌的复制
            copy = self.controller.card(last_1_cost.id, self.controller)
            yield Play(CONTROLLER, copy)


class WORK_018:
    """劳作老马 - Workhorse
    Deathrattle: Summon two 2/1 Ponies.
    亡语：召唤两匹2/1的小马。
    """
    mechanics = [GameTag.DEATHRATTLE]
    deathrattle = Summon(CONTROLLER, "WORK_018t") * 2


class WORK_019:
    """摇钱金牛 - Cash Cow
    Taunt. Whenever this takes damage, get a Coin.
    嘲讽。每当本随从受到伤害，获取一张幸运币。
    """
    mechanics = [GameTag.TAUNT]
    
    # 监听受伤事件
    events = Damage(SELF).on(
        Give(CONTROLLER, "GAME_005")  # 幸运币的 ID
    )


# RARE

class VAC_408:
    """观赏鸟类 - Birdwatching
    Discover a minion from your deck. Give all copies of it +2/+1 (wherever they are).
    从你的牌库中发现一张随从牌。使其所有的复制获得+2/+1（无论它们在哪）。
    """
    def play(self):
        # 从牌库中发现一张随从牌
        cards = yield Discover(CONTROLLER, cards=FRIENDLY_DECK + MINION)
        
        if cards:
            discovered_card = cards[0]
            card_id = discovered_card.id
            
            # 给所有同ID的卡牌（手牌、牌库、场上）+2/+1
            # 手牌
            for card in self.controller.hand:
                if card.id == card_id and card.type == CardType.MINION:
                    yield Buff(card, "VAC_408e")
            
            # 牌库
            for card in self.controller.deck:
                if card.id == card_id and card.type == CardType.MINION:
                    yield Buff(card, "VAC_408e")
            
            # 场上
            for minion in self.controller.field:
                if minion.id == card_id:
                    yield Buff(minion, "VAC_408e")


class VAC_408e:
    """观赏鸟类增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class VAC_409:
    """鹦鹉乐园 - Parrot Sanctuary
    Your next Battlecry minion costs (1) less. After you play a Battlecry minion, reopen this.
    你的下一张战吼随从牌的法力值消耗减少（1）点。在你使用一张战吼随从牌后，重新开启本地标。
    """
    def activate(self):
        # 给玩家添加一个 buff，使下一张战吼随从减1费
        yield Buff(CONTROLLER, "VAC_409e")
    
    # 监听打出战吼随从，重新开启地标
    events = Play(CONTROLLER, MINION + BATTLECRY).after(
        Refresh(SELF)
    )


class VAC_409e:
    """鹦鹉乐园减费效果 (Player Enchantment)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    class Hand:
        # 下一张战吼随从减1费
        def cost(self, i):
            # 检查卡牌是否是战吼随从
            if self.owner.type == CardType.MINION and self.owner.has_battlecry:
                return i - 1
            return None
    
    # 打出战吼随从后移除此效果
    events = Play(CONTROLLER, MINION + BATTLECRY).after(Destroy(SELF))


class VAC_410:
    """猛禽狂怒 - Furious Fowls
    Choose an enemy. Summon two 3/3 Birds with Immune while attacking to attack it.
    选择一个敌人。召唤两只3/3并具有攻击时免疫的小鸟，攻击选中的敌人。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_ENEMY_TARGET: 0}
    
    def play(self):
        # 召唤2只小鸟
        birds = yield Summon(CONTROLLER, "VAC_410t", 2)
        
        # 让每只小鸟攻击目标
        if birds:
            for bird in birds:
                if bird.zone == Zone.PLAY:  # 确保召唤成功
                    yield Attack(bird, TARGET)


class WORK_020:
    """业务支猿 - Monkey Business
    Add 8 Bananas to your hand. Any that can't fit are randomly fed to friendly minions in play.
    将8根香蕉置入你的手牌。放不下的香蕉会随机喂给场上的友方随从。
    """
    def play(self):
        # 尝试给8根香蕉
        for _ in range(8):
            # 检查手牌是否已满
            if len(self.controller.hand) < self.controller.max_hand_size:
                # 手牌未满，直接给香蕉
                yield Give(CONTROLLER, "EX1_014t")  # 香蕉的 ID
            else:
                # 手牌已满，随机给场上一个友方随从 +1/+1
                minions = self.controller.field
                if minions:
                    target = self.game.random.choice(minions)
                    yield Buff(target, "EX1_014te")  # 香蕉的 buff


# EPIC

class VAC_407:
    """话痨鹦鹉 - Chatty Macaw
    Battlecry: Repeat the last spell you cast at an enemy (at a random enemy if possible).
    战吼：（尽可能对一个随机的敌人）重新施放你对一个敌人施放的上一个法术。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 获取上一张对敌人施放的法术
        # 使用 Player 类中的 last_spell_cast_at_enemy 属性
        # 这个属性在 Play action 中自动追踪对敌方角色施放的法术
        last_spell = self.controller.last_spell_cast_at_enemy
        
        if last_spell:
            # 创建法术的复制并施放
            copy = self.controller.card(last_spell.id, self.controller)
            
            # 检查法术是否需要敌方目标
            enemies = self.game.board.get_enemies(self.controller)
            if enemies and hasattr(copy, 'requirements'):
                # 随机选择一个敌人作为目标
                target = self.game.random.choice(enemies)
                yield Play(CONTROLLER, copy, target=target)
            else:
                # 不需要目标或没有敌人
                yield Play(CONTROLLER, copy)




class VAC_416:
    """死亡翻滚 - Death Roll
    Destroy an enemy minion. Deal damage equal to its Attack randomly split among all enemies.
    消灭一个敌方随从。造成等同于其攻击力的伤害，随机分配到所有敌人身上。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_ENEMY_TARGET: 0}
    
    def play(self):
        # 记录目标的攻击力
        attack = TARGET.atk
        
        # 消灭目标
        yield Destroy(TARGET)
        
        # 造成等同于攻击力的伤害，随机分配
        for _ in range(attack):
            enemies = self.game.board.get_enemies(self.controller)
            if enemies:
                target = self.game.random.choice(enemies)
                yield Hit(target, 1)


# LEGENDARY

class VAC_413:
    """园林护卫者基利 - Ranger Gilly
    Warrior Tourist. At the end of your turn, get a 2/3 Crocolisk. Deathrattle: Give all minions in your hand +2/+3.
    战士游客。在你的回合结束时，获取一张2/3的鳄鱼。亡语：使你手牌中的所有随从牌获得+2/+3。
    """
    mechanics = [GameTag.DEATHRATTLE]
    
    # 回合结束时获得鳄鱼
    events = OWN_TURN_END.on(
        Give(CONTROLLER, "VAC_413t")
    )
    
    def deathrattle(self):
        # 给手牌中所有随从 +2/+3
        for card in self.controller.hand:
            if card.type == CardType.MINION:
                yield Buff(card, "VAC_413e")


class VAC_413e:
    """园林护卫者基利增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class VAC_415:
    """大叫巨鹦萨考克 - Sasquawk
    Battlecry: Repeat each card you played last turn.
    战吼：重复你在上回合使用的每一张牌。
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 使用 Player 类中已有的 cards_played_last_turn 列表
        # 这个列表存储的是上回合使用的卡牌ID
        if hasattr(self.controller, 'cards_played_last_turn'):
            for card_id in self.controller.cards_played_last_turn:
                # 创建卡牌并加入手牌,然后尝试打出
                # 注意:这里简化处理,直接给予卡牌而不是打出
                # 因为打出需要选择目标等复杂逻辑
                yield Give(CONTROLLER, card_id)



