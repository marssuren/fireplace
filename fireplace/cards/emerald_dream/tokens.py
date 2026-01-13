"""
深入翡翠梦境 - TOKENS
"""
from ..utils import *
from ... import enums


# Death Knight Tokens

class EDR_814t:
    """水蛭 - Leech
    0/2 Beast
    """
    tags = {
        GameTag.ATK: 0,
        GameTag.HEALTH: 2,
    }


class EDR_813t1:
    """蚂蚁 - Ant
    1/1 Beast
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class FIR_901t:
    """霜灼幼龙 - Frostburn Whelp
    4/4 Dragon with Taunt
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.TAUNT: True,
    }


class EDR_818t:
    """甲虫 - Beetle
    1/1 Beast
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


# Druid Tokens

class EDR_271t:
    """树人 - Treant
    2/2 with dynamic Deathrattle
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }

    @property
    def deathrattle(self):
        """动态亡语:获取存储的法术的复制"""
        # 从 buff 中获取存储的法术ID
        spell_id = None
        for buff in self.buffs:
            if hasattr(buff, 'spell_id'):
                spell_id = buff.spell_id
                break
        
        if spell_id:
            from ...actions import Give
            return Give(CONTROLLER, spell_id)
        return None


# EDR_843 森林再生 - Choose One 选项
class EDR_843a:
    """抽法术牌 - Draw Spell"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class EDR_843b:
    """抽随从牌 - Draw Minion"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


# EDR_209 森林之王塞纳留斯 - Choose One 选项
class EDR_209a:
    """给予随从增益 - Buff Minions"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class EDR_209b:
    """召唤古树 - Summon Ancient"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class EDR_209t:
    """古树 - Ancient
    5/5 with Taunt
    """
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True,
    }


class EDR_209e:
    """+1/+3 增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# EDR_845 哈缪尔·符文图腾 - Imbue 追踪 Buff
class EDR_845e:
    """Imbue 追踪 Buff
    追踪法术施放次数,每2个法术触发一次 Imbue
    """
    tags = {
        enums.TRIGGER_COUNT,  # 触发计数器
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 监听法术施放事件
    def _trigger_imbue_on_count(self, player, played_card, target=None):
        """法术施放后的处理逻辑"""
        from .imbue_helpers import trigger_imbue
        
        # 增加计数
        self.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] = self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) + 1
        
        # 检查是否达到2个法术
        if self.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] >= 2:
            # 触发 Imbue
            trigger_imbue(self.owner.controller)
            # 重置计数器
            self.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] = 0
    
    events = OWN_SPELL_PLAY.after(_trigger_imbue_on_count)


class EDR_464e:
    """泰兰德效果 - Tyrande Effect
    接下来的3个法术会施放两次
    
    实现说明:
    - 监听 OWN_SPELL_PLAY 事件
    - 再次触发法术效果(使用 Battlecry action 模拟)
    - 计数器递减
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        enums.TURNS_REMAINING: 3,  # 剩余次数
    }
    
    # 监听法术施放事件
    events = OWN_SPELL_PLAY.after(
        lambda self, player, played_card, target: [
            # 再次触发法术效果
            # 使用 Battlecry action 来模拟 play 效果
            Battlecry(card, target),
            # 递减计数
            UpdateProgress(SELF, -1), # 实际上是用 UpdateProgress 或直接修改
            # 如果计数归零，移除 Buff
            Destroy(SELF) if Attr(SELF, GameTag.TAG_SCRIPT_DATA_NUM_1) <= 1 else None,
            # 更新计数器 (这里为了简单，我们用 SetTag 或 Decrease logic)
            # 由于 UpdateProgress 可能不支持直接减，我们用脚本更新
            EDR_464e._update_count(self)
        ]
    )
    
    @staticmethod
    def _update_count(buff):
        current = buff.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        buff.tags[GameTag.TAG_SCRIPT_DATA_NUM_1] = current - 1


