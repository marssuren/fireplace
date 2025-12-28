from ..utils import *


##
# Minions


class ULD_174:
    """Serpent Egg / 海蛇蛋
    亡语：召唤一条3/4的海蛇。"""

    # <b>Deathrattle:</b> Summon a 3/4 Sea Serpent.
    deathrattle = Summon(CONTROLLER, "ULD_174t")


class ULD_179:
    """Phalanx Commander / 方阵指挥官
    你的嘲讽随从拥有+2攻击力。"""

    # Your <b>Taunt</b> minions have +2 Attack.
    update = Refresh(FRIENDLY_MINIONS + TAUNT, {GameTag.ATK: +2})


class ULD_182:
    """Spitting Camel / 乱喷的骆驼
    在你的回合结束时，随机对另一个友方随从造成1点伤害。"""

    # [x]At the end of your turn, __deal 1 damage to another__ random friendly minion.
    events = OWN_TURN_END.on(Hit(RANDOM_OTHER_FRIENDLY_MINION, 1))


class ULD_183:
    """Anubisath Warbringer / 阿努比萨斯战争使者
    亡语：使你手牌中的所有随从牌获得+3/+3。"""

    # <b>Deathrattle:</b> Give all minions in your hand +3/+3.
    deathrattle = Buff(FRIENDLY_HAND + MINION, "ULD_183e")


ULD_183e = buff(+3, +3)


class ULD_184:
    """Kobold Sandtrooper / 狗头人沙漠步兵
    亡语：对敌方英雄造成3点伤害。"""

    # <b>Deathrattle:</b> Deal 3 damage to the enemy_hero.
    deathrattle = Hit(ENEMY_HERO, 3)


class ULD_185:
    """Temple Berserker / 神殿狂战士
    复生 受伤时拥有+2 攻击力。"""

    # <b>Reborn</b> Has +2 Attack while damaged.
    enrage = Refresh(SELF, buff="ULD_185e")


ULD_185e = buff(atk=2)


class ULD_188:
    """Golden Scarab / 金甲虫
    战吼：发现一张 法力值消耗为（4）的卡牌。"""

    # <b><b>Battlecry:</b> Discover</b> a 4-Cost card.
    play = DISCOVER(RandomCollectible(cost=4))


class ULD_189:
    """Faceless Lurker / 无面潜伏者
    嘲讽。战吼：将本随从的生命值翻倍。"""

    # <b>Taunt</b> <b>Battlecry:</b> Double this minion's Health.
    play = Buff(SELF, "ULD_189e")


class ULD_189e:
    def apply(self, target):
        self._xhealth = target.health * 2

    max_health = lambda self, _: self._xhealth


class ULD_190:
    """Pit Crocolisk / 深坑鳄鱼
    战吼：造成5点伤害。"""

    # <b>Battlecry:</b> Deal 5 damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 5)


class ULD_191:
    """Beaming Sidekick / 欢快的同伴
    战吼：使一个友方随从获得+2生命值。"""

    # <b>Battlecry:</b> Give a friendly minion +2 Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ULD_191e")


ULD_191e = buff(health=2)


class ULD_271:
    """Injured Tol'vir / 受伤的托维尔人
    嘲讽。战吼：对本随从造成3点伤害。"""

    # <b>Taunt</b> <b>Battlecry:</b> Deal 3 damage to this minion.
    play = Hit(SELF, 3)


class ULD_282:
    """Jar Dealer / 陶罐商人
    亡语：随机将一张法力值消耗为（1）的随从牌置入你的手牌。"""

    # [x]<b>Deathrattle:</b> Add a random 1-Cost minion to your hand.
    deathrattle = Give(CONTROLLER, RandomMinion(cost=1))


class ULD_289:
    """Fishflinger / 鱼人投手
    战吼：将一张随机鱼人牌分别置入每个玩家的手牌。"""

    # <b>Battlecry:</b> Add a random Murloc to each player's_hand.
    play = Give(ALL_PLAYERS, RandomMurloc())


class ULD_712:
    """Bug Collector / 昆虫收藏家
    战吼：召唤一只1/1并具有突袭的蝗虫。"""

    # <b>Battlecry:</b> Summon a 1/1 Locust with <b>Rush</b>.
    play = Summon(CONTROLLER, "ULD_430t")


class ULD_719:
    """Desert Hare / 沙漠野兔
    战吼：召唤两只1/1的沙漠野兔。"""

    # <b>Battlecry:</b> Summon two 1/1 Desert Hares.
    play = SummonBothSides(CONTROLLER, "ULD_719") * 2
