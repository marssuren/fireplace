"""
Map Cards (地图卡牌) 机制辅助函数 - 失落之城（2025年7月）

Map Cards 机制说明：
- 打出地图后发现一张卡牌
- 如果在同一回合打出发现的卡牌，可以再次发现
- 共有6张地图卡牌

官方验证来源：
- Blizzard官网
- Hearthstone Wiki (wiki.gg)
- 补丁 35.0.0 更新说明
"""

from ...enums import MAP_DISCOVERED_THIS_TURN


def mark_map_discovered_card(player, card_id):
    """
    标记本回合从地图发现的卡牌

    Args:
        player: 玩家对象
        card_id: 发现的卡牌ID
    """
    if not hasattr(player, 'map_discovered_cards_this_turn'):
        player.map_discovered_cards_this_turn = []

    player.map_discovered_cards_this_turn.append(card_id)


def check_is_map_discovered_card(player, card_id):
    """
    检查卡牌是否为本回合从地图发现的

    Args:
        player: 玩家对象
        card_id: 要检查的卡牌ID

    Returns:
        bool: 是否为本回合从地图发现的卡牌
    """
    if not hasattr(player, 'map_discovered_cards_this_turn'):
        return False

    return card_id in player.map_discovered_cards_this_turn


def clear_map_discovered_cards(player):
    """
    清除本回合从地图发现的卡牌记录（回合结束时调用）

    Args:
        player: 玩家对象
    """
    if hasattr(player, 'map_discovered_cards_this_turn'):
        player.map_discovered_cards_this_turn = []