class DARK_GIFT_BUFF:
    """黑暗之赐通用 Buff - Dark Gift Buff
    
    用于通过 Buff Action 应用黑暗之赐效果，从而正确触发 Buff 事件
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, bonus_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.bonus_id = bonus_id
        
    def apply(self, target):
        from .dark_gift_helpers import get_dark_gift_bonus_by_id, apply_dark_gift_to_object
        
        if self.bonus_id:
            bonus = get_dark_gift_bonus_by_id(self.bonus_id)
            if bonus:
                # 使用辅助函数直接应用属性，避免无限递归
                # 注意：这里我们只做属性修改，不应用标签（如果标签包含 Buff 触发器的话）
                # 但 Dark Gift 的标签通常是静态的
                apply_dark_gift_to_object(target, bonus)


# EDR_209 森林之王塞纳留斯 - Choose One 选项已移至 druid.py 中定义


# FIR_907 阿梅达希尔 - 地标升级计数器
class FIR_907e:
    """使用次数计数器"""
    tags = {
        GameTag.TAG_SCRIPT_DATA_NUM_1: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# 其他德鲁伊 Enchantments
class EDR_060e:
    """嘲讽增益"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_270e:
    """法力值消耗减少2点"""
    tags = {
        GameTag.COST: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_271e:
    """存储法术ID的Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    def __init__(self, *args, spell_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id


class EDR_847e:
    """下一个英雄技能0费"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    auras = [Buff(FRIENDLY_HERO_POWER, "EDR_847e_cost")]
    events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))


class EDR_847e_cost:
    """英雄技能0费"""
    tags = {
        GameTag.COST_SET: 0,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class FIR_906e:
    """+1/+1 增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class FIR_908e:
    """+1/+2 和突袭"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }



# Demon Hunter Tokens

class EDR_840t1:
    """乌鸦恐魇种 - Crow Dreadseed
    1费 3/1 野兽+亡灵
    扰魔。休眠1回合。
    """
    tags = {
        GameTag.ELUSIVE: True,
        GameTag.DORMANT: True,
    }
    
    # 休眠1回合
    dormant_turns = 1


class EDR_840t2:
    """猎犬恐魇种 - Hound Dreadseed
    2费 4/4 野兽+亡灵
    休眠2回合。苏醒时,在本回合中使你的英雄获得+3攻击力。
    """
    tags = {
        GameTag.DORMANT: True,
    }
    
    # 休眠2回合
    dormant_turns = 2
    
    # 苏醒时给英雄+3攻击
    awaken = Buff(FRIENDLY_HERO, "EDR_840t2e")


class EDR_840t2e:
    """猎犬恐魇种英雄增益 - Hound Dreadseed Hero Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }
    # 回合结束时移除
    events = OWN_TURN_END.on(
        lambda self: [Destroy(SELF)]
    )


class EDR_840t3:
    """巨蛇恐魇种 - Serpent Dreadseed
    3费 5/5 野兽+亡灵
    嘲讽。吸血。休眠3回合。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.LIFESTEAL: True,
        GameTag.DORMANT: True,
    }
    
    # 休眠3回合
    dormant_turns = 3


# Hunter Tokens

class EDR_263t:
    """狼 - Wolf
    3/2 野兽，突袭
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
    }


class EDR_416t:
    """羊 - Sheep
    3/3，休眠2回合
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.DORMANT: True,
    }
    
    # 休眠2回合
    dormant_turns = 2


