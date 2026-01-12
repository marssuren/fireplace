"""
深入翡翠梦境 - DEMONHUNTER
"""
from ..utils import *
from .dark_gift_helpers import apply_dark_gift


# COMMON

class EDR_840:
    """恐怖收割 - Grim Harvest
    Draw a card. Summon a random Dormant Dreadseed.
    
    2费 法术
    抽一张牌。随机召唤一个休眠的恐魇种。
    """
    requirements = {}

    def play(self):
        # 抽一张牌
        yield Draw(CONTROLLER)
        # 随机召唤一个休眠的恐魇种 (3种之一)
        dreadseed_tokens = ["EDR_840t1", "EDR_840t2", "EDR_840t3"]
        yield Summon(CONTROLLER, self.game.random.choice(dreadseed_tokens))


class EDR_842:
    """亵渎之矛 - Defiled Spear
    [x]After your hero attacks an enemy, deal your hero's Attack damage to another random enemy.
    
    4费 2/3 武器
    在你的英雄攻击一个敌人后，对另一个随机敌人造成等同于你英雄攻击力的伤害。
    """
    # 监听英雄攻击事件
    events = Attack.on(
        lambda self, source, target: source == self.controller.hero and target.controller == self.controller.opponent,
        lambda self, source, target: [
            # 对另一个随机敌人造成等同于英雄攻击力的伤害
            Hit(RandomTarget(ENEMY_CHARACTERS - target), source.atk)
        ]
    )


class EDR_890:
    """梦魇龙裔 - Nightmare Dragonkin
    Deathrattle: Reduce the Cost of the right-most card in your hand by (2).
    
    3费 3/4 龙
    亡语:使你手牌中最右边的卡牌的法力值消耗减少(2)点。
    """
    deathrattle = Buff(Find(CONTROLLER_HAND + FRIENDLY + RIGHTMOST), "EDR_890e")


class EDR_890e:
    """梦魇龙裔减费 - Nightmare Dragonkin Cost Reduction"""
    tags = {GameTag.COST: -2}


class FIR_952:
    """灼热掠夺者 - Scorchreaver
    [x]Battlecry: Discover a Fel spell. Reduce the Cost of Fel spells in your hand by (1).
    
    3费 3/4 恶魔
    战吼:发现一张邪能法术牌。使你手牌中所有邪能法术牌的法力值消耗减少(1)点。
    """
    requirements = {}

    def play(self):
        # 发现一张邪能法术牌
        yield GenericChoice(CONTROLLER, RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.SPELL and c.spell_school == SpellSchool.FEL,
            count=3
        ))
        # 使手牌中所有邪能法术减少(1)费
        for card in self.controller.hand:
            if card.type == CardType.SPELL and card.spell_school == SpellSchool.FEL:
                yield Buff(card, "FIR_952e")


class FIR_952e:
    """灼热掠夺者减费 - Scorchreaver Cost Reduction"""
    tags = {GameTag.COST: -1}


# RARE

class EDR_841:
    """恐魂腐蚀者 - Dreadsoul Corrupter
    [x]Battlecry and Deathrattle: Summon a random Dormant Dreadseed.
    
    3费 3/3 恶魔
    战吼，亡语:随机召唤一个休眠的恐魇种。
    """
    def play(self):
        # 战吼:随机召唤一个休眠的恐魇种
        dreadseed_tokens = ["EDR_840t1", "EDR_840t2", "EDR_840t3"]
        yield Summon(CONTROLLER, self.game.random.choice(dreadseed_tokens))
    
    # 亡语:随机召唤一个休眠的恐魇种
    @property
    def deathrattle(self):
        dreadseed_tokens = ["EDR_840t1", "EDR_840t2", "EDR_840t3"]
        return [Summon(CONTROLLER, self.game.random.choice(dreadseed_tokens))]


