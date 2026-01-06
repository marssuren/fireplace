#!/usr/bin/env python
"""查找 Miniaturize 的中文名称"""

import json
from pathlib import Path

json_path = Path(__file__).parent / "cards.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 找到一张 Miniaturize 卡牌
mini_cards = [c for c in data if "MINIATURIZE" in c.get("mechanics", []) and c.get("collectible", False)]

print("=" * 80)
print("Miniaturize 机制中文名称查找")
print("=" * 80)
print()

# 显示前5张卡牌的描述
for i, card in enumerate(mini_cards[:5], 1):
    print(f"{i}. {card['id']} - {card['name']}")
    print(f"   费用: {card.get('cost')} | 身材: {card.get('attack', '?')}/{card.get('health', '?')}")
    text = card.get("text", "")
    print(f"   描述: {text}")
    print()
    
    # 尝试提取中文关键词
    if "微缩" in text:
        print("   ✓ 找到关键词: 微缩")
    if "小型化" in text:
        print("   ✓ 找到关键词: 小型化")
    if "Miniaturize" in text:
        print("   ✓ 找到关键词: Miniaturize")
    print()

# 查看 Token 卡牌的描述
print("=" * 80)
print("Token 卡牌描述")
print("=" * 80)
print()

token = next((t for t in data if t["id"] == "MIS_025t"), None)
if token:
    print(f"Token: {token['id']} - {token['name']}")
    print(f"描述: {token.get('text', 'N/A')}")
