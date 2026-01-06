#!/usr/bin/env python
"""
威兹班的工坊 (Whizbang's Workshop) 卡牌实现验证工具

用途：
1. 验证所有卡牌是否已实现
2. 检查卡牌基础属性（费用、攻击、生命）是否与官方数据一致
3. 生成实现进度报告
"""

import json
import os
import sys
from pathlib import Path

# 添加 fireplace 到路径
FIREPLACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(FIREPLACE_ROOT))

from fireplace import cards as fireplace_cards
from fireplace.enums import CardClass, CardType, Rarity


# 职业映射
CLASS_MAP = {
    "DEATHKNIGHT": CardClass.DEATHKNIGHT,
    "DEMONHUNTER": CardClass.DEMONHUNTER,
    "DRUID": CardClass.DRUID,
    "HUNTER": CardClass.HUNTER,
    "MAGE": CardClass.MAGE,
    "PALADIN": CardClass.PALADIN,
    "PRIEST": CardClass.PRIEST,
    "ROGUE": CardClass.ROGUE,
    "SHAMAN": CardClass.SHAMAN,
    "WARLOCK": CardClass.WARLOCK,
    "WARRIOR": CardClass.WARRIOR,
    "NEUTRAL": CardClass.NEUTRAL,
}

CLASS_FILES = {
    CardClass.DEATHKNIGHT: "deathknight",
    CardClass.DEMONHUNTER: "demonhunter",
    CardClass.DRUID: "druid",
    CardClass.HUNTER: "hunter",
    CardClass.MAGE: "mage",
    CardClass.PALADIN: "paladin",
    CardClass.PRIEST: "priest",
    CardClass.ROGUE: "rogue",
    CardClass.SHAMAN: "shaman",
    CardClass.WARLOCK: "warlock",
    CardClass.WARRIOR: "warrior",
    CardClass.NEUTRAL: "neutral",
}

RARITY_MAP = {
    "COMMON": Rarity.COMMON,
    "RARE": Rarity.RARE,
    "EPIC": Rarity.EPIC,
    "LEGENDARY": Rarity.LEGENDARY,
    "FREE": Rarity.FREE,
}

TYPE_MAP = {
    "MINION": CardType.MINION,
    "SPELL": CardType.SPELL,
    "WEAPON": CardType.WEAPON,
    "HERO": CardType.HERO,
    "LOCATION": CardType.LOCATION,
}


def load_official_data():
    """加载官方卡牌数据"""
    json_path = Path(__file__).parent / "cards.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 只保留可收集卡牌
    collectible = [c for c in data if c.get("collectible", False)]
    return {c["id"]: c for c in collectible}


def check_card_implementation(card_id, official_data):
    """检查单张卡牌的实现状态"""
    try:
        card_class = fireplace_cards.db[card_id]
        
        # 检查是否只是占位符
        source = card_class.__dict__
        is_placeholder = (
            not hasattr(card_class, "play") and
            not hasattr(card_class, "update") and
            not hasattr(card_class, "events") and
            not hasattr(card_class, "powered_up") and
            len([k for k in source.keys() if not k.startswith("_")]) == 0
        )
        
        if is_placeholder:
            return {
                "status": "placeholder",
                "implemented": False,
                "message": "仅占位符，未实现"
            }
        
        # 验证基础属性
        issues = []
        official = official_data[card_id]
        
        # 检查费用
        if "cost" in official:
            expected_cost = official["cost"]
            actual_cost = getattr(card_class, "cost", None)
            if actual_cost != expected_cost:
                issues.append(f"费用不匹配: 期望 {expected_cost}, 实际 {actual_cost}")
        
        # 检查攻击力（仅随从和武器）
        if official.get("type") in ["MINION", "WEAPON"] and "attack" in official:
            expected_atk = official["attack"]
            actual_atk = getattr(card_class, "atk", None)
            if actual_atk != expected_atk:
                issues.append(f"攻击力不匹配: 期望 {expected_atk}, 实际 {actual_atk}")
        
        # 检查生命值/耐久度
        if official.get("type") == "MINION" and "health" in official:
            expected_health = official["health"]
            actual_health = getattr(card_class, "health", None)
            if actual_health != expected_health:
                issues.append(f"生命值不匹配: 期望 {expected_health}, 实际 {actual_health}")
        elif official.get("type") == "WEAPON" and "durability" in official:
            expected_dur = official["durability"]
            actual_dur = getattr(card_class, "durability", None)
            if actual_dur != expected_dur:
                issues.append(f"耐久度不匹配: 期望 {expected_dur}, 实际 {actual_dur}")
        
        if issues:
            return {
                "status": "incorrect",
                "implemented": True,
                "message": "; ".join(issues)
            }
        
        return {
            "status": "ok",
            "implemented": True,
            "message": "已实现"
        }
        
    except KeyError:
        return {
            "status": "missing",
            "implemented": False,
            "message": "未找到实现"
        }
    except Exception as e:
        return {
            "status": "error",
            "implemented": False,
            "message": f"检查出错: {str(e)}"
        }


