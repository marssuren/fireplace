# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立史诗
"""

from ..utils import *


class DED_521:
    """最疯狂的爆破者 / Maddest Bomber
    Battlecry: Deal 12 damage randomly split among all other characters."""
    play = Hit(ALL_CHARACTERS - SELF, 1) * 12


class SW_069:
    """热情的柜员 / Enthusiastic Banker
    At the end of your turn, store a card from your deck. Deathrattle: Add the stored cards to your hand."""
    events = OwnTurnEnds(CONTROLLER).on(
        Find(FRIENDLY_DECK) & (
            Setaside(RANDOM(FRIENDLY_DECK)) & Buff(SELF, "SW_069e")
        )
    )
    deathrattle = lambda self: [Give(self.controller, card) for card in getattr(self, 'stored_cards', [])]


class SW_069e:
    """热情的柜员存储"""
    def apply(self, target):
        if not hasattr(target, 'stored_cards'):
            target.stored_cards = []
        # 存储最近被移到暂存区的卡牌
        setaside_cards = [c for c in target.game.entities if c.zone == Zone.SETASIDE and c.controller == target.controller]
        if setaside_cards:
            target.stored_cards.append(setaside_cards[-1])


class SW_073:
    """奶酪商贩 / Cheesemonger
    Whenever your opponent casts a spell, add a random spell with the same Cost to your hand."""
    events = CastSpell(OPPONENT).on(
        Give(CONTROLLER, RandomSpell(cost=COST(CastSpell.CARD)))
    )


class SW_074:
    """贵族 / Nobleman
    Battlecry: Create a Golden copy of a random card in your hand."""
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY_HAND)))


class SW_075:
    """艾尔文野猪 / Elwynn Boar
    Deathrattle: If you had 7 Elwynn Boars die this game, equip a 15/3 Sword of a Thousand Truths."""
    # 需要追踪本局游戏中死亡的艾尔文野猪数量
    deathrattle = Buff(FRIENDLY_HERO, "SW_075e")


class SW_075e:
    """艾尔文野猪计数器"""
    def apply(self, target):
        # 增加死亡计数
        if not hasattr(target, 'elwynn_boars_died'):
            target.elwynn_boars_died = 0
        target.elwynn_boars_died += 1

        # 如果达到7只，装备武器
        if target.elwynn_boars_died >= 7:
            from ..actions import Summon
            Summon(target.controller, "SW_075t").trigger(target)


class SW_075t:
    """千真剑 / Sword of a Thousand Truths"""
    # 15/3 武器，在 CardDefs.xml 中定义
    pass


class SW_077:
    """监狱囚徒 / Stockades Prisoner
    Starts Dormant. After you play 3 cards, this awakens."""
    # 休眠机制：打出3张牌后苏醒
    # 需要在控制器级别追踪打出的卡牌数量
    events = Play(CONTROLLER).after(
        Buff(FRIENDLY_HERO, "SW_077e")
    )


class SW_077e:
    """监狱囚徒计数器"""
    def apply(self, target):
        # 增加打出卡牌计数
        if not hasattr(target, 'cards_played_for_prisoner'):
            target.cards_played_for_prisoner = 0
        target.cards_played_for_prisoner += 1

        # 如果达到3张，唤醒所有监狱囚徒
        if target.cards_played_for_prisoner >= 3:
            prisoners = [m for m in target.controller.field if m.id == "SW_077" and m.dormant]
            for prisoner in prisoners:
                prisoner.dormant = False
