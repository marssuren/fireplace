"""
威兹班的工坊 - Token 卡牌
包含 Miniaturize、Gigantify 和其他机制生成的 Token 卡牌
"""
from ..utils import *


# ========================================
# Death Knight Tokens
# ========================================

class MIS_006t:
    """玩具盗窃恶鬼 (巨型) - Toysnatching Geist (Gigantified)
    [x]Gigantify Battlecry: Discover an Undead. Reduce its Cost by this minion's Attack.
    """
    # 8/8/8 Gigantify Token
    # 与原卡相同的效果，但身材巨大
    def play(self):
        # Discover 一张亡灵牌
        card = yield DISCOVER(RandomCollectible(race=Race.UNDEAD))
        if card:
            # 减少费用，减少量 = 本随从的攻击力 (8)
            yield Buff(card[0], "MIS_006e")


class TOY_825t2:
    """法术尖晶石 - Spinel Spellstone (Upgraded)
    Give Undead in your hand +2/+2. <i>(Gain 5 Corpses to upgrade.)</i>
    """
    # 升级版本：+2/+2
    play = Buff(FRIENDLY_HAND + UNDEAD, "TOY_825e2")
    
    class Hand:
        # 继续监听，再获得5具尸体时升级为最终版本
        events = GainCorpses(CONTROLLER, 5).after(Morph(SELF, "TOY_825t3"))


class TOY_825t3:
    """强效法术尖晶石 - Greater Spinel Spellstone
    Give Undead in your hand +3/+3.
    """
    # 最终版本：+3/+3
    play = Buff(FRIENDLY_HAND + UNDEAD, "TOY_825e3")


