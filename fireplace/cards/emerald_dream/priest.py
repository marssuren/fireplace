"""
深入翡翠梦境 - PRIEST
"""
from ..utils import *
from .imbue_helpers import trigger_imbue


# COMMON

class EDR_449:
    """月翼信使 - Lunarwing Messenger
    Lifesteal. Battlecry: Imbue your Hero Power.
    
    2费 3/3 野兽
    吸血。战吼:灌注你的英雄技能。
    """
    tags = {
        GameTag.LIFESTEAL: True,
    }
    requirements = {}
    
    def play(self):
        # 战吼:灌注英雄技能
        trigger_imbue(self.controller)


class EDR_460:
    """新月祈愿 - Wish of the New Moon
    Deal $6 damage to a minion. (Cast 3 spells to gain Lifesteal.)
    
    3费 奥术法术
    对一个随从造成$6点伤害。(施放3个法术后获得吸血。)
    
    实现说明:
    - 使用 Hand Aura 动态检查本回合施放的法术数量
    - 当施放3个法术后,本牌获得吸血效果
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 检查是否已施放3个法术(包括本牌)
        # 注意:本牌施放时 spells_played_this_turn 已经+1
        has_lifesteal = self.controller.spells_played_this_turn >= 3
        
        # 造成伤害
        if has_lifesteal:
            # 临时设置吸血标签
            self.tags[GameTag.LIFESTEAL] = True
            yield Hit(TARGET, 6)
            # 移除临时标签
            self.tags[GameTag.LIFESTEAL] = False
        else:
            # 普通伤害
            yield Hit(TARGET, 6)
    
    class Hand:
        """手牌光环:显示是否已获得吸血"""
        def _update_lifesteal(self):
            # 检查是否已施放3个法术
            if self.owner.controller.spells_played_this_turn >= 3:
                # 临时添加吸血标签用于显示
                self.owner.tags[GameTag.LIFESTEAL] = True
            else:
                # 移除吸血标签
                self.owner.tags[GameTag.LIFESTEAL] = False
        
        # 初始化时更新一次
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._update_lifesteal()
        
        events = (
            OWN_SPELL_PLAY.after(lambda self, *args: self._update_lifesteal()),
            OWN_TURN_BEGIN.on(lambda self: self._update_lifesteal()),
        )


class EDR_472:
    """轮回编织者 - Weaver of the Cycle
    Battlecry: If you're holding a spell that costs (5) or more, deal 3 damage.
    
    3费 3/3 随从
    战吼:如果你的手牌中有法力值消耗大于或等于(5)点的法术牌,则造成3点伤害。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    
    def play(self):
        # 检查手牌中是否有5费或更高的法术牌
        has_expensive_spell = any(
            c.type == CardType.SPELL and c.cost >= 5
            for c in self.controller.hand
        )
        
        if has_expensive_spell and TARGET:
            # 造成3点伤害
            yield Hit(TARGET, 3)


class FIR_777:
    """卡多雷精魂 - Spirit of the Kaldorei
    Taunt, Lifesteal. Battlecry: If you used your Hero Power this turn, gain +3/+3.
    
    2费 1/3 亡灵
    嘲讽。吸血。战吼:如果你在本回合中使用过英雄技能,获得+3/+3。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
    }
    requirements = {}
    
    def play(self):
        # 检查本回合是否使用过英雄技能
        # 使用 times_hero_power_used_this_game 和上回合的值对比
        # 或者检查英雄技能的 exhausted 状态
        if self.controller.hero.power and self.controller.hero.power.exhausted:
            # 获得+3/+3
            yield Buff(SELF, "FIR_777e")


class FIR_916:
    """焚火飞升 - Smoldering Ascent
    Deal ${0} damage to all enemy minions. (Upgrades each turn, but discards after {1}!)
    
    2费 火焰法术
    对所有敌方随从造成$X点伤害。(每回合升级,但本牌会在X回合后弃掉!)
    X = 持有回合数 + 1
    
    实现说明:
    - 初始效果为造成1点伤害
    - 每回合开始时升级:2点、3点
    - 第3回合开始时(持有2回合后)自动弃掉
    - 参考 FIR_914 (焚火之力) 的实现
    """
    requirements = {}
    
    def play(self):
        # 获取持有回合数(初始为0,表示刚抽到)
        turns_held = getattr(self, 'turns_held', 0)
        # 造成伤害(至少1点)
        damage = turns_held + 1
        yield Hit(ENEMY_MINIONS, damage)
    
    class Hand:
        # 每回合开始时增加持有回合数并检查是否弃牌
        def _on_turn_begin(self):
            # 增加持有回合数
            self.owner.turns_held = getattr(self.owner, 'turns_held', 0) + 1
            # 如果持有3回合,弃掉此牌
            if self.owner.turns_held >= 3:
                yield Discard(SELF)
        
        events = OWN_TURN_BEGIN.on(_on_turn_begin)


# RARE

class EDR_462:
    """逐月幼龙 - Selenic Drake
    Elusive. At the end of your turn, get a random Dragon.
    
    4费 3/4 龙
    扰魔。在你的回合结束时,随机获取一张龙牌。
    """
    tags = {
        GameTag.ELUSIVE: True,
    }
    
    # 回合结束时获取随机龙牌
    events = OWN_TURN_END.on(
        Give(CONTROLLER, RandomCollectible(race=Race.DRAGON))
    )


class EDR_463:
    """暮光侵扰 - Twilight Influence
    Choose One - Destroy a minion with 3 or less Attack; or Summon a random 2-Cost minion.
    
    3费 暗影法术
    抉择:消灭一个攻击力小于或等于3点的随从;或者随机召唤一个法力值消耗为(2)的随从。
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ["EDR_463a", "EDR_463b"]


