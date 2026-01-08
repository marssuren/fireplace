from ..utils import *


##
# Minions


class UNG_001:
    """Pterrordax Hatchling / 翼手龙宝宝
    战吼：进化。"""

    play = Adapt(SELF)


class UNG_009:
    """Ravasaur Runt / 暴掠龙幼崽
    战吼：如果你控制至少两个其他随从，便获得进化。"""

    play = (Count(FRIENDLY_MINIONS - SELF) >= 2) & Adapt(SELF)


class UNG_010:
    """Sated Threshadon / 臃肿的蛇颈龙
    嘲讽。亡语：召唤三个1/1的鱼人。"""

    deathrattle = Summon(CONTROLLER, "UNG_201t") * 3


class UNG_073:
    """Rockpool Hunter / 石塘猎人
    战吼：使一个友方鱼人获得+1/+1。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 14,
    }
    play = Buff(TARGET, "UNG_073e")


UNG_073e = buff(+1, +1)


class UNG_076:
    """Eggnapper / 卑劣的窃蛋者
    亡语：召唤两个1/1的迅猛龙。"""

    deathrattle = Summon(CONTROLLER, "UNG_076t1") * 2


class UNG_082:
    """Thunder Lizard / 雷霆蜥蜴
    战吼：如果你在上个回合使用过元素牌，则获得进化。"""

    play = ELEMENTAL_PLAYED_LAST_TURN & Adapt(SELF)


class UNG_084:
    """Fire Plume Phoenix / 火羽凤凰
    战吼：造成3点伤害。"""

    requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 3)


class UNG_205:
    """Glacial Shard / 冰川裂片
    战吼： 冻结一个敌人。"""

    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Freeze(TARGET)


class UNG_801:
    """Nesting Roc / 筑巢双头鹏
    战吼：如果你控制至少两个其他随从，便获得嘲讽。"""

    play = (Count(FRIENDLY_MINIONS - SELF) >= 2) & Taunt(SELF)


class UNG_803:
    """Emerald Reaver / 翡翠掠夺者
    战吼：对每个英雄造成1点伤害。"""

    play = Hit(ALL_HEROES, 1)


class UNG_809:
    """Fire Fly / 火羽精灵
    战吼：将一张1/2的元素牌置入你的手牌。"""

    play = Give(CONTROLLER, "UNG_809t1")


class UNG_818:
    """Volatile Elemental / 不稳定的元素
    亡语：随机对一个敌方随从造成3点伤害。"""

    deathrattle = Hit(RANDOM_ENEMY_MINION, 3)


class UNG_845:
    """Igneous Elemental / 火岩元素
    亡语：将两张1/2的烈焰元素置入你的手牌。"""

    deathrattle = Give(CONTROLLER, "UNG_809t1") * 2


class UNG_928:
    """Tar Creeper / 焦油爬行者
    嘲讽 在你对手的回合拥有+2攻击力。"""

    update = CurrentPlayer(OPPONENT) & Refresh(SELF, {GameTag.ATK: +2})


class UNG_937:
    """Primalfin Lookout / 蛮鱼斥候
    战吼：如果你控制着其他鱼人，发现一张鱼人牌。"""

    play = Find(FRIENDLY_MINIONS + MURLOC - SELF) & DISCOVER(RandomMurloc())
