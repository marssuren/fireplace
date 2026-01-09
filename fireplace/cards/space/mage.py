"""
深暗领域 - MAGE
"""
from ..utils import *


# 星灵(Protoss)法术ID列表 - 深暗领域迷你包
# 这些是星灵主题的法术卡牌
PROTOSS_SPELL_IDS = [
    "SC_755",  # 水晶 - 德鲁伊法术
    "SC_759",  # 护盾充能器 - 法师法术
    "SC_760",  # 谐振盘 - 法师法术
    "SC_753",  # 光子炮台 - 中立法术
    # 可以根据需要添加更多星灵法术
]


# COMMON

class GDB_303:
    """爆炎流星 - Blasteroid
    Battlecry: Shuffle 5 random Fire spells into your deck. They cost (2) less.
    
    3费 3/4 法师随从 - 元素
    战吼:随机将5张火焰法术牌洗入你的牌库,其法力值消耗减少(2)点。
    """
    race = Race.ELEMENTAL
    
    def play(self):
        # 随机将5张火焰法术牌洗入牌库,并减少2点费用
        for _ in range(5):
            # 给予随机火焰法术并减费,然后洗入牌库
            card = yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.FIRE))
            if card:
                yield Buff(card, "GDB_303e")
                yield Shuffle(CONTROLLER, card)


