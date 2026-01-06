import json

with open('cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

paladin_cards = [c for c in data if c.get('cardClass') == 'PALADIN' and 'WHIZBANG' in c.get('set', '')]

print(f'Found {len(paladin_cards)} Paladin cards\n')

for card in sorted(paladin_cards, key=lambda x: (x.get('cost', 0), x.get('id'))):
    print(f"ID: {card['id']}")
    print(f"Name: {card.get('name', 'N/A')}")
    print(f"Cost: {card.get('cost', 'N/A')}")
    print(f"Type: {card.get('type', 'N/A')}")
    print(f"Rarity: {card.get('rarity', 'N/A')}")
    print(f"Text: {card.get('text', 'N/A')}")
    print(f"Mechanics: {card.get('mechanics', [])}")
    if card.get('attack') is not None:
        print(f"Attack: {card.get('attack')}")
    if card.get('health') is not None:
        print(f"Health: {card.get('health')}")
    print('-' * 80)
