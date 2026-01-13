"""
穿越时间流 - 中立 - COMMON
"""
from ..utils import *
from .rewind_helpers import execute_with_rewind, mark_card_rewind


class TIME_002:
    """永世巫师 - Aeon Wizard
    回溯。战吼：随机获取2张你职业的法术牌。
    
    Rewind. Battlecry: Get 2 random spells from your class.
    """
    requirements = {}
    
    def play(self):
        # 标记卡牌具有回溯能力
        mark_card_rewind(self, rewind_count=1)

        # 定义卡牌效果
        def effect():
            # 随机获取2张职业法术
            for _ in range(2):
                yield Give(self.controller, RandomSpell(card_class=self.controller.hero.card_class))


        # 使用 Rewind 包装器执行效果
        yield from execute_with_rewind(self, effect)

class TIME_035:
    """时间机器 - Time Machine
    嘲讽。亡语：随机获取一张回溯牌。
    
    Taunt. Deathrattle: Get a random Rewind card.
    """
    deathrattle = Give(CONTROLLER, RandomCard(rewind=True))


class TIME_040:
    """消散的回忆 - Fading Memory
    亡语：随机获取一张来自过去的法力值消耗为（5）的随从牌。
    
    Deathrattle: Get a random 5-Cost minion from the past.
    """
    deathrattle = Give(CONTROLLER, RandomMinion(cost=5))


class TIME_045:
    """永恒雏龙 - Whelp of the Infinite
    剧毒。重生
    
    Poisonous. Reborn
    """
    # 剧毒和重生都是标签属性，不需要脚本实现
    pass


class TIME_046:
    """赛博格族长 - Cyborg Patriarch
    休眠3回合。嘲讽
    
    Dormant for 3 turns. Taunt
    """
    # 休眠和嘲讽都是标签属性，不需要脚本实现
    pass


class TIME_047:
    """狡诈的郊狼 - Devious Coyote
    潜行。在本回合中，敌方英雄每受到一次伤害，本牌的法力值消耗便减少（1）点。
    
    Stealth. Costs (1) less for each time the enemy hero took damage this turn.
    
    实现说明：
    - 使用光环系统动态计算费用
    - 通过监听敌方英雄受伤事件来追踪受伤次数
    - 回合结束时重置计数
    """
    # 使用光环系统实现动态减费
    class Hand:
        """手牌光环：根据敌方英雄受伤次数减费"""
        def cost_func(self, i):
            """计算动态费用
            
            参数:
                i: 当前费用值
            返回:
                调整后的费用值
            """
            # 获取敌方英雄本回合受伤次数
            opponent_hero = self.controller.opponent.hero
            damage_count = getattr(opponent_hero, 'times_damaged_this_turn', 0)
            # 每次受伤减1费，最低0费
            return max(0, i - damage_count)
        
        update = Refresh(SELF, {GameTag.COST: cost_func})


class TIME_048:
    """钟表发条暴怒者 - Clockwork Rager
    战吼：在本对战中，你每进行过一个回合，便获得+1生命值。
    
    Battlecry: Gain +1 Health for each turn you've taken this game.
    """
    requirements = {}
    
    def play(self):
        # 获取玩家已经进行的回合数
        # 游戏回合数除以2（因为每个玩家轮流）
        turns_taken = (self.game.turn + 1) // 2
        
        # 每回合+1生命值
        if turns_taken > 0:
            yield Buff(self, "TIME_048e", max_health=turns_taken)


class TIME_048e:
    """钟表发条暴怒者 - 生命值增益"""
    # 动态生命值buff，通过参数传递
    pass


class TIME_049:
    """危险的异变体 - Dangerous Variant
    在你的回合开始时，变形成一个随机的法力值消耗为（5）的随从。
    
    At the start of your turn, transform into a random 5-Cost minion.
    """
    events = [
        OWN_TURN_BEGIN.on(lambda self, player: Morph(self, RandomMinion(cost=5)))
    ]


class TIME_050:
    """灵知沙漏 - Sentient Hourglass
    突袭。在本随从受到伤害并存活后，交换其攻击力和生命值。
    
    Rush. After this minion survives damage, swap its stats.
    
    实现说明：
    - 使用 AFTER_DAMAGE 事件监听受伤
    - 交换攻防：需要保存当前值，然后通过SetTag设置新值
    - 确保只在存活时触发
    """
    events = [
        Damage(SELF).after(
            lambda self, target, amount: (
                self.zone == Zone.PLAY and
                self.health > 0 and
                self._swap_stats()
            )
        )
    ]
    
    def _swap_stats(self):
        """交换攻击力和生命值"""
        # 保存当前属性
        current_atk = self.atk
        current_health = self.health
        
        # 通过SetTag交换属性
        # 注意：需要同时设置ATK和HEALTH
        return [
            SetTag(self, {
                GameTag.ATK: current_health,
                GameTag.HEALTH: current_atk,
            })
        ]


class TIME_053:
    """流沙巨口 - Sandmaw
    7/2 野兽
    
    7/2 Beast
    """
    # 白板随从，不需要脚本
    pass


class TIME_054:
    """时空艇长 - Time Skipper
    在每个玩家的回合结束时，使其获得一枚幸运币。
    
    At the end of each player's turn, give them a Coin.
    """
    events = [
        # 己方回合结束
        OWN_TURN_END.on(lambda self, player: Give(CONTROLLER, "GAME_005")),
        # 对手回合结束
        TURN_END.on(
            lambda self, player: (
                entity == self.controller.opponent and
                [Give(self.controller.opponent, "GAME_005")]
            )
        )
    ]


