from ..utils import *


##
# Minions


class OG_179:
    """Fiery Bat / 炽炎蝙蝠
    亡语：随机对一个敌人造成1点伤害。"""

    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


class OG_292:
    """Forlorn Stalker / 狼人追猎者
    战吼：使你手牌中所有亡语随从牌获得+1/+1。"""

    play = Buff(FRIENDLY_HAND + MINION + DEATHRATTLE, "OG_292e")


OG_292e = buff(+1, +1)


class OG_216:
    """Infested Wolf / 寄生恶狼
    亡语：召唤两只1/1的蜘蛛。"""

    deathrattle = Summon(CONTROLLER, "OG_216a") * 2


class OG_309:
    """Princess Huhuran / 哈霍兰公主
    战吼：触发一个友方随从的亡语。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Deathrattle(TARGET)


class OG_308:
    """Giant Sand Worm / 巨型沙虫
    每当本随从攻击并消灭一个随从，可再次攻击。"""

    events = Attack(SELF, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & ExtraAttack(SELF)
    )


##
# Spells


class OG_045:
    """Infest / 寄生感染
    使你的所有随从获得 “亡语：随机将一张野兽牌置入你的手牌”。"""

    play = Buff(FRIENDLY_MINIONS, "OG_045a")


class OG_045a:
    """Nerubian Spores"""

    deathrattle = Give(CONTROLLER, RandomBeast())
    tags = {GameTag.DEATHRATTLE: True}


class OG_061:
    """On the Hunt / 搜寻猎物
    造成$1点伤害。召唤一个1/1的獒犬。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1), Summon(CONTROLLER, "OG_061t")


class OG_211:
    """Call of the Wild / 兽群呼唤
    召唤全部三个动物伙伴。"""

    play = (
        Summon(CONTROLLER, "NEW1_034"),
        Summon(CONTROLLER, "NEW1_033"),
        Summon(CONTROLLER, "NEW1_032"),
    )
