import os
import re
import json
import sys

# Configuration
TARGET_SET = "RETURN_OF_THE_LICH_KING"
# Assume script is in [TargetDir]/audit/verify_script.py, so we look at [TargetDir]
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/.."
CARDS_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards.json")

def load_cards_db():
    if not os.path.exists(CARDS_JSON_PATH):
        print(f"Error: cards.json not found at {CARDS_JSON_PATH}")
        sys.exit(1)
    with open(CARDS_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_implemented_cards():
    implemented_cards = set()
    for root, dirs, files in os.walk(BASE_DIR):
        if 'audit' in root:
            continue
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(r'class\s+([A-Z0-9_]+)', content)
                    implemented_cards.update(matches)
    return implemented_cards

def main():
    print(f"Scanning {BASE_DIR} for implemented cards...")
    implemented = get_implemented_cards()
    
    print(f"Loading {TARGET_SET} card data...")
    db = load_cards_db()
    
    # Filter for Collectible cards of the target set
    # Note: Using 'collectible' flag usually, but checking set ID mostly
    target_cards = [c for c in db if c.get('set') == TARGET_SET and c.get('collectible', False)]
    
    total_count = len(target_cards)
    implemented_count = 0
    missing = []
    
    for card in target_cards:
        card_id = card['id']
        if card_id in implemented:
            implemented_count += 1
        else:
            missing.append(f"{card_id} ({card.get('name', 'Unknown')})")
            
    print("-" * 50)
    print(f"Expansion: {TARGET_SET}")
    print(f"Progress: {implemented_count}/{total_count} ({(implemented_count/total_count*100) if total_count else 0:.1f}%)")
    print("-" * 50)
    
    if missing:
        print(f"Missing Cards ({len(missing)}):")
        # Print first 10 missing
        for m in missing[:10]:
            print(f" - {m}")
        if len(missing) > 10:
            print(f" ... and {len(missing) - 10} more.")

if __name__ == "__main__":
    main()
