"""
深入翡翠梦境 - PALADIN
"""
from ..utils import *
from .imbue_helpers import trigger_imbue


# COMMON

class EDR_255:
    """复苏烈焰 - Renewing Flames
    Lifesteal. Deal $5 damage to the lowest Health enemy, twice.
    
    7费 自然法术
    吸血。对生命值最低的敌人造成5点伤害，触发两次。
    """
    requirements = {}
    
    def play(self):
        # 对生命值最低的敌人造成5点伤害，触发两次
        for _ in range(2):
            # 找到生命值最低的敌人
            enemies = list(self.controller.opponent.field) + [self.controller.opponent.hero]
            if enemies:
                lowest_health_enemy = min(enemies, key=lambda e: e.health)
                yield Hit(lowest_health_enemy, 5)


class EDR_257:
    """圣光抚愈者 - Lightmender
    Taunt. Choose One - +3 Attack and Divine Shield; or +3 Health and Lifesteal.
    
    4费 3/3 随从
    嘲讽。抉择：获得+3攻击力和圣盾；或者获得+3生命值和吸血。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.CHOOSE_ONE: True,
    }
    choose = ["EDR_257a", "EDR_257b"]


class EDR_257a:
    """圣光抚愈者 - 选项A
    +3 Attack and Divine Shield
    
    获得+3攻击力和圣盾。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    play = Buff(TARGET, "EDR_257e_attack")


class EDR_257b:
    """圣光抚愈者 - 选项B
    +3 Health and Lifesteal
    
    获得+3生命值和吸血。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    play = Buff(TARGET, "EDR_257e_health")


class EDR_451:
    """金萼幼龙 - Goldpetal Drake
    Battlecry and Deathrattle: Imbue your Hero Power.
    
    3费 3/3 龙
    战吼，亡语：灌注你的英雄技能。
    """
    requirements = {}
    
    def play(self):
        # 战吼：灌注英雄技能
        trigger_imbue(self.controller)
    
    @property
    def deathrattle(self):
        # 亡语：灌注英雄技能
        trigger_imbue(self.controller)
        return []  # trigger_imbue 直接修改状态，不需要返回 action


class FIR_914:
    """焚火之力 - Smoldering Strength
    Give a friendly minion +{0}/+{0}. (Upgrades each turn, but discards after 3!)
    
    1费 法术
    使一个友方随从获得+X/+X。（每回合升级，但3回合后弃掉！）
    X = 持有回合数 + 1
    
    实现说明：
    - 初始效果为 +1/+1
    - 每回合开始时升级：+2/+2, +3/+3
    - 第3回合开始时（持有2回合后）自动弃掉
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    
    def play(self):
        # 获取持有回合数（初始为0，表示刚抽到）
        turns_held = getattr(self, 'turns_held', 0)
        # 给予目标随从 +X/+X（至少+1/+1）
        bonus = turns_held + 1
        yield Buff(TARGET, "FIR_914e", atk_bonus=bonus, health_bonus=bonus)
    
    class Hand:
        # 每回合开始时增加持有回合数并检查是否弃牌
        def _on_turn_begin(self):
            # 增加持有回合数
            self.owner.turns_held = getattr(self.owner, 'turns_held', 0) + 1
            # 如果持有3回合，弃掉此牌
            if self.owner.turns_held >= 3:
                yield Discard(SELF)
        
        events = OWN_TURN_BEGIN.on(_on_turn_begin)


class FIR_941:
    """烧灼映像 - Searing Reflection
    Draw a minion. Summon an 8/8 copy of it with Divine Shield.
    
    7费 法术
    抽一张随从牌。召唤一个8/8并具有圣盾的该随从的复制。
    """
    requirements = {}
    
    def play(self):
        # 抽一张随从牌
        drawn_card = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)
        
        if drawn_card:
            # 创建一个8/8的复制
            copy = self.controller.card(drawn_card[0].id, source=self)
            copy.atk = 8
            copy.max_health = 8
            copy.tags[GameTag.DIVINE_SHIELD] = True
            # 召唤该复制
            yield Summon(CONTROLLER, copy)


