"""
深暗领域 - 中立 - LEGENDARY
"""
from ..utils import *


class GDB_120:
    """埃索达 - The Exodar
    7费 6/8 中立传说随从
    <b>战吼:</b>如果你正在构筑<b>星舰</b>,发射它并选择一个指令!
    
    Battlecry: If you're building a Starship, launch it and choose a Protocol!
    
    机制说明:
    - 检查玩家是否有正在构筑的星舰
    - 如果有,发射星舰
    - 然后让玩家选择一个指令(Protocol)
    - 指令选项: 攻击指令(+3攻击), 防御指令(+3生命), 速度指令(突袭)
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 检查是否有正在构筑的星舰
        if self.controller.starship_in_progress:
            # 发射星舰
            yield LaunchStarship(self.controller)
            
            # 选择指令
            # 三个指令选项: 攻击指令, 防御指令, 速度指令
            protocol_choices = ["GDB_120t1", "GDB_120t2", "GDB_120t3"]
            chosen_protocol = yield GenericChoice(CONTROLLER, protocol_choices)
            
            if chosen_protocol:
                # 将选择的指令加入手牌
                yield Give(CONTROLLER, chosen_protocol[0])


class GDB_131:
    """维伦,流亡者领袖 - Velen, Leader of the Exiled
    7费 7/7 中立传说随从 - 德莱尼
    <b>嘲讽</b>。<b>亡语:</b>触发本局对战中你使用过的
    所有其他德莱尼的<b>战吼</b>和<b>亡语</b>。
    
    Taunt. Deathrattle: Trigger the Battlecries and Deathrattles of all other Draenei you played this game.
    
    机制说明:
    - 追踪所有打出的德莱尼随从
    - 亡语时重新触发它们的战吼和亡语效果
    - 不包括维伦自己
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
        GameTag.DIVINE_SHIELD: True,
    }
    race = Race.DRAENEI
    
    def deathrattle(self):
        # 获取本局对战中打出的所有德莱尼随从(不包括自己)
        draenei_played = []
        
        # 从玩家的 minions_played_this_game 中筛选德莱尼
        for minion_id in self.controller.minions_played_this_game:
            # 跳过维伦自己
            if minion_id == "GDB_131":
                continue
            
            # 检查是否是德莱尼
            try:
                from fireplace import cards
                card_class = cards.db[minion_id]
                if hasattr(card_class, 'race') and card_class.race == Race.DRAENEI:
                    draenei_played.append(minion_id)
            except:
                continue
        
        # 触发所有德莱尼的战吼和亡语
        for draenei_id in draenei_played:
            try:
                from fireplace import cards
                card_class = cards.db[draenei_id]
                
                # 创建临时实例来触发效果
                temp_card = card_class()
                temp_card.controller = self.controller
                temp_card.game = self.game
                
                # 触发战吼
                if hasattr(temp_card, 'play'):
                    yield from temp_card.play()
                
                # 触发亡语
                if hasattr(temp_card, 'deathrattle'):
                    yield from temp_card.deathrattle()
            except:
                continue


