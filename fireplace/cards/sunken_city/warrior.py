# -*- coding: utf-8 -*-
"""
探寻沉没之城（Voyage to the Sunken City）- 战士
"""

from ..utils import *

class TID_714:
    """火成熔岩吞食者 - 4费 3/5
    嘲讽。战吼：探底。获得等同于选中的牌的法力值消耗的护甲值"""
    tags = {GameTag.TAUNT: True}
    play = (Dredge(CONTROLLER), GainArmor(CONTROLLER, COST(DREDGED_CARD)))


class TID_715:
    """巨型剧斗 - 3费法术
    随机将一张巨型随从牌置入双方玩家的手牌。你的那张法力值消耗减少（2）点"""
    play = (
        Give(CONTROLLER, RandomMinion(tag=GameTag.COLOSSAL)),
        Buff(LAST_GIVEN, "TID_715e"),
        Give(OPPONENT, RandomMinion(tag=GameTag.COLOSSAL))
    )


class TID_715e:
    """巨型减费"""
    tags = {GameTag.COST: -2}


class TID_716:
    """潮汐亡魂 - 8费 5/8
    战吼：造成5点伤害。获得8点护甲值"""
    play = (Hit(TARGET, 5), GainArmor(FRIENDLY_HERO, 8))


class TSC_659:
    """海沟追猎者 - 9费 8/9
    战吼：随机攻击三个不同的敌人"""
    play = (
        Attack(SELF, RANDOM(ALL_ENEMIES)),
        Attack(SELF, RANDOM(ALL_ENEMIES)),
        Attack(SELF, RANDOM(ALL_ENEMIES))
    )


class TSC_660:
    """奈利，超巨蛇颈龙 - 7费 5/5
    巨型+1。战吼：发现三个海盗来构成奈利的船员团队"""
    colossal_appendages = ["TSC_660t"]
    play = (
        Discover(CONTROLLER, RandomMinion(race=Race.PIRATE)) * 3
    )


class TSC_913:
    """艾萨拉的三叉戟 - 3费 3/2武器
    亡语：将一张\"沉没的三叉戟\"置于你的牌库底"""
    deathrattle = ShuffleIntoDeck(CONTROLLER, "TSC_913t", position='bottom')


class TSC_917:
    """黑鳞蛮兵 - 7费 5/6
    嘲讽。战吼：如果你装备着武器，召唤一个5/6并具有突袭的纳迦"""
    tags = {GameTag.TAUNT: True}
    play = (Find(FRIENDLY_WEAPON), Summon(CONTROLLER, "TSC_917t"))


class TSC_939:
    """火焰熔铸 - 2费法术
    摧毁你的武器，然后抽数量等同于其攻击力的牌"""
    def play(self):
        # 摧毁武器，抽等同于其攻击力的牌
        if self.controller.weapon:
            atk = self.controller.weapon.atk
            yield Destroy(self.controller.weapon)
            for _ in range(atk):
                yield Draw(CONTROLLER)


class TSC_940:
    """深海来客 - 3费法术
    使你牌库底五张牌的法力值消耗减少（3）点，然后探底"""
    play = (
        Buff(FRIENDLY_DECK[-5:], "TSC_940e"),
        Dredge(CONTROLLER)
    )


class TSC_940e:
    """深渊减费"""
    tags = {GameTag.COST: -3}


class TSC_941:
    """保卫城市 - 2费法术
    获得3点护甲值。召唤一个2/3并具有嘲讽的纳迦"""
    play = (GainArmor(CONTROLLER, 3), Summon(CONTROLLER, "TSC_941t"))


class TSC_942:
    """黑曜石铸匠 - 2费 3/2
    战吼：探底。如果选中的是随从牌或武器牌，则使其获得+1/+1"""
    play = (
        Dredge(CONTROLLER),
        Find(DREDGED_CARD + (MINION | WEAPON)) & Buff(DREDGED_CARD, "TSC_942e")
    )


class TSC_942e:
    """黑曜石增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_943:
    """艾什凡女勋爵 - 5费 5/5
    战吼：使你手牌，牌库和战场上的所有武器获得+1/+1"""
    play = (Buff(FRIENDLY_HAND + WEAPON, "TSC_943e"), Buff(FRIENDLY_DECK + WEAPON, "TSC_943e"), Buff(FRIENDLY_WEAPON, "TSC_943e"))


class TSC_943e:
    """武器增益"""
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1}


class TSC_944:
    """辛艾萨莉之火 - 2费法术
    将你牌库里的所有卡牌替换成法力值消耗大于或等于（5）点的随从牌。替换后的牌法力值消耗为（5）点"""
    def play(self):
        # 将牌库所有牌替换成5费以上随从
        deck_size = len(self.controller.deck)
        # 清空牌库
        for card in list(self.controller.deck):
            yield Destroy(card)
        # 加入随机高费随从
        for _ in range(deck_size):
            yield Shuffle(CONTROLLER, RandomMinion(cost_min=5))
        # 设置费用为5
        yield Buff(FRIENDLY_DECK, "TSC_944e")


class TSC_944e:
    """津艾萨里之火"""
    tags = {GameTag.COST: 5}