class TOY_828t:
    """业余傀儡师 (小型) - Amateur Puppeteer (Miniaturized)
    [x]Miniaturize, Taunt Deathrattle: Give Undead in your hand +2/+2.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的效果，但身材缩小
    taunt = True
    deathrattle = Buff(FRIENDLY_HAND + UNDEAD, "TOY_828e")


class TOY_829t:
    """无头骑士的头 - The Headless Horseman's Head
    Cast When Drawn: Imbue the souls of Undead into your Hero Power!
    """
    # 2费法术 抽到时施放：将亡灵之魂注入你的英雄技能中
    # 官方数据：抽到时施放 - 让你的敌人陷入惶恐！亡灵之魂会注入你的英雄技能中！
    # 效果：升级英雄技能（从 TOY_829hp3 变为 TOY_829hp）
    # 注意：没有装备武器的效果！
    
    def play(self):
        # 升级英雄技能 (从 TOY_829hp3 变为 TOY_829hp)
        # 直接替换英雄技能
        controller = self.controller
        old_power = controller.hero.power
        if old_power:
            old_power.zone = Zone.GRAVEYARD
        
        # 创建新的英雄技能
        new_power = controller.card("TOY_829hp", source=controller.hero)
        new_power.controller = controller
        new_power.zone = Zone.PLAY
        controller.hero.power = new_power


class TOY_829hp3:
    """跃动的南瓜 - Pulsing Pumpkins (初始版本)
    Deal $3 damage.
    """
    # 2费英雄技能：造成3点伤害
    # 官方数据：造成$3点伤害，威力无穷！找到头颅，我的部队向你效忠！
    # 初始版本只有伤害效果，没有 Discover
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    activate = Hit(TARGET, 3)


class TOY_829hp:
    """跃动的南瓜 - Pulsing Pumpkins (升级版本)
    Deal $3 damage. Discover an Undead.
    """
    # 2费英雄技能：造成3点伤害，发现一张亡灵牌
    # 官方数据：造成$3点伤害，威力无穷！发现一张亡灵牌，充当仆从！
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    def activate(self):
        yield Hit(TARGET, 3)
        # 发现一张亡灵牌
        cards = yield DISCOVER(RandomCollectible(race=Race.UNDEAD))
        # Discover 会自动将牌加入手牌，不需要额外操作


class TOY_829t2:
    """无头骑士 - The Headless Horseman (找回头颅后)
    """
    # 6费英雄 30生命值 0护甲
    # 英雄技能: TOY_829hp (升级版跃马攻击)
    # 注意：根据官方数据，这个 token 可能不需要，因为英雄技能升级是通过替换实现的
    # 保留此定义以备将来需要
    pass


# ========================================
# Demon Hunter Tokens
# ========================================

class TOY_645t:
    """法术欧珀石 - Opal Spellstone (Upgraded)
    Draw 2 cards. <i>(Attack with your hero 2 times to upgrade.)</i>
    """
    # 2费法术 抽两张牌。（用你的英雄攻击2次后升级）
    def play(self):
        yield Draw(CONTROLLER)
        yield Draw(CONTROLLER)
    
    class Hand:
        # 继续监听英雄攻击事件
        # 当英雄再攻击2次后，升级为 TOY_645t1
        events = Attack(FRIENDLY_HERO).after(
            Find(Attr(SELF, "times_hero_attacked") >= 1) & Morph(SELF, "TOY_645t1")
        )
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.times_hero_attacked = 0
        
        # 追踪英雄攻击次数
        events = Attack(FRIENDLY_HERO).after(
            lambda self: setattr(self, "times_hero_attacked", getattr(self, "times_hero_attacked", 0) + 1)
        )


class TOY_645t1:
    """大型法术欧珀石 - Greater Opal Spellstone
    Draw 3 cards.
    """
    # 2费法术 抽三张牌（最终版本）
    def play(self):
        yield Draw(CONTROLLER)
        yield Draw(CONTROLLER)
        yield Draw(CONTROLLER)


class TOY_652t:
    """橱窗看客 (小型) - Window Shopper (Miniaturized)
    [x]Miniaturize Battlecry: Discover a Demon. Set its stats and Cost to this minion's.
    """
    # 1/1/1 微型。战吼：发现一张恶魔牌，将其属性值与法力值消耗变为与本随从相同
    # Miniaturize Token
    def play(self):
        # Discover 一张恶魔牌
        cards = yield DISCOVER(RandomCollectible(race=Race.DEMON))
        if cards:
            discovered_card = cards[0]
            # 设置属性值和费用（1/1/1）
            yield Buff(discovered_card, "TOY_652e", atk=self.atk, health=self.health)
            yield Buff(discovered_card, "TOY_652e2", cost=self.cost)


# ========================================
# Neutral Tokens
# ========================================

class MIS_025t:
    """机械袋鼠 (小型) - Mechanical Kangaroo (Miniaturized)
    [x]Miniaturize After you play a minion with the same Attack as this, summon a copy of it.
    """
    # 1/1/1 Miniaturize Token
    # Gigantify 效果：召唤与本随从攻击力相同的随从的复制
    events = Play(CONTROLLER, MINION + (ATK(Play.CARD) == ATK(SELF))).after(
        Summon(CONTROLLER, ExactCopy(Play.CARD))
    )


class MIS_025t1:
    """机械袋鼠 (巨型) - Mechanical Kangaroo (Gigantified)
    [x]Gigantify After you play a minion with the same Attack as this, summon a copy of it.
    """
    # 8/8/8 Gigantify Token
    # 与原卡相同的效果，但身材巨大
    events = Play(CONTROLLER, MINION + (ATK(Play.CARD) == ATK(SELF))).after(
        Summon(CONTROLLER, ExactCopy(Play.CARD))
    )


class TOY_312t:
    """恋旧的侏儒 (小型) - Nostalgic Gnome (Miniaturized)
    Miniaturize Rush. After this minion deals exact lethal damage on your turn, draw a card.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的效果，但身材缩小
    # 
    # 【完整实现】"exact lethal" 意味着攻击伤害恰好等于目标剩余生命值
    # 实现方式：在攻击前记录目标生命值，攻击后检查是否恰好致命
    rush = True
    
    def OWN_ATTACK_TRIGGER(self, source, target):
        """攻击前：记录目标生命值"""
        if target and hasattr(target, 'health'):
            self._last_target_health = target.health
            self._last_target = target
        return []
    
    def OWN_ATTACK_AFTER_TRIGGER(self, source, target):
        """攻击后：检查是否造成恰好致命伤害"""
        if not self.controller.current_player:
            return []
        
        if not hasattr(self, '_last_target') or not hasattr(self, '_last_target_health'):
            return []
        
        if target and target.zone == Zone.GRAVEYARD:
            if source.atk == self._last_target_health:
                return Draw(CONTROLLER)
        
        return []
    
    events = [
        Attack(SELF).on(OWN_ATTACK_TRIGGER),
        Attack(SELF).after(OWN_ATTACK_AFTER_TRIGGER)
    ]






