#!/usr/bin/env python
"""
检查 Whizbang's Workshop 卡牌文件中的占位符和 TODO 标记

用途：
1. 扫描所有卡牌文件，查找 TODO 标记
2. 识别未实现的卡牌（仅有 pass 语句）
3. 生成待办事项清单
"""

import re
from pathlib import Path


def scan_file(filepath):
    """扫描单个文件，查找占位符和 TODO"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 查找所有类定义
    class_pattern = r'class\s+(\w+):\s*\n\s*"""([^"]+)"""'
    classes = re.findall(class_pattern, content)
    
    results = []
    for class_name, docstring in classes:
        # 查找类的完整内容
        class_start = content.find(f"class {class_name}:")
        next_class = content.find("\nclass ", class_start + 1)
        if next_class == -1:
            class_content = content[class_start:]
        else:
            class_content = content[class_start:next_class]
        
        # 检查是否有 TODO
        has_todo = "TODO" in class_content
        
        # 检查是否只有 pass
        is_placeholder = (
            "pass" in class_content and
            "def " not in class_content and
            "events = " not in class_content and
            "update = " not in class_content
        )
        
        if has_todo or is_placeholder:
            # 提取卡牌名称
            card_name = docstring.split("\n")[0].strip()
            results.append({
                "class": class_name,
                "name": card_name,
                "has_todo": has_todo,
                "is_placeholder": is_placeholder,
            })
    
    return results


def main():
    """主函数"""
    whizbang_dir = Path(__file__).parent.parent
    
    print("=" * 80)
    print("威兹班的工坊 (Whizbang's Workshop) 占位符检查")
    print("=" * 80)
    print()
    
    # 扫描所有 Python 文件
    all_issues = {}
    total_todos = 0
    total_placeholders = 0
    
    for py_file in sorted(whizbang_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        
        results = scan_file(py_file)
        if results:
            all_issues[py_file.stem] = results
            total_todos += sum(1 for r in results if r["has_todo"])
            total_placeholders += sum(1 for r in results if r["is_placeholder"])
    
    # 显示结果
    for filename in sorted(all_issues.keys()):
        issues = all_issues[filename]
        print(f"## {filename}.py ({len(issues)} 个问题)")
        print("-" * 80)
        
        for issue in issues:
            status = []
            if issue["is_placeholder"]:
                status.append("占位符")
            if issue["has_todo"]:
                status.append("TODO")
            
            status_str = ", ".join(status)
            print(f"  [!] {issue['class']} ({issue['name']}): {status_str}")
        
        print()
    
    # 总结
    print("=" * 80)
    print("[SUMMARY] 统计")
    print("=" * 80)
    print(f"包含 TODO 的卡牌: {total_todos}")
    print(f"占位符卡牌: {total_placeholders}")
    print()
    
    if total_todos == 0 and total_placeholders == 0:
        print("[OK] 没有发现占位符或 TODO 标记！")
    else:
        print(f"[TODO] 需要处理 {total_placeholders} 个占位符")
    print()


if __name__ == "__main__":
    main()
