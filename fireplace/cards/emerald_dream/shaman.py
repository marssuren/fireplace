"""
漫游翡翠梦境 - SHAMAN
"""
from ..utils import *
from .imbue_helpers import trigger_imbue


# COMMON

class EDR_231:
    """守护巨龙之拥 - Aspect's Embrace
    Restore #4 Health. Draw a card. Imbue your Hero Power.
    
    2费 法术
    恢复4点生命值。抽一张牌。灌注你的英雄技能。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    
    def play(self):
        # 恢复4点生命值
        yield Heal(TARGET, 4)
        # 抽一张牌
        yield Draw(CONTROLLER)
        # 触发 Imbue
        trigger_imbue(self.controller)


class EDR_233:
    """森林之灵 - Spirits of the Forest
    Choose One - Summon three 2/3 Wolves with Taunt; or Summon two 4/3 Falcons with Windfury.
    
    5费 自然法术
    抉择：召唤三只2/3并具有嘲讽的狼；或者召唤两只4/3并具有风怒的猎鹰。
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ["EDR_233a", "EDR_233b"]


class EDR_233a:
    """森林之灵 - 选项A
    Summon three 2/3 Wolves with Taunt
    
    召唤三只2/3并具有嘲讽的狼。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    play = Summon(CONTROLLER, "EDR_233t1") * 3


class EDR_233b:
    """森林之灵 - 选项B
    Summon two 4/3 Falcons with Windfury
    
    召唤两只4/3并具有风怒的猎鹰。
    """
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    play = Summon(CONTROLLER, "EDR_233t2") * 2


class EDR_477:
    """明根捕食花 - Glowroot Lure
    Taunt. Costs (1) less for each time you used your Hero Power this game.
    
    6费 6/6 随从
    嘲讽。在本局对战中，你每使用一次英雄技能，本牌的法力值消耗便减少（1）点。
    
    实现说明：
    - 使用 Player 的 times_hero_power_used_this_game 追踪英雄技能使用次数
    - 动态计算费用减少
    - 参考：titans/neutral_epic.py - TTN_862 (动态费用)
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    cost_mod = lambda self, i: -getattr(self.controller, 'times_hero_power_used_this_game', 0)
class FIR_778:
    """毁灭化身 - Avatar of Destruction
    Taunt. Deathrattle: Deal 9 damage to all enemy minions.
    
    9费 9/9 元素
    嘲讽。亡语：对所有敌方随从造成9点伤害。
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    deathrattle = Hit(ENEMY_MINIONS, 9)


# RARE

class EDR_232:
    """台风 - Typhoon
    Each minion gets shuffled into a random player's deck.
    
    10费 自然法术
    将每个随从洗入随机玩家的牌库。
    
    实现说明：
    - 遍历所有场上随从
    - 随机选择一个玩家（自己或对手）
    - 将随从洗入该玩家的牌库
    """
    requirements = {}
    
    def play(self):
        import random
        # 获取所有场上的随从（需要先复制列表，因为会修改）
        all_minions = list(self.controller.field) + list(self.controller.opponent.field)
        
        for minion in all_minions:
            # 随机选择一个玩家
            target_player = random.choice([self.controller, self.controller.opponent])
            # 将随从洗入该玩家的牌库
            yield Shuffle(target_player, minion)


class EDR_234:
    """翡翠厚赠 - Emerald Bounty
    Draw 2 cards. You can't play them for 2 turns.
    
    2费 法术
    抽两张牌。你无法在2回合内使用这些牌。
    
    实现说明：
    - 抽两张牌
    - 给抽到的牌添加 Enchantment，记录回合数
    - 在2回合内无法使用（通过 CANT_PLAY 标签实现）
    - 参考：titans/neutral_legendary.py - TTN_903 (回合计数机制)
    """
    requirements = {}
    
    def play(self):
        # 抽两张牌
        for _ in range(2):
            drawn_cards = yield Draw(CONTROLLER)
            if drawn_cards:
                # 给抽到的牌添加延迟使用的 Enchantment
                yield Buff(drawn_cards[0], "EDR_234e")


class EDR_518:
    """活体园林 - Living Garden
    Battlecry: Imbue your Hero Power. Reduce the Cost of a minion in your hand by (1).
    
    3费 2/4 元素
    战吼：灌注你的英雄技能。使你手牌中一张随从牌的法力值消耗减少（1）点。
    """
    requirements = {}
    
    def play(self):
        # 触发 Imbue
        trigger_imbue(self.controller)
        
        # 使手牌中一张随机随从牌的费用减少1点
        minions_in_hand = [c for c in self.controller.hand if c.type == CardType.MINION]
        if minions_in_hand:
            import random
            target_minion = random.choice(minions_in_hand)
            yield Buff(target_minion, "EDR_518e")


class FIR_923:
    """炎魔之火 - Flames of the Firelord
    Deal $4 damage to a random enemy minion. If you're holding a card that costs (8) or more, deal $8 instead.
    
    2费 火焰法术
    随机对一个敌方随从造成4点伤害。如果你的手牌中有法力值消耗大于或等于（8）点的牌，改为造成8点。
    """
    requirements = {}
    
    def play(self):
        # 检查手牌中是否有8费或更高的牌
        has_expensive_card = any(c.cost >= 8 for c in self.controller.hand)
        
        # 确定伤害值
        damage = 8 if has_expensive_card else 4
        
        # 随机对一个敌方随从造成伤害
        enemy_minions = list(self.controller.opponent.field)
        if enemy_minions:
            import random
            target = random.choice(enemy_minions)
            yield Hit(target, damage)


class FIR_927:
    """烬鳞雏龙 - Emberscarred Whelp
    Battlecry: Discover a 5-Cost card. Gain 1 Mana Crystal next turn only.
    
    3费 3/2 龙
    战吼：发现一张法力值消耗为（5）的牌。仅在下回合，获得1个法力水晶。
    
    实现说明：
    - 发现一张5费牌
    - 给玩家添加一个 Enchantment，下回合开始时给予1个临时法力水晶
    - 临时法力水晶在回合结束时移除
    - 参考：titans/neutral_epic.py - TTN_862 (临时法力水晶)
    """
    requirements = {}
    
    def play(self):
        # 发现一张5费牌
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.cost == 5,
            count=3
        ))
        
        # 添加下回合临时法力水晶的 Enchantment
        yield Buff(CONTROLLER, "FIR_927e")


# EPIC

class EDR_230:
    """豆蔓蛮兵 - Beanstalk Brute
    Battlecry: Give +4/+4 to the top 3 minions in your deck.
    
    5费 4/4 元素
    战吼：使你牌库中最上方的3张随从牌获得+4/+4。
    
    实现说明：
    - 遍历牌库顶部的牌
    - 找到前3张随从牌
    - 给予+4/+4增益
    """
    requirements = {}
    
    def play(self):
        # 找到牌库顶部的前3张随从牌
        minion_count = 0
        for card in self.controller.deck:
            if card.type == CardType.MINION:
                yield Buff(card, "EDR_230e")
                minion_count += 1
                if minion_count >= 3:
                    break


class EDR_529:
    """胆大的魔荚人 - Plucky Podling
    If this would transform into a minion, it transforms into one that costs (2) more.
    
    1费 1/2 随从
    如果本随从即将变形成为某随从，则会变形成为法力值消耗增加（2）点的随从。
    
    实现说明：
    - 使用自定义标签 TRANSFORM_COST_MODIFIER 标记变形费用修改
    - Morph action 会检查这个标签并修改目标随从的费用
    - 参考：nathria/shaman.py - REV_925 (瓦丝琪女男爵的 TRANSFORM_IMMUNE 机制)
    
    核心扩展：
    - 需要在 enums.py 中添加 TRANSFORM_COST_MODIFIER 标签
    - 需要在 actions.py 的 Morph 类中添加费用修改逻辑
    """
    # 标记变形时费用+2
    # 这个标签会被 Morph action 检查
    from fireplace import enums
    tags = {enums.TRANSFORM_COST_MODIFIER: 2}


# LEGENDARY

class EDR_031:
    """欧恩哈拉 - Ohn'ahra
    At the end of your turn, play the top 3 cards from your deck.
    
    9费 5/11 野兽
    在你的回合结束时，使用你牌库顶的3张牌。
    
    实现说明：
    - 监听回合结束事件
    - 从牌库顶抽取3张牌并立即使用
    - 使用 ForcePlay 自动打出牌（类似 Yogg-Saron）
    - 参考：titans/neutral_legendary.py - TTN_903 (自动使用牌)
    """
    events = OWN_TURN_END.on(
        lambda self: [
            # 使用牌库顶的3张牌
            _play_top_cards_auto(self, 3)
        ]
    )


def _play_top_cards_auto(source, count):
    """从牌库顶自动使用指定数量的牌
    
    实现说明：
    - 从牌库顶抽牌
    - 使用 ForcePlay 自动打出（会自动选择随机目标）
    - 如果无法打出（如法力不足），牌会留在手牌中
    - 参考：OG_042 (尤格-萨隆) 的自动施法机制
    """
    for _ in range(count):
        if source.controller.deck:
            # 抽一张牌
            drawn = yield Draw(CONTROLLER)
            if drawn and drawn[0]:
                card = drawn[0]
                # 检查是否有足够的法力
                if source.controller.can_pay_cost(card):
                    # 使用 ForcePlay 自动打出
                    # ForcePlay 会自动选择随机目标（如果需要）
                    yield ForcePlay(source.controller, card)


class EDR_238:
    """麦琳瑟拉 - Merithra
    Battlecry: Resurrect all different friendly minions that cost (8) or more.
    
    6费 4/4 随从
    战吼：复活所有法力值消耗大于或等于（8）点的不同的友方随从。
    
    实现说明：
    - 从墓地中找到所有8费+的友方随从
    - 去重（不同的随从）
    - 复活它们
    - 参考：titans/priest.py - TTN_737 (复活机制)
    """
    requirements = {}
    
    def play(self):
        # 找到墓地中所有8费+的友方随从
        dead_minions = [
            card for card in self.controller.graveyard
            if card.type == CardType.MINION and card.cost >= 8
        ]
        
        # 去重：只保留不同的随从（按卡牌ID去重）
        seen_ids = set()
        unique_minions = []
        for minion in dead_minions:
            if minion.id not in seen_ids:
                seen_ids.add(minion.id)
                unique_minions.append(minion)
        
        # 复活这些随从
        for minion in unique_minions:
            yield Summon(CONTROLLER, minion.id)