class EDR_463a:
    """暮光侵扰 - 选项A
    Destroy a minion with 3 or less Attack
    
    消灭一个攻击力小于或等于3点的随从。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_MAX_ATTACK: 3,
    }
    play = Destroy(TARGET)


class EDR_463b:
    """暮光侵扰 - 选项B
    Summon a random 2-Cost minion
    
    随机召唤一个法力值消耗为(2)的随从。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    play = Summon(CONTROLLER, RandomMinion(cost=2))


class EDR_970:
    """卡多雷女祭司 - Kaldorei Priestess
    Battlecry: Give all enemy minions -2 Attack until your next turn. Imbue your Hero Power.
    
    3费 3/3 随从
    战吼:直到你的下个回合,使所有敌方随从获得-2攻击力。灌注你的英雄技能。
    """
    requirements = {}
    
    def play(self):
        # 给所有敌方随从-2攻击力
        yield Buff(ENEMY_MINIONS, "EDR_970e")
        # 触发 Imbue
        trigger_imbue(self.controller)


class FIR_918:
    """新月辉光 - Light of the New Moon
    Give a minion +3/+3. (Cast 3 spells to return this to your hand when played.)
    
    3费 奥术法术
    使一个随从获得+3/+3。(施放3个法术,即可在使用时将本牌移回你的手牌)
    
    实现说明:
    - 施放时检查是否已施放3个法术(包括本牌)
    - 如果是,给玩家添加一个 buff,在本牌施放后将其返回手牌
    - 参考 VAC_427 (甜筒殡淇淋) 的实现
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 给予目标+3/+3
        yield Buff(TARGET, "FIR_918e")
        
        # 检查是否已施放3个法术(包括本牌)
        # 注意:本牌施放时 spells_played_this_turn 已经+1
        if self.controller.spells_played_this_turn >= 3:
            # 将本牌返回手牌
            # 使用 Give 创建一个新的复制
            yield Give(CONTROLLER, self.id)


# EPIC

class EDR_461:
    """新月仪式 - Ritual of the New Moon
    Summon two random 3-Cost minions. (Cast 3 spells to summon 6-Cost minions instead.)
    
    5费 奥术法术
    随机召唤两个法力值消耗为(3)的随从。(施放3个法术后改为召唤法力值消耗为(6)的随从。)
    
    实现说明:
    - 检查本回合施放的法术数量
    - 如果已施放3个法术(包括本牌),召唤6费随从
    - 否则召唤3费随从
    """
    requirements = {}
    
    def play(self):
        # 检查是否已施放3个法术(包括本牌)
        # 注意:本牌施放时 spells_played_this_turn 已经+1
        if self.controller.spells_played_this_turn >= 3:
            # 召唤两个6费随从
            yield Summon(CONTROLLER, RandomMinion(cost=6)) * 2
        else:
            # 召唤两个3费随从
            yield Summon(CONTROLLER, RandomMinion(cost=3)) * 2


class EDR_476:
    """月亮井 - Moonwell
    Deal $4 damage to all enemy characters. Restore #4 Health to all friendly characters.
    
    7费 法术
    对所有敌方角色造成$4点伤害。为所有友方角色恢复#4点生命值。
    """
    requirements = {}
    
    def play(self):
        # 对所有敌方角色造成4点伤害
        yield Hit(ENEMY_CHARACTERS, 4)
        # 为所有友方角色恢复4点生命值
        yield Heal(FRIENDLY_CHARACTERS, 4)


# LEGENDARY

class EDR_464:
    """泰兰德 - Tyrande
    Battlecry: The next 3 spells you play cast twice.
    
    4费 5/4 随从
    战吼:你使用的接下来3个法术会施放两次。
    
    实现说明:
    - 给玩家添加一个 buff,追踪剩余的双倍施放次数
    - 每次施放法术时,如果有剩余次数,则重复施放法术的play()方法并递减计数
    - 注意:这是简化实现,直接调用play()方法。完整实现需要处理目标选择等复杂情况
    - 对于无目标法术和AOE法术,这个实现是准确的
    - 对于有目标法术,可能需要使用相同的目标或重新选择目标
    """
    requirements = {}
    
    def play(self):
        # 给玩家添加泰兰德效果
        yield Buff(CONTROLLER, "EDR_464e")


class EDR_895:
    """艾维娜,艾露恩钦选者 - Aviana, Elune's Chosen
    Battlecry: Start a three turn lunar cycle. When the Full Moon rises, your cards cost (1) this game.
    
    9费 7/11 随从
    战吼:开启为期三回合的月相演变。当满月升起时,在本局对战中你的卡牌法力值消耗为(1)点。
    
    实现说明:
    - 给玩家添加一个 buff,追踪月相演变进度
    - 月相:新月(0) -> 上弦月(1) -> 满月(2)
    - 每回合开始时推进月相
    - 当满月升起时(第3回合开始),所有卡牌费用变为1
    - 参考 titans/paladin.py - TTN_854e (持续回合数机制)
    """
    requirements = {}
    
    def play(self):
        # 给玩家添加月相演变效果
        yield Buff(CONTROLLER, "EDR_895e")