class EDR_261e:
    """两栖之灵增益 - Amphibian's Spirit Buff
    +2/+2 和传递性亡语
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
    }
    
    @property
    def deathrattle(self):
        """动态亡语：使一个友方随从获得+2/+2和此亡语"""
        from ...actions import Buff
        from ...dsl.selector import FRIENDLY_MINIONS
        import random
        
        # 选择一个随机友方随从
        friendly_minions = [m for m in self.owner.controller.field if m != self.owner]
        if friendly_minions:
            target = random.choice(friendly_minions)
            return Buff(target, "EDR_261e")
        return None


# Hunter Hero Power

class EDR_HUNTER_HP:
    """狼之祝福 - Blessing of the Wolf
    Hunter 的 Imbued Hero Power
    
    2费英雄技能
    使你手牌中的一个随机野兽获得+X攻击力，其法力值消耗减少(X)点。
    X = Imbue 等级
    """
    def use(self, target=None):
        from ...dsl.selector import FRIENDLY
        import random
        
        # 获取 Imbue 等级
        imbue_level = getattr(self.controller, 'imbue_level', 1)
        
        # 找到手牌中的所有野兽
        beasts_in_hand = [c for c in self.controller.hand if c.race == Race.BEAST]
        
        if beasts_in_hand:
            # 随机选择一个野兽
            target_beast = random.choice(beasts_in_hand)
            # 给予攻击力增益和费用减少
            yield Buff(target_beast, "EDR_HUNTER_HPe", atk_bonus=imbue_level, cost_reduction=imbue_level)


class EDR_HUNTER_HPe:
    """狼之祝福增益 - Blessing of the Wolf Buff"""
    def __init__(self, *args, atk_bonus=1, cost_reduction=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk_bonus = atk_bonus
        self.cost_reduction = cost_reduction
    
    @property
    def atk(self):
        return self.atk_bonus
    
    @property
    def cost(self):
        return -self.cost_reduction


# Mage Tokens and Enchantments

# Mage Hero Power
class EDR_MAGE_HP:
    """小精灵祝福 - Blessing of the Wisp
    Mage 的 Imbued Hero Power
    
    2费英雄技能
    召唤X个小精灵，造成X点伤害，随机分配到所有敌人身上。
    X = Imbue 等级
    """
    def use(self, target=None):
        # 获取 Imbue 等级
        imbue_level = getattr(self.controller, 'imbue_level', 1)
        
        # 召唤小精灵
        for _ in range(imbue_level):
            yield Summon(CONTROLLER, "CS2_231")  # Wisp
        
        # 造成伤害，随机分配到所有敌人
        yield Hit(ENEMY_CHARACTERS, imbue_level, distribute=True)


# EDR_872 生命火花 - Choose One 选项
class EDR_872a:
    """生命火花 - 选项A
    Discover a Mage spell.
    
    发现一张法师法术牌。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class EDR_872b:
    """生命火花 - 选项B
    Discover a Druid spell.
    
    发现一张德鲁伊法术牌。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}


# EDR_517 亢祖 - Choose 选项
class EDR_517a:
    """保留法术 - Keep Spell"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class EDR_517b:
    """放到对手牌库顶 - Put on Opponent's Deck"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


# Mage Enchantments

class FIR_913e:
    """地狱火先锋增益 - Inferno Herald Buff
    法力值消耗减少3点
    """
    tags = {
        GameTag.COST: -3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_874e:
    """星体平衡增益 - Stellar Balance Buff
    法术伤害+1
    """
    tags = {
        GameTag.SPELLPOWER: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class FIR_911e:
    """焚火林地回合计数器 - Smoldering Grove Turn Counter"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    def apply(self, target):
        # 增加持有回合数
        target.turns_in_hand = getattr(target, 'turns_in_hand', 0) + 1


# Neutral Common Tokens

class EDR_492t:
    """小鸭 - Duckling
    1/1 野兽，突袭
    """
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.RUSH: True,
    }


class EDR_978t:
    """踏青驼鹿 - Meadowstrider (1费版本)
    1费 4/4 野兽，嘲讽
    亡语:将一张法力值消耗为(1)点的踏青驼鹿置于你的牌库底。
    """
    tags = {
        GameTag.COST: 1,
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.TAUNT: True,
    }
    
    def deathrattle(self):
        # 创建一张1费的踏青驼鹿
        meadowstrider = self.controller.card("EDR_978t", source=self)
        # 放到牌库底
        yield Shuffle(CONTROLLER, meadowstrider)


# Neutral Rare Tokens

