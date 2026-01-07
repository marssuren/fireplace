"""
深入翡翠梦境 - HUNTER
"""
from ..utils import *
from .imbue_helpers import trigger_imbue


# COMMON

class EDR_226:
    """奇异训犬师 - Exotic Houndmaster
    Battlecry: Draw a Beast. Imbue your Hero Power.
    
    2费 2/2 随从
    战吼:抽一张野兽牌。灌注你的英雄技能。
    """
    requirements = {}
    
    def play(self):
        # 抽一张野兽牌
        yield ForceDraw(CONTROLLER, FRIENDLY_DECK + BEAST)
        # 触发 Imbue
        trigger_imbue(self.controller)



class EDR_263:
    """巨狼的恩赐 - Grace of the Greatwolf
    Choose One - Deal $4 damage to the enemy hero; or Summon two 3/2 Wolves with Rush.
    
    4费 法术
    抉择：对敌方英雄造成4点伤害；或召唤两个3/2并具有突袭的狼。
    """
    choose = ["EDR_263a", "EDR_263b"]


class EDR_263a:
    """巨狼的恩赐 - 选项A
    Deal $4 damage to the enemy hero.
    
    对敌方英雄造成4点伤害。
    """
    requirements = {}
    
    def play(self):
        yield Hit(ENEMY_HERO, 4)


class EDR_263b:
    """巨狼的恩赐 - 选项B
    Summon two 3/2 Wolves with Rush.
    
    召唤两个3/2并具有突袭的狼。
    """
    requirements = {}
    
    def play(self):
        # 召唤两个狼
        yield Summon(CONTROLLER, "EDR_263t")
        yield Summon(CONTROLLER, "EDR_263t")


class EDR_481:
    """神秘符文熊 - Mythical Runebear
    Taunt. Battlecry: If this has 4 or more Attack, summon a copy of this.
    
    4费 3/4 野兽
    嘲讽。战吼：如果此随从具有4点或更高攻击力，召唤一个此随从的复制。
    """
    tags = {
        GameTag.TAUNT: True,
    }
    
    def play(self):
        # 检查攻击力是否 >= 4
        if self.atk >= 4:
            # 召唤一个复制
            yield Summon(CONTROLLER, ExactCopy(SELF))


class FIR_909:
    """爆裂射击 - Bursting Shot
    Deal $2 damage to three random enemies.
    
    2费 火焰法术
    对三个随机敌人造成2点伤害。
    """
    requirements = {}
    
    def play(self):
        # 对三个随机敌人造成2点伤害
        for _ in range(3):
            yield Hit(RandomTarget(ENEMY_CHARACTERS), 2)


class FIR_960:
    """龙裔护育师 - Tending Dragonkin
    Battlecry: Copy the lowest Cost Beast in your hand.
    
    5费 5/5 龙
    战吼：复制你手牌中法力值消耗最低的野兽牌。
    """
    requirements = {}
    
    def play(self):
        # 找到手牌中法力值消耗最低的野兽牌
        beasts_in_hand = [c for c in self.controller.hand if c.race == Race.BEAST]
        
        if beasts_in_hand:
            # 按费用排序，取最低的
            lowest_cost_beast = min(beasts_in_hand, key=lambda c: c.cost)
            # 复制该野兽牌
            yield Give(CONTROLLER, ExactCopy(lowest_cost_beast))


# RARE

class EDR_227:
    """幽爪熊 - Umbraclaw
    Rush. Deathrattle: Imbue your Hero Power.
    
    4费 5/2 野兽
    突袭。亡语：灌注你的英雄技能。
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    @property
    def deathrattle(self):
        # 触发 Imbue
        trigger_imbue(self.controller)
        return []  # trigger_imbue 直接修改状态，不需要返回 action



class EDR_262:
    """灵魂联结 - Spirit Bond
    Deal $3 damage to a minion. If that kills it, summon a 3/2 Wolf with Rush.
    
    3费 法术
    对一个随从造成3点伤害。如果杀死它，召唤一个3/2并具有突袭的狼。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 造成3点伤害
        yield Hit(TARGET, 3)
        # 检查目标是否死亡
        if TARGET.dead or TARGET.to_be_destroyed:
            # 召唤一个狼
            yield Summon(CONTROLLER, "EDR_263t")


class EDR_416:
    """牧人之杖 - Shepherd's Crook
    After your hero attacks, summon a 3/3 Sheep that's Dormant for 2 turns.
    
    3费 3/2 武器
    在你的英雄攻击后，召唤一个3/3并休眠2回合的羊。
    """
    # 监听英雄攻击事件
    events = OWN_HERO_ATTACK.after(
        lambda self, source, target: [
            Summon(CONTROLLER, "EDR_416t")
        ]
    )


class FIR_953:
    """熔岩猎犬 - Magma Hound
    Rush. After this attacks a minion and survives, deal this minion's Attack damage split among all enemies.
    
    8费 5/8 野兽+元素
    突袭。在此随从攻击一个随从并存活后，造成等同于此随从攻击力的伤害，随机分配到所有敌人身上。
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    # 监听攻击事件
    events = SELF_ATTACK.after(
        # 条件：攻击的是随从 且 自己存活
        lambda self, source, target: target.type == CardType.MINION and not self.dead,
        lambda self, source, target: [
            # 造成等同于攻击力的伤害，随机分配到所有敌人
            Hit(ENEMY_CHARACTERS, self.atk, distribute=True)
        ]
    )


# EPIC

class EDR_014:
    """茏葱梦刃豹 - Verdant Dreamsaber
    Battlecry: If this costs (3) or less, attack two random enemy minions.
    
    5费 4/7 野兽
    战吼：如果此牌的法力值消耗为(3)或更低，攻击两个随机敌方随从。
    """
    requirements = {}
    
    def play(self):
        # 检查当前费用是否 <= 3
        if self.cost <= 3:
            # 攻击两个随机敌方随从
            for _ in range(2):
                targets = self.controller.opponent.field
                if targets:
                    import random
                    target = random.choice(targets)
                    yield Attack(SELF, target)


class EDR_261:
    """两栖之灵 - Amphibian's Spirit
    Give a minion +2/+2 and "Deathrattle: Give a friendly minion +2/+2 and this Deathrattle."
    
    3费 自然法术
    使一个随从获得+2/+2和"亡语：使一个友方随从获得+2/+2和此亡语"。
    """
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    
    def play(self):
        # 给予 +2/+2 和亡语效果
        yield Buff(TARGET, "EDR_261e")


# LEGENDARY

class EDR_480:
    """戈德林 - Goldrinn
    Rush. Friendly Beasts deal double damage.
    
    9费 9/9 野兽
    突袭。友方野兽造成双倍伤害。
    """
    tags = {
        GameTag.RUSH: True,
    }
    
    # 光环效果：友方野兽造成双倍伤害
    update = Refresh(FRIENDLY_MINIONS + BEAST, {
        GameTag.MULTIPLY_DAMAGE: 2,
    })


class EDR_853:
    """布罗尔·熊皮 - Broll Bearmantle
    After you cast a spell, summon a random Animal Companion.
    
    5费 3/5 随从
    在你施放一个法术后，召唤一个随机动物伙伴。
    """
    # 监听法术施放事件
    events = OWN_SPELL_PLAY.after(
        lambda self, source, target: [
            # 随机召唤一个动物伙伴
            # Animal Companions: NEW1_032 (Misha), NEW1_033 (Leokk), NEW1_034 (Huffer)
            Summon(CONTROLLER, RandomID("NEW1_032", "NEW1_033", "NEW1_034"))
        ]
    )