# RARE

class EDR_251:
    """龙鳞军备 - Dragonscale Armaments
    Draw a spell that started in your deck and one that didn't.
    
    1费 神圣法术
    抽取你套牌中和套牌之外的法术牌各一张。
    """
    requirements = {}
    
    def play(self):
        # 抽取套牌中的法术牌（started_in_deck = True）
        deck_spells = [c for c in self.controller.deck if c.type == CardType.SPELL and getattr(c, 'started_in_deck', True)]
        if deck_spells:
            import random
            yield Draw(CONTROLLER, random.choice(deck_spells))
        
        # 抽取套牌外的法术牌（started_in_deck = False）
        non_deck_spells = [c for c in self.controller.deck if c.type == CardType.SPELL and not getattr(c, 'started_in_deck', True)]
        if non_deck_spells:
            import random
            yield Draw(CONTROLLER, random.choice(non_deck_spells))


class EDR_253:
    """巨熊之槌 - Ursine Maul
    After your hero attacks, draw your highest Cost card.
    
    4费 4/2 武器
    在你的英雄攻击后，抽取你法力值消耗最高的牌。
    """
    # 监听英雄攻击事件
    events = OWN_HERO_ATTACK.after(
        lambda self, source, target: [
            # 找到牌库中法力值消耗最高的牌
            Draw(CONTROLLER, Find(
                FRIENDLY_DECK,
                lambda c: c == max(self.controller.deck, key=lambda card: card.cost, default=None)
            )) if self.controller.deck else None
        ]
    )


class EDR_264:
    """圣光护盾 - Aegis of Light
    Summon a random 2-Cost minion and give it Taunt. Imbue your Hero Power.
    
    2费 神圣法术
    随机召唤一个法力值消耗为（2）的随从并使其获得嘲讽。灌注你的英雄技能。
    """
    requirements = {}
    
    def play(self):
        # 随机召唤一个2费随从
        yield Summon(CONTROLLER, RandomMinion(cost=2))
        # 给予嘲讽
        yield Buff(Find(CONTROLLER_FIELD + FRIENDLY + LAST_SUMMONED), "EDR_264e")
        # 触发 Imbue
        trigger_imbue(self.controller)


class FIR_961:
    """灰叶树精 - Ashleaf Pixie
    Battlecry: If you're holding a spell that costs (5) or more, gain Divine Shield and Lifesteal.
    
    3费 3/3 随从
    战吼：如果你手牌中有法力值消耗大于或等于（5）点的法术牌，获得圣盾和吸血。
    """
    requirements = {}
    
    def play(self):
        # 检查手牌中是否有5费或更高的法术牌
        has_expensive_spell = any(
            c.type == CardType.SPELL and c.cost >= 5
            for c in self.controller.hand
        )
        
        if has_expensive_spell:
            # 获得圣盾和吸血
            yield Buff(SELF, "FIR_961e")


# EPIC

class EDR_252:
    """乌索尔印记 - Mark of Ursol
    Choose a minion. If it's an enemy, set its stats to 1/1. If it's friendly, set its stats to 3/3 instead.
    
    2费 法术
    选择一个随从。如果是敌方随从，将其属性值变为1/1；如果是友方随从，改为将其属性值变为3/3。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 检查目标是友方还是敌方
        if TARGET.controller == self.controller:
            # 友方随从：属性值变为3/3
            yield Buff(TARGET, "EDR_252e_friendly")
        else:
            # 敌方随从：属性值变为1/1
            yield Buff(TARGET, "EDR_252e_enemy")


class EDR_256:
    """梦境卫士 - Dreamwarden
    Taunt. Battlecry: If there is a card in your deck that didn't start there, draw it and gain +2/+2.
    
    4费 3/4 龙
    嘲讽。战吼：如果你的牌库中有对战开始时不在牌库中的牌，则抽取其中的一张并获得+2/+2。
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    def play(self):
        # 找到牌库中不是对战开始时就在牌库中的牌
        non_starting_cards = [c for c in self.controller.deck if not getattr(c, 'started_in_deck', True)]
        
        if non_starting_cards:
            # 随机抽取一张
            import random
            card_to_draw = random.choice(non_starting_cards)
            yield Draw(CONTROLLER, card_to_draw)
            # 获得+2/+2
            yield Buff(SELF, "EDR_256e")


