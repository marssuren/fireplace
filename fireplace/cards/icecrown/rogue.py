from ..utils import *


##
# Minions


class ICC_065:
    """Bone Baron / 白骨大亨
    亡语： 将两张1/1的“骷髅”置入你的手牌。"""

    deathrattle = Give(CONTROLLER, "ICC_026t") * 2


class ICC_240:
    """Runeforge Haunter / 符文熔铸游魂
    在你的回合时，你的武器不会失去 耐久度。"""

    update = CurrentPlayer(CONTROLLER) & Refresh(
        FRIENDLY_WEAPON, {GameTag.IMMUNE: True}
    )


class ICC_809:
    """Plague Scientist / 瘟疫科学家
    连击：使一个友方随从获得剧毒。"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
    }
    combo = GivePoisonous(TARGET)


class ICC_811:
    """Lilian Voss / 莉莉安·沃斯
    战吼：随机将你手牌中所有的法术牌替换成（你对手职业的）法术牌。"""

    play = Find(ENEMY_HERO - NEUTRAL) & (
        Morph(FRIENDLY_HAND + SPELL, RandomSpell(card_class=ENEMY_CLASS))
    )


class ICC_910:
    """Spectral Pillager / 鬼灵匪贼
    连击：在本回合中，你每使用一张其他牌，便对一个随从造成2点伤害。"""

    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
    }
    combo = Hit(TARGET, NUM_CARDS_PLAYED_THIS_TURN)


##
# Spells


class ICC_201:
    """Roll the Bones / 命运骨骰
    抽一张牌。如果这张牌有亡语，则再次施放本法术。"""

    play = Draw(CONTROLLER).then(Find(Draw.CARD + DEATHRATTLE) & CastSpell("ICC_201"))


class ICC_221:
    """Leeching Poison / 吸血药膏
    在本回合中，你的武器获得 吸血。"""

    requirements = {
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = GiveLifesteal(FRIENDLY_WEAPON)


class ICC_233:
    """Doomerang / 末日回旋镖
    对一个随从投掷你的武器。武器会造成伤害，然后移回你的手牌。"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = Hit(TARGET, ATK(FRIENDLY_WEAPON)), Bounce(FRIENDLY_WEAPON)


##
# Weapons


class ICC_850:
    """Shadowblade / 暗影之刃
    战吼：在本回合中，你的英雄免疫。"""

    play = Buff(FRIENDLY_HERO, "ICC_850e")


ICC_850e = buff(immune=True)


##
# Heros


class ICC_827:
    """Valeera the Hollow / 虚空之影瓦莉拉
    战吼：获得潜行直到你的下个回合。"""

    play = (
        Stealth(FRIENDLY_HERO),
        Buff(FRIENDLY_HERO, "ICC_827e3"),
        Give(CONTROLLER, "ICC_827t"),
    )


class ICC_827e3:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class ICC_827p:
    tags = {enums.PASSIVE_HERO_POWER: True}
    events = OWN_TURN_BEGIN.on(Give(CONTROLLER, "ICC_827t"))


class ICC_827t:
    requirements = {
        PlayReq.REQ_MUST_PLAY_OTHER_CARD_FIRST: 0,
    }

    class Hand:
        events = (
            Play(CONTROLLER).on(
                Morph(SELF, ExactCopy(Play.CARD)).then(Buff(Morph.CARD, "ICC_827e"))
            ),
            OWN_TURN_END.on(Destroy(SELF)),
        )
        update = Find(FRIENDLY_HERO_POWER - EXHAUSTED + ID("ICC_827p")) | Destroy(SELF)


class ICC_827e:
    class Hand:
        events = (
            Play(CONTROLLER).on(
                Morph(OWNER, ExactCopy(Play.CARD)).then(Buff(Morph.CARD, "ICC_827e"))
            ),
            OWN_TURN_END.on(Destroy(SELF)),
        )
        update = Find(FRIENDLY_HERO_POWER - EXHAUSTED + ID("ICC_827p")) | Destroy(SELF)

    events = REMOVED_IN_PLAY
