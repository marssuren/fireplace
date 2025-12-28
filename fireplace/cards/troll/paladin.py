from ..utils import *


##
# Minions


class TRL_300:
    """Shirvallah, the Tiger / 西瓦尔拉，猛虎之神
    圣盾，突袭，吸血 你每消耗1点法力值用于法术牌上，本牌的法力值消耗便减少（1）点。"""

    # [x]<b>Divine Shield</b>, <b>Rush</b>, <b>Lifesteal</b> Costs (1) less for each Mana
    # you've spent on spells.
    cost_mod = -AttrValue("spent_mana_on_spells_this_game")(CONTROLLER)


class TRL_306:
    """Immortal Prelate / 永恒祭司
    亡语：将本随从洗入你的牌库。保留所有附加效果。"""

    # <b>Deathrattle:</b> Shuffle this into your deck. It keeps any enchantments.
    tags = {enums.KEEP_BUFF: True}
    deathrattle = Shuffle(CONTROLLER, SELF)


class TRL_308:
    """High Priest Thekal / 高阶祭司塞卡尔
    战吼：保留英雄的1点生命值，将其余部分转化为护甲值。"""

    # <b>Battlecry:</b> Convert all but 1_of your Hero's Health into Armor.
    play = (
        GainArmor(FRIENDLY_HERO, CURRENT_HEALTH(FRIENDLY_HERO) - 1),
        SetCurrentHealth(FRIENDLY_HERO, 1),
    )


class TRL_309:
    """Spirit of the Tiger / 猛虎之灵
    潜行一回合。在你施放一个法术后，召唤一只属性值 等于其法力值消耗的老虎。"""

    # [x]<b>Stealth</b> for 1 turn. After you cast a spell, summon a Tiger with stats equal
    # to its Cost.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Play(CONTROLLER, SPELL).after(
            SummonCustomMinion(
                CONTROLLER,
                "TRL_309t",
                COST(Play.CARD),
                COST(Play.CARD),
                COST(Play.CARD),
            )
        ),
    )


class TRL_545(ThresholdUtils):
    """Zandalari Templar"""

    # [x]<b>Battlecry:</b> If you've restored 10 Health this game, gain +4/+4 and
    # <b>Taunt</b>.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = ThresholdUtils.powered_up & Buff(SELF, "TRL_545e")


TRL_545e = buff(+4, +4)


##
# Spells


class TRL_302:
    """Time Out! / 暂避锋芒
    直到你的 下个回合，你的英雄免疫。"""

    # Your hero is <b>Immune</b> until your next turn.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(SELF, "TRL_302e")


class TRL_302e:
    tags = {
        GameTag.CANT_BE_DAMAGED: True,
        GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True,
    }
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class TRL_305:
    """A New Challenger... / 新人登场
    发现一张法力值消耗为（6）的随从牌。召唤该随从并使其获得嘲讽和圣盾。"""

    # <b>Discover</b> a 6-Cost minion. Summon it with <b>Taunt</b> and <b>Divine
    # Shield</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Discover(CONTROLLER, RandomMinion(cost=6)).then(
        Summon(CONTROLLER, Discover.CARD).then(
            Taunt(Summon.CARD),
            GiveDivineShield(Summon.CARD),
        )
    )


class TRL_307:
    """Flash of Light / 圣光闪现
    恢复#4点生命值。抽一张牌。"""

    # Restore #4 Health. Draw a card.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Heal(TARGET, 4), Draw(CONTROLLER)


##
# Weapons


class TRL_304:
    """Farraki Battleaxe / 法拉基战斧
    超杀：使你手牌中的一张随从牌 获得+2/+2。"""

    # <b>Overkill:</b> Give a minion in your hand +2/+2.
    overkill = Buff(FRIENDLY_HAND + MINION, "TRL_304e")


TRL_304e = buff(+2, +2)


class TRL_543:
    """Bloodclaw / 血爪
    战吼：对你的英雄造成5点伤害。"""

    # <b>Battlecry:</b> Deal 5 damage to your hero.
    play = Hit(FRIENDLY_HERO, 5)
