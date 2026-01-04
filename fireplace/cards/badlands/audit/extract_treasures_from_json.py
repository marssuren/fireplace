
import json
import sys

def main():
    json_path = "d:/Projects/Yolo/hearthstone_zero/fireplace/fireplace/cards/233025/zhCN/cards.game_playable.json"
    
    print(f"Reading {json_path}...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Total cards in file: {len(data)}")
    
    wild_west_cards = [c for c in data if c.get('set') == 'WILD_WEST']
    print(f"Total WILD_WEST cards: {len(wild_west_cards)}")
    
    uncollectible_ww = [c for c in wild_west_cards if not c.get('collectible', False)]
    print(f"Uncollectible WILD_WEST cards: {len(uncollectible_ww)}")
    
    # Filter for potential treasures (Cost 1-4, likely Spells or Minions)
    potential_treasures = []
    for c in uncollectible_ww:
        cost = c.get('cost', -1)
        if cost in [1, 2, 3, 4]:
            potential_treasures.append(c)
            
    # Sort by cost then name
    potential_treasures.sort(key=lambda x: (x.get('cost', 0), x.get('name', '')))
    
    print("\n--- Potential Treasures ---")
    current_cost = -1
    for c in potential_treasures:
        cost = c.get('cost', 0)
        if cost != current_cost:
            print(f"\n[Cost {cost}]")
            current_cost = cost
            
        print(f"ID: {c.get('id'):<10} | Name: {c.get('name'):<15} | Type: {c.get('type'):<8} | Class: {c.get('cardClass'):<10} | Desc: {c.get('text', '')[:50]}...")

if __name__ == "__main__":
    main()
