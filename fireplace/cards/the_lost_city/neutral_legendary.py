"""
失落之城 - NEUTRAL LEGENDARY (完整实现版)
"""
from ..utils import *


# ========================================
# DINO_410 - 凯洛斯的蛋
# ========================================

class DINO_410:
    """凯洛斯的蛋 - The Egg of Kairos
    
    3费 0/3 传说
    <b>亡语：</b>召唤一枚轻微开裂的蛋。<i>（破壳5次即可孵化为一只20/20并具有<b>嘲讽</b>的野兽！）</i>
    
    官方验证: ✅
    - 属性: 3费 0/3
    - 亡语：召唤下一阶段的蛋
    - 5个阶段：原始蛋 → 轻微开裂 → 开裂 → 严重开裂 → 即将孵化 → 凯洛斯（20/20嘲讽野兽）
    
    参考实现:
    - 使用 Token 系统定义各阶段的蛋
    - 每个阶段的亡语召唤下一阶段
    
    Token 定义:
    - DINO_410t1: 轻微开裂的蛋 (Slightly Cracked Egg)
    - DINO_410t2: 开裂的蛋 (Cracked Egg)
    - DINO_410t3: 严重开裂的蛋 (Heavily Cracked Egg)
    - DINO_410t4: 即将孵化的蛋 (Nearly Hatched Egg)
    - DINO_410t5: 凯洛斯 (Kairos) - 20/20 嘲讽野兽
    """
    # 亡语：召唤轻微开裂的蛋
    deathrattle = Summon(CONTROLLER, "DINO_410t1")


# ========================================
# DINO_430 - 兽语者塔卡
# ========================================

class DINO_430:
    """兽语者塔卡 - Beast Speaker Taka
    
    7费 2/2 传说
    <b>战吼：</b><b>发现</b>一只任意职业的<b>传说</b>野兽并获得其属性值。<b>亡语：</b>召唤该野兽。
    
    官方验证: ✅
    - 属性: 7费 2/2
    - 战吼：发现传说野兽，获得其攻击力和生命值
    - 亡语：召唤发现的野兽
    
    参考实现:
    - EDR_856 (Nightmare Lord Xavius) - 使用 Choice 发现
    - 使用 Buff 存储发现的野兽ID和属性
    - 使用 @property deathrattle 动态召唤
    
    实现说明:
    - 使用 Choice 发现传说野兽（不自动加入手牌）
    - 使用 Buff 修改塔卡的属性值
    - 将野兽ID存储在 buff 中
    - 亡语时召唤该野兽
    
    核心修复:
    - 不使用 GenericChoice（会自动加入手牌）
    - 使用 Buff 修改属性而不是直接赋值
    """
    
    def play(self):
        # 发现一张传说野兽牌（使用 Choice 避免自动加入手牌）
        yield Choice(
            CONTROLLER,
            cards=RandomCardGenerator(
                CONTROLLER,
                card_filter=lambda c: (
                    c.type == CardType.MINION and
                    c.rarity == Rarity.LEGENDARY and
                    Race.BEAST in (c.races if hasattr(c, 'races') and c.races else [c.race] if hasattr(c, 'race') and c.race else [])
                ),
                count=3
            )
        ).then(
            # 选择后处理：存储ID并修改属性
            lambda self, choice: self._handle_discovered_beast(choice)
        )
    
    def _handle_discovered_beast(self, beast_card):
        """处理发现的野兽：存储ID并修改属性"""
        if not beast_card:
            return []
        
        # 获取野兽的属性
        beast_atk = beast_card.atk
        beast_health = beast_card.max_health
        beast_id = beast_card.id
        
        # 存储野兽ID到 buff 中（用于亡语）
        yield Buff(SELF, "DINO_430e", beast_id=beast_id)
        
        # 使用 Buff 修改塔卡的属性值
        # 计算需要增加的属性值
        atk_bonus = beast_atk - self.atk
        health_bonus = beast_health - self.max_health
        
        if atk_bonus != 0 or health_bonus != 0:
            yield Buff(SELF, "DINO_430e2", atk=atk_bonus, max_health=health_bonus)
    
    @property
    def deathrattle(self):
        """动态亡语：召唤发现的野兽"""
        # 查找 buff 中存储的野兽ID
        beast_id = None
        for buff in self.buffs:
            if buff.id == "DINO_430e" and hasattr(buff, 'beast_id'):
                beast_id = buff.beast_id
                break
        
        if beast_id:
            return Summon(CONTROLLER, beast_id)
        else:
            # 如果没有发现野兽，返回空操作
            return []


