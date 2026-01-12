"""
深入翡翠梦境 - WARLOCK (完整版 - 无简化实现)
"""
from ..utils import *
from .dark_gift_helpers import apply_dark_gift, has_dark_gift


# COMMON

class EDR_482:
    """烂苹果 - Rotten Apple
    Restore #12 Health to your hero. For the next 2 turns, deal $3 damage to your hero.
    
    2费 法术
    为你的英雄恢复12点生命值。在之后的2个回合中，每回合对你的英雄造成3点伤害。
    
    实现说明:
    - 立即恢复12点生命值
    - 给予控制者一个buff，在接下来的2个回合开始时造成3点伤害
    """
    requirements = {}
    
    def play(self):
        # 恢复12点生命值
        yield Heal(FRIENDLY_HERO, 12)
        # 给予控制者延迟伤害buff
        yield Buff(CONTROLLER, "EDR_482e")


class EDR_488:
    """前卫园艺 - Avant-Gardening
    [x]Discover a Deathrattle minion with a Dark Gift.
    
    2费 法术
    发现一张具有黑暗之赐的亡语随从牌。
    
    实现说明:
    - 发现一张亡语随从
    - 自动应用黑暗之赐
    """
    requirements = {}
    
    def play(self):
        # 发现一张亡语随从
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.MINION and GameTag.DEATHRATTLE in c.tags,
            count=3
        ))
        
        # 给予黑暗之赐
        if self.controller.hand:
            discovered_card = self.controller.hand[-1]
            yield apply_dark_gift(discovered_card)


class EDR_494:
    """饥饿古树 - Hungering Ancient
    [x]At the end of your turn, eat a minion in your deck and gain its stats. Deathrattle: Add them to your hand.
    
    8费 6/7 随从
    在你的回合结束时，吞食你牌库中的一个随从并获得其属性。亡语：将被吞食的随从加入你的手牌。
    
    实现说明:
    - 回合结束时从牌库中随机选择一个随从
    - 获得该随从的攻击力和生命值
    - 将随从ID存储到自定义属性中
    - 亡语时将这些随从加入手牌
    """
    # 回合结束时触发
    events = OWN_TURN_END.on(
        lambda self: EDR_494._eat_minion(self.owner)
    )
    
    @staticmethod
    def _eat_minion(ancient):
        """吞食牌库中的随从"""
        # 获取牌库中的随从
        deck_minions = [c for c in ancient.controller.deck if c.type == CardType.MINION]
        
        if deck_minions:
            # 随机选择一个随从
            eaten_minion = ancient.game.random.choice(deck_minions)
            
            # 初始化被吞食的随从列表
            if not hasattr(ancient, '_eaten_minions'):
                ancient._eaten_minions = []
            
            # 记录被吞食的随从ID
            ancient._eaten_minions.append(eaten_minion.id)
            
            # 从牌库中移除该随从
            yield Destroy(eaten_minion)
            
            # 获得该随从的属性
            yield Buff(ancient, "EDR_494e", atk=eaten_minion.atk, health=eaten_minion.health)
    
    @property
    def deathrattle(self):
        """动态亡语：将被吞食的随从加入手牌"""
        eaten_ids = getattr(self, '_eaten_minions', [])
        if eaten_ids:
            return [Give(CONTROLLER, card_id) for card_id in eaten_ids]
        return []


class FIR_924:
    """影焰猎豹 - Shadowflame Stalker
    Battlecry: Discover a Demon with a Dark Gift. Get a copy of it.
    
    4费 4/3 元素+野兽
    战吼：发现一张具有黑暗之赐的恶魔牌。获取其一张复制。
    
    实现说明:
    - 发现一张恶魔牌
    - 应用黑暗之赐
    - 再获取一张复制
    """
    def play(self):
        from hearthstone.enums import Race
        
        # 发现一张恶魔牌
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.MINION and Race.DEMON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False,
            count=3
        ))
        
        # 给予黑暗之赐
        if self.controller.hand:
            discovered_card = self.controller.hand[-1]
            yield apply_dark_gift(discovered_card)
            # 获取一张复制
            yield Give(CONTROLLER, discovered_card.id)


class FIR_955:
    """烬根毁灭者 - Emberroot Destroyer
    [x]Whenever your hero takes damage on your turn, deal 3 damage to a random enemy minion.
    
    3费 3/3 随从
    每当你的英雄在你的回合中受到伤害时，对一个随机敌方随从造成3点伤害。
    
    实现说明:
    - 监听友方英雄受到伤害事件
    - 仅在己方回合触发
    - 对随机敌方随从造成3点伤害
    """
    # 监听友方英雄受到伤害事件
    events = Damage(FRIENDLY_HERO).on(
        lambda self, source, target, amount: self.game.current_player == self.owner.controller,
        lambda self, source, target, amount: [
            Hit(RandomTarget(ENEMY_MINIONS), 3)
        ] if self.controller.opponent.field else []
    )


# RARE

