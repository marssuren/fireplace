"""
批量转换 actions.py 中的 log.info() 调用为 log_info() 调用的脚本。

使用方法:
    python convert_logs_to_i18n.py

注意: 运行前请备份 actions.py 文件！
"""
import re
import os

# 定义所有需要替换的日志模式
REPLACEMENTS = [
    # 格式: (原始 log.info 调用的正则表达式, 新的 log_info 调用)
    (
        r'log\.info\("%r triggers off %r from %r", entity, self, source\)',
        'log_info("trigger_off", entity=entity, trigger=self, source=source)'
    ),
    (
        r'log\.info\("%r attacks %r", attacker, defender\)',
        'log_info("attacks", attacker=attacker, defender=defender)'
    ),
    (
        r'log\.info\("Attack has been interrupted\."\)',
        'log_info("attack_interrupted")'
    ),
    (
        r'log\.info\("Processing Deathrattle for %r", card\)',
        'log_info("processing_deathrattle", card=card)'
    ),
    (
        r'log\.info\("Jousting %r vs %r", challenger, defender\)',
        'log_info("jousting", challenger=challenger, defender=defender)'
    ),
]

def main():
    file_path = os.path.join(os.path.dirname(__file__), 'fireplace', 'actions.py')

    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        return

    # 读取文件
    print(f"正在读取 {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 备份原文件
    backup_path = file_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已创建备份: {backup_path}")

    # 应用替换
    replaced_count = 0
    for pattern, replacement in REPLACEMENTS:
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            replaced_count += matches
            print(f"  替换了 {matches} 处: {pattern[:50]}...")

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n完成! 共替换了 {replaced_count} 处日志调用。")
    print(f"如需恢复，请使用备份文件: {backup_path}")

if __name__ == '__main__':
    main()
