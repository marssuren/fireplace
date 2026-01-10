"""
决战荒芜之地 - WARRIOR
"""
from ..utils import *


# COMMON

class DEEP_011:
    """灼燃之心 - Burning Heart
    对一个随从造成$2点伤害，如果它依然存活，使你的英雄在本回合中获得+3攻击力。
    Deal $2 damage to a minion. If it survives, give your hero +3 Attack this turn.
    """
    # Type: SPELL | Cost: 1 | Rarity: COMMON | School: FIRE
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}
    
    def play(self):
        yield Hit(TARGET, 2)
        # 检查目标是否依然存活
        if TARGET.zone == Zone.PLAY:
            yield Buff(FRIENDLY_HERO, "DEEP_011e")


class DEEP_011e:
    """本回合+3攻击力"""
    tags = {GameTag.ATK: 3}
    events = OWN_TURN_END.on(Destroy(SELF))


class DEEP_019:
    """赤红岩床 - Crimson Expanse
    选择一个受伤的随从，召唤一个它的休眠一回合的复制。
    [x]Choose a damaged minion. Summon a copy of it that goes Dormant for one turn.
    """
    # Type: LOCATION | Cost: 4 | Durability: 2 | Rarity: COMMON
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: True,
        PlayReq.REQ_MINION_TARGET: True,
        PlayReq.REQ_DAMAGED_TARGET: True
    }
    
    def activate(self):
        # 召唤复制并设置为休眠
        yield Summon(CONTROLLER, ExactCopy(TARGET)).then(
            SetTag(Summon.CARD, GameTag.DORMANT),
            Buff(Summon.CARD, "DEEP_019e")
        )


class DEEP_019e:
    """休眠1回合"""
    events = OWN_TURN_BEGIN.on(
        SetTags(OWNER, {GameTag.DORMANT: False}),
        Destroy(SELF)
    )


class WW_329:
    """机甲爆王 - Detonation Juggernaut
    嘲讽。战吼：使你手牌中的嘲讽随从牌获得+2/+2。
    Taunt. Battlecry: Give Taunt minions in your hand +2/+2.
    """
    # Type: MINION | Cost: 4 | Attack: 3 | Health: 4 | Race: MECHANICAL | Rarity: COMMON
    taunt = True
    
    def play(self):
        yield Buff(FRIENDLY_HAND + MINION + TAUNT, "WW_329e")


class WW_329e:
    """+2/+2"""
    tags = {GameTag.ATK: 2, GameTag.HEALTH: 2}


class WW_334:
    """加固护板 - Reinforced Plating
    获得6点护甲值。发掘一个宝藏。
    Gain 6 Armor. Excavate a treasure.
    """
    # Type: SPELL | Cost: 3 | Rarity: COMMON
    def play(self):
        yield GainArmor(FRIENDLY_HERO, 6)
        yield Excavate(CONTROLLER)


class WW_347:
    """矿镐战斧 - Battlepickaxe
    在你使用一张嘲讽随从牌后，获得+1耐久度。
    After you play a Taunt minion, gain +1 Durability.
    """
    # Type: WEAPON | Cost: 3 | Attack: 4 | Durability: 1 | Rarity: COMMON
    events = Play(CONTROLLER, MINION + TAUNT).after(
        Buff(SELF, "WW_347e")
    )


class WW_347e:
    """+1耐久度"""
    tags = {GameTag.DURABILITY: 1}


# RARE

class DEEP_010:
    """余震 / Aftershocks
    对所有随从造成$1点伤害，造成三次。如果你在上个回合施放过法术，则法力值消耗减少（2）点。
    Deal $1 damage to all minions, three times. Costs (2) less if you cast a spell last turn."""
    # Type: SPELL | Cost: 4 | Rarity: RARE | School: NATURE
    def play(self):
        for _ in range(3):
            yield Hit(ALL_MINIONS, 1)
    
    # 检查上回合是否施放过法术，减少费用
    cost_mod = lambda self, i: -2 if getattr(self.controller, 'spells_played_last_turn', 0) > 0 else 0


