"""
决战荒芜之地 - DEMONHUNTER
"""
from ..utils import *


# COMMON

class WW_403:
    """袋底藏沙 - Pocket Sand
    造成$3点伤害。<b>快枪:</b>你的对手的下一张牌法力值消耗增加(1)点。
    """
    # Type: SPELL | Cost: 2 | Rarity: COMMON | Mechanics: QUICKDRAW
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    
    def play(self):
        # 造成3点伤害
        yield Hit(self.target, 3)
        
        # 快枪：本回合获得并立即使用时触发
        if self.drawn_this_turn:
            yield Buff(OPPONENT, "WW_403e")


class WW_403e:
    """对手下一张牌+1费"""
    events = Play(CONTROLLER).on(
        Buff(Play.CARD, "WW_403e2"),
        Destroy(SELF)
    )


class WW_403e2:
    """费用+1"""
    tags = {GameTag.COST: 1}


class WW_404:
    """绿洲歹徒 - Oasis Outlaws
    <b>发现</b>一张纳迦牌。如果你在持有本牌时使用过纳迦牌，其法力值消耗减少(1)点。
    """
    # Type: SPELL | Cost: 1 | Rarity: COMMON | Mechanics: DISCOVER
    # 需要追踪在手牌时是否使用过纳迦
    
    class Hand:
        # 在手牌时监听纳迦使用
        events = Play(CONTROLLER, NAGA).on(
            lambda self: setattr(self, 'naga_played_while_holding', True)
        )
    
    def play(self):
        # 发现纳迦牌
        # 使用 getattr 安全访问属性，因为法术牌没有自定义 __init__
        if getattr(self, 'naga_played_while_holding', False):
            # 减少1费
            yield Discover(CONTROLLER, RandomCollectible(race=Race.NAGA)).then(
                Buff(Discover.CARD, "WW_404e")
            )
        else:
            yield Discover(CONTROLLER, RandomCollectible(race=Race.NAGA))


class WW_404e:
    """费用-1"""
    tags = {GameTag.COST: -1}


class WW_406:
    """午夜啸狼 - Midnight Wolf
    <b>突袭</b>。<b>流放:</b>召唤一个本随从的复制。
    """
    # Type: MINION | Cost: 6 | Rarity: COMMON | Stats: 6/6 | Race: BEAST | Mechanics: OUTCAST, RUSH
    outcast = Summon(CONTROLLER, ExactCopy(SELF))


# RARE

class DEEP_012:
    """影石潜伏者 - Shadestone Skulker
    <b>突袭</b>。<b>战吼:</b>夺取你的武器并获得其属性值。<b>亡语:</b>还回武器。
    """
    # Type: MINION | Cost: 1 | Rarity: RARE | Stats: 1/1 | Race: ELEMENTAL | Mechanics: BATTLECRY, DEATHRATTLE, RUSH
    # 使用 Bounce 来还回武器到手牌，保留耐久度
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stored_weapon = None
    
    def play(self):
        weapon = self.controller.weapon
        if weapon:
            # 保存武器引用
            self.stored_weapon = weapon
            
            # 获得武器的属性
            yield Buff(SELF, "DEEP_012e", atk=weapon.atk, max_health=weapon.durability)
            
            # 移除武器（暂时）
            yield Destroy(weapon)
    
    def deathrattle(self):
        # 还回武器到手牌（Bounce会保留耐久度）
        if hasattr(self, 'stored_weapon') and self.stored_weapon:
            yield Bounce(self.stored_weapon)


