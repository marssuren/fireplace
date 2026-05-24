"""
CardSet helpers aligned with fireplace_cs CardSetExtensions.

「最新扩展包」按官方 Set ID（枚举整型）判定，而非卡牌 ID 前缀。
"""

from hearthstone.enums import CardSet

# Cataclysm (大地的裂变) — mirrors fireplace_cs CardSet.CATACLYSM = 1980
_CATACLYSM_SET_ID = 1980

_STANDARD_MAIN_SET_IDS = (
    int(CardSet.TIMETRAVEL),
    int(CardSet.THE_LOST_CITY),
    int(CardSet.EMERALD_DREAM),
    _CATACLYSM_SET_ID,
)


def newest_expansion_set_id() -> int:
    """Max Set ID among current standard main expansions (excludes CORE / EVENT)."""
    return max(_STANDARD_MAIN_SET_IDS)


def is_newest_expansion(card_set) -> bool:
    if card_set is None:
        return False
    return int(card_set) == newest_expansion_set_id()
