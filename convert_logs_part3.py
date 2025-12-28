"""
转换剩余的日志调用 - 第3部分（最后一批）
"""
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_final_replacements():
    """最后一批需要替换的日志"""
    return [
        # 单个参数
        (r'log\.info\("%r requires a target for its battlecry\. Will not trigger\."\)',
         'log_info("requires_target_battlecry", card=card)'),
        (r'log\.info\("Triggering deathrattles for %r again", target\)',
         'log_info("triggering_deathrattles_again", target=target)'),
        (r'log\.info\("%r is dormant cannot be destroyed", target\)',
         'log_info("dormant_cannot_destroy", target=target)'),
        (r'log\.info\("%s can\'t fatigue and does not take damage", target\)',
         'log_info("cant_fatigue", target=target)'),
        (r'log\.info\("%s gets an extra attack change\.", target\)',
         'log_info("extra_attack_change", target=target)'),
        (r'log\.info\("Refresh Hero Power %s\.", heropower\)',
         'log_info("refresh_hero_power", heropower=heropower)'),
        (r'log\.info\("%r clear progress", target\)',
         'log_info("clear_progress", target=target)'),

        # 两个参数
        (r'log\.info\("%r is bounced to a full hand and gets destroyed", target\)',
         'log_info("bounced_destroyed", target=target)'),
        (r'log\.info\("%r is bounced back to %s\'s hand", target, target\.controller\)',
         'log_info("bounced_to_hand", target=target, controller=target.controller)'),
        (r'log\.info\("%s takes %i fatigue damage", target, target\.fatigue_counter\)',
         'log_info("fatigue_damage", target=target, amount=target.fatigue_counter)'),
        (r'log\.info\("Give\(%r\) fails because %r\'s hand is full", card, target\)',
         'log_info("give_fails_hand_full", card=card, target=target)'),
        (r'log\.info\("Retargeting %r\'s attack to %r", target, new_target\)',
         'log_info("retargeting_attack", target=target, new_target=new_target)'),
        (r'log\.info\("Setting current health on %r to %i", target, amount\)',
         'log_info("setting_health", target=target, amount=amount)'),
        (r'log\.info\("%r shuffles into %s\'s deck", cards, target\)',
         'log_info("shuffles_into_deck", cards=cards, target=target)'),
        (r'log\.info\("Shuffle\(%r\) fails because %r\'s deck is full", card, target\)',
         'log_info("shuffle_fails_deck_full", card=card, target=target)'),
        (r'log\.info\("%s summons a Jade Golem for %s", source, target\)',
         'log_info("summons_jade_golem", source=source, target=target)'),
        (r'log\.info\("%s cast spell %s don\'t have a legal target", source, card\)',
         'log_info("spell_no_legal_target", source=source, card=card)'),
        (r'log\.info\("%r add progress from %r", target, card\)',
         'log_info("add_progress", target=target, card=card)'),

        # 三个参数
        (r'log\.info\("%s cast spell %s target %s", source, card, target\)',
         'log_info("cast_spell_target", source=source, card=card, target=target)'),
        (r'log\.info\("%r adapts %r for %s", source, cards, target\)',
         'log_info("adapts", source=source, cards=cards, target=target)'),
    ]

file_path = r"D:\Projects\Yolo\fireplace\fireplace\actions.py"

print("读取文件...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = get_final_replacements()
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
print("所有日志已转换为 i18n 版本！")
