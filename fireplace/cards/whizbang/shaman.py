"""
威兹班的工坊 - SHAMAN
"""
from ..utils import *


# COMMON

class TOY_508:
    """立体书 - Pop-Up Book
    Deal $2 damage. Summon two 0/1 Frogs with Taunt.
    造成$2点伤害。召唤两只0/1并具有<b>嘲讽</b>的青蛙。
    """
    # 1费自然法术
    # 效果：造成2点伤害，召唤两只0/1嘲讽青蛙
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)
        
        # 召唤两只0/1嘲讽青蛙
        yield Summon(CONTROLLER, "TOY_508t")
        yield Summon(CONTROLLER, "TOY_508t")


class TOY_046:
    """超值惊喜 - Incredible Value
    <b>Discover</b> a 4-Cost minion. Set its Attack and Health to 7.
    <b>发现</b>一张法力值消耗为（4）的随从牌，将其攻击力和生命值变为7。
    """
    # 3费暗影法术
    # 效果：发现4费随从，设置属性为7/7
    
    def play(self):
        # 发现一张4费随从牌
        cards = yield DISCOVER(RandomCollectible(type=CardType.MINION, cost=4))
        
        if cards:
            discovered_card = cards[0]
            # 将其攻击力和生命值设置为7
            yield Buff(discovered_card, "TOY_046e", atk=7, max_health=7)


class TOY_513:
    """沙画元素 - Sand Art Elemental
    <b>Miniaturize</b>
    <b>Battlecry:</b> Give your hero +1 Attack and <b>Windfury</b> this turn.
    <b>微缩</b>
    <b>战吼：</b>在本回合中，使你的英雄获得+1攻击力和<b>风怒</b>。
    """
    # 4费 4/4 元素 微缩
    # 战吼：英雄+1攻击力和风怒（本回合）
    
    def play(self):
        # 给英雄+1攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "TOY_513e")
        # 给英雄风怒（本回合）
        yield Buff(FRIENDLY_HERO, "TOY_513e2")


class MIS_306:
    """火箭跳蛙 - Rocket Hopper
    <b>Rush</b>. <b>Overload:</b> (4)
    <b>突袭</b>。<b>过载：</b>（4）
    """
    # 5费 10/10 野兽 突袭 过载(4)
    # 迷你包卡牌
    rush = True


# RARE

class MIS_701:
    """恋旧风潮 - Wave of Nostalgia
    Transform ALL minions into random Legendary ones from the past.
    将所有随从变形成为来自过去的随机<b>传说</b>随从。
    """
    # 6费自然法术
    # 效果：将所有随从变形为随机传说随从（来自过去的扩展包）
    # 迷你包卡牌
    
    def play(self):
        # 获取所有随从（双方）
        all_minions = (FRIENDLY_MINIONS + ENEMY_MINIONS).eval(self.game, self)
        
        # 对每个随从进行变形
        for minion in all_minions:
            # 随机选择一张传说随从（来自过去的扩展包）
            # 排除当前扩展包 WHIZBANGS_WORKSHOP
            legendary_minion = yield RandomCollectible(
                type=CardType.MINION,
                rarity=Rarity.LEGENDARY,
                card_set=~CardSet.WHIZBANGS_WORKSHOP
            )
            
            if legendary_minion:
                yield Morph(minion, legendary_minion)


class MIS_307:
    """水宝宝鱼人 - Murloc Growfin
    <b>Gigantify</b>
    <b>Battlecry:</b> Summon a Tinyfin with <b>Rush</b> and stats equal to this minion's.
    <b>扩大</b>
    <b>战吼：</b>召唤一个属性值等同于本随从并具有<b>突袭</b>的鱼人宝宝。
    """
    # 1费 1/1 鱼人 扩大化
    # 战吼：召唤一个属性等同于本随从并具有突袭的鱼人宝宝
    # 迷你包卡牌
    
    def play(self):
        # 召唤鱼人宝宝 Token
        tinyfin = yield Summon(CONTROLLER, "MIS_307t")
        
        if tinyfin:
            # 设置属性值等同于本随从
            yield Buff(tinyfin[0], "MIS_307e", atk=self.atk, max_health=self.max_health)


