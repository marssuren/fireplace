"""
胜地历险记 - WARLOCK
"""
from ..utils import *


# COMMON

class VAC_939:
    """吃掉小鬼！ - Eat! The! Imp!
    Destroy a friendly minion to draw 3 cards.
    消灭一个友方随从以抽三张牌。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 消灭目标友方随从
        if TARGET:
            yield Destroy(TARGET)
            # 抽3张牌
            yield Draw(CONTROLLER) * 3


class VAC_940:
    """派对邪犬 - Party Fiend
    Battlecry: Summon two 1/1 Felbeasts. Deal 3 damage to your hero.
    战吼：召唤两只1/1的邪能兽。对你的英雄造成3点伤害。
    """
    mechanics = [GameTag.BATTLECRY]

    def play(self):
        # 召唤两只1/1邪能兽
        yield Summon(CONTROLLER, "VAC_940t") * 2
        # 对友方英雄造成3点伤害
        yield Hit(FRIENDLY_HERO, 3)


class VAC_942:
    """无畏的火焰杂耍者 - Fearless Flamejuggler
    Battlecry: Gain stats equal to the damage your hero has taken this turn.
    战吼：获得等同于你的英雄在本回合中所受伤害量的属性值。
    """
    mechanics = [GameTag.BATTLECRY]

    def play(self):
        # 获取本回合英雄受到的伤害
        # 需要从 Player 对象中获取 damage_taken_this_turn 属性
        damage = getattr(self.controller, 'damage_taken_this_turn', 0)

        if damage > 0:
            # 获得等量的攻击力和生命值
            yield Buff(SELF, "VAC_942e")


class VAC_942e:
    """无畏的火焰杂耍者增益效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 动态计算属性值
    def atk(self, i):
        # 从施法者获取伤害值
        damage = getattr(self.source.controller, 'damage_taken_this_turn', 0)
        return i + damage

    def max_health(self, i):
        damage = getattr(self.source.controller, 'damage_taken_this_turn', 0)
        return i + damage


class WORK_009:
    """月度魔范员工 - Imployee of the Month
    Battlecry: Give a friendly minion Lifesteal.
    战吼：使一个友方随从获得吸血。
    """
    mechanics = [GameTag.BATTLECRY]
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        if TARGET:
            # 给予吸血
            yield Buff(TARGET, "WORK_009e")


class WORK_009e:
    """吸血效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.LIFESTEAL: True,
    }


# RARE

class VAC_943:
    """祭献小鬼 - Sacrificial Imp
    Deathrattle: If it's your turn, summon a 6/6 Imp with Taunt.
    亡语：如果此时是你的回合，召唤一个6/6并具有嘲讽的小鬼。
    """
    mechanics = [GameTag.DEATHRATTLE]

    def deathrattle(self):
        # 检查是否是自己的回合
        if self.controller == self.game.current_player:
            # 召唤6/6嘲讽小鬼
            yield Summon(CONTROLLER, "VAC_943t")


class VAC_951:
    """"健康"饮品 - "Health" Drink
    Lifesteal. Deal $3 damage to a minion. <i>(3 Drinks left!)</i>
    吸血。对一个随从造成$3点伤害。（还剩3杯！）

    这是一个 Drink Spell（饮品法术），使用后会返回手牌，共可使用3次。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 对目标造成3点伤害（带吸血效果）
        if TARGET:
            # 吸血伤害：先造成伤害，然后治疗英雄
            damage_dealt = yield Hit(TARGET, 3)
            # 吸血效果：治疗等量生命值
            if damage_dealt:
                actual_damage = damage_dealt[0] if isinstance(damage_dealt, list) else damage_dealt
                if actual_damage > 0:
                    yield Heal(FRIENDLY_HERO, actual_damage)

        # 返回2杯版本到手牌
        yield Give(CONTROLLER, "VAC_951t")


class VAC_952:
    """邪能篝火 - Felfire Bonfire
    Deal $4 damage to a minion. If it dies, your next Deathrattle minion costs (3) less.
    对一个随从造成$4点伤害。如果该随从死亡，你的下一个亡语随从的法力值消耗减少（3）点。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        target = self.target
        if target:
            # 记录目标是否存活
            target_alive = target.zone == Zone.PLAY

            # 造成4点伤害
            yield Hit(target, 4)

            # 检查目标是否死亡
            if target_alive and target.zone != Zone.PLAY:
                # 目标死亡，给玩家添加buff
                yield Buff(CONTROLLER, "VAC_952e")


class VAC_952e:
    """邪能篝火效果 - 下一个亡语随从减3费"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 监听打出亡语随从
    events = Play(CONTROLLER, MINION + DEATHRATTLE).after(
        Destroy(SELF)  # 触发后移除buff
    )

    class Hand:
        # 手牌中的亡语随从减3费
        def cost_func(self, i):
            if self.owner.type == CardType.MINION and self.owner.has_deathrattle:
                return max(0, i - 3)
            return None


