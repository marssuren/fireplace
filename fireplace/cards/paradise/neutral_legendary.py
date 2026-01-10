"""
胜地历险记 - 中立 - LEGENDARY
"""
from ..utils import *


# ========== VAC_321 - 伊辛迪奥斯 ==========
class VAC_321:
    """伊辛迪奥斯 - Incindius
    在你的回合结束时,你的爆发升级。战吼:将5张爆发洗入你的牌库。
    At the end of your turn, upgrade your Eruptions. Battlecry: Shuffle 5 of them into your deck.
    """
    mechanics = [GameTag.BATTLECRY, GameTag.TRIGGER_VISUAL]
    
    def play(self):
        # 战吼:洗入5张爆发
        for _ in range(5):
            yield Shuffle(CONTROLLER, "VAC_321t")
    
    def on_turn_end(self):
        """回合结束时升级牌库中的爆发"""
        # 遍历牌库中的所有爆发卡牌并升级
        for card in list(self.controller.deck):
            if card.id == "VAC_321t":
                # 升级爆发：增加伤害
                # eruption_damage 属性已在 VAC_321t 类中正式声明
                card.eruption_damage += 1
    
    events = OWN_TURN_END.on(
        lambda self: self.on_turn_end()
    )


# ========== VAC_446 - 挂机的阿凯 ==========
class VAC_446:
    """挂机的阿凯 - A. F. Kay
    在你的回合结束时,使所有其他未攻击的友方随从获得+2/+2。
    At the end of your turn, give all other friendly minions that didn't attack +2/+2.
    """
    mechanics = [GameTag.TRIGGER_VISUAL]
    
    def on_turn_end(self):
        """回合结束时给未攻击的随从加buff"""
        for minion in self.controller.field:
            if minion != self:
                # 检查随从是否在本回合攻击过
                # 使用 num_attacks 属性判断
                if minion.num_attacks == 0:
                    yield Buff(minion, "VAC_446e")
    
    events = OWN_TURN_END.on(
        lambda self: self.on_turn_end()
    )


class VAC_446e:
    """挂机的阿凯增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# ========== VAC_702 - 经理马林 ==========
class VAC_702:
    """经理马林 - Marin the Manager
    战吼:选择一张神奇宝藏。将其余3张洗入你的牌库。
    Battlecry: Choose a fantastic treasure. Shuffle the other 3 into your deck.
    """
    mechanics = [GameTag.BATTLECRY]
    
    # 四个宝藏的ID
    # 这些是Paradise扩展包的新宝藏Token
    TREASURES = [
        "VAC_702t",  # Zarog's Crown - 发现传说随从并召唤2个
        "VAC_702t2", # Wondrous Wand - 抽3张牌并减3费
        "VAC_702t3", # Golden Kobold - 6/6嘲讽,战吼:手牌变传说且减1费
        "VAC_702t4", # Tolin's Goblet - 抽1张牌并复制满手牌
    ]
    
    def play(self):
        # 让玩家选择一个宝藏
        treasures = [self.controller.card(tid) for tid in self.__class__.TREASURES]
        chosen = yield GenericChoice(CONTROLLER, treasures)
        
        if chosen:
            # 将选中的宝藏加入手牌
            yield Give(CONTROLLER, chosen[0].id)
            
            # 将其余3个宝藏洗入牌库
            for treasure_id in self.__class__.TREASURES:
                if treasure_id != chosen[0].id:
                    yield Shuffle(CONTROLLER, treasure_id)


# ========== VAC_955 - 戈贡佐姆 ==========
class VAC_955:
    """戈贡佐姆 - Gorgonzormu
    战吼:获取一张法力值消耗为(2)的奶酪。奶酪可以召唤三个法力值消耗为(1)的随从,且每回合都会升级。
    Battlecry: Get a 2-Cost Cheese that summons three 1-Cost minions. It upgrades each turn.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 给玩家一张美味奶酪
        yield Give(CONTROLLER, "VAC_955t")


