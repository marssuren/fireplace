"""
完整的日志转换脚本 - 将 actions.py 中所有 log.info() 转换为 log_info()
"""
import re

def get_all_replacements():
    """返回所有需要替换的日志调用"""
    return [
        # 第1部分：简单消息（无参数）
        (r'log\.info\("Attack has been interrupted\."\)',
         'log_info("attack_interrupted")'),
        (r'log\.info\("Game start"\)',
         'log_info("game_start")'),

        # 第2部分：三个参数
        (r'log\.info\("%r triggers off %r from %r", entity, self, source\)',
         'log_info("trigger_off", entity=entity, trigger=self, source=source)'),
        (r'log\.info\("%r triggering %r targeting %r", source, self, targets\)',
         'log_info("triggering_targeting", source=source, trigger=self, targets=targets)'),
        (r'log\.info\("%r copy deathrattle from %r by %r", source, target, buff\)',
         'log_info("copy_deathrattle", source=source, target=target, buff=buff)'),
        (r'log\.info\("%r marks %r for imminent death", source, target\)',
         'log_info("marks_imminent_death", source=source, target=target)'),
        (r'log\.info\("Retargeting %r from %r to %r", target, target\.target, new_target\)',
         'log_info("retargeting_from_to", target=target, old_target=target.target, new_target=new_target)'),

        # 第3部分：两个参数
        (r'log\.info\("%r attacks %r", attacker, defender\)',
         'log_info("attacks", attacker=attacker, defender=defender)'),
        (r'log\.info\("Jousting %r vs %r", challenger, defender\)',
         'log_info("jousting", challenger=challenger, defender=defender)'),
        (r'log\.info\("%r destroys %r", source, target\)',
         'log_info("destroys", source=source, target=target)'),
        (r'log\.info\("Morphing %r into %r", target, card\)',
         'log_info("morphing", target=target, card=card)'),
        (r'log\.info\("%r choice from %r", player, cards\)',
         'log_info("choice_from", player=player, cards=cards)'),
        (r'log\.info\("%r store card %r", buff, card\)',
         'log_info("store_card", buff=buff, card=card)'),
        (r'log\.info\("Giving %r to %s", cards, target\)',
         'log_info("giving_to", cards=cards, target=target)'),
        (r'log\.info\("%s summons %r", target, cards\)',
         'log_info("summons", target=target, cards=cards)'),
        (r'log\.info\("%s takes control of %r", controller, target\)',
         'log_info("takes_control", controller=controller, target=target)'),
        (r'log\.info\("swap state %s and %s", target, other\)',
         'log_info("swap_state", target=target, other=other)'),

        # 第4部分：单个参数
        (r'log\.info\("Processing Deathrattle for %r", card\)',
         'log_info("processing_deathrattle", card=card)'),
        (r'log\.info\("Discarding %r", target\)',
         'log_info("discarding", target=target)'),
        (r'log\.info\("Revealing %r", target\)',
         'log_info("revealing", target=target)'),
        (r'log\.info\("Silencing %r", self\)',
         'log_info("silencing", target=self)'),
        (r'log\.info\("%s overload gets cleared", target\)',
         'log_info("overload_cleared", target=target)'),
        (r'log\.info\("Choosing card %r" % \(choice\)\)',
         'log_info("choosing_card", choice=choice)'),
    ]

def main():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    file_path = r"D:\Projects\Yolo\fireplace\fireplace\actions.py"

    print("读取文件...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 备份
    backup = file_path + '.backup'
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"备份: {backup}")

    # 替换
    replacements = get_all_replacements()
    total = 0

    for pattern, replacement in replacements:
        count = len(re.findall(pattern, content))
        if count > 0:
            content = re.sub(pattern, replacement, content)
            total += count
            print(f"[OK] 替换 {count} 处")

    # 保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n完成! 共 {total} 处")

if __name__ == '__main__':
    main()
