#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分析 Gigantify 机制"""
import json
from pathlib import Path

# 读取卡牌数据
cards_file = Path(__file__).parent / "cards.json"
with open(cards_file, encoding='utf-8') as f:
    cards = json.load(f)

print("=" * 80)
print("【Gigantify 机制分析】")
print("=" * 80)

gigantify_cards = [c for c in cards if 'GIGANTIFY' in c.get('mechanics', [])]
print(f"\nGigantify 卡牌数量: {len(gigantify_cards)}\n")

for i, card in enumerate(gigantify_cards):
    print(f"{i+1}. {card['id']} - {card['name']}")
    print(f"   费用: {card.get('cost', 0)} | 攻击: {card.get('attack', 0)} | 生命: {card.get('health', 0)}")
    print(f"   描述: {card.get('text', '')}")
    print()