class TIME_056:
    """青铜雏龙 - Whelp of the Bronze
    吸血。圣盾
    
    Lifesteal. Divine Shield
    """
    # 吸血和圣盾都是标签属性，不需要脚本实现
    pass


class TIME_057:
    """年迈的真理追寻者 - Wizened Truthseeker
    战吼：将双方玩家手牌中每张牌的法力值消耗重置为其原始法力值消耗。
    
    Battlecry: Set the Cost of every card in both player's hands back to their original Costs.
    
    实现说明：
    - 移除所有费用相关的buff
    - 使用SetTag直接设置费用为原始费用
    - 处理双方玩家的手牌
    """
    requirements = {}
    
    def play(self):
        # 重置双方手牌的费用
        for player in [self.controller, self.controller.opponent]:
            for card in player.hand:
                # 获取原始费用
                if hasattr(card, 'data') and hasattr(card.data, 'cost'):
                    original_cost = card.data.cost
                    
                    # 使用SetTag直接设置费用为原始费用
                    # 这会覆盖所有费用修改效果
                    yield SetTags(card, {GameTag.COST: original_cost})


class TIME_059:
    """悖论活体 - Living Paradox
    扰魔。战吼：召唤两个2/1并具有扰魔的悖论活体。
    
    Elusive. Battlecry: Summon two 2/1 Living Paradoxes with Elusive.
    """
    requirements = {}
    
    def play(self):
        # 召唤两个2/1扰魔Token
        yield Summon(self.controller, "TIME_059t")
        yield Summon(self.controller, "TIME_059t")


class TIME_060:
    """量子反稳定机 - Quantum Destabilizer
    本随从受到的所有伤害翻倍。
    
    This minion takes double damage from all sources.
    
    实现说明:
    - 重写 get_damage 方法来翻倍伤害
    """
    def get_damage(self, amount: int, target) -> int:
        """重写伤害计算,如果目标是自己则翻倍"""
        if target == self:
            return amount * 2
        return amount


class TIME_062:
    """史书守护者 - Chronicle Keeper
    战吼：如果你的手牌中有龙牌，获得嘲讽和圣盾。
    
    Battlecry: If you're holding a Dragon, gain Taunt and Divine Shield.
    """
    requirements = {}
    
    def play(self):
        # 检查手牌中是否有龙
        has_dragon = False
        for card in self.controller.hand:
            if card.type == CardType.MINION and hasattr(card, 'race') and card.race == Race.DRAGON:
                has_dragon = True
                break
        
        # 如果有龙，获得嘲讽和圣盾
        if has_dragon:
            yield Buff(self, "TIME_062e")


class TIME_062e:
    """史书守护者 - 嘲讽和圣盾"""
    tags = {
        GameTag.TAUNT: True,
        GameTag.DIVINE_SHIELD: True,
    }


class TIME_100:
    """沙漏侍者 - Hourglass Attendant
    圣盾。在你的回合结束时，使你手牌中的所有随从牌获得+1/+1。
    
    Divine Shield. At the end of your turn, give all minions in your hand +1/+1.
    """
    events = [
        OWN_TURN_END.on(
            lambda self, player: [
                Buff(card, "TIME_100e")
                for card in self.controller.hand
                if card.type == CardType.MINION
            ]
        )
    ]


class TIME_100e:
    """沙漏侍者 - +1/+1增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class TIME_101:
    """穿越的炎术士 - Misplaced Pyromancer
    每当你粉碎一张牌时，对所有敌方随从造成2点伤害。
    
    Whenever you Shatter a card, deal 2 damage to all enemy minions.
    
    实现说明：
    - Shatter（粉碎）是指从手牌中移除卡牌的机制
    - 在炉石中，Shatter通常与弃牌（Discard）类似
    - 使用Discard事件作为触发条件
    - 注意：如果未来有专门的Shatter事件，可以替换
    """
    events = [
        Discard(CONTROLLER).on(
            lambda self, entity, card: Hit(ENEMY_MINIONS, 2)
        )
    ]


class TIME_428:
    """昨日鱼人 - Yesterloc
    在你的回合结束时，使你的其他随从获得+1生命值。
    
    At the end of your turn, give your other minions +1 Health.
    """
    events = [
        OWN_TURN_END.on(
            lambda self, player: [
                Buff(minion, "TIME_428e")
                for minion in self.controller.field
                if minion != self
            ]
        )
    ]


class TIME_428e:
    """昨日鱼人 - +1生命值"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.HEALTH: 1,
    }


class TIME_434:
    """时空旅行者 - Temporal Traveler
    亡语：召唤一个4/1的暗影，使其攻击一个随机敌方随从。
    
    Deathrattle: Summon a 4/1 Shadow that attacks a random enemy minion.
    
    实现说明：
    - 亡语分两步：1) 召唤暗影 2) 让暗影攻击
    - 攻击需要在召唤完成后进行
    - 如果没有敌方随从，只召唤不攻击
    """
    def deathrattle(self):
        """动态亡语：召唤暗影并攻击"""
        # 召唤4/1暗影Token
        yield Summon(CONTROLLER, "TIME_434t")
        
        # 检查是否有敌方随从
        if self.controller.opponent.field:
            # 获取刚召唤的暗影（场上最后一个随从）
            if self.controller.field:
                shadow = self.controller.field[-1]
                # 让暗影攻击随机敌方随从
                target = self.game.random.choice(list(self.controller.opponent.field))
                yield Attack(shadow, target)