# ========== VAC_959 - 诚信商家格里伏塔 ==========
class VAC_959:
    """诚信商家格里伏塔 - Griftah, Trusted Vendor
    战吼:发现一款神奇的护符,赠予双方玩家。(敌人的护符为伪劣版本!)
    Battlecry: Discover an amazing Amulet to give to both players. (The enemy's is a phony version!)
    """
    mechanics = [GameTag.BATTLECRY, GameTag.DISCOVER]
    
    # 护符列表 (真品和假货成对)
    AMULETS = [
        ("VAC_959t",  "VAC_959t2"),  # Amulet of Mobility - 抽牌
        ("VAC_959t3", "VAC_959t4"),  # Amulet of Critters - 召唤随从
        ("VAC_959t5", "VAC_959t6"),  # Amulet of Energy - 恢复生命
        ("VAC_959t7", "VAC_959t8"),  # Amulet of Passions - 控制随从
        ("VAC_959t9", "VAC_959t10"), # Amulet of Strides - 减费
        ("VAC_959t11", "VAC_959t12"), # Amulet of Tracking - 获取传说
        ("VAC_959t13", "VAC_959t14"), # Amulet of Damage - 造成伤害
    ]
    
    def play(self):
        # 发现一个护符 (只显示真品)
        real_amulets = [pair[0] for pair in self.__class__.AMULETS]
        cards = [self.controller.card(aid) for aid in real_amulets]
        discovered = yield GenericChoice(CONTROLLER, cards)
        
        if discovered:
            chosen_id = discovered[0].id
            # 给玩家真品
            yield Give(CONTROLLER, chosen_id)
            
            # 找到对应的假货给对手
            for real, fake in self.__class__.AMULETS:
                if real == chosen_id:
                    yield Give(OPPONENT, fake)
                    break


