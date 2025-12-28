from ..utils import *


##
# Minions


class CFM_061:
    """Jinyu Waterspeaker / 锦鱼人水语者
    战吼：恢复#6点生命值。过载：（1）"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 6)


class CFM_312(JadeGolemUtils):
    """Jade Chieftain"""

    play = SummonJadeGolem(CONTROLLER).then(Taunt(SummonJadeGolem.CARD))


class CFM_324:
    """White Eyes / 白眼大侠
    嘲讽，亡语： 将风暴守护者洗入你的牌库。"""

    deathrattle = Shuffle(CONTROLLER, "CFM_324t")


class CFM_697:
    """Lotus Illusionist / 玉莲帮幻术师
    在本随从攻击英雄后，随机变形成为 法力值消耗为（6）的随从。"""

    events = Attack(SELF, ENEMY_HERO).after(Morph(SELF, RandomMinion(cost=6)))


##
# Spells


class CFM_310:
    """Call in the Finishers / 神奇四鱼
    召唤四个1/1的鱼人。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "CFM_310t") * 4


class CFM_313:
    """Finders Keepers / 先到先得
    发现一张具有过载的牌。 过载： （1）"""

    play = DISCOVER(RandomCollectible(card_class=CardClass.SHAMAN, overload=True))


class CFM_696:
    """Devolve / 衰变
    随机将所有 敌方随从变形成为法力值消耗减少（1）点的随从。"""

    requirements = {PlayReq.REQ_HERO_TARGET: 0}
    play = Evolve(ENEMY_MINIONS, -1)


class CFM_707(JadeGolemUtils):
    """Jade Lightning"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 4), SummonJadeGolem(CONTROLLER)


##
# Weapons


class CFM_717(JadeGolemUtils):
    """Jade Claws"""

    play = SummonJadeGolem(CONTROLLER)
