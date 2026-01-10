"""
胜地历险记 - DRUID
"""
from ..utils import *


# COMMON

class VAC_508:
    """能量零食 - Trail Mix
    Gain 2 Mana Crystals next turn only.
    下回合获得2个法力水晶（仅限下回合）。
    """
    def play(self):
        # 给玩家添加一个 buff，在下回合开始时获得2点临时法力
        yield Buff(CONTROLLER, "VAC_508e")


class VAC_508e:
    """能量零食效果 (Player Enchantment)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    # 在下回合开始时，给予2点临时法力，然后移除此效果
    events = OWN_TURN_BEGIN.on(
        ManaThisTurn(CONTROLLER, 2),
        Destroy(SELF)
    )


class VAC_518:
    """始祖龟旅行者 - Tortollan Traveler
    [x]Taunt Deathrattle: Draw another Taunt minion. Reduce its Cost by (2).
    嘲讽。亡语：抽一张嘲讽随从牌。使其法力值消耗减少（2）点。
    """
    mechanics = [GameTag.TAUNT, GameTag.DEATHRATTLE]

    def deathrattle(self):
        # 从牌库中抽取一张嘲讽随从
        cards = yield ForceDraw(FRIENDLY_DECK + MINION + TAUNT)
        if cards:
            # 使抽到的卡牌法力值消耗减少2点
            yield Buff(cards[0], "VAC_518e")


class VAC_518e:
    """始祖龟旅行者减费效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    cost = -2


class VAC_950:
    """抱石伙伴 - Bouldering Buddy
    [x]Rush, Taunt Costs (1) if you have at least 10 Mana Crystals.
    突袭，嘲讽。如果你有至少10个法力水晶，则法力值消耗为（1）点。
    """
    mechanics = [GameTag.RUSH, GameTag.TAUNT]

    # 如果玩家有至少10个法力水晶，则费用为1
    cost_mod = Find(Attr(CONTROLLER, GameTag.RESOURCES) >= 10) & SET(1)


class WORK_050:
    """安戈洛宣传单 - Un'Goro Brochure
    [x]Draw two minions. Give them +2/+2. <i>(Flips each turn.)</i>
    抽两张随从牌。使其获得+2/+2。（每回合翻转。）
    """
    def play(self):
        # 从牌库中抽取2张随从牌
        cards = yield ForceDraw(FRIENDLY_DECK + MINION, 2)
        # 给抽到的随从牌+2/+2
        for card in cards:
            yield Buff(card, "WORK_050e")


class WORK_050e:
    """安戈洛宣传单增益效果"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


# RARE

class VAC_511:
    """嗜睡巨龙 - Dozing Dragon
    [x]Dormant for 2 turns. While Dormant, summon a 3/5 Dragon with Taunt  at the end of your turn.
    休眠2回合。休眠状态下，在你的回合结束时，召唤一条3/5并具有嘲讽的龙。
    """
    def play(self):
        yield SetDormant(SELF, 2)
        yield Buff(SELF, "VAC_511e")


class VAC_511e:
    """嗜睡巨龙休眠期间效果"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}
    events = OWN_TURN_END.on(
        Find(Attr(OWNER, GameTag.DORMANT) == 1) & Summon(CONTROLLER, "VAC_511t")
    )


class VAC_517:
    """远足步道 - Hiking Trail
    Discover a Taunt minion. After you gain Armor, reopen this.
    发现一张嘲讽随从牌。在你获得护甲后，重新开启本地标。
    """
    def activate(self):
        # 发现一张嘲讽随从
        yield GenericChoice(CONTROLLER, Discover(CONTROLLER, RandomMinion(taunt=True)))

    # 在获得护甲后，重新开启地标
    events = GainArmor(FRIENDLY_HERO).after(Refresh(SELF, {enums.LOCATION_COOLDOWN: -1}))


class VAC_948:
    """补水区 - Hydration Station
    Resurrect three of your different highest Cost Taunt minions.
    复活三个不同的法力值消耗最高的嘲讽随从。
    """
    def play(self):
        # 从已死亡的嘲讽随从中，选择法力值消耗最高的3个不同随从
        # 使用 DeDuplicate 去重，然后按费用排序，选择前3个
        targets = DeDuplicate(FRIENDLY + KILLED + MINION + TAUNT)
        # 复活3个不同的最高费用嘲讽随从
        yield Summon(CONTROLLER, Copy(RANDOM(targets, card_class=CardClass.INVALID, cost=Count(targets)) * 3))


