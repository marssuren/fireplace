# Paradise Rogue 实现总结

## 完成时间
2026-01-06

## 官方验证状态
✅ **已完成官方数据验证** (2026-01-06)
- 验证通过：13/13 (100%)
- 发现问题：3张（已全部修正）
- 详见：`ROGUE_OFFICIAL_VERIFICATION_REPORT.md`

## 卡牌实现进度
**13/13 (100%)** ✅

## 核心机制扩展

### 1. Player 类扩展 (`player.py`)
添加了两个新属性来追踪"另一职业卡牌"的使用情况：

```python
# 追踪使用过的另一职业卡牌（用于VAC_700横夺硬抢等卡牌）- 胜地历险记（2024年7月）
self.cards_played_from_other_class_count = 0  # 使用过的另一职业卡牌数量
self.last_card_played_from_other_class = None  # 上一张使用的另一职业卡牌
```

### 2. Play Action 扩展 (`actions.py`)
在 Play action 中添加了追踪逻辑：

```python
# 追踪使用过的另一职业卡牌（用于VAC_700横夺硬抢、VAC_333蓄谋诈骗犯等卡牌）
# 判断是否为另一职业的卡牌（排除中立和本职业）
if hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL:
    player_class = player.hero.card_class if player.hero else None
    if player_class and card.card_class != player_class:
        # 这是另一职业的卡牌
        player.cards_played_from_other_class_count += 1
        player.last_card_played_from_other_class = card
```

## 卡牌实现详情

### COMMON (4张)

#### VAC_335 - 小偷小摸 (Petty Theft)
- **费用**: 2
- **类型**: 法术
- **效果**: 随机获取两张其他职业的法力值消耗为（1）的法术牌
- **实现**: 使用 `RandomCollectible` 配合 `~CardClass.ROGUE` 过滤器

#### VAC_460 - 把经理叫来！ (Oh, Manager!)
- **费用**: 2
- **类型**: 法术
- **效果**: 造成$2点伤害。连击：获取一张幸运币
- **实现**: 基础伤害 + 连击效果获得 `GAME_005` (幸运币)

#### VAC_332 - 海滩导购 (Sea Shill)
- **费用**: 3
- **类型**: 随从 (3/2 海盗)
- **效果**: 战吼：你使用的下一张另一职业的牌法力值消耗减少（2）点
- **实现**: 
  - 给玩家添加 `VAC_332e` buff
  - 监听 Play 事件，检查卡牌职业
  - 匹配时给卡牌添加减费 buff 并移除玩家 buff

#### WORK_005 - 快刀快递 (Sharp Shipment)
- **费用**: 4
- **类型**: 法术
- **效果**: 使你的武器获得+2/+2
- **实现**: 给武器添加 `WORK_005e` buff（+2攻击力和+2耐久度）

### RARE (5张)

#### VAC_330 - 金属探测器 (Metal Detector)
- **费用**: 3
- **类型**: 武器 (3/2)
- **效果**: 亡语：获取一张幸运币
- **实现**: 亡语效果 `Give(CONTROLLER, "GAME_005")`

#### VAC_334 - 小玩物小屋 (Knickknack Shack)
- **费用**: 3
- **类型**: 地标 (4生命值)
- **效果**: 抽一张牌。如果你在本回合中使用抽到的这张牌，重新开启本地标
- **实现**:
  - 抽牌后给抽到的牌添加 `VAC_334e` buff
  - buff 监听 Play 事件
  - 如果在本回合使用，重置地标的 `exhausted` 属性

#### WORK_006 - 拨号机器人 (Robocaller)
- **费用**: 3
- **类型**: 随从 (3/2 机械)
- **效果**: 战吼：抽取法力值消耗为{0}，{1}和{2}的牌各一张。（每回合随机拨号！）
- **实现**: 
  - 随机生成3个不同的费用（0-10）
  - 从牌库中抽取对应费用的牌

