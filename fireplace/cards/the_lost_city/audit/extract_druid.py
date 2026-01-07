import json

with open('collectible_cards.json', encoding='utf-8') as f:
    data = json.load(f)

druid_cards = sorted(
    [c for c in data if c.get('cardClass') == 'DRUID'],
    key=lambda x: (
        {'COMMON': 1, 'RARE': 2, 'EPIC': 3, 'LEGENDARY': 4}.get(x.get('rarity', ''), 0),
        x.get('cost', 0)
    )
)

for c in druid_cards:
    print(f"\n{c['id']}: {c['name']}")
    print(f"  费用: {c.get('cost', 0)}")
    print(f"  稀有度: {c.get('rarity', '')}")
    print(f"  类型: {c.get('type', '')}")
    if c.get('type') == 'MINION':
        print(f"  属性: {c.get('attack', 0)}/{c.get('health', 0)}")
        if c.get('race'):
            print(f"  种族: {c.get('race', '')}")
        if c.get('races'):
            print(f"  种族列表: {c.get('races', [])}")
    if c.get('spellSchool'):
        print(f"  学派: {c.get('spellSchool', '')}")
    if c.get('mechanics'):
        print(f"  机制: {c.get('mechanics', [])}")
    print(f"  效果: {c.get('text', '')}")