class EDR_260t:
    """幻影绿翼龙 - Illusory Greenwing (抽到时召唤版本)
    4/5 龙，嘲讽
    抽到时召唤。
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True,
        GameTag.TOPDECK: True,  # Cast When Drawn / Summoned When Drawn
    }
    
    def draw(self):
        # 抽到时召唤自己
        yield Summon(CONTROLLER, self)


# ========================================
# Neutral Legendary Tokens and Enchantments
# ========================================

# EDR_888 护路者玛洛恩 - Enchantment
class EDR_888e:
    """护路者玛洛恩 - 费用变为(1)"""
    tags = {
        GameTag.COST_SET: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# EDR_846 莎拉达希尔 - 腐化梦境牌 Tokens

class FIR_846t1:
    """腐化的梦境 - Corrupted Dream
    0费法术
    将一个随从洗入其拥有者的牌库。
    """
    tags = {
        GameTag.COST: 0,
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 将目标随从洗入其拥有者的牌库
        yield Shuffle(TARGET.controller, TARGET)


class FIR_846t2:
    """腐化的伊瑟拉苏醒 - Corrupted Awakening
    2费法术
    对所有敌人造成5点伤害。
    """
    tags = {
        GameTag.COST: 2,
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    def play(self):
        yield Hit(ENEMY_CHARACTERS, 5)


class FIR_846t3:
    """腐化的梦魇 - Corrupted Nightmare
    0费法术
    使一个随从获得+5/+5，并在本回合中免疫。
    """
    tags = {
        GameTag.COST: 0,
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        yield Buff(TARGET, "FIR_846t3e")


class FIR_846t3e:
    """+5/+5 和本回合免疫"""
    tags = {
        GameTag.IMMUNE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }
    # 回合结束时移除免疫
    events = OWN_TURN_END.on(
        lambda self: [SetTag(self.owner, {GameTag.IMMUNE: False})]
    )


class FIR_846t4:
    """腐化的翡翠幼龙 - Corrupted Emerald Drake
    4费 14/12 龙
    """
    tags = {
        GameTag.COST: 4,
        GameTag.ATK: 14,
        GameTag.HEALTH: 12,
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CARDRACE: Race.DRAGON,
    }


class FIR_846t5:
    """腐化的笑姐 - Corrupted Laughing Sister
    2费 6/10 随从
    扰魔。使你的英雄也获得扰魔。
    """
    tags = {
        GameTag.COST: 2,
        GameTag.ELUSIVE: True,
        GameTag.ATK: 6,
        GameTag.HEALTH: 10,
        GameTag.CARDTYPE: CardType.MINION,
    }
    
    # 进入场时给英雄扰魔
    play = Buff(FRIENDLY_HERO, "FIR_846t5e")


class FIR_846t5e:
    """英雄扰魔"""
    tags = {
        GameTag.ELUSIVE: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# ========================================
# Paladin Tokens and Enchantments
# ========================================

# Paladin Hero Power

class EDR_PALADIN_HP:
    """龙之祝福 - Blessing of the Dragon
    Paladin 的 Imbued Hero Power
    
    2费英雄技能
    将两张翡翠传送门洗入你的牌库。（你的传送门召唤X费龙。）
    X = Imbue 等级
    """
    def use(self, target=None):
        # 获取 Imbue 等级
        imbue_level = getattr(self.controller, 'imbue_level', 1)
        
        # 创建两张翡翠传送门
        for _ in range(2):
            portal = self.controller.card("EDR_PALADIN_PORTAL", source=self)
            # 设置传送门召唤的龙的费用
            portal.dragon_cost = imbue_level
            # 洗入牌库
            yield Shuffle(CONTROLLER, portal)


class EDR_PALADIN_PORTAL:
    """翡翠传送门 - Emerald Portal
    Paladin Imbued Hero Power 生成的传送门
    
    X费 法术
    召唤一个X费龙。
    X = Imbue 等级
    """
    tags = {
        GameTag.CARDTYPE: CardType.SPELL,
    }
    
    @property
    def cost(self):
        return getattr(self, 'dragon_cost', 1)
    
    def play(self):
        # 召唤一个对应费用的龙
        dragon_cost = getattr(self, 'dragon_cost', 1)
        yield Summon(CONTROLLER, RandomMinion(cost=dragon_cost, race=Race.DRAGON))


# EDR_257 圣光抚愈者 - Choose One 选项的 Enchantments

class EDR_257e_attack:
    """+3攻击力和圣盾"""
    tags = {
        GameTag.ATK: 3,
        GameTag.DIVINE_SHIELD: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_257e_health:
    """+3生命值和吸血"""
    tags = {
        GameTag.HEALTH: 3,
        GameTag.LIFESTEAL: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# FIR_914 焚火之力 - Enchantment

class FIR_914e:
    """焚火之力增益 - Smoldering Strength Buff
    +X/+X 增益
    """
    def __init__(self, *args, atk_bonus=1, health_bonus=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk_bonus = atk_bonus
        self.health_bonus = health_bonus
    
    @property
    def atk(self):
        return self.atk_bonus
    
    @property
    def max_health(self):
        return self.health_bonus


# EDR_264 圣光护盾 - Enchantment

class EDR_264e:
    """嘲讽增益"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# FIR_961 灰叶树精 - Enchantment

