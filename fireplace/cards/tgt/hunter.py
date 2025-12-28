from ..utils import *


##
# Minions


class AT_010:
    """Ram Wrangler / 暴躁的牧羊人
    战吼：如果你控制任何野兽，则随机召唤一个野兽。"""

    powered_up = Find(FRIENDLY_MINIONS + BEAST)
    play = powered_up & Summon(CONTROLLER, RandomBeast())


class AT_057:
    """Stablemaster / 兽栏大师
    战吼：在本回合中，使一个友方野兽获得免疫。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Buff(TARGET, "AT_057o")


AT_057o = buff(immune=True)


class AT_058:
    """King's Elekk / 皇家雷象
    战吼：揭示双方牌库里的一张随从牌。如果你的牌法力值消耗较大，抽这张牌。"""

    play = JOUST & Draw(CONTROLLER, Joust.CHALLENGER)


class AT_059:
    """Brave Archer / 神勇弓箭手
    激励：如果你没有其他手牌，则对敌方英雄造成2点伤害。"""

    inspire = EMPTY_HAND & Hit(ENEMY_HERO, 2)


class AT_063:
    """Acidmaw / 酸喉
    每当有敌方随从受到伤害时，将其消灭。"""

    events = Damage(MINION - SELF).on(Destroy(Damage.TARGET))


class AT_063t:
    """Dreadscale"""

    events = OWN_TURN_END.on(Hit(ALL_MINIONS - SELF, 1))


##
# Spells


class AT_056:
    """Powershot / 强风射击
    对一个随从及其相邻的随从造成$2点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET | TARGET_ADJACENT, 2)


class AT_061:
    """Lock and Load / 子弹上膛
    在本回合中，每当你施放一个法术，随机获取一张 猎人卡牌。"""

    play = Buff(CONTROLLER, "AT_061e")


class AT_061e:
    events = OWN_SPELL_PLAY.on(
        Give(CONTROLLER, RandomCollectible(card_class=CardClass.HUNTER))
    )


class AT_062:
    """Ball of Spiders / 天降蛛群
    召唤三只1/1并具有“亡语：随机获取一张野兽牌”的 结网蛛。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "FP1_011") * 3


##
# Secrets


class AT_060:
    """Bear Trap / 捕熊陷阱
    奥秘：在你的英雄受到攻击后，召唤一个3/3并具有嘲讽的灰熊。"""

    secret = Attack(CHARACTER, FRIENDLY_HERO).after(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "CS2_125"))
    )
