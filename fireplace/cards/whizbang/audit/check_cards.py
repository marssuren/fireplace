import json

with open('cards.json', encoding='utf-8') as f:
    cards = json.load(f)

# 查找特定的 Death Knight 卡牌
target_ids = ['TOY_827', 'TOY_823', 'TOY_829', 'TOY_830']

for card_id in target_ids:
    card = next((c for c in cards if c['id'] == card_id), None)
    if card:
        print(f'\n=== {card_id} ===')
        print(json.dumps(card, indent=2, ensure_ascii=False))