class FIR_961e:
    """圣盾和吸血增益"""
    tags = {
        GameTag.DIVINE_SHIELD: True,
        GameTag.LIFESTEAL: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# EDR_252 乌索尔印记 - Enchantments

class EDR_252e_friendly:
    """友方随从属性变为3/3"""
    tags = {
        GameTag.ATK_SET: 3,
        GameTag.HEALTH_SET: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_252e_enemy:
    """敌方随从属性变为1/1"""
    tags = {
        GameTag.ATK_SET: 1,
        GameTag.HEALTH_SET: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# EDR_256 梦境卫士 - Enchantment

class EDR_256e:
    """+2/+2 增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# EDR_259 乌索尔 - Enchantment

class EDR_259e:
    """乌索尔光环效果 - Ursol Aura
    存储法术ID并持续3回合，每回合开始时重复施放法术
    
    实现说明：
    - 使用 PROGRESS 标签追踪已经过的回合数
    - 每回合开始时重复施放存储的法术
    - 3回合后自动移除
    - 参考：titans/paladin.py - TTN_854e (持续回合数机制)
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.PROGRESS: 0,  # 追踪已经过的回合数
    }
    
    def __init__(self, *args, spell_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id
    
    # 每回合开始时重复施放法术并增加回合计数
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 重复施放法术（如果有存储的法术ID）
            _cast_ursol_spell(self) if hasattr(self, 'spell_id') and self.spell_id else None,
            # 增加回合计数
            UpdateProgress(SELF, 1),
            # 检查是否达到3回合，如果是则移除
            Destroy(SELF) if Attr(SELF, GameTag.PROGRESS) >= 3 else None
        ]
    )


def _cast_ursol_spell(enchantment):
    """重复施放乌索尔存储的法术"""
    from ...actions import Play
    
    # 创建法术的一个副本并施放
    if enchantment.spell_id:
        spell_copy = enchantment.owner.controller.card(enchantment.spell_id, source=enchantment.owner)
        return Play(spell_copy)
    return None


# ========================================
# Priest Tokens and Enchantments
# ========================================

# Priest Hero Power

class EDR_PRIEST_HP:
    """月之祝福 - Blessing of the Moon
    Priest 的 Imbued Hero Power
    
    2费英雄技能
    为一个随从恢复X点生命值。如果目标生命值已满,则改为使其获得+X生命值上限。
    X = Imbue 等级
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def use(self, target):
        # 获取 Imbue 等级
        imbue_level = getattr(self.controller, 'imbue_level', 1)
        
        # 检查目标生命值是否已满
        if target.health >= target.max_health:
            # 生命值已满,给予生命值上限增益
            yield Buff(target, "EDR_PRIEST_HPe", health_bonus=imbue_level)
        else:
            # 恢复生命值
            yield Heal(target, imbue_level)


class EDR_PRIEST_HPe:
    """月之祝福增益 - Blessing of the Moon Buff"""
    def __init__(self, *args, health_bonus=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.health_bonus = health_bonus
    
    @property
    def max_health(self):
        return self.health_bonus


# Priest Enchantments

class FIR_777e:
    """+3/+3 增益"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_970e:
    """-2攻击力增益(直到下回合)"""
    tags = {
        GameTag.ATK: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 在施放者的下个回合开始时移除
    events = Turn(Attr(SELF, GameTag.CONTROLLER)).on(
        Destroy(SELF)
    )


class FIR_918e:
    """+3/+3 增益"""
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class EDR_464e:
    """泰兰德效果 - 接下来3个法术施放两次
    
    实现说明:
    - 使用 TAG_SCRIPT_DATA_NUM_1 追踪剩余次数
    - 监听法术施放事件
    - 重复施放法术并递减计数
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        enums.TURNS_REMAINING: 3,  # 剩余次数
    }
    
    def _on_spell_play(self, source, card, *args):
        """法术施放后的处理逻辑"""
        # 获取剩余次数
        remaining = self.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0)
        
        if remaining > 0:
            # 重复施放法术
            from ...actions import SetTag
            
            # 递减计数
            yield SetTag(SELF, {GameTag.TAG_SCRIPT_DATA_NUM_1: remaining - 1})
            
            # 重复施放法术效果
            if hasattr(card, 'play') and callable(card.play):
                yield from card.play()
            
            # 如果计数归零,移除 buff
            if remaining - 1 <= 0:
                yield Destroy(SELF)
    
    events = OWN_SPELL_PLAY.after(_on_spell_play)


class EDR_895e:
    """艾维娜月相演变效果
    
    实现说明:
    - 使用 PROGRESS 标签追踪月相(0=新月, 1=上弦月, 2=满月)
    - 每回合开始时推进月相
    - 当满月升起时,给所有卡牌添加费用变为1的 Aura
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.PROGRESS: 0,  # 月相进度
    }
    
    def _advance_lunar_cycle(self):
        """推进月相"""
        # SetTag 已经通过 from ..utils import *
from ... import enums 导入
        
        # 获取当前月相
        current_phase = self.tags.get(GameTag.PROGRESS, 0)
        
        # 推进月相
        new_phase = current_phase + 1
        yield SetTag(SELF, {GameTag.PROGRESS: new_phase})
        
        # 检查是否到达满月(第3回合,即 PROGRESS=2)
        if new_phase >= 2:
            # 激活满月效果:所有卡牌费用变为1
            # 给玩家添加永久 Aura
            yield Buff(CONTROLLER, "EDR_895e_fullmoon")
            # 移除月相追踪 buff
            yield Destroy(SELF)
    
    events = OWN_TURN_BEGIN.on(_advance_lunar_cycle)


class EDR_895e_fullmoon:
    """艾维娜满月效果 - 所有卡牌费用变为1
    
    实现说明:
    - 永久 Aura,影响手牌和牌库中的所有卡牌
    - 使用 Hand 和 Deck Aura 实现
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    class Hand:
        """手牌中的卡牌费用变为1"""
        def cost_func(self, i):
            return 1
    
    class Deck:
        """牌库中的卡牌费用变为1"""
        def cost_func(self, i):
            return 1


# ========================================
# Rogue Tokens and Enchantments
# ========================================

# EDR_523 欺诈之网 - Spider Token
class EDR_523t:
    """蜘蛛 - Spider
    4/4 with Stealth
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.STEALTH: True,
        GameTag.CARDTYPE: CardType.MINION,
    }


