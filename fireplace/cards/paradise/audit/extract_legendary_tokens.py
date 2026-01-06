import json

# 读取卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取相关Token
keywords = ['爆发', '宝藏', '奶酪', '护符', '旅行', 'Eruption', 'Treasure', 'Cheese', 'Amulet', 'Tour']
tokens = []

for card in data:
    if card.get('set') == 'ISLAND_VACATION' and card.get('collectible') == False:
        name = card.get('name', '')
        if any(keyword in name for keyword in keywords):
            tokens.append(card)

print(f'找到 {len(tokens)} 个相关Token')
for card in tokens:
    print(f"{card['id']}: {card['name']} - {card.get('text', '')[:50]}")

# 保存到文件
with open('legendary_tokens.json', 'w', encoding='utf-8') as f:
    json.dump(tokens, f, ensure_ascii=False, indent=2)
