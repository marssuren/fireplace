"""
深入翡翠梦境 - MAGE
"""
from ..utils import *
from .imbue_helpers import trigger_imbue


# COMMON

class EDR_519:
    """小精灵驾驭者 - Wisprider
    Battlecry: Imbue your Hero Power, then trigger it.
    
    5费 4/4 随从
    战吼：灌注你的英雄技能，然后触发它。
    """
    requirements = {}
    
    def play(self):
        # 触发 Imbue（直接调用，不需要 yield）
        trigger_imbue(self.controller)
        # 触发英雄技能
        # 使用英雄技能的 use 方法
        if self.controller.hero.power:
            for action in self.controller.hero.power.use():
                yield action


class EDR_520:
    """禁忌神龛 - Forbidden Shrine
    Spend all your Mana. Cast a random spell that costs that much.
    
    1费 地标（3生命）
    花费你所有的法力值。施放一个法力值消耗与之相同的随机法术。
    """
    tags = {
        GameTag.CARDTYPE: CardType.LOCATION,
        GameTag.COST: 1,
        GameTag.HEALTH: 3,
    }
    
    def activate(self):
        # 获取当前可用法力值
        available_mana = self.controller.mana
        
        # 花费所有法力值
        yield SpendMana(CONTROLLER, available_mana)
        
        # 施放一个法力值消耗相同的随机法术
        if available_mana > 0:
            yield CastSpell(RandomSpell(cost=available_mana))


class EDR_941:
    """星涌术 - Starsurge
    Deal $1 damage to a minion. (Improved by each friendly minion that died this game.)
    
    3费 法术
    对一个随从造成1点伤害。（在本局对战中每有一个友方随从死亡，伤害+1）
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 基础伤害为1
        base_damage = 1
        # 获取本局对战中死亡的友方随从数量
        friendly_minions_died = getattr(self.controller, 'friendly_minions_died_this_game', 0)
        # 总伤害 = 基础伤害 + 死亡随从数
        total_damage = base_damage + friendly_minions_died
        
        # 造成伤害
        yield Hit(TARGET, total_damage)


class FIR_913:
    """地狱火先锋 - Inferno Herald
    After you cast a Fire spell, get a random Elemental and reduce its Cost by (3).
    
    4费 3/6 元素
    在你施放一个火焰法术后，随机获取一张元素牌，其法力值消耗减少(3)点。
    """
    # 监听火焰法术施放事件
    events = OWN_SPELL_PLAY.after(
        lambda self, source, target: source.spell_school == SpellSchool.FIRE,
        lambda self, source, target: [
            # 随机获取一张元素牌
            RandomCard(CONTROLLER, race=Race.ELEMENTAL),
            # 减少3费
            Buff(Find(CONTROLLER_HAND + FRIENDLY + LAST_CARD_PLAYED), "FIR_913e")
        ]
    )


# RARE

class EDR_804:
    """巫卜 - Divination
    Destroy a friendly Wisp to draw 3 cards.
    
    2费 奥术法术
    消灭一个友方小精灵以抽3张牌。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 检查目标是否为小精灵（Wisp 的 ID 为 CS2_231）
        if TARGET.id == "CS2_231":
            # 消灭目标
            yield Destroy(TARGET)
            # 抽3张牌
            yield Draw(CONTROLLER) * 3


class EDR_872:
    """生命火花 - Spark of Life
    Choose One - Discover a Mage spell; or Discover a Druid spell.
    
    1费 法术
    抉择：发现一张法师法术牌；或者发现一张德鲁伊法术牌。
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("EDR_872a", "EDR_872b")


# EDR_872a 和 EDR_872b 已在 tokens.py 中定义


class EDR_940:
    """喜悦的枭兽 - Merry Moonkin
    At the end of your turn, gain 1 Armor. Repeat for each Wisp you control.
    
    4费 3/6 随从
    在你的回合结束时，获得1点护甲值。你每控制一个小精灵，重复一次。
    """
    # 监听回合结束事件
    events = OWN_TURN_END.on(
        lambda self: [
            # 基础获得1点护甲
            GainArmor(FRIENDLY_HERO, 1),
            # 每个小精灵额外获得1点护甲
            GainArmor(FRIENDLY_HERO, 1) * Count(FRIENDLY_MINIONS + ID("CS2_231"))
        ]
    )


class FIR_910:
    """灼烧之风 - Scorching Winds
    Deal $3 damage. Discard a random Fire spell to deal $3 more.
    
    3费 火焰法术
    造成3点伤害。随机弃一张火焰法术牌以再造成3点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)
        
        # 检查手牌中是否有火焰法术
        fire_spells = [c for c in self.controller.hand if c.type == CardType.SPELL and c.spell_school == SpellSchool.FIRE]
        
        if fire_spells:
            # 随机弃一张火焰法术
            import random
            discarded = random.choice(fire_spells)
            yield Discard(discarded)
            # 再造成3点伤害
            yield Hit(TARGET, 3)


