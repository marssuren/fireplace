"""
威兹班的工坊 - WARRIOR
"""
from ..utils import *


# COMMON

class MIS_902:
    """零件破拆 - Part Scrapper
    Lose up to 5 Armor. Your next Mech costs that much less.
    失去最多5点护甲值,你的下一张机械牌减少等量的法力值消耗。
    """
    # 2费法术
    # 效果：失去最多5点护甲值,下一张机械牌减少等量费用
    # 迷你包卡牌
    
    def play(self):
        """
        失去护甲并减少下一张机械牌的费用
        """
        # 获取当前护甲值
        current_armor = self.controller.hero.armor
        
        # 计算实际失去的护甲值（最多5点）
        armor_lost = min(current_armor, 5)
        
        if armor_lost > 0:
            # 失去护甲
            yield Hit(FRIENDLY_HERO, armor_lost, source=SELF)
            
            # 给控制者添加 Buff，记录减少的费用
            buff = yield Buff(CONTROLLER, "MIS_902e")
            if buff:
                buff[0].cost_reduction = armor_lost


class TOY_605:
    """质量保证 - Quality Assurance
    Draw 2 Taunt minions.
    抽两张<b>嘲讽</b>随从牌。
    """
    # 2费法术
    # 效果：抽2张嘲讽随从牌
    
    def play(self):
        # 抽2张嘲讽随从牌
        yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION + TAUNT) * 2


class TOY_606:
    """测试假人 - Testing Dummy
    <b>Taunt</b>. <b>Deathrattle:</b> Deal $8 damage randomly split among all enemy minions.
    <b>嘲讽</b>。<b>亡语：</b>造成8点伤害,随机分配到所有敌方随从身上。
    """
    # 6费 4/8 机械 嘲讽
    # 亡语：造成8点伤害,随机分配到所有敌方随从
    taunt = True
    
    def deathrattle(self):
        """
        亡语：造成8点伤害,随机分配到所有敌方随从
        """
        # 造成8点伤害,随机分配
        for _ in range(8):
            yield Hit(RANDOM(ENEMY_MINIONS), 1)


class TOY_907:
    """安全护目镜 - Safety Goggles
    Gain 6 Armor. Costs (0) if you don't have any Armor.
    获得6点护甲值。如果你没有护甲值,本牌的法力值消耗为(0)点。
    """
    # 2费法术
    # 效果：获得6点护甲值
    # 费用：如果没有护甲值则为0费
    
    play = GainArmor(FRIENDLY_HERO, 6)
    
    # 费用调整
    class Hand:
        """动态费用调整 Aura"""
        def apply(self, target):
            # 如果没有护甲值,费用为0
            if target.controller.hero.armor == 0:
                target.cost = 0


# RARE

class MIS_705:
    """标准的卡牌包 - Standardized Pack
    Add 5 random Taunt minions to your hand. They are <b>Temporary</b>.
    随机将五张<b>嘲讽</b>随从牌置入你的手牌。这些牌为<b>临时</b>牌。
    """
    # 1费法术
    # 效果：随机获得5张嘲讽随从,这些牌为临时牌
    # 迷你包卡牌
    
    def play(self):
        """
        获得5张随机嘲讽随从,标记为临时牌
        """
        for _ in range(5):
            # 随机获得一张嘲讽随从
            card = yield Give(CONTROLLER, RandomCollectible(type=CardType.MINION, tag=GameTag.TAUNT))
            
            if card:
                # 标记为临时卡牌（回合结束时弃掉）
                yield Buff(card[0], "MIS_705e")


class MIS_711:
    """安全专家 - Safety Expert
    <b>Rush</b>. <b>Deathrattle:</b> Shuffle three Bombs into your opponent's deck.
    <b>突袭</b>。<b>亡语：</b>将三张"炸弹" 牌洗入你对手的牌库。
    """
    # 10费 8/8 机械 突袭
    # 亡语：将3张炸弹洗入对手牌库
    # 迷你包卡牌
    rush = True
    
    def deathrattle(self):
        """
        亡语：将3张炸弹洗入对手牌库
        """
        # 炸弹 Token ID: GIL_537t (来自 boomsday 扩展包)
        for _ in range(3):
            yield Shuffle(OPPONENT, "GIL_537t")


