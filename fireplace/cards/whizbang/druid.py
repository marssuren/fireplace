"""
威兹班的工坊 - DRUID
"""
from ..utils import *


# COMMON

class MIS_300:
    """抱抱泰迪熊 - Snuggle Teddy
    Gigantify Elusive, Lifesteal, Taunt
    """
    # 3费 2/4 野兽 扩大。扰魔，吸血，嘲讽
    # 官方数据：扩大机制由核心引擎自动处理，生成 8费 8/8 的 MIS_300t
    # 关键词：ELUSIVE（扰魔）、LIFESTEAL（吸血）、TAUNT（嘲讽）、GIGANTIFY（扩大）
    elusive = True
    lifesteal = True
    taunt = True


class TOY_804:
    """林中奇遇 - Woodland Wonders
    Summon two 2/5 Beetles with Taunt. Costs (3) less if you have Spell Damage.
    """
    # 5费法术 召唤两只2/5并具有嘲讽的甲虫。如果你拥有法术伤害，法力值消耗减少（3）点
    # 官方数据：自然学派法术，条件费用减少
    
    def play(self):
        # 召唤两只 2/5 嘲讽甲虫（TOY_804t）
        yield Summon(CONTROLLER, "TOY_804t")
        yield Summon(CONTROLLER, "TOY_804t")
    
    
    cost_mod = lambda self, i: -3 if SPELLPOWER(FRIENDLY_HERO).eval(self.game, self) > 0 else 0


class TOY_850:
    """魔法妙妙屋 - Magical Dollhouse
    [x]Gain Spell Damage +1 this turn only.
    """
    # 2费地标 3耐久 在本回合中获得法术伤害+1
    # 官方数据：Location 类型，每次使用获得临时法术伤害
    
    def activate(self):
        # 给控制者添加本回合法术伤害+1的 Buff
        yield Buff(FRIENDLY_HERO, "TOY_850e")


class TOY_850e:
    """魔法妙妙屋 Buff"""
    tags = {
        GameTag.SPELLPOWER: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True  # 本回合结束时移除
    }


class TOY_851:
    """无底玩具箱 - Bottomless Toy Chest
    Discover a card from your deck. If you have Spell Damage, copy it.
    """
    # 2费法术 从你的牌库中发现一张牌。如果你拥有法术伤害，复制它
    # 官方数据：奥术学派法术，条件复制
    
    def play(self):
        # 从牌库中发现一张牌
        cards = yield GenericChoice(CONTROLLER, FRIENDLY_DECK)
        if cards:
            discovered_card = cards[0]
            # 将发现的牌加入手牌
            yield Give(CONTROLLER, discovered_card.id)
            
            # 如果拥有法术伤害，再复制一张
            if SPELLPOWER(FRIENDLY_HERO).eval(self.game, self) > 0:
                yield Give(CONTROLLER, discovered_card.id)


# RARE

class MIS_301:
    """豆蔓疯长 - Overgrown Beanstalk
    Summon a 2/2 Treant. Draw a card for each Treant you control.
    """
    # 3费法术 召唤一个2/2的树人。你每控制一个树人，抽一张牌
    # 官方数据：自然学派法术，树人协同
    # 注意：树人识别通过名称匹配，因为 fireplace 中树人没有统一的种族标签
    # 这是项目中处理树人的标准方式（参考其他扩展包的树人卡牌）
    
    def play(self):
        # 先召唤一个树人
        yield Summon(CONTROLLER, "MIS_301t")
        
        # 计算场上树人数量（包括刚召唤的）
        # 树人通过名称识别（fireplace 标准做法）
        treants = FRIENDLY_MINIONS.eval(self.game, self)
        treant_count = sum(1 for minion in treants if "树人" in minion.data.name or "Treant" in minion.data.name)
        
        # 每个树人抽一张牌
        for _ in range(treant_count):
            yield Draw(CONTROLLER)


class TOY_800:
    """闪光试剂瓶 - Sparkling Phial
    [x]Deal $2 damage. Your next card this turn costs that much less.
    """
    # 4费法术 造成$2点伤害。你在本回合中使用的下一张牌的法力值消耗减少等同于伤害值的数值
    # 官方数据：奥术学派法术，需要目标
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)
        
        # 给控制者添加 Buff，下一张牌费用减少2点
        # 这个 Buff 会在下一张牌打出时自动应用费用减少
        yield Buff(CONTROLLER, "TOY_800e")


