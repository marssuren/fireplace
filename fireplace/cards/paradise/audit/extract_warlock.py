import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 筛选术士卡牌
warlock_cards = [c for c in data if c.get('cardClass') == 'WARLOCK' and c.get('collectible')]

# 按稀有度和费用排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
warlock_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', 'COMMON'), 0), x.get('cost', 0)))

# 输出
print(f"找到 {len(warlock_cards)} 张术士卡牌：\n")
for card in warlock_cards:
    print(f"ID: {card['id']}")
    print(f"名称: {card['name']}")
    print(f"费用: {card.get('cost', 'N/A')}")
    print(f"稀有度: {card.get('rarity', 'N/A')}")
    print(f"类型: {card.get('type', 'N/A')}")
    if card.get('type') == 'MINION':
        print(f"身材: {card.get('attack', 0)}/{card.get('health', 0)}")
    print(f"效果: {card.get('text', 'N/A')}")
    print(f"机制: {card.get('mechanics', [])}")
    print("-" * 80)

# 保存到文件
with open('warlock_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(warlock_cards, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到 warlock_cards_data.json")
