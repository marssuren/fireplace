from ..utils import *


##
# Minions


class ICC_019:
    """Skelemancer / 骷髅法师
    亡语：如果此时是你对手的回合，则召唤一个8/8的骷髅。"""

    deathrattle = CurrentPlayer(OPPONENT) & Summon(CONTROLLER, "ICC_019t")


class ICC_026:
    """Grim Necromancer / 冷酷的死灵法师
    战吼：召唤两个1/1的骷髅。"""

    play = SummonBothSides(CONTROLLER, "ICC_026t") * 2


ICC_028e = buff(health=2)


class ICC_028:
    """Sunborne Val'kyr / 阳焰瓦格里
    战吼：使相邻的随从获得+2生命值。"""

    play = Buff(SELF_ADJACENT, "ICC_028e")


class ICC_029:
    """Cobalt Scalebane / 深蓝刃鳞龙兽
    在你的回合结束时，随机使另一个友方随从获得+3攻击力。"""

    events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "ICC_029e"))


ICC_029e = buff(atk=3)


class ICC_031:
    """Night Howler / 暗夜嗥狼
    每当本随从受到伤害，获得+2攻击力。"""

    events = Damage(SELF).on(Buff(SELF, "ICC_031e"))


ICC_031e = buff(atk=2)


class ICC_067:
    """Vryghoul / 维库食尸鬼
    亡语：如果此时是你对手的回合，则召唤一个2/2的食尸鬼。"""

    deathrattle = CurrentPlayer(OPPONENT) & Summon(CONTROLLER, "ICC_900t")


class ICC_092:
    """Acherus Veteran / 阿彻鲁斯老兵
    战吼：使一个友方随从获得+1攻击力。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_092e")


ICC_092e = buff(atk=1)


class ICC_093:
    """Tuskarr Fisherman / 海象人渔夫
    战吼：使一个友方随从获得法术伤害+1。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_093e")


ICC_093e = buff(spellpower=1)


class ICC_094:
    """Fallen Sun Cleric / 堕落残阳祭司
    战吼：使一个友方随从获得+1/+1。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_094e")


ICC_094e = buff(+1, +1)


class ICC_097:
    """Grave Shambler / 墓地蹒跚者
    每当你的武器被摧毁时，便获得+1/+1。"""

    events = Death(FRIENDLY + WEAPON).on(Buff(SELF, "ICC_097e"))


ICC_097e = buff(+1, +1)


class ICC_467:
    """Deathspeaker / 亡语者
    战吼：在本回合中，使一个友方随从获得免疫。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "ICC_467e")


ICC_467e = buff(immune=True)


class ICC_468:
    """Wretched Tiller / 失心农夫
    每当本随从攻击时，对敌方英雄造成2点伤害。"""

    events = Attack(SELF).on(Hit(ENEMY_HERO, 2))


class ICC_705:
    """Bonemare / 骨魇
    战吼：使一个友方随从获得+4/+4和嘲讽。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_705e")


ICC_705e = buff(+4, +4, taunt=True)


class ICC_855:
    """Hyldnir Frostrider / 海德尼尔冰霜骑士
    战吼：冻结你的其他随从。"""

    play = Freeze(FRIENDLY_MINIONS - SELF)


class ICC_900:
    """Necrotic Geist / 死灵恶鬼
    每当你的其他随从死亡时，召唤一个2/2的食尸鬼。"""

    events = Death(FRIENDLY_MINIONS - SELF).on(Summon(CONTROLLER, "ICC_900t"))


class ICC_904:
    """Wicked Skeleton / 邪骨骷髅
    战吼：在本回合中每有一个随从死亡，便获得+1/+1。"""

    play = Buff(SELF, "ICC_904e") * Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


ICC_904e = buff(+1, +1)
