"""
深暗领域 - DRUID
"""
from ..utils import *


# COMMON

class GDB_103:
    """沙塔尔力场 - Sha'tari Cloakfield
    Elusive. Your first spell each turn costs (1) less. Starship Piece

    2费 1/4 德鲁伊随从 - 星舰组件
    <b>扰魔</b>。你每个回合使用的第一张法术牌的法力值消耗减少（1）点。
    <b>星舰组件</b>
    """
    tags = {
        GameTag.ELUSIVE: True,
    }
    # 你每个回合使用的第一张法术牌的法力值消耗减少（1）点
    # 使用 SPELLS_COST_LESS_FIRST_PER_TURN 机制
    update = Refresh(CONTROLLER, {GameTag.COST: -1}, FRIENDLY_HAND + SPELL).on(
        Play(CONTROLLER, SPELL)
    )


class GDB_852:
    """阿肯尼特的启示 - Arkonite Revelation
    Draw a card. If it's a spell, it costs (1) less.
    
    1费 德鲁伊法术 - 奥术
    抽一张牌。如果是法术牌，其法力值消耗减少（1）点。
    """
    def play(self):
        # 抽一张牌
        cards = yield Draw(CONTROLLER)
        # 如果抽到的是法术牌，减少1费
        if cards:
            for card in cards:
                if card and card.type == CardType.SPELL:
                    yield Buff(card, "GDB_852e")


class GDB_852e:
    """法力值消耗减少（1）点"""
    tags = {
        GameTag.COST: -1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_883:
    """求救信号 - Distress Signal
    Summon two random 2-Cost minions. Refresh 2 Mana Crystals.
    
    4费 德鲁伊法术 - 奥术
    召唤两个随机的法力值消耗为（2）点的随从。刷新2点法力水晶。
    """
    def play(self):
        # 召唤两个随机的2费随从
        yield Summon(CONTROLLER, RandomMinion(cost=2)) * 2
        # 刷新2点法力水晶
        yield FillMana(CONTROLLER, 2)


class SC_755:
    """建造水晶塔 - Construct Pylons
    Your next Protoss card this turn costs (2) less.
    
    0费 德鲁伊法术
    在本回合中，你的下一张神族牌的法力值消耗减少（2）点。
    """
    def play(self):
        # 给控制者添加一个buff，使下一张神族牌减2费
        yield Buff(CONTROLLER, "SC_755e")


class SC_755e:
    """神族牌减费buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    # 使手牌中的神族牌减2费（仅限本回合的下一张）
    update = Refresh(CONTROLLER, {GameTag.COST: -2}, FRIENDLY_HAND + PROTOSS)
    # 打出一张神族牌后移除此buff
    events = Play(CONTROLLER, PROTOSS).on(Destroy(SELF))


class SC_756:
    """航母 - Carrier
    At the end of your turn, summon four 4/1 Interceptors that attack random enemies.
    
    12费 2/14 德鲁伊随从 - 机械
    在你的回合结束时，召唤四个4/1的拦截机并使其攻击随机敌人。
    """
    # 在回合结束时召唤四个拦截机
    events = OwnTurnEnd(CONTROLLER).on(
        Summon(CONTROLLER, "SC_756t") * 4
    )


# RARE

class GDB_108:
    """星光反应堆 - Starlight Reactor
    After you cast an Arcane spell, recast it (targets chosen randomly). Starship Piece

    3费 3/3 德鲁伊随从 - 星舰组件
    在你施放一个奥术法术后，再次施放该法术（目标随机而定）。
    <b>星舰组件</b>
    """
    # 在你施放一个奥术法术后，再次施放该法术（目标随机而定）
    events = Play(CONTROLLER, SPELL + ARCANE).after(
        CastSpell(CONTROLLER, Copy(Play.CARD))
    )


class GDB_851:
    """星域相变射线 - Astral Phaser
    Choose One - Deal $2 damage to two random enemy minions; or Make one Dormant for 2 turns.
    
    2费 德鲁伊法术 - 奥术
    <b>抉择：</b>对两个随机敌方随从造成2点伤害；或使一个敌方随从<b>休眠</b>2回合。
    """
    tags = {
        GameTag.CHOOSE_ONE: True,
    }
    choose = ("GDB_851a", "GDB_851b")
    
    def play(self):
        if self.choice == "GDB_851a":
            # 对两个随机敌方随从造成2点伤害
            yield Hit(RANDOM(ENEMY_MINIONS), 2) * 2
        elif self.choice == "GDB_851b":
            # 使一个敌方随从休眠2回合
            # 参考nathria/druid.py MAW_026的实现
            yield SetTag(self.target, {GameTag.DORMANT: 2})


class GDB_851a:
    """造成伤害 - Deal Damage"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}


class GDB_851b:
    """休眠 - Make Dormant"""
    tags = {GameTag.CARDTYPE: CardType.SPELL}
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_ENEMY_TARGET: 0}


