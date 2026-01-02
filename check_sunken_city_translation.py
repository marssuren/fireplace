#!/usr/bin/env python3
"""
检查沉没之城卡牌的中文翻译和实现是否一致
"""

import json
import re
import os

# 读取中文翻译
with open('/Users/liangxinyu/Dev/Projects/MachineLearning/hearthstone_zero/fireplace/cards_zhCN.json', 'r', encoding='utf-8') as f:
    cards_zh = json.load(f)

# 转换为字典
cards_dict = {card['id']: card for card in cards_zh if card.get('id', '').startswith(('TSC_', 'TID_'))}

print("=" * 80)
print("沉没之城卡牌翻译和实现一致性检查")
print("=" * 80)

# 需要检查的卡牌列表（从我们的实现中提取）
issues = []

# 检查一些关键卡牌
check_cards = [
    # 德鲁伊
    ('TID_081', '水栖形态', '抽一张牌。如果你在本回合打出过娜迦牌，再抽一张牌。'),
    ('TID_082', '月光指引', '抽一张牌。如果你在本回合打出过法术牌，再抽一张牌。'),
    ('TSC_029', '奇迹生长', '选择一项：使一个随从获得+2/+2；或使其获得+4/+4。'),
    
    # 圣骑士
    ('TID_077', '光芒', '嘲讽。你每打出一张圣骑士牌，本牌的法力值消耗便减少(1)点。'),
    ('TSC_030', '利维坦', '巨型+1 突袭，圣盾 在本随从攻击后，疏浚。'),
    
    # 潜行者
    ('TSC_916', '去钓鱼', '疏浚。连击：抽一张牌。'),
    ('TSC_937', '蟹巴托亚', '巨型+2 你的蟹巴托亚之爪获得+2攻击力。'),
]

for card_id, expected_name, expected_text in check_cards:
    if card_id in cards_dict:
        card = cards_dict[card_id]
        actual_name = card.get('name', '')
        actual_text = card.get('text', '').replace('<b>', '').replace('</b>', '').replace('$', '')
        
        # 检查名称
        if actual_name != expected_name:
            issues.append({
                'id': card_id,
                'type': '名称不匹配',
                'expected': expected_name,
                'actual': actual_name
            })
        
        # 检查描述（简化比较）
        if expected_text and expected_text not in actual_text and actual_text not in expected_text:
            issues.append({
                'id': card_id,
                'type': '描述可能不匹配',
                'expected': expected_text[:50],
                'actual': actual_text[:50]
            })

print(f"\n检查了 {len(check_cards)} 张卡牌")
print(f"发现 {len(issues)} 个潜在问题\n")

if issues:
    print("发现的问题：")
    print("-" * 80)
    for issue in issues:
        print(f"\n卡牌ID: {issue['id']}")
        print(f"问题类型: {issue['type']}")
        print(f"期望值: {issue['expected']}")
        print(f"实际值: {issue['actual']}")
else:
    print("✅ 所有检查的卡牌翻译和实现一致！")

print("\n" + "=" * 80)
print("现在检查所有沉没之城卡牌的中文翻译...")
print("=" * 80)

# 列出所有卡牌
print(f"\n共有 {len(cards_dict)} 张沉没之城卡牌")
print("\n按职业分类：")

# 按职业分类
classes = {}
for card_id, card in cards_dict.items():
    class_name = card.get('cardClass', 'NEUTRAL')
    if class_name not in classes:
        classes[class_name] = []
    classes[class_name].append((card_id, card.get('name', 'Unknown')))

for class_name, cards in sorted(classes.items()):
    print(f"\n{class_name}: {len(cards)}张")
    for card_id, name in sorted(cards)[:3]:  # 只显示前3张
        print(f"  {card_id}: {name}")
    if len(cards) > 3:
        print(f"  ... 还有 {len(cards) - 3} 张")

print("\n" + "=" * 80)