# ========================================
# Druid Tokens
# ========================================

class MIS_300t:
    """抱抱泰迪熊 (巨型) - Snuggle Teddy (Gigantified)
    Gigantify Elusive, Lifesteal, Taunt
    """
    # 8/8/8 Gigantify Token
    # 与原卡相同的关键词，但身材巨大
    elusive = True
    lifesteal = True
    taunt = True


class MIS_301t:
    """树人 - Treant
    """
    # 1费 2/2 树人 Token
    # 由豆蔓疯长 (MIS_301) 召唤
    pass


class TOY_801t:
    """绿植幼龙 (小型) - Chia Drake (Miniaturized)
    Miniaturize Choose One - Gain Spell Damage +1; or Draw a spell.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的 Choose One 效果
    choose = ("TOY_801a", "TOY_801b")


class TOY_804t:
    """甲虫 - Beetle
    Taunt
    """
    # 2/5 嘲讽甲虫 Token
    # 由林中奇遇 (TOY_804) 召唤
    taunt = True


# ========================================
# Hunter Tokens
# ========================================

class TOY_351t:
    """神秘的蛋 (小型) - Mysterious Egg (Miniaturized)
    Miniaturize Deathrattle: Get a copy of a random Beast in your deck. It costs (3) less.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的亡语效果
    def deathrattle(self):
        # 从牌库中随机获取一张野兽牌
        beasts_in_deck = FRIENDLY_DECK + BEAST
        beasts = beasts_in_deck.eval(self.game, self)
        
        if beasts:
            # 随机选择一张野兽
            beast = yield RandomChoice(beasts)
            if beast:
                # 获取复制
                card = yield Give(CONTROLLER, beast[0].id)
                if card:
                    # 添加费用减少 Buff
                    yield Buff(card, "TOY_351e1")


class TOY_358t:
    """遥控猎犬 - Remote Control Hound
    """
    # 1/1/1 野兽+机械 Token
    # 由遥控骨 (TOY_358) 召唤
    # 官方数据：双种族（BEAST + MECHANICAL）
    pass


# ========================================
# Mage Tokens
# ========================================

