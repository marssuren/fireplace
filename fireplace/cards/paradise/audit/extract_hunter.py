"""
提取 Paradise 扩展包中的 Hunter 卡牌数据
"""
import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选 Hunter 卡牌 (cardClass = "HUNTER" 且 set = "ISLAND_VACATION")
hunter_cards = [
    card for card in all_cards
    if card.get('cardClass') == 'HUNTER' and card.get('set') == 'ISLAND_VACATION'
]

# 按稀有度和费用排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
hunter_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', 'COMMON'), 0), x.get('cost', 0)))

# 输出到文件
with open('hunter_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(hunter_cards, f, ensure_ascii=False, indent=2)

# 打印摘要
print(f"找到 {len(hunter_cards)} 张 Hunter 卡牌")
for card in hunter_cards:
    print(f"- {card.get('id')}: {card.get('name')} ({card.get('rarity')}) - {card.get('text', '')[:50]}")