class WORK_007:
    """最后期限 - Deadline
    Tradeable, Temporary. Destroy a minion.
    可交易，临时。消灭一个随从。
    """
    mechanics = [GameTag.TRADEABLE]
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        if TARGET:
            yield Destroy(TARGET)


class WORK_008:
    """合约细则 - Fine Print
    Deal $4 damage to all minions. <i>(Excess damage hits your hero.)</i>
    对所有随从造成$4点伤害。（超过其生命值的伤害会命中你的英雄。）
    """
    mechanics = [GameTag.ImmuneToSpellpower]

    def play(self):
        # 对所有随从造成4点伤害，超出部分伤害英雄
        all_minions = list(self.game.board.filter(ALL_MINIONS))

        for minion in all_minions:
            # 计算实际伤害和溢出伤害
            current_health = minion.health
            damage_to_deal = 4

            # 造成伤害
            yield Hit(minion, damage_to_deal)

            # 如果伤害超过生命值，溢出伤害打到友方英雄
            if damage_to_deal > current_health:
                excess_damage = damage_to_deal - current_health
                yield Hit(FRIENDLY_HERO, excess_damage)


# EPIC

class VAC_941:
    """弃明投暗 - Announce Darkness
    Replace your Hero Power and non-Warlock cards with Warlock ones. They cost (1) less.
    将你的英雄技能和非术士卡牌替换成术士的。它们的法力值消耗减少（1）点。

    官方规则：
    1. 替换英雄技能为术士的"生命分流"，费用减1（变为1费）
    2. 替换手牌和牌库中的非术士卡牌（包括中立卡）为术士卡牌
    3. 所有新卡牌费用减1
    """
    def play(self):
        # 1. 替换英雄技能为术士的基础英雄技能 "生命分流" (Life Tap)
        # 参考 stormwind/warlock.py 的实现方式
        new_power = self.controller.card("CS2_056", source=self.controller.hero)
        self.controller.hero.power = new_power
        new_power.controller = self.controller
        new_power.zone = Zone.PLAY

        # 给新英雄技能减1费
        yield Buff(new_power, "VAC_941e")

        # 2. 替换手牌、牌库中的非术士卡牌（包括中立卡）
        zones_to_replace = [self.controller.hand, self.controller.deck]

        for zone in zones_to_replace:
            # 注意：中立卡也要替换！
            cards_to_replace = [c for c in list(zone) if c.card_class != CardClass.WARLOCK]

            for card in cards_to_replace:
                # 记录原卡的费用和类型
                original_cost = card.cost
                original_type = card.type

                # 移除原卡
                yield Destroy(card)

                # 生成一张术士卡牌（同类型、相近费用）
                new_card = yield Give(CONTROLLER, RandomCollectible(
                    card_class=CardClass.WARLOCK,
                    type=original_type,
                    cost=original_cost
                ))

                # 给新卡减1费
                if new_card:
                    yield Buff(new_card[0], "VAC_941e")


class VAC_941e:
    """弃明投暗减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    tags = {GameTag.COST: -1}


class VAC_944:
    """咒怨纪念品 - Cursed Souvenir
    Give a minion +3/+3 and "At the start of your turn, deal 3 damage to your hero."
    使一个随从获得+3/+3和"在你的回合开始时，对你的英雄造成3点伤害"。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        if TARGET:
            yield Buff(TARGET, "VAC_944e")


class VAC_944e:
    """咒怨纪念品效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }

    # 在回合开始时对友方英雄造成3点伤害
    events = OWN_TURN_BEGIN.on(
        Hit(FRIENDLY_HERO, 3)
    )


# LEGENDARY

class VAC_503:
    """召唤师达克玛洛 - Summoner Darkmarrow
    Death Knight Tourist. Your Deathrattles trigger twice. After you play a Deathrattle minion, destroy it.
    死亡骑士游客。你的亡语会触发两次。在你使用一张亡语随从牌后，将其消灭。
    """
    mechanics = [GameTag.AURA, GameTag.TRIGGER_VISUAL]

    # 亡语触发两次的光环效果
    update = Refresh(FRIENDLY_MINIONS + DEATHRATTLE)

    class Board:
        # 场上的亡语随从触发两次
        def extra_deathrattles(self, i):
            return i + 1

    # 监听打出亡语随从
    events = Play(CONTROLLER, MINION + DEATHRATTLE).after(
        lambda self, source, card, *args: card.deathrattles and Destroy(card)
    )


class VAC_945:
    """派对策划者沃娜 - Party Planner Vona
    Battlecry: If you've taken 8 damage on your turns, summon Ourobos.
    战吼：如果你在你的回合中受到过8点伤害，召唤乌洛波斯。
    """
    mechanics = [GameTag.BATTLECRY]

    def play(self):
        # 检查在自己回合中受到的总伤害（本局游戏累计）
        # 使用核心已有的属性: damage_taken_on_own_turn_this_game
        damage = self.controller.damage_taken_on_own_turn_this_game

        if damage >= 8:
            # 召唤乌洛波斯 (Ourobos)
            yield Summon(CONTROLLER, "VAC_945t")
