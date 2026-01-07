"""
Fabled 机制辅助函数 - 穿越时间流（2025年11月）

Fabled 机制说明：
- Fabled 是传说卡牌"套餐"系统
- 将 Fabled 卡牌加入套牌时，会自动添加 2-3 张额外的独特卡牌
- 每个职业都有自己的 Fabled 传说卡牌
- 这些额外卡牌在组牌阶段就加入套牌
"""
from ...enums import FABLED, FABLED_CARDS


# Fabled 卡牌及其附带卡牌的映射表
FABLED_CARD_PACKAGES = {
    # Death Knight - Talanji of the Graves
    "TIME_619": ["TIME_619t", "TIME_619t5"],  # Bwonsamdi + What Befell Zandalar
    
    # Hunter - Ranger General Sylvanas
    "TIME_609": ["TIME_609t1", "TIME_609t2"],  # Alleria + Vereesa
    
    # Rogue - Garona Halforcen
    "TIME_875": ["TIME_875t", "TIME_875t2"],  # King Llane + The Kingslayers
    
    # Warrior - Lo'Gosh, Blood Fighter
    "TIME_850": ["TIME_850t"],  # Blood Fighter
    
    # Priest - Medivh the Hallowed
    "TIME_890": ["TIME_890t"],  # Karazhan
    
    # 示例：每个 Fabled 卡牌对应的附带卡牌列表
    # "TIME_XXX": ["TIME_XXXt1", "TIME_XXXt2", "TIME_XXXt3"],
}


def is_fabled_card(card_id):
    """
    检查卡牌是否为 Fabled 卡牌

    Args:
        card_id: 卡牌ID

    Returns:
        bool: 是否为 Fabled 卡牌
    """
    return card_id in FABLED_CARD_PACKAGES


def get_fabled_package_cards(card_id):
    """
    获取 Fabled 卡牌附带的额外卡牌列表

    Args:
        card_id: Fabled 卡牌ID

    Returns:
        list: 附带的卡牌ID列表，如果不是 Fabled 卡牌则返回空列表
    """
    return FABLED_CARD_PACKAGES.get(card_id, [])


def mark_card_fabled(card, package_cards):
    """
    标记卡牌为 Fabled 卡牌

    Args:
        card: 卡牌对象
        package_cards: 附带的卡牌ID列表
    """
    card.tags[FABLED] = True
    card.tags[FABLED_CARDS] = package_cards


def add_fabled_package_to_deck(deck_list):
    """
    在组牌时自动添加 Fabled 卡牌的附带卡牌

    Args:
        deck_list: 套牌列表（卡牌ID列表）

    Returns:
        list: 添加了 Fabled 附带卡牌后的套牌列表
    """
    expanded_deck = deck_list.copy()

    for card_id in deck_list:
        if is_fabled_card(card_id):
            package_cards = get_fabled_package_cards(card_id)
            expanded_deck.extend(package_cards)

    return expanded_deck
