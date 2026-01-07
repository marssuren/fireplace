"""
Kindred (同族) 机制辅助函数 - 失落之城（2025年7月）

Kindred 机制说明：
- 如果你在上一回合打出过相同随从类型或法术学派的卡牌，则触发额外效果
- 类似于元素的机制，但扩展到所有随从类型和法术学派
- 某些 Kindred 卡牌可能有双类型要求（任一类型/学派都可触发）
- 如果 Kindred 效果修改费用，在手牌中就会生效
- TLC_251 蛮鱼挑战者可以使下一个延系效果触发两次

官方验证来源：
- Blizzard官网
- Hearthstone Wiki (wiki.gg)
- 补丁 35.0.0 更新说明
"""

from hearthstone.enums import CardType, Race, SpellSchool
from ...enums import KINDRED, KINDRED_ACTIVE


def check_kindred_active(player, card_type=None, race=None, spell_school=None):
    """
    检查 Kindred 效果是否激活，并返回触发次数
    
    Args:
        player: 玩家对象
        card_type: 卡牌类型（CardType.MINION 或 CardType.SPELL）
        race: 随从种族（Race 枚举），如果为 None 则检查是否打出过任意该类型的卡牌
        spell_school: 法术学派（SpellSchool 枚举）
    
    Returns:
        int: 触发次数
            - 0: 未激活（上回合未打出相应类型的卡牌）
            - 1: 正常触发（上回合打出过相应类型的卡牌）
            - 2: 双倍触发（上回合打出过相应类型的卡牌 + TLC_251 蛮鱼挑战者效果）
    
    注意：
        - 返回值可以直接用作布尔值（0=False, 1/2=True）
        - 向后兼容：现有代码 `if check_kindred_active(...)` 仍然有效
        - 新代码可以使用 `for _ in range(check_kindred_active(...))` 实现多次触发
    """
    # 检查上一回合打出的卡牌ID列表
    if not hasattr(player, 'cards_played_last_turn'):
        return 0

    # 导入卡牌数据库
    from .. import db
    
    # 首先检查是否满足 Kindred 条件
    is_active = False

    for card_id in player.cards_played_last_turn:
        # 从卡牌ID获取卡牌数据
        try:
            card_data = db[card_id]
        except KeyError:
            continue

        # 检查随从种族
        if card_type == CardType.MINION:
            # 如果指定了种族，检查是否匹配
            if race is not None:
                if hasattr(card_data, 'race'):
                    # 支持单种族和多种族
                    card_races = getattr(card_data, 'races', [card_data.race])
                    if race in card_races:
                        is_active = True
                        break
            else:
                # 如果没有指定种族，只要是随从就返回 True
                if card_data.type == CardType.MINION:
                    is_active = True
                    break

        # 检查法术学派
        if card_type == CardType.SPELL:
            # 如果指定了学派，检查是否匹配
            if spell_school is not None:
                if hasattr(card_data, 'spell_school'):
                    if card_data.spell_school == spell_school:
                        is_active = True
                        break
            else:
                # 如果没有指定学派，只要是法术就返回 True
                if card_data.type == CardType.SPELL:
                    is_active = True
                    break
    
    # 如果 Kindred 未激活，直接返回 0
    if not is_active:
        return 0
    
    # Kindred 已激活，检查是否需要双倍触发
    # TLC_251 蛮鱼挑战者：你的下一个延系效果会触发两次
    if hasattr(player, 'kindred_double_trigger') and player.kindred_double_trigger:
        player.kindred_double_trigger = False  # 重置标记（只影响下一个延系效果）
        return 2  # 双倍触发
    
    return 1  # 正常触发