class FIR_911:
    """焚火林地 - Smoldering Grove
    Draw {0} card. (Upgrades each turn, but discards after {1}!)
    
    2费 火焰法术
    抽1张牌。（每回合升级，但3回合后弃掉此牌！）
    """
    requirements = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turns_in_hand = 0
    
    def play(self):
        # 抽牌数量 = 持有回合数 + 1
        draw_count = self.turns_in_hand + 1
        
        # 抽牌
        yield Draw(CONTROLLER) * draw_count
    
    class Hand:
        # 每回合开始时增加持有回合数
        events = OWN_TURN_BEGIN.on(
            lambda self: [
                # 增加持有回合数
                Buff(SELF, "FIR_911e"),
                # 检查是否达到3回合，如果是则弃掉此牌
                Discard(SELF) if self.owner.turns_in_hand >= 3 else None
            ]
        )


# EPIC

class EDR_871:
    """灵体采集者 - Spirit Gatherer
    Battlecry: Get a Wisp. Imbue your Hero Power.
    
    费用未知 随从
    战吼：获取一张小精灵牌。灌注你的英雄技能。
    """
    requirements = {}
    
    def play(self):
        # 获取一张小精灵牌（Wisp ID: CS2_231）
        yield Give(CONTROLLER, "CS2_231")
        # 触发 Imbue
        trigger_imbue(self.controller)


class EDR_874:
    """星体平衡 - Stellar Balance
    Get a Moonfire and a Starfire. Give them Spell Damage +1.
    
    2费 奥术法术
    获取一张月火术和一张星火术，使其获得法术伤害+1。
    """
    requirements = {}
    
    def play(self):
        # 获取月火术（Moonfire ID: CS2_008）
        yield Give(CONTROLLER, "CS2_008")
        # 给予法术伤害+1
        yield Buff(Find(CONTROLLER_HAND + FRIENDLY + LAST_CARD_PLAYED), "EDR_874e")
        
        # 获取星火术（Starfire ID: CS2_032）
        yield Give(CONTROLLER, "CS2_032")
        # 给予法术伤害+1
        yield Buff(Find(CONTROLLER_HAND + FRIENDLY + LAST_CARD_PLAYED), "EDR_874e")


# LEGENDARY

class EDR_430:
    """艾森娜 - Aessina
    Battlecry: If 20 friendly minions have died this game, deal 20 damage split among all enemies.
    
    8费 6/8 亡灵
    战吼：如果在本局对战中已有20个友方随从死亡，造成20点伤害，随机分配到所有敌人身上。
    """
    requirements = {}
    
    def play(self):
        # 检查是否有20个友方随从死亡
        friendly_minions_died = getattr(self.controller, 'friendly_minions_died_this_game', 0)
        
        if friendly_minions_died >= 20:
            # 造成20点伤害，随机分配到所有敌人
            yield Hit(ENEMY_CHARACTERS, 20, distribute=True)


class EDR_517:
    """亢祖 - Q'onzu
    Battlecry: Discover a spell. Choose to keep it or put it on top of your opponent's deck.
    
    3费 3/4 野兽 (法师传说随从)
    战吼：发现一张法术牌。选择保留它或将其置于你对手的牌库顶。
    
    实现说明:
    - 第一步: 发现一张法术牌 (从3张中选1张)
    - 第二步: 选择保留它或放到对手牌库顶 (玩家/AI选择)
    """
    requirements = {}
    
    def play(self):
        # 第一步: 发现一张法术牌
        discovered = yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.SPELL,
            count=3
        ))
        
        # 如果成功发现了法术牌
        if discovered:
            # 第二步: 让玩家/AI选择保留或放到对手牌库顶
            # 创建两个选项
            choice = yield GenericChoice(CONTROLLER, ["EDR_517_keep", "EDR_517_topdeck"])
            
            if choice and choice.id == "EDR_517_topdeck":
                # 选择放到对手牌库顶
                # 将法术从手牌移除并放到对手牌库顶
                discovered.zone = Zone.SETASIDE
                yield PutOnTop(OPPONENT, discovered)
            # 否则保留在手牌中(什么都不做)