# ========== WORK_027 - 梦想策划师杰弗里斯 ==========
class WORK_027:
    """梦想策划师杰弗里斯 - Dreamplanner Zephrys
    战吼:选择一条旅行路线,从中获取两张可能会表现完美的卡牌。
    Battlecry: Choose a Travel Tour to get two potentially perfect cards from it.
    """
    mechanics = [GameTag.BATTLECRY]
    
    # 三个旅行路线的卡池（基于官方数据）
    # 数据来源: HearthstoneTopDecks官方卡池列表
    
    # Extravagant Tour - "Spend Mana" (高费/主动卡牌)
    EXTRAVAGANT_TOUR = [
        # 官方确认的卡牌
        "CS2_042",   # Fire Elemental (6费)
        "EX1_250",   # Earth Elemental (5费)
        "EX1_164",   # Nourish (5费)
        "CS2_011",   # Sprint (7费)
        "EX1_110",   # Cairne Bloodhoof (6费)
        "EX1_411",   # Gorehowl (7费)
        "ICC_210",   # Natalie Seline (8费)
        "EX1_295",   # Ice Block (3费)
        "EX1_144",   # Shadowstep (0费)
        "CS2_222",   # Stormwind Champion (7费)
        "EX1_116",   # Leeroy Jenkins (6费)
        "NEW1_030",  # Black Knight (6费)
        "EX1_012",   # Bloodmage Thalnos (2费传说)
        "CS2_213",   # Reckless Rocketeer (6费)
        "CS2_029",   # Fireball (4费)
        "EX1_279",   # Pyroblast (10费)
    ]
    
    # Hectic Tour - "Damage Enemy Hero" (伤害卡牌)
    HECTIC_TOUR = [
        # 官方确认的卡牌
        "CS2_045",   # Rockbiter Weapon (1费)
        "CS2_046",   # Bloodlust (5费)
        "NEW1_005",  # Doomhammer (5费)
        "NEW1_033",  # King Krush (9费)
        "EX1_279",   # Pyroblast (10费)
        "CS2_029",   # Fireball (4费)
        "CS2_108",   # Mortal Strike (4费)
        "CS2_039",   # Windfury (2费)
        "CS2_011",   # Savage Roar (3费)
        "EX1_241",   # Lava Burst (3费)
        "EX1_306",   # Soulfire (1费)
        "EX1_384",   # Avenging Wrath (6费)
        "CS2_234",   # Mind Blast (2费)
        "EX1_238",   # Lightning Bolt (1费)
        "CS2_233",   # Eviscerate (2费)
        "CS2_024",   # Frostbolt (2费)
        "EX1_116",   # Leeroy Jenkins (6费)
        "EX1_298",   # Ragnaros the Firelord (8费)
        "NEW1_010",  # Al'Akir the Windlord (8费)
    ]
    
    # Modest Tour - "Impact Enemy's Battlefield" (场面控制)
    MODEST_TOUR = [
        # 官方确认的卡牌
        "EX1_066",   # Acidic Swamp Ooze (2费)
        "EX1_622",   # Shadow Word: Death (3费)
        "CS2_141",   # Ironforge Rifleman (3费)
        "CS2_189",   # Elven Archer (1费)
        "CS2_142",   # Kobold Geomancer (2费)
        "EX1_015",   # Novice Engineer (2费)
        "CS2_032",   # Flamestrike (7费)
        "EX1_277",   # Arcane Missiles (1费)
        "CS2_025",   # Arcane Explosion (2费)
        "CS2_093",   # Consecration (4费)
        "EX1_371",   # Hand of A'dal (2费)
        "CS2_114",   # Cleave (2费)
        "EX1_246",   # Hex (3费)
        "CS2_104",   # Rampage (2费)
    ]
    
    def play(self):
        # 让玩家选择旅行路线
        # 使用 GenericChoice 选择路线
        tour_options = [
            self.controller.card("WORK_027t1"),  # Extravagant Tour
            self.controller.card("WORK_027t2"), # Hectic Tour
            self.controller.card("WORK_027t3"), # Modest Tour
        ]
        
        chosen_tour = yield GenericChoice(CONTROLLER, tour_options)
        
        if chosen_tour:
            tour_id = chosen_tour[0].id
            
            # 根据选择的路线获取卡池
            if tour_id == "WORK_027t1":
                card_pool = self.__class__.EXTRAVAGANT_TOUR
            elif tour_id == "WORK_027t2":
                card_pool = self.__class__.HECTIC_TOUR
            else:
                card_pool = self.__class__.MODEST_TOUR
            
            # 从卡池中随机获取2张卡牌
            selected_cards = self.game.random.sample(card_pool, min(2, len(card_pool)))
            for card_id in selected_cards:
                yield Give(CONTROLLER, card_id)


# ========== WORK_043 - 旅行管理员杜加尔 ==========
class WORK_043:
    """旅行管理员杜加尔 - Travelmaster Dungar
    战吼:从你的牌库中召唤三个来自不同扩展包的随从。
    Battlecry: Summon three minions from your deck that are from different expansions.
    """
    mechanics = [GameTag.BATTLECRY]
    
    def play(self):
        # 获取牌库中的所有随从
        minions_in_deck = [
            card for card in self.controller.deck 
            if card.type == CardType.MINION
        ]
        
        if not minions_in_deck:
            return
        
        # 按扩展包分组
        expansions_dict = {}
        for minion in minions_in_deck:
            card_set = minion.data.card_set
            if card_set not in expansions_dict:
                expansions_dict[card_set] = []
            expansions_dict[card_set].append(minion)
        
        # 从不同扩展包中各选一个随从
        summoned_count = 0
        used_expansions = set()
        
        # 随机选择扩展包顺序
        expansion_keys = list(expansions_dict.keys())
        self.game.random.shuffle(expansion_keys)
        
        for expansion in expansion_keys:
            if summoned_count >= 3:
                break
            
            if expansion not in used_expansions:
                # 从该扩展包随机选一个随从
                minion = self.game.random.choice(expansions_dict[expansion])
                # 召唤该随从
                yield Summon(CONTROLLER, minion)
                used_expansions.add(expansion)
                summoned_count += 1


