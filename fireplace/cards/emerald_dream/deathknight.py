"""
深入翡翠梦境 - DEATHKNIGHT
"""
from ..utils import *
from .dark_gift_helpers import apply_dark_gift


# COMMON

class EDR_811:
    """暴行祭礼 - Rite of Atrocity
    Discover an Undead. Spend 2 Corpses to give it a Dark Gift.
    
    1费 法术 - 亡灵符文
    发现一张亡灵牌。消耗2残骸，使其获得黑暗之赐。
    """
    requirements = {}

    def play(self):
        # 发现一张亡灵牌
        from hearthstone.enums import Race
        yield GenericChoice(CONTROLLER, cards=RandomCardGenerator(
            CONTROLLER,
            card_filter=lambda c: c.type == CardType.MINION and Race.UNDEAD in getattr(c, 'races', [c.race]) if hasattr(c, 'race') else False,
            count=3
        ))
        
        # 检查是否有足够的残骸
        if self.controller.corpses >= 2:
            # 消耗2残骸
            self.controller.corpses -= 2
            # 获取刚发现的卡牌（手牌中最后一张）
            if self.controller.hand:
                discovered_card = self.controller.hand[-1]
                # 应用黑暗之赐
                yield apply_dark_gift(discovered_card)


class EDR_814:
    """感染吐息 - Infested Breath
    Deal $2 damage. Summon a 0/2 Leech.
    
    2费 法术 - 鲜血符文
    造成$2点伤害。召唤一个0/2的水蛭。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        # 造成2点伤害
        yield Hit(TARGET, 2)
        # 召唤一个0/2水蛭
        yield Summon(CONTROLLER, "EDR_814t")


class EDR_816:
    """怪异魔蚊 - Monstrous Mosquito
    At the end of your turn, give your other minions +1 Attack.
    
    1费 1/2 野兽
    在你的回合结束时，使你的其他随从获得+1攻击力。
    """
    # 回合结束时触发
    events = OWN_TURN_END.on(
        lambda self: [Buff(FRIENDLY_MINIONS - SELF, "EDR_816e")]
    )


class EDR_816e:
    """怪异魔蚊增益 - Monstrous Mosquito Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


class FIR_900:
    """火化 - Cremate
    Discover a minion with a Dark Gift. It costs (2) less.
    
    3费 法术 - 火焰学派
    发现一张具有黑暗之赐的随从牌。其法力值消耗减少(2)点。
    """
    requirements = {}

    def play(self):
        # 发现一张随从牌
        # 注意：Dark Gift 会在发现后自动应用（通过 Discover 机制）
        # 这里我们使用标准的 Discover 随从，然后应用 Dark Gift 和减费
        yield Discover(CONTROLLER, RandomMinion())
        
        # 获取刚发现的卡牌
        if self.controller.hand:
            discovered_card = self.controller.hand[-1]
            # 应用黑暗之赐
            yield apply_dark_gift(discovered_card)
            # 减少2费
            yield Buff(discovered_card, "FIR_900e")


class FIR_900e:
    """火化减费 - Cremate Cost Reduction"""
    cost = -2


# RARE

class EDR_813:
    """病变虫群 - Morbid Swarm
    Choose One - Summon two 1/1 Ants; or Spend 2 Corpses to deal $4 damage to a minion.
    
    1费 法术 - 鲜血+亡灵符文
    抉择：召唤两个1/1的蚂蚁；或消耗2残骸，对一个随从造成4点伤害。
    """
    choose = ("EDR_813a", "EDR_813b")


class EDR_813a:
    """召唤蚂蚁 - Summon Ants"""
    requirements = {}
    
    def play(self):
        # 召唤两个1/1蚂蚁
        yield Summon(CONTROLLER, "EDR_813t1")
        yield Summon(CONTROLLER, "EDR_813t1")


