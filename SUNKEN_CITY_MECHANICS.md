# 探寻沉没之城新机制分析

## 1. DREDGE（疏浚）机制

### 机制说明
**Dredge** 允许玩家查看牌库底部的3张牌，并选择其中一张移到牌库顶部。

### 实现要点
- 需要实现查看牌库底部的功能
- 需要实现选择并移动卡牌的功能
- 在AI训练中，可以随机选择或使用策略选择

### 示例卡牌
1. **TID_003 - Tidelost Burrower**
   - 战吼：疏浚。如果是鱼人，召唤一个2/2的复制。

2. **TID_099 - K9-0tron**
   - 战吼：疏浚。如果是1费随从，召唤它。

3. **TID_700 - Disarming Elemental**
   - 战吼：为对手疏浚。将其费用设为6。

### 实现方案
```python
# 添加到 fireplace/actions.py
class Dredge(TargetedAction):
    """疏浚：查看牌库底部3张牌，选择一张移到顶部"""

    def do(self, source, target):
        # 获取牌库底部3张牌
        deck = target.controller.deck
        if len(deck) < 1:
            return

        # 查看底部最多3张
        bottom_cards = deck[-min(3, len(deck)):]

        # AI训练中随机选择一张（或使用策略）
        if bottom_cards:
            chosen = random.choice(bottom_cards)
            # 移到顶部
            deck.remove(chosen)
            deck.insert(0, chosen)
```

---

## 2. COLOSSAL（巨型）机制

### 机制说明
**Colossal** 随从在召唤时会额外召唤附属部件（Appendages）。
- Colossal +N 表示召唤N个附属部件
- 附属部件是独立的随从，有自己的效果

### 示例卡牌
1. **TSC_962 - Gigafin (巨鳍鲨)**
   - 7费 7/4 Colossal +2
   - 战吼：吞噬3个敌方随从
   - 亡语：吐出被吞噬的随从

2. **TSC_950 - Hydralodon (九头蛇龙)**
   - 8费 5/5 Colossal +2
   - 突袭，每个头部独立攻击

3. **TSC_937 - Crabatoa (巨蟹)**
   - 7费 5/4 Colossal +1
   - 战吼：获得+1/+1（每有一个友方随从）

### 实现方案
```python
# 在 fireplace/actions.py 的 Summon.do() 中添加
def do(self, source, target):
    # ... 现有召唤逻辑 ...
    
    # 检查是否有 Colossal
    if hasattr(target, 'colossal_appendages'):
        # 召唤附属部件
        for appendage_id in target.colossal_appendages:
            yield Summon(target.controller, appendage_id)
```

## 3. AZSHARAN（艾萨拉）机制

### 机制说明
**Azsharan** 卡牌会将一张"沉没的"（Sunken）版本洗入牌库底部。
- 打出Azsharan卡牌时，触发效果并洗入Sunken版本
- Sunken版本通常是增强版，费用更高，效果更强

### 示例卡牌
1. **TSC_039 - Azsharan Scavenger (艾萨拉拾荒者)**
   - 2费 2/3 战吼：将"沉没的拾荒者"洗入牌库底部
   - Sunken版本：4费 4/6

2. **TSC_057 - Azsharan Defector (艾萨拉叛逃者)**
   - 2费 2/3 战吼：将"沉没的叛逃者"洗入牌库底部
   - Sunken版本：5费 5/6 战吼：发现一张法术

### 实现方案
```python
# 在卡牌定义中
class TSC_039:
    """Azsharan Scavenger"""
    play = Shuffle(CONTROLLER, "TSC_039t", position=BOTTOM)

class TSC_039t:
    """Sunken Scavenger"""
    # 增强版本的定义
    pass
```


---

## 实现优先级

### 高优先级（核心机制）
1. **Dredge** - 20张卡牌使用，需要扩展fireplace核心
2. **Colossal** - 12张卡牌使用，需要修改Summon逻辑
3. **Azsharan** - 11张卡牌使用，相对简单，使用现有Shuffle

### 实现策略
1. 先实现Azsharan（最简单）
2. 再实现Dredge（需要新Action）
3. 最后实现Colossal（需要修改核心召唤逻辑）

---

## 下一步行动
1. 生成卡牌代码框架（170张）
2. 实现Azsharan机制
3. 实现Dredge机制
4. 实现Colossal机制
5. 逐个实现卡牌效果