class WW_346:
    """爆破龟 - Blast Tortoise
    嘲讽。战吼：对所有敌方随从造成等同于本随从攻击力的伤害。
    [x]Taunt Battlecry: Deal damage to all enemy minions equal to this minion's Attack.
    """
    # Type: MINION | Cost: 6 | Attack: 2 | Health: 7 | Race: BEAST | Rarity: RARE
    taunt = True
    
    def play(self):
        yield Hit(ENEMY_MINIONS, ATK(SELF))


class WW_367:
    """倒霉的炸药师 - Unlucky Powderman
    嘲讽。亡语：使你手牌和牌库中的嘲讽随从牌获得+1/+1。
    Taunt Deathrattle: Give Taunt minions in your hand and deck +1/+1.
    """
    # Type: MINION | Cost: 2 | Attack: 2 | Health: 2 | Race: UNDEAD | Rarity: RARE
    taunt = True
    deathrattle = Buff(FRIENDLY_HAND + MINION + TAUNT | FRIENDLY_DECK + MINION + TAUNT, "WW_367e")


class WW_367e:
    """+1/+1"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class WW_380:
    """起爆炸药 - Blast Charge
    消灭一个受伤的敌方随从。发掘一个宝藏。
    Destroy a damaged enemy minion. Excavate a treasure.
    """
    # Type: SPELL | Cost: 2 | Rarity: RARE
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: True,
        PlayReq.REQ_MINION_TARGET: True,
        PlayReq.REQ_DAMAGED_TARGET: True,
        PlayReq.REQ_ENEMY_TARGET: True
    }
    
    def play(self):
        yield Destroy(TARGET)
        yield Excavate(CONTROLLER)


# EPIC

class WW_348:
    """误炸 - Misfire
    对随机随从分别造成$3点，$2点和$1点伤害。快枪：可以选择目标。
    Deal $3, $2, and $1 damage to random minions. Quickdraw: Choose targets.
    """
    # Type: SPELL | Cost: 2 | Rarity: EPIC | Mechanics: QUICKDRAW
    
    def play(self):
        if self.drawn_this_turn:
            # 快枪：选择三个目标
            # 第一个目标造成3点伤害
            target1 = yield GenericChoice(CONTROLLER, ALL_MINIONS)
            if target1:
                yield Hit(target1, 3)
            
            # 第二个目标造成2点伤害
            target2 = yield GenericChoice(CONTROLLER, ALL_MINIONS)
            if target2:
                yield Hit(target2, 2)
            
            # 第三个目标造成1点伤害
            target3 = yield GenericChoice(CONTROLLER, ALL_MINIONS)
            if target3:
                yield Hit(target3, 1)
        else:
            # 普通：随机目标
            # 造成3点伤害
            minions = list(self.game.board)
            if minions:
                target = self.game.random.choice(minions)
                yield Hit(target, 3)
            
            # 造成2点伤害
            minions = list(self.game.board)
            if minions:
                target = self.game.random.choice(minions)
                yield Hit(target, 2)
            
            # 造成1点伤害
            minions = list(self.game.board)
            if minions:
                target = self.game.random.choice(minions)
                yield Hit(target, 1)


class WW_349:
    """荒芜之地乱斗打手 - Badlands Brawler
    战吼：发起一场绝命乱斗！如果你已经发掘过两次，则本随从总会赢得胜利。
    Battlecry: Start a Brawl! If you've Excavated twice, this always wins.
    """
    # Type: MINION | Cost: 7 | Attack: 4 | Health: 4 | Rarity: EPIC
    def play(self):
        if self.controller.times_excavated >= 2:
            # 发掘2次或以上：本随从必胜
            # 给自己添加"总是赢得绝命乱斗"标记
            yield Buff(SELF, "WW_349e")
            # 执行绝命乱斗
            yield Find(ALL_MINIONS + ALWAYS_WINS_BRAWLS) & Destroy(
                ALL_MINIONS - RANDOM(ALL_MINIONS + ALWAYS_WINS_BRAWLS)
            ) | Destroy(ALL_MINIONS - RANDOM_MINION)
        else:
            # 正常绝命乱斗
            yield Find(ALL_MINIONS + ALWAYS_WINS_BRAWLS) & Destroy(
                ALL_MINIONS - RANDOM(ALL_MINIONS + ALWAYS_WINS_BRAWLS)
            ) | Destroy(ALL_MINIONS - RANDOM_MINION)


class WW_349e:
    """总是赢得绝命乱斗"""
    tags = {GameTag.ALWAYS_WINS_BRAWLS: True}


# LEGENDARY

class DEEP_020:
    """深岩矿工布莱恩 - Deepminer Brann
    战吼：如果你的套牌里没有相同的牌，则在本局对战的剩余时间内，你的战吼会触发两次。
    [x]Battlecry: If your deck started with no duplicates, your Battlecries trigger twice for the rest of the game.
    """
    # Type: MINION | Cost: 6 | Attack: 2 | Health: 4 | Rarity: LEGENDARY
    def play(self):
        # 检查起始套牌是否无重复
        if Evaluator(FindDuplicates, FRIENDLY_DECK) == 0:
            yield Buff(FRIENDLY_HERO, "DEEP_020e")


class DEEP_020e:
    """战吼触发两次"""
    tags = {GameTag.EXTRA_BATTLECRIES: 1}


class WW_372:
    """爆破工头索格伦 - Boomboss Tho'grun
    战吼：将3张TNT炸药洗入你对手的牌库。当抽到炸药时，炸毁其手牌，牌库和面板上的各一张牌。
    [x]Battlecry: Shuffle 3 T.N.T. into your opponent's deck. When drawn, blow up a card in their hand, deck, and board.
    """
    # Type: MINION | Cost: 8 | Attack: 7 | Health: 7 | Rarity: LEGENDARY
    def play(self):
        for _ in range(3):
            yield Shuffle(OPPONENT, "WW_372t")


class WW_372t:
    """TNT炸药 - T.N.T.
    当抽到时，炸毁你手牌、牌库和面板上的各一张牌。
    When drawn, blow up a card in your hand, deck, and board.
    """
    # Type: SPELL | Cost: 0 | Rarity: LEGENDARY
    # 当抽到时触发
    drawn = (
        # 炸毁手牌中的一张牌（排除自己）
        Find(FRIENDLY_HAND - SELF) & Destroy(RANDOM(FRIENDLY_HAND - SELF)),
        # 炸毁牌库中的一张牌
        Find(FRIENDLY_DECK) & Mill(RANDOM(FRIENDLY_DECK)),
        # 炸毁场上的一张随从
        Find(FRIENDLY_MINIONS) & Destroy(RANDOM(FRIENDLY_MINIONS))
    )


class WW_375:
    """偃息的焰喉 - Slagmaw the Slumbering
    突袭。嘲讽。休眠6回合。（发掘即可提前2回合唤醒！）
    Rush, Taunt Dormant for 6 turns. <i>(Excavate to awaken 2 turns sooner!)</i>
    """
    # Type: MINION | Cost: 4 | Attack: 16 | Health: 16 | Race: ELEMENTAL/BEAST | Rarity: LEGENDARY
    rush = True
    taunt = True
    tags = {GameTag.DORMANT: True}
    dormant_turns = 6
    
    # 监听发掘事件，每次发掘减少2回合休眠时间
    # 核心的 dormant_turns property 会在计数清零时自动唤醒（card.py 第1325-1334行）
    events = Excavate(CONTROLLER).after(
        lambda self, source: setattr(source.owner, 'dormant_turns', source.owner.dormant_turns - 2)
    )