class EDR_813b:
    """虫群伤害 - Swarm Damage"""
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 检查是否有足够的残骸
        if self.controller.corpses >= 2:
            # 消耗2残骸
            self.controller.corpses -= 2
            # 造成4点伤害
            yield Hit(TARGET, 4)


class EDR_815:
    """尸魔花 - Corpse Flower
    After your opponent summons a minion, spend 2 Corpses to deal 3 damage to it.
    
    3费 0/5 亡灵
    在你的对手召唤一个随从后，消耗2残骸，对其造成3点伤害。
    """
    # 监听对手召唤随从事件
    events = Summon.on(
        lambda self, source, target: target.controller == self.controller.opponent and self.controller.corpses >= 2,
        lambda self, source, target: [
            # 消耗2残骸
            SetTags(CONTROLLER, {GameTag.CORPSES: self.controller.corpses - 2}),
            # 造成3点伤害
            Hit(target, 3)
        ]
    )


class EDR_817:
    """血虫感染 - Sanguine Infestation
    Draw 2 cards. Summon two 0/2 Leeches.
    
    5费 法术
    抽两张牌。召唤两个0/2的水蛭。
    """
    requirements = {}

    def play(self):
        # 抽两张牌
        yield Draw(CONTROLLER) * 2
        # 召唤两个0/2水蛭
        yield Summon(CONTROLLER, "EDR_814t")
        yield Summon(CONTROLLER, "EDR_814t")


class FIR_901:
    """霜灼巢母 - Frostburn Matriarch
    Battlecry: If you're holding a minion with a Dark Gift, summon two 4/4 Dragons with Taunt.
    
    5费 4/4 龙
    战吼：如果你的手牌中有具有黑暗之赐的随从牌，召唤两个4/4并具有嘲讽的龙。
    """
    def play(self):
        # 检查手牌中是否有具有黑暗之赐的随从
        from ...enums import DARK_GIFT
        has_dark_gift = any(
            card.type == CardType.MINION and getattr(card, 'tags', {}).get(DARK_GIFT, False)
            for card in self.controller.hand
        )
        
        if has_dark_gift:
            # 召唤两个4/4嘲讽龙
            yield Summon(CONTROLLER, "FIR_901t")
            yield Summon(CONTROLLER, "FIR_901t")


# EPIC

class EDR_810:
    """丑恶的残躯 - Hideous Husk
    [x]Your Leeches steal 1 more Health from their victims. Battlecry: Summon two 0/2 Leeches.
    
    6费 3/5 野兽+亡灵
    你的水蛭从其受害者身上多偷取1点生命值。战吼：召唤两个0/2的水蛭。
    """
    def play(self):
        # 战吼：召唤两个0/2水蛭
        yield Summon(CONTROLLER, "EDR_814t")
        yield Summon(CONTROLLER, "EDR_814t")
    
    # 光环效果：水蛭多偷1生命值
    # 给所有友方水蛭添加额外吸血buff
    update = Refresh(FRIENDLY_MINIONS, {
        "EDR_810e": lambda self, i: i.id == "EDR_814t"  # 只对水蛭生效
    })


class EDR_810e:
    """丑恶的残躯光环 - Hideous Husk Aura
    
    这个buff会在水蛭攻击时额外治疗1点生命值
    通过监听攻击事件实现
    """
    tags = {
        GameTag.LIFESTEAL: True,  # 确保有吸血
    }
    
    # 监听拥有此buff的随从攻击时，额外治疗1点生命值
    events = Attack.on(
        lambda self, source, target: source == self.owner,
        lambda self, source, target: [
            Heal(FRIENDLY_HERO, 1)  # 额外治疗1点生命值
        ]
    )