class DINO_430e:
    """兽语者塔卡增益 - 存储发现的野兽ID"""
    # 这个 buff 仅用于存储数据，不提供属性加成
    pass


class DINO_430e2:
    """兽语者塔卡增益 - 属性值修改"""
    # 这个 buff 用于修改属性值
    # atk 和 max_health 会在运行时动态设置
    pass


# ========================================
# TLC_100 - 导航员伊莉斯
# ========================================

class TLC_100:
    """导航员伊莉斯 - Elise the Navigator
    
    4费 3/5 传说
    <b>战吼：</b>如果你的套牌中的牌有10种不同的法力值消耗，制造一个自定义的地标。
    
    官方验证: ✅
    - 属性: 4费 3/5
    - 条件：套牌中有10种不同费用的牌
    - 效果：制造自定义地标（Un'Goro Pack）
    
    参考实现:
    - 检查套牌中不同费用的数量
    - 使用 Give 给予自定义地标
    
    实现说明:
    - 遍历套牌中的所有牌
    - 统计不同的法力值消耗
    - 如果达到10种，给予地标 Token
    """
    
    def play(self):
        # 统计套牌中不同的法力值消耗
        cost_set = set()
        for card in self.controller.deck:
            cost_set.add(card.cost)
        
        # 如果有10种不同的法力值消耗
        if len(cost_set) >= 10:
            # 制造自定义地标（Un'Goro Pack）
            yield Give(CONTROLLER, "TLC_100t")


# ========================================
# TLC_102 - 托加
# ========================================

class TLC_102:
    """托加 - Torga
    
    4费 2/7 亡灵+野兽 传说
    <b>战吼：</b>抽一张<b>延系</b>牌以及另一张可以激活其效果的牌。
    
    官方验证: ✅
    - 属性: 4费 2/7 亡灵+野兽
    - 战吼：抽延系牌 + 激活牌
    
    参考实现:
    - 从牌库中查找延系牌
    - 从牌库中查找可以激活该延系牌的牌
    - 使用 ForceDraw 抽取指定卡牌
    
    实现说明:
    - 延系牌：具有 KINDRED 标签的牌
    - 激活牌：与延系牌相同类型/学派的牌
    - 先抽延系牌，再抽激活牌
    
    核心修复:
    - 使用 ForceDraw 而不是 Draw 来抽取指定卡牌
    """
    
    def play(self):
        from .kindred_helpers import check_kindred_active
        
        # 从牌库中查找延系牌
        kindred_cards = [c for c in self.controller.deck if c.tags.get(GameTag.KINDRED, False)]
        
        if kindred_cards:
            # 随机选择一张延系牌并抽取
            import random
            kindred_card = random.choice(kindred_cards)
            yield ForceDraw(CONTROLLER, kindred_card)
            
            # 查找可以激活该延系牌的牌
            # 需要检查随从类型或法术学派
            activator_cards = []
            
            for card in self.controller.deck:
                if card == kindred_card:
                    continue
                
                # 检查是否可以激活延系效果
                # 随从：检查种族
                if card.type == CardType.MINION and kindred_card.type == CardType.MINION:
                    if hasattr(card, 'races') and hasattr(kindred_card, 'races'):
                        if any(race in kindred_card.races for race in card.races if race != Race.INVALID):
                            activator_cards.append(card)
                    elif hasattr(card, 'race') and hasattr(kindred_card, 'race'):
                        if card.race == kindred_card.race and card.race != Race.INVALID:
                            activator_cards.append(card)
                
                # 法术：检查学派
                if card.type == CardType.SPELL and kindred_card.type == CardType.SPELL:
                    if hasattr(card, 'spell_school') and hasattr(kindred_card, 'spell_school'):
                        if card.spell_school == kindred_card.spell_school and card.spell_school != SpellSchool.INVALID:
                            activator_cards.append(card)
            
            # 如果找到激活牌，随机抽取一张
            if activator_cards:
                activator_card = random.choice(activator_cards)
                yield ForceDraw(CONTROLLER, activator_card)
        else:
            # 如果没有延系牌，抽两张普通牌
            yield Draw(CONTROLLER)
            yield Draw(CONTROLLER)


# ========================================
# TLC_106 - 末日使者安布拉
# ========================================