class GDB_855:
    """吞星兽 - Star Grazer
    Elusive, Taunt. Spellburst: Give your hero +8 Attack this turn and gain 8 Armor.
    
    8费 8/8 德鲁伊随从 - 野兽
    <b>扰魔</b>，<b>嘲讽</b>
    <b>法术迸发：</b>使你的英雄在本回合中获得+8攻击力，并获得8点护甲值。
    """
    tags = {
        GameTag.ELUSIVE: True,
        GameTag.TAUNT: True,
        GameTag.SPELLBURST: True,
    }
    
    # Spellburst效果：给英雄+8攻击力（本回合）并获得8点护甲
    events = [
        OWN_SPELL_PLAY.on(
            Buff(FRIENDLY_HERO, "GDB_855e"),
            GainArmor(FRIENDLY_HERO, 8),
            SetTag(SELF, {GameTag.SPELLBURST: False})
        )
    ]


class GDB_855e:
    """英雄+8攻击力（本回合）"""
    tags = {
        GameTag.ATK: 8,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }
    # 回合结束时移除
    events = OwnTurnEnd(CONTROLLER).on(Destroy(SELF))


class SC_763:
    """不朽者 - Immortal
    Taunt, Divine Shield. Battlecry: Spend 4 Mana to double this minion's stats.
    
    7费 5/8 德鲁伊随从 - 机械
    <b>嘲讽</b>，<b>圣盾</b>
    <b>战吼：</b>花费4点法力值，使本随从的属性值翻倍。
    """
    tags = {
        GameTag.TAUNT: True,
        GameTag.DIVINE_SHIELD: True,
    }
    
    def play(self):
        # 检查是否有至少4点法力值
        if self.controller.mana >= 4:
            # 花费4点法力值
            yield SpendMana(CONTROLLER, 4)
            # 使本随从的属性值翻倍
            yield Buff(SELF, "SC_763e")


class SC_763e:
    """属性翻倍"""
    def apply(self, target):
        # 翻倍攻击力和生命值
        target.atk *= 2
        target.max_health *= 2


# EPIC

class GDB_857:
    """究极边境 - Final Frontier
    Discover a 10-Cost minion from the past. Set its Cost to (1).
    
    7费 德鲁伊法术 - 奥术
    <b>发现</b>一张过去的法力值消耗为（10）点的随从牌。将其法力值消耗变为（1）点。
    """
    def play(self):
        # 发现一张10费随从（从过去的扩展包中）
        yield Discover(CONTROLLER, RandomMinion(cost=10)).then(
            Give(CONTROLLER, Discover.CARD),
            # 将其费用设置为1
            Buff(Discover.CARD, "GDB_857e")
        )


class GDB_857e:
    """法力值消耗变为（1）点"""
    tags = {
        GameTag.COST: SET(1),
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class GDB_882:
    """宇宙浑象 - Cosmic Phenomenon
    Summon three 2/3 Elementals with Taunt. If your board is full, give your minions +1/+1.
    
    5费 德鲁伊法术 - 奥术
    召唤三个2/3并具有<b>嘲讽</b>的元素。如果你的随从已满，则使你的随从获得+1/+1。
    """
    def play(self):
        # 检查场上是否已满（7个随从）
        board_full = len(self.controller.field) >= 7
        
        if board_full:
            # 场上已满，给所有随从+1/+1
            yield Buff(FRIENDLY_MINIONS, "GDB_882e")
        else:
            # 召唤三个2/3嘲讽元素
            yield Summon(CONTROLLER, "GDB_882t") * 3


class GDB_882t:
    """宇宙元素 - Cosmic Elemental
    2/3 元素，嘲讽
    """
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        GameTag.TAUNT: True,
    }
    race = Race.ELEMENTAL


