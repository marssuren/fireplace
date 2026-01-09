from ..utils import *


##
# Minions


class ICC_018:
    """Phantom Freebooter / 幻影海盗
    战吼： 获得等同于你的武器属性的属性值。"""

    play = (Find(FRIENDLY_WEAPON), Buff(
        SELF,
        "ICC_018e",
        atk=ATK(FRIENDLY_WEAPON),
        max_health=CURRENT_DURABILITY(FRIENDLY_WEAPON)
    ))


class ICC_027:
    """Bone Drake / 白骨幼龙
    亡语：随机将一张龙牌置入你的手牌。"""

    deathrattle = Give(CONTROLLER, RandomDragon())


class ICC_099:
    """Ticking Abomination / 自爆憎恶
    亡语：对你所有的随从造成5点伤害。"""

    deathrattle = Hit(FRIENDLY_MINIONS, 5)


class ICC_257:
    """Corpse Raiser / 唤尸者
    战吼：使一个友方随从获得“亡语：再次召唤该随从。”"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_257e")


class ICC_257e:
    deathrattle = Summon(CONTROLLER, Copy(OWNER))
    tags = {GameTag.DEATHRATTLE: True}


class ICC_466:
    """Saronite Chain Gang / 萨隆苦囚
    嘲讽。战吼：召唤一个萨隆苦囚。"""

    play = Summon(CONTROLLER, ExactCopy(SELF))


class ICC_700:
    """Happy Ghoul / 开心的食尸鬼
    在本回合中，如果你的英雄受到治疗，则 法力值消耗为（0）点。"""

    class Hand:
        events = Heal(FRIENDLY_HERO).on(Buff(SELF, "ICC_700e"))


@custom_card
class ICC_700e:
    tags = {
        GameTag.CARDNAME: "Happy Ghoul Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    cost = SET(0)
    events = REMOVED_IN_PLAY


class ICC_702:
    """Shallow Gravedigger / 孱弱的掘墓者
    亡语：随机将一个具有亡语的随从置入你的手牌。"""

    deathrattle = Give(CONTROLLER, RandomMinion(deathrattle=True))


class ICC_902:
    """Mindbreaker / 摧心者
    双方英雄技能均无法使用。"""

    update = Refresh(ALL_HERO_POWERS, {enums.HEROPOWER_DISABLED: True})


class ICC_911:
    """Keening Banshee / 哀泣女妖
    每当你使用一张牌，便移除你的牌库顶的三张牌。"""

    events = Play(CONTROLLER).on(Mill(CONTROLLER) * 3)