class EDR_812:
    """畸怪符文剑 - Grotesque Runeblade
    [x]Battlecry: If the last card you played had an Unholy rune, gain +1 Attack. Repeat for Blood and +1 Durability.
    
    2费 2/0 武器
    战吼：如果你打出的上一张牌具有亡灵符文，获得+1攻击力。如果具有鲜血符文，则改为获得+1耐久度。
    """
    def play(self):
        # 获取上一张打出的牌（核心已实现 last_card_played）
        if self.controller.last_card_played:
            last_card = self.controller.last_card_played
            
            # 检查符文消耗
            if hasattr(last_card, 'rune_cost'):
                rune_cost = last_card.rune_cost
                
                # 如果有亡灵符文，+1攻击力
                if rune_cost.get('unholy', 0) > 0:
                    yield Buff(FRIENDLY_WEAPON, "EDR_812e1")
                
                # 如果有鲜血符文，+1耐久度
                if rune_cost.get('blood', 0) > 0:
                    yield Buff(FRIENDLY_WEAPON, "EDR_812e2")


class EDR_812e1:
    """畸怪符文剑攻击增益 - Grotesque Runeblade Attack"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
    }


class EDR_812e2:
    """畸怪符文剑耐久增益 - Grotesque Runeblade Durability"""
    max_durability = 1


# LEGENDARY

class EDR_818:
    """尼珊德拉 - Nythendra
    [x]Taunt. Deathrattle: Split into 1/1 Beetles. At the start of your turn, reform with any remaining.
    
    7费 7/7 亡灵+龙
    嘲讽。亡语：分裂成1/1的甲虫。在你的回合开始时，用剩余的甲虫重组。
    
    注意：根据官方数据，分裂的甲虫数量等于尼珊德拉的攻击力
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    @property
    def deathrattle(self):
        """动态亡语：根据当前攻击力召唤甲虫"""
        # 召唤数量等于当前攻击力的甲虫
        beetle_count = self.atk
        return [Summon(CONTROLLER, "EDR_818t") for _ in range(beetle_count)]


class EDR_818t:
    """甲虫 - Nythendric Beetle
    1/1 Beast
    At the start of your turn, if you control any Beetles, reform into Nythendra.
    
    1/1 野兽
    在你的回合开始时，如果你控制任意数量的甲虫，将它们全部重组为尼珊德拉。
    
    注意：重组后的尼珊德拉攻击/生命等于甲虫数量
    """
    # 回合开始时检查并重组
    events = OWN_TURN_BEGIN.on(
        lambda self: [
            # 统计场上所有甲虫
            EDR_818t._reform_nythendra(self)
        ] if any(m.id == "EDR_818t" for m in self.controller.field) else []
    )
    
    @staticmethod
    def _reform_nythendra(beetle):
        """重组尼珊德拉的辅助函数"""
        # 统计场上甲虫数量
        beetles = [m for m in beetle.controller.field if m.id == "EDR_818t"]
        beetle_count = len(beetles)
        
        if beetle_count > 0:
            # 销毁所有甲虫
            for b in beetles:
                yield Destroy(b)
            
            # 召唤一个攻击/生命等于甲虫数量的尼珊德拉
            yield Summon(beetle.controller, "EDR_818")
            
            # 给新召唤的尼珊德拉设置属性
            # 注意：这里需要动态设置攻击和生命值
            if beetle.controller.field:
                nythendra = beetle.controller.field[-1]  # 最后召唤的随从
                if nythendra.id == "EDR_818":
                    # 设置攻击和生命值为甲虫数量
                    yield Buff(nythendra, "EDR_818e", atk_bonus=beetle_count - 7, health_bonus=beetle_count - 7)


