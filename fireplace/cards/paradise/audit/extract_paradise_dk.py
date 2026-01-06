#!/usr/bin/env python3
"""
提取 Paradise Death Knight 卡牌数据
"""
import json

# 读取 cards.json
CARDS_PATH = r"D:\Projects\Yolo\hearthstone_zero\fireplace\fireplace\cards\233025\zhCN\cards.game_playable.json"
try:
    with open(CARDS_PATH, 'r', encoding='utf-8') as f:
        all_cards = json.load(f)
except FileNotFoundError:
    print(f"Error: {CARDS_PATH} not found.")
    exit(1)

# 筛选 Death Knight 卡牌 (由 cardClass 判断)
# Token 可能没有 cardClass 或者 cardClass 是 NEUTRAL，我们需要通过 ID 关联
# 这里我们提取所有 set 为 ISLAND_VACATION 的不可收集卡牌作为潜在 Token
dk_cards = [card for card in all_cards if card.get('cardClass') == 'DEATHKNIGHT' and card.get('set') == 'ISLAND_VACATION' and card.get('collectible')]
tokens = [card for card in all_cards if card.get('set') == 'ISLAND_VACATION' and not card.get('collectible')]

# 尝试找到与 DK 卡牌相关的 Token
related_tokens = []
for card in dk_cards:
    card_id = card.get('id')
    # 简单的关联规则：Token ID 以 Card ID 开头
    related = [t for t in tokens if t.get('id', '').startswith(card_id)]
    related_tokens.extend(related)

# 去重
related_tokens = list({t['id']: t for t in related_tokens}.values())

dk_cards.extend(related_tokens)

# 按稀有度排序
rarity_order = {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}
dk_cards.sort(key=lambda x: (rarity_order.get(x.get('rarity', ''), 5), x.get('id', '')))

# 输出详细信息
print(f"找到 {len(dk_cards)} 张 Death Knight 卡牌\n")
print("=" * 80)

for card in dk_cards:
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
    
    if card.get('spellSchool'):
        print(f"法术派系: {card.get('spellSchool')}")

    print("-" * 80)

# 保存到文件
with open('deathknight_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(dk_cards, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到 deathknight_cards_data.json")
