"""
决战荒芜之地 - 中立 - COMMON
"""
from ..utils import *


class DEEP_006:
    """岩石幼龙 - Stone Drake
    Divine Shield, Taunt, Lifesteal, Elusive
    """
    # 2/8 龙 - 圣盾、嘲讽、吸血、扰魔
    divine_shield = True
    taunt = True
    lifesteal = True
    elusive = True


class WW_001:
    """狗头人矿工 - Kobold Miner
    Battlecry: Excavate a treasure.
    """
    # 1/1 战吼：发掘一个宝藏
    play = Excavate(CONTROLLER)


class WW_044:
    """列车机务工 - Tram Mechanic
    Deathrattle: Get a Barrel of Sludge. <i>TOXIC WASTE: Handle with care.</i>
    """
    # 2/1 亡语：获取一桶淤泥
    deathrattle = Give(CONTROLLER, "WW_044t")


class WW_300:
    """陷坑蜘蛛 - Trapdoor Spider
    [x]Stealth, Poisonous After your opponent plays a minion, attack it.
    """
    # 1/2 潜行，剧毒。在你的对手使用一个随从后，攻击它
    stealth = True
    poisonous = True
    events = Play(OPPONENT, MINION).after(Attack(SELF, Play.CARD))


class WW_331:
    """奇迹推销员 - Miracle Salesman
    Deathrattle: Get a Tradeable Snake Oil.
    """
    # 2/2 亡语：获取一张可交易的蛇油
    deathrattle = Give(CONTROLLER, "WW_331t")


class WW_376:
    """仙人掌暴怒者 - Cactus Rager
    Poisonous
    """
    # 5/1 剧毒
    poisonous = True


class WW_383:
    """干鳞警官 - Dryscale Deputy
    Battlecry: The next time you draw a spell, get a copy of it.
    """
    # 2/2 战吼：下一次你抽到一张法术牌时，获取一张它的复制
    play = Buff(CONTROLLER, "WW_383e")


class WW_383e:
    """下次抽法术时复制"""
    events = Draw(CONTROLLER, SPELL).on(
        Give(CONTROLLER, Copy(Draw.CARD)),
        Destroy(SELF)
    )


class WW_391:
    """淘金客 - Gold Panner
    At the end of your turn, draw a card.
    """
    # 1/2 在你的回合结束时，抽一张牌
    events = OWN_TURN_END.on(Draw(CONTROLLER))


class WW_397:
    """炸裂元素 - Dang-Blasted Elemental
    Taunt Deathrattle: Deal 2 damage to all minions except friendly Elementals.
    """
    # 3/3 嘲讽，亡语：对除友方元素以外的所有随从造成2点伤害
    taunt = True
    deathrattle = Hit(ALL_MINIONS - (FRIENDLY_MINIONS + ELEMENTAL), 2)


class WW_398:
    """提灯门卫 - Gaslight Gatekeeper
    [x]Battlecry: Shuffle your hand into your deck, then draw that many cards.
    """
    # 3/4 战吼：将你的手牌洗入牌库，然后抽取等同数量的牌
    def play(self):
        hand_count = len(self.controller.hand)
        # 将手牌洗入牌库
        yield Shuffle(FRIENDLY_HAND)
        # 抽取等同数量的牌
        yield Draw(CONTROLLER) * hand_count


class WW_399:
    """正午决斗者 - High Noon Duelist
    Deathrattle: Both players DRAW! Destroy the card that costs less.
    """
    # 4/3 亡语：双方玩家各抽牌！摧毁其中法力值消耗较低的牌
    def deathrattle(self):
        # 双方各抽一张牌
        friendly_card = yield Draw(CONTROLLER)
        enemy_card = yield Draw(OPPONENT)

        if friendly_card and enemy_card:
            friendly_cost = friendly_card[0].cost if friendly_card else 999
            enemy_cost = enemy_card[0].cost if enemy_card else 999

            # 摧毁费用较低的牌
            if friendly_cost < enemy_cost:
                yield Destroy(friendly_card[0])
            elif enemy_cost < friendly_cost:
                yield Destroy(enemy_card[0])
            # 如果费用相同，都摧毁
            elif friendly_cost == enemy_cost:
                yield Destroy(friendly_card[0])
                yield Destroy(enemy_card[0])


class WW_418:
    """食人魔帮歹徒 - Ogre-Gang Outlaw
    Rush 50% chance to attack the wrong enemy.
    """
    # 4/4 突袭，50%概率攻击错误的敌人
    rush = True
    forgetful = True


