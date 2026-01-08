"""
决战荒芜之地 - HUNTER
"""
from ..utils import *


# COMMON

class DEEP_003:
    """磷光射击 - Shimmer Shot
    Deal $1 damage. Summon a random minion of that Cost.
    造成$1点伤害，随机召唤一个法力值消耗与伤害量相同的随从。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self):
        # 计算实际伤害量（基础1点 + 法术伤害加成）
        spell_damage = self.controller.spell_damage
        actual_damage = 1 + spell_damage

        # 造成伤害
        yield Hit(TARGET, actual_damage)

        # 召唤一个法力值消耗等于伤害量的随机随从
        yield Summon(CONTROLLER, RandomMinion(cost=actual_damage))


class DEEP_005:
    """黑曜亡魂 - Obsidian Revenant
    [x]Taunt Deathrattle: Summon two random Deathrattle minions that cost (3) or less.
    嘲讽。亡语：随机召唤两个法力值消耗小于或等于(3)点的亡语随从。
    """
    deathrattle = Summon(CONTROLLER, RandomMinion(deathrattle=True, cost=COST <= 3)) * 2


class WW_806:
    """潜踪群蛇 - Sneaky Snakes
    Summon two 1/1 Snakes with Stealth.
    召唤两只1/1并具有潜行的蛇。
    """
    play = Summon(CONTROLLER, "WW_806t") * 2


class WW_806t:
    """蛇 - Snake"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.STEALTH: True,
        GameTag.RACE: Race.BEAST,
    }


class WW_807:
    """秃鹫信使 - Messenger Buzzard
    [x]Deathrattle: Draw a Beast. Give minions in your hand +1/+1.
    亡语：抽一张野兽牌。使你手牌中的随从获得+1/+1。
    """
    deathrattle = (
        ForceDraw(CONTROLLER, FRIENDLY_DECK + BEAST) &
        Buff(FRIENDLY_HAND + MINION, "WW_807e")
    )


class WW_807e:
    """+1/+1 增益"""
    atk = 1
    max_health = 1


class WW_808:
    """银蛇 - Silver Serpent
    Rush, Poisonous Quickdraw: Gain Immune this turn.
    突袭，剧毒。快枪：在本回合中获得免疫。
    """
    def play(self):
        # 快枪：本回合获得并立即使用时触发
        if self.drawn_this_turn:
            yield Buff(SELF, "WW_808e")


class WW_808e:
    """免疫增益"""
    tags = {
        GameTag.IMMUNE: True,
    }
    events = OwnTurnEnds(CONTROLLER).on(Destroy(SELF))


# RARE

class DEEP_001:
    """错位化石 - Mismatched Fossils
    Discover a Beast and an Undead. Swap their stats.
    发现一张野兽牌和一张亡灵牌，交换其属性值。
    """
    def play(self):
        # 发现一张野兽牌
        beast_card = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, MINION + BEAST)
        )

        if not beast_card:
            return

        # 发现一张亡灵牌
        undead_card = yield GenericChoice(
            CONTROLLER,
            Discover(CONTROLLER, MINION + UNDEAD)
        )

        if not undead_card:
            # 如果没有选择亡灵牌，只给野兽牌
            yield Give(CONTROLLER, beast_card)
            return

        # 交换属性值
        beast_atk = beast_card.atk
        beast_health = beast_card.health
        undead_atk = undead_card.atk
        undead_health = undead_card.health

        # 给野兽牌添加到手牌，并设置交换后的属性
        yield Give(CONTROLLER, beast_card)
        yield Give(CONTROLLER, undead_card)

        # 应用属性交换buff
        if beast_card in self.controller.hand:
            yield Buff(beast_card, "DEEP_001e", atk=undead_atk, max_health=undead_health)

        if undead_card in self.controller.hand:
            yield Buff(undead_card, "DEEP_001e", atk=beast_atk, max_health=beast_health)


class DEEP_001e:
    """属性交换增益"""
    def __init__(self, tags, data):
        super().__init__(tags, data)
        # 从 data 中获取动态设置的属性值
        self.atk = data.get('atk', 0)
        self.max_health = data.get('max_health', 0)


class WW_809:
    """骷髅牛 - Bovine Skeleton
    Deathrattle: If this has 4 or more Attack, summon a Bovine Skeleton.
    亡语：如果本随从的攻击力大于或等于4点，召唤一只骷髅牛。
    """
    def deathrattle(self):
        if self.atk >= 4:
            yield Summon(CONTROLLER, "WW_809")


