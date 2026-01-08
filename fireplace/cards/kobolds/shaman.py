from ..utils import *


##
# Minions


class LOOT_062:
    """Kobold Hermit / 狗头人隐士
    战吼：选择一个基础图腾并召唤它。"""

    # <b>Battlecry:</b> Choose a basic Totem. Summon it.
    play = Choice(CONTROLLER, BASIC_TOTEMS).then(Summon(CONTROLLER, Choice.CARD))


class LOOT_358:
    """Grumble, Worldshaker / 撼世者格朗勃尔
    战吼： 将你的其他随从移回你的手牌，并使其法力值消耗变为（1）点。"""

    # <b>Battlecry:</b> Return your other minions to your hand. They cost (1).
    play = Bounce(FRIENDLY_MINIONS - SELF).then(Buff(Bounce.TARGET, "LOOT_358e"))


class LOOT_358e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class LOOT_517:
    """Murmuring Elemental / 低语元素
    战吼：你在本回合中的下一个战吼将触发两次。"""

    # <b>Battlecry:</b> Your next <b>Battlecry</b> this turn triggers_twice.
    play = Buff(CONTROLLER, "LOOT_517e")


class LOOT_517e:
    tags = {GameTag.TAG_ONE_TURN_EFFECT: True}
    update = Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True})
    events = Play(CONTROLLER, BATTLECRY).after(Destroy(SELF))


class LOOT_518:
    """Windshear Stormcaller / 风剪唤风者
    战吼：如果你控制全部四种基础图腾，则召唤风领主奥拉基尔。"""

    # <b>Battlecry:</b> If you control all 4 basic Totems, summon Al'Akir_the_Windlord.
    play = FindAll(*[FRIENDLY_MINIONS + ID(totem) for totem in BASIC_TOTEMS]) & Summon(
        CONTROLLER, "NEW1_010"
    )


##
# Spells


class LOOT_060:
    """Crushing Hand / 粉碎之手
    对一个随从造成$8点伤害。 过载：（3）"""

    # Deal $8 damage to a minion. <b><b>Overload</b>:</b> (3)
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 8)


class LOOT_064:
    """Lesser Sapphire Spellstone / 小型法术蓝宝石
    选择一个友方随从，召唤一个它的复制。@（过载三个法力水晶后升级。）"""

    # Summon 1 copy of a friendly minion. @<i>(<b>Overload</b> 3 Mana Crystals to
    # upgrade.)</i>
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))
    progress_total = 3
    reward = Morph(SELF, "LOOT_064t1")

    class Hand:
        # 过载3个法力水晶后升级
        events = Overload(CONTROLLER).on(AddProgress(SELF, CONTROLLER, Overload.AMOUNT))


class LOOT_064t1:
    """Sapphire Spellstone"""

    # Summon 2 copies of a friendly minion. @
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET)) * 2
    progress_total = 3
    reward = Morph(SELF, "LOOT_064t2")

    class Hand:
        # 过载3个法力水晶后升级
        events = Overload(CONTROLLER).on(AddProgress(SELF, CONTROLLER, Overload.AMOUNT))


class LOOT_064t2:
    """Greater Sapphire Spellstone"""

    # Summon 3 copies of a friendly minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET)) * 3


class LOOT_344:
    """Primal Talismans / 原始护身符
    使你的所有随从获得 “亡语：随机召唤一个基础图腾。”"""

    # Give your minions "<b>Deathrattle:</b> Summon a random basic Totem."
    play = Buff(ALL_MINIONS, "LOOT_344e")


class LOOT_344e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, RandomBasicTotem())


class LOOT_373:
    """Healing Rain / 治疗之雨
    恢复#12点生命值，随机分配到所有友方角色上。"""

    # Restore #12 Health randomly split among all friendly characters.
    play = Heal(RANDOM_FRIENDLY_CHARACTER, 1) * SPELL_HEAL(12)


class LOOT_504:
    """Unstable Evolution / 不稳定的异变
    回响 将一个友方随从随机变形成为一个法力值消耗增加（1）点的随从。"""

    # Transform a friendly minion into one that costs (1) more. Repeatable this turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Evolve(TARGET, 1), Give(CONTROLLER, "LOOT_504t")


class LOOT_504t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Evolve(TARGET, 1), Give(CONTROLLER, "LOOT_504t")
    events = OWN_TURN_END.on(Destroy(SELF))


##
# Weapons


class LOOT_506:
    """The Runespear / 符文之矛
    在你的英雄攻击后，发现一张法术牌，并向随机目标施放。"""

    # After your hero attacks, <b>Discover</b> a spell and cast it with random targets.
    events = Attack(FRIENDLY_HERO).after(
        Discover(CONTROLLER, RandomSpell()).then(CastSpell(Discover.CARD))
    )