class GDB_303e:
    """爆炎流星减费效果"""
    tags = {
        GameTag.COST: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_305:
    """阳炎耀斑 - Solar Flare
    Deal $2 damage to all enemies. Costs (1) less for each Elemental you control.
    
    5费 法师法术 - 火焰
    对所有敌人造成$2点伤害。你每控制一个元素,本牌的法力值消耗便减少(1)点。
    """
    # 动态计算费用
    @property
    def cost(self):
        base_cost = self.data.cost
        # 计算场上元素数量
        elemental_count = len([m for m in self.controller.field if m.race == Race.ELEMENTAL])
        return max(0, base_cost - elemental_count)
    
    def play(self):
        # 对所有敌人造成2点伤害
        yield Hit(ENEMY_CHARACTERS, 2)


class GDB_456:
    """自燃 - Spontaneous Combustion
    Deal $4 damage to a random enemy. If you played an Elemental last turn, choose the target.
    
    2费 法师法术 - 火焰
    随机对一个敌人造成$4点伤害。如果你在上个回合使用过元素牌,则可以选择目标。
    """
    # 根据上回合是否使用过元素来决定是否需要目标
    @property
    def requirements(self):
        # 检查上回合是否使用过元素
        if hasattr(self.controller, 'cards_played_last_turn'):
            played_elemental_last_turn = any(
                hasattr(card, 'race') and card.race == Race.ELEMENTAL 
                for card in self.controller.cards_played_last_turn
            )
            if played_elemental_last_turn:
                # 需要选择目标
                return {
                    PlayReq.REQ_TARGET_TO_PLAY: 0,
                    PlayReq.REQ_ENEMY_TARGET: 0
                }
        # 不需要目标
        return {}
    
    def play(self):
        # 检查上回合是否使用过元素
        played_elemental_last_turn = False
        if hasattr(self.controller, 'cards_played_last_turn'):
            played_elemental_last_turn = any(
                hasattr(card, 'race') and card.race == Race.ELEMENTAL 
                for card in self.controller.cards_played_last_turn
            )
        
        if played_elemental_last_turn and self.target:
            # 对选择的目标造成4点伤害
            yield Hit(TARGET, 4)
        else:
            # 随机对一个敌人造成4点伤害
            yield Hit(RANDOM_ENEMY_CHARACTER, 4)


class SC_759:
    """护盾充能器 - Shield Battery
    Gain 6 Armor. Your next Protoss spell costs (2) less.
    
    2费 法师法术
    获得6点护甲值。你的下一张星灵法术牌法力值消耗减少(2)点。
    """
    def play(self):
        # 获得6点护甲值
        yield GainArmor(FRIENDLY_HERO, 6)
        # 下一张星灵法术减费2点
        yield Buff(CONTROLLER, "SC_759e")


class SC_759e:
    """护盾充能器效果 - 下一张星灵法术减费2点"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 给手牌中的星灵法术减费
    auras = [
        Buff(FRIENDLY_HAND + SPELL, "SC_759e2")
    ]
    
    # 使用一张星灵法术后移除此效果
    events = Play(CONTROLLER, SPELL).after(
        lambda self, source, card: Destroy(SELF) if card.id in PROTOSS_SPELL_IDS else None
    )


class SC_759e2:
    """星灵法术减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    @property
    def cost(self, i):
        # 只对星灵法术生效
        if self.owner.id in PROTOSS_SPELL_IDS:
            return -2
        return 0


class SC_760:
    """谐振盘 - Resonance Coil
    Deal $5 damage to a minion. Get a random Protoss spell.
    
    3费 法师法术
    对一个随从造成$5点伤害。随机获取一张星灵法术牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0
    }
    
    def play(self):
        # 对目标造成5点伤害
        yield Hit(TARGET, 5)
        # 随机获取一张星灵法术
        if PROTOSS_SPELL_IDS:
            protoss_spell = self.game.random.choice(PROTOSS_SPELL_IDS)
            yield Give(CONTROLLER, protoss_spell)


# RARE

class GDB_134:
    """阿肯飞翼驾驶员 - Arkwing Pilot
    At the end of your turn, deal 3 damage to a random enemy. Spellburst: Summon an Arkwing Pilot.
    
    7费 4/3 法师随从 - 德莱尼
    在你的回合结束时,随机对一个敌人造成3点伤害。
    法术迸发:召唤一个阿肯飞翼驾驶员。
    """
    race = Race.DRAENEI
    tags = {GameTag.SPELLBURST: True}
    
    # 回合结束时随机对一个敌人造成3点伤害
    events = [
        OWN_TURN_END.on(
            Hit(RANDOM_ENEMY_CHARACTER, 3)
        ),
        # 法术迸发:召唤一个阿肯飞翼驾驶员
        OWN_SPELL_PLAY.on(
            Summon(CONTROLLER, "GDB_134"),
            SetTag(SELF, {GameTag.SPELLBURST: False})
        )
    ]


class GDB_135:
    """聪明的技师 - Ingenious Artificer
    Battlecry: The next Draenei you play refreshes Mana Crystals equal to its Attack.
    
    5费 4/6 法师随从 - 德莱尼
    战吼:你使用的下一个德莱尼会复原等同于其攻击力的法力水晶。
    """
    race = Race.DRAENEI
    
    def play(self):
        # 给控制者添加buff,下一个德莱尼会复原法力水晶
        yield Buff(CONTROLLER, "GDB_135e")


class GDB_135e:
    """聪明的技师效果 - Player Enchantment"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    # 监听德莱尼被打出
    events = Play(CONTROLLER, MINION).after(
        lambda self, source, card: [
            FillMana(CONTROLLER, card.atk) if card.race == Race.DRAENEI else None,
            Destroy(SELF) if card.race == Race.DRAENEI else None
        ]
    )


class GDB_302:
    """吸积炽焰 - Blazing Accretion
    Battlecry: Destroy the top 3 cards of your deck. Any Fire spells or Elementals are drawn instead.
    
    3费 3/1 法师随从 - 元素
    战吼:摧毁你牌库顶的3张牌,其中的火焰法术牌或元素牌会由摧毁改为抽取。
    """
    race = Race.ELEMENTAL
    
    def play(self):
        # 检查牌库顶的3张牌
        for _ in range(3):
            if not self.controller.deck:
                break
            
            top_card = self.controller.deck[0]
            
            # 检查是否是火焰法术或元素
            is_fire_spell = (top_card.type == CardType.SPELL and 
                           hasattr(top_card, 'spell_school') and 
                           top_card.spell_school == SpellSchool.FIRE)
            is_elemental = (top_card.type == CardType.MINION and 
                          top_card.race == Race.ELEMENTAL)
            
            if is_fire_spell or is_elemental:
                # 抽取
                yield Draw(CONTROLLER)
            else:
                # 摧毁
                yield Mill(CONTROLLER)


class SC_758:
    """巨像 - Colossus
    Battlecry: Deal 1 damage to all enemies, twice. (Improved by Protoss spells you cast this game!)
    
    12费 9/4 法师随从 - 机械
    战吼:对所有敌人造成1点伤害,触发两次。
    (在本局对战中你每施放过一个星灵法术都会提升!)
    """
    race = Race.MECHANICAL
    
    def play(self):
        # 计算本局施放的星灵法术数量
        protoss_count = 0
        if hasattr(self.controller, 'protoss_spells_cast_this_game'):
            protoss_count = self.controller.protoss_spells_cast_this_game
        
        # 基础触发2次,每个星灵法术+1次
        times = 2 + protoss_count
        
        # 对所有敌人造成1点伤害,重复times次
        for _ in range(times):
            yield Hit(ENEMY_CHARACTERS, 1)


# EPIC

class GDB_133:
    """袖珍次元 - Pocket Dimension
    Discover a spell. Repeat until you see one for the second time.
    
    4费 法师法术 - 奥术
    发现一张法术牌。重复此效果,直到你再次见到选项中见过的牌。
    
    实现说明:
    - 这个卡牌会不断发现法术,直到发现选项中出现之前见过的法术
    - "见过"指的是在发现选项中出现过,而不是已经选择过
    - 实现时需要记录所有出现在发现选项中的法术ID
    """
    def play(self):
        # 记录所有出现在发现选项中的法术ID
        seen_spell_ids = set()

        # 最多循环20次,防止无限循环
        for iteration in range(20):
            # 创建发现action
            discover_action = Discover(CONTROLLER, RandomSpell())

            # 执行发现 - 这会让玩家选择一张牌
            result = yield discover_action

            if not result:
                break

            # 获取本次发现的所有3个选项
            # discover_action.cards 包含了所有选项
            current_options = getattr(discover_action, 'cards', [])

            # 检查这3个选项中是否有之前见过的
            found_duplicate = False
            for option in current_options:
                option_id = option.id if hasattr(option, 'id') else str(option)
                if option_id in seen_spell_ids:
                    # 找到重复的了,停止循环
                    found_duplicate = True
                    break
                # 记录这个选项
                seen_spell_ids.add(option_id)

            if found_duplicate:
                # 见到重复的了,停止
                break


class GDB_301:
    """超级新星 - Supernova
    Fill your hand with random Fire spells. They cost (1).
    
    8费 法师法术 - 火焰
    用随机火焰法术牌填满你的手牌。这些法术牌的法力值消耗为(1)点。
    """
    def play(self):
        # 计算手牌空位
        hand_space = 10 - len(self.controller.hand)
        
        # 填满手牌
        for _ in range(hand_space):
            # 获取随机火焰法术并设置费用为1
            card = yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.FIRE))
            if card:
                yield Buff(card, "GDB_301e")


