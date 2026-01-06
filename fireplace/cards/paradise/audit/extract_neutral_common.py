"""
提取 Paradise 扩展包中立普通卡牌数据
"""
import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选中立普通卡牌
neutral_common_cards = []
for card in all_cards:
    # 检查是否为 Paradise 扩展包的中立普通卡牌
    if (card.get('set') == 'ISLAND_VACATION' and 
        card.get('cardClass') == 'NEUTRAL' and 
        card.get('rarity') == 'COMMON' and
        card.get('collectible') == True):
        neutral_common_cards.append(card)

# 按卡牌ID排序
neutral_common_cards.sort(key=lambda x: x.get('id', ''))

# 保存到文件
with open('neutral_common_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(neutral_common_cards, f, ensure_ascii=False, indent=2)

# 打印统计信息
print(f"找到 {len(neutral_common_cards)} 张中立普通卡牌")
print("\n卡牌列表:")
for card in neutral_common_cards:
    print(f"  {card['id']}: {card.get('name', 'Unknown')} ({card.get('cost', '?')} 费)")