class TOY_604:
    """砰砰扳手 - Boom Wrench
    <b>Miniaturize</b>
    <b>Deathrattle:</b> Trigger the <b>Deathrattle</b> of a random friendly Mech.
    <b>微缩</b>
    <b>亡语：</b>随机触发一个友方机械的<b>亡语</b>。
    """
    # 3费 3/0 武器 微缩
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


class TOY_651:
    """实验室奴隶主 - Lab Patron
    Whenever you gain Armor, summon another Lab Patron <i>(once per turn)</i>.
    每当你获得护甲值,召唤另一个实验室奴隶主<i>(每回合一次)</i>。
    """
    # 4费 3/3
    # 效果：每当获得护甲值,召唤另一个实验室奴隶主(每回合一次)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化每回合触发标记
        self.triggered_this_turn = False
    
    # 监听事件
    def _on_gain_armor(self, source, target, amount):
        """获得护甲时触发"""
        if not self.triggered_this_turn:
            self.triggered_this_turn = True
            return [Summon(CONTROLLER, ExactCopy(SELF))]
        return []
    
    events = [
        # 每回合开始时重置触发标记
        BeginTurn(CONTROLLER).on(lambda self, player: setattr(self, 'triggered_this_turn', False) or []),
        
        # 监听获得护甲事件
        GainArmor(CONTROLLER).after(_on_gain_armor)
    ]


class TOY_908:
    """焰火机师 - Fireworker
    <b>Deathrattle:</b> Summon two 1/1 Boom Bots. <i>WARNING: Bots may explode.</i>
    <b>亡语：</b>
    召唤两个1/1的砰砰机器人。<i>警告：该机器人随时可能爆炸。</i>
    """
    # 5费 5/5 机械
    # 亡语：召唤两个1/1砰砰机器人
    
    def deathrattle(self):
        """
        亡语：召唤两个砰砰机器人
        """
        # 砰砰机器人 Token ID: GVG_110t (来自 gvg 扩展包)
        yield Summon(CONTROLLER, "GVG_110t") * 2


# EPIC

class TOY_602:
    """化工泄漏 - Chemical Spill
    Summon the highest Cost minion from your hand, then deal $5 damage to it.
    从你的手牌中召唤法力值消耗最高的随从,然后对其造成$5点伤害。
    """
    # 6费法术
    # 效果：召唤手牌中费用最高的随从,然后对其造成5点伤害
    
    def play(self):
        """
        召唤手牌中费用最高的随从,然后造成伤害
        """
        # 获取手牌中的所有随从
        minions_in_hand = FRIENDLY_HAND + MINION
        minions_list = minions_in_hand.eval(self.game, self)
        
        if minions_list:
            # 找到费用最高的随从
            highest_cost_minion = max(minions_list, key=lambda m: m.cost)
            
            # 召唤它
            summoned = yield Summon(CONTROLLER, highest_cost_minion)
            
            if summoned:
                # 对其造成5点伤害
                yield Hit(summoned[0], 5)


class TOY_603:
    """炮灰出动 - Wreck'em and Deck'em
    Choose a friendly Mech. Summon a copy of it that attacks a random enemy, then dies.
    选择一个友方机械,召唤一个它的复制并使其攻击随机敌人然后死亡。
    """
    # 3费法术
    # 效果：选择友方机械,召唤复制并攻击随机敌人后死亡
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_WITH_RACE: Race.MECHANICAL}
    
    def play(self):
        """
        召唤目标机械的复制,攻击随机敌人后死亡
        """
        if TARGET:
            # 召唤复制
            copy = yield Summon(CONTROLLER, ExactCopy(TARGET))
            
            if copy:
                summoned_minion = copy[0]
                
                # 获取所有可攻击的敌人
                enemies = ENEMY_CHARACTERS
                enemies_list = enemies.eval(self.game, self)
                
                # 筛选可以被攻击的敌人
                valid_targets = [e for e in enemies_list if summoned_minion.can_attack(e)]
                
                if valid_targets:
                    # 随机选择一个敌人
                    target = self.game.random.choice(valid_targets)
                    
                    # 攻击
                    yield Attack(summoned_minion, target)
                
                # 然后死亡
                yield Destroy(summoned_minion)


# LEGENDARY

