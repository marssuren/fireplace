
import json
import sys
import os

def main():
    json_path = "d:/Projects/Yolo/hearthstone_zero/fireplace/fireplace/cards/233025/zhCN/cards.game_playable.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Filter for WW_001t and DEEP_999t cards
    treasures = []
    ids_to_find = ["WW_001t", "DEEP_999t"]
    
    for card in data:
        cid = card.get('id', '')
        if any(cid.startswith(prefix) for prefix in ids_to_find):
            treasures.append(card)

    treasures.sort(key=lambda x: (x.get('cost', 0), x.get('id')))

    print("# Excavate Treasures Data")
    print("excavate_treasures = {")
    
    current_tier = 0
    
    tier_map = {
        1: "TIER_1",
        2: "TIER_2",
        3: "TIER_3",
        4: "TIER_4"
    }

    for t in treasures:
        cost = t.get('cost', 0)
        if cost not in tier_map:
            continue
            
        print(f"    # Cost {cost} ({t.get('id')}) - {t.get('name')}")
        print(f"    # Description: {t.get('text', '')}")
        print(f"    '{t.get('id')}': {cost},")

    print("}")

    # Also categorize by Tier lists
    print("\n# Tier Lists")
    for cost in [1, 2, 3, 4]:
        tier_cards = [t['id'] for t in treasures if t.get('cost') == cost]
        print(f"TIER_{cost}_TREASURES = [")
        for cid in tier_cards:
            print(f"    '{cid}',")
        print("]")

if __name__ == "__main__":
    main()