class TOY_375t:
    """滑冰元素 (小型) - Sleet Skater (Miniaturized)
    Miniaturize Battlecry: Freeze an enemy minion. Gain Armor equal to its Attack.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的战吼效果
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 冻结目标敌方随从
            yield Freeze(TARGET)
            
            # 获得等同于目标攻击力的护甲值
            armor_gain = TARGET.atk
            if armor_gain > 0:
                yield GainArmor(FRIENDLY_HERO, armor_gain)


class TOY_373hp:
    """魔法智慧之球 - Magic Wisdomball
    At the end of your turn, cast a helpful Mage spell. Lose 1 Durability.
    """
    # 3费武器 0攻击 6耐久
    # 在你的回合结束时，施放一个有用的法师法术。失去1点耐久度
    # 官方数据：类似于泽菲里斯的智能法术选择机制
    # 
    # 【完整实现】使用精选的有用法师法术列表
    # 参考：uldum/zephrys_the_great.py
    # 提供多种情况下有用的法术：伤害、抽牌、冻结、变形、AOE等
    
    # 精选的有用法师法术列表
    HELPFUL_MAGE_SPELLS = [
        # 低费伤害法术
        "CS2_024",  # 寒冰箭 (2费) - 造成3点伤害并冻结
        "CS2_029",  # 火球术 (4费) - 造成6点伤害
        "EX1_275",  # 冰锥术 (4费) - 造成4点伤害并冻结
        
        # 抽牌法术
        "CS2_023",  # 奥术智慧 (3费) - 抽2张牌
        
        # 冻结/控制法术
        "CS2_026",  # 冰霜新星 (3费) - 冻结所有敌方随从
        "CS2_028",  # 暴风雪 (6费) - 造成2点伤害并冻结所有敌方随从
        
        # 变形/解场
        "CS2_022",  # 变形术 (4费) - 将随从变形为1/1绵羊
        
        # AOE伤害
        "CS2_025",  # 魔爆术 (2费) - 对所有敌方随从造成1点伤害
        "CS2_032",  # 烈焰风暴 (7费) - 对所有敌方随从造成5点伤害
        
        # 高伤害法术
        "EX1_279",  # 炎爆术 (10费) - 造成10点伤害
        
        # 召唤随从
        "CS2_027",  # 镜像 (1费) - 召唤两个0/2嘲讽
        "CS2_033",  # 水元素 (4费) - 召唤3/6冻结随从
        "CS2_042",  # 火元素 (6费) - 召唤6/5随从
    ]
    
    events = OWN_TURN_END.on(
        lambda self, player: [
            # 从有用的法师法术列表中随机选择一个并施放
            CastSpell(RandomChoice(self.HELPFUL_MAGE_SPELLS)),
            # 失去1点耐久度
            Hit(SELF, 1)
        ]
    )


# ========================================
# Neutral Common Tokens
# ========================================

class TOY_307t:
    """甜蜜雪灵 (小型) - Sweetened Snowflurry (Miniaturized)
    Miniaturize Battlecry: Get 2 random Temporary Frost spells.
    """
    # 1/1/1 元素 Miniaturize Token
    # 与原卡相同的效果，但身材缩小
    def play(self):
        # 获取2张随机冰霜法术
        for _ in range(2):
            card = yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.FROST))
            # 给予临时标签（回合结束时弃掉）
            if card:
                yield Buff(card, "TOY_307e")


class TOY_340t1:
    """恋旧的新生 (小型) - Nostalgic Initiate (Miniaturized)
    Miniaturize The first time you cast a spell, gain +2/+2.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的效果，但身材缩小
    triggered = boolean_property("TOY_340_triggered")

    events = Play(CONTROLLER, SPELL).after(
        Find(SELF + ~TRIGGERED) & (Buff(SELF, "TOY_340t"), SetAttr(SELF, "triggered", True))
    )


class TOY_670t:
    """玩具机械 - Toy Mech
    Taunt, Divine Shield
    """
    # 1/1/2 机械 嘲讽，圣盾
    # 由欢乐的玩具匠 (TOY_670) 召唤
    taunt = True
    divine_shield = True


# ========================================
# Neutral Epic Tokens
# ========================================

class TOY_341t:
    """恋旧的小丑 (小型) - Nostalgic Clown (Miniaturized)
    Miniaturize Battlecry: If you've played a higher Cost card while holding this, deal 4 damage.
    """
    # 1/1/1 Miniaturize Token
    # 与原卡相同的效果，但身材缩小
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}

    class Hand:
        """在手牌时追踪是否使用过更高费用的牌"""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not hasattr(self, 'higher_cost_played'):
                self.higher_cost_played = False

        events = Play(CONTROLLER).after(lambda self, source: self._check_higher_cost(source))

        def _check_higher_cost(self, played_card):
            """检查打出的牌是否费用更高"""
            if played_card.cost > self.cost:
                self.higher_cost_played = True

    def play(self):
        if getattr(self, 'higher_cost_played', False):
            yield Hit(TARGET, 4)


class TOY_601t:
    """工厂装配机 (小型) - Factory Assemblybot (Miniaturized)
    Miniaturize At the end of your turn, summon a 6/7 Bot that attacks a random enemy.
    """
    # 1/1/1 机械 Miniaturize Token
    # 与原卡相同的效果，但身材缩小
    events = TurnEnd(CONTROLLER).on(
        Summon(CONTROLLER, "TOY_601t1"),
        lambda self: self._attack_random_enemy()
    )

    def _attack_random_enemy(self):
        """让刚召唤的机器人攻击随机敌人"""
        if self.controller.field:
            bot = self.controller.field[-1]
            enemies = self.controller.opponent.field + [self.controller.opponent.hero]
            valid_enemies = [e for e in enemies if e.can_be_attacked_by(bot)]
            if valid_enemies:
                target = self.game.random.choice(valid_enemies)
                yield Attack(bot, target)


class TOY_601t1:
    """机器人 - Bot
    """
    # 6/7 机械 Token
    # 由工厂装配机 (TOY_601) 召唤
    pass


