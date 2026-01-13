from ..utils import *


##
# Minions

class SCH_317:
    """Playmaker / 战术大师
    After you play a Rush minion, summon a copy with 1 Health remaining.
    在你打出一张突袭随从后，召唤一个生命值为1的复制。"""

    # 3费 3/3 在你打出一张突袭随从后，召唤一个生命值为1的复制
    events = Play(CONTROLLER, MINION + RUSH).after(
        Summon(CONTROLLER, ExactCopy(Play.CARD)).then(SetCurrentHealth(Summon.CARD, 1))
    )


class SCH_337:
    """Troublemaker / 麻烦制造者
    At the end of your turn, summon two 3/3 Ruffians that attack random enemies.
    在你的回合结束时，召唤两个3/3的恶棍，攻击随机敌人。"""

    # 8费 6/8 在你的回合结束时，召唤两个3/3的恶棍，攻击随机敌人
    events = OWN_TURN_END.on(Summon(CONTROLLER, "SCH_337t") * 2)


class SCH_621:
    """Rattlegore / 骸骨之王
    Deathrattle: Resummon this with -1/-1.
    亡语：重新召唤该随从，并使其-1/-1。"""

    # 9费 9/9 传说 亡语：重新召唤该随从，并使其-1/-1
    deathrattle = Summon(CONTROLLER, "SCH_621").then(
        Buff(Summon.CARD, "SCH_621e")
    )


class SCH_621e:
    """Rattlegore Debuff - -1/-1"""
    tags = {
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.ATK: -1,
        GameTag.HEALTH: -1,
    }


##
# Spells

class SCH_237:
    """Athletic Studies / 体育研习
    Discover a Rush minion. Your next one costs (1) less.
    发现一张突袭随从牌。你的下一张突袭随从牌法力值消耗减少（1）点。"""

    # 1费 发现一张突袭随从牌。你的下一张突袭随从牌法力值消耗减少（1）点
    play = Discover(CONTROLLER, RandomMinion(rush=True)), Buff(CONTROLLER, "SCH_237e")


class SCH_237e:
    """Athletic Studies Buff"""
    update = Refresh(FRIENDLY_HAND + MINION + RUSH, {GameTag.COST: -1})
    events = Play(FRIENDLY + MINION + RUSH).on(Destroy(SELF))


class SCH_525:
    """In Formation! / 列队前进！
    Add 2 random Taunt minions to your hand.
    将2张随机嘲讽随从牌加入你的手牌。"""

    # 2费 将2张随机嘲讽随从牌加入你的手牌
    play = Give(CONTROLLER, RandomMinion(taunt=True)) * 2


##
# Weapons

class SCH_238:
    """Reaper's Scythe / 收割者镰刀
    Spellburst: Also damages adjacent minions this turn.
    法术迸发：本回合同时对相邻的随从造成伤害。"""

    # 4费 4/2 武器 法术迸发：本回合同时对相邻的随从造成伤害
    spellburst = Buff(SELF, "SCH_238e")


class SCH_238e:
    """Reaper's Scythe Cleave Buff"""
    # 在英雄攻击随从后，对相邻的随从造成伤害
    events = Attack(FRIENDLY_HERO, MINION).after(
        lambda self, card: [
            Hit(adj, source.atk) for adj in target.adjacent_minions
        ]
    )
    # 回合结束时移除效果
    events = TURN_END.on(Destroy(SELF))
