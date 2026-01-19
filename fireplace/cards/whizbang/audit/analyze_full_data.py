#!/usr/bin/env python
"""分析完整的卡牌数据，查找 Whizbang's Workshop 的 Token 卡"""

import json
from pathlib import Path

# 加载完整的卡牌数据
full_data_path = r"G:\Projects\Yolo\hearthstone_zero\fireplace\fireplace\cards\233275\zhCN\cards.game_playable.json"
with open(full_data_path, "r", encoding="utf-8") as f:
    all_cards = json.load(f)

print("=" * 80)
print("Whizbang's Workshop 完整卡牌数据分析")
print("=" * 80)
print()

# 筛选 Whizbang 卡牌
whizbang_cards = [c for c in all_cards if c.get("set") == "WHIZBANGS_WORKSHOP"]
print(f"Whizbang 卡牌总数: {len(whizbang_cards)}")

# 分类
collectible = [c for c in whizbang_cards if c.get("collectible", False)]
tokens = [c for c in whizbang_cards if not c.get("collectible", False)]

print(f"  可收集卡牌: {len(collectible)}")
print(f"  Token/不可收集: {len(tokens)}")
print()

# 查找 Miniaturize Token
print("=" * 80)
print("Miniaturize Token 卡牌")
print("=" * 80)
print()

miniaturize_collectible = [c for c in collectible if "MINIATURIZE" in c.get("mechanics", [])]
print(f"拥有 MINIATURIZE 的可收集卡牌: {len(miniaturize_collectible)}")
print()

# 尝试匹配 Token
for card in miniaturize_collectible[:5]:
    card_id = card["id"]
    card_name = card["name"]
    
    # 查找可能的 Token ID
    possible_token_ids = [
        f"{card_id}t",
        f"{card_id}a",
        f"{card_id}_MINI",
        f"{card_id}m",
    ]
    
    found_tokens = []
    for token in tokens:
        if token["id"] in possible_token_ids or card_id in token.get("id", ""):
            found_tokens.append(token)
    
    print(f"{card_id} - {card_name}")
    print(f"  费用: {card.get('cost', 'N/A')} | 类型: {card.get('type', 'N/A')}")
    if card.get("type") == "MINION":
        print(f"  身材: {card.get('attack', '?')}/{card.get('health', '?')}")
    
    if found_tokens:
        for token in found_tokens:
            print(f"  -> Token: {token['id']} - {token.get('name', 'N/A')}")
            print(f"     费用: {token.get('cost', 'N/A')} | 类型: {token.get('type', 'N/A')}")
            if token.get("type") == "MINION":
                print(f"     身材: {token.get('attack', '?')}/{token.get('health', '?')}")
    else:
        print(f"  -> 未找到明显的 Token")
    print()

# 显示所有 Token 卡牌
print("=" * 80)
print(f"所有 Token 卡牌列表（共 {len(tokens)} 张）")
print("=" * 80)
print()

for token in tokens[:30]:
    print(f"{token['id']} - {token.get('name', 'N/A')}")
    print(f"  类型: {token.get('type', 'N/A')} | 费用: {token.get('cost', 'N/A')}")
    if token.get("type") == "MINION":
        print(f"  身材: {token.get('attack', '?')}/{token.get('health', '?')}")
    if "text" in token:
        text = token["text"][:100]
        print(f"  描述: {text}")
    print()

# 导出完整的 Whizbang 数据（包含 Token）
output_path = Path(__file__).parent / "cards_with_tokens.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(whizbang_cards, f, ensure_ascii=False, indent=2)

print("=" * 80)
print(f"已导出完整数据到: {output_path}")
print(f"  可收集: {len(collectible)}")
print(f"  Token: {len(tokens)}")
print(f"  总计: {len(whizbang_cards)}")
print("=" * 80)