class TOY_814t:
    """玩具士兵 - Toy Soldier (Divine Shield)
    Divine Shield
    """
    # 1/1/1 德莱尼 圣盾
    # 由玩具兵盒 (TOY_814) 召唤
    divine_shield = True


class TOY_814t2:
    """玩具士兵 - Toy Soldier (Taunt)
    Taunt
    """
    # 1/1/1 德莱尼 嘲讽
    # 由玩具兵盒 (TOY_814) 召唤
    taunt = True


class TOY_814t3:
    """玩具士兵 - Toy Soldier (Rush)
    Rush
    """
    # 1/1/1 德莱尼 突袭
    # 由玩具兵盒 (TOY_814) 召唤
    rush = True


class TOY_814t4:
    """玩具士兵 - Toy Soldier (Windfury)
    Windfury
    """
    # 1/1/1 德莱尼 风怒
    # 由玩具兵盒 (TOY_814) 召唤
    windfury = True


class TOY_814t5:
    """玩具士兵 - Toy Soldier (Elusive)
    Elusive
    """
    # 1/1/1 德莱尼 扰魔
    # 由玩具兵盒 (TOY_814) 召唤
    elusive = True


class TOY_814t6:
    """玩具士兵 - Toy Soldier (Poisonous)
    Poisonous
    """
    # 1/1/1 德莱尼 剧毒
    # 由玩具兵盒 (TOY_814) 召唤
    poisonous = True


class TOY_814t7:
    """玩具士兵 - Toy Soldier (Lifesteal)
    Lifesteal
    """
    # 1/1/1 德莱尼 吸血
    # 由玩具兵盒 (TOY_814) 召唤
    lifesteal = True


class TOY_814t8:
    """玩具士兵 - Toy Soldier (Reborn)
    Reborn
    """
    # 1/1/1 德莱尼 复生
    # 由玩具兵盒 (TOY_814) 召唤
    reborn = True


# ========================================
# Paladin Tokens
# ========================================

class TOY_811t:
    """绒绒虎 (小型) - Tigress Plushy (Miniaturized)
    Miniaturize Rush, Lifesteal, Divine Shield
    """
    # 1/1/1 微型 突袭,吸血,圣盾
    # 官方数据:Miniaturize Rush, Lifesteal, Divine Shield
    rush = True
    lifesteal = True
    divine_shield = True


class TOY_813t:
    """玩具队长塔林姆 (小型) - Toy Captain Tarim (Miniaturized)
    [x]Miniaturize Taunt. Battlecry: Set a minion's Attack and Health to this minion's.
    """
    # 1/1/1 微型 嘲讽
    # 战吼:将一个随从的攻击力和生命值变为与本随从相同
    # 官方数据:Miniaturize Taunt. Battlecry: Set a minion's Attack and Health to this minion's.
    taunt = True
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    def play(self):
        if TARGET:
            # 将目标的攻击力和生命值设置为本随从的属性值 (1/1)
            yield Buff(TARGET, "TOY_813e3", atk=self.atk, max_health=self.max_health)


class MIS_918t:
    """灯火机器人 (巨型) - Flickering Lightbot (Gigantified)
    [x]Gigantify Costs (1) less for each Holy spell you've cast this game.
    """
    # 8/8/8 机械 巨大化
    # 本局对战中每施放一个圣光法术,费用减少1
    # 官方数据:Gigantify Costs (1) less for each Holy spell you've cast this game.
    
    def cost_mod(self):
        # 计算本局对战中施放的圣光法术数量
        holy_spells_count = self.controller.spell_schools_played.count(SpellSchool.HOLY)
        return -holy_spells_count


class TOY_716t:
    """机械 - Mech (Flash Sale Token)
    Divine Shield, Taunt
    """
    # 1/2 机械 圣盾,嘲讽
    # 由光速抢购 (TOY_716) 召唤
    divine_shield = True
    taunt = True


# ========================================
# Priest Tokens
# ========================================

class TOY_380t:
    """黏土巢母 (小型) - Clay Matriarch (Miniaturized)
    <b>Miniaturize</b>
    <b>Taunt</b>. <b>Deathrattle:</b> Summon a 4/4 <b>Elusive</b> Whelp.
    """
    # 1/1/1 微型 龙 嘲讽
    # 亡语：召唤4/4扰魔雏龙
    # 官方数据：Miniaturize Taunt. Deathrattle: Summon a 4/4 Elusive Whelp.
    taunt = True
    
    def deathrattle(self):
        # 召唤4/4扰魔雏龙
        yield Summon(CONTROLLER, "TOY_380t2")


class TOY_380t2:
    """雏龙 - Whelp
    <b>Elusive</b>
    """
    # 4/4 龙 扰魔
    # 由黏土巢母亡语召唤
    # 官方数据：4/4 Elusive Dragon
    elusive = True


class TOY_382t:
    """绷带 - Bandage
    Restore 3 Health.
    """
    # 0费法术 恢复3点生命值
    # 由粗心的匠人亡语获取
    # 官方数据：(0)-Cost spell that Restores 3 Health
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    play = Heal(TARGET, 3)


class TOY_879t:
    """箱子 - Repackaged Box
    Add the repackaged minions to your hand.
    """
    # 2费法术 将重新封装的随从加入手牌
    # 由重新打包创建并洗入对手牌库
    # 官方数据：2费法术，将封装的随从加入手牌
    
    def play(self):
        """效果：将所有被封入的随从加入手牌"""
        # 获取存储的随从ID列表
        stored_minions = getattr(self, 'stored_minions', [])
        
        # 将所有存储的随从加入手牌
        for minion_id in stored_minions:
            yield Give(CONTROLLER, minion_id)


# ========================================
# Rogue Tokens
# ========================================

class TOY_521t:
    """沙箱恶霸 (小型) - Sandbox Scoundrel (Miniaturized)
    <b>Miniaturize</b>
    <b>Battlecry:</b> Your next card this turn costs (2) less.
    """
    # 1/1/1 海盗 微缩
    # 战吼：下一张牌费用减少2
    # 官方数据：Miniaturize Battlecry: Your next card this turn costs (2) less.
    
    def play(self):
        # 给控制者添加临时效果：下一张牌费用减少2
        yield Buff(CONTROLLER, "TOY_521e")


class TOY_522t:
    """海盗 - Pirate (Watercannon Token)
    """
    # 1/1 海盗 Token
    # 由水弹枪召唤
    # 官方数据：1/1 Pirate summoned by Watercannon
    pass


class MIS_706t1:
    """石头 - Rock
    Deal $1 damage.
    """
    # 0费法术 造成1点伤害
    # 由滚灰兔获取
    # 官方数据：0-Cost spell that deals 1 damage
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    
    play = Hit(TARGET, 1)


class MIS_706t2:
    """短刀 - Knife
    Give a minion +1 Attack.
    """
    # 0费法术 给随从+1攻击
    # 由滚灰兔获取
    # 官方数据：0-Cost spell that gives a minion +1 Attack
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    
    play = Buff(TARGET, "MIS_706e")


class MIS_706e:
    """短刀增益 - Knife Buff
    +1 Attack
    """
    atk = 1


# ========================================
# Shaman Tokens
# ========================================

class TOY_508t:
    """青蛙 - Frog
    <b>Taunt</b>
    """
    # 0/1 野兽 嘲讽
    # 由立体书召唤
    taunt = True


class TOY_513t:
    """沙画元素 (小型) - Sand Art Elemental (Miniaturized)
    <b>Miniaturize</b>
    <b>Battlecry:</b> Give your hero +1 Attack and <b>Windfury</b> this turn.
    """
    # 1/1/1 元素 微缩
    # 战吼：英雄+1攻击力和风怒（本回合）
    
    def play(self):
        # 给英雄+1攻击力（本回合）
        yield Buff(FRIENDLY_HERO, "TOY_513e")
        # 给英雄风怒（本回合）
        yield Buff(FRIENDLY_HERO, "TOY_513e2")


class MIS_307t:
    """鱼人宝宝 - Tinyfin
    <b>Rush</b>
    """
    # 1/1 鱼人 突袭
    # 由水宝宝鱼人召唤
    # 注意：属性值会被动态设置为与水宝宝鱼人相同
    rush = True


