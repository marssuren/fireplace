"""
Imbue 机制辅助函数 - 深入翡翠梦境（2025年3月）

Imbue 机制说明：
- 第一次打出带有 Imbue 的卡牌时，英雄技能会转换为新的职业专属英雄技能
- 后续每次打出 Imbue 卡牌，会升级英雄技能（增加数值）
- 适用职业：Druid, Hunter, Mage, Paladin, Priest, Shaman
"""

from hearthstone.enums import Zone
from ...enums import IMBUE, IMBUE_LEVEL, IMBUED_HERO_POWER


# 职业对应的 Imbued 英雄技能映射
IMBUED_HERO_POWERS = {
    "DRUID": "EDR_DRUID_HP",      # 待定：需要查询官方数据
    "HUNTER": "EDR_HUNTER_HP",    # Blessing of the Wolf (狼之祝福)
    "MAGE": "EDR_MAGE_HP",        # Blessing of the Wisp (小精灵祝福)
    "PALADIN": "EDR_PALADIN_HP",  # Blessing of the Dragon (龙之祝福)
    "PRIEST": "EDR_PRIEST_HP",    # Blessing of the Moon (月之祝福)
    "SHAMAN": "EDR_SHAMAN_HP",    # Blessing of the Wind (风之祝福) - 已确认
}




def trigger_imbue(controller):
    """
    触发 Imbue 效果：转换或升级英雄技能

    Args:
        controller: 玩家对象

    Returns:
        None（直接修改 controller 的状态）
    """
    # 获取玩家职业
    player_class = controller.hero.card_class.name

    # 检查职业是否支持 Imbue
    if player_class not in IMBUED_HERO_POWERS:
        return

    # 第一次触发 Imbue：转换英雄技能
    if controller.imbue_level == 0:
        # 保存原始英雄技能
        if not controller.original_hero_power:
            controller.original_hero_power = controller.hero.power

        # 获取新的 Imbued 英雄技能ID
        new_power_id = IMBUED_HERO_POWERS[player_class]

        # 创建新的英雄技能
        new_power = controller.card(new_power_id, source=controller.hero)
        new_power.controller = controller
        new_power.zone = Zone.PLAY

        # 替换英雄技能
        if controller.hero.power:
            controller.hero.power.zone = Zone.GRAVEYARD
        controller.hero.power = new_power

        # 标记为 Imbued
        new_power.tags[IMBUED_HERO_POWER] = True

        # 设置 Imbue 等级为 1
        controller.imbue_level = 1
        controller.imbued_hero_power_id = new_power_id

    # 后续触发 Imbue：升级英雄技能
    else:
        controller.imbue_level += 1

        # 升级逻辑：增加英雄技能的数值
        # 具体升级效果由各个英雄技能的实现决定
        # 这里只更新等级，实际效果在英雄技能的 use() 方法中根据等级动态计算


def get_imbue_level(controller):
    """
    获取当前 Imbue 等级

    Args:
        controller: 玩家对象

    Returns:
        int: 当前 Imbue 等级
    """
    return getattr(controller, 'imbue_level', 0)