class TOY_800e:
    """闪光试剂瓶 Buff - 下一张牌费用减少"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True  # 本回合结束时移除
    }
    
    # 使用 Aura 给手牌中的所有卡牌添加费用减少
    # 但只有第一张打出的牌会真正消耗这个效果
    update = Refresh(FRIENDLY_HAND, buff="TOY_800e2")
    
    # 监听卡牌打出，移除此 Buff
    events = Play(CONTROLLER).after(Destroy(SELF))


class TOY_800e2:
    """费用减少 Buff（应用到手牌）"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -2


class TOY_801:
    """绿植幼龙 - Chia Drake
    Miniaturize Choose One - Gain Spell Damage +1; or Draw a spell.
    """
    # 4费 2/4 龙 微缩。抉择：获得法术伤害+1；或者抽一张法术牌
    # 官方数据：Miniaturize 机制由核心引擎自动处理，生成 1费 1/1 的 TOY_801t
    # Choose One 机制
    
    choose = ("TOY_801a", "TOY_801b")


class TOY_801a:
    """获得法术伤害+1"""
    play = Buff(FRIENDLY_HERO, "TOY_801e")


class TOY_801e:
    """法术伤害+1 Buff"""
    tags = {
        GameTag.SPELLPOWER: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_801b:
    """抽一张法术牌"""
    play = ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)


class TOY_802:
    """发条树苗 - Wind-Up Sapling
    [x]Tradeable Battlecry: Refresh 1 Mana Crystal. <i>(Trade to upgrade!)</i>
    """
    # 2费 2/1 可交易。战吼：刷新1点法力水晶。（交易后升级！）
    # 官方数据：Tradeable 机制，战吼刷新法力水晶
    # 
    # 【交易升级机制】每次交易后，刷新的法力水晶数量增加
    # - 基础版本：刷新 1 点法力水晶
    # - 交易 1 次后：刷新 2 点法力水晶
    # - 交易 2 次后：刷新 3 点法力水晶
    # - 以此类推
    # 
    # 实现方式：使用卡牌自定义属性 times_traded 追踪交易次数
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化交易次数计数器
        if not hasattr(self, 'times_traded'):
            self.times_traded = 0
    
    def play(self):
        # 刷新法力水晶，数量 = 1 + 交易次数
        mana_to_refresh = 1 + getattr(self, 'times_traded', 0)
        for _ in range(mana_to_refresh):
            yield GainMana(CONTROLLER, 1)
    
    # 监听交易事件，增加交易计数器
    # 注意：Tradeable 机制由核心引擎处理，这里我们需要在卡牌返回牌库时增加计数器
    # 使用 ZoneChange 事件监听卡牌从手牌返回牌库
    events = ZoneChange(SELF, Zone.HAND, Zone.DECK).after(
        lambda self: setattr(self, 'times_traded', getattr(self, 'times_traded', 0) + 1)
    )


# EPIC

class TOY_803:
    """青玉展品 - Jade Display
    [x]Deathrattle: Your Jade Displays have +1/+1 this game. Shuffle 2 of them into your deck.
    """
    # 1费 1/1 亡语：在本局对战中，你的青玉展品拥有+1/+1。将2张青玉展品洗入你的牌库
    # 官方数据：自我增强机制，类似青玉莲花
    # 
    # 【核心引擎扩展】使用自定义属性 controller.jade_display_buff
    # 这是一个游戏级别的计数器，用于追踪青玉展品的增强次数
    # 类似于青玉莲花的 jade_golem 计数器（参考 gadgetzan/druid.py）
    # 这个属性在 Player 类中动态创建，不需要预先声明
    
    def deathrattle(self):
        # 增加青玉展品的全局计数器
        if not hasattr(self.controller, "jade_display_buff"):
            self.controller.jade_display_buff = 0
        self.controller.jade_display_buff += 1
        
        # 将2张青玉展品洗入牌库
        yield Shuffle(CONTROLLER, "TOY_803")
        yield Shuffle(CONTROLLER, "TOY_803")
    
    @property
    def atk_buff(self):
        """根据全局计数器增加攻击力"""
        return getattr(self.controller, "jade_display_buff", 0)
    
    @property
    def health_buff(self):
        """根据全局计数器增加生命值"""
        return getattr(self.controller, "jade_display_buff", 0)
    
    # 使用 Aura 动态更新属性
    update = Refresh(SELF, {
        GameTag.ATK: lambda self, i: self.atk + getattr(self.controller, "jade_display_buff", 0),
        GameTag.HEALTH: lambda self, i: self.max_health + getattr(self.controller, "jade_display_buff", 0)
    })


