"""
提取 Paradise 中立史诗卡牌数据
"""
import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

# 中立史诗卡牌ID列表
neutral_epic_ids = [
    "VAC_439",    # 海滨巨人 - Seaside Giant
    "VAC_447",    # 恐惧的逃亡者 - Dread Deserter
    "VAC_523",    # 混调师 - Mixologist
    "VAC_935",    # 随行肉虫 - Carry-On Grub
    "VAC_958",    # 进化融合怪 - Adaptive Amalgam
    "WORK_042",   # 食肉格块 - Carnivorous Cubicle
]

# 提取中立史诗卡牌
neutral_epic_cards = []
for card in all_cards:
    if card.get('id') in neutral_epic_ids:
        neutral_epic_cards.append(card)

# 按ID顺序排序
neutral_epic_cards.sort(key=lambda x: neutral_epic_ids.index(x['id']))

# 保存到文件
with open('neutral_epic_cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(neutral_epic_cards, f, ensure_ascii=False, indent=2)

print(f"已提取 {len(neutral_epic_cards)} 张中立史诗卡牌数据")
for card in neutral_epic_cards:
    print(f"  - {card['id']}: {card.get('name', 'Unknown')}")
