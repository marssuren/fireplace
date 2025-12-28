"""
Internationalization (i18n) support for Fireplace.
Provides translation functionality for game logs and messages.
"""
import os
import json
from typing import Dict, Any

# Default language
_current_language = "en"

# Translation dictionaries
_translations: Dict[str, Dict[str, str]] = {}

# Path to translation files
_LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locales")


def load_translations():
    """Load all available translation files."""
    global _translations

    if not os.path.exists(_LOCALE_DIR):
        return

    for filename in os.listdir(_LOCALE_DIR):
        if filename.endswith(".json"):
            lang_code = filename[:-5]  # Remove .json extension
            filepath = os.path.join(_LOCALE_DIR, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    _translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load translation file {filename}: {e}")


def set_language(lang: str):
    """
    Set the current language for translations.

    Args:
        lang: Language code (e.g., 'en', 'zh_CN')
    """
    global _current_language
    _current_language = lang

    # Load translations if not already loaded
    if not _translations:
        load_translations()


def get_language() -> str:
    """Get the current language code."""
    return _current_language


def _(key: str, **kwargs) -> str:
    """
    Translate a message key to the current language.

    Args:
        key: The message key to translate
        **kwargs: Format arguments for the translated string

    Returns:
        Translated and formatted string
    """
    # Load translations if not already loaded
    if not _translations:
        load_translations()

    # Get translation for current language, fallback to English, then to key itself
    translation = _translations.get(_current_language, {}).get(key)

    if translation is None and _current_language != "en":
        translation = _translations.get("en", {}).get(key)

    if translation is None:
        translation = key

    # Format the string with provided arguments
    try:
        return translation.format(**kwargs)
    except (KeyError, ValueError):
        return translation


# Initialize translations on module import
load_translations()