class EDR_818e:
    """尼珊德拉重组增益 - Nythendra Reform Buff"""
    def __init__(self, *args, atk_bonus=0, health_bonus=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk = atk_bonus
        self.max_health = health_bonus


class EDR_819:
    """乌索克 - Ursoc
    Battlecry: Attack ALL other minions. Deathrattle: Resurrect any this killed.
    
    9费 6/14 野兽
    战吼：攻击所有其他随从。亡语：复活所有被其杀死的随从。
    
    注意：只复活被其攻击杀死的随从，不包括攻击它而死的随从
    """
    def play(self):
        # 获取所有其他随从
        all_other_minions = [m for m in self.game.board if m != self]
        
        # 记录每个随从攻击前的状态
        killed_minions = []
        
        for minion in all_other_minions:
            # 记录攻击前的生命值
            was_alive = not minion.dead
            
            # 攻击随从
            yield Attack(SELF, minion)
            
            # 检查是否被杀死（攻击前活着，攻击后死了）
            if was_alive and minion.dead:
                killed_minions.append(minion.id)
        
        # 将被杀死的随从ID存储到自定义属性中
        # 使用 SetAttr 来存储数据
        self._killed_minions = killed_minions
    
    @property
    def deathrattle(self):
        """动态亡语：复活被杀死的随从"""
        # 从自定义属性中获取被杀死的随从ID列表
        killed_ids = getattr(self, '_killed_minions', [])
        
        if killed_ids:
            return [Summon(CONTROLLER, card_id) for card_id in killed_ids]
        return []


class FIR_951:
    """沃尔科罗斯 - Volcoross
    [x]Rush, Taunt Battlecry: Choose to spend 10, 20, or 30 Corpses to gain that many stats.
    
    8费 5/5 元素+野兽
    突袭。嘲讽。战吼：选择消耗10份，20份或30份残骸以获得等量属性值。
    """
    tags = {
        GameTag.RUSH: True,
        GameTag.TAUNT: True,
    }
    
    choose = ("FIR_951a", "FIR_951b", "FIR_951c")


class FIR_951a:
    """消耗10残骸 - Spend 10 Corpses"""
    requirements = {}
    
    def play(self):
        if self.controller.corpses >= 10:
            self.controller.corpses -= 10
            # 获得+10/+10
            # 注意：需要找到刚召唤的沃尔科罗斯
            volcoross = [m for m in self.controller.field if m.id == "FIR_951"]
            if volcoross:
                yield Buff(volcoross[-1], "FIR_951e", atk=10, health=10)


class FIR_951b:
    """消耗20残骸 - Spend 20 Corpses"""
    requirements = {}
    
    def play(self):
        if self.controller.corpses >= 20:
            self.controller.corpses -= 20
            # 获得+20/+20
            volcoross = [m for m in self.controller.field if m.id == "FIR_951"]
            if volcoross:
                yield Buff(volcoross[-1], "FIR_951e", atk=20, health=20)


class FIR_951c:
    """消耗30残骸 - Spend 30 Corpses"""
    requirements = {}
    
    def play(self):
        if self.controller.corpses >= 30:
            self.controller.corpses -= 30
            # 获得+30/+30
            volcoross = [m for m in self.controller.field if m.id == "FIR_951"]
            if volcoross:
                yield Buff(volcoross[-1], "FIR_951e", atk=30, health=30)


class FIR_951e:
    """沃尔科罗斯增益 - Volcoross Buff"""
    # 动态属性增益
    def __init__(self, *args, atk=0, health=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.atk = atk
        self.max_health = health


# Enchantments (来自其他职业，但在这里定义以保持完整性)

class EDR_060e:
    """大地庇护嘲讽 - Ward of Earth Taunt"""
    tags = {
        GameTag.TAUNT: True,
    }


class EDR_270e:
    """丰裕之角减费 - Horn of Plenty Cost Reduction"""
    cost = -2


class FIR_908e:
    """火炭变色龙增益 - Charred Chameleon Buff"""
    tags = {
        GameTag.RUSH: True,
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
    }


class EDR_847e:
    """梦缚信徒增益 - Dreambound Disciple Buff"""
    # 下一个英雄技能0费
    # 这需要在英雄技能使用时检查并移除
    pass


class EDR_271e:
    """林地塑型者树人 - Grove Shaper Treant Buff"""
    # 用于存储法术ID
    def __init__(self, *args, spell_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id


class FIR_906e:
    """过热增益 - Overheat Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }
