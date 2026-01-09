from ..utils import *
from fireplace.dsl.lazynum import EventArgument

class ETC_536:
    """Audio Splitter - 音频切分机
    3费 4/3 机械
    亡语：复制你手牌中法力值消耗最高的法术牌。
    """
    race = Race.MECHANICAL
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        
    }
    
    def deathrattle(self):
        # 筛选手牌中的法术
        spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        if spells:
            # 找最高费
            max_cost = max(c.cost for c in spells)
            targets = [c for c in spells if c.cost == max_cost]
            # 随机选择一个（如果有多个同为最高费）
            target = self.game.random.choice(targets)
            yield Give(CONTROLLER, Copy(target))

class JAM_001:
    """Costumed Singer - 盛装歌手
    1费 2/1
    在你的回合结束时，抽一张奥秘牌。
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.COST: 1,
    }
    # 回合结束：抽奥秘
    events = OwnTurnEnd.on(Draw(CONTROLLER, FRIENDLY_DECK + SECRET))

class ETC_029:
    """Keyboard Soloist - 键盘独演者
    4费 4/3 纳迦
    战吼：如果你没有控制其他随从，召唤两个1/2并具有法术伤害+1的扩音器。
    """
    race = Race.NAGA
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.COST: 4,
        
    }
    
    def play(self):
        # 检查是否没有其他随从
        if len(self.controller.field) == 1: # 只有自己
            yield Summon(CONTROLLER, "ETC_029t") * 2

class ETC_029t:
    """Speaker - 扩音器"""
    race = Race.MECHANICAL
    tags = {
        GameTag.ATK: 1, 
        GameTag.HEALTH: 2, 
        
        GameTag.SPELLPOWER: 1
    }

class ETC_535:
    """Synthesize - 元素混合
    3费法术
    随机将法力值消耗为（1），（2）和（3）的元素牌各一张置入你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
    }
    
    def play(self):
        # 1费元素
        yield Give(CONTROLLER, RandomMinion(race=Race.ELEMENTAL, cost=1))
        # 2费元素
        yield Give(CONTROLLER, RandomMinion(race=Race.ELEMENTAL, cost=2))
        # 3费元素
        yield Give(CONTROLLER, RandomMinion(race=Race.ELEMENTAL, cost=3))

class ETC_521:
    """Cosmic Keyboard - 星界键盘
    2费 武器 0/3
    在你施放一个法术后，召唤一个属性值等同于其法力值消耗的元素。失去1点耐久度。
    """
    tags = {
        GameTag.CARDTYPE: CardType.WEAPON,
        GameTag.COST: 2,
        GameTag.ATK: 0,
        GameTag.HEALTH: 3,
    }
    
    # 监听施法
    # 需要获取施放法术的 Cost
    # EventArgument[1] 通常是 Card 对象
    def _summon_elemental(self, source, card):
        minion = yield Summon(CONTROLLER, "ETC_521t")
        if minion:
            stats = card.cost
            yield Buff(minion, "ETC_521e", atk=stats, max_health=stats)
        yield Hit(SELF, 1)

    events = Play(CONTROLLER, SPELL).after(_summon_elemental)

class ETC_521t:
    """Sound Construct - 音响元素"""
    race = Race.ELEMENTAL
    tags = {
        
        GameTag.ATK: 1, # 初始值，会被Buff覆盖
        GameTag.HEALTH: 1
    }

class ETC_521e:
    tags = {GameTag.ATK: 0, GameTag.HEALTH: 0} # 占位，由脚本动态赋值

class ETC_528:
    """Lightshow - 灯光表演
    3费法术
    向敌人发射2道可以造成2点伤害的灯光。你此后的灯光表演多发射一道。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 3,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    def play(self):
        # 官方文本："Shoot 2 beams at enemies that each deal 2 damage.
        # Your future Lightshows shoot one more beam."
        #
        # 逻辑：基础2道 + 之前施放的次数
        # - 第一次施放：count=1, 射 2 + (1-1) = 2 道
        # - 第二次施放：count=2, 射 2 + (2-1) = 3 道
        # - 第三次施放：count=3, 射 2 + (3-1) = 4 道
        count = self.controller.times_played("ETC_528")
        beam_count = 2 + max(0, count - 1)
        
        for i in range(beam_count):
            yield Hit(RANDOM_ENEMY_CHARACTER, 2)

class JAM_000:
    """Remixed Dispense-o-bot - 混搭派送机
    3费 3/3 机械
    在你的手牌中时会获得一项额外效果，该效果每回合都会改变。
    (需实现4种形态切换)
    """
    race = Race.MECHANICAL
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.COST: 3,
        
    }
    # 变身逻辑：回合开始时变形为下一个形态
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_000a"))

class JAM_000a:
    """Money Dispense-o-bot - 撒币派送机 (Coin)"""
    race = Race.MECHANICAL
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.COST: 3, }
    deathrattle = Give(CONTROLLER, "GAME_005") * 2 # 2个幸运币
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_000b"))

class JAM_000b:
    """Mystery Dispense-o-bot - 神秘派送机 (Random Spell)"""
    race = Race.MECHANICAL
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.COST: 3, }
    deathrattle = Give(CONTROLLER, RandomSpell()) # 随机法术
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_000c"))

class JAM_000c:
    """Merch Dispense-o-bot - 周边派送机

    官方文本："Battlecry: Get two random Mechs. (Changes each turn.)"
    战吼：获得两张随机机械牌（每回合改变）
    """
    race = Race.MECHANICAL
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.COST: 3, }

    def play(self):
        # 获得两张随机机械牌
        # 参考：RandomCollectible(race=Race.MECHANICAL)
        for i in range(2):
            yield Give(CONTROLLER, RandomCollectible(race=Race.MECHANICAL))

    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_000d"))

class JAM_000d:
    """Melody Dispense-o-bot - 旋律派送机 (Divine Shield/Taunt?)"""
    race = Race.MECHANICAL
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.COST: 3,  
            GameTag.DIVINE_SHIELD: True, GameTag.TAUNT: True}
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, "JAM_000"))


class ETC_532:
    """Rewind - 倒带
    2费法术
    发现你在本局对战中施放过的其他法术的一张复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    def play(self):
        # 本局对战施放过的法术，排除自己
        copy = Copy(FRIENDLY_PLAYED_SPELLS_THIS_GAME - ID("ETC_532"))
        yield Discover(copy)