class TOY_607:
    """发明家砰砰 - Inventor Boom
    <b>Battlecry:</b> Resurrect two different friendly Mechs that cost (5) or more. They attack random enemies.
    <b>战吼：</b>复活两个不同的法力值消耗大于或等于(5)点的友方机械,并使其随机攻击敌人。
    """
    # 8费 7/7 传说
    # 战吼：复活两个不同的5费+机械,并使其攻击随机敌人
    
    def play(self):
        """
        复活两个不同的5费+机械,并使其攻击随机敌人
        """
        # 获取墓地中所有5费+的机械
        graveyard = self.controller.graveyard
        mechs = [card for card in graveyard 
                if card.type == CardType.MINION 
                and Race.MECHANICAL in card.races 
                and card.cost >= 5]
        
        if not mechs:
            return
        
        # 复活两个不同的机械
        resurrected_ids = set()
        resurrected_count = 0
        
        # 随机打乱顺序
        import random
        random.shuffle(mechs)
        
        for mech in mechs:
            # 确保不重复
            if mech.id not in resurrected_ids and resurrected_count < 2:
                # 复活
                summoned = yield Summon(CONTROLLER, Copy(mech))
                
                if summoned:
                    resurrected_ids.add(mech.id)
                    resurrected_count += 1
                    
                    summoned_minion = summoned[0]
                    
                    # 获取所有可攻击的敌人
                    enemies = ENEMY_CHARACTERS
                    enemies_list = enemies.eval(self.game, self)
                    
                    # 筛选可以被攻击的敌人
                    valid_targets = [e for e in enemies_list if summoned_minion.can_attack(e)]
                    
                    if valid_targets:
                        # 随机选择一个敌人
                        target = self.game.random.choice(valid_targets)
                        
                        # 攻击
                        yield Attack(summoned_minion, target)
            
            if resurrected_count >= 2:
                break


class TOY_906:
    """机械腐面 - Botface
    <b>Taunt</b>. After this takes damage, get two random <b>Minis</b>.
    <b>嘲讽</b>。在本随从受到伤害后,随机获取两张<b>微型</b>牌。
    """
    # 9费 4/12 机械 传说 嘲讽
    # 效果：受到伤害后,获得2张随机微型牌
    taunt = True
    
    # 监听受伤事件
    def _on_damage(self, source, target, amount):
        """受到伤害后获得2张随机微型牌"""
        # 获取所有微型牌（Miniaturize Token）
        # 从 tokens.py 中获取所有以 't' 结尾的微型卡牌
        miniaturize_tokens = [
            # Death Knight
            "TOY_828t",
            # Demon Hunter
            "TOY_652t",
            # Druid
            "TOY_801t",
            # Hunter
            "TOY_351t",
            # Mage
            "TOY_375t",
            # Neutral
            "MIS_025t", "TOY_312t", "TOY_307t", "TOY_340t1", "TOY_341t", "TOY_601t",
            # Paladin
            "TOY_811t", "TOY_813t",
            # Priest
            "TOY_380t",
            # Rogue
            "TOY_521t",
            # Shaman
            "TOY_513t", "TOY_501t",
            # Warlock
            "TOY_915t",
            # Warrior
            "TOY_604t"
        ]
        
        # 随机选择2张
        import random
        token1 = random.choice(miniaturize_tokens)
        token2 = random.choice(miniaturize_tokens)
        
        return [
            Give(CONTROLLER, token1),
            Give(CONTROLLER, token2)
        ]
    
    events = Damage(SELF).after(_on_damage)


# ========================================
# Buff 定义
# ========================================

class MIS_902e:
    """废铁零件 - Part Scrapper Buff
    Your next Mech costs less.
    你的下一张机械牌法力值消耗减少。
    """
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化费用减少量
        self.cost_reduction = 0
    
    # 监听打出机械牌事件
    events = Play(CONTROLLER, MINION + RACE(Race.MECHANICAL)).after(
        lambda self, source, card: Destroy(SELF)
    )
    
    # 费用减少 Aura（应用于手牌中的机械牌）
    class Hand:
        """在手牌时应用费用减少"""
        def apply(self, target):
            # 只对机械牌生效
            if target.type == CardType.MINION and Race.MECHANICAL in target.races:
                # 获取控制者身上的 MIS_902e Buff
                for buff in target.controller.buffs:
                    if buff.id == "MIS_902e" and hasattr(buff, 'cost_reduction'):
                        target.cost -= buff.cost_reduction


class MIS_705e:
    """临时卡牌标记 - Temporary Card Marker
    Discarded at end of turn
    回合结束时弃掉
    """
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.GHOSTLY: True  # 临时卡牌标记
    }
