#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通灵学园卡牌代码生成器
自动生成 fireplace 卡牌实现的基础代码框架
"""

import json
from collections import defaultdict
from typing import Dict, List, Any


def load_cards() -> List[Dict[str, Any]]:
    """加载通灵学园卡牌数据"""
    with open('scholomance_cards.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_card_class_name(card: Dict[str, Any]) -> str:
    """获取卡牌的类名（卡牌ID）"""
    return card['id']


def get_card_comment(card: Dict[str, Any]) -> str:
    """生成卡牌的注释（名称和描述）"""
    name = card.get('name', 'Unknown')
    text = card.get('text', '')
    # 移除 HTML 标签
    text = text.replace('<b>', '').replace('</b>', '')
    text = text.replace('<i>', '').replace('</i>', '')
    text = text.replace('[x]', '').replace('\n', ' ')

    return f'"""{name}\n    {text}"""'


def has_spellburst(card: Dict[str, Any]) -> bool:
    """检查卡牌是否有 Spellburst 机制"""
    mechanics = card.get('mechanics', [])
    return 'SPELLBURST' in mechanics


def has_battlecry(card: Dict[str, Any]) -> bool:
    """检查卡牌是否有战吼"""
    mechanics = card.get('mechanics', [])
    text = card.get('text', '').lower()
    return 'BATTLECRY' in mechanics or 'battlecry' in text


def has_deathrattle(card: Dict[str, Any]) -> bool:
    """检查卡牌是否有亡语"""
    mechanics = card.get('mechanics', [])
    text = card.get('text', '').lower()
    return 'DEATHRATTLE' in mechanics or 'deathrattle' in text


def is_dual_class(card: Dict[str, Any]) -> bool:
    """检查是否是双职业卡牌"""
    classes = card.get('classes', [])
    return len(classes) > 1


def generate_card_code(card: Dict[str, Any]) -> str:
    """生成单张卡牌的代码"""
    class_name = get_card_class_name(card)
    comment = get_card_comment(card)

    lines = [f"class {class_name}:"]
    lines.append(f"    {comment}")
    lines.append("")

    # 添加 TODO 注释
    card_type = card.get('type', 'UNKNOWN')
    mechanics = card.get('mechanics', [])

    if mechanics:
        lines.append(f"    # TODO: Implement mechanics: {', '.join(mechanics)}")

    if has_spellburst(card):
        lines.append("    # TODO: Implement Spellburst effect")
        lines.append("    # spellburst = ...")

    if has_battlecry(card):
        lines.append("    # TODO: Implement Battlecry effect")
        lines.append("    # play = ...")

    if has_deathrattle(card):
        lines.append("    # TODO: Implement Deathrattle effect")
        lines.append("    # deathrattle = ...")

    if card_type == 'SPELL':
        lines.append("    # TODO: Implement spell effect")
        lines.append("    # play = ...")

    if not mechanics and card_type == 'MINION':
        lines.append("    # TODO: Implement card effect")
        lines.append("    pass")

    lines.append("")
    return "\n".join(lines)


def generate_file_header() -> str:
    """生成文件头部"""
    return "from ..utils import *\n\n"


def generate_class_file(cards: List[Dict[str, Any]], class_name: str) -> str:
    """生成一个职业的完整文件内容"""
    lines = [generate_file_header()]

    # 按类型分组
    minions = [c for c in cards if c.get('type') == 'MINION']
    spells = [c for c in cards if c.get('type') == 'SPELL']
    weapons = [c for c in cards if c.get('type') == 'WEAPON']

    if minions:
        lines.append("##")
        lines.append("# Minions")
        lines.append("")
        for card in minions:
            lines.append(generate_card_code(card))

    if spells:
        lines.append("\n##")
        lines.append("# Spells")
        lines.append("")
        for card in spells:
            lines.append(generate_card_code(card))

    if weapons:
        lines.append("\n##")
        lines.append("# Weapons")
        lines.append("")
        for card in weapons:
            lines.append(generate_card_code(card))

    return "\n".join(lines)


if __name__ == "__main__":
    print("通灵学园卡牌代码生成器")
    print("=" * 50)

    cards = load_cards()
    print(f"加载了 {len(cards)} 张卡牌")

    # 按职业分组
    cards_by_class = defaultdict(list)
    for card in cards:
        card_class = card.get('cardClass', 'NEUTRAL')
        cards_by_class[card_class].append(card)

    print(f"\n职业分布:")
    for cls, cls_cards in sorted(cards_by_class.items()):
        print(f"  {cls}: {len(cls_cards)} 张")

    # 生成文件
    print("\n开始生成代码文件...")
    import os
    output_dir = "fireplace/cards/scholomance_generated"
    os.makedirs(output_dir, exist_ok=True)

    for cls, cls_cards in cards_by_class.items():
        if cls == 'NEUTRAL':
            # 中立卡牌按稀有度分文件
            by_rarity = defaultdict(list)
            for card in cls_cards:
                rarity = card.get('rarity', 'COMMON').lower()
                by_rarity[rarity].append(card)

            for rarity, rarity_cards in by_rarity.items():
                filename = f"{output_dir}/neutral_{rarity}.py"
                content = generate_class_file(rarity_cards, f"NEUTRAL_{rarity.upper()}")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  生成: {filename} ({len(rarity_cards)} 张卡)")
        else:
            # 职业卡牌一个文件
            filename = f"{output_dir}/{cls.lower()}.py"
            content = generate_class_file(cls_cards, cls)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  生成: {filename} ({len(cls_cards)} 张卡)")

    print("\n代码生成完成！")
    print(f"输出目录: {output_dir}")
