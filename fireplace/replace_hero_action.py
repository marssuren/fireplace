from collections import OrderedDict

from hearthstone.enums import (
    BlockType,
    CardClass,
    CardType,
    GameTag,
    Mulligan,
    PlayState,
    Race,
    Step,
    Zone,
)

from .dsl import LazyNum, LazyValue, Selector
from .dsl.copy import Copy, RebornCopy
from .dsl.random_picker import RandomMinion
from .dsl.selector import SELF
from .entity import Entity
from .enums import DISCARDED
from .exceptions import InvalidAction
from .logging import log, log_info
from .i18n import _ as translate
from .utils import random_class


class ReplaceHero(TargetedAction):
    """
    Replace a player's hero with a new hero card.
    Preserves health, armor, and other important stats.
    """
    
    TARGET = ActionArg()
    CARD = CardArg()
    
    def do(self, source, target, cards):
        """
        Replace target player's hero with the specified hero card
        
        Args:
            source: The source of this action
            target: The player whose hero to replace
            cards: The new hero card(s) to use
        """
        log_info("replace_hero", target=target, cards=cards)
        
        if not isinstance(cards, list):
            cards = [cards]
        
        for card in cards:
            if card.type != CardType.HERO:
                log_info(f"Cannot replace hero with non-hero card: {card}")
                continue
            
            old_hero = target.hero
            
            # Create the new hero
            if isinstance(card, str):
                new_hero = target.card(card, source=source)
            else:
                new_hero = card
            
            # Preserve important stats from old hero
            new_hero.controller = target
            new_hero.zone = Zone.PLAY
            
            # Preserve health and armor
            current_health = old_hero.health
            current_armor = old_hero.armor
            max_health = new_hero.max_health
            
            # Set health (don't exceed new max health)
            new_hero.health = min(current_health, max_health)
            new_hero.armor = current_armor
            
            # Preserve attack if hero had a weapon
            if old_hero.atk > 0 and not target.weapon:
                new_hero.atk = old_hero.atk
            
            # Preserve damage taken
            damage_taken = old_hero.max_health - current_health
            if damage_taken > 0:
                new_hero.damage = min(damage_taken, new_hero.max_health)
            
            # Replace the hero
            old_hero.zone = Zone.GRAVEYARD
            target.hero = new_hero
            
            # Handle hero power
            if hasattr(new_hero, 'power') and new_hero.power:
                # Create the new hero power
                if isinstance(new_hero.power, str):
                    power_card = target.card(new_hero.power, source=new_hero)
                else:
                    power_card = new_hero.power
                
                # Remove old hero power
                if old_hero.power:
                    old_hero.power.zone = Zone.GRAVEYARD
                
                # Set new hero power
                power_card.controller = target
                power_card.zone = Zone.PLAY
                new_hero.power = power_card
            
            log_info(f"Hero replaced: {old_hero} -> {new_hero}")
            
            # Broadcast the hero replacement event
            source.game.manager.targeted_action(self, source, target, new_hero)
            self.broadcast(source, EventListener.AFTER, target, new_hero)
        
        return cards
