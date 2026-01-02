# 探寻沉没之城 - 中立普通卡牌检查报告

## 检查时间

2025-12-31

## 检查结果

### ✅ 卡牌完整性

**所有 21 张中立普通卡牌均已实现，无遗漏。**

### 已实现的中立普通卡牌列表

| 卡牌 ID | 中文名称     | 英文名称              | 费用 | 类型 |
| ------- | ------------ | --------------------- | ---- | ---- |
| TID_713 | 泡泡元素     | Bubbler               | 1    | 随从 |
| TSC_001 | 海军水雷     | Naval Mine            | 2    | 随从 |
| TSC_002 | 刺豚拳手     | Pufferfist            | 3    | 随从 |
| TSC_007 | 潜水跳板船员 | Gangplank Diver       | 5    | 随从 |
| TSC_013 | 潜水泥鳞鱼人 | Slimescale Diver      | 3    | 随从 |
| TSC_017 | 巫婆纳迦     | Baba Naga             | 4    | 随从 |
| TSC_020 | 野蛮的女巫   | Barbaric Sorceress    | 6    | 随从 |
| TSC_034 | 鳄鱼人掠夺者 | Gorloc Ravager        | 5    | 随从 |
| TSC_053 | 虹彩闪鳞纳迦 | Rainbow Glowscale     | 2    | 随从 |
| TSC_632 | 械钳虾       | Click-Clocker         | 1    | 随从 |
| TSC_638 | 食人鱼集群   | Piranha Swarmer       | 1    | 随从 |
| TSC_640 | 堡礁行者     | Reefwalker            | 3    | 随从 |
| TSC_646 | 海底侦察兵   | Seascout Operator     | 3    | 随从 |
| TSC_647 | 潜水俯冲鹈鹕 | Pelican Diver         | 1    | 随从 |
| TSC_823 | 暗水记录员   | Murkwater Scribe      | 2    | 随从 |
| TSC_909 | 拖网海象人   | Tuskarrrr Trawler     | 2    | 随从 |
| TSC_911 | 挖掘专家     | Excavation Specialist | 4    | 随从 |
| TSC_919 | 艾萨拉的哨兵 | Azsharan Sentinel     | 5    | 随从 |
| TSC_928 | 安保自动机   | Security Automaton    | 2    | 随从 |
| TSC_935 | 自私的扇贝   | Selfish Shellfish     | 4    | 随从 |
| TSC_938 | 宝藏守卫     | Treasure Guard        | 3    | 随从 |

### ✅ 翻译更新

**已将所有卡牌名称和描述更新为官方中文翻译**

#### 主要翻译修正：

1. **TID_713**: Bubbler → **泡泡元素**

    - "受到恰好 1 点伤害" → "在本随从受到刚好一点伤害"
    - "该随从" → "本随从"

2. **TSC_001**: Naval Mine → **海军水雷**

3. **TSC_002**: Pufferfist → **刺豚拳手**

4. **TSC_007**: Gangplank Diver → **潜水跳板船员**

    - "攻击时免疫" → "攻击时具有免疫"

5. **TSC_013**: Slimescale Diver → **潜水泥鳞鱼人**

6. **TSC_017**: Baba Naga → **巫婆纳迦**

    - "持有该牌时" → "本牌在你手中时"

7. **TSC_020**: Barbaric Sorceress → **野蛮的女巫**

    - "双方手牌" → "每个玩家手牌"
    - "法术的费用" → "法术牌的法力值消耗"

8. **TSC_034**: Gorloc Ravager → **鳄鱼人掠夺者**

    - "抽 3 张" → "抽三张"

9. **TSC_053**: Rainbow Glowscale → **虹彩闪鳞纳迦**

10. **TSC_632**: Click-Clocker → **械钳虾**

11. **TSC_638**: Piranha Swarmer → **食人鱼集群**

    - "食人鱼群" → "食人鱼集群"

12. **TSC_640**: Reefwalker → **堡礁行者**

    - "食人鱼群" → "食人鱼集群"

13. **TSC_646**: Seascout Operator → **海底侦察兵**

    - "控制一个机械" → "控制任何机械"
    - "召唤两个" → "召唤两条"

14. **TSC_647**: Pelican Diver → **潜水俯冲鹈鹕**

15. **TSC_823**: Murkwater Scribe → **暗水记录员**

    - "你的下一个法术费用" → "你使用的下一张法术牌法力值消耗"

16. **TSC_909**: Tuskarrrr Trawler → **拖网海象人**

17. **TSC_911**: Excavation Specialist → **挖掘专家**

    - "使其费用" → "选中的牌法力值消耗"

18. **TSC_919**: Azsharan Sentinel → **艾萨拉的哨兵**

    - "洗入...底部" → "置于...底"

19. **TSC_928**: Security Automaton → **安保自动机**

20. **TSC_935**: Selfish Shellfish → **自私的扇贝**

    - "抽 2 张牌" → "抽两张牌"

21. **TSC_938**: Treasure Guard → **宝藏守卫**

#### 术语统一：

-   "持有该牌时" → "本牌在你手中时"
-   "费用" → "法力值消耗"
-   "该随从" → "本随从"
-   "恰好" → "刚好"
-   "食人鱼群" → "食人鱼集群"
-   "洗入" → "置于"
-   数字统一使用中文："3" → "三"，"2" → "两"

### 数据来源

-   英文卡牌数据：`fireplace/sunken_city_cards.json`
-   中文翻译数据：`fireplace/cards_zhCN.json`

## 总结

中立普通卡牌的探寻沉没之城扩展包实现已完成，所有 21 张卡牌均已实现且翻译已更新为官方中文版本。
