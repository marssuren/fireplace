
import os

actions_path = "d:/Projects/Yolo/hearthstone_zero/fireplace/fireplace/actions.py"

excavate_code = """

class Excavate(GameAction):
    \"\"\"
    Excavate a treasure.
    \"\"\"
    def do(self, source, controller):
        from fireplace.cards.badlands.excavate import TIER_1_IDS, TIER_2_IDS, TIER_3_IDS, TIER_4_IDS
        
        # Increment total excavates
        controller.times_excavated += 1
        
        current_stage = controller.excavate_tier
        
        reward_tier_int = 0
        next_stage = 0
        
        if current_stage == 0:
            reward_tier_int = 1
            next_stage = 1
        elif current_stage == 1:
            reward_tier_int = 2
            next_stage = 2
        elif current_stage == 2:
            reward_tier_int = 3
            next_stage = 3
        elif current_stage == 3:
            # Check for Tier 4 eligibility
            has_tier_4 = controller.hero.card_class in TIER_4_IDS
            if has_tier_4:
                reward_tier_int = 4
                next_stage = 0
            else:
                reward_tier_int = 1
                next_stage = 1
        
        controller.excavate_tier = next_stage
        
        # Select Card
        card_id = None
        if reward_tier_int == 1:
            card_id = source.game.random.choice(TIER_1_IDS)
        elif reward_tier_int == 2:
            card_id = source.game.random.choice(TIER_2_IDS)
        elif reward_tier_int == 3:
            card_id = source.game.random.choice(TIER_3_IDS)
        elif reward_tier_int == 4:
            card_id = TIER_4_IDS.get(controller.hero.card_class)
            
        if card_id:
             source.game.add_card(controller, card_id, source=source)
"""

with open(actions_path, 'a', encoding='utf-8') as f:
    f.write(excavate_code)

print("Appended Excavate to actions.py")
