from ..utils import *


##
# Minions

class SCH_242:
    """Gibberling / 叽叽喳喳
    Spellburst: Summon a Gibberling.
    法术迸发：召唤一个叽叽喳喳。"""

    # 2费 1/1 法术迸发：召唤一个叽叽喳喳
    spellburst = Summon(CONTROLLER, "SCH_242")


class SCH_613:
    """Groundskeeper / 园丁
    Taunt Battlecry: If you're holding a spell that costs (5) or more, restore 5 Health.
    嘲讽 战吼：如果你的手牌中有一张法力值消耗大于或等于5的法术牌，恢复5点生命值。"""

    # 4费 4/5 嘲讽 战吼：如果你的手牌中有一张法力值消耗大于或等于5的法术牌，恢复5点生命值
    # 嘲讽通过 CardDefs.xml 中的 TAUNT 标签定义
    play = Find(FRIENDLY_HAND + SPELL + (COST >= 5)) & Heal(FRIENDLY_HERO, 5)


class SCH_616:
    """Twilight Runner / 暮光奔行者
    Stealth Whenever this attacks, draw 2 cards.
    潜行 每当该随从攻击时，抽2张牌。"""

    # 5费 5/4 潜行 每当该随从攻击时，抽2张牌
    # 潜行通过 CardDefs.xml 中的 STEALTH 标签定义
    events = Attack(SELF).after(Draw(CONTROLLER) * 2)


class SCH_614:
    """Forest Warden Omu / 森林守护者奥姆
    Spellburst: Refresh your Mana Crystals.
    法术迸发：刷新你的法力水晶。"""

    # 6费 5/4 传说 法术迸发：刷新你的法力水晶
    spellburst = ManaThisTurn(CONTROLLER, FULL_MANA_CRYSTALS(CONTROLLER))


##
# Spells

class SCH_427:
    """Lightning Bloom / 闪电绽放
    Refresh 2 Mana Crystals. Overload: (2)
    刷新2个法力水晶。过载：（2）"""

    # 0费 刷新2个法力水晶。过载：（2）
    play = ManaThisTurn(CONTROLLER, 2)


class SCH_333:
    """Nature Studies / 自然研习
    Discover a spell. Your next one costs (1) less.
    发现一张法术牌。你的下一张法术牌法力值消耗减少（1）点。"""

    # 1费 发现一张法术牌。你的下一张法术牌法力值消耗减少（1）点
    play = Discover(CONTROLLER, RandomSpell()), Buff(CONTROLLER, "SCH_333e")


class SCH_333e:
    """Nature Studies Buff"""
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = Play(FRIENDLY + SPELL).on(Destroy(SELF))


class SCH_606:
    """Partner Assignment / 搭档作业
    Add a random 2-Cost and 3-Cost Beast to your hand.
    将一张随机的2费和3费野兽牌加入你的手牌。"""

    # 1费 将一张随机的2费和3费野兽牌加入你的手牌
    play = Give(CONTROLLER, RandomMinion(cost=2, race=Race.BEAST)), Give(CONTROLLER, RandomMinion(cost=3, race=Race.BEAST))


class SCH_612:
    """Runic Carvings / 符文雕刻
    Choose One - Summon four 2/2 Treant Totems; or Overload: (2) to summon them with Rush.
    抉择：召唤四个2/2的树人图腾；或者过载：（2）召唤四个具有突袭的树人图腾。"""

    # 6费 抉择：召唤四个2/2的树人图腾；或者过载：（2）召唤四个具有突袭的树人图腾
    choose = ["SCH_612a", "SCH_612b"]


class SCH_609:
    """Survival of the Fittest / 适者生存
    Give +4/+4 to all minions in your hand, deck, and battlefield.
    使你的手牌、牌库和战场上的所有随从获得+4/+4。"""

    # 10费 使你的手牌、牌库和战场上的所有随从获得+4/+4
    play = Buff(FRIENDLY_HAND + MINION, "SCH_609e"), Buff(FRIENDLY_DECK + MINION, "SCH_609e"), Buff(FRIENDLY_MINIONS, "SCH_609e")


SCH_609e = buff(atk=4, health=4)

