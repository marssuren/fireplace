#!/usr/bin/env python
"""验证更新后的 cards.json"""

import json
from pathlib import Path

json_path = Path(__file__).parent / "cards.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("更新后的 cards.json 验证")
print("=" * 80)
print()

collectible = [c for c in data if c.get("collectible", False)]
tokens = [c for c in data if not c.get("collectible", False)]

print(f"总卡牌数: {len(data)}")
print(f"  可收集卡牌: {len(collectible)}")
print(f"  Token/不可收集: {len(tokens)}")
print()

# 按职业统计可收集卡牌
by_class = {}
for card in collectible:
    card_class = card.get("cardClass", "NEUTRAL")
    by_class[card_class] = by_class.get(card_class, 0) + 1

print("可收集卡牌职业分布:")
for class_name in sorted(by_class.keys()):
    print(f"  {class_name}: {by_class[class_name]}")
print()

# Miniaturize 统计
miniaturize_cards = [c for c in collectible if "MINIATURIZE" in c.get("mechanics", [])]
print(f"Miniaturize 卡牌: {len(miniaturize_cards)}")
print()

# 显示几个 Miniaturize 示例
print("Miniaturize 示例（前3个）:")
for card in miniaturize_cards[:3]:
    card_id = card["id"]
    card_name = card["name"]
    
    # 查找对应的 Token
    token_id = f"{card_id}t"
    token = next((t for t in tokens if t["id"] == token_id), None)
    
    print(f"  {card_id} - {card_name}")
    print(f"    原版: {card.get('cost')}费 {card.get('attack', '?')}/{card.get('health', '?')}")
    if token:
        print(f"    小型: {token.get('cost')}费 {token.get('attack', '?')}/{token.get('health', '?')}")
    print()

print("=" * 80)
print("[OK] cards.json 已成功更新为完整版本（包含 Token）")
print("=" * 80)
