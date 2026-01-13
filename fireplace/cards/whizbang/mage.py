"""
威兹班的工坊 - MAGE
"""
from ..utils import *


# COMMON

class MIS_302:
    """买一冻一 - Buy One, Get One Freeze
    Freeze a minion. Summon a Frozen copy of it.
    """
    # 3费法术 冻结一个随从，召唤一个它的被冻结的复制
    # 官方数据：冰霜学派法术，需要目标
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        # 冻结目标随从
        yield Freeze(TARGET)
        
        # 召唤一个被冻结的复制
        # 使用 SummonCopy 召唤复制
        copy = yield SummonCopy(TARGET)
        
        # 冻结刚召唤的复制
        if copy:
            yield Freeze(copy)


class TOY_037:
    """寻物解谜 - Hidden Objects
    Discover a Secret. Set its Cost to (1).
    """
    # 2费法术 发现一张奥秘牌，将其法力值消耗变为（1）点
    # 官方数据：奥术学派法术，Discover 机制
    
    def play(self):
        # 发现一张法师奥秘
        cards = yield GenericChoice(CONTROLLER, FRIENDLY_CLASS + SECRET)
        if cards:
            # Discover 会自动将牌加入手牌
            # 添加费用修改 Buff
            yield Buff(cards[0], "TOY_037e")


class TOY_037e:
    """找到了！ - 费用变为1"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    cost_mod = lambda self, i: 1 - self.owner.cost if (hasattr(self, 'owner') and self.owner) else 0


class TOY_370:
    """三芯诡烛 - Triplewick Trickster
    Battlecry: Deal 2 damage to a random enemy, three times.
    """
    # 4费 2/3 元素 战吼：随机对一个敌人造成2点伤害，触发三次
    # 官方数据：元素种族，战吼机制
    
    def play(self):
        # 随机对敌人造成2点伤害，重复3次
        for _ in range(3):
            yield Hit(RANDOM_ENEMY_CHARACTER, 2)


class TOY_374:
    """找不同 - Spot the Difference
    Discover a 3-Cost minion to summon. If your deck has no minions, repeat this.
    """
    # 4费法术 发现一个法力值消耗为（3）点的随从并召唤它。如果你的牌库里没有随从牌，重复此效果
    # 官方数据：奥术学派法术，Discover 机制，"无随从"协同
    
    def play(self):
        # 检查牌库中是否有随从
        deck_has_no_minions = not (FRIENDLY_DECK + MINION).eval(self.game, self)
        
        # 第一次发现并召唤
        cards = yield GenericChoice(CONTROLLER, RandomCollectible(card_type=CardType.MINION, cost=3))
        if cards:
            yield Summon(CONTROLLER, cards[0])
        
        # 如果牌库没有随从，再次发现并召唤
        if deck_has_no_minions:
            cards = yield GenericChoice(CONTROLLER, RandomCollectible(card_type=CardType.MINION, cost=3))
            if cards:
                yield Summon(CONTROLLER, cards[0])


# RARE

class MIS_107:
    """玩具故障 - Malfunction
    Deal $3 damage split among all enemy minions. If your deck has no minions, deal $3 more.
    """
    # 2费法术 造成$3点伤害，随机分配到所有敌方随从身上。如果你的牌库中没有随从牌，再造成$3点
    # 官方数据：奥术学派法术，"无随从"协同，免疫法术伤害加成
    
    def play(self):
        # 检查牌库中是否有随从
        deck_has_no_minions = not (FRIENDLY_DECK + MINION).eval(self.game, self)
        
        # 基础伤害3点
        total_damage = 3
        
        # 如果牌库没有随从，再造成3点伤害
        if deck_has_no_minions:
            total_damage += 3
        
        # 随机分配伤害到所有敌方随从
        # 使用 HitAll 分配伤害（fireplace 会自动随机分配）
        for _ in range(total_damage):
            yield Hit(RANDOM(ENEMY_MINIONS), 1)


class MIS_303:
    """暗月魔术师 - Darkmoon Magician
    Elusive. After you cast a spell, cast a random spell that costs (1) more.
    """
    # 3费 2/4 扰魔。在你施放一个法术后，随机施放一个法力值消耗增加（1）点的法术
    # 官方数据：扰魔关键词，触发效果
    # 
    # 【完整实现】使用事件参数追踪刚施放的法术费用
    # 参考：uldum/mage.py 中的 ULD_238 (火焰风暴)
    elusive = True
    
    def OWN_SPELL_PLAY_TRIGGER(self, player, card, *args):
        """在施放法术后，随机施放一个费用为 (card.cost + 1) 的法术"""
        # 获取刚施放的法术费用
        spell_cost = card.cost
        # 随机施放一个费用为 (spell_cost + 1) 的法术
        return [CastSpell(RandomSpell(cost=spell_cost + 1))]
    
    events = OWN_SPELL_PLAY.after(OWN_SPELL_PLAY_TRIGGER)


class TOY_371:
    """加工失误 - Manufacturing Error
    Draw 3 cards. If your deck has no minions, they cost (3) less.
    """
    # 5费法术 抽三张牌。如果你的牌库里没有随从牌，这三张牌的法力值消耗减少（3）点
    # 官方数据：奥术学派法术，"无随从"协同
    
    def play(self):
        # 检查牌库中是否有随从
        deck_has_no_minions = not (FRIENDLY_DECK + MINION).eval(self.game, self)
        
        # 抽三张牌
        drawn_cards = []
        for _ in range(3):
            cards = yield Draw(CONTROLLER)
            if cards:
                drawn_cards.extend(cards)
        
        # 如果牌库没有随从，给抽到的牌添加费用减少 Buff
        if deck_has_no_minions:
            for card in drawn_cards:
                if card.zone == Zone.HAND:  # 确保卡牌在手牌中
                    yield Buff(card, "TOY_371e")


class TOY_371e:
    """独特缺陷 - 费用减少3"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -3