class TLC_106:
    """末日使者安布拉 - Spiritsinger Umbra
    
    7费 6/6 传说
    <b>战吼：</b>触发本局对战中死亡的5个友方随从的<b>亡语</b>。
    
    官方验证: ✅
    - 属性: 7费 6/6
    - 战吼：触发墓地中5个随从的亡语
    
    参考实现:
    - N'Zoth 系列卡牌 - 复活亡语随从
    - 使用 FRIENDLY_GRAVEYARD 查找亡语随从
    
    实现说明:
    - 从墓地中查找具有亡语的随从
    - 随机选择5个
    - 触发它们的亡语效果
    """
    
    def play(self):
        # 从墓地中查找具有亡语的随从
        deathrattle_minions = [
            m for m in self.controller.graveyard 
            if m.type == CardType.MINION and m.tags.get(GameTag.DEATHRATTLE, False)
        ]
        
        # 随机选择最多5个
        import random
        selected_minions = random.sample(deathrattle_minions, min(5, len(deathrattle_minions)))
        
        # 触发它们的亡语效果
        for minion in selected_minions:
            # 获取亡语效果
            if hasattr(minion, 'deathrattle'):
                deathrattle_effect = minion.deathrattle
                
                # 如果是 property，需要获取其值
                if isinstance(deathrattle_effect, property):
                    deathrattle_effect = deathrattle_effect.fget(minion)
                
                # 触发亡语效果
                if deathrattle_effect:
                    yield deathrattle_effect


# ========================================
# TLC_110 - 城市首脑埃舒
# ========================================

class TLC_110:
    """城市首脑埃舒 - City Chief Esho
    
    6费 5/7 传说
    <b>战吼：</b>如果你牌库中的随从牌均属于同一随从类型，使你的其他随从获得+2/+2<i>（无论它们在哪）</i>。
    
    官方验证: ✅
    - 属性: 6费 5/7
    - 条件：牌库中所有随从同一种族
    - 效果：所有其他随从+2/+2（手牌、牌库、场上）
    
    参考实现:
    - 检查牌库中随从的种族
    - 使用 Buff 给予全局加成
    
    实现说明:
    - 遍历牌库中的所有随从
    - 检查是否都属于同一种族
    - 如果是，给手牌、牌库、场上的其他随从+2/+2
    """
    
    def play(self):
        # 获取牌库中的所有随从
        deck_minions = [c for c in self.controller.deck if c.type == CardType.MINION]
        
        if not deck_minions:
            return
        
        # 检查是否所有随从都属于同一种族
        # 注意：需要处理多种族随从
        race_set = set()
        
        for minion in deck_minions:
            # 获取随从的种族列表
            if hasattr(minion, 'races') and minion.races:
                # 多种族随从：添加所有非 INVALID 的种族
                for race in minion.races:
                    if race != Race.INVALID:
                        race_set.add(race)
            elif hasattr(minion, 'race') and minion.race and minion.race != Race.INVALID:
                # 单种族随从
                race_set.add(minion.race)
        
        # 如果只有一个种族（或没有种族），满足条件
        if len(race_set) <= 1:
            # 给所有其他随从+2/+2
            # 场上的随从
            yield Buff(FRIENDLY_MINIONS - SELF, "TLC_110e")
            # 手牌中的随从
            yield Buff(FRIENDLY_HAND + MINION, "TLC_110e")
            # 牌库中的随从
            yield Buff(FRIENDLY_DECK + MINION, "TLC_110e")


class TLC_110e:
    """城市首脑埃舒增益 - +2/+2"""
    atk = 2
    max_health = 2


# ========================================
# TLC_480 - 克罗格，环形山之王
# ========================================

class TLC_480:
    """克罗格，环形山之王 - Krog, Crater King
    
    9费 8/7 野兽 传说
    在你的回合结束时，将所有敌方随从的攻击力和生命值变为1。
    
    官方验证: ✅
    - 属性: 9费 8/7 野兽
    - 回合结束时：敌方随从属性变为1/1
    
    参考实现:
    - 使用 OWN_TURN_END 事件
    - 使用 Buff 将属性设置为1/1
    
    实现说明:
    - 监听己方回合结束事件
    - 给所有敌方随从施加属性重置 buff
    """
    
    # 监听己方回合结束事件
    events = OWN_TURN_END.on(
        # 将所有敌方随从的属性值变为1/1
        Buff(ENEMY_MINIONS, "TLC_480e")
    )


class TLC_480e:
    """克罗格增益 - 属性值变为1/1"""
    # 使用 lambda 函数将属性设置为固定值
    atk = lambda self, i: 1
    max_health = lambda self, i: 1

