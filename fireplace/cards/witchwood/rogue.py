from ..utils import *


##
# Minions


class GIL_510:
    """Mistwraith / 迷雾幽灵
    每当你使用一张回响牌时，获得+1/+1。"""

    # Whenever you play an <b>Echo</b>_card, gain +1/+1.
    events = Play(CONTROLLER, ECHO).after(Buff(SELF, "GIL_510e"))


GIL_510e = buff(+1, +1)


class GIL_557:
    """Cursed Castaway / 被诅咒的海盗
    突袭，亡语： 从你的牌库中抽一张连击牌。"""

    # <b>Rush</b> <b>Deathrattle:</b> Draw a <b>Combo</b> card from your deck.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + COMBO))


class GIL_598:
    """Tess Greymane / 苔丝·格雷迈恩
    战吼：重新使用在本局对战中你所使用过的另一职业的卡牌（目标随机而定）。"""

    # [x]<b>Battlecry:</b> Replay every card from another class you've played this game
    # <i>(targets chosen randomly)</i>.
    play = Replay(Copy(SHUFFLE(CARDS_PLAYED_THIS_GAME + OTHER_CLASS_CHARACTER)))


class GIL_677:
    """Face Collector / 面具收集者
    回响，战吼：随机将一张传说随从牌置入你的手牌。"""

    # <b>Echo</b> <b>Battlecry:</b> Add a random <b>Legendary</b> minion to your hand.
    play = Give(CONTROLLER, RandomLegendaryMinion())


class GIL_827:
    """Blink Fox / 闪狐
    战吼：随机将一张（你对手职业的）卡牌置入你的手牌。"""

    # <b>Battlecry:</b> Add a random card to your hand <i>(from your opponent's class).</i>
    play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


class GIL_902:
    """Cutthroat Buccaneer / 刺喉海盗
    连击：使你的武器获得+1攻击力。"""

    # <b>Combo:</b> Give your weapon +1 Attack.
    combo = Buff(FRIENDLY_WEAPON, "GIL_902e")


GIL_902e = buff(atk=1)


##
# Spells


class GIL_506:
    """Cheap Shot / 偷袭
    回响 对一个随从造成 $2点伤害。"""

    # <b>Echo</b> Deal $2 damage to a_minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class GIL_687:
    """WANTED! / 通缉令
    对一个随从造成$3点伤害。如果消灭该随从，将一张幸运币置入你的手牌。"""

    # Deal $3 damage to a minion. If that kills it, add a Coin to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Dead(TARGET) & Give(CONTROLLER, THE_COIN)


class GIL_696:
    """Pick Pocket / 搜索
    回响 随机将一张（你对手职业的）卡牌置入你的手牌。"""

    # <b>Echo</b> Add a random card to your hand <i>(from your opponent's class).</i>
    play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


##
# Weapons


class GIL_672:
    """Spectral Cutlass / 幽灵弯刀
    吸血 每当你使用一张另一职业的卡牌时，获得+1耐久度。"""

    # [x]<b>Lifesteal</b> Whenever you play a card from another class, gain +1 Durability.
    events = Play(CONTROLLER, OTHER_CLASS_CHARACTER).after(Buff(SELF, "GIL_672e"))


GIL_672e = buff(health=1)