class TOY_507:
    """童话林地 - Fairy Tale Forest
    Draw a <b>Battlecry</b> minion. It costs (1) less.
    抽一张<b>战吼</b>随从牌，其法力值消耗减少（1）点。
    """
    # 3费地标 2耐久
    # 效果：抽一张战吼随从牌，费用减少1
    
    def activate(self):
        # 抽一张战吼随从牌
        drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + BATTLECRY)
        
        if drawn:
            # 费用减少1
            yield Buff(drawn[0], "TOY_507e")


class TOY_500:
    """苏打火山 - Baking Soda Volcano
    <b>Lifesteal</b>. Deal $10 damage randomly split among all minions. <b>Overload:</b> (1)
    <b>吸血</b>。造成$10点伤害，随机分配到所有随从身上。<b>过载：</b>（1）
    """
    # 4费火焰法术 吸血 过载(1)
    # 效果：造成10点伤害随机分配到所有随从
    # 注意：ImmuneToSpellpower 标签表示不受法术伤害加成影响
    # 吸血机制会自动处理（通过 LIFESTEAL 标签）
    
    # 使用标准的随机分配伤害模式（参考 LOOT_373 Healing Rain）
    play = Hit(RANDOM(FRIENDLY_MINIONS + ENEMY_MINIONS), 1) * 10


class TOY_877:
    """星空祈愿 - Wish Upon a Star
    Give +2/+3 to all minions in your hand, deck, and battlefield.
    使你手牌，牌库和战场上的所有随从获得+2/+3。
    """
    # 7费奥术法术
    # 效果：手牌、牌库、战场上的所有随从+2/+3
    
    play = Buff(FRIENDLY_HAND + FRIENDLY_DECK + FRIENDLY_MINIONS + MINION, "TOY_877e")


# EPIC

class TOY_503:
    """闪岩哨兵 - Shining Sentinel
    <b>Taunt</b>. <b>Elusive</b>
    <b>Battlecry:</b> Summon a copy of this.
    <b>嘲讽</b>。<b>扰魔</b>
    <b>战吼：</b>召唤一个本随从的复制。
    """
    # 7费 3/7 元素 嘲讽 扰魔
    # 战吼：召唤复制
    taunt = True
    elusive = True
    
    def play(self):
        # 召唤本随从的复制
        yield Summon(CONTROLLER, ExactCopy(SELF))


class TOY_506:
    """很久以前…… - Once Upon a Time...
    Summon a random 3-Cost Beast, Dragon, Elemental, and Murloc.
    随机召唤法力值消耗为（3）的野兽，龙，元素和鱼人各一个。
    """
    # 6费自然法术
    # 效果：召唤随机3费野兽、龙、元素、鱼人各一个
    
    def play(self):
        # 召唤3费野兽
        beast = yield RandomCollectible(type=CardType.MINION, cost=3, race=Race.BEAST)
        if beast:
            yield Summon(CONTROLLER, beast)
        
        # 召唤3费龙
        dragon = yield RandomCollectible(type=CardType.MINION, cost=3, race=Race.DRAGON)
        if dragon:
            yield Summon(CONTROLLER, dragon)
        
        # 召唤3费元素
        elemental = yield RandomCollectible(type=CardType.MINION, cost=3, race=Race.ELEMENTAL)
        if elemental:
            yield Summon(CONTROLLER, elemental)
        
        # 召唤3费鱼人
        murloc = yield RandomCollectible(type=CardType.MINION, cost=3, race=Race.MURLOC)
        if murloc:
            yield Summon(CONTROLLER, murloc)


# LEGENDARY

class TOY_501:
    """沙德木刻 - Shudderblock
    <b>Miniaturize</b>
    <b>Battlecry:</b> Your next <b>Battlecry</b> triggers 3 times, but can't damage the enemy hero.
    <b>微缩</b>
    <b>战吼：</b>你的下一个<b>战吼</b>会触发3次，但无法伤害敌方英雄。
    """
    # 6费 5/5 传说随从 微缩
    # 战吼：下一个战吼触发3次（1次原始 + 2次额外），但无法伤害敌方英雄
    # 参考 LOOT_517 (Murmuring Elemental) 的实现
    # 
    # 【核心引擎扩展】已完整实现
    # 1. Battlecry action 扩展：
    #    - 添加 get_extra_battlecry_count() 方法来统计 EXTRA_BATTLECRIES buff 的数量
    #    - 修改 do() 方法，根据 buff 数量决定额外触发次数
    #    - 通过叠加两个 EXTRA_BATTLECRIES buff，可以让战吼触发3次
    # 2. Hit action 扩展：
    #    - 添加对 battlecry_cant_damage_enemy_hero 属性的检查
    #    - 当战吼效果尝试伤害敌方英雄时，自动跳过伤害
    #    - 完整实现"无法伤害敌方英雄"的限制
    
    def play(self):
        # 给控制者添加两个 EXTRA_BATTLECRIES buff
        # 核心引擎会统计 buff 数量，让战吼额外触发2次（总共3次）
        # 同时这些 buff 带有 battlecry_cant_damage_enemy_hero 标记
        yield Buff(CONTROLLER, "TOY_501e")
        yield Buff(CONTROLLER, "TOY_501e")


