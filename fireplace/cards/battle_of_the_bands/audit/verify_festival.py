import json
import os
import re
import sys

def main():
    # 强制设置控制台编码
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')

    # 1. 确定路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'cards.json')
    target_dir = os.path.dirname(script_dir) # 扫描上一级目录

    if not os.path.exists(json_path):
        print(f"错误: 未找到数据文件 {json_path}")
        return

    # 2. 加载 JSON 数据
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 仅审查可收集卡牌
    collectible_cards = {c['id']: c for c in data if c.get('collectible')}
    print(f"数据源加载完成: 共找到 {len(collectible_cards)} 张可收集卡牌。")

    # 3. 扫描 Python 文件
    implemented_ids = set()
    class_pattern = re.compile(r'class\s+([A-Z0-9_]+)\b')

    py_files = [f for f in os.listdir(target_dir) if f.endswith('.py')]
    print(f"正在扫描 {len(py_files)} 个 Python 文件 (位于 {os.path.basename(target_dir)})...")
    
    for filename in py_files:
        path = os.path.join(target_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = class_pattern.findall(content)
            implemented_ids.update(matches)

    # 4. 比对结果
    missing_ids = []
    implemented_count = 0

    for card_id, card_data in collectible_cards.items():
        if card_id in implemented_ids:
            implemented_count += 1
        else:
            missing_ids.append(card_data)

    # 5. 输出报告
    total = len(collectible_cards)
    progress = (implemented_count / total) * 100 if total > 0 else 0

    print(f"\n================ 审查报告 ================")
    print(f"目标系列: 传奇音乐节 (Festival of Legends)")
    print(f"实现进度: {implemented_count}/{total} ({progress:.1f}%)")
    
    if missing_ids:
        print(f"\n[❌ 缺失卡牌] ({len(missing_ids)} 张):")
        missing_ids.sort(key=lambda x: (x.get('cardClass', 'NEUTRAL'), x.get('cost', 0)))
        current_class = None
        for c in missing_ids:
            card_class = c.get('cardClass', 'NEUTRAL')
            if card_class != current_class:
                print(f"\n--- {card_class} ---")
                current_class = card_class
            print(f"  - {c.get('name', 'Unknown')} (ID: {c['id']}, Cost: {c.get('cost')})")
    else:
        print(f"\n[✅ 完美] 所有可收集卡牌均已在代码中找到定义！")
        print("(注意：此检查仅确认类定义存在，请务必检查逻辑是否为 pass)")

if __name__ == '__main__':
    main()
