from ..utils import *


##
# Minions

class SCH_700:
    """Spirit Jailer / 精魂狱卒
    Battlecry: Shuffle 2 Soul Fragments into your deck."""

    # 战吼：将两张灵魂残片洗入你的牌库
    play = Shuffle(CONTROLLER, ["GAME_005"] * 2)


class SCH_147:
    """Boneweb Egg / 骨网之卵
    Deathrattle: Summon two 2/1 Spiders. If you discard this, trigger its Deathrattle."""

    # 亡语：召唤两只2/1的蜘蛛
    deathrattle = Summon(CONTROLLER, "SCH_147t") * 2

    # 如果你弃掉这张牌，触发其亡语
    # 注：InvisibleDeathrattle 机制在 fireplace 中通过 Discard 事件处理


class SCH_147t:
    """Boneweb Spider / 骨网蜘蛛
    2/1 Spider token"""
    # Token: 2/1 蜘蛛（属性在CardDefs.xml中定义）
    pass


class SCH_517:
    """Shadowlight Scholar / 影光学者
    Battlecry: Destroy a Soul Fragment in your deck to deal 3 damage."""

    # 战吼：摧毁一张你牌库中的灵魂残片，造成3点伤害
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }

    # 使用条件效果：如果牌库中有灵魂残片，则移除一张并造成伤害
    play = Find(FRIENDLY_DECK + ID("GAME_005")) & (
        Destroy(RANDOM(FRIENDLY_DECK + ID("GAME_005"))),
        Hit(TARGET, 3)
    )


class SCH_343:
    """Void Drinker / 虚空吸食者
    Taunt. Battlecry: Destroy a Soul Fragment in your deck to gain +3/+3."""

    # 嘲讽（在CardDefs.xml中已定义）
    # 战吼：摧毁一张你牌库中的灵魂残片，获得+3/+3
    play = Find(FRIENDLY_DECK + ID("GAME_005")) & (
        Destroy(RANDOM(FRIENDLY_DECK + ID("GAME_005"))),
        Buff(SELF, "SCH_343e")
    )


SCH_343e = buff(atk=3, health=3)


class SCH_703:
    """Soulciologist Malicia / 灵魂学家玛丽希亚
    Battlecry: For each Soul Fragment in your deck, summon a 3/3 Soul with Rush."""

    def play(self):
        # 计算牌库中灵魂残片的数量
        soul_fragments = self.controller.deck.filter(id="GAME_005")
        count = len(soul_fragments)
        # 为每张灵魂残片召唤一个3/3突袭灵魂
        for _ in range(count):
            yield Summon(CONTROLLER, "SCH_703t")

class SCH_703t:
    """Soul / 灵魂
    3/3 with Rush"""
    # Token: 3/3 突袭灵魂（属性在CardDefs.xml中定义）
    pass


class SCH_181:
    """Archwitch Willow / 高阶女巫维洛
    Battlecry: Summon a random Demon from your hand and deck."""

    def play(self):
        # 从手牌和牌库中随机召唤一个恶魔
        demons = (self.controller.hand + self.controller.deck).filter(race=Race.DEMON)
        if demons:
            demon = random.choice(demons)
            yield Summon(CONTROLLER, demon)


##
# Spells

class SCH_158:
    """Demonic Studies / 恶魔研习
    Discover a Demon. Your next one costs (1) less."""

    # 发现一张恶魔牌。你的下一张恶魔牌法力值消耗减少（1）点
    play = Discover(CONTROLLER, RandomMinion(race=Race.DEMON)), Buff(CONTROLLER, "SCH_158e")


class SCH_158e:
    """Demonic Studies Buff"""
    update = Refresh(FRIENDLY_HAND + MINION + (RACE == Race.DEMON), {GameTag.COST: -1})
    events = Play(FRIENDLY + MINION + (RACE == Race.DEMON)).on(Destroy(SELF))


class SCH_702:
    """Felosophy / 邪能学说
    Copy the lowest Cost Demon in your hand. Outcast: Give both +1/+1."""

    def play(self):
        # 复制你手牌中法力值消耗最低的恶魔牌
        demons = self.controller.hand.filter(race=Race.DEMON)
        if demons:
            # 找到费用最低的恶魔
            lowest_cost_demon = min(demons, key=lambda c: c.cost)
            # 复制该恶魔
            yield Give(CONTROLLER, lowest_cost_demon.id)

            # 流放：使这两张恶魔牌获得+1/+1
            if self.outcast:
                # 给原始恶魔和复制的恶魔都加buff
                yield Buff(lowest_cost_demon, "SCH_702e")
                # 复制的卡牌是手牌中最后一张
                copied_demon = self.controller.hand[-1]
                if copied_demon.id == lowest_cost_demon.id:
                    yield Buff(copied_demon, "SCH_702e")


SCH_702e = buff(atk=1, health=1)


class SCH_701:
    """Soul Shear / 灵魂剥离
    Deal $3 damage to a minion. Shuffle 2 Soul Fragments into your deck."""

    # 对一个随从造成3点伤害。将两张灵魂残片洗入你的牌库
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Shuffle(CONTROLLER, ["GAME_005"] * 2)


class SCH_307:
    """School Spirits / 校园精魂
    Deal $2 damage to all minions. Shuffle 2 Soul Fragments into your deck."""

    # 对所有随从造成2点伤害。将两张灵魂残片洗入你的牌库
    play = Hit(ALL_MINIONS, 2), Shuffle(CONTROLLER, ["GAME_005"] * 2)
