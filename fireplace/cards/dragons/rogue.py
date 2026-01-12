from ..utils import *


##
# Minions


class DRG_027:
    """Umbral Skulker / 幽影潜藏者
    战吼：如果你已经祈求过两次，则将三张幸运币置入你的手牌。"""

    # [x]<b>Battlecry:</b> If you've <b>Invoked</b> twice, add 3 Coins to your hand.
    powered_up = INVOKED_TWICE
    play = powered_up & Give(CONTROLLER, THE_COIN) * 3


class DRG_031:
    """Necrium Apothecary / 死金药剂师
    连击：从你的牌库中抽一张亡语随从牌并获得其亡语。"""

    # <b>Combo:</b> Draw a <b>Deathrattle</b> minion from your deck and gain its
    # <b>Deathrattle</b>.
    combo = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE)).then(
        CopyDeathrattleBuff(ForceDraw.TARGET, "DRG_031e")
    )


class DRG_034:
    """Stowaway / 偷渡者
    战吼：如果你的牌库中有对战开始时不在牌库中的牌，则抽取其中的两张。"""

    # [x]<b>Battlecry:</b> If there are cards in your deck that didn't start there, draw 2
    # of them.
    play = ForceDraw(RANDOM(FRIENDLY_DECK - STARTING_DECK) * 2)


class DRG_035:
    """Bloodsail Flybooter / 血帆飞贼
    战吼：将两张1/1的海盗牌置入你的手牌。"""

    # <b>Battlecry:</b> Add two 1/1 Pirates to your hand.
    play = Give(CONTROLLER, "DRG_035t") * 2


class DRG_036:
    """Waxadred / 蜡烛巨龙
    亡语：将一支蜡烛洗入你的牌库。抽到蜡烛时，重新召唤蜡烛巨龙。"""

    # [x]<b>Deathrattle:</b> Shuffle a Candle into your deck that resummons Waxadred when
    # drawn.
    deathrattle = Shuffle(CONTROLLER, "DRG_036t")


class DRG_036t:
    play = Summon(CONTROLLER, "DRG_036")
    draw = CAST_WHEN_DRAWN


class DRG_037:
    """Flik Skyshiv / 菲里克·飞刺
    战吼：消灭一个随从及其所有的复制（无论它们在哪）。"""

    # [x]<b>Battlecry:</b> Destroy a minion and all copies of it <i>(wherever they
    # are)</i>.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Destroy(
        FilterSelector(
            lambda entity, source: getattr(entity, "id", None) == source.target.id
        )
    )


##
# Spells


class DRG_028:
    """Dragon's Hoard / 巨龙宝藏
    发现一张另一职业的传说 随从牌。"""

    # <b>Discover</b> a <b>Legendary</b>_minion from another class.
    play = DISCOVER(RandomLegendaryMinion(card_class=ANOTHER_CLASS))


class DRG_030:
    """Praise Galakrond! / 赞美迦拉克隆
    使一个随从获得+1攻击力。祈求迦拉克隆。"""

    # [x]Give a minion +1 Attack. <b>Invoke</b> Galakrond.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "DRG_030e"), INVOKE


DRG_030e = buff(atk=1)


class DRG_033:
    """Candle Breath / 烛火吐息
    抽三张牌。如果你的手牌中有龙牌，这张牌的法力值消耗减少（3）点。"""

    # Draw 3 cards. Costs (3)_less while you're holding a Dragon.
    cost_mod = HOLDING_DRAGON & -3
    play = Draw(CONTROLLER) * 3


class DRG_247:
    """Seal Fate / 封印命运
    对一个未受伤的角色造成$3点伤害。祈求迦拉克隆。"""

    # Deal $3 damage to an undamaged character. <b>Invoke</b> Galakrond.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,
    }
    play = Hit(TARGET, 3), INVOKE


##
# Heros


class DRG_610(GalakrondUtils):
    """Galakrond, the Nightmare"""

    # [x]<b>Battlecry:</b> Draw 1 card. It costs (0). <i>(@)</i>
    progress_total = 2
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DRG_610e"))
    reward = Find(SELF + FRIENDLY_HERO) | Morph(SELF, "DRG_610t2")


class DRG_610t2(GalakrondUtils):
    """Galakrond, the Apocalypse"""

    # [x]<b>Battlecry:</b> Draw 2 cards. They cost (0). <i>(@)</i>
    progress_total = 2
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DRG_610e")) * 2
    reward = Find(SELF + FRIENDLY_HERO) | Morph(SELF, "DRG_610t3")


class DRG_610t3:
    """Galakrond, Azeroth's End"""

    # [x]<b>Battlecry:</b> Draw 4 cards. They cost (0). Equip a 5/2 Claw.
    play = (
        Draw(CONTROLLER).then(Buff(Draw.CARD, "DRG_610e")) * 4,
        Summon(CONTROLLER, "DRG_238ht"),
    )


class DRG_238p2:
    """Galakrond's Guile"""

    # <b>Hero Power</b> Add a <b>Lackey</b> to your hand.
    activate = Give(CONTROLLER, RandomLackey())


class DRG_610e:
    tags = {GameTag.COST: 1}
    events = REMOVED_IN_PLAY
