#!/usr/bin/env python
"""查找 Whizbang's Workshop 的 Token 卡牌"""

import json
from pathlib import Path

json_path = Path(__file__).parent / "cards.json"
with open(json_path, "r", encoding="utf-8") as f:
    all_data = json.load(f)

print("=" * 80)
print("威兹班的工坊 Token 卡牌分析")
print("=" * 80)
print()

# 统计
collectible = [c for c in all_data if c.get('collectible', False)]
non_collectible = [c for c in all_data if not c.get('collectible', False)]

print(f"可收集卡牌: {len(collectible)}")
print(f"Token/不可收集卡牌: {len(non_collectible)}")
print()

# 查找 Miniaturize 卡牌
print("=" * 80)
print("Miniaturize 卡牌及其 Token")
print("=" * 80)
print()

miniaturize_cards = [c for c in collectible if 'MINIATURIZE' in c.get('mechanics', [])]
all_cards_dict = {c['id']: c for c in all_data}

for card in miniaturize_cards[:10]:
    card_id = card['id']
    card_name = card['name']
    
    # 尝试查找对应的 Token（通常是 {ID}t 或 {ID}a）
    possible_tokens = [
        f"{card_id}t",
        f"{card_id}a",
        f"{card_id}_MINI",
    ]
    
    found_token = None
    for token_id in possible_tokens:
        if token_id in all_cards_dict:
            found_token = all_cards_dict[token_id]
            break
    
    print(f"{card_id} - {card_name}")
    print(f"  费用: {card.get('cost', 'N/A')} | 类型: {card.get('type', 'N/A')}")
    if card.get('type') == 'MINION':
        print(f"  身材: {card.get('attack', '?')}/{card.get('health', '?')}")
    
    if found_token:
        print(f"  -> Token: {found_token['id']} - {found_token.get('name', 'N/A')}")
        print(f"     费用: {found_token.get('cost', 'N/A')} | 类型: {found_token.get('type', 'N/A')}")
        if found_token.get('type') == 'MINION':
            print(f"     身材: {found_token.get('attack', '?')}/{found_token.get('health', '?')}")
    else:
        print(f"  -> Token: 未找到（可能需要手动查找）")
    
    print()

print("=" * 80)
print("所有 Token 卡牌列表（前30个）")
print("=" * 80)
print()

for token in non_collectible[:30]:
    print(f"{token['id']} - {token.get('name', 'N/A')}")
    print(f"  类型: {token.get('type', 'N/A')} | 费用: {token.get('cost', 'N/A')}")
    if 'text' in token:
        text = token['text'][:80]
        print(f"  描述: {text}")
    print()
