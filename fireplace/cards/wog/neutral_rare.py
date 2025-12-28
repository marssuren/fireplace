from ..utils import *


##
# Minions


class OG_162:
    """Disciple of C'Thun / 克苏恩的信徒
    战吼： 造成2点伤害。使你的克苏恩获得+2/+2（无论它在哪里）。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 2), Buff(CTHUN, "OG_281e", atk=2, max_health=2)


class OG_255:
    """Doomcaller / 厄运召唤者
    战吼：使你的克苏恩获得+2/+2（无论它在哪里）。如果克苏恩死亡，将其洗入你的牌库。"""

    play = (
        Buff(CTHUN, "OG_281e", atk=2, max_health=2),
        Find(KILLED + CTHUN) & Shuffle(CONTROLLER, "OG_280"),
    )


class OG_034:
    """Silithid Swarmer / 异种群居蝎
    在本回合中，除非你的英雄进行过攻击，否则无法进行攻击。"""

    update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & (
        Refresh(SELF, {GameTag.CANT_ATTACK: True})
    )


class OG_339:
    """Skeram Cultist / 斯克拉姆狂热者
    战吼： 使你的克苏恩 获得+2/+2（无论它在哪里）。"""

    play = Buff(CTHUN, "OG_281e", atk=2, max_health=2)


class OG_147:
    """Corrupted Healbot / 腐化治疗机器人
    亡语：为敌方英雄恢复#8点生命值。"""

    deathrattle = Heal(ENEMY_HERO, 8)


class OG_161:
    """Corrupted Seer / 腐化先知
    战吼：对所有非鱼人随从造成2点伤害。"""

    play = Hit(ALL_MINIONS - MURLOC, 2)


class OG_254:
    """Eater of Secrets / 奥秘吞噬者
    战吼：摧毁所有敌方奥秘。每摧毁一个，便获得+1/+1。"""

    play = (Buff(SELF, "OG_254e") * Count(ENEMY_SECRETS), Destroy(ENEMY_SECRETS))


OG_254e = buff(+1, +1)


class OG_320:
    """Midnight Drake / 午夜幼龙
    战吼：你每有一张其他手牌，便获得+1攻击力。"""

    play = Buff(SELF, "OG_320e") * Count(FRIENDLY_HAND)


OG_320e = buff(atk=1)


class OG_322:
    """Blackwater Pirate / 黑水海盗
    你的武器法力值消耗减少（2）点。"""

    update = Refresh(FRIENDLY_HAND + WEAPON, {GameTag.COST: -2})
