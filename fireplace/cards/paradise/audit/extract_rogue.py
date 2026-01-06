import json

# 读取完整的 cards.json
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选 Rogue 职业卡牌
rogue_cards = [
    card for card in all_cards 
    if card.get('cardClass') == 'ROGUE' and card.get('collectible') == True
]

# 按稀有度和费用排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
rogue_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', ''), 5), x.get('cost', 0)))

# 保存到文件
with open('rogue_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(rogue_cards, f, ensure_ascii=False, indent=4)

# 打印卡牌信息
print(f"找到 {len(rogue_cards)} 张 Rogue 卡牌：\n")
for card in rogue_cards:
    print(f"[{card.get('rarity', 'UNKNOWN')}] {card.get('id')} - {card.get('name')} ({card.get('cost')}费)")
    print(f"  类型: {card.get('type')}")
    if card.get('text'):
        print(f"  效果: {card.get('text')}")
    print()
