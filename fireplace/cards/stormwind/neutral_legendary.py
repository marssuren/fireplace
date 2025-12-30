# -*- coding: utf-8 -*-
"""
暴风城（United in Stormwind）- 中立传说
"""

from ..utils import *


class DED_006:
    """重拳先生 / Mr. Smite
    Your Pirates have Charge."""
    update = Refresh(FRIENDLY_MINIONS + PIRATE, {GameTag.CHARGE: True})


class DED_525:
    """哥利亚，斯尼德的杰作 / Goliath, Sneed's Masterpiece
    Battlecry: Fire five rockets at enemy minions that deal 2 damage each. (You pick the targets!)"""
    # 玩家选择5次目标，每次造成2点伤害
    play = (
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2) &
        Find(ENEMY_MINIONS) & Hit(TARGET, 2)
    )


class SW_045:
    """拍卖师亚克森 / Auctioneer Jaxon
    Whenever you Trade, Discover a card from your deck to draw instead."""
    events = Trade(CONTROLLER).on(
        GenericChoice(CONTROLLER, Discover(CONTROLLER, FRIENDLY_DECK))
    )


class SW_078:
    """普瑞斯托女士 / Lady Prestor
    Battlecry: Transform minions in your deck into random Dragons. (They keep their original stats and Cost.)"""
    # 将牌库中的所有随从变形为随机龙，保持原始属性和费用
    play = lambda self: [
        Transform(minion, RandomMinion(race=Race.DRAGON, cost=minion.cost, atk=minion.atk, health=minion.health))
        for minion in self.controller.deck
        if minion.type == CardType.MINION
    ]


class SW_079:
    """飞行管理员杜加尔 / Flightmaster Dungar
    Battlecry: Choose a flightpath and go Dormant. Awaken with a bonus when you complete it!"""
    # 选择飞行路线：短途、中途、长途
    play = GenericChoice(CONTROLLER, [
        "SW_079a",  # 短途：2回合后苏醒，抽1张牌
        "SW_079b",  # 中途：3回合后苏醒，抽2张牌
        "SW_079c",  # 长途：4回合后苏醒，抽3张牌
    ])


class SW_080:
    """考内留斯·罗姆 / Cornelius Roame
    At the start and end of each player's turn, draw a card."""
    events = [
        OwnTurnBegins(CONTROLLER).on(Draw(CONTROLLER)),
        OwnTurnEnds(CONTROLLER).on(Draw(CONTROLLER)),
        OwnTurnBegins(OPPONENT).on(Draw(CONTROLLER)),
        OwnTurnEnds(OPPONENT).on(Draw(CONTROLLER))
    ]


class SW_081:
    """瓦里安，暴风城国王 / Varian, King of Stormwind
    Battlecry: Draw a Rush minion to gain Rush. Repeat for Taunt and Divine Shield."""
    play = (
        # 抽一张突袭随从，获得突袭
        Find(FRIENDLY_DECK + MINION + RUSH) & (
            Draw(CONTROLLER, TARGET) & SetTag(SELF, {GameTag.RUSH: True})
        ) &
        # 抽一张嘲讽随从，获得嘲讽
        Find(FRIENDLY_DECK + MINION + TAUNT) & (
            Draw(CONTROLLER, TARGET) & SetTag(SELF, {GameTag.TAUNT: True})
        ) &
        # 抽一张圣盾随从，获得圣盾
        Find(FRIENDLY_DECK + MINION + DIVINE_SHIELD) & (
            Draw(CONTROLLER, TARGET) & SetTag(SELF, {GameTag.DIVINE_SHIELD: True})
        )
    )