class TOY_504:
    """神秘女巫哈加莎 - Hagatha the Fabled
    <b>Battlecry:</b> Draw 2 spells that cost (5) or more. Transform them into Slimes that cast the spells.
    <b>战吼：</b>抽两张法力值消耗大于或等于（5）点的法术牌，并将其变形成为会施放对应法术的泥浆怪。
    """
    # 4费 4/3 传说随从
    # 战吼：抽两张5费及以上法术，变形为施放对应法术的泥浆怪
    # 泥浆怪是2/2元素，战吼时施放存储的法术
    
    def play(self):
        # 抽两张5费及以上的法术牌
        for _ in range(2):
            # 抽一张5费及以上的法术牌
            drawn = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL + (COST(ForceDraw.CARD) >= 5))
            
            if drawn:
                spell_card = drawn[0]
                # 记录法术ID（在变形前）
                spell_id = spell_card.id
                
                # 变形为泥浆怪 Token
                # 使用 Morph 将法术变形为泥浆怪
                # 泥浆怪会在打出时施放对应的法术
                slime_cards = yield Morph(spell_card, "TOY_504t")
                
                # 将法术ID存储到泥浆怪上（用于战吼时施放）
                if slime_cards:
                    slime = slime_cards[0] if isinstance(slime_cards, list) else slime_cards
                    # 使用属性存储法术ID
                    slime.stored_spell_id = spell_id


# ========================================
# Buff 定义
# ========================================

class TOY_046e:
    """超值惊喜增益 - Incredible Value Buff
    Set to 7/7
    """
    # 这个 Buff 会在运行时动态设置 atk 和 max_health
    # 参数由 Buff action 传入
    pass


class TOY_513e:
    """沙画元素增益（攻击力） - Sand Art Elemental Buff (Attack)
    +1 Attack this turn
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.ATK: 1,
    }


class TOY_513e2:
    """沙画元素增益（风怒） - Sand Art Elemental Buff (Windfury)
    Windfury this turn
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True,
        GameTag.WINDFURY: True
    }


class MIS_307e:
    """鱼人宝宝增益 - Tinyfin Buff
    Stats equal to Murloc Growfin
    """
    # 这个 Buff 会在运行时动态设置 atk 和 max_health
    # 参数由 Buff action 传入
    pass


class TOY_507e:
    """童话林地增益 - Fairy Tale Forest Buff
    Costs (1) less
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost_mod = -1


class TOY_877e:
    """星空祈愿增益 - Wish Upon a Star Buff
    +2/+3
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
    }


class TOY_501e:
    """沙德木刻增益 - Shudderblock Buff
    Next Battlecry triggers one extra time, but can't damage enemy hero
    """
    # 控制者 Buff：战吼额外触发一次，但无法伤害敌方英雄
    # 参考 LOOT_517e (Murmuring Elemental) 的实现
    # 通过叠加两个此 Buff，核心引擎会让战吼触发3次（1次原始 + 2次额外）
    
    tags = {GameTag.TAG_ONE_TURN_EFFECT: True}
    
    # 使用 Refresh 给控制者添加 EXTRA_BATTLECRIES 效果
    update = Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True})
    
    # 在打出战吼随从后移除此 Buff
    events = Play(CONTROLLER, MINION + BATTLECRY).after(Destroy(SELF))
    
    # 【核心引擎扩展】"无法伤害敌方英雄"的限制
    # 已扩展 Hit action 来检查此属性
    # 当战吼效果尝试伤害敌方英雄时，Hit action 会检查此标记并跳过伤害
    battlecry_cant_damage_enemy_hero = True
