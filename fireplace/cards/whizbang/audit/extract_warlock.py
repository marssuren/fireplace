#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
提取 Warlock 卡牌数据
"""
import json

# 读取 cards.json
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 筛选 Warlock 卡牌
warlock_cards = [
    card for card in all_cards
    if card.get('cardClass') == 'WARLOCK' 
    and card.get('set') == 'WHIZBANGS_WORKSHOP'
    and card.get('collectible', False)  # 只要可收集卡牌
]

# 按稀有度和费用排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
warlock_cards.sort(key=lambda c: (rarity_order.get(c.get('rarity', ''), 5), c.get('cost', 0)))

print(f"找到 {len(warlock_cards)} 张 Warlock 卡牌\n")
print("=" * 80)

for card in warlock_cards:
    print(f"\nID: {card['id']}")
    print(f"名称: {card.get('name', 'N/A')}")
    print(f"稀有度: {card.get('rarity', 'N/A')}")
    print(f"类型: {card.get('type', 'N/A')}")
    print(f"费用: {card.get('cost', 'N/A')}")
    
    if card.get('type') == 'MINION':
        print(f"属性: {card.get('attack', 0)}/{card.get('health', 0)}")
        if card.get('race'):
            print(f"种族: {card.get('race')}")
    
    if card.get('type') == 'WEAPON':
        print(f"武器: {card.get('attack', 0)}/{card.get('durability', 0)}")
    
    if card.get('mechanics'):
        print(f"机制: {', '.join(card.get('mechanics', []))}")
    
    if card.get('text'):
        print(f"效果: {card.get('text')}")
    
    print("-" * 80)

# 保存到文件
with open('warlock_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(warlock_cards, f, ensure_ascii=False, indent=2)

with open('warlock_cards_data.txt', 'w', encoding='utf-8') as f:
    for card in warlock_cards:
        f.write(f"\n{'=' * 80}\n")
        f.write(f"ID: {card['id']}\n")
        f.write(f"名称: {card.get('name', 'N/A')}\n")
        f.write(f"稀有度: {card.get('rarity', 'N/A')}\n")
        f.write(f"类型: {card.get('type', 'N/A')}\n")
        f.write(f"费用: {card.get('cost', 'N/A')}\n")
        
        if card.get('type') == 'MINION':
            f.write(f"属性: {card.get('attack', 0)}/{card.get('health', 0)}\n")
            if card.get('race'):
                f.write(f"种族: {card.get('race')}\n")
        
        if card.get('type') == 'WEAPON':
            f.write(f"武器: {card.get('attack', 0)}/{card.get('durability', 0)}\n")
        
        if card.get('mechanics'):
            f.write(f"机制: {', '.join(card.get('mechanics', []))}\n")
        
        if card.get('text'):
            f.write(f"效果: {card.get('text')}\n")

print(f"\n数据已保存到 warlock_cards_data.json 和 warlock_cards_data.txt")
