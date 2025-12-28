"""
Script to update actions.py to use i18n translation functions.
This script replaces log.info() calls with log_info() calls using translation keys.
"""
import re

# Mapping of log patterns to translation keys
LOG_REPLACEMENTS = [
    (r'log\.info\("%r triggers off %r from %r", entity, self, source\)',
     'log_info("trigger_off", entity=entity, trigger=self, source=source)'),

    (r'log\.info\("%r attacks %r", attacker, defender\)',
     'log_info("attacks", attacker=attacker, defender=defender)'),

    (r'log\.info\("Attack has been interrupted\."\)',
     'log_info("attack_interrupted")'),

    (r'log\.info\("Processing Deathrattle for %r", card\)',
     'log_info("processing_deathrattle", card=card)'),

    (r'log\.info\("Jousting %r vs %r", challenger, defender\)',
     'log_info("jousting", challenger=challenger, defender=defender)'),

    (r'log\.info\("%s plays %r \(target=%r, index=%r\)", player, card, target, index\)',
     'log_info("plays_card", player=player, card=card, target=target, index=index)'),

    (r'log\.info\("%r requires a target for its battlecry\. Will not trigger\."\)',
     'log_info("requires_target_battlecry", card=card)'),

    (r'log\.info\("%r cannot overload %s", source, player\)',
     'log_info("cannot_overload", source=source, player=player)'),

    (r'log\.info\("%r overloads %s for %i", source, player, amount\)',
     'log_info("overloads", source=source, player=player, amount=amount)'),

    (r'log\.info\("%r triggering %r targeting %r", source, self, targets\)',
     'log_info("triggering_targeting", source=source, trigger=self, targets=targets)'),
]

def update_file():
    """Read actions.py, apply replacements, and write back."""
    file_path = r"D:\Projects\Yolo\fireplace\fireplace\actions.py"

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'from .logging import log, log_info' in content:
        print("File already updated with i18n support.")
        return

    # Update import statement
    content = content.replace(
        'from .logging import log',
        'from .logging import log, log_info'
    )

    # Apply replacements
    for pattern, replacement in LOG_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {len(LOG_REPLACEMENTS)} log statements in actions.py")

if __name__ == '__main__':
    update_file()
