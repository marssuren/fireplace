"""
转换剩余的日志调用 - 第2部分
"""
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_remaining_replacements():
    """剩余需要替换的日志"""
    return [
        # 四个参数
        (r'log\.info\("%s plays %r \(target=%r, index=%r\)", player, card, target, index\)',
         'log_info("plays_card", player=player, card=card, target=target, index=index)'),

        # 三个参数
        (r'log\.info\("%r overloads %s for %i", source, player, amount\)',
         'log_info("overloads", source=source, player=player, amount=amount)'),
        (r'log\.info\("%r discovers %r for %s", source, cards, target\)',
         'log_info("discovers", source=source, cards=cards, target=target)'),
        (r'log\.info\("%r heals %r for %i", source, target, amount\)',
         'log_info("heals", source=source, target=target, amount=amount)'),
        (r'log\.info\("Activating %r combo targeting %r", card, target\)',
         'log_info("activating_combo", card=card, target=target)'),
        (r'log\.info\("Activating %r action targeting %r", card, target\)',
         'log_info("activating_action", card=card, target=target)'),

        # 两个参数
        (r'log\.info\("%r cannot overload %s", source, player\)',
         'log_info("cannot_overload", source=source, player=player)'),
        (r'log\.info\("%r queues up callback %r", self, action\)',
         'log_info("queues_callback", action=self, callback=action)'),
        (r'log\.info\("%r put on %s\'s deck top", cards, target\)',
         'log_info("put_on_deck_top", cards=cards, target=target)'),
        (r'log\.info\("Put\(%r\) fails because %r\'s deck is full", card, target\)',
         'log_info("put_fails_deck_full", card=card, target=target)'),
        (r'log\.info\("%s overdraws and loses %r!", target, card\)',
         'log_info("overdraws", target=target, card=card)'),
        (r'log\.info\("%s draws %r", target, card\)',
         'log_info("draws", target=target, card=card)'),
        (r'log\.info\("%s pays %i mana", target, amount\)',
         'log_info("pays_mana", target=target, amount=amount)'),
    ]

file_path = r"D:\Projects\Yolo\fireplace\fireplace\actions.py"

print("读取文件...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = get_remaining_replacements()
total = 0

for pattern, replacement in replacements:
    count = len(re.findall(pattern, content))
    if count > 0:
        content = re.sub(pattern, replacement, content)
        total += count
        print(f"[OK] 替换 {count} 处")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n完成! 共替换 {total} 处")