class WW_423:
    """沙龙酒仙 - Saloon Brewmaster
    Battlecry: Return a friendly minion to your hand. Give it +2/+2.
    """
    # 2/2 战吼：将一个友方随从移回你的手牌，使其获得+2/+2
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True, PlayReq.REQ_FRIENDLY_TARGET: True, PlayReq.REQ_MINION_TARGET: True}

    def play(self):
        if self.target:
            yield Bounce(TARGET)
            yield Buff(TARGET, "WW_423e")


class WW_423e:
    """+2/+2 增益"""
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CARDTYPE: CardType.ENCHANTMENT
    }


class WW_428:
    """侵蚀沉积岩 - Eroded Sediment
    [x]Battlecry: If you played an Elemental last turn, Discover any Elemental from the past.
    """
    # 4/3 战吼：如果你上回合使用过元素牌，发现一张过去的任意元素牌
    def play(self):
        if self.controller.elemental_played_last_turn > 0:
            # 发现一张元素牌（从过去的卡池中）
            yield GenericChoice(CONTROLLER, RandomCollectible(race=Race.ELEMENTAL, card_set=CardSet.WILD))


class WW_433:
    """排舞的伴侣 - Linedance Partner
    Battlecry: If you're holding another 3-Cost card, summon a random 3-Cost minion.
    """
    # 3/2 战吼：如果你手牌中有其他法力值消耗为3的牌，随机召唤一个法力值消耗为3的随从
    def play(self):
        # 检查手牌中是否有其他费用为3的卡牌
        other_3_cost_cards = [c for c in self.controller.hand if c != self and c.cost == 3]
        if other_3_cost_cards:
            yield Summon(CONTROLLER, RandomMinion(cost=3))


class WW_434:
    """日斑巨龙 - Sunspot Dragon
    [x]Tradeable, Lifesteal Quickdraw: Deal 6 damage.
    """
    # 6/6 可交易，吸血。快枪：造成6点伤害
    lifesteal = True
    tradeable = True
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True}

    def play(self):
        # 快枪：本回合获得并立即使用时触发
        if self.drawn_this_turn and self.target:
            yield Hit(TARGET, 6)


class WW_435:
    """飞踏野兔 - Bunny Stomper
    Your Beasts have Rush.
    """
    # 1/3 你的野兽拥有突袭
    update = Refresh(FRIENDLY_MINIONS + BEAST, {GameTag.RUSH: True})


class WW_827:
    """雏龙牧人 - Whelp Wrangler
    At the end of your turn, get a 1/2 Whelp with Taunt.
    """
    # 2/3 在你的回合结束时，获取一个1/2并具有嘲讽的雏龙
    events = OWN_TURN_END.on(Give(CONTROLLER, "WW_827t"))


class WW_900:
    """蹄铁发射机 - Horseshoe Slinger
    Battlecry: Deal 2 damage to a random enemy minion. Quickdraw: And one of its neighbors.
    """
    # 1/1 战吼：随机对一个敌方随从造成2点伤害。快枪：并对一个相邻随从造成伤害
    def play(self):
        target = yield RandomTarget(ENEMY_MINIONS)
        if target:
            yield Hit(target, 2)

            # 快枪：本回合获得并立即使用时触发
            if self.drawn_this_turn:
                # 对相邻随从造成伤害
                neighbors = target.adjacent_minions
                if neighbors:
                    neighbor = yield RandomTarget(neighbors)
                    if neighbor:
                        yield Hit(neighbor, 2)


class WW_901:
    """贪婪的伴侣 - Greedy Partner
    Battlecry: If you're holding another 2-Cost card, get a Coin.
    """
    # 2/3 战吼：如果你手牌中有其他法力值消耗为2的牌，获取一张幸运币
    def play(self):
        # 检查手牌中是否有其他费用为2的卡牌
        other_2_cost_cards = [c for c in self.controller.hand if c != self and c.cost == 2]
        if other_2_cost_cards:
            yield Give(CONTROLLER, "GAME_005")


class WW_906:
    """吵闹的伴侣 - Rowdy Partner
    Battlecry: If you're holding another 4-Cost card, deal 4 damage.
    """
    # 4/3 战吼：如果你手牌中有其他法力值消耗为4的牌，造成4点伤害
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: True}

    def play(self):
        # 检查手牌中是否有其他费用为4的卡牌
        other_4_cost_cards = [c for c in self.controller.hand if c != self and c.cost == 4]
        if other_4_cost_cards:
            yield Hit(TARGET, 4)


