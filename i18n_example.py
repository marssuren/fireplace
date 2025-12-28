"""
Example demonstrating how to use i18n (internationalization) in Fireplace.

This example shows:
1. How to set the language
2. How to use translated log messages
3. How to switch between English and Chinese
"""

# Import the i18n module
from fireplace.i18n import set_language, get_language
from fireplace.logging import log_info

def demo_english_logs():
    """Demonstrate logging in English."""
    print("\n=== English Logs ===")
    set_language("en")
    print(f"Current language: {get_language()}")

    # Example log messages
    log_info("game_start")
    log_info("attacks", attacker="Minion A", defender="Minion B")
    log_info("draws", target="Player 1", card="Fireball")
    log_info("heals", source="Priest", target="Hero", amount=5)
    log_info("fatigue_damage", target="Player 2", amount=3)

def demo_chinese_logs():
    """Demonstrate logging in Chinese."""
    print("\n=== 中文日志 ===")
    set_language("zh_CN")
    print(f"当前语言: {get_language()}")

    # Example log messages (same calls, different output)
    log_info("game_start")
    log_info("attacks", attacker="随从 A", defender="随从 B")
    log_info("draws", target="玩家 1", card="火球术")
    log_info("heals", source="牧师", target="英雄", amount=5)
    log_info("fatigue_damage", target="玩家 2", amount=3)

if __name__ == "__main__":
    print("Fireplace i18n Demo")
    print("=" * 50)

    # Demo English
    demo_english_logs()

    # Demo Chinese
    demo_chinese_logs()

    print("\n" + "=" * 50)
    print("Demo completed!")
