"""
检查 cards.json 结构
"""
import json

# 读取完整的卡牌数据
with open('cards.json', 'r', encoding='utf-8') as f:
    all_cards = json.load(f)

print(f"Total cards: {len(all_cards)}")

# 查看第一张卡的结构
if all_cards:
    sample = all_cards[0]
    print(f"\nSample card keys: {list(sample.keys())}")
    print(f"\nSample card:")
    print(json.dumps(sample, ensure_ascii=False, indent=2)[:500])

# 查找 VAC_412
vac_412 = [c for c in all_cards if c.get('id') == 'VAC_412']
if vac_412:
    print(f"\nVAC_412 found:")
    print(json.dumps(vac_412[0], ensure_ascii=False, indent=2))
else:
    print("\nVAC_412 not found")

# 查找所有包含 HUNTER 的卡牌
hunter_cards = [c for c in all_cards if 'HUNTER' in str(c)]
print(f"\nCards with HUNTER in data: {len(hunter_cards)}")

# 查找 set = PARADISE 的卡牌
paradise_cards = [c for c in all_cards if c.get('set') == 'PARADISE']
print(f"Cards with set=PARADISE: {len(paradise_cards)}")
