from ..utils import *


##
# Minions


class CFM_060:
    """Red Mana Wyrm / 猩红法力浮龙
    每当你施放一个法术，便获得 +2攻击力。"""

    events = OWN_SPELL_PLAY.on(Buff(SELF, "CFM_060e"))


CFM_060e = buff(atk=2)


class CFM_063:
    """Kooky Chemist / 化学怪人
    战吼： 使一个随从的攻击力和生命值互换。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Buff(TARGET, "CFM_063e")


CFM_063e = AttackHealthSwapBuff()


class CFM_067:
    """Hozen Healer / 猢狲医者
    战吼：为一个随从恢复所有生命值。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Heal(TARGET, MAX_HEALTH(TARGET))


class CFM_120:
    """Mistress of Mixtures / 亡灵药剂师
    亡语：为每个英雄恢复#4点生命值。"""

    deathrattle = Heal(ALL_HEROES, 4)


class CFM_619:
    """Kabal Chemist / 暗金教炼金师
    战吼：随机将一张药水牌置入你的手牌。"""

    play = Give(CONTROLLER, RandomPotion())


class CFM_646:
    """Backstreet Leper / 后街男巫
    亡语：对敌方英雄造成2点伤害。"""

    deathrattle = Hit(ENEMY_HERO, 2)


class CFM_647:
    """Blowgill Sniper / 吹箭鱼人
    战吼：造成1点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1)


class CFM_648:
    """Big-Time Racketeer / 犯罪高手
    战吼：召唤一个6/6的食人魔。"""

    play = Summon(CONTROLLER, "CFM_648t")


class CFM_651:
    """Naga Corsair / 纳迦海盗
    战吼：使你的武器获得+1攻击力。"""

    play = Buff(FRIENDLY_WEAPON, "CFM_651e")


CFM_651e = buff(atk=1)


class CFM_654:
    """Friendly Bartender / 热心的酒保
    在你的回合结束时，为你的英雄恢复#1点生命值。"""

    events = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 1))


class CFM_655:
    """Toxic Sewer Ooze / 毒性污水软泥怪
    战吼：使对手的武器失去1点耐久度。"""

    play = Hit(ENEMY_WEAPON, 1)


class CFM_656:
    """Streetwise Investigator / 街头调查员
    战吼：使所有敌方随从失去潜行。"""

    play = Unstealth(ENEMY_MINIONS)


class CFM_659:
    """Gadgetzan Socialite / 加基森名媛
    战吼： 恢复#2点生命值。"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Heal(TARGET, 2)


class CFM_715(JadeGolemUtils):
    """Jade Spirit"""

    play = SummonJadeGolem(CONTROLLER)


class CFM_809:
    """Tanaris Hogchopper / 野猪骑士塔纳利
    战吼：如果你的对手没有手牌，便获得 冲锋。"""

    play = Find(ENEMY_HAND) | GiveCharge(SELF)


class CFM_851:
    """Daring Reporter / 勇敢的记者
    每当你的对手抽一张牌时，便获得+1/+1。"""

    events = Draw(OPPONENT).on(Buff(SELF, "CFM_851e"))


CFM_851e = buff(+1, +1)


class CFM_853:
    """Grimestreet Smuggler / 污手街走私者
    战吼：随机使你手牌中的一张随从牌获得+1/+1。"""

    play = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_853e")


CFM_853e = buff(+1, +1)
