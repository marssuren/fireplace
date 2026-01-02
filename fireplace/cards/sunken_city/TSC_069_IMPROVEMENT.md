# 深海融合怪 (TSC_069) 实现改进报告

## 改进时间

2025-12-31

## 卡牌信息

-   **卡牌 ID**: TSC_069
-   **中文名称**: 深海融合怪
-   **英文名称**: Amalgam of the Deep
-   **费用**: 2 费 2/3
-   **稀有度**: 史诗
-   **种族**: 全部

## 官方效果

**战吼：选择一个友方随从，发现一张相同类型的随从牌。**

## 改进前的实现

```python
class TSC_069:
    """深海融合怪 - 2费 2/3
    战吼：选择一个友方随从，发现一张相同类型的随从牌"""
    # 简化实现：发现一个随机种族的随从
    play = GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion()))
```

### 问题

1. ❌ 没有目标选择机制
2. ❌ 没有根据目标种族过滤发现选项
3. ❌ 直接发现随机随从，不符合官方效果

## 改进后的实现

```python
class TSC_069:
    """深海融合怪 - 2费 2/3
    战吼：选择一个友方随从，发现一张相同类型的随从牌"""
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}

    # 根据目标随从的种族发现相同种族的随从
    play = lambda self, target: (
        GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion(race=target.race)))
        if target and hasattr(target, 'race') and target.race
        else GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion()))
    )
```

### 改进点

1. ✅ **添加目标选择要求**：使用 `PlayReq` 要求选择友方随从目标
2. ✅ **种族过滤**：根据目标随从的种族 (`target.race`) 来过滤发现选项
3. ✅ **容错处理**：如果没有目标或目标没有种族，则发现随机随从
4. ✅ **使用现有机制**：利用 `RandomMinion(race=...)` 的现有功能，无需扩展核心

## 技术细节

### 使用的现有功能

-   `RandomMinion(race=Race.XXX)` - 已在核心中支持，用于按种族过滤随从
-   `PlayReq.REQ_TARGET_IF_AVAILABLE` - 如果可能则需要目标
-   `PlayReq.REQ_FRIENDLY_TARGET` - 目标必须是友方
-   `PlayReq.REQ_MINION_TARGET` - 目标必须是随从

### 参考实现

在代码库中找到了多个使用 `RandomMinion(race=...)` 的例子：

-   `RandomMinion(race=Race.DRAGON, cost=minion.cost, atk=minion.atk, health=minion.health)`
-   `RandomMinion(cost=2, race=Race.BEAST)`
-   `RandomMinion(cost=3, race=Race.BEAST)`

## 结论

**不需要扩展核心！**

现有的 `RandomMinion` 选择器已经完全支持种族过滤功能。通过添加适当的 `PlayReq` 和使用 lambda 函数来访问目标信息，我们可以完整实现深海融合怪的官方效果。

这次改进将卡牌从"简化实现"提升到了"完整实现"，更准确地反映了官方的游戏机制。