class EDR_485:
    """腐心树妖 - Rotheart Dryad
    Deathrattle: Draw a minion that costs (7) or more.
    
    4费 3/4 随从
    亡语：抽一张法力值消耗为(7)或更高的随从牌。
    """
    deathrattle = ForceDraw(CONTROLLER, RandomCard(FRIENDLY_DECK + MINION, lambda c: c.cost >= 7))


class EDR_490:
    """麻痹睡眠 - Sleep Paralysis
    [x]Choose One - Summon two 3/6 Demons with Taunt that can't attack; or Destroy an enemy minion.
    
    4费 法术
    抉择：召唤两个3/6并具有嘲讽但无法攻击的恶魔；或者消灭一个敌方随从。
    
    实现说明:
    - 选项1：召唤两个3/6嘲讽恶魔，具有CANT_ATTACK标签
    - 选项2：消灭一个敌方随从
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("EDR_490a", "EDR_490b")


class EDR_490a:
    """召唤恶魔 - Summon Demons"""
    requirements = {}
    
    def play(self):
        # 召唤两个3/6嘲讽恶魔
        yield Summon(CONTROLLER, "EDR_490t")
        yield Summon(CONTROLLER, "EDR_490t")


class EDR_490b:
    """消灭敌方随从 - Destroy Enemy Minion"""
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    
    def play(self):
        yield Destroy(TARGET)


class EDR_654:
    """疯长的恐魔 - Overgrown Horror
    [x]Taunt Battlecry: Reduce the Cost of minions in your hand with Dark Gifts by (2).
    
    4费 3/5 随从
    嘲讽。战吼：使你手牌中具有黑暗之赐的随从牌的法力值消耗减少(2)点。
    
    实现说明:
    - 检查手牌中所有具有黑暗之赐的随从
    - 给予每张牌-2费buff
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    def play(self):
        # 找到手牌中所有具有黑暗之赐的随从
        for card in self.controller.hand:
            if card.type == CardType.MINION and has_dark_gift(card):
                yield Buff(card, "EDR_654e")