class GDB_882e:
    """+1/+1 增益"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


# LEGENDARY

class GDB_854:
    """乌鲁，泛天巨兽 - Uluu, the Everdrifter
    Each turn this is in your hand, gain two random Choose One choices.
    
    5费 6/5 德鲁伊随从 - 野兽（传说）
    在本牌位于你的手牌中时，每个回合获得两个随机的<b>抉择</b>选项。
    
    实现说明：
    - 每回合在手牌中时，从所有可收集的Choose One卡牌中随机选择2个效果
    - 动态更新choose_cards列表，使卡牌变成Choose One卡牌
    - 打出时可以选择其中一个效果执行
    - 使用自定义事件处理器来动态生成Choose One选项
    """
    # 每个回合开始时，如果在手牌中，动态生成Choose One选项
    events = TurnStart(ALL_PLAYERS).on(
        Find(SELF + IN_HAND) & UpdateDynamicChooseOneOptions(SELF)
    )
    
    def play(self):
        # 打出时执行选中的Choose One效果
        # 由于choose_cards已经动态更新，正常的Choose One机制会处理选择
        # 这里不需要额外的逻辑
        pass


def UpdateDynamicChooseOneOptions(card_selector):
    """动态更新Uluu的Choose One选项
    
    从所有可收集的Choose One卡牌中随机选择2个效果
    并更新卡牌的choose_cards列表
    """
    def action(source):
        # 获取所有可收集的Choose One卡牌
        from ..cards import db
        
        # 收集所有Choose One选项
        all_choose_options = []
        for card_id, card_data in db.items():
            # 只选择可收集的卡牌
            if not getattr(card_data, 'collectible', False):
                continue
            # 检查是否有choose_cards属性
            if hasattr(card_data, 'choose_cards') and card_data.choose_cards:
                # 添加所有choose选项
                for option_id in card_data.choose_cards:
                    # 排除会变形卡牌的选项（如德鲁伊之爪）
                    # 排除需要目标的选项（避免复杂性）
                    option_data = db.get(option_id)
                    if option_data:
                        # 简单过滤：排除变形类选项
                        if not hasattr(option_data.scripts, 'play') or not any(
                            'Morph' in str(getattr(option_data.scripts.play, '__name__', ''))
                            for _ in [1]  # 简化检查
                        ):
                            all_choose_options.append(option_id)
        
        # 随机选择2个不同的选项
        if len(all_choose_options) >= 2:
            selected_options = source.game.random.sample(all_choose_options, 2)
            
            # 清空现有的choose_cards
            del source.choose_cards[:]
            
            # 添加新选择的选项
            for option_id in selected_options:
                option_card = source.controller.card(option_id, source=source, parent=source)
                source.choose_cards.append(option_card)
            
            # 标记卡牌为Choose One卡牌
            source.tags[GameTag.CHOOSE_ONE] = True
    
    return lambda source: action(source)


class GDB_856:
    """大主教奥萨尔 - Exarch Othaar
    Battlecry: If you're building a Starship, get 3 different Arcane spells and reduce their Costs by (2).
    
    4费 3/3 德鲁伊随从 - 德莱尼（传说）
    <b>战吼：</b>如果你正在建造<b>星舰</b>，则获取3张不同的奥术法术，并使其法力值消耗减少（2）点。
    """
    def play(self):
        # 检查是否正在建造星舰
        if self.controller.starship_in_progress:
            # 获取3张不同的奥术法术
            # 收集已获得的卡牌ID以确保不重复
            obtained_ids = set()
            obtained_cards = []
            
            # 尝试获取3张不同的奥术法术（最多尝试10次避免无限循环）
            attempts = 0
            while len(obtained_cards) < 3 and attempts < 10:
                attempts += 1
                cards = yield Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.ARCANE))
                if cards:
                    for card in cards:
                        if card and card.id not in obtained_ids:
                            obtained_ids.add(card.id)
                            obtained_cards.append(card)
                            # 给获得的法术减2费
                            yield Buff(card, "GDB_856e")
                            break


class GDB_856e:
    """法力值消耗减少（2）点"""
    tags = {
        GameTag.COST: -2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