class GDB_301e:
    """超级新星费用效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    @property
    def cost(self, i):
        # 设置费用为1
        return 1 - self.owner.data.cost


# LEGENDARY

class GDB_136:
    """大主教哈塔鲁 - Exarch Hataaru
    Battlecry: Discover a spell and reduce its Cost by (1). If you play it this turn, repeat this effect.
    
    5费 5/5 法师随从 - 德莱尼(传说)
    战吼:发现一张法术牌并使其法力值消耗减少(1)点。如果你在本回合使用这张法术牌,重复此效果。
    """
    race = Race.DRAENEI
    
    def play(self):
        # 发现一张法术并减费
        cards = yield Discover(CONTROLLER, RandomSpell())
        
        if not cards:
            return
        
        discovered_card = cards[0]
        
        # 减少1点费用
        yield Buff(discovered_card, "GDB_136e2")
        
        # 添加监听器,如果本回合使用这张牌,重复效果
        yield Buff(CONTROLLER, "GDB_136e", discovered_card_id=discovered_card.id)


class GDB_136e:
    """大主教哈塔鲁重复效果监听器"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discovered_card_id = kwargs.get('discovered_card_id', None)
        self.triggered = False
    
    # 监听法术被打出
    events = [
        Play(CONTROLLER, SPELL).after(
            lambda self, source, card: [
                # 如果是发现的那张牌且本回合使用且未触发过
                DiscoverAndRepeat(source.controller) if (
                    card.id == self.discovered_card_id and 
                    not self.triggered
                ) else None,
                setattr(self, 'triggered', True) if card.id == self.discovered_card_id else None
            ]
        ),
        # 回合结束时移除
        OWN_TURN_END.on(Destroy(SELF))
    ]


def DiscoverAndRepeat(controller):
    """发现法术并减费的辅助函数"""
    def action(source):
        # 发现一张法术
        cards = yield Discover(controller, RandomSpell())
        
        if not cards:
            return
        
        discovered_card = cards[0]
        
        # 减少1点费用
        yield Buff(discovered_card, "GDB_136e2")
        
        # 添加监听器,如果本回合使用这张牌,继续重复
        yield Buff(controller, "GDB_136e", discovered_card_id=discovered_card.id)
    
    return action


class GDB_136e2:
    """大主教哈塔鲁减费效果"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_304:
    """恒星之火萨鲁恩 - Saruun
    Battlecry: Give all Elementals in your deck Fire Spell Damage +1.
    
    6费 7/6 法师随从 - 元素(传说)
    战吼:使你牌库中的所有元素获得火焰法术伤害+1。
    
    实现说明:
    - 这张卡给牌库中的元素添加法术伤害+1
    - 由于核心引擎暂不支持特定法术学派的法术伤害,这里使用通用法术伤害+1
    - 未来可以扩展核心引擎来支持火焰法术专属伤害
    """
    race = Race.ELEMENTAL
    
    def play(self):
        # 给牌库中所有元素添加法术伤害+1
        for card in self.controller.deck:
            if card.type == CardType.MINION and card.race == Race.ELEMENTAL:
                yield Buff(card, "GDB_304e")


class GDB_304e:
    """恒星之火萨鲁恩效果 - 法术伤害+1"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.SPELLPOWER: 1  # 法术伤害+1
    }
    # 注意: 这个buff会对所有法术生效,而不仅仅是火焰法术
    # 这是因为核心引擎暂不支持特定法术学派的法术伤害
    # 未来可以通过扩展核心引擎来实现火焰法术专属伤害
