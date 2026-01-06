#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分析 Whizbang's Workshop 核心机制"""
import json
from pathlib import Path

# 读取卡牌数据
cards_file = Path(__file__).parent / "cards.json"
with open(cards_file, encoding='utf-8') as f:
    cards = json.load(f)

# 分析 Miniaturize 机制
print("=" * 80)
print("【Miniaturize 机制分析】")
print("=" * 80)
miniaturize_cards = [c for c in cards if 'MINIATURIZE' in c.get('mechanics', [])]
print(f"\nMiniaturize 卡牌数量: {len(miniaturize_cards)}\n")

for card in miniaturize_cards[:5]:
    print(f"ID: {card['id']}")
    print(f"名称: {card['name']}")
    print(f"费用: {card.get('cost', 0)} | 攻击: {card.get('attack', 0)} | 生命: {card.get('health', 0)}")
    print(f"描述: {card.get('text', '')[:100]}")
    
    # 查找对应的 token
    token_id = card['id'] + 't'
    token = next((c for c in cards if c['id'] == token_id), None)
    if token:
        print(f"  → Token: {token['id']} - {token['name']}")
        print(f"     费用: {token.get('cost', 0)} | 攻击: {token.get('attack', 0)} | 生命: {token.get('health', 0)}")
        print(f"     描述: {token.get('text', '')[:100]}")
    print()

# 分析 Gigantify 机制
print("\n" + "=" * 80)
print("【Gigantify 机制分析】")
print("=" * 80)
gigantify_cards = [c for c in cards if 'GIGANTIFY' in c.get('mechanics', [])]
print(f"\nGigantify 卡牌数量: {len(gigantify_cards)}\n")

for card in gigantify_cards[:5]:
    print(f"ID: {card['id']}")
    print(f"名称: {card['name']}")
    print(f"费用: {card.get('cost', 0)} | 攻击: {card.get('attack', 0)} | 生命: {card.get('health', 0)}")
    print(f"描述: {card.get('text', '')[:100]}")
    print()

# 分析同时拥有两种机制的卡牌
print("\n" + "=" * 80)
print("【同时拥有 Miniaturize 和 Gigantify 的卡牌】")
print("=" * 80)
both_mechanics = [c for c in cards if 'MINIATURIZE' in c.get('mechanics', []) and 'GIGANTIFY' in c.get('mechanics', [])]
print(f"\n数量: {len(both_mechanics)}\n")

for card in both_mechanics:
    print(f"ID: {card['id']}")
    print(f"名称: {card['name']}")
    print(f"费用: {card.get('cost', 0)} | 攻击: {card.get('attack', 0)} | 生命: {card.get('health', 0)}")
    print(f"描述: {card.get('text', '')[:150]}")
    
    # 查找所有相关 token
    base_id = card['id']
    tokens = [c for c in cards if c['id'].startswith(base_id + 't')]
    for token in tokens:
        print(f"  → Token: {token['id']} - {token['name']}")
        print(f"     费用: {token.get('cost', 0)} | 攻击: {token.get('attack', 0)} | 生命: {token.get('health', 0)}")
        print(f"     描述: {token.get('text', '')[:100]}")
    print()

# 统计所有 Token 卡牌
print("\n" + "=" * 80)
print("【Token 卡牌统计】")
print("=" * 80)
all_tokens = [c for c in cards if not c.get('collectible', True)]
print(f"\n总 Token 数量: {len(all_tokens)}")

miniaturize_tokens = [c for c in all_tokens if c['id'].endswith('t') and not c['id'].endswith('t1') and any(c['id'].startswith(m['id']) for m in miniaturize_cards)]
print(f"Miniaturize Token 数量: {len(miniaturize_tokens)}")

gigantify_tokens = [c for c in all_tokens if c['id'].endswith('t1')]
print(f"Gigantify Token 数量: {len(gigantify_tokens)}")

print("\n示例 Miniaturize Token:")
for token in miniaturize_tokens[:3]:
    print(f"  {token['id']} - {token['name']} ({token.get('cost', 0)}费 {token.get('attack', 0)}/{token.get('health', 0)})")

print("\n示例 Gigantify Token:")
for token in gigantify_tokens[:3]:
    print(f"  {token['id']} - {token['name']} ({token.get('cost', 0)}费 {token.get('attack', 0)}/{token.get('health', 0)})")
