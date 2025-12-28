"""
批量转换 actions.py 中的所有 log.info() 为 log_info()
"""
import re

def convert_log_calls():
    file_path = r"D:\Projects\Yolo\fireplace\fireplace\actions.py"

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 备份
    with open(file_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(content)

    # 定义所有替换规则
    replacements = [
        # 第1组：简单消息（无参数）
        (r'log\.info\("Attack has been interrupted\."\)',
         'log_info("attack_interrupted")'),
        (r'log\.info\("Game start"\)',
         'log_info("game_start")'),

        # 第2组：单个 %r 参数
        (r'log\.info\("Processing Deathrattle for %r", card\)',
         'log_info("processing_deathrattle", card=card)'),
        (r'log\.info\("Discarding %r", target\)',
         'log_info("discarding", target=target)'),
        (r'log\.info\("Revealing %r", target\)',
         'log_info("revealing", target=target)'),
        (r'log\.info\("Silencing %r", self\)',
         'log_info("silencing", target=self)'),
