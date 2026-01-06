import json

with open('cards.json', encoding='utf-8') as f:
    cards = json.load(f)

dk_cards = [c for c in cards if c.get('cardClass') == 'DEATHKNIGHT' and c.get('collectible')]

print(f'=== Death Knight 卡牌数据 ({len(dk_cards)}张) ===\n')

# 按稀有度分组
rarity_order = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY']
for rarity in rarity_order:
    rarity_cards = [c for c in dk_cards if c.get('rarity') == rarity]
    if not rarity_cards:
        continue
    
    print(f'\n### {rarity} ({len(rarity_cards)}张) ###\n')
    
    for c in sorted(rarity_cards, key=lambda x: x['id']):
        card_id = c['id']
        name = c['name']
        cost = c.get('cost', 'N/A')
        card_type = c.get('type', 'UNKNOWN')
        
        # 基本信息
        if card_type == 'MINION':
            atk = c.get('attack', '?')
            hp = c.get('health', '?')
            info = f"{cost}费 {atk}/{hp}"
        elif card_type == 'SPELL':
            info = f"{cost}费法术"
        elif card_type == 'WEAPON':
            atk = c.get('attack', '?')
            dur = c.get('durability', '?')
            info = f"{cost}费武器 {atk}/{dur}"
        else:
            info = f"{cost}费 {card_type}"
        
        print(f'{card_id}: {name}')
        print(f'  类型: {info}')
        
        # 机制
        mechanics = c.get('mechanics', [])
        if mechanics:
            print(f'  机制: {", ".join(mechanics)}')
        
        # 符文消耗
        rune_cost = c.get('runeCost')
        if rune_cost:
            runes = []
            if rune_cost.get('blood', 0) > 0:
                runes.append(f"鲜血x{rune_cost['blood']}")
            if rune_cost.get('frost', 0) > 0:
                runes.append(f"冰霜x{rune_cost['frost']}")
            if rune_cost.get('unholy', 0) > 0:
                runes.append(f"邪恶x{rune_cost['unholy']}")
            if runes:
                print(f'  符文: {", ".join(runes)}')
        
        # 效果文本
        text = c.get('text', '')
        if text:
            # 移除HTML标签以便阅读
            import re
            clean_text = re.sub(r'<[^>]+>', '', text)
            print(f'  效果: {clean_text}')
        
        print()

print('\n=== 总结 ===')
print(f'总计: {len(dk_cards)} 张可收集卡牌')
for rarity in rarity_order:
    count = len([c for c in dk_cards if c.get('rarity') == rarity])
    if count > 0:
        print(f'{rarity}: {count}张')
