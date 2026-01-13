from ..utils import *


##
# Minions

class SCH_538:
    """Ace Hunter Kreen / 金牌猎手克里
    Your other characters are Immune while attacking."""

    # 你的其他角色在攻击时免疫
    class Hand:
        events = Attack(FRIENDLY - SELF).on(
            Buff(Attack.ATTACKER, "SCH_538e")
        )


class SCH_538e:
    """Immune while attacking"""
    tags = {GameTag.IMMUNE_WHILE_ATTACKING: True}
    events = Attack(OWNER).after(Destroy(SELF))


class SCH_276:
    """Magehunter / 法师猎手
    Rush Whenever this attacks a minion, Silence it."""

    # 突袭（在CardDefs.xml中已定义）
    # 每当本随从攻击一个随从时，将其沉默
    events = Attack(SELF, MINION).after(Silence(Attack.DEFENDER))


class SCH_355:
    """Shardshatter Mystic / 残片震爆秘术师
    Battlecry: Destroy a Soul Fragment in your deck to deal 3 damage to all other minions."""

    # 战吼：摧毁一张你牌库中的灵魂残片，对所有其他随从造成3点伤害
    # 使用条件效果：如果牌库中有灵魂残片，则移除一张并造成伤害
    play = Find(FRIENDLY_DECK + ID("GAME_005")) & (
        Destroy(RANDOM(FRIENDLY_DECK + ID("GAME_005"))),
        Hit(ALL_MINIONS - SELF, 3)
    )


class SCH_603:
    """Star Student Stelina / 明星学员斯特里娜
    Outcast: Look at 3 cards in your opponent's hand. Shuffle one of them into their deck."""

    # 流放：检视对手的三张手牌，将其中一张洗入对手的牌库
    # 完整实现：使用 GenericChoice 让玩家查看并选择
    def play(self):
        if self.outcast:
            opponent_hand = list(self.controller.opponent.hand)
            if opponent_hand:
                # 随机选择最多3张牌让玩家查看
                import random
                cards_to_show = random.sample(opponent_hand, min(3, len(opponent_hand)))
                
                # 让玩家从这3张牌中选择一张洗入对手牌库
                choice = yield GenericChoice(
                    self.controller, cards_to_show
                )
                
                if choice:
                    card_to_shuffle = choice[0]
                    yield Shuffle(self.controller.opponent, card_to_shuffle)


class SCH_705:
    """Vilefiend Trainer / 邪犬训练师
    Outcast: Summon two 1/1 Demons."""

    def play(self):
        if self.outcast:
            # 召唤两个1/1的恶魔
            yield Summon(CONTROLLER, "SCH_705t") * 2


class SCH_705t:
    """Vilefiend / 邪犬
    1/1 Demon token"""
    # Token: 1/1 恶魔（属性在CardDefs.xml中定义）
    pass


class SCH_618:
    """Blood Herald / 嗜血传令官
    Whenever a friendly minion dies while this is in your hand, gain +1/+1."""

    # 如果这张牌在你的手牌中，每当一个友方随从死亡，便获得+1/+1
    class Hand:
        events = Death(FRIENDLY + MINION).on(Buff(SELF, "SCH_618e"))


SCH_618e = buff(atk=1, health=1)


class SCH_704:
    """Soulshard Lapidary / 铸魂宝石匠
    Battlecry: Destroy a Soul Fragment in your deck to give your hero +5 Attack this turn."""

    # 战吼：摧毁一张你牌库中的灵魂残片，在本回合中使你的英雄获得+5攻击力
    play = Find(FRIENDLY_DECK + ID("GAME_005")) & (
        Destroy(RANDOM(FRIENDLY_DECK + ID("GAME_005"))),
        Buff(FRIENDLY_HERO, "SCH_704e")
    )


