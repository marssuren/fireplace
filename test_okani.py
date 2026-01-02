# -*- coding: utf-8 -*-
"""
测试剑圣奥卡尼（TSC_032）的秘密选择机制
"""

import pytest
from fireplace import cards
from fireplace.game import Game
from fireplace.player import Player
from hearthstone.enums import CardClass, Zone


def test_okani_secret_choice():
    """测试奥卡尼的秘密选择机制"""
    # 创建游戏
    player1 = Player("Player1", ["TSC_032"] * 30, CardClass.MAGE)
    player2 = Player("Player2", ["CS2_118"] * 30, CardClass.MAGE)  # 火球术
    game = Game(players=(player1, player2))
    game.start()
    
    # 跳过 mulligan
    for player in game.players:
        if player.choice:
            player.choice.choose()
    
    # 玩家1打出奥卡尼
    okani_card = player1.give("TSC_032")
    player1.give("THE_COIN")  # 给硬币以支付费用
    okani_card.play()
    
    # 验证奥卡尼在场上
    assert len(player1.field) == 1
    okani = player1.field[0]
    assert okani.id == "TSC_032"
    assert okani.atk == 2
    assert okani.health == 6
    
    # 验证玩家有选择（秘密选择）
    assert player1.choice is not None
    assert hasattr(player1.choice, 'secret')  # 验证是秘密选择
    assert player1.choice.secret == True
    
    # 选择反制随从
    choice_cards = player1.choice.cards
    assert len(choice_cards) == 2
    counter_minion = [c for c in choice_cards if c.id == "TSC_032a"][0]
    player1.choice.choose(counter_minion)
    
    # 验证奥卡尼获得了反制随从的buff
    assert len(okani.buffs) == 1
    assert okani.buffs[0].id == "TSC_032e_minion"
    
    # 玩家2打出一个随从
    game.end_turn()
    minion = player2.give("CS2_118")  # 火球术（实际上应该是随从，这里简化）
    
    print("✅ 奥卡尼的秘密选择机制测试通过！")


def test_okani_counter_spell():
    """测试奥卡尼反制法术"""
    player1 = Player("Player1", ["TSC_032"] * 30, CardClass.MAGE)
    player2 = Player("Player2", ["CS2_029"] * 30, CardClass.MAGE)  # 火球术
    game = Game(players=(player1, player2))
    game.start()
    
    # 跳过 mulligan
    for player in game.players:
        if player.choice:
            player.choice.choose()
    
    # 玩家1打出奥卡尼并选择反制法术
    okani_card = player1.give("TSC_032")
    player1.give("THE_COIN")
    okani_card.play()
    
    # 选择反制法术
    choice_cards = player1.choice.cards
    counter_spell = [c for c in choice_cards if c.id == "TSC_032b"][0]
    player1.choice.choose(counter_spell)
    
    okani = player1.field[0]
    assert len(okani.buffs) == 1
    assert okani.buffs[0].id == "TSC_032e_spell"
    
    print("✅ 奥卡尼反制法术测试通过！")


if __name__ == "__main__":
    test_okani_secret_choice()
    test_okani_counter_spell()
    print("\n🎉 所有测试通过！")