def generate_report():
    """生成验证报告"""
    print("=" * 80)
    print("威兹班的工坊 (Whizbang's Workshop) 卡牌实现验证报告")
    print("=" * 80)
    print()
    
    # 加载官方数据
    official_data = load_official_data()
    print(f"📊 官方数据: {len(official_data)} 张可收集卡牌")
    print()
    
    # 按职业分组
    by_class = {}
    for card_id, card_data in official_data.items():
        card_class = card_data.get("cardClass", "NEUTRAL")
        if card_class not in by_class:
            by_class[card_class] = []
        by_class[card_class].append(card_id)
    
    # 统计
    total_cards = 0
    implemented_cards = 0
    placeholder_cards = 0
    missing_cards = 0
    incorrect_cards = 0
    
    # 按职业验证
    for class_name in sorted(by_class.keys()):
        card_ids = sorted(by_class[class_name])
        class_total = len(card_ids)
        class_implemented = 0
        class_placeholder = 0
        class_missing = 0
        class_incorrect = 0
        
        print(f"## {class_name} ({class_total} 张)")
        print("-" * 80)
        
        issues = []
        for card_id in card_ids:
            result = check_card_implementation(card_id, official_data)
            total_cards += 1
            
            if result["status"] == "ok":
                class_implemented += 1
                implemented_cards += 1
            elif result["status"] == "placeholder":
                class_placeholder += 1
                placeholder_cards += 1
                card_name = official_data[card_id].get("name", card_id)
                issues.append(f"  ⚠️  {card_id} ({card_name}): {result['message']}")
            elif result["status"] == "missing":
                class_missing += 1
                missing_cards += 1
                card_name = official_data[card_id].get("name", card_id)
                issues.append(f"  ❌ {card_id} ({card_name}): {result['message']}")
            elif result["status"] == "incorrect":
                class_incorrect += 1
                incorrect_cards += 1
                card_name = official_data[card_id].get("name", card_id)
                issues.append(f"  🔧 {card_id} ({card_name}): {result['message']}")
        
        # 显示职业统计
        completion = (class_implemented / class_total * 100) if class_total > 0 else 0
        status_icon = "✅" if completion == 100 else "🟡" if completion > 0 else "❌"
        print(f"{status_icon} 完成度: {class_implemented}/{class_total} ({completion:.1f}%)")
        
        if class_placeholder > 0:
            print(f"   占位符: {class_placeholder}")
        if class_missing > 0:
            print(f"   缺失: {class_missing}")
        if class_incorrect > 0:
            print(f"   属性错误: {class_incorrect}")
        
        # 显示问题
        if issues:
            print()
            for issue in issues:
                print(issue)
        
        print()
    
    # 总体统计
    print("=" * 80)
    print("📈 总体统计")
    print("=" * 80)
    print(f"总卡牌数: {total_cards}")
    print(f"✅ 已完成: {implemented_cards} ({implemented_cards/total_cards*100:.1f}%)")
    print(f"⚠️  占位符: {placeholder_cards} ({placeholder_cards/total_cards*100:.1f}%)")
    print(f"❌ 缺失: {missing_cards} ({missing_cards/total_cards*100:.1f}%)")
    print(f"🔧 属性错误: {incorrect_cards} ({incorrect_cards/total_cards*100:.1f}%)")
    print()
    
    overall_completion = (implemented_cards / total_cards * 100) if total_cards > 0 else 0
    if overall_completion == 100:
        print("🎉 恭喜！所有卡牌已完成实现！")
    else:
        remaining = total_cards - implemented_cards
        print(f"🎯 还需实现 {remaining} 张卡牌")
    print()


if __name__ == "__main__":
    generate_report()