class WW_810:
    """迷彩坐骑 - Camouflage Mount
    Give a minion +3/+3 and a random Bonus Effect. When it dies, summon a Chameleon.
    使一个随从获得+3/+3和一个随机奖励效果。当它死亡时，召唤一只变色龙。
    """
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}

    def play(self):
        # 给予+3/+3
        yield Buff(TARGET, "WW_810e")

        # 随机给予一个奖励效果
        bonus_buffs = ["WW_810e_taunt", "WW_810e_divine_shield", "WW_810e_rush", "WW_810e_windfury"]
        random_buff = self.game.random.choice(bonus_buffs)
        yield Buff(TARGET, random_buff)

        # 添加亡语：召唤变色龙
        yield Buff(TARGET, "WW_810e_deathrattle")


class WW_810e:
    """+3/+3 增益"""
    atk = 3
    max_health = 3


class WW_810e_taunt:
    """嘲讽"""
    tags = {GameTag.TAUNT: True}


class WW_810e_divine_shield:
    """圣盾"""
    tags = {GameTag.DIVINE_SHIELD: True}


class WW_810e_rush:
    """突袭"""
    tags = {GameTag.RUSH: True}


class WW_810e_windfury:
    """风怒"""
    tags = {GameTag.WINDFURY: True}


class WW_810e_deathrattle:
    """亡语：召唤变色龙"""
    deathrattle = Summon(CONTROLLER, "WW_810t")


class WW_810t:
    """变色龙 - Chameleon"""
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.RACE: Race.BEAST,
    }


class WW_811:
    """宽檐高帽 - Ten Gallon Hat
    [x]Draw a minion. Give it +1/+1 and "Deathrattle: Get a Ten Gallon Hat."
    抽一张随从牌。使其获得+1/+1和"亡语：获取一张宽檐高帽牌。"
    """
    def play(self):
        # 抽一张随从牌
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + MINION)

        # 如果成功抽到牌，给予增益
        if cards:
            for card in cards:
                if card:
                    yield Buff(card, "WW_811e")


class WW_811e:
    """+1/+1 和亡语增益"""
    atk = 1
    max_health = 1
    deathrattle = Give(CONTROLLER, "WW_811")


# EPIC

class WW_812:
    """跨鞍飞驰 - Saddle Up!
    Give your minions "Deathrattle: Summon a random Beast that costs (3) or less."
    使你的随从获得"亡语：随机召唤一只法力值消耗小于或等于(3)点的野兽。"
    """
    play = Buff(FRIENDLY_MINIONS, "WW_812e")


class WW_812e:
    """亡语增益"""
    deathrattle = Summon(CONTROLLER, RandomMinion(race=Race.BEAST, cost=COST <= 3))


class WW_813:
    """明星手枪 - Starshooter
    After your hero attacks, get an Arcane Shot.
    在你的英雄攻击后，获取一张奥术射击牌。
    """
    events = Attack(FRIENDLY_HERO).after(Give(CONTROLLER, "CS2_094"))


# LEGENDARY

class WW_814:
    """刺牙 - Spurfang
    [x]Battlecry and Deathrattle: Summon a random Beast with Cost equal to this minion's Attack.
    战吼和亡语：随机召唤一只法力值消耗等于本随从攻击力的野兽。
    """
    def play(self):
        # 战吼：召唤野兽
        cost = self.atk
        yield Summon(CONTROLLER, RandomMinion(race=Race.BEAST, cost=cost))

    def deathrattle(self):
        # 亡语：召唤野兽
        cost = self.atk
        yield Summon(CONTROLLER, RandomMinion(race=Race.BEAST, cost=cost))


class WW_815:
    """迷失者塞尔杜林 - Theldurin the Lost
    [x]Battlecry: If your deck started with no duplicates, gain Immune this turn and attack all enemies.
    战吼：如果你的套牌里没有相同的牌，在本回合中获得免疫并攻击所有敌人。
    """
    # 使用 FindDuplicates 评估器检查无重复套牌（参考 uldum/hunter.py ULD_156）
    powered_up = -FindDuplicates(FRIENDLY_DECK)

    def play(self):
        # 检查是否满足无重复条件
        if not self.powered_up:
            return

        # 获得免疫
        yield Buff(SELF, "WW_815e")

        # 攻击所有敌人（参考 uldum/hunter.py ULD_212 的攻击实现）
        enemies = list(self.controller.opponent.characters)
        for enemy in enemies:
            if enemy.zone == Zone.PLAY and self.zone == Zone.PLAY:
                yield Attack(SELF, enemy)


class WW_815e:
    """免疫增益"""
    tags = {
        GameTag.IMMUNE: True,
    }
    events = OwnTurnEnds(CONTROLLER).on(Destroy(SELF))
