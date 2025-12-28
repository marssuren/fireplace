"""
自动转换 actions.py 中的日志调用为 i18n 版本
运行此脚本将自动替换所有 log.info() 为 log_info()
"""
import re
import os

def main():
    file_path = r"D:\Projects\Yolo\fireplace\fireplace\actions.py"

    print("正在读取文件...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建备份
    backup_path = file_path + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已创建备份: {backup_path}")

    # 定义所有替换规则（按行号顺序）
    replacements = [
        # 行155
        (r'log\.info\("%r triggers off %r from %r", entity, self, source\)',
         'log_info("trigger_off", entity=entity, trigger=self, source=source)'),

        # 行241
        (r'log\.info\("%r attacks %r", attacker, defender\)',
         'log_info("attacks", attacker=attacker, defender=defender)'),

        # 行257
        (r'log\.info\("Attack has been interrupted\."\)',
         'log_info("attack_interrupted")'),

        # 行365
        (r'log\.info\("Processing Deathrattle for %r", card\)',
         'log_info("processing_deathrattle", card=card)'),

        # 行412
        (r'log\.info\("Jousting %r vs %r", challenger, defender\)',
         'log_info("jousting", challenger=challenger, defender=defender)'),
    ]

    print("\n开始替换...")
    count = 0
    for pattern, replacement in replacements:
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            count += matches
            print(f"  ✓ 替换了 {matches} 处")

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n完成! 共替换了 {count} 处日志调用")
    print(f"如需恢复，请使用: {backup_path}")

if __name__ == '__main__':
    main()
