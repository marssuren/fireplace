import json

# 读取 cards.json
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选圣骑士卡牌
paladin_cards = [card for card in all_cards if card.get('cardClass') == 'PALADIN' and card.get('collectible')]

# 按稀有度排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
paladin_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', ''), 5), x.get('cost', 0)))

# 输出详细信息
print(f"找到 {len(paladin_cards)} 张圣骑士卡牌：\n")
for card in paladin_cards:
    print(f"ID: {card['id']}")
    print(f"名称: {card['name']}")
    print(f"稀有度: {card.get('rarity', 'N/A')}")
    print(f"费用: {card.get('cost', 'N/A')}")
    print(f"类型: {card.get('type', 'N/A')}")
    if card.get('type') == 'MINION':
        print(f"属性: {card.get('attack', 0)}/{card.get('health', 0)}")
    elif card.get('type') == 'WEAPON':
        print(f"属性: {card.get('attack', 0)}/{card.get('durability', 0)}")
    elif card.get('type') == 'LOCATION':
        print(f"生命值: {card.get('health', 0)}")
    print(f"效果: {card.get('text', 'N/A')}")
    print(f"机制: {card.get('mechanics', [])}")
    print("-" * 80)

# 保存到文件
with open('paladin_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(paladin_cards, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到 paladin_cards_data.json")
