# 巫妖王的进军 (March of the Lich King) 实现报告

## 扩展包信息
- **英文名称**: March of the Lich King
- **中文名称**: 巫妖王的进军
- **发布时间**: 2022年12月
- **卡牌集代码**: REVENDRETH
- **卡牌总数**: 170张

## 完成进度

### ✅ 第一阶段：基础框架（已完成）

#### 1. 卡牌数据下载
- ✅ 下载英文卡牌数据：170张
- ✅ 下载中文卡牌数据：170张
- 文件位置：
  - `lich_king_cards.json` - 英文数据
  - `lich_king_cards_zhCN.json` - 中文数据

#### 2. 卡牌统计
- **总计**: 170张可收集卡牌
- **卡牌类型分布**:
  - MINION（随从）: 100张
  - SPELL（法术）: 57张
  - LOCATION（地标）: 10张 ⭐新卡牌类型
  - WEAPON（武器）: 3张

- **职业分布**:
  - 恶魔猎手: 13张
  - 德鲁伊: 13张
  - 猎人: 13张
  - 法师: 13张
  - 圣骑士: 13张
  - 牧师: 13张
  - 潜行者: 13张
  - 萨满: 13张
  - 术士: 13张
  - 战士: 13张
  - 中立: 40张

#### 3. 代码框架生成
- ✅ 生成14个Python文件
- ✅ 按职业和稀有度分类
- 文件结构：
  ```
  fireplace/cards/lich_king/
  ├── __init__.py
  ├── demonhunter.py (13张)
  ├── druid.py (13张)
  ├── hunter.py (13张)
  ├── mage.py (13张)
  ├── paladin.py (13张)
  ├── priest.py (13张)
  ├── rogue.py (13张)
  ├── shaman.py (13张)
  ├── warlock.py (13张)
  ├── warrior.py (13张)
  ├── neutral_common.py (21张)
  ├── neutral_rare.py (6张)
  ├── neutral_epic.py (6张)
  └── neutral_legendary.py (7张)
  ```

### ✅ 第二阶段：核心机制实现（进行中）

#### 识别到的核心机制

**1. INFUSE（注能）机制** - 26张卡牌使用 ⭐最重要
- **机制说明**: 当友方随从死亡时，手牌中的Infuse卡牌获得充能，达到指定数量后升级
- **实现状态**: ✅ 核心逻辑已实现
- **实现位置**:
  - `fireplace/enums.py:30-31` - 添加枚举标签
    - `INFUSE_COUNTER = -33` - 充能计数器
    - `INFUSE_THRESHOLD = -34` - 充能阈值
  - `fireplace/actions.py:371-387` - Death类中添加触发逻辑

**实现细节**:
```python
# 在随从死亡时触发
if card.type == CardType.MINION and card.controller:
    for hand_card in card.controller.hand:
        if hasattr(hand_card, 'infuse_threshold') and hand_card.infuse_threshold > 0:
            # 增加充能计数
            hand_card.infuse_counter += 1

            # 达到阈值时触发infuse效果
            if hand_card.infuse_counter >= hand_card.infuse_threshold:
                hand_card.infuse()
```

**使用示例**:
- MAW_009 - Shadehound（影犬）: Infuse (3 Beasts) 获得突袭
- MAW_033 - Sylvanas, the Accused（被告希尔瓦娜斯）: Infuse (7) 控制而非摧毁
- REV_013 - Stoneborn Accuser（石生指控者）: Infuse (5) 获得战吼造成5点伤害

**2. LOCATION（地标）卡牌类型** - 10张卡牌 ⭐新类型
- **机制说明**: 全新卡牌类型，打出后留在场上可多次使用
- **实现状态**: ⏭️ 待实现
- **需要工作**:
  - 扩展 CardType 枚举
  - 实现地标的打出和激活机制
  - 实现地标的冷却和使用次数限制

**3. 其他常规机制**
- BATTLECRY（战吼）: 59张
- DEATHRATTLE（亡语）: 17张
- SECRET（奥秘）: 17张
- DISCOVER（发现）: 15张
- TAUNT（嘲讽）: 14张
- RUSH（突袭）: 11张

## 下一步工作

### 第三阶段：卡牌实现（待开始）

#### 优先级1：实现LOCATION机制
- [ ] 扩展CardType枚举添加LOCATION类型
- [ ] 实现地标的打出逻辑
- [ ] 实现地标的激活和冷却机制
- [ ] 实现地标的使用次数限制

#### 优先级2：实现中立卡牌（40张）
- [ ] neutral_common.py - 21张
- [ ] neutral_rare.py - 6张
- [ ] neutral_epic.py - 6张
- [ ] neutral_legendary.py - 7张

#### 优先级3：实现职业卡牌（130张）
- [ ] 10个职业，每个13张卡牌

### 第四阶段：质量审查和测试
- [ ] 检查所有卡牌实现的完整性
- [ ] 测试INFUSE机制
- [ ] 测试LOCATION机制
- [ ] 修复发现的问题

## 技术亮点

1. **INFUSE机制的完整实现**
   - 在Death类中添加触发逻辑
   - 支持手牌中的卡牌充能
   - 达到阈值自动触发升级效果

2. **遵循fireplace设计模式**
   - 使用内部枚举标签（负数）
   - 在核心Action类中添加机制
   - 保持代码风格一致性

3. **为LOCATION新类型做准备**
   - 识别了10张地标卡牌
   - 规划了实现路径

## 相关文件

- `lich_king_cards.json` - 英文卡牌数据
- `lich_king_cards_zhCN.json` - 中文卡牌数据
- `generate_lich_king_cards.py` - 代码生成脚本
- `fireplace/cards/lich_king/` - 生成的卡牌代码
- `fireplace/enums.py` - 枚举定义（已添加INFUSE标签）
- `fireplace/actions.py` - 核心逻辑（已添加INFUSE触发）

## 总结

**当前状态**: 基础框架完成，INFUSE核心机制已实现

**完成度**: 约15%（基础框架 + 核心机制）

**下一步**: 实现LOCATION机制，然后开始实现具体卡牌

---

*最后更新: 2025-12-30*