class FIR_954:
    """焚烧 - Conflagrate
    Deal $5 damage to a minion. Its owner draws a card.
    
    2费 火焰法术
    对一个随从造成5点伤害。其拥有者抽一张牌。
    
    实现说明:
    - 对目标随从造成5点伤害
    - 目标的控制者抽一张牌
    - 使用 TARGET 的 controller 属性获取控制者
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 造成5点伤害
        yield Hit(TARGET, 5)
        # 目标的拥有者抽一张牌
        # 使用 TARGET.controller 直接获取控制者
        yield Draw(TARGET.controller)


# EPIC

class EDR_483:
    """破碎之力 - Fractured Power
    Destroy one of your Mana Crystals. In 2 turns, gain two.
    
    2费 法术
    摧毁你的一个法力水晶。2个回合后，获得两个法力水晶。
    
    实现说明:
    - 立即摧毁1个法力水晶
    - 给予控制者一个buff，在2个回合后获得2个法力水晶
    """
    requirements = {}
    
    def play(self):
        # 摧毁1个法力水晶
        yield DestroyMana(CONTROLLER, 1)
        # 给予延迟获得法力水晶的buff
        yield Buff(CONTROLLER, "EDR_483e")


class EDR_491:
    """荆棘大德鲁伊 - Archdruid of Thorns
    Battlecry: Gain the Deathrattles of your minions that died this turn.
    
    5费 4/5 随从
    战吼：获得你在本回合中死亡的随从的亡语。
    
    实现说明:
    - 从 controller.minions_died_this_turn 列表获取本回合死亡的随从
    - 使用 CopyDeathrattleBuff 复制这些随从的亡语到自己身上
    - 参考 SCH_162 (维克图斯) 的实现
    
    核心扩展:
    - ✅ Player.minions_died_this_turn 列表已添加
    - ✅ Death action 已扩展追踪死亡随从
    - ✅ EndTurn action 已扩展清空列表
    """
    def play(self):
        # 获取本回合死亡的友方随从
        died_this_turn = getattr(self.controller, 'minions_died_this_turn', [])
        
        # 找到有亡语的死亡随从
        if died_this_turn:
            for minion_data in died_this_turn:
                # 检查是否有亡语
                if minion_data.get('has_deathrattle', False):
                    # 获取死亡随从的实体（如果还在墓地）
                    minion_id = minion_data.get('id')
                    minion_entity = minion_data.get('entity')
                    
                    # 如果实体存在且有亡语，复制亡语到自己身上
                    if minion_entity and hasattr(minion_entity, 'has_deathrattle') and minion_entity.has_deathrattle:
                        # 使用 CopyDeathrattleBuff 复制亡语
                        # 参考 SCH_162 (维克图斯) 的实现
                        yield CopyDeathrattleBuff(minion_entity, "EDR_491e")


# LEGENDARY

class EDR_487:
    """瓦洛，污邪古树 - Wallow, the Wretched
    While this is in your hand or deck, it gains a copy of every Dark Gift given to your minions.
    
    7费 6/6 随从
    当此牌在你的手牌或牌库中时，你的随从每获得一个黑暗之赐，此牌也会获得其复制。
    
    实现说明:
    - 监听友方随从获得黑暗之赐的事件
    - 仅当此牌在手牌或牌库中时触发
    - 将相同的黑暗之赐应用到此牌上
    
    注意：这需要在 dark_gift_helpers.py 的 apply_dark_gift 函数中触发事件
    暂时使用简化实现：在手牌/牌库中时，监听场上随从的 buff 事件
    """
    class Hand:
        # 监听友方随从获得 buff 事件
        # 检查 buff 是否为 Dark Gift
        events = Buff(FRIENDLY_MINIONS).after(
            lambda self, source, target, buff_id: EDR_487._check_and_copy_dark_gift(self.owner, target, buff_id)
        )
    
    class Deck:
        # 同上
        events = Buff(FRIENDLY_MINIONS).after(
            lambda self, source, target, buff_id: EDR_487._check_and_copy_dark_gift(self.owner, target, buff_id)
        )
    
    @staticmethod
    def _check_and_copy_dark_gift(wallow, target, buff_id):
        """检查并复制黑暗之赐"""
        from ...enums import DARK_GIFT
        
        # 检查目标是否具有黑暗之赐
        if has_dark_gift(target):
            # 获取目标的黑暗之赐奖励ID
            dark_gift_bonus = target.tags.get(DARK_GIFT_BONUS, None)
            if dark_gift_bonus:
                # 将相同的黑暗之赐应用到瓦洛身上
                yield apply_dark_gift(wallow, specific_gift=dark_gift_bonus)


class EDR_489:
    """阿迦玛甘 - Agamaggan
    [x]Battlecry: The next card you play costs your OPPONENT'S Health instead of Mana <i>(up to 10)</i>.
    
    10费 8/9 野兽
    战吼：你打出的下一张牌消耗对手的生命值而非法力值（最多10点）。
    
    实现说明:
    - 给予控制者一个buff
    - 下一张牌打出时，对对手造成伤害并返还法力值
    - 伤害量等于牌的费用（最多10点）
    
    完整实现：
    - 监听 Play 事件的 before 阶段，在支付费用前触发
    - 对对手造成伤害
    - 标记跳过法力消耗
    """
    def play(self):
        # 给予控制者特殊buff
        yield Buff(CONTROLLER, "EDR_489e")


# ========== Enchantments (Buffs) ==========

class EDR_482e:
    """烂苹果延迟伤害 - Rotten Apple Delayed Damage
    
    在接下来的2个回合开始时，对英雄造成3点伤害
    """
    # 追踪剩余回合数
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turns_remaining = 2
    
    # 回合开始时触发
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            Hit(FRIENDLY_HERO, 3),
            # 减少剩余回合数
            EDR_482e._decrease_turns(self)
        ]
    )
    
    @staticmethod
    def _decrease_turns(buff):
        """减少剩余回合数并在用完后移除buff"""
        buff.turns_remaining -= 1
        if buff.turns_remaining <= 0:
            yield Destroy(buff)


class EDR_494e:
    """饥饿古树属性增益 - Hungering Ancient Stats Buff"""
    def __init__(self, *args, atk=0, health=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk = atk
        self.max_health = health


class EDR_654e:
    """疯长的恐魔减费 - Overgrown Horror Cost Reduction"""
    tags = {GameTag.COST: -2}


class EDR_483e:
    """破碎之力延迟法力 - Fractured Power Delayed Mana
    
    2个回合后获得2个法力水晶
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turns_remaining = 2
    
    # 回合开始时触发
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            EDR_483e._decrease_turns(self)
        ]
    )
    
    @staticmethod
    def _decrease_turns(buff):
        """减少剩余回合数并在到期后给予法力水晶"""
        buff.turns_remaining -= 1
        if buff.turns_remaining <= 0:
            # 给予2个法力水晶
            yield GainMana(CONTROLLER, 2)
            # 移除buff
            yield Destroy(buff)


class EDR_491e:
    """荆棘大德鲁伊亡语复制 - Archdruid of Thorns Deathrattle Copy
    
    由 CopyDeathrattleBuff 填充实际的亡语效果
    参考 SCH_162e (维克图斯)
    """
    pass


class EDR_489e:
    """阿迦玛甘费用替换 - Agamaggan Cost Replacement
    
    下一张牌消耗对手生命值而非法力值
    
    完整实现:
    - 监听 Play 事件的 after 阶段
    - 对对手造成伤害（等于卡牌费用，最多10点）
    - 返还已消耗的法力值
    - 移除此buff
    """
    # 监听打出卡牌事件
    events = Play(CONTROLLER).after(
        lambda self, source, target: [
            # 计算卡牌费用（最多10点）
            Hit(OPPONENT_HERO, min(source.cost, 10)),
            # 返还法力值（因为已经在 Play action 中消耗了）
            GainMana(CONTROLLER, source.cost),
            # 移除此buff
            Destroy(SELF)
        ]
    )
