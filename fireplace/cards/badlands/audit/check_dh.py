import json

with open('cards.json', encoding='utf-8') as f:
    data = json.load(f)

dh_cards = [c for c in data if c.get('cardClass') == 'DEMONHUNTER' or 'DEMONHUNTER' in c.get('classes', [])]
print(f'Found {len(dh_cards)} DH cards')
for c in dh_cards:
    print(f"{c['id']}: {c['name']} - {c.get('text', '')}")
