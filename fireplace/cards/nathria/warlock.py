"""纳斯利亚堡的悬案（Murder at Castle Nathria）卡牌实现"""
from ..utils import *


class MAW_000:
    """Imp-oster - 冒牌小鬼
    <b>Battlecry:</b> Choose a friendly Imp. Transform into a copy of it.
    <b>战吼：</b>选择一个友方小鬼。变形成为它的一个复制。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON,  # 小鬼是恶魔种族
    }
    
    def play(self):
        # 变形为目标小鬼的复制
        if TARGET:
            yield Morph(SELF, ExactCopy(TARGET))


class MAW_001:
    """Arson Accusation - 纵火指控
    Choose a minion. Destroy it after your hero takes damage.
    选择一个随从。在你的英雄受到伤害后，消灭它。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 给目标添加标记
        yield Buff(TARGET, "MAW_001e")


class MAW_001e:
    """Arson Accusation Mark - 纵火指控标记"""
    # 监听己方英雄受到伤害
    # Damage 事件的 on 参数: (source, target, amount, source_entity)
    def _check_and_destroy(self, source, target, amount, source_entity=None):
        # 如果受伤的是己方英雄
        if target.controller == self.controller:
            # 消灭被标记的随从
            yield Destroy(OWNER)
    
    events = Damage(FRIENDLY_HERO).on(_check_and_destroy)


class MAW_002:
    """Habeas Corpses - 尸身保护令
    <b>Discover</b> a friendly minion to resurrect and give it <b>Rush</b>.
It dies at the end of turn.
    <b>发现</b>一个友方随从并将其复活，使其获得<b>突袭</b>。在回合结束时，其死亡。
    """
    def play(self):
        # 从死亡的友方随从中发现一个
        dead_minions = list(FRIENDLY + KILLED + MINION).eval(self.game, self)
        if dead_minions:
            # 发现
            choice = yield Discover(CONTROLLER, dead_minions)
            if choice:
                # 复活
                minion = yield Summon(CONTROLLER, Copy(choice[0]))
                if minion:
                    # 给予突袭
                    yield Buff(minion, "MAW_002e")


class MAW_002e:
    """Habeas Corpses Effect - 尸身保护令效果"""
    # 给予突袭
    tags = {GameTag.RUSH: True}
    
    # 回合结束时死亡
    events = TURN_END.on(Destroy(OWNER))


class REV_239:
    """Suffocating Shadows - 窒息暗影
    [x]When you play or 
discard this, destroy a 
random enemy minion.
    当你打出或弃掉该牌时，随机消灭一个敌方随从。
    """
    def play(self):
        # 打出时：消灭随机敌方随从
        yield Destroy(RANDOM(ENEMY_MINIONS))
    
    def discard(self):
        # 弃掉时：消灭随机敌方随从
        yield Destroy(RANDOM(ENEMY_MINIONS))


class REV_240:
    """Tome Tampering - 篡改卷宗
    [x]Shuffle 1-Cost 
copies of cards in your 
hand into your deck, 
then discard your hand.
    将你手牌中所有卡牌的1费复制洗入你的牌库，然后弃掉你的手牌。
    """
    def play(self):
        # 复制手牌并洗入牌库
        for card in list(FRIENDLY_HAND.eval(self.game, self)):
            # 创建1费复制
            copy_card = yield Copy(card, cost=1)
            if copy_card:
                yield Shuffle(CONTROLLER, copy_card)
        
        # 弃掉手牌
        yield Discard(FRIENDLY_HAND)


class REV_242:
    """Flustered Librarian - 慌乱的图书管理员
    Has +1 Attack for each
Imp you control.
    你每控制一个小鬼，其便获得+1攻击力。
    """
    # 动态攻击力：使用 Aura 而不是 lambda
    # 计算小鬼数量并设置攻击力
    @property
    def atk(self):
        # 基础攻击力 + 小鬼数量
        base_atk = 2  # 假设基础攻击力是2
        imp_count = len([m for m in self.controller.field if Race.DEMON in m.races])
        return base_atk + imp_count


class REV_244:
    """Mischievous Imp - 调皮的小鬼
    <b>Battlecry:</b> Summon a copy of this. <b>Infuse (3):</b> Summon two copies instead.
    <b>战吼：</b>召唤一个该随从的复制。<b>注能(3)：</b>改为召唤两个复制。
    """
    infuse = 3
    
    def play(self):
        # 根据是否注能，召唤不同数量的复制
        count = 2 if self.infused else 1
        for i in range(count):
            yield Summon(CONTROLLER, Copy(SELF))


class REV_245:
    """Impending Catastrophe - 灾祸降临
    Draw a card. Repeat for each Imp you control.
    抽一张牌。你每控制一个小鬼，便重复一次。
    """
    def play(self):
        # 计算小鬼数量（+1是因为至少抽1张）
        imp_count = len([m for m in self.controller.field if Race.DEMON in m.races]) + 1
        
        # 抽牌
        for i in range(imp_count):
            yield Draw(CONTROLLER)