class EDR_882:
    """跳脸惊吓 - Jumpscare!
    Discover a Demon that costs (5) or more with a Dark Gift. Shuffle the other two into your deck.
    
    4费 法术
    发现一张法力值消耗大于或等于(5)点并具有黑暗之赐的恶魔牌。将另外两张洗入你的牌库。
    """
    requirements = {}

    def play(self):
        # 生成3个5费以上的恶魔并应用黑暗之赐
        from ...enums import Race
        
        # 创建3个带Dark Gift的恶魔选项
        demon_filter = lambda c: (
            c.type == CardType.MINION and 
            Race.DEMON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False and
            c.cost >= 5
        )
        
        # 生成3个选项
        option1 = self.controller.card(RandomCard(CONTROLLER, card_filter=demon_filter).id)
        option2 = self.controller.card(RandomCard(CONTROLLER, card_filter=demon_filter).id)
        option3 = self.controller.card(RandomCard(CONTROLLER, card_filter=demon_filter).id)
        
        # 应用黑暗之赐
        yield apply_dark_gift(option1)
        yield apply_dark_gift(option2)
        yield apply_dark_gift(option3)
        
        # 发现机制:选择一张加入手牌,其他两张洗入牌库
        yield GenericChoice(CONTROLLER, [option1, option2, option3])
        
        # 将未选择的两张洗入牌库
        # 获取选中的卡牌
        chosen_card = None
        if self.controller.hand:
            chosen_card = self.controller.hand[-1]  # 最后加入手牌的是选中的
        
        # 将未选择的洗入牌库
        for option in [option1, option2, option3]:
            if option != chosen_card:
                yield Shuffle(CONTROLLER, option)


class EDR_891:
    """贪婪的地狱猎犬 - Ravenous Felhunter
    Deathrattle: Resurrect a friendly Deathrattle minion that costs (4) or less. Summon a copy of it.
    
    5费 5/3 恶魔
    亡语:复活一个法力值消耗小于或等于(4)点的友方亡语随从。召唤它的一个复制。
    """
    @property
    def deathrattle(self):
        """动态亡语:复活一个4费以下的亡语随从并召唤复制"""
        # 获取本局游戏中死亡的4费以下亡语随从
        dead_deathrattle_minions = [
            m for m in self.controller.graveyard
            if m.type == CardType.MINION and 
            hasattr(m, 'deathrattle') and 
            m.deathrattle is not None and
            m.cost <= 4
        ]
        
        if dead_deathrattle_minions:
            # 随机选择一个
            target = self.game.random.choice(dead_deathrattle_minions)
            # 复活它并召唤一个复制
            return [
                Summon(CONTROLLER, target.id),
                Summon(CONTROLLER, target.id)
            ]
        return None


class FIR_904:
    """邪火爆焰 - Felfire Blaze
    [x]After you cast a Fel spell, destroy this and deal 2 damage to all enemies.
    
    2费 2/3 元素
    在你施放一个邪能法术后,消灭该随从并对所有敌人造成2点伤害。
    """
    # 监听邪能法术施放事件
    events = OWN_SPELL_PLAY.after(
        lambda self, source, target: source.spell_school == SpellSchool.FEL,
        lambda self, source, target: [
            # 消灭自己
            Destroy(SELF),
            # 对所有敌人造成2点伤害
            Hit(ENEMY_CHARACTERS, 2)
        ]
    )


# EPIC

class EDR_820:
    """飞龙之眠 - Wyvern's Slumber
    Choose One - Summon two Dormant Dreadseeds; or Deal $2 damage to all minions.
    
    3费 法术
    抉择:召唤两个休眠的恐魇种;或对所有随从造成$2点伤害。
    """
    choose = ("EDR_820a", "EDR_820b")


class EDR_820a:
    """召唤恐魇种 - Summon Dreadseeds"""
    requirements = {}
    
    def play(self):
        # 召唤两个随机休眠的恐魇种
        dreadseed_tokens = ["EDR_840t1", "EDR_840t2", "EDR_840t3"]
        yield Summon(CONTROLLER, self.game.random.choice(dreadseed_tokens))
        yield Summon(CONTROLLER, self.game.random.choice(dreadseed_tokens))


class EDR_820b:
    """群体伤害 - AoE Damage"""
    requirements = {}
    
    def play(self):
        # 对所有随从造成2点伤害
        yield Hit(ALL_MINIONS, 2)


