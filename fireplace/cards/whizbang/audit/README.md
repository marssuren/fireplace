# 威兹班的工坊 (Whizbang's Workshop) 测试套件

本目录包含用于验证 Whizbang's Workshop 扩展包卡牌实现的工具。

## 📁 文件说明

### `cards.json`
官方卡牌数据（中文），**包含完整的 373 张卡牌**：
- **183 张可收集卡牌**：所有可以加入套牌的卡牌
- **190 张 Token/不可收集卡牌**：包括 Miniaturize 小型版本、附魔、衍生物等
- 卡牌 ID、名称、描述
- 费用、攻击、生命值等属性
- 稀有度、职业、类型
- 机制标签（Battlecry、Deathrattle、Miniaturize 等）

**数据来源**: `fireplace/cards/233025/zhCN/cards.game_playable.json`（游戏版本 23.30.25）

### `verify_whizbang.py`
**卡牌实现验证工具**

功能：
- 检查所有卡牌是否已实现
- 验证卡牌属性（费用、攻击、生命）是否与官方数据一致
- 按职业生成实现进度报告

使用方法：
```bash
cd fireplace/fireplace/cards/whizbang
python audit/verify_whizbang.py
```

### `check_placeholders.py`
**占位符检查工具**

功能：
- 扫描所有卡牌文件，查找 TODO 标记
- 识别未实现的卡牌（仅有 pass 语句）
- 生成待办事项清单

使用方法：
```bash
cd fireplace/fireplace/cards/whizbang
python audit/check_placeholders.py
```

## 📊 扩展包信息

- **英文名称**: Whizbang's Workshop
- **中文名称**: 威兹班的工坊
- **发布时间**: 2024年3月
- **卡牌总数**: 373 张（183 可收集 + 190 Token）
- **所属年份**: 2024 天马年 (Year of the Pegasus)
- **游戏版本**: 23.30.25

### 职业分布
| 职业 | 卡牌数 |
|------|--------|
| Death Knight | 13 |
| Demon Hunter | 13 |
| Druid | 13 |
| Hunter | 13 |
| Mage | 13 |
| Paladin | 13 |
| Priest | 13 |
| Rogue | 13 |
| Shaman | 13 |
| Warlock | 12 |
| Warrior | 13 |
| Neutral | 40 |

## 🎯 核心机制

根据官方数据分析，本扩展包包含以下核心机制：

### **Miniaturize (小型化)** - 19张卡牌 ⭐ 新机制
- 卡牌入手时自动生成一张费用更低的"小型版本"
- 小型版本通常为 1 费，身材按比例缩小
- Token 卡命名规则：`{原卡ID}t`（例如：`TOY_307t`）
- **已确认有完整的 Token 数据**

### **Gigantify (巨大化)** - 5张卡牌 ⭐ 新机制  
- 卡牌效果根据"本随从的攻击力"进行增强
- 部分卡牌同时拥有 Miniaturize 和 Gigantify（如 `MIS_025`）
- Token 卡命名规则：`{原卡ID}t1`（巨大化版本，例如：`MIS_025t1` 为 8费8/8）

### 其他机制
- **Battlecry** (战吼): 54张
- **Deathrattle** (亡语): 25张  
- **Discover** (发现): 15张
- **Taunt** (嘲讽): 14张
- **Rush** (突袭): 9张
- **Lifesteal** (吸血): 7张

## 📝 实现规范

遵循项目标准：
1. **完整参考核心机制**: 优先复用现有核心机制
2. **扩展核心机制**: 必要时扩展 `Player` 或 `Action` 等核心类
3. **代码整洁**: 保持代码整洁，避免简化/妥协实现
4. **准确实现**: 以 `cards.json` 中的官方数据为准

## 🔄 工作流程

1. **研究机制**: 分析官方数据，识别核心机制
2. **分职业实现**: 按职业逐步实现卡牌
3. **持续验证**: 使用 `verify_whizbang.py` 检查进度
4. **清理占位符**: 使用 `check_placeholders.py` 确保无遗漏

## ✅ 当前状态

- [x] Audit 工具已创建
- [x] 官方数据已准备 (cards.json)
- [ ] 卡牌实现: 0/183 (0%)
- [ ] 核心机制研究
- [ ] 开始实现

---

**上一个扩展包**: Showdown in the Badlands (决战荒芜之地) - ✅ 100% 完成  
**下一个扩展包**: Perils in Paradise (胜地历险记) - 待实现