class JAM_002:
    """Star Power - 星辰能量
    5费法术
    随机对一个敌方随从造成5点伤害。重复此效果，每次伤害减少1点。
    （注：遵循数据库特殊描述，而非标准卡牌效果）
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 5,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    def play(self):
        # 5, 4, 3, 2, 1
        for damage in range(5, 0, -1):
            yield Hit(RANDOM_ENEMY_MINION, damage)

class ETC_534:
    """Holotechnician - 全息技师
    2费 3/2
    在任意随从受到刚好1点伤害后，将其消灭。
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.COST: 2,
    }
    
    # 监听：任意随从受伤，且 amount == 1
    # Check amount logic
    # events syntax: Damage(Selector, amount=1).after(...)
    events = Damage(ALL_MINIONS, amount=1).after(Destroy(EventArgument.TARGET))

class ETC_205:
    """Volume Up - 加大音量
    4费法术
    抽三张法术牌。压轴：从中发现一张复制。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 4,
    }
    
    def play(self):
        # 抽3张法术，并捕获它们
        drawn_cards = yield Draw(CONTROLLER, FRIENDLY_DECK + SPELL) * 3
        
        # 压轴检查
        if self.controller.mana == 0 and drawn_cards:
            # 从抽到的牌中发现一张复制
            # drawn_cards 是 Card 对象列表
            # Discover 需要 Selector 或 List
            # 使用 GenericChoice 包装列表
            yield Discover(Copy(GenericChoice(drawn_cards)))

class ETC_395:
    """DJ Manastorm - DJ法力风暴
    9费 8/8 (数据中Cost=9? 文本说0/1逻辑)
    战吼：将你手牌中的法术牌法力值消耗变为（0）点。在你使用其中一张后，其余的法力值消耗增加（1）点。
    """
    race = Race.GNOME
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.COST: 9, # 遵循 inspect 结果
        
    }
    
    def play(self):
        # 1. 战吼：手牌法术变0
        spells = [c for c in self.controller.hand if c.type == CardType.SPELL]
        if spells:
            yield Buff(spells, "ETC_395e")
        
        # 2. 添加全局监听器（通过给玩家挂Buff实现）
        yield Buff(CONTROLLER, "ETC_395_Manager")

class ETC_395e:
    """Discounted - 减费"""
    tags = {GameTag.COST: SET(0)}

class ETC_395_Manager:
    """DJ Manager - DJ效果管理器"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    # 监听：施放法术后
    # 效果：手牌中所有法术费用+1
    # 这里的逻辑是：所有（包括刚抽到的？）文本说 "Rest" (其余)。
    # 通常理解为受战吼影响的那些。但根据实现难度和Hearthstone通常的一致性，
    # 往往是 "Your spells cost (0). After you cast a spell, increase cost of spells in hand by (1)."
    # 如果是对所有手牌生效，则 Buff(FRIENDLY_HAND + SPELL)
    events = Play(CONTROLLER, SPELL).after(
        Buff(FRIENDLY_HAND + SPELL, "ETC_395_Debuff")
    )

class ETC_395_Debuff:
    """Cost Increase - 费用增加"""
    tags = {GameTag.COST: 1} # 叠加+1

class ETC_206:
    """Infinitize the Maxitude - 巅峰无限
    2费法术
    发现一张法术牌，其法力值消耗减少（1）点。压轴：在回合结束时将本牌移回你的手牌。
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.COST: 2,
        GameTag.SPELL_SCHOOL: SpellSchool.ARCANE,
    }
    
    def play(self):
        # 发现法术，减1费
        # 使用 .then() 方法在 Discover 后对选中的卡牌施加减费 Buff
        # 参考：WW_358 (badlands/deathknight.py) 使用相同模式
        yield Discover(CONTROLLER, RandomSpell()).then(
            Buff(Give.CARD, "ETC_313e")
        )

        # 压轴：回合结束时回手
        if self.controller.mana == 0:
            # 给控制器添加一个回合结束时的效果
            yield Buff(CONTROLLER, "ETC_206e")


class ETC_313e:
    """减费 Buff - 减少1费"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -1,
    }


class ETC_206e:
    """Return to Hand Effect - 回手效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 回合结束时将一张 ETC_206 加入手牌
    events = OWN_TURN_END.on(
        Give(CONTROLLER, "ETC_206"),
        Destroy(SELF)
    )
