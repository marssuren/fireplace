"""
Rewind 机制辅助函数 - 穿越时间流（2025年11月）

Rewind 机制说明：
- 玩家可以"重新来过"，撤销卡牌效果并重新打出
- 用于处理随机效果不满意的情况
- 每张卡牌可以有不同的 Rewind 次数（1次、2次、3次等）
"""
from ...enums import REWIND, REWIND_COUNT, REWIND_AVAILABLE
from ...actions import RewindChoice


def mark_card_rewind(card, rewind_count=1):
    """
    标记卡牌具有 Rewind 效果

    Args:
        card: 卡牌对象
        rewind_count: 可以 Rewind 的次数（默认1次）
    """
    card.tags[REWIND] = True
    card.tags[REWIND_COUNT] = rewind_count
    card.tags[REWIND_AVAILABLE] = True


def check_can_rewind(card):
    """
    检查卡牌是否可以 Rewind

    Args:
        card: 卡牌对象

    Returns:
        bool: 是否可以 Rewind
    """
    if not card.tags.get(REWIND, False):
        return False

    if not card.tags.get(REWIND_AVAILABLE, False):
        return False

    remaining_count = card.tags.get(REWIND_COUNT, 0)
    return remaining_count > 0


def consume_rewind(card):
    """
    消耗一次 Rewind 机会

    Args:
        card: 卡牌对象
    """
    if not check_can_rewind(card):
        return

    current_count = card.tags.get(REWIND_COUNT, 0)
    card.tags[REWIND_COUNT] = current_count - 1

    # 如果次数用完，标记为不可用
    if card.tags[REWIND_COUNT] <= 0:
        card.tags[REWIND_AVAILABLE] = False


def get_rewind_count(card):
    """
    获取卡牌剩余的 Rewind 次数

    Args:
        card: 卡牌对象

    Returns:
        int: 剩余 Rewind 次数
    """
    if not card.tags.get(REWIND, False):
        return 0

    return card.tags.get(REWIND_COUNT, 0)


def create_rewind_point(game):
    """
    创建一个 Rewind 时间点（快照）
    应在打出具有 Rewind 效果的卡牌前调用
    """
    game.save_rewind_snapshot()


def rewind_game(game):
    """
    执行回溯操作
    1. 恢复快照
    2. 修改随机种子（确保下次结果不同）
    """
    if not game.restore_rewind_snapshot():
        return False

    # 关键：恢复状态后，随机数生成器的状态也恢复了。
    # 为了让"重来"的结果不同，我们修改 Mersenne Twister 的内部状态。
    #
    # 原理：Mersenne Twister 是递归算法，修改 state[0] 会通过雪崩效应
    # 影响整个随机数序列，无论卡牌使用多少个随机数都会产生不同结果。
    old_state = game.random.getstate()
    version, state_tuple, index = old_state

    # 修改状态数组的第一个元素
    new_tuple = list(state_tuple)
    new_tuple[0] = (new_tuple[0] + 1) % (2**32)

    new_state = (version, tuple(new_tuple), index)
    game.random.setstate(new_state)

    return True


def execute_with_rewind(card, effect_generator):
    """
    执行带有 Rewind 功能的卡牌效果

    正确实现方案：
    - 第一步：创建游戏快照
    - 第二步：执行卡牌效果
    - 第三步：暂停游戏，让玩家/AI 选择是否回溯
      - 选项1：接受结果（继续游戏）
      - 选项2：重新来过（回溯并重新执行）

    这是正确的 Rewind 机制实现，给予玩家/AI 对随机结果的控制权。

    Args:
        card: 卡牌对象
        effect_generator: 卡牌效果的生成器函数（必须是可调用对象）

    Yields:
        卡牌效果的动作
    """
    # 1. 创建回溯点（保存游戏快照）
    create_rewind_point(card.game)

    # 2. 执行卡牌效果
    for action in effect_generator():
        yield action

    # 3. 如果可以回溯，让玩家选择
    if check_can_rewind(card):
        # 创建两个选项卡牌
        accept_option = card.controller.card("REWIND_ACCEPT", source=card)
        retry_option = card.controller.card("REWIND_RETRY", source=card)

        # 将必要信息存储到 retry 选项中（使用 setattr 避免属性冲突）
        object.__setattr__(retry_option, 'original_card', card)
        object.__setattr__(retry_option, 'effect_generator', effect_generator)

        # 让玩家选择：接受结果 or 重新来过
        yield RewindChoice(card.controller, [accept_option, retry_option])
