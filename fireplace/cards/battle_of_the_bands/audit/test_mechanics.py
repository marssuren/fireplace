# -*- coding: utf-8 -*-
"""
传奇音乐节 - 核心机制测试
测试关键机制的基本功能：Finale、Overload、Location、Predamage 等
"""
import sys
import os

# 添加 fireplace 到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from fireplace import cards
from fireplace.game import Game
from fireplace.player import Player
from fireplace.card import Card
from fireplace.enums import CardClass, CardType, Zone
from fireplace.exceptions import GameOver

def setup_game():
    """创建一个基础游戏环境"""
    cards.db.initialize()
    
    player1 = Player("Player1", [], CardClass.MAGE, GameType.FT_RANKED)
    player2 = Player("Player2", [], CardClass.WARRIOR, GameType.FT_RANKED)
    
    game = Game(players=(player1, player2))
    game.start()
    
    return game, player1, player2

def test_finale_mechanism():
    """测试压轴机制 - ETC_205 (DJ Manastorm)"""
    print("\n[测试 1] 压轴机制 (Finale)")
    print("-" * 50)
    
    try:
        game, p1, p2 = setup_game()
        
        # 给玩家足够的法力
        p1.max_mana = 9
        p1.mana = 9
        
        # 创建 DJ Manastorm (ETC_205) - 9费，压轴：将手牌法力值设为0
        dj = p1.give("ETC_205")
        dj.zone = Zone.HAND
        
        # 给手牌添加一些卡
        for _ in range(3):
            card = p1.give("CS2_029")  # Fireball
            card.zone = Zone.HAND
        
        initial_costs = [c.cost for c in p1.hand if c != dj]
        print(f"   初始手牌费用: {initial_costs}")
        
        # 打出 DJ（应该触发压轴）
        dj.play()
        
        final_costs = [c.cost for c in p1.hand]
        print(f"   压轴后手牌费用: {final_costs}")
        
        if all(cost == 0 for cost in final_costs):
            print("   ✅ 压轴机制正常工作")
            return True
        else:
            print("   ❌ 压轴机制未生效")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

def test_overload_mechanism():
    """测试过载机制 - ETC_370 (Pack the House)"""
    print("\n[测试 2] 过载机制 (Overload)")
    print("-" * 50)
    
    try:
        game, p1, p2 = setup_game()
        
        p1.max_mana = 10
        p1.mana = 10
        
        # Pack the House - 7费，过载(2)
        card = p1.give("ETC_370")
        card.zone = Zone.HAND
        
        print(f"   施放前: 法力 {p1.mana}/{p1.max_mana}, 过载 {p1.overloaded}")
        
        card.play()
        
        print(f"   施放后: 法力 {p1.mana}/{p1.max_mana}, 过载 {p1.overloaded}")
        
        # 结束回合，检查下回合锁定的法力
        game.end_turn()
        game.end_turn()  # 对手回合
        
        print(f"   下回合: 法力 {p1.mana}/{p1.max_mana}, 锁定 {p1.locked_mana}")
        
        if p1.locked_mana == 2:
            print("   ✅ 过载机制正常工作")
            return True
        else:
            print("   ❌ 过载锁定异常")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

def test_location_mechanism():
    """测试地标机制 - JAM_009 (Dance Floor)"""
    print("\n[测试 3] 地标机制 (Location)")
    print("-" * 50)
    
    try:
        game, p1, p2 = setup_game()
        
        p1.max_mana = 10
        p1.mana = 10
        
        # 召唤一个随从
        minion = p1.give("CS2_189")  # Elven Archer
        minion.play()
        
        # 打出地标
        location = p1.give("JAM_009")
        location.zone = Zone.HAND
        
        print(f"   地标耐久: {location.health if hasattr(location, 'health') else 'N/A'}")
        print(f"   场上随从: {len(p1.field)}")
        
        location.play()
        
        print(f"   地标已打出，类型: {location.type}")
        
        if location.type == CardType.LOCATION:
            print("   ✅ 地标机制基础正常")
            return True
        else:
            print("   ❌ 地标类型异常")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

def test_predamage_mechanism():
    """测试伤害预防机制 - ETC_084 (Felstring Harp)"""
    print("\n[测试 4] 伤害预防机制 (Predamage)")
    print("-" * 50)
    
    try:
        game, p1, p2 = setup_game()
        
        p1.max_mana = 10
        p1.mana = 10
        
        # 装备 Felstring Harp
        weapon = p1.give("ETC_084")
        weapon.zone = Zone.HAND
        weapon.play()
        
        initial_health = p1.hero.health
        print(f"   初始生命: {initial_health}")
        print(f"   武器已装备: {p1.weapon}")
        
        # 尝试对英雄造成伤害（在自己回合）
        p1.hero.damage(5)
        
        final_health = p1.hero.health
        print(f"   受伤后生命: {final_health}")
        
        # Felstring Harp 应该将伤害转为治疗
        if final_health > initial_health:
            print("   ✅ 伤害预防机制正常工作")
            return True
        else:
            print("   ⚠️  伤害预防可能未生效（需检查回合状态）")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

def main():
    print("=" * 60)
    print("传奇音乐节 - 核心机制测试")
    print("=" * 60)
    
    results = []
    
    # 运行所有测试
    results.append(("Finale", test_finale_mechanism()))
    results.append(("Overload", test_overload_mechanism()))
    results.append(("Location", test_location_mechanism()))
    results.append(("Predamage", test_predamage_mechanism()))
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:15s} {status}")
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 所有核心机制测试通过！")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，需要进一步检查")

if __name__ == '__main__':
    main()