#### VAC_333 - 蓄谋诈骗犯 (Conniving Conman)
- **费用**: 4
- **类型**: 随从 (4/4 海盗)
- **效果**: 战吼：再次使用你使用过的上一张另一职业的牌
- **实现**:
  - 使用 `controller.last_card_played_from_other_class` 获取上一张卡牌
  - 根据卡牌类型（法术/随从/武器）重新使用

#### WORK_004 - 旅社谍战 (Agency Espionage)
- **费用**: 4
- **类型**: 法术
- **效果**: 将每个其他职业的各一张牌洗入你的牌库，其法力值消耗为（1）点
- **实现**:
  - 遍历所有其他职业（排除潜行者和中立）
  - 从每个职业获取一张随机卡牌
  - 设置费用为1并洗入牌库

### EPIC (2张)

#### VAC_701 - 刀剑保养师 (Swarthy Swordshiner)
- **费用**: 3
- **类型**: 随从 (3/3 海盗)
- **效果**: 战吼：将你的武器的攻击力和耐久度变为3
- **实现**: 使用 `SetTag` 设置武器的 `ATK` 和 `DURABILITY` 为3

#### VAC_700 - 横夺硬抢 (Snatch and Grab)
- **费用**: 8
- **类型**: 法术
- **效果**: 随机消灭两个敌方随从。你每使用过一张另一职业的卡牌，本牌的法力值消耗便减少（1）点
- **实现**:
  - 随机选择最多2个敌方随从并消灭
  - Hand 类中实现费用减免：`i - cards_played_from_other_class_count`

### LEGENDARY (2张)

#### VAC_336 - 面具变装大师 (Maestra, Mask Merchant)
- **费用**: 5
- **类型**: 随从 (6/5)
- **效果**: 术士游客。战吼：发现一张来自过去的（另一职业的）英雄牌
- **实现**: 
  - 使用 `GenericChoice` + `Discover`
  - 过滤器：`card_class=~CardClass.ROGUE, type=CardType.HERO`

#### VAC_464 - 财宝猎人尤朵拉 (Treasure Hunter Eudora)
- **费用**: 5
- **类型**: 随从 (4/5 海盗)
- **效果**: 战吼：开启一项使用3张其他职业的牌即可完成的支线任务，发现神奇的战利品！
- **实现**:
  - 给玩家添加 `VAC_464e` buff（支线任务效果）
  - 记录初始的 `cards_played_from_other_class_count`
  - 监听 Play 事件，检查是否使用了另一职业的牌
  - 使用3张后完成任务，发现传说卡牌

## 技术亮点

### 1. 另一职业卡牌判定
```python
if hasattr(card, 'card_class') and card.card_class != CardClass.NEUTRAL:
    player_class = player.hero.card_class if player.hero else None
    if player_class and card.card_class != player_class:
        # 这是另一职业的卡牌
```

### 2. 地标重开机制 (VAC_334)
- 通过监听 Play 事件
- 检查打出的牌是否为抽到的牌
- 检查是否在本回合
- 重置地标的 `exhausted` 属性

### 3. 支线任务系统 (VAC_464)
- 使用 buff 存储任务状态
- 记录初始计数器
- 监听事件并检查完成条件
- 完成后触发奖励并移除 buff

### 4. 动态费用减免 (VAC_700)
- 使用 Hand 类的 cost 方法
- 根据核心引擎追踪的数据动态计算费用

## 代码质量

- ✅ 完整中文注释
- ✅ 符合项目规范
- ✅ 无简化/妥协实现
- ✅ 无未声明的属性或机制
- ✅ 核心引擎扩展已完成

## 下一步

建议进行以下工作：
1. 官方数据验证（通过 web 搜索验证所有卡牌效果）
2. 单元测试（测试核心机制和复杂卡牌）
3. 继续实现其他职业（Shaman, Warlock, Warrior）
