"""
Dark Gift (黑暗之赐) 机制辅助函数 - 深入翡翠梦境（2025年3月）

Dark Gift 机制说明：
- 在发现（Discover）效果中为随从添加额外奖励效果
- 发现时展示3个随从选项，每个都带有随机奖励效果
- 适用职业：Death Knight, Demon Hunter, Rogue, Warlock, Warrior
- 共有10种不同的Dark Gift奖励效果

官方验证来源：
- Blizzard官网
- Hearthstone Wiki (wiki.gg)
- 补丁 32.2.0.219846 更新说明
"""

import random
from ....enums import GameTag
from ...enums import DARK_GIFT, DARK_GIFT_BONUS


# Dark Gift 可能的奖励效果列表（共10种）
# 官方验证: ✅ 所有10种奖励效果已完整实现
DARK_GIFT_BONUSES = [
    {
        "id": "DARK_GIFT_1",
        "name": "+2/+2 和扰魔",
        "atk": 2,
        "health": 2,
        "tags": {GameTag.ELUSIVE: True},
        "conditions": lambda minion: not minion.tags.get(GameTag.ELUSIVE, False),
    },
    {
        "id": "DARK_GIFT_2",
        "name": "+3 攻击和吸血",
        "atk": 3,
        "health": 0,
        "tags": {GameTag.LIFESTEAL: True},
        "conditions": lambda minion: not minion.tags.get(GameTag.LIFESTEAL, False),
    },
    {
        "id": "DARK_GIFT_3",
        "name": "+4 生命和嘲讽",
        "atk": 0,
        "health": 4,
        "tags": {GameTag.TAUNT: True},
        "conditions": lambda minion: not minion.tags.get(GameTag.TAUNT, False),
    },
    {
        "id": "DARK_GIFT_4",
        "name": "冲锋",
        "atk": 0,
        "health": 0,
        "tags": {GameTag.CHARGE: True},
        "conditions": lambda minion: (
            not minion.tags.get(GameTag.CHARGE, False) and 
            minion.atk > 0  # 0攻击的随从不能获得冲锋
        ),
    },
    {
        "id": "DARK_GIFT_5",
        "name": "战吼触发两次",
        "atk": 0,
        "health": 0,
        "tags": {GameTag.EXTRA_BATTLECRIES: 1},
        "conditions": lambda minion: minion.tags.get(GameTag.BATTLECRY, False),  # 只给有战吼的随从
    },
    {
        "id": "DARK_GIFT_6",
        "name": "打出时召唤一个2/2复制",
        "atk": 0,
        "health": 0,
        "tags": {GameTag.DARK_GIFT_SUMMON_COPY: True},  # 自定义标签
        "conditions": lambda minion: True,
    },
    {
        "id": "DARK_GIFT_7",
        "name": "复生",
        "atk": 0,
        "health": 0,
        "tags": {GameTag.REBORN: True},
        "conditions": lambda minion: not minion.tags.get(GameTag.REBORN, False),
    },
    {
        "id": "DARK_GIFT_8",
        "name": "圣盾和风怒",
        "atk": 0,
        "health": 0,
        "tags": {
            GameTag.DIVINE_SHIELD: True,
            GameTag.WINDFURY: True,
        },
        "conditions": lambda minion: (
            not minion.tags.get(GameTag.DIVINE_SHIELD, False) and
            not minion.tags.get(GameTag.WINDFURY, False)
        ),
    },
    {
        "id": "DARK_GIFT_9",
        "name": "费用减少(2)点,但-2攻击",
        "atk": -2,
        "health": 0,
        "cost_mod": -2,
        "tags": {},
        "conditions": lambda minion: minion.atk >= 3,  # 只给攻击力>=3的随从,确保不会降到0以下
    },
    {
        "id": "DARK_GIFT_10",
        "name": "+4/+5,置于牌库顶",
        "atk": 4,
        "health": 5,
        "tags": {GameTag.DARK_GIFT_TO_DECK_TOP: True},  # 自定义标签,表示需要置于牌库顶
        "conditions": lambda minion: True,
    },
]


def get_available_dark_gifts(minion):
    """
    获取对指定随从可用的Dark Gift列表
    
    根据补丁 32.2.0.219846 的规则:
    - 带有关键词的Dark Gift不会应用到已有该关键词的随从上
    - 0攻击的随从不能获得冲锋
    - 战吼触发两次只给有战吼的随从
    - 费用减少但-2攻击只给攻击力>=3的随从
    
    Args:
        minion: 随从卡牌对象
    
    Returns:
        list: 可用的Dark Gift列表
    """
    available = []
    for bonus in DARK_GIFT_BONUSES:
        # 检查条件函数
        if "conditions" in bonus and callable(bonus["conditions"]):
            if bonus["conditions"](minion):
                available.append(bonus)
        else:
            available.append(bonus)
    
    return available if available else DARK_GIFT_BONUSES  # 如果没有可用的,返回全部


def get_dark_gift_bonus_by_id(bonus_id):
    """根据ID获取Dark Gift奖励对象"""
    return next((b for b in DARK_GIFT_BONUSES if b["id"] == bonus_id), None)


def apply_dark_gift_to_object(minion, bonus):
    """
    直接应用Dark Gift属性到对象（底层实现）
    
    Args:
        minion: 目标对象
        bonus: 奖励字典
    """
    # 应用属性加成
    if bonus.get("atk", 0) != 0:
        minion.atk += bonus["atk"]
    if bonus.get("health", 0) > 0:
        minion.health += bonus["health"]
        minion.max_health += bonus["health"]
    
    # 应用费用修正
    if "cost_mod" in bonus and bonus["cost_mod"] != 0:
        minion.cost += bonus["cost_mod"]

    # 应用标签效果
    for tag, value in bonus["tags"].items():
        minion.tags[tag] = value

    # 标记为具有 Dark Gift
    minion.tags[DARK_GIFT] = True
    minion.tags[DARK_GIFT_BONUS] = bonus["id"]


def apply_dark_gift(minion, specific_gift=None):
    """
    为随从应用随机的 Dark Gift 奖励效果
    
    Args:
        minion: 随从卡牌对象
        specific_gift: 可选,指定特定的Dark Gift ID
    
    Returns:
        Buff Action: 用于应用效果的 Action
    """
    from .tokens import DARK_GIFT_BUFF
    from ...actions import Buff
    
    if specific_gift:
        # 应用指定的Dark Gift
        bonus = get_dark_gift_bonus_by_id(specific_gift)
        if not bonus:
            raise ValueError(f"Unknown Dark Gift ID: {specific_gift}")
    else:
        # 获取可用的Dark Gift并随机选择
        available_gifts = get_available_dark_gifts(minion)
        bonus = random.choice(available_gifts)
    
    # 返回 Buff Action
    # 这会触发 Buff 应用事件，从而被 EDR_487 等卡牌监听到
    return Buff(minion, "DARK_GIFT_BUFF", bonus_id=bonus["id"])


def get_dark_gift_bonus_name(bonus_id):
    """
    根据奖励效果ID获取名称
    
    Args:
        bonus_id: 奖励效果ID
    
    Returns:
        str: 奖励效果名称
    """
    for bonus in DARK_GIFT_BONUSES:
        if bonus["id"] == bonus_id:
            return bonus["name"]
    return "未知奖励"


def has_dark_gift(card):
    """
    检查卡牌是否具有Dark Gift
    
    Args:
        card: 卡牌对象
    
    Returns:
        bool: 是否具有Dark Gift
    """
    return card.tags.get(DARK_GIFT, False)
