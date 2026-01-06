import json

with open('cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

dh_cards = [c for c in cards if c.get('playerClass') == 'DEMONHUNTER' and c.get('set') == 'WHIZBANG' and c.get('collectible')]

for c in sorted(dh_cards, key=lambda x: x.get('cost', 0)):
    print(f"\n{'='*80}")
    print(f"ID: {c['id']}")
    print(f"名称: {c.get('name', 'N/A')}")
    print(f"费用: {c.get('cost', 'N/A')}")
    print(f"类型: {c.get('type', 'N/A')}")
    if c.get('type') == 'MINION':
        print(f"身材: {c.get('attack', 'N/A')}/{c.get('health', 'N/A')}")
    if c.get('type') == 'WEAPON':
        print(f"武器: {c.get('attack', 'N/A')}/{c.get('durability', 'N/A')}")
    print(f"稀有度: {c.get('rarity', 'N/A')}")
    print(f"描述: {c.get('text', 'N/A')}")
    if c.get('mechanics'):
        print(f"机制: {c.get('mechanics')}")
    if c.get('referencedTags'):
        print(f"引用标签: {c.get('referencedTags')}")