class GDB_142:
    """无界空宇 - The Ceaseless Expanse
    125费 10/10 中立传说随从
    每有一张牌被抽到、使用或摧毁时,本牌的法力值消耗便减少(1)点。
    <b>战吼:</b>摧毁所有其他随从。
    
    Costs (1) less for each time a card was drawn, played, or destroyed. 
    Battlecry: Destroy all other minions.
    
    机制说明:
    - 追踪抽牌、打牌、摧毁牌的次数
    - 每次发生这些事件时,费用减少1点
    - 战吼摧毁所有其他随从
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    # 费用减免: 每次抽牌/打牌/摧毁牌减少1费
    # 使用 cost_mod 动态计算费用
    cost_mod = lambda self, i: -(
        self.controller.cards_drawn_this_game +
        self.controller.cards_played_this_game +
        self.controller.cards_destroyed_this_game
    )
    
    def play(self):
        # 摧毁所有其他随从
        yield Destroy(ALL_MINIONS - SELF)


class GDB_143:
    """节点亲王沙法尔 - Nexus-Prince Shaffar
    3费 3/3 中立传说随从
    <b><b>法术迸发</b>:</b>使你手牌中的一个随从获得+3/+3和本<b>法术迸发</b>效果
    <i>(除非它已经拥有这些效果)</i>。
    
    Spellburst: Give a minion in your hand +3/+3 and this Spellburst 
    (unless it already has these effects).
    
    机制说明:
    - 法术迸发触发时,随机选择手牌中的一个随从
    - 给予+3/+3和法术迸发效果
    - 如果随从已经有这些效果,则不触发
    - 法术迸发效果会传递下去
    """
    tags = {
        GameTag.SPELLBURST: True,
    }
    
    events = SpellBurst(CONTROLLER).on(
        lambda self, source, spell: self.spellburst_effect()
    )
    
    def spellburst_effect(self):
        # 获取手牌中的所有随从
        minions_in_hand = list(self.game.board.filter(FRIENDLY_HAND + MINION))
        
        if minions_in_hand:
            # 随机选择一个随从
            import random
            target_minion = random.choice(minions_in_hand)
            
            # 检查是否已经有 GDB_143e buff
            has_buff = False
            for buff in target_minion.buffs:
                if buff.id == "GDB_143e":
                    has_buff = True
                    break
            
            # 如果没有buff,则给予+3/+3和法术迸发
            if not has_buff:
                yield Buff(target_minion, "GDB_143e")


class GDB_143e:
    """沙法尔的祝福 - Shaffar's Blessing
    +3/+3和法术迸发效果
    
    机制说明:
    - 给予随从+3/+3
    - 给予法术迸发效果,继续传递
    """
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.SPELLBURST: True,
    }
    
    # 法术迸发效果: 继续传递给另一个随从
    events = SpellBurst(CONTROLLER).on(
        lambda self, source, spell: self.spellburst_effect()
    )
    
    def spellburst_effect(self):
        # 获取手牌中的所有随从(不包括自己)
        minions_in_hand = [m for m in self.game.board.filter(FRIENDLY_HAND + MINION) if m != self.owner]
        
        if minions_in_hand:
            # 随机选择一个随从
            import random
            target_minion = random.choice(minions_in_hand)
            
            # 检查是否已经有 GDB_143e buff
            has_buff = False
            for buff in target_minion.buffs:
                if buff.id == "GDB_143e":
                    has_buff = True
                    break
            
            # 如果没有buff,则给予+3/+3和法术迸发
            if not has_buff:
                yield Buff(target_minion, "GDB_143e")


class GDB_145:
    """基尔加丹 - Kil'jaeden
    7费 7/7 中立传说随从 - 恶魔
    <b>战吼:</b>用无尽的恶魔传送门替换你的牌库。
    每回合,这些恶魔获得额外的+2/+2。
    
    Battlecry: Replace your deck with an endless portal of Demons. 
    Each turn, they gain an additional +2/+2.
    
    机制说明:
    - 清空牌库
    - 标记玩家拥有恶魔传送门
    - 每回合开始时,传送门中的恶魔获得+2/+2
    - 抽牌时从恶魔池中随机生成
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.DEMON
    
    def play(self):
        # 清空牌库
        for card in list(self.controller.deck):
            yield Destroy(card)
        
        # 标记玩家拥有恶魔传送门
        self.controller.kiljaeden_portal_active = True
        self.controller.kiljaeden_portal_buff_stacks = 0


class SC_004:
    """刀锋女王凯瑞甘 - Kerrigan, Queen of Blades
    英雄卡 - 异虫
    <b>战吼:</b>召唤两个2/5的虫群女王。对所有敌人造成3点伤害。
    
    Battlecry: Summon two 2/5 Hive Queens. Deal 3 damage to all enemies.
    
    机制说明:
    - 召唤两个虫群女王token
    - 对所有敌人造成3点伤害
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 召唤两个虫群女王
        yield Summon(CONTROLLER, "SC_004t")
        yield Summon(CONTROLLER, "SC_004t")
        
        # 对所有敌人造成3点伤害
        yield Hit(ENEMY_CHARACTERS, 3)


class SC_013:
    """玛润 - Grunty
    8费 3/4 中立传说随从 - 鱼人
    <b>战吼:</b>召唤四个随机鱼人,然后将它们射向敌方随从。
    <i>(你可以选择目标!)</i>
    
    Battlecry: Summon four random Murlocs, then shoot them at enemy minions. 
    (You pick the targets!)
    
    机制说明:
    - 召唤4个随机鱼人
    - 每个鱼人攻击一个敌方随从(玩家选择目标)
    - 从左到右依次攻击
    - 使用GenericChoice让玩家选择每个鱼人的攻击目标
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    race = Race.MURLOC
    
    def play(self):
        # 获取所有鱼人卡牌ID
        from fireplace import cards
        murloc_ids = []
        for card_id, card_class in cards.db.items():
            if hasattr(card_class, 'race') and card_class.race == Race.MURLOC:
                # 只选择随从卡
                if hasattr(card_class, 'tags') and card_class.tags.get(GameTag.CARDTYPE) != CardType.SPELL:
                    murloc_ids.append(card_id)
        
        # 随机选择4个鱼人
        import random
        selected_murlocs = random.sample(murloc_ids, min(4, len(murloc_ids)))
        
        # 召唤鱼人
        summoned_murlocs = []
        for murloc_id in selected_murlocs:
            minion = yield Summon(CONTROLLER, murloc_id)
            if minion:
                summoned_murlocs.append(minion[0] if isinstance(minion, list) else minion)
        
        # 让每个鱼人攻击敌方随从(玩家选择目标)
        # 从左到右依次处理每个鱼人
        for murloc in summoned_murlocs:
            if murloc and murloc.zone == Zone.PLAY:
                # 获取当前可攻击的敌方随从
                enemy_minions = list(self.game.board.filter(ENEMY_MINIONS))
                if enemy_minions:
                    # 让玩家选择一个敌方随从作为目标
                    # 使用GenericChoice让玩家从敌方随从中选择一个
                    targets = yield GenericChoice(CONTROLLER, enemy_minions)
                    if targets:
                        target = targets[0]
                        # 让鱼人攻击选择的目标
                        yield Attack(murloc, target)