class TOY_375:
    """滑冰元素 - Sleet Skater
    Miniaturize Battlecry: Freeze an enemy minion. Gain Armor equal to its Attack.
    """
    # 5费 3/4 元素 微缩。战吼：冻结一个敌方随从，获得等同于其攻击力的护甲值
    # 官方数据：Miniaturize 机制由核心引擎自动处理，生成 1费 1/1 的 TOY_375t
    # 元素种族，战吼机制
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        target = self.target
        if target:
            # 冻结目标敌方随从
            yield Freeze(target)
            
            # 获得等同于目标攻击力的护甲值
            armor_gain = target.atk
            if armor_gain > 0:
                yield GainArmor(FRIENDLY_HERO, armor_gain)


class TOY_377:
    """霜巫十字绣 - Frost Lich Cross-Stitch
    Deal $3 damage to a character. If it dies, summon a 3/6 Water Elemental that Freezes.
    """
    # 4费法术 对一个角色造成$3点伤害。如果该角色死亡，召唤一个3/6的可冻结攻击目标的水元素
    # 官方数据：冰霜学派法术，需要目标
    # 注意：官方在 Patch 29.0.3 中将伤害从4点调整为3点
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 记录目标
        target = TARGET
        
        # 造成3点伤害
        yield Hit(target, 3)
        
        # 检查目标是否死亡
        if target.dead or target.zone != Zone.PLAY:
            # 召唤一个3/6的水元素（使用经典版本的水元素 CS2_033）
            # 水元素具有冻结效果
            yield Summon(CONTROLLER, "CS2_033")


# EPIC

class TOY_372:
    """匣中古神 - Yogg in the Box
    Cast 5 random spells. If your deck has no minions, the spells cast cost (5) or more.
    """
    # 8费法术 随机施放5个法术。如果你的牌库里没有随从牌，施放的法术法力值消耗为（5）点或更高
    # 官方数据：暗影学派法术，"无随从"协同
    
    def play(self):
        # 检查牌库中是否有随从
        deck_has_no_minions = not (FRIENDLY_DECK + MINION).eval(self.game, self)
        
        # 施放5个随机法术
        for _ in range(5):
            if deck_has_no_minions:
                # 施放费用 >= 5 的随机法术
                yield CastSpell(RandomSpell(min_cost=5))
            else:
                # 施放任意随机法术
                yield CastSpell(RandomSpell())


class TOY_376:
    """水彩美术家 - Watercolor Artist
    Battlecry: Draw a Frost spell. At the start of your turns, reduce its Cost by (1).
    """
    # 3费 3/3 战吼：抽一张冰霜法术牌，在你的回合开始时，其法力值消耗减少（1）点
    # 官方数据：战吼机制，持续效果
    # 
    # 【实现说明】使用 Buff 标记抽到的冰霜法术，然后在回合开始时减少费用
    # 这个 Buff 会持续存在，每回合开始时触发费用减少
    
    def play(self):
        # 抽一张冰霜法术
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL + FROST)
        
        if cards:
            frost_spell = cards[0]
            # 给抽到的冰霜法术添加持续效果 Buff
            yield Buff(frost_spell, "TOY_376e1")


class TOY_376e:
    """冲刷褪色 - 费用减少"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -1


class TOY_376e1:
    """颜料风干 - 标记 Buff（每回合费用减少）"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: False  # 持续效果
    }
    
    # 在每个回合开始时减少费用
    events = [
        OWN_TURN_BEGIN.on(lambda self, player: 
            Buff(SELF.owner, "TOY_376e")
        )
    ]


# LEGENDARY

class TOY_373:
    """益智大师卡德加 - Puzzlemaster Khadgar
    Battlecry: Equip a 0/6 Wisdomball that casts helpful Mage spells!
    """
    # 6费 5/5 传说 战吼：装备一个会施放有用的法师法术的0/6的魔法智慧之球！
    # 官方数据：战吼机制，装备武器
    # 
    # 【完整实现】武器会施放智能法术（类似泽菲里斯）
    # 具体实现在 tokens.py 中的 TOY_373hp
    
    def play(self):
        # 装备魔法智慧之球武器（TOY_373hp）
        yield Summon(CONTROLLER, "TOY_373hp")


class TOY_378:
    """星空投影球 - The Galactic Projection Orb
    Recast a random spell of each Cost you've cast this game (targets enemies if possible).
    """
    # 10费法术 传说 重新施放你在本局对战中使用过的每种法力值消耗的随机法术（尽可能以敌人为目标）
    # 官方数据：奥术学派法术，追踪施放过的法术费用
    # 
    # 【核心引擎扩展】使用 controller.spell_costs_played_this_game
    # 这是一个游戏级别的集合，用于追踪本局对战中施放过的法术费用
    # 类似于 spell_schools_played_this_game 的实现方式
    # 已在 Player.__init__ 中初始化，在 Play action 中更新
    # 参考：player.py 第122-124行，actions.py 第785-787行
    
    def play(self):
        # 获取本局对战中施放过的所有法术费用
        spell_costs = getattr(self.controller, 'spell_costs_played_this_game', set())
        
        # 对每种费用，随机施放一个该费用的法术
        for cost in sorted(spell_costs):  # 按费用排序施放
            # 随机选择一个该费用的法术并施放
            # 注意：官方效果为"尽可能以敌人为目标"
            # fireplace 的 CastSpell 会自动处理目标选择
            yield CastSpell(RandomSpell(cost=cost))


# Token 卡牌定义将在 tokens.py 中添加