class EDR_892:
    """残暴的魔蝠 - Ferocious Felbat
    [x]Deathrattle: Resurrect a different friendly Deathrattle minion that costs (5) or more. Summon a copy of it.
    
    7费 7/5 恶魔
    亡语:复活一个法力值消耗大于或等于(5)点的不同友方亡语随从。召唤它的一个复制。
    """
    @property
    def deathrattle(self):
        """动态亡语:复活一个5费以上的不同亡语随从并召唤复制"""
        # 获取本局游戏中死亡的5费以上亡语随从(排除自己)
        dead_deathrattle_minions = [
            m for m in self.controller.graveyard
            if m.type == CardType.MINION and 
            hasattr(m, 'deathrattle') and 
            m.deathrattle is not None and
            m.cost >= 5 and
            m.id != self.id  # 排除自己
        ]
        
        if dead_deathrattle_minions:
            # 随机选择一个
            target = self.game.random.choice(dead_deathrattle_minions)
            # 复活它并召唤一个复制
            return [
                Summon(CONTROLLER, target.id),
                Summon(CONTROLLER, target.id)
            ]
        return None


class FIR_902:
    """燃薪咒符 - Sigil of Cinder
    [x]At the start of your next turn, deal $6 damage randomly split among all enemies.
    
    2费 法术 - 邪能学派
    在你的下个回合开始时,随机对所有敌人造成总共$6点伤害。
    """
    requirements = {}

    def play(self):
        # 给控制者添加一个buff,在下回合开始时触发
        yield Buff(CONTROLLER, "FIR_902e")


class FIR_902e:
    """燃薪咒符延迟效果 - Sigil of Cinder Delayed Effect"""
    # 在下回合开始时触发
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 随机对所有敌人造成6点伤害
            Hit(RandomTarget(ENEMY_CHARACTERS), 1) * 6,
            # 移除自己
            Destroy(SELF)
        ]
    )


# LEGENDARY

class EDR_421:
    """年兽 - Omen
    [x]Rush, Windfury Deathrattle: Deal 1 damage to all enemies. <i>(Improves after this attacks!)</i>
    
    10费 6/12 野兽+恶魔
    突袭。风怒。亡语:对所有敌人造成1点伤害。(在该随从攻击后改进!)
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.WINDFURY: True,
    }
    
    # 攻击后改进亡语效果
    events = Attack.after(
        lambda self, source, target: source == self,
        lambda self, source, target: [
            # 增加亡语伤害计数
            Buff(SELF, "EDR_421e")
        ]
    )
    
    @property
    def deathrattle(self):
        """动态亡语:对所有敌人造成伤害,伤害值随攻击次数增加"""
        # 计算攻击次数(通过buff层数)
        damage = 1
        for buff in self.buffs:
            if buff.id == "EDR_421e":
                damage += 1
        
        return [Hit(ENEMY_CHARACTERS, damage)]


class EDR_421e:
    """年兽改进 - Omen Improvement"""
    # 每次攻击后叠加一层
    pass


class EDR_493:
    """阿莱纳希 - Alara'shi
    [x]Battlecry: Transform minions in your hand into random Demons. <i>(They keep their original stats and Cost.)</i>
    
    5费 5/5 野兽+恶魔
    战吼:将你手牌中的所有随从牌转化为随机恶魔牌。(保留原本的属性和法力值消耗。)
    """
    def play(self):
        # 获取手牌中的所有随从牌(排除自己)
        minions_in_hand = [c for c in self.controller.hand if c.type == CardType.MINION and c != self]
        
        for minion in minions_in_hand:
            # 保存原始属性
            original_cost = minion.cost
            original_atk = minion.atk
            original_health = minion.health
            original_max_health = minion.max_health
            
            # 随机选择一个恶魔ID
            from ...enums import Race
            demon_filter = lambda c: (
                c.type == CardType.MINION and 
                Race.DEMON in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False
            )
            
            # 获取随机恶魔的ID
            random_demon = RandomCard(CONTROLLER, card_filter=demon_filter)
            demon_id = random_demon.id if hasattr(random_demon, 'id') else random_demon
            
            # 转化为随机恶魔
            yield Morph(minion, demon_id)
            
            # Morph后需要重新获取卡牌引用(通过手牌位置)
            # 由于Morph会替换卡牌,我们需要在Morph后立即应用buff
            # 使用SetTag直接设置属性以保留原始数值
            yield SetTags(minion, {GameTag.COST: original_cost})
            yield SetTags(minion, {GameTag.ATK: original_atk})
            yield SetTags(minion, {GameTag.HEALTH: original_health})
            yield SetTags(minion, {GameTag.DAMAGE: 0})  # 重置伤害
