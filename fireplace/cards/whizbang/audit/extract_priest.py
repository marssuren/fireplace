#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取 Priest 卡牌数据
"""
import json

with open('cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 筛选 Priest 卡牌 (PRIEST)
priest_cards = [card for card in data if card.get('cardClass') == 'PRIEST' and card.get('collectible')]

# 按稀有度排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
priest_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', ''), 5), x.get('cost', 0)))

output = []
output.append(f"找到 {len(priest_cards)} 张 Priest 卡牌\n")
output.append("="*80)

for card in priest_cards:
    output.append(f"\n【{card.get('rarity', 'UNKNOWN')}】 {card.get('id')} - {card.get('name')}")
    output.append(f"  类型: {card.get('type')}, 费用: {card.get('cost')}")
    if card.get('type') == 'MINION':
        output.append(f"  属性: {card.get('attack')}/{card.get('health')}")
    if card.get('mechanics'):
        output.append(f"  机制: {', '.join(card.get('mechanics', []))}")
    if card.get('referencedTags'):
        output.append(f"  标签: {', '.join(card.get('referencedTags', []))}")
    output.append(f"  描述: {card.get('text', '')}")

output.append("\n" + "="*80)
output.append(f"\n总计: {len(priest_cards)} 张卡牌")

# 写入文件
with open('priest_cards_data.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

# 同时输出 JSON 格式
with open('priest_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(priest_cards, f, ensure_ascii=False, indent=2)

print("数据已保存到 priest_cards_data.txt 和 priest_cards_data.json")
