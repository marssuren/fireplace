# -*- coding: utf-8 -*-
"""
奥特兰克的决裂（Fractured in Alterac Valley）- 潜行者
"""

from ..utils import *


class AV_201:
    """冷牙雪人 / Coldtooth Yeti
    连击：获得+3攻击力。"""
    combo = Buff(SELF, "AV_201e")


class AV_201e:
    """冷牙雪人增益"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 3,
    }


class AV_402:
    """脑叶切除器 / The Lobotomizer
    荣誉消灭：获得对手牌库顶的一张牌的复制。"""
    def honorable_kill(self):
        """获得对手牌库顶的一张牌的复制"""
        if self.controller.opponent.deck:
            top_card = self.controller.opponent.deck[-1]  # 牌库顶是列表的最后一个元素
            yield Give(CONTROLLER, Copy(top_card))


class AV_601:
    """被遗忘的中尉 / Forsaken Lieutenant
    潜行。在你使用一张亡语随从后，变形成为它的2/2复制，并具有突袭。"""
    events = Play(CONTROLLER, MINION + DEATHRATTLE).after(
        (Morph(SELF, Copy(Play.CARD)),
         SetTag(SELF, {GameTag.ATK: 2, GameTag.HEALTH: 2}),
         SetTag(SELF, {GameTag.RUSH: True}))
    )


class AV_710:
    """侦察 / Reconnaissance
    发现一张其他职业的亡语随从牌。其法力值消耗减少（2）点。"""
    play = GenericChoice(CONTROLLER, Discover(
        CONTROLLER,
        # 从非潜行者职业的亡语随从中发现（包括中立）
        RandomCollectible(card_class=~CardClass.ROGUE, type=CardType.MINION, mechanics=[GameTag.DEATHRATTLE])
    )).then(lambda card: Buff(card, "AV_710e"))


class AV_710e:
    """侦察减费"""
    tags = {GameTag.COST: -2}


class ONY_032:
    """奈法利安之牙 / Tooth of Nefarian
    造成$3点伤害。荣誉消灭：发现一张其他职业的法术牌。"""
    play = Hit(TARGET, 3)
    honorable_kill = GenericChoice(CONTROLLER, Discover(
        CONTROLLER,
        RandomCollectible(card_class=~CardClass.ROGUE, type=CardType.SPELL)
    ))


class AV_711:
    """双面间谍 / Double Agent
    战吼：如果你的手牌中有其他职业的牌，召唤一个本随从的复制。"""
    powered_up = Find(FRIENDLY_HAND + FuncSelector(
        lambda entities, src: [e for e in entities if hasattr(e, 'card_class') and e.card_class != CardClass.ROGUE and e.card_class != CardClass.NEUTRAL]
    ))
    play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class ONY_030:
    """军情七处走私者 / SI:7 Smuggler
    战吼：如果你的手牌中有其他职业的牌，抽两张牌。"""
    powered_up = Find(FRIENDLY_HAND + FuncSelector(
        lambda entities, src: [e for e in entities if hasattr(e, 'card_class') and e.card_class != CardClass.ROGUE and e.card_class != CardClass.NEUTRAL]
    ))
    play = powered_up & (Draw(CONTROLLER) * 2)


class ONY_031:
    """烟幕 / Smokescreen
    你的随从获得潜行，直到你的下个回合。"""
    play = Buff(FRIENDLY_MINIONS, "ONY_031e")


class ONY_031e:
    """烟幕效果"""
    tags = {GameTag.STEALTH: True}
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class AV_298:
    """野爪豺狼人 / Wildpaw Gnoll
    突袭。在本局对战中，每有一张非潜行者职业的牌加入你的手牌，本牌的法力值消耗便减少（1）点。"""
    cost_mod = lambda self, i: -getattr(self.controller, 'non_rogue_cards_added_to_hand', 0)


class AV_400:
    """雪落墓地 / Snowfall Graveyard
    你的亡语触发两次。持续3回合。"""
    play = Buff(FRIENDLY_HERO, "AV_400e")


class AV_400e:
    """雪落墓地效果"""
    tags = {GameTag.EXTRA_DEATHRATTLES: 1}
    turns_remaining = 3

    events = OWN_TURN_END.on(
        lambda self: (
            setattr(self, 'turns_remaining', self.turns_remaining - 1),
            self.turns_remaining <= 0 and Destroy(SELF)
        )[-1] if self.turns_remaining > 0 else Destroy(SELF)
    )


class AV_403:
    """塞拉辛·疾行者 / Cera'thine Fleetrunner
    战吼：将你手牌和牌库中的随从替换为其他职业的随从。这些随从的法力值消耗减少（2）点。"""
    def play(self):
        """替换手牌和牌库中的随从为其他职业的随从"""
        # 替换手牌中的随从
        for minion in list(self.controller.hand):
            if minion.type == CardType.MINION:
                # 变形为其他职业的随机随从，并获取新卡牌引用
                new_card = yield Morph(minion, RandomCollectible(
                    card_class=~CardClass.ROGUE,
                    type=CardType.MINION
                ))
                # 给予减费buff（使用变形后的新卡牌）
                if new_card:
                    yield Buff(new_card, "AV_403e")

        # 替换牌库中的随从
        for minion in list(self.controller.deck):
            if minion.type == CardType.MINION:
                # 变形为其他职业的随机随从，并获取新卡牌引用
                new_card = yield Morph(minion, RandomCollectible(
                    card_class=~CardClass.ROGUE,
                    type=CardType.MINION
                ))
                # 给予减费buff（使用变形后的新卡牌）
                if new_card:
                    yield Buff(new_card, "AV_403e")



class AV_403e:
    """塞拉辛·疾行者减费"""
    tags = {GameTag.COST: -2}


class AV_405:
    """违禁品藏匿处 / Contraband Stash
    重新使用本局对战中你使用过的5张其他职业的牌。"""
    def play(self):
        """重新使用本局对战中使用过的其他职业的牌"""
        # 筛选其他职业的牌（排除潜行者和中立）
        other_class_cards = [
            card for card in self.controller.cards_played_this_game
            if hasattr(card, 'card_class') and
               card.card_class != CardClass.ROGUE and
               card.card_class != CardClass.NEUTRAL
        ]

        # 随机选择最多5张牌
        if not other_class_cards:
            return

        cards_to_replay = self.game.random.sample(
            other_class_cards,
            min(5, len(other_class_cards))
        )

        # 重新使用这些牌
        for card in cards_to_replay:
            if card.type == CardType.SPELL:
                # 重新施放法术
                yield CastSpell(CONTROLLER, Copy(card))
            elif card.type == CardType.MINION:
                # 召唤随从
                yield Summon(CONTROLLER, Copy(card))
            elif card.type == CardType.WEAPON:
                # 装备武器
                yield Summon(CONTROLLER, Copy(card))



class AV_203:
    """暗影工匠斯卡布斯 / Shadowcrafter Scabbs
    战吼：将所有随从移回其拥有者的手牌。召唤两个4/2并具有潜行的暗影。"""
    play = (
        Bounce(ALL_MINIONS),
        Summon(CONTROLLER, "AV_203t") * 2
    )


class AV_203t:
    """暗影 / Shadow
    4/2 潜行"""
    # 在 CardDefs.xml 中定义

