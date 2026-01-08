from ..utils import *


##
# Minions


class ICC_058:
    """Brrrloc / 冷冻鱼人
    战吼： 冻结一个敌人。"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Freeze(TARGET)


class ICC_088:
    """Voodoo Hexxer / 巫毒妖术师
    嘲讽 冻结任何受到本随从伤害的角色。"""

    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class ICC_090:
    """Snowfury Giant / 雪怒巨人
    在本局对战中，你每过载一个法力水晶，本牌的法力值消耗便减少（1）点。"""

    cost_mod = -Attr(CONTROLLER, GameTag.OVERLOAD_THIS_GAME)


class ICC_289:
    """Moorabi / 莫拉比
    每当有其他随从被冻结，将一张被冻结随从的复制置入你的 手牌。"""

    events = SetTags(ALL_MINIONS - SELF, (GameTag.FROZEN,)).after(
        Give(CONTROLLER, Copy(SetTags.TARGET))
    )


##
# Spells


class ICC_056:
    """Cryostasis / 低温静滞
    使一个随从获得+3/+3，并使其冻结。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_056e"), Freeze(TARGET)


ICC_056e = buff(+3, +3)


class ICC_078:
    """Avalanche / 雪崩
    冻结一个随从，并对其相邻的随从造成$3点伤害。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Freeze(TARGET), Hit(TARGET_ADJACENT, 3)


class ICC_089:
    """Ice Fishing / 冰钓术
    从你的牌库中抽两张鱼人牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC)) * 2


##
# Weapons


class ICC_236:
    """Ice Breaker / 破冰斧
    消灭所有受到该武器伤害的被冻结的随从。"""

    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Find(FROZEN + Attack.DEFENDER) & Destroy(Attack.DEFENDER)
    )


##
# Heros


class ICC_481:
    """Thrall, Deathseer / 死亡先知萨尔
    战吼：随机将你的所有随从变形成为法力值消耗增加（2）点的随从。"""

    play = Evolve(FRIENDLY_MINIONS, 2)


class ICC_481p:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    activate = Evolve(TARGET, 1)
