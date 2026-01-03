"""巫妖王的进军 - 迷你扩展包 (March of the Lich King)"""
from ..utils import *


class RLK_222:
    """阿斯塔洛·血誓 (Astalor Bloodsworn)
    战吼：将护卫阿斯塔洛置入你的手牌。法力渴求（5）：造成2点伤害。
    机制: BATTLECRY, MANATHIRST
    """
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}

    def play(self, target=None):
        # 将护卫阿斯塔洛置入手牌
        yield Give(CONTROLLER, "RLK_222t")
        # 法力渴求（5）：造成2点伤害
        if self.controller.max_mana >= 5 and target:
            yield Hit(target, 2)


class RLK_590:
    """太阳之井 (The Sunwell)
    用随机法术牌填满你的手牌。你每有一张其他手牌，本牌的法力值消耗便减少（1）点。
    """
    # 动态减费：每有一张其他手牌减少1费
    def cost_mod(self, card, cost):
        # 计算手牌中除了自己之外的卡牌数量
        other_cards_in_hand = len([c for c in card.controller.hand if c != card])
        return cost - other_cards_in_hand

    # 战吼：用随机法术填满手牌
    def play(self):
        # 计算手牌空位（最多10张手牌）
        hand_space = 10 - len(self.controller.hand)
        # 填满手牌空位，每次给予一张随机法术
        for _ in range(hand_space):
            yield Give(CONTROLLER, RandomSpell())


class RLK_591:
    """白骨领主霜语 (Bonelord Frostwhisper)
    亡语：在本局对战的剩余时间内，每回合中你的第一张牌法力值消耗为（0）点。你的英雄会在3回合后死亡。
    机制: DEATHRATTLE
    """
    deathrattle = (
        # 给控制者添加永久buff：每回合第一张牌费用为0
        Buff(CONTROLLER, "RLK_591e"),
        # 给控制者添加死亡倒计时buff：3回合后死亡
        Buff(CONTROLLER, "RLK_591e2")
    )


class RLK_591e:
    """白骨领主霜语增益 - 第一张牌0费 (Frostwhisper's Blessing)"""
    # 回合开始时重置标记
    events = OwnTurnBegin(CONTROLLER).on(
        SetAttr(CONTROLLER, "frostwhisper_first_card_played", False)
    )

    # 刷新手牌中所有卡牌的费用
    def update(self, entity):
        # 如果本回合还没打出第一张牌，则所有手牌减费到0
        if not getattr(entity, "frostwhisper_first_card_played", False):
            return Find(FRIENDLY_HAND) | Buff("RLK_591e_cost")
        return []


class RLK_591e2:
    """白骨领主霜语增益 - 死亡倒计时 (Death Countdown)"""
    # 初始化倒计时为3
    def apply(self, target):
        target.frostwhisper_turns_remaining = 3

    # 每回合开始时减少倒计时
    events = OwnTurnBegin(CONTROLLER).on(
        lambda self, entity: (
            setattr(entity, "frostwhisper_turns_remaining",
                   getattr(entity, "frostwhisper_turns_remaining", 3) - 1),
            Destroy(entity) if getattr(entity, "frostwhisper_turns_remaining", 0) <= 0 else None
        )
    )


class RLK_591e_cost:
    """白骨领主霜语增益 - 费用修改 (Cost Reduction)"""
    # 将费用设置为0
    tags = {GameTag.COST: 0}

    # 当卡牌被打出时，标记第一张牌已打出
    events = Play(OWNER).on(
        SetAttr(CONTROLLER, "frostwhisper_first_card_played", True)
    )


class RLK_592:
    """无敌 (Invincible)
    复生。战吼，亡语：随机使另一个友方亡灵获得+5/+5和嘲讽。
    机制: BATTLECRY, DEATHRATTLE, REBORN
    """
    tags = {GameTag.REBORN: True}

    # 战吼：随机使另一个友方亡灵获得+5/+5和嘲讽
    play = Buff(RANDOM(FRIENDLY_MINIONS + UNDEAD - SELF), "RLK_592e")

    # 亡语：随机使另一个友方亡灵获得+5/+5和嘲讽
    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS + UNDEAD), "RLK_592e")


class RLK_592e:
    """无敌增益 (Invincible's Blessing)"""
    tags = {
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
        GameTag.TAUNT: True
    }


class RLK_593:
    """洛瑟玛·塞隆 (Lor'themar Theron)
    战吼：使你牌库中所有随从牌的属性值翻倍。
    机制: BATTLECRY
    """
    # 战吼：遍历牌库中的所有随从，给予属性翻倍buff
    def play(self):
        for minion in self.controller.deck:
            if minion.type == CardType.MINION:
                yield Buff(minion, "RLK_593e")


class RLK_593e:
    """洛瑟玛·塞隆增益 (Lor'themar's Blessing)"""
    # 使用lambda函数动态计算翻倍后的属性值
    tags = {
        GameTag.ATK: lambda self, entity: entity.atk,  # 额外增加当前攻击力（相当于翻倍）
        GameTag.HEALTH: lambda self, entity: entity.health  # 额外增加当前生命值（相当于翻倍）
    }


