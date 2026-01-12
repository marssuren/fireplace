from ..utils import *


##
# Minions


class UNG_838:
    """Tar Lord / 焦油兽王
    嘲讽 在你对手的回合拥有+4攻击力。"""

    update = CurrentPlayer(OPPONENT) & Refresh(SELF, {GameTag.ATK: +4})


class UNG_925:
    """Ornery Direhorn / 暴躁的恐角龙
    嘲讽，战吼：进化。"""

    play = Adapt(SELF)


class UNG_926:
    """Cornered Sentry / 身陷绝境的哨卫
    嘲讽，战吼： 为你的对手召唤三只1/1的迅猛龙。"""

    play = Summon(OPPONENT, "UNG_076t1") * 3


class UNG_933:
    """King Mosh / 暴龙之王摩什
    战吼：消灭所有受伤的随从。"""

    play = Destroy(ALL_MINIONS + DAMAGED)


class UNG_957:
    """Direhorn Hatchling / 恐角龙宝宝
    嘲讽。亡语： 将一张8/12并具有嘲讽的“恐角龙头领”洗入你的牌库。"""

    deathrattle = Shuffle(CONTROLLER, "UNG_957t1")


##
# Spells


class UNG_922:
    """Explore Un'Goro / 探索安戈洛
    将你牌库里的所有卡牌替换成 “发现一张牌”。"""

    play = Morph(FRIENDLY_DECK, "UNG_922t1")


class UNG_922t1:
    play = DISCOVER(RandomCollectible())


class UNG_923:
    """Iron Hide / 铜皮铁甲
    获得5点护甲值。"""

    play = GainArmor(FRIENDLY_HERO, 5)


class UNG_927:
    """Sudden Genesis / 基因转接
    复制所有受伤的友方随从。"""

    play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + DAMAGED))


class UNG_934:
    """Fire Plume's Heart / 火羽之心
    任务：使用七张具有嘲讽的随从牌。 奖励：萨弗拉斯。"""

    progress_total = 7
    quest = Play(CONTROLLER, TAUNT).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_934t1")


class UNG_934t1:
    play = Summon(CONTROLLER, "UNG_934t2")


class UNG_934t2:
    activate = Hit(RANDOM_ENEMY_CHARACTER, 8)


##
# Weapons


class UNG_929:
    """Molten Blade / 熔岩之刃
    如果这张牌在你的手牌中，每个回合都会变成一张新的武器牌。"""

    class Hand:
        def _morph_and_buff(self):
            morphed = yield Morph(SELF, RandomWeapon())
            if morphed:
                yield Buff(morphed, "UNG_929e")
        
        events = OWN_TURN_BEGIN.on(_morph_and_buff)


class UNG_929e:
    class Hand:
        def _morph_and_buff(self):
            morphed = yield Morph(OWNER, RandomWeapon())
            if morphed:
                yield Buff(morphed, "UNG_929e")
        
        events = OWN_TURN_BEGIN.on(_morph_and_buff)

    events = REMOVED_IN_PLAY
