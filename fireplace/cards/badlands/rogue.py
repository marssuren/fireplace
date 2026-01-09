"""
决战荒芜之地 - ROGUE
"""
from ..utils import *


# COMMON

class DEEP_014:
    """疾速矿锄 - Quick Pick
    After your hero attacks, draw a card.
    在你的英雄攻击后，抽一张牌。
    """
    # Type: WEAPON | Cost: 2 | Rarity: COMMON | Stats: 1/2 | Mechanics: TRIGGER_VISUAL
    # 英雄攻击后抽牌
    events = Attack(FRIENDLY_HERO).after(Draw(CONTROLLER))


class WW_410:
    """三条七 - Triple Sevens
    Deal $7 damage to a minion. Draw 7 cards.
    对一个随从造成$7点伤害。抽7张牌。
    """
    # Type: SPELL | Cost: 7 | Rarity: COMMON
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: True, PlayReq.REQ_MINION_TARGET: True}

    def play(self):
        # 对目标造成7点伤害
        yield Hit(TARGET, 7)
        # 抽7张牌
        yield Draw(CONTROLLER) * 7


class WW_411:
    """持枪要挟 - Stick Up
    [x]Discover a Quickdraw card from another class.
    发现一张另一职业的快枪牌。
    """
    # Type: SPELL | Cost: 1 | Rarity: COMMON | Mechanics: DISCOVER

    def play(self):
        # 发现一张其他职业的快枪牌
        # 使用 mechanics 参数过滤快枪牌
        yield Discover(CONTROLLER, RandomCollectible(
            card_class=ANOTHER_CLASS,
            mechanics=GameTag.QUICKDRAW
        )).then(Give(CONTROLLER, Discover.CARD))


class WW_412:
    """血石牌铁铲 - Bloodrock Co. Shovel
    Deathrattle: Excavate a treasure.
    亡语：发掘一个宝藏。
    """
    # Type: WEAPON | Cost: 1 | Rarity: COMMON | Stats: 1/3 | Mechanics: DEATHRATTLE, EXCAVATE

    deathrattle = Excavate(CONTROLLER)


# RARE

class DEEP_022:
    """愚人金 - Fool's Gold
    Get a random Golden Pirate and Elemental from other classes.
    随机获取其他职业的金色海盗牌和元素牌各一张。
    """
    # Type: SPELL | Cost: 1 | Rarity: RARE

    def play(self):
        # 获取一张其他职业的金色海盗牌
        pirate = RandomCollectible(card_class=ANOTHER_CLASS, race=Race.PIRATE).evaluate(self)
        if pirate:
            yield Give(CONTROLLER, pirate).then(SetTag(Give.CARD, {GameTag.PREMIUM: True}))

        # 获取一张其他职业的金色元素牌
        elemental = RandomCollectible(card_class=ANOTHER_CLASS, race=Race.ELEMENTAL).evaluate(self)
        if elemental:
            yield Give(CONTROLLER, elemental).then(SetTag(Give.CARD, {GameTag.PREMIUM: True}))


class WW_363:
    """押注猎手 - Bounty Wrangler
    快枪或连击：获取一张幸运币。
    """
    # Type: MINION | Cost: 3 | Rarity: RARE | Stats: 3/3 | Mechanics: COMBO: QUICKDRAW
    
    def play(self):
        # 快枪或连击：满足任一条件即可获得幸运币
        if self.drawn_this_turn or self.controller.cards_played_this_turn > 0:
            yield Give(CONTROLLER, "GAME_005")  # 幸运币


class WW_413:
    """古董投手 - Antique Flinger
    Battlecry: If you've Excavated twice, destroy an enemy minion.
    战吼：如果你已发掘过两次，消灭一个敌方随从。
    """
    # Type: MINION | Cost: 3 | Rarity: RARE | Stats: 4/3 | Mechanics: BATTLECRY
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True, PlayReq.REQ_ENEMY_TARGET: True, PlayReq.REQ_MINION_TARGET: True}

    def play(self):
        # 检查是否已发掘过至少2次
        if self.controller.times_excavated >= 2:
            if self.target:
                yield Destroy(TARGET)


class WW_416:
    """龟壳游戏 - Shell Game
    [x]Get a random Epic, Rare, and Common card from other classes.
    随机获取其他职业的史诗，稀有和普通卡牌各一张。
    """
    # Type: SPELL | Cost: 2 | Rarity: RARE

    def play(self):
        # 获取一张其他职业的史诗牌
        yield Give(CONTROLLER, RandomCollectible(
            card_class=ANOTHER_CLASS,
            rarity=Rarity.EPIC
        ))
        # 获取一张其他职业的稀有牌
        yield Give(CONTROLLER, RandomCollectible(
            card_class=ANOTHER_CLASS,
            rarity=Rarity.RARE
        ))
        # 获取一张其他职业的普通牌
        yield Give(CONTROLLER, RandomCollectible(
            card_class=ANOTHER_CLASS,
            rarity=Rarity.COMMON
        ))


