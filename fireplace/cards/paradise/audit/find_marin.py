import json

with open('cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 查找Paradise扩展包的所有非收集卡
all_tokens = [c for c in data if not c.get('collectible', False) and c.get('set') == 'ISLAND_VACATION']

# 查找与Marin宝藏相关的Token
keywords = ['marin', 'zarog', 'wondrous', 'golden kobold', 'tolin', 'treasure', 'crown', 'wand', 'goblet']
marin_related = []

for card in all_tokens:
    name = card.get('name', '').lower()
    text = card.get('text', '').lower()
    if any(keyword in name or keyword in text for keyword in keywords):
        marin_related.append(card)

print(f"找到 {len(marin_related)} 个可能相关的Token:")
for c in marin_related:
    print(f"\nID: {c['id']}")
    print(f"名称: {c.get('name', 'N/A')}")
    print(f"类型: {c.get('type', 'N/A')}")
    print(f"描述: {c.get('text', 'N/A')[:100]}")
