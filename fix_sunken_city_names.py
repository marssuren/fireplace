#!/usr/bin/env python3
"""
根据官方翻译修正沉没之城卡牌的中文名称和描述
"""

import json
import re
import os

# 读取官方翻译
with open('/Users/liangxinyu/Dev/Projects/MachineLearning/hearthstone_zero/fireplace/cards_zhCN.json', 'r', encoding='utf-8') as f:
    cards_zh = json.load(f)

# 转换为字典
cards_dict = {card['id']: card for card in cards_zh if card.get('id', '').startswith(('TSC_', 'TID_'))}

# 需要修正的卡牌名称映射（我的翻译 -> 官方翻译）
name_corrections = {
    # 圣骑士
    'TID_077': ('光芒', '光鳐'),
    'TSC_030': ('利维坦', '海兽号'),
    
    # 潜行者
    'TSC_916': ('去钓鱼', '垂钓时光'),
    'TSC_937': ('蟹巴托亚', '可拉巴托亚'),
    
    # 德鲁伊 - TSC_029是错误的，应该是TSC_656
    # 这个需要特殊处理
}

# 文件路径
base_path = '/Users/liangxinyu/Dev/Projects/MachineLearning/hearthstone_zero/fireplace/fireplace/cards/sunken_city'

修正计数 = 0

# 修正每个文件
for filename in os.listdir(base_path):
    if not filename.endswith('.py'):
        continue
    
    filepath = os.path.join(base_path, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 对每个需要修正的卡牌进行替换
    for card_id, (old_name, new_name) in name_corrections.items():
        # 替换类定义中的中文名称
        pattern = f'(class {card_id}:.*?""".*?- ){old_name}'
        replacement = f'\\1{new_name}'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 如果内容有变化，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        修正计数 += 1
        print(f"✅ 修正了 {filename}")

print(f"\n总计修正了 {修正计数} 个文件")

# 特殊处理：检查TSC_029的问题
print("\n" + "=" * 80)
print("检查TSC_029问题...")
print("=" * 80)

# TSC_029应该是"盖亚，巨力机甲"（法师）
# TSC_656应该是"奇迹生长"（德鲁伊）

if 'TSC_029' in cards_dict:
    card = cards_dict['TSC_029']
    print(f"\nTSC_029 官方信息：")
    print(f"  名称: {card.get('name')}")
    print(f"  职业: {card.get('cardClass')}")
    print(f"  类型: {card.get('type')}")
    print(f"  费用: {card.get('cost')}")
    print(f"  效果: {card.get('text', '')}")

if 'TSC_656' in cards_dict:
    card = cards_dict['TSC_656']
    print(f"\nTSC_656 官方信息：")
    print(f"  名称: {card.get('name')}")
    print(f"  职业: {card.get('cardClass')}")
    print(f"  类型: {card.get('type')}")
    print(f"  费用: {card.get('cost')}")
    print(f"  效果: {card.get('text', '')}")

print("\n⚠️ 需要手动修正druid.py中的TSC_029和TSC_656！")