# EPIC

class WW_006:
    """飞镖投掷 - Dart Throw
    [x]Throw two $2 damage darts at random enemy minions. <i>(If both hit the same minion, get a Coin!)</i>
    随机向敌方随从投掷两枚造成$2点伤害的飞镖。（如果两枚击中同一个随从，获得一张幸运币！）
    """
    # Type: SPELL | Cost: 2 | Rarity: EPIC

    def play(self):
        # 投掷第一枚飞镖
        target1 = yield RandomTarget(ENEMY_MINIONS)
        if target1:
            yield Hit(target1, 2)

            # 投掷第二枚飞镖
            target2 = yield RandomTarget(ENEMY_MINIONS)
            if target2:
                yield Hit(target2, 2)

                # 如果两枚飞镖击中同一个随从，获得幸运币
                if target1 == target2:
                    yield Give(CONTROLLER, "GAME_005")  # 幸运币


class WW_415:
    """许愿井 - Wishing Well
    [x]After you play a Coin, get a random Legendary minion from another class and set its Cost to (1).
    在你使用一张幸运币后，随机获取一张另一职业的传说随从牌并将其法力值消耗变为（1）点。
    """
    # Type: MINION | Cost: 5 | Rarity: EPIC | Stats: 0/7 | Mechanics: TRIGGER_VISUAL

    # 监听使用幸运币（GAME_005）
    events = Play(CONTROLLER, "GAME_005").after(
        Give(CONTROLLER, RandomLegendaryMinion(card_class=ANOTHER_CLASS)).then(
            Buff(Give.CARD, "WW_415e")
        )
    )


class WW_415e:
    """许愿井增益 - 设置费用为1"""
    tags = {GameTag.COST: 1}


# LEGENDARY

class WW_364:
    """威拉罗克·温布雷 - Velarok Windblade
    [x]While this is in your hand, play a card from another class to reveal Velarok's true form!
    当本牌在你手牌中时，使用一张另一职业的卡牌以揭示威拉罗克的真正形态！
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 3/3

    class Hand:
        # 监听使用卡牌事件，检查是否为其他职业的卡牌
        # 使用自定义函数来检查卡牌职业
        def _check_and_morph(self, source):
            """检查使用的卡牌是否来自其他职业，如果是则变形"""
            # Play.CARD 在事件触发时会被设置为使用的卡牌
            played_card = Play.CARD.eval(source.game, source)[0] if Play.CARD.eval(source.game, source) else None
            if played_card:
                # 检查卡牌职业是否与英雄职业不同
                # 中立卡牌 (NEUTRAL) 不算其他职业
                hero_class = source.controller.hero.card_class
                card_class = played_card.card_class

                if card_class != CardClass.NEUTRAL and card_class != hero_class:
                    yield Morph(SELF, "WW_364t")

        events = Play(CONTROLLER).after(_check_and_morph)


class WW_364t:
    """威拉罗克·温布雷（真实形态） - Velarok Windblade (True Form)
    Charge. After this attacks, Discover a card from another class. It costs (3) less.
    冲锋。在本随从攻击后，发现一张另一职业的卡牌，其法力值消耗减少（3）点。
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 4/4 | Race: DRAGON | Mechanics: CHARGE
    tags = {
        GameTag.CHARGE: True,
        GameTag.CARDRACE: Race.DRAGON,
    }

    # 攻击后触发：发现一张其他职业的卡牌并减少3费
    events = Attack(SELF).after(
        Discover(CONTROLLER, RandomCollectible(card_class=ANOTHER_CLASS)).then(
            Buff(Discover.CARD, "WW_364t_e")
        )
    )


class WW_364t_e:
    """威拉罗克真实形态增益 - 减少3费"""
    tags = {GameTag.COST: -3}


class WW_417:
    """钻头小子 - Drilly the Kid
    战吼、快枪和亡语：发掘一个宝藏。
    """
    # Type: MINION | Cost: 3 | Rarity: LEGENDARY | Stats: 2/4 | Mechanics: BATTLECRY, DEATHRATTLE, EXCAVATE, QUICKDRAW
    
    def play(self):
        # 战吼：发掘一个宝藏
        yield Excavate(CONTROLLER)
        
        # 快枪：本回合获得并立即使用时，额外发掘一个宝藏
        if self.drawn_this_turn:
            yield Excavate(CONTROLLER)
    
    def deathrattle(self):
        # 亡语：发掘一个宝藏
        yield Excavate(CONTROLLER)