class DEEP_012e:
    """属性增益"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}


class DEEP_013:
    """邪能陷隙 - Fel Fissure
    对所有随从造成$2点伤害。在你的下个回合开始时，再对所有随从造成$2点伤害。
    """
    # Type: SPELL | Cost: 4 | Rarity: RARE
    
    def play(self):
        # 立即造成2点伤害
        yield Hit(ALL_MINIONS, 2)
        # 给玩家添加buff，下回合开始时再次造成伤害
        yield Buff(CONTROLLER, "DEEP_013e")


class DEEP_013e:
    """延迟伤害效果"""
    events = OWN_TURN_BEGIN.on(
        Hit(ALL_MINIONS, 2),
        Destroy(SELF)
    )


class WW_405:
    """迅疾连射 - Fan the Hammer
    造成$6点伤害，分配到生命值最低的敌人身上。
    """
    # Type: SPELL | Cost: 4 | Rarity: RARE | Mechanics: ImmuneToSpellpower
    # 分配伤害到最低生命值的敌人
    
    def play(self):
        # 造成6点伤害，分配到最低生命值的敌人
        for i in range(6):
            # 每次找最低生命值的敌人
            targets = sorted(
                [t for t in self.game.board if t.controller == self.controller.opponent and t.health > 0],
                key=lambda x: x.health
            )
            if targets:
                yield Hit(targets[0], 1)


class WW_407:
    """焦渴的亡命徒 - Parched Desperado
    <b>战吼:</b>如果你在持有本牌时施放过法术，使你的英雄在本回合中获得+3攻击力。
    """
    # Type: MINION | Cost: 2 | Rarity: RARE | Stats: 3/2 | Race: NAGA | Mechanics: BATTLECRY
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_cast_while_holding = False
    
    class Hand:
        # 在手牌时监听法术施放
        events = Play(CONTROLLER, SPELL).on(
            lambda self: setattr(self.owner, 'spell_cast_while_holding', True)
        )
    
    def play(self):
        if self.spell_cast_while_holding:
            yield Buff(FRIENDLY_HERO, "WW_407e")


class WW_407e:
    """英雄+3攻击力"""
    tags = {GameTag.ATK: 3}
    events = OWN_TURN_END.on(Destroy(SELF))


class WW_409:
    """装填弹膛 - Load the Chamber
    造成$2点伤害。你的下一张纳迦牌、邪能法术和武器的法力值消耗减少(1)点。
    """
    # Type: SPELL | Cost: 3 | Rarity: RARE
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True}
    
    def play(self):
        # 造成2点伤害
        yield Hit(self.target, 2)
        # 给玩家添加3个buff，分别为下一张纳迦、邪能法术、武器减费
        yield Buff(CONTROLLER, "WW_409e1")  # 纳迦
        yield Buff(CONTROLLER, "WW_409e2")  # 邪能法术
        yield Buff(CONTROLLER, "WW_409e3")  # 武器


class WW_409e1:
    """下一张纳迦-1费"""
    events = Play(CONTROLLER, NAGA).on(
        Buff(Play.CARD, "WW_409e_cost"),
        Destroy(SELF)
    )


class WW_409e2:
    """下一张邪能法术-1费"""
    events = Play(CONTROLLER, SPELL + FEL).on(
        Buff(Play.CARD, "WW_409e_cost"),
        Destroy(SELF)
    )


class WW_409e3:
    """下一张武器-1费"""
    events = Play(CONTROLLER, WEAPON).on(
        Buff(Play.CARD, "WW_409e_cost"),
        Destroy(SELF)
    )


class WW_409e_cost:
    """费用-1"""
    tags = {GameTag.COST: -1}


# EPIC

class WW_402:
    """盲眼神射手 - Blindeye Sharpshooter
    在你使用一张纳迦牌后，对一个随机敌人造成2点伤害并抽一张法术牌。<i>(然后切换！)</i>
    """
    # Type: MINION | Cost: 3 | Rarity: EPIC | Stats: 1/3 | Race: NAGA | Mechanics: TRIGGER_VISUAL
    # "切换"意味着效果会交替：造成伤害->抽法术 -> 造成伤害->抽法术
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_effect_is_damage = True  # True=伤害, False=抽牌
    
    def naga_trigger(self):
        """纳迦触发效果：交替执行伤害和抽牌"""
        if self.next_effect_is_damage:
            # 造成2点伤害
            yield Hit(RANDOM(ENEMY_CHARACTERS), 2)
        else:
            # 抽一张法术牌
            yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
        # 切换效果
        self.next_effect_is_damage = not self.next_effect_is_damage
    
    events = Play(CONTROLLER, NAGA).after(
        lambda self: self.naga_trigger()
    )


class WW_408:
    """机器调酒师 - Bartend-O-Bot
    <b>战吼:</b>抽一张具有<b>流放</b>效果的牌并将其移动到你的手牌最左侧。
    """
    # Type: MINION | Cost: 2 | Rarity: EPIC | Stats: 3/1 | Race: MECHANICAL | Mechanics: BATTLECRY
    
    def play(self):
        # 从牌库中找到流放牌并抽取
        outcast_cards = [c for c in self.controller.deck if hasattr(c, 'outcast')]
        if outcast_cards:
            card = self.game.random.choice(outcast_cards)
            # 抽这张牌
            drawn = yield Draw(CONTROLLER, card)
            # 将其移动到手牌最左侧
            if drawn and drawn[0] in self.controller.hand:
                self.controller.hand.remove(drawn[0])
                self.controller.hand.insert(0, drawn[0])


# LEGENDARY

class WW_400:
    """蛇眼 - Snake Eyes
    <b>战吼:</b>投掷两个骰子，然后<b>发现</b>两张对应费用的牌。<i>(投出相同点数可额外<b>发现</b>一次！)</i>
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 2/4 | Race: NAGA | Mechanics: BATTLECRY, DISCOVER
    
    def play(self):
        # 投掷两个骰子
        dice1 = self.game.random.randint(1, 6)
        dice2 = self.game.random.randint(1, 6)
        
        # 发现对应费用的牌(使用cost_min和cost_max来精确匹配费用)
        yield Discover(CONTROLLER, RandomCollectible(cost_min=dice1, cost_max=dice1))
        yield Discover(CONTROLLER, RandomCollectible(cost_min=dice2, cost_max=dice2))
        
        # 如果投出相同点数,额外发现一次
        if dice1 == dice2:
            yield Discover(CONTROLLER, RandomCollectible(cost_min=dice1, cost_max=dice1))


class WW_401:
    """枪手库尔特鲁斯 - Gunslinger Kurtrus
    <b>战吼:</b>如果你的套牌里没有相同的牌，向敌方手牌中的随从开枪六次，每次造成2点伤害。
    """
    # Type: MINION | Cost: 5 | Rarity: LEGENDARY | Stats: 4/6 | Mechanics: BATTLECRY
    
    # 使用 FindDuplicates 评估器检查无重复套牌
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    
    def play(self):
        # 检查是否为无重复套牌
        if self.powered_up:
            # 向敌方手牌中的随从开枪6次
            for i in range(6):
                enemy_hand_minions = [c for c in self.controller.opponent.hand if c.type == CardType.MINION]
                if enemy_hand_minions:
                    target = self.game.random.choice(enemy_hand_minions)
                    yield Hit(target, 2)