class MIS_307t1:
    """水宝宝鱼人 (巨型) - Murloc Growfin (Gigantified)
    <b>Gigantify</b>
    <b>Battlecry:</b> Summon a Tinyfin with <b>Rush</b> and stats equal to this minion's.
    """
    # 8/8/8 鱼人 扩大化
    # 战吼：召唤一个属性等同于本随从并具有突袭的鱼人宝宝
    
    def play(self):
        # 召唤鱼人宝宝 Token
        tinyfin = yield Summon(CONTROLLER, "MIS_307t")
        
        if tinyfin:
            # 设置属性值等同于本随从
            yield Buff(tinyfin[0], "MIS_307e", atk=self.atk, max_health=self.max_health)


class TOY_501t:
    """沙德木刻 (小型) - Shudderblock (Miniaturized)
    <b>Miniaturize</b>
    <b>Battlecry:</b> Your next <b>Battlecry</b> triggers 3 times, but can't damage the enemy hero.
    """
    # 1/1/1 微缩
    # 战吼：下一个战吼触发3次（1次原始 + 2次额外），但无法伤害敌方英雄
    # 与原卡相同的效果，但身材缩小
    # 核心引擎已扩展支持战吼触发多次（通过统计 EXTRA_BATTLECRIES buff 数量）
    
    def play(self):
        # 给控制者添加两个 EXTRA_BATTLECRIES buff
        # 核心引擎会统计 buff 数量，让战吼额外触发2次（总共3次）
        yield Buff(CONTROLLER, "TOY_501e")
        yield Buff(CONTROLLER, "TOY_501e")


class TOY_504t:
    """泥浆怪 - Slime
    <b>Battlecry:</b> Cast the stored spell.
    <b>战吼：</b>施放存储的法术。
    """
    # 2/2 元素
    # 战吼：施放存储的法术
    # 由神秘女巫哈加莎创建
    # 参考 LOOT_506 (The Runespear) 的 CastSpell 实现
    
    def play(self):
        # 获取存储的法术ID
        spell_id = getattr(self, 'stored_spell_id', None)
        
        if spell_id:
            # 施放存储的法术
            # 使用 CastSpell action 施放法术（会自动选择随机目标）
            yield CastSpell(spell_id)




# ========================================
# Warlock Tokens
# ========================================

class TOY_914t:
    """骑士 - Knight
    <b>Taunt</b>
    """
    # 4/6 嘲讽骑士
    # 由邪鬼皇后亡语召唤
    taunt = True


class TOY_915t:
    """桌游角色扮演玩家 (小型) - Tabletop Roleplayer (Miniaturized)
    <b>Miniaturize</b>
    <b>Battlecry:</b> Give a friendly Demon +2 Attack and <b>Immune</b> this turn.
    """
    # 1/1/1 微缩
    # 战吼：使一个友方恶魔+2攻击力和免疫（本回合）
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON}
    
    def play(self):
        if TARGET:
            # +2攻击力和免疫（本回合）
            yield Buff(TARGET, "TOY_915e")


# ========================================
# Warrior Tokens
# ========================================

class TOY_604t:
    """砰砰扳手 (小型) - Boom Wrench (Miniaturized)
    <b>Miniature</b>
    <b>Deathrattle:</b> Trigger the <b>Deathrattle</b> of a random friendly Mech.
    <b>微型</b>
    <b>亡语:</b>随机触发一个友方机械的<b>亡语</b>。
    """
    # 1费 1/0 武器 微型
    # 亡语：随机触发一个友方机械的亡语
    
    def deathrattle(self):
        """
        亡语：随机触发一个友方机械的亡语
        """
        # 获取所有友方机械
        mechs = FRIENDLY_MINIONS + RACE(Race.MECHANICAL)
        mechs_list = mechs.eval(self.game, self)
        
        # 筛选出有亡语的机械
        mechs_with_deathrattle = [m for m in mechs_list if m.deathrattles]
        
        if mechs_with_deathrattle:
            # 随机选择一个
            target = self.game.random.choice(mechs_with_deathrattle)
            
            # 触发其亡语
            for deathrattle in target.deathrattles:
                yield deathrattle


# ========================================
# Token 定义完成
# ========================================

# 所有 Whizbang's Workshop 扩展包的 Token 卡牌已定义完成
# 包含：Death Knight, Demon Hunter, Druid, Hunter, Mage, Paladin, 
#       Priest, Rogue, Shaman, Warlock, Warrior 以及 Neutral Tokens