class WORK_024:
    """蛮熊搬家 - Handle with Bear
    [x]Get two 3/3 Bears with Taunt. Each turn they are in your hand, they gain +1/+1.
    获得两张3/3并具有嘲讽的熊。它们在你的手牌中时，每回合获得+1/+1。
    """
    def play(self):
        # 给玩家2张熊Token
        yield Give(CONTROLLER, "WORK_024t")
        yield Give(CONTROLLER, "WORK_024t")


class WORK_025:
    """数据分析狮 - Number Cruncher
    [x]Rush, Taunt Choose Thrice - Gain +2 Attack; or +2 Health.
    突袭，嘲讽。选择三次：获得+2攻击力；或+2生命值。
    """
    mechanics = [GameTag.RUSH, GameTag.TAUNT]

    play = (
        Choice(CONTROLLER, ["WORK_025a", "WORK_025b"]).then(Battlecry(Choice.CARD, SELF)),
        Choice(CONTROLLER, ["WORK_025a", "WORK_025b"]).then(Battlecry(Choice.CARD, SELF)),
        Choice(CONTROLLER, ["WORK_025a", "WORK_025b"]).then(Battlecry(Choice.CARD, SELF))
    )


class WORK_025a:
    """获得+2攻击力"""
    play = Buff(TARGET, "WORK_025ae")


WORK_025ae = buff(atk=2)


class WORK_025b:
    """获得+2生命值"""
    play = Buff(TARGET, "WORK_025be")


WORK_025be = buff(health=2)


# EPIC

class VAC_907:
    """星夜露宿 - Sleep Under the Stars
    [x]Choose Thrice - Draw 2 cards; Gain 5 Armor; Refresh 3 Mana Crystals.
    选择三次：抽2张牌；获得5点护甲；刷新3个法力水晶。
    """
    play = (
        Choice(CONTROLLER, ["VAC_907a", "VAC_907b", "VAC_907c"]).then(Battlecry(Choice.CARD, None)),
        Choice(CONTROLLER, ["VAC_907a", "VAC_907b", "VAC_907c"]).then(Battlecry(Choice.CARD, None)),
        Choice(CONTROLLER, ["VAC_907a", "VAC_907b", "VAC_907c"]).then(Battlecry(Choice.CARD, None))
    )


class VAC_907a:
    """抽2张牌"""
    play = Draw(CONTROLLER) * 2


class VAC_907b:
    """获得5点护甲"""
    play = GainArmor(FRIENDLY_HERO, 5)


class VAC_907c:
    """刷新3个法力水晶"""
    play = GainMana(CONTROLLER, 3)


class VAC_949:
    """攀上新高 - New Heights
    [x]Increase your maximum Mana by 3 and gain an empty Mana Crystal.
    使你的最大法力值增加3点，并获得一个空的法力水晶。
    """
    def play(self):
        # 增加最大法力值3点
        yield GainEmptyMana(CONTROLLER, 3)


# LEGENDARY

class VAC_506:
    """巡游船长萝拉 - Cruise Captain Lora
    [x]Battlecry: Summon 2 random locations.
    战吼：召唤2个随机地标。
    """
    mechanics = [GameTag.BATTLECRY]

    def play(self):
        # 召唤2个随机地标
        yield Summon(CONTROLLER, RandomCollectible(type=CardType.LOCATION))
        yield Summon(CONTROLLER, RandomCollectible(type=CardType.LOCATION))


class VAC_519:
    """米斯塔·维斯塔 - Mistah Vistah
    [x]Mage Tourist Battlecry: In 3 turns, replay every spell you've cast   between now and then.
    法师游客。战吼：3回合后，重新施放你在此期间施放的所有法术。
    """
    mechanics = [GameTag.BATTLECRY]

    def play(self):
        # 给玩家添加一个 buff，记录施放的法术，并在3回合后重放
        yield Buff(CONTROLLER, "VAC_519e")


class VAC_519e:
    """米斯塔·维斯塔效果 (Player Enchantment)"""
    tags = {GameTag.CARDTYPE: CardType.ENCHANTMENT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spells_cast = []
        self.turns_remaining = 3

    # 记录施放的法术
    events = [
        Play(CONTROLLER, SPELL).after(lambda self, source, card: self.spells_cast.append(card.id)),
        OWN_TURN_END.on(
            lambda self, source: setattr(self, 'turns_remaining', self.turns_remaining - 1) or (
                [Play(CONTROLLER, source.controller.card(spell_id)) for spell_id in self.spells_cast] if self.turns_remaining == 0 else []
            ),
            Find(lambda self: self.turns_remaining == 0) & Destroy(SELF)
        )
    ]
