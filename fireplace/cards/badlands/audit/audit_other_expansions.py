
import os
import json

EXPANSIONS = [
    ("blackrock", "BRM"),
    ("boomsday", "BOOMSDAY"),
    ("classic", "CORE"), # or CLASSIC based on exact DB definition
    ("dalaran", "DALARAN"),
    ("dragons", "DRAGONS"),
    ("gangs", "GANGS"),
    ("gvg", "GVG"),
    ("icecrown", "ICECROWN"),
    ("initiate", "DEMON_HUNTER_INITIATE"),
    ("karazhan", "KARA"),
    ("kobolds", "LOOTAPALOOZA"),
    ("league", "LOE"),
    ("naxxramas", "NAXX"),
    ("outlands", "BLACK_TEMPLE"),
    ("path_of_arthas", "PATH_OF_ARTHAS"),
    ("return_to_naxxramas", "RETURN_OF_THE_LICH_KING"),
    ("scholomance", "SCHOLOMANCE"), 
    ("stormwind", "STORMWIND"),
    ("tgt", "TGT"),
    ("troll", "TROLL"),
    ("uldum", "ULDUM"),
    ("ungoro", "UNGORO"),
    ("witchwood", "GILNEAS"),
    ("wog", "OG"),
]

SOURCE_DATA_PATH = r"d:\Projects\Yolo\hearthstone_zero\fireplace\fireplace\cards\233025\zhCN\cards.game_playable.json"
CARDS_DIR = r"d:\Projects\Yolo\hearthstone_zero\fireplace\fireplace\cards"

def main():
    print("Loading source data...")
    with open(SOURCE_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    available_sets = set(c.get('set') for c in data)
    print(f"Available sets in JSON: {sorted(list(available_sets))}")
    
    # Mapping refinement based on usual HS Enum names
    folder_to_set = {
        "blackrock": "BRM",
        "boomsday": "BOOMSDAY",
        "classic": "CORE", 
        "dalaran": "DALARAN",
        "dragons": "DRAGONS",
        "gangs": "GANGS",
        "gvg": "GVG",
        "icecrown": "ICECROWN",
        "initiate": "DEMON_HUNTER_INITIATE",
        "karazhan": "KARA",
        "kobolds": "LOOTAPALOOZA",
        "league": "LOE",
        "naxxramas": "NAXX",
        "outlands": "BLACK_TEMPLE",
        "path_of_arthas": "PATH_OF_ARTHAS",
        "return_to_naxxramas": "RETURN_OF_THE_LICH_KING", 
        "scholomance": "SCHOLOMANCE",
        "stormwind": "STORMWIND",
        "tgt": "TGT",
        "troll": "TROLL",
        "uldum": "ULDUM",
        "ungoro": "UNGORO",
        "witchwood": "GILNEAS",
        "wog": "OG",
    }

    for folder, set_id in folder_to_set.items():
        # Special logic adjustments
        if set_id == "CORE":
             # Try to satisfy "classic" using LEGACY or VANILLA if CORE not ideal, but CORE is modern.
             # User mentioned "Classic".
             pass 

        if set_id not in available_sets:
             # Try to find close matches or skip
             # For Return to Naxx, it's a mini-set. Usually shares tag or has specific tag.
             # In modern HS data, Mini-sets share the parent expansion tag but have 'subset' field maybe?
             # Or they have their own tag. 
             # Let's simple check.
             if set_id == "RETURN_OF_THE_LICH_KING" and "RETURN_OF_THE_LICH_KING" in available_sets:
                 pass 
             else:
                 print(f"Warning: Set ID {set_id} for {folder} not found in data. Skipping.")
                 continue

        print(f"Processing {folder} (Set: {set_id})...")
        
        target_dir = os.path.join(CARDS_DIR, folder, "audit")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Collectible Only as per standard resumption practice (unless told otherwise)
        set_cards = [c for c in data if c.get('set') == set_id and c.get('collectible') == True]
        
        with open(os.path.join(target_dir, "cards.json"), 'w', encoding='utf-8') as f:
            json.dump(set_cards, f, indent=4, ensure_ascii=False)
            
        print(f"  Saved {len(set_cards)} cards to {target_dir}")

if __name__ == "__main__":
    main()
