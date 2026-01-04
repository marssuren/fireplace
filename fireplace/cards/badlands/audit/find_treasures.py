
import sys
import os

# Adjust path to import fireplace
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from fireplace.cards import db
from hearthstone.enums import CardSet, GameTag

def main():
    db.initialize()
    
    print("Searching for Badlands (WILD_WEST) uncollectible cards...")
    
    badlands_cards = [
        card for card in db.values() 
        if card.card_set == CardSet.WILD_WEST and not card.collectible
    ]
    
    print(f"Found {len(badlands_cards)} uncollectible cards.")
    
    # Filter for potential treasures (Tier 1-4)
    # Common treasures cost 1, Rare 2, Epic 3, Legendary 4
    
    tiers = {1: [], 2: [], 3: [], 4: []}
    
    for card in badlands_cards:
        if card.type == 4: # Minion
            print(f"[{card.id}] {card.name} (Cost: {card.cost}, Type: {card.type})")
        elif card.type == 5: # Spell
            print(f"[{card.id}] {card.name} (Cost: {card.cost}, Type: {card.type})")
        elif card.type == 7: # Weapon (if any) or Location
            print(f"[{card.id}] {card.name} (Cost: {card.cost}, Type: {card.type})")
            
        # Heuristic for treasures
        if card.cost in [1, 2, 3, 4]:
            tiers[card.cost].append(card)

    print("\n--- Potential Treasures by Cost ---")
    for cost, cards in tiers.items():
        print(f"\nCost {cost} (Tier {cost}?):")
        for c in cards:
            print(f"  {c.id}: {c.name} - {c.description}")

if __name__ == "__main__":
    main()