class SCH_704e:
    """Soulshard Lapidary Buff"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 5,
    }
    events = TURN_END.on(Destroy(SELF))


class SCH_354:
    """Ancient Void Hound / 上古虚空恶犬
    At the end of your turn, steal 1 Attack and Health from all enemy minions."""

    # 在你的回合结束时，从所有敌方随从处偷取1点攻击力和生命值
    events = OWN_TURN_END.on(
        Buff(SELF, "SCH_354e", atk=Count(ENEMY_MINIONS), health=Count(ENEMY_MINIONS)),
        Buff(ENEMY_MINIONS, "SCH_354e2")
    )


class SCH_354e:
    """Ancient Void Hound Buff (Gain)"""
    atk = lambda self, i: self.atk
    max_health = lambda self, i: self.max_health


SCH_354e2 = buff(atk=-1, health=-1)


##
# Spells

class SCH_600:
    """Demon Companion / 恶魔伙伴
    Summon a random Demon Companion."""

    # 随机召唤一个恶魔伙伴
    play = Summon(CONTROLLER, RandomCollectible(race=Race.DEMON, card_class=CardClass.DEMONHUNTER, cost=1))


class SCH_422:
    """Double Jump / 二段跳
    Draw an Outcast card from your deck."""

    def play(self):
        # 从你的牌库中抽一张流放牌
        outcast_cards = self.controller.deck.filter(outcast=True)
        if outcast_cards:
            yield Draw(CONTROLLER, outcast_cards[0])


class SCH_356:
    """Glide / 滑翔
    Shuffle your hand into your deck. Draw 4 cards. Outcast: Your opponent does the same."""

    def play(self):
        # 将你的手牌洗入你的牌库，抽四张牌
        for card in list(self.controller.hand):
            yield Shuffle(CONTROLLER, card)
        yield Draw(CONTROLLER) * 4

        # 流放：使你的对手做出相同行为
        if self.outcast:
            for card in list(self.controller.opponent.hand):
                yield Shuffle(self.controller.opponent, card)
            yield Draw(self.controller.opponent) * 4


class SCH_253:
    """Cycle of Hatred / 仇恨之轮
    Deal $3 damage to all minions. Summon a 3/3 Spirit for every minion killed."""

    def play(self):
        # 对所有随从造成3点伤害
        minions_before = len(self.game.board)
        yield Hit(ALL_MINIONS, 3)
        # 每消灭一个随从，召唤一个3/3的怨魂
        minions_after = len(self.game.board)
        killed = minions_before - minions_after
        for _ in range(killed):
            yield Summon(CONTROLLER, "SCH_253t")


class SCH_253t:
    """Wrathspike / 怨魂
    3/3 Spirit token"""
    # Token: 3/3 怨魂（属性在CardDefs.xml中定义）
    pass


class SCH_357:
    """Fel Guardians / 邪能护卫
    Summon three 1/2 Demons with Taunt. Costs (1) less whenever a friendly minion dies."""

    # 召唤三个1/2并具有嘲讽的恶魔
    play = Summon(CONTROLLER, "SCH_357t") * 3

    # 每当一个友方随从死亡，本牌的法力值消耗便减少（1）点
    class Hand:
        events = Death(FRIENDLY + MINION).on(Buff(SELF, "SCH_357e"))


class SCH_357e:
    """Fel Guardians Cost Reduction"""
    tags = {GameTag.COST: -1}


class SCH_357t:
    """Fel Guardian / 邪能护卫
    1/2 Demon with Taunt"""
    # Token: 1/2 嘲讽恶魔（属性在CardDefs.xml中定义）
    pass


##
# Weapons

class SCH_279:
    """Trueaim Crescent / 引月长弓
    After your Hero attacks a minion, your minions attack it too."""

    # 在你的英雄攻击一个随从后，你的所有随从也会攻击该随从
    events = Attack(FRIENDLY_HERO, MINION).after(
        lambda self, card: [Attack(minion, target) for minion in source.controller.field]
    )


class SCH_252:
    """Marrowslicer / 切髓之刃
    Battlecry: Shuffle 2 Soul Fragments into your deck."""

    # 战吼：将两张灵魂残片洗入你的牌库
    play = Shuffle(CONTROLLER, ["GAME_005"] * 2)