class TOY_805:
    """缩小术 - Ensmallen
    Reduce the Cost and Attack of minions in your deck by (1).
    """
    # 3费法术 使你牌库中的随从牌的法力值消耗和攻击力减少（1）点
    # 官方数据：自然学派法术，永久性 Buff
    
    def play(self):
        # 给牌库中所有随从添加费用和攻击力减少的 Buff
        minions_in_deck = FRIENDLY_DECK + MINION
        for minion in minions_in_deck.eval(self.game, self):
            yield Buff(minion, "TOY_805e")


class TOY_805e:
    """缩小术 Buff"""
    tags = {
        GameTag.ATK: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    cost_mod = -1


# LEGENDARY

class MIS_712:
    """模玩泰拉图斯 - Toyrantus
    Taunt, Elusive Battlecry: If you have 10 Mana Crystals, gain +7/+7.
    """
    # 6费 7/7 野兽 传说 嘲讽，扰魔。战吼：如果你有10点法力水晶，获得+7/+7
    # 官方数据：条件 Buff
    taunt = True
    elusive = True
    
    def play(self):
        # 检查是否有10点法力水晶
        if self.controller.max_mana >= 10:
            yield Buff(SELF, "MIS_712e")


class MIS_712e:
    """模玩泰拉图斯 Buff"""
    tags = {
        GameTag.ATK: 7,
        GameTag.HEALTH: 7,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class TOY_806:
    """天空慈母艾维娜 - Sky Mother Aviana
    [x]Battlecry: Shuffle 10 random Legendary minions into your deck. They cost (1).
    """
    # 5费 5/5 传说 战吼：随机将10张传说随从牌洗入你的牌库，它们的法力值消耗为（1）点
    # 官方数据：随机传说随从，费用修改
    
    def play(self):
        # 随机生成10张传说随从牌并洗入牌库
        for _ in range(10):
            # 随机获取一张传说随从
            card = yield RandomCollectible(card_type=CardType.MINION, rarity=Rarity.LEGENDARY)
            if card:
                # 添加费用减少的 Buff
                yield Buff(card, "TOY_806e")
                # 洗入牌库
                yield Shuffle(CONTROLLER, card)


class TOY_806e:
    """艾维娜的祝福 - 费用变为1"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    
    cost_mod = lambda self, i: 1 - self.owner.cost if (hasattr(self, 'owner') and self.owner) else 0


class TOY_807:
    """欧洛尼乌斯 - Owlonius
    [x]Spell Damage +1 Your spells get double bonus from Spell Damage.
    """
    # 7费 6/6 传说 法术伤害+1。你的法术从法术伤害中获得双倍加成
    # 官方数据：法术伤害增强，使用核心引擎的 SPELLPOWER_DOUBLE 标签
    # 
    # 【完整实现】使用 GameTag.SPELLPOWER_DOUBLE
    # 参考：classic/priest.py 中的先知维伦 (EX1_350)
    # 核心引擎在 player.py 的 get_spell_damage() 方法中处理此标签
    # 
    # 工作原理：
    # 1. 法术基础伤害 + 法术伤害加成 = 总伤害
    # 2. 如果有 SPELLPOWER_DOUBLE，法术伤害加成部分翻倍
    # 3. 例如：火球术(6点) + 法术伤害+2 = 6 + 2*2 = 10点伤害
    
    spellpower = 1
    
    # 使用 Aura 给控制者添加 SPELLPOWER_DOUBLE 标签
    # 这会让法术伤害加成翻倍（核心引擎自动处理）
    update = Refresh(CONTROLLER, {
        GameTag.SPELLPOWER_DOUBLE: 1
    })