# LEGENDARY

class EDR_258:
    """坚韧的托雷斯 - Toreth the Unbreaking
    Divine Shield, Taunt. Your Divine Shields take three hits to break.
    
    5费 3/4 随从
    圣盾。嘲讽。你的圣盾承受三次伤害才会破灭。
    
    实现说明：
    - 使用 Predamage 事件拦截对友方圣盾角色的伤害
    - 检查目标是否有 TAG_SCRIPT_DATA_NUM_1 标记（托雷斯效果）
    - 递减计数，只有当计数降到1时才移除圣盾
    - 参考：titans/paladin.py - TTN_858 (Predamage 用法)
    - 参考：paradise/warrior.py - VAC_527 (Predamage 限制伤害)
    """
    tags = {
        GameTag.DIVINE_SHIELD: True,
        GameTag.TAUNT: True,
    }
    
    # 光环效果：给所有友方圣盾角色添加3次伤害计数
    update = Refresh(FRIENDLY_CHARACTERS + DIVINE_SHIELD, {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 3,  # 圣盾需要承受3次伤害
    })
    
    # 使用 Predamage 事件拦截伤害，实现圣盾3次伤害机制
    events = Predamage(FRIENDLY_CHARACTERS + DIVINE_SHIELD).on(
        lambda self, source, target, amount: [
            # 检查目标是否有托雷斯的计数标记
            _handle_toreth_divine_shield(self, target, amount)
        ]
    )


def _handle_toreth_divine_shield(source, target, amount):
    """处理托雷斯的圣盾3次伤害机制"""
    # 获取当前圣盾计数
    shield_count = target.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
    
    if shield_count > 1:
        # 还有多次伤害机会，递减计数但不移除圣盾
        from ...actions import SetTag, Predamage as PredamageAction
        return [
            # 递减计数
            SetTag(target, {GameTag.TAG_SCRIPT_DATA_NUM_1: shield_count - 1}),
            # 将伤害设为0（圣盾吸收伤害）
            PredamageAction(target, 0)
        ]
    else:
        # 最后一次伤害，正常移除圣盾
        # 不需要额外操作，让游戏引擎正常处理
        return []


class EDR_259:
    """乌索尔 - Ursol
    Battlecry: Cast the highest Cost spell from your hand as an Aura that lasts 3 turns.
    
    8费 9/7 野兽
    战吼：将你手牌中法力值消耗最高的法术变为持续3回合的光环并施放。
    
    实现说明：
    - 找到最高费用法术并立即施放一次
    - 创建一个持续3回合的 Enchantment
    - Enchantment 每回合开始时重复施放法术效果
    - 3回合后自动移除
    - 参考：titans/paladin.py - TTN_854e (持续回合数机制)
    """
    requirements = {}
    
    def play(self):
        # 找到手牌中法力值消耗最高的法术
        spells_in_hand = [c for c in self.controller.hand if c.type == CardType.SPELL]
        
        if spells_in_hand:
            highest_cost_spell = max(spells_in_hand, key=lambda c: c.cost)
            
            # 立即施放一次法术
            yield Play(highest_cost_spell)
            
            # 创建一个持续3回合的光环，每回合重复施放法术
            yield Buff(CONTROLLER, "EDR_259e", spell_id=highest_cost_spell.id)