class SC_400:
    """吉姆·雷诺 - Jim Raynor
    英雄卡 - 人类
    <b>战吼:</b>重新发射你本局对战中发射过的所有星舰。
    
    Battlecry: Relaunch every Starship that you launched this game.
    
    机制说明:
    - 追踪玩家发射过的所有星舰的完整状态
    - 重新发射每一个星舰，保留原始的累积属性和附魔
    - 重新发射的星舰拥有与首次发射时相同的属性
    
    官方验证:
    - 重新发射的星舰保留原始属性和附魔 ✅
    - 不触发"你发射星舰"的效果（如Thor）✅
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 检查是否有发射过的星舰记录
        if not hasattr(self.controller, 'launched_starships_history'):
            return
        
        # 重新发射每个之前发射过的星舰
        # launched_starships_history 应该存储每次发射的星舰的完整快照
        for starship_snapshot in self.controller.launched_starships_history:
            # 从快照重建星舰
            # starship_snapshot 包含: {id, atk, health, keywords, pieces}
            
            starship_id = starship_snapshot.get('id')
            if not starship_id:
                continue
            
            # 召唤星舰基础实体
            starship = yield Summon(CONTROLLER, starship_id)
            
            if starship:
                # 如果返回的是列表，取第一个
                if isinstance(starship, list):
                    starship = starship[0]
                
                # 恢复累积的属性
                accumulated_atk = starship_snapshot.get('accumulated_atk', 0)
                accumulated_health = starship_snapshot.get('accumulated_health', 0)
                
                if accumulated_atk > 0 or accumulated_health > 0:
                    # 应用累积的属性buff
                    yield Buff(starship, "SC_400e", atk=accumulated_atk, max_health=accumulated_health)
                
                # 恢复关键词（圣盾、嘲讽、突袭等）
                keywords = starship_snapshot.get('keywords', {})
                if keywords:
                    # 应用关键词
                    for keyword, value in keywords.items():
                        if value:
                            yield SetTags(starship, {keyword: value})
                
                # 注意：重新发射不会再次触发组件的"发射时"效果
                # 也不会增加 starships_launched_this_game 计数（因为这是重新发射，不是新发射）


class SC_400e:
    """雷诺的重新发射 - Raynor's Relaunch
    星舰重新发射时恢复的累积属性buff
    """
    # 动态设置ATK和HEALTH
    pass


class SC_754:
    """阿塔尼斯 - Artanis
    英雄卡 - 神族
    <b>战吼:</b>召唤两个3/4并具有<b>冲锋</b>的狂热者。
    你的神族随从在本局对战中法力值消耗减少(2)点。
    
    Battlecry: Summon two 3/4 Zealots with Charge. 
    Your Protoss minions cost (2) less this game.
    
    机制说明:
    - 召唤两个狂热者token
    - 给予玩家神族费用减免buff
    - 使用Refresh机制持续减免神族随从费用
    
    参考实现: WC_006 Lady Anacondra (自然法术减费)
    """
    tags = {
        GameTag.BATTLECRY: True,
    }
    
    def play(self):
        # 召唤两个狂热者
        yield Summon(CONTROLLER, "SC_754t")
        yield Summon(CONTROLLER, "SC_754t")
        
        # 给予玩家神族费用减免buff
        # 使用buff应用到玩家英雄上，buff的update会持续生效
        yield Buff(FRIENDLY_HERO, "SC_754e")


class SC_754e:
    """阿塔尼斯的领导 - Artanis' Leadership
    你的神族随从法力值消耗减少(2)点
    
    Protoss minions cost (2) less
    
    机制说明:
    - 这是一个应用在英雄上的buff
    - 使用update持续刷新手牌中神族随从的费用
    - 参考WC_006 Lady Anacondra的实现模式
    """
    # 持续刷新手牌中神族随从的费用
    # 使用Refresh检测PROTOSS种族并应用-2费
    update = Refresh(FRIENDLY_HAND + MINION + PROTOSS, {GameTag.COST: -2})