class REV_371:
    """Vile Library - 邪恶图书馆
    Give a friendly minion +1/+1. Repeat for each Imp you control.
    使一个友方随从获得+1/+1。你每控制一个小鬼，便重复一次。
    """
    # LOCATION 地标
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def activate(self):
        # 计算小鬼数量（+1是因为至少buff一次）
        imp_count = len([m for m in self.controller.field if Race.DEMON in m.races]) + 1
        
        # 给予buff
        if TARGET:
            for i in range(imp_count):
                yield Buff(TARGET, "REV_371e")


class REV_371e:
    """Vile Library Buff - 邪恶图书馆增益"""
    atk = 1
    max_health = 1


class REV_372:
    """Shadow Waltz - 暗影华尔兹
    Summon a 3/5 Shadow with <b>Taunt</b>. If a minion died this turn, summon another.
    召唤一个3/5并具有<b>嘲讽</b>的暗影。如果在本回合中有随从死亡，再召唤一个。
    """
    def play(self):
        # 召唤第一个暗影
        yield Summon(CONTROLLER, "REV_372t")
        
        # 检查本回合是否有随从死亡
        # 使用核心追踪的 minions_killed_this_turn 属性
        if hasattr(self.controller, 'minions_killed_this_turn') and self.controller.minions_killed_this_turn > 0:
            # 召唤第二个暗影
            yield Summon(CONTROLLER, "REV_372t")


class REV_372t:
    """Shadow - 暗影"""
    # Token: 3/5 嘲讽
    tags = {GameTag.TAUNT: True}


class REV_373:
    """Lady Darkvein - 暗脉女勋爵
    <b>Battlecry:</b> Summon two
2/1 Shades. Each gains
a <b>Deathrattle</b> to cast your 
last Shadow spell.
    <b>战吼:</b>召唤两个2/1的阴影。每个都获得一个<b>亡语</b>，施放你的上一个暗影法术。
    """
    def play(self):
        # 召唤两个阴影
        shade1 = yield Summon(CONTROLLER, "REV_373t")
        shade2 = yield Summon(CONTROLLER, "REV_373t")
        
        # 给每个阴影添加亡语
        # 获取上一个暗影法术（使用核心追踪的属性）
        if hasattr(self.controller, 'last_shadow_spell') and self.controller.last_shadow_spell:
            spell_id = self.controller.last_shadow_spell if isinstance(self.controller.last_shadow_spell, str) else self.controller.last_shadow_spell.id
            if shade1:
                yield Buff(shade1, "REV_373e", spell_id=spell_id)
            if shade2:
                yield Buff(shade2, "REV_373e", spell_id=spell_id)


class REV_373t:
    """Shade - 阴影"""
    # Token: 2/1
    pass


class REV_373e:
    """Lady Darkvein Deathrattle - 暗脉女勋爵亡语"""
    def __init__(self, *args, spell_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id
    
    def deathrattle(self):
        # 施放储存的暗影法术
        if self.spell_id:
            # 创建法术的复制并施放
            spell_copy = self.controller.card(self.spell_id)
            yield CastSpell(spell_copy)


class REV_374:
    """Shadowborn - 影裔魔
    <b>Deathrattle:</b> Reduce the Cost of the highest Cost Shadow spell in your hand by (3).
    <b>亡语：</b>使你手牌中法力值消耗最高的暗影法术的法力值消耗减少（3）点。
    """
    def deathrattle(self):
        # 找到手牌中费用最高的暗影法术
        # 暗影法术：具有 SHADOW 学派的法术
        shadow_spells = [
            card for card in self.controller.hand 
            if card.type == CardType.SPELL and hasattr(card, 'spell_school') 
            and card.spell_school == SpellSchool.SHADOW
        ]
        
        if shadow_spells:
            # 找到费用最高的
            highest_cost_spell = max(shadow_spells, key=lambda c: c.cost)
            # 减费3
            yield Buff(highest_cost_spell, "REV_374e")


class REV_374e:
    """Shadowborn Effect - 影裔魔效果"""
    class Hand:
        cost = -3


class REV_835:
    """Imp King Rafaam - 小鬼大王拉法姆
    <b>Battlecry:</b> Resurrect
four friendly Imps.
<b>Infuse (5):</b> Give your
Imps +2/+2.
    <b>战吼:</b>复活四个友方小鬼。<b>注能(5):</b>使你的小鬼获得+2/+2。
    """
    infuse = 5
    
    def play(self):
        # 复活4个小鬼
        # 正确使用选择器
        dead_minions = list((FRIENDLY + KILLED + MINION).eval(self.game, self))
        dead_imps = [card for card in dead_minions if Race.DEMON in card.races]
        
        # 随机选择4个
        if dead_imps:
            imps_to_resurrect = self.game.random.sample(dead_imps, min(4, len(dead_imps)))
            for imp in imps_to_resurrect:
                yield Summon(CONTROLLER, Copy(imp))
        
        # 如果已注能，给所有小鬼+2/+2
        if self.infused:
            for minion in list(FRIENDLY_MINIONS.eval(self.game, self)):
                if Race.DEMON in minion.races:
                    yield Buff(minion, "REV_835e")


class REV_835e:
    """Imp King Rafaam Buff - 小鬼大王拉法姆增益"""
    atk = 2
    max_health = 2


