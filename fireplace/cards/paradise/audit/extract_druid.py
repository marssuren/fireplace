"""
提取 Paradise 扩展包中的 Druid 卡牌数据
"""
import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选 Druid 卡牌
druid_cards = [
    card for card in all_cards
    if card.get('cardClass') == 'DRUID' and card.get('set') == 'ISLAND_VACATION'
]

# 按稀有度排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
druid_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', ''), 5), x.get('id', '')))

# 保存结果
with open('druid_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(druid_cards, f, ensure_ascii=False, indent=2)

print(f"提取了 {len(druid_cards)} 张 Druid 卡牌")
for card in druid_cards:
    print(f"  {card['id']}: {card.get('name', 'Unknown')} ({card.get('rarity', 'Unknown')})")
