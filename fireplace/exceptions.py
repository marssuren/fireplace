class InvalidAction(Exception):
    pass


class GameOver(Exception):
    pass


class InfiniteLoopDetected(Exception):
    """当检测到可能的无限循环时抛出"""
    pass
