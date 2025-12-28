from ..utils import *


##
# Minions


class LOOT_078:
    """Cave Hydra / 洞穴多头蛇
    同时对其攻击目标相邻的随从造成伤害。"""

    # Also damages the minions next to whomever this attacks.
    events = Attack(SELF).on(CLEAVE)


class LOOT_511:
    """Kathrena Winterwisp / 卡瑟娜·冬灵
    战吼，亡语：招募一个野兽。"""

    # <b>Battlecry and Deathrattle:</b> <b>Recruit</b> a Beast.
    play = deathrattle = Recruit(BEAST)


class LOOT_520:
    """Seeping Oozeling / 渗水的软泥怪
    战吼： 随机获得牌库中一个随从的亡语。"""

    # <b>Battlecry:</b> Gain the <b>Deathrattle</b> of a random minion in your deck.
    play = (
        CopyDeathrattleBuff(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE), "LOOT_520e"),
    )


##
# Spells


class LOOT_077:
    """Flanking Strike / 侧翼打击
    对一个随从造成$3点伤害。召唤一只3/3的狼。"""

    # Deal $3 damage to a minion. Summon a 3/3 Wolf.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Summon(CONTROLLER, "LOOT_077t")


class LOOT_079:
    """Wandering Monster / 游荡怪物
    奥秘： 当一个敌人攻击你的英雄时，随机召唤一个法力值消耗为（3）的随从，并使其成为攻击的目标。"""

    # <b>Secret:</b> When an enemy attacks your hero, summon a 3-Cost minion as the new
    # target.
    secret = Attack(ENEMY_MINIONS, FRIENDLY_HERO).on(
        Reveal(SELF),
        Retarget(Attack.ATTACKER, Summon(CONTROLLER, RandomMinion(cost=3))),
    )


class LOOT_080:
    """Lesser Emerald Spellstone / 小型法术翡翠
    召唤两只3/3的狼。（使用一个奥秘后升级。）"""

    # Summon two 3/3_Wolves. <i>(Play a <b>Secret</b> to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "LOOT_077t") * 2

    class Hand:
        events = Play(CONTROLLER, SECRET).after(Morph(SELF, "LOOT_080t2"))


class LOOT_080t2:
    """Emerald Spellstone"""

    # Summon three 3/3_Wolves. <i>(Play a <b>Secret</b> to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "LOOT_077t") * 3

    class Hand:
        events = Play(CONTROLLER, SECRET).after(Morph(SELF, "LOOT_080t3"))


class LOOT_080t3:
    """Greater Emerald Spellstone"""

    # Summon four 3/3_Wolves.
    play = Summon(CONTROLLER, "LOOT_077t") * 4


class LOOT_217:
    """To My Side! / 来我身边
    召唤一个动物伙伴，如果你的牌库里没有随从牌，则召唤两个。"""

    # [x]Summon an Animal Companion, or 2 if your deck has no minions.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]
    play = Find(FRIENDLY_DECK + MINION) & (Summon(CONTROLLER, RandomEntourage())) | (
        Summon(CONTROLLER, RandomEntourage() * 2)
    )


class LOOT_522:
    """Crushing Walls / 碾压墙
    消灭对手场上最左边和最右边的随从。"""

    # Destroy your opponent's left and right-most minions.
    play = Destroy(ENEMY_MINIONS + (LEFTMOST_FIELD | RIGTHMOST_FIELD))


##
# Weapons


class LOOT_085:
    """Rhok'delar / 伦鲁迪洛尔
    战吼：如果你的牌库里没有随从牌，则用随机猎人法术牌填满你的手牌。"""

    # <b>Battlecry:</b> If your deck has no minions, fill your_hand with Hunter_spells.
    play = Find(FRIENDLY_DECK + MINION) | (
        Give(CONTROLLER, RandomSpell(card_class=CardClass.HUNTER))
        * (MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND))
    )


class LOOT_222:
    """Candleshot / 蜡烛弓
    你的英雄在攻击时免疫。"""

    # Your hero is <b>Immune</b> while attacking.
    update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})