# FIR_922 燃薪之剑 - Weapon Buff
class FIR_922e:
    """+3攻击力增益"""
    tags = {
        GameTag.ATK: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# FIR_919 永燃火凤 - Deathrattle Enchantment
class FIR_919e:
    """永燃火凤亡语效果 - 回合结束时获取复制"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 回合结束时给予复制
    events = OWN_TURN_END.on(
        Give(CONTROLLER, "FIR_919")
    )


# EDR_525 倒刺荆棘 - Choose One Enchantments
class EDR_525e_poisonous:
    """本回合剧毒"""
    tags = {
        GameTag.POISONOUS: True,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    # 回合结束时移除
    events = OWN_TURN_END.on(Destroy(SELF))


class EDR_525e_deathrattle:
    """亡语:对所有敌人造成2点伤害"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    @property
    def deathrattle(self):
        """动态亡语:对所有敌人造成2点伤害"""
        from ...actions import Hit
        from ...dsl.selector import ENEMY_CHARACTERS
        return Hit(ENEMY_CHARACTERS, 2)


# EDR_526 雷弗拉尔 - Trap Enchantment
class EDR_526e:
    """困住效果 - 增加费用使其无法使用,1回合后恢复
    
    实现说明:
    - 增加大量费用使卡牌无法使用
    - 1回合后自动移除
    """
    tags = {
        GameTag.COST: 99,  # 增加99费,基本无法使用
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 对手回合结束时移除
    events = OPPONENT_TURN_END.on(Destroy(SELF))


# EDR_527 阿莎曼 - Cost Reduction Enchantment
class EDR_527e:
    """费用减少3点"""
    tags = {
        GameTag.COST: -3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# ========================================
# Shaman Tokens and Enchantments
# ========================================

# EDR_233 森林之灵 - Choose One Tokens

class EDR_233t1:
    """狼 - Wolf
    2/3 野兽，嘲讽
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.TAUNT: True,
    }


class EDR_233t2:
    """猎鹰 - Falcon
    4/3 野兽，风怒
    """
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 3,
        GameTag.WINDFURY: True,
    }


# Shaman Hero Power

class EDR_SHAMAN_HP:
    """风之祝福 - Blessing of the Wind
    Shaman 的 Imbued Hero Power
    
    2费英雄技能
    将一个友方随从变形成为法力值消耗增加 (X) 点的随从。
    X = Imbue 等级
    
    官方数据来源：
    - 英文名：Blessing of the Wind
    - 中文名：风之祝福
    - 效果：Transform a friendly minion into one that costs (X) more
    - 初始等级：X=1 (费用+1)
    - 每次 Imbue：X 增加 1 (费用+2, +3, ...)
    
    参考：
    - nathria/shaman.py - REV_920 (可信的伪装，变形+2费)
    - nathria/shaman.py - REV_923 (淤泥之池，变形+1费)
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def use(self, target):
        # 获取 Imbue 等级
        imbue_level = getattr(self.controller, 'imbue_level', 1)
        
        # 将目标随从变形为费用 + imbue_level 的随从
        if target:
            new_cost = target.cost + imbue_level
            yield Morph(target, RandomMinion(cost=new_cost))


class EDR_SHAMAN_HP_TOKEN:
    """元素图腾 - Elemental Totem (已弃用)
    
    注意：根据官方数据，Shaman 的 Imbued Hero Power 不是召唤图腾
    而是变形随从，因此这个 Token 不再使用
    """
    tags = {
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CARDRACE: Race.TOTEM,
    }


# Shaman Enchantments

class EDR_234e:
    """翡翠厚赠延迟使用效果 - Emerald Bounty Delay
    
    实现说明：
    - 使用 TAG_SCRIPT_DATA_NUM_1 追踪剩余回合数
    - 初始为2，每回合递减
    - 当计数>0时，无法使用（CANT_PLAY）
    - 参考：titans/neutral_legendary.py - TTN_903e
    
    修正：直接设置 CANT_PLAY 标签，避免使用 lambda 在 auras 中
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_SCRIPT_DATA_NUM_1: 2,  # 剩余回合数
        GameTag.CANT_PLAY: True,  # 初始状态无法使用
    }
    
    # 每回合开始时递减计数并更新状态
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 递减计数
            SetTag(self.owner, {GameTag.TAG_SCRIPT_DATA_NUM_1: max(0, self.owner.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) - 1)}),
            # 如果计数<=0，移除无法使用标签并销毁此效果
            SetTag(self.owner, {GameTag.CANT_PLAY: False}) if self.owner.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) <= 1 else None,
            Destroy(SELF) if self.owner.tags.get(GameTag.TAG_SCRIPT_DATA_NUM_1, 0) <= 1 else None
        ]
    )


class EDR_518e:
    """活体园林费用减少 - Living Garden Cost Reduction
    费用减少1点
    """
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class FIR_927e:
    """烬鳞雏龙临时法力水晶 - Emberscarred Whelp Temp Mana
    
    实现说明：
    - 下回合开始时给予1个临时法力水晶
    - 回合结束时移除临时法力水晶
    - 参考：titans/neutral_epic.py - TTN_862e
    
    修正：直接修改 temp_mana 属性而非使用 GainMana/LoseMana
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 对手回合结束时（即自己回合开始前）给予临时法力水晶
    events = OPPONENT_TURN_END.on(
        lambda self: [
            # 给予1个临时法力水晶（直接修改 temp_mana 属性）
            _grant_temp_mana(self.owner.controller, 1),
            # 添加回合结束时移除法力水晶的标记
            Buff(CONTROLLER, "FIR_927e_temp"),
            # 移除此效果
            Destroy(SELF)
        ]
    )


def _grant_temp_mana(player, amount):
    """给予玩家临时法力水晶"""
    player.temp_mana += amount
    return []


class FIR_927e_temp:
    """烬鳞雏龙临时法力水晶移除标记"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    
    # 回合结束时移除临时法力水晶
    events = OWN_TURN_END.on(
        lambda self: [
            # 移除1个临时法力水晶
            _remove_temp_mana(self.owner.controller, 1),
            # 移除此效果
            Destroy(SELF)
        ]
    )


def _remove_temp_mana(player, amount):
    """移除玩家的临时法力水晶"""
    player.temp_mana = max(0, player.temp_mana - amount)
    return []




class EDR_230e:
    """+4/+4 增益"""
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# ========================================
# Warlock Tokens and Enchantments
# ========================================

class EDR_490t:
    """麻痹睡眠恶魔 - Sleep Paralysis Demon
    3/6 恶魔，嘲讽，无法攻击
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 6,
        GameTag.TAUNT: True,
        GameTag.CANT_ATTACK: True,
        GameTag.CARDRACE: Race.DEMON,
    }
 
 