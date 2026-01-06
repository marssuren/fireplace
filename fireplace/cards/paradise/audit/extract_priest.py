"""
提取 Paradise 扩展包的 Priest 卡牌数据
"""
import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选 Priest 卡牌
priest_cards = []
for card in all_cards:
    # 检查是否为 Priest 卡牌且属于 ISLAND_VACATION 扩展包
    if (card.get('cardClass') == 'PRIEST' and 
        card.get('set') == 'ISLAND_VACATION' and
        card.get('collectible') == True):
        priest_cards.append(card)

# 按稀有度和费用排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
priest_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', 'COMMON'), 0), x.get('cost', 0)))

# 输出结果
print(f"找到 {len(priest_cards)} 张 Priest 卡牌：\n")
for card in priest_cards:
    print(f"ID: {card.get('id')}")
    print(f"名称: {card.get('name')} ({card.get('text', 'N/A')})")
    print(f"稀有度: {card.get('rarity')}")
    print(f"费用: {card.get('cost')}")
    print(f"类型: {card.get('type')}")
    if card.get('type') == 'MINION':
        print(f"身材: {card.get('attack')}/{card.get('health')}")
    print(f"描述: {card.get('text', 'N/A')}")
    print(f"机制: {card.get('mechanics', [])}")
    print("-" * 80)

# 保存到文件
with open('priest_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(priest_cards, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到 priest_cards_data.json")
