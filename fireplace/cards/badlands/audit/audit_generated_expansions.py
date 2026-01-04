
import os
import json

# Mapping 'generated' folders to their Set IDs
# Based on folder names and available JSON Set IDs
GENERATED_MAP = [
    ("alterac_generated", "ALTERAC_VALLEY"),
    ("barrens_generated", "THE_BARRENS"),
    ("darkmoon_generated", "DARKMOON_FAIRE"),
    ("emerald_dream_generated", "EMERALD_DREAM"), # Likely Badlands Mini-set or related
    ("paradise_generated", "ISLAND_VACATION"),    # Perils in Paradise
    ("scholomance_generated", "SCHOLOMANCE"),     # Note: 'scholomance' folder also exists
    ("space_generated", "SPACE"),                 # The Great Dark Beyond
    ("time_travel_generated", "TIME_TRAVEL"),     # Caverns of Time
    ("whizbang_generated", "WHIZBANGS_WORKSHOP"), # Whizbang's Workshop
    ("nathria_generated", "REVENDRETH"),          # Castle Nathria (checking if missed earlier)
]

SOURCE_DATA_PATH = r"d:\Projects\Yolo\hearthstone_zero\fireplace\fireplace\cards\233025\zhCN\cards.game_playable.json"
CARDS_DIR = r"d:\Projects\Yolo\hearthstone_zero\fireplace\fireplace\cards"

def main():
    print("Loading source data...")
    with open(SOURCE_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    available_sets = set(c.get('set') for c in data)
    print(f"Verified available sets provided by data source.")

    for folder, set_id in GENERATED_MAP:
        if set_id not in available_sets:
            print(f"Warning: Set ID {set_id} for {folder} not found in data. Skipping.")
            continue

        print(f"Processing {folder} (Set: {set_id})...")
        
        target_dir = os.path.join(CARDS_DIR, folder, "audit")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Harvest all collectible cards for this set
        set_cards = [c for c in data if c.get('set') == set_id and c.get('collectible') == True]
        
        with open(os.path.join(target_dir, "cards.json"), 'w', encoding='utf-8') as f:
            json.dump(set_cards, f, indent=4, ensure_ascii=False)
            
        print(f"  Saved {len(set_cards)} cards to {target_dir}")

if __name__ == "__main__":
    main()
