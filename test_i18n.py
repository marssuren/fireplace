"""
测试 i18n 功能的脚本
"""
import sys
import os

# 添加 fireplace 到路径
sys.path.insert(0, os.path.dirname(__file__))

from fireplace.i18n import set_language, get_language, _

def test_basic_translation():
    """测试基本翻译功能"""
    print("=== 测试基本翻译 ===\n")

    # 测试英文
    set_language("en")
    print(f"Language: {get_language()}")
    print(f"game_start: {_('game_start')}")
    print(f"attack_interrupted: {_('attack_interrupted')}")
    print()

    # 测试中文
    set_language("zh_CN")
    print(f"语言: {get_language()}")
    print(f"game_start: {_('game_start')}")
    print(f"attack_interrupted: {_('attack_interrupted')}")
    print()

def test_formatted_translation():
    """测试带参数的翻译"""
    print("=== 测试格式化翻译 ===\n")

    # 英文
    set_language("en")
    print("English:")
    print(_("attacks", attacker="Minion A", defender="Minion B"))
    print(_("heals", source="Priest", target="Hero", amount=5))
    print()

    # 中文
    set_language("zh_CN")
    print("中文:")
    print(_("attacks", attacker="随从A", defender="随从B"))
    print(_("heals", source="牧师", target="英雄", amount=5))
    print()

if __name__ == "__main__":
    # 设置 UTF-8 输出（Windows 兼容）
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Fireplace i18n 功能测试\n")
    print("=" * 50)

    try:
        test_basic_translation()
        test_formatted_translation()
        print("=" * 50)
        print("[PASS] 所有测试通过!")
    except Exception as e:
        print(f"[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
