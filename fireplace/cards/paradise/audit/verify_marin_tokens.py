import json

# 读取卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("验证 Marin the Manager 的 Token ID")
print("=" * 60)

# 查找Marin相关的Token
marin_tokens = [card for card in data if 'VAC_702' in card.get('id', '') and not card.get('collectible', False)]

print(f"\n找到 {len(marin_tokens)} 个 VAC_702 相关Token:\n")
for card in marin_tokens:
    print(f"ID: {card['id']}")
    print(f"名称: {card.get('name', 'N/A')}")
    print(f"类型: {card.get('type', 'N/A')}")
    print(f"描述: {card.get('text', 'N/A')[:80]}")
    print("-" * 60)

# 同时查找LOOT_998系列（Kobolds宝藏）
print("\n" + "=" * 60)
print("查找 LOOT_998 系列宝藏（Kobolds & Catacombs）")
print("=" * 60)

loot_tokens = [card for card in data if 'LOOT_998' in card.get('id', '')]
print(f"\n找到 {len(loot_tokens)} 个 LOOT_998 相关Token:\n")
for card in loot_tokens[:10]:
    print(f"ID: {card['id']}")
    print(f"名称: {card.get('name', 'N/A')}")
    print(f"扩展包: {card.get('set', 'N/A')}")
    print("-" * 60)
