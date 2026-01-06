#!/usr/bin/env python3
"""
提取 Warrior 卡牌数据
"""
import json

# 读取 cards.json
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选 Warrior 卡牌
warrior_cards = [card for card in all_cards if card.get('cardClass') == 'WARRIOR']

# 按稀有度排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
warrior_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', ''), 5), x.get('id', '')))

# 输出详细信息
print(f"找到 {len(warrior_cards)} 张 Warrior 卡牌\n")
print("=" * 80)

for card in warrior_cards:
    print(f"\nID: {card.get('id')}")
    print(f"名称: {card.get('name')} ({card.get('text', 'N/A')})")
    print(f"稀有度: {card.get('rarity')}")
    print(f"类型: {card.get('type')}")
    print(f"费用: {card.get('cost')}")
    
    if card.get('type') == 'MINION':
        print(f"属性: {card.get('attack')}/{card.get('health')}")
    elif card.get('type') == 'WEAPON':
        print(f"属性: {card.get('attack')}/{card.get('durability')}")
    
    if card.get('mechanics'):
        print(f"机制: {', '.join(card.get('mechanics', []))}")
    
    if card.get('text'):
        print(f"效果: {card.get('text')}")
    
    if card.get('race'):
        print(f"种族: {card.get('race')}")
    
    print("-" * 80)

# 保存到文件
with open('warrior_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(warrior_cards, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到 warrior_cards_data.json")
