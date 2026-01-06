import json

with open('cards.json', encoding='utf-8') as f:
    cards = json.load(f)

dk_cards = [c for c in cards if c.get('cardClass') == 'DEATHKNIGHT' and c.get('collectible')]

print(f'Found {len(dk_cards)} Death Knight collectible cards\n')

for c in dk_cards:
    card_id = c['id']
    name = c['name']
    cost = c.get('cost', 'N/A')
    card_type = c.get('type', 'UNKNOWN')
    
    if card_type == 'MINION':
        atk = c.get('attack', '?')
        hp = c.get('health', '?')
        print(f"{card_id}: {name} - {cost}费 {atk}/{hp}")
    elif card_type == 'SPELL':
        print(f"{card_id}: {name} - {cost}费法术")
    elif card_type == 'WEAPON':
        atk = c.get('attack', '?')
        dur = c.get('durability', '?')
        print(f"{card_id}: {name} - {cost}费武器 {atk}/{dur}")
    else:
        print(f"{card_id}: {name} - {cost}费 {card_type}")
    
    text = c.get('text', '')
    if text:
        print(f"  效果: {text}")
    print()
