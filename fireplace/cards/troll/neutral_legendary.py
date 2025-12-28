from ..utils import *


##
# Minions


class TRL_096:
    """Griftah / 格里伏塔
    战吼：发现两张牌。随机交给你的对手其中一张。"""

    # [x]<b>Battlecry:</b> <b>Discover</b> two cards. Give one to your opponent at random.
    play = DISCOVER(RandomCollectible()).then(
        SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_ENT_1: Discover.CARD}),
        DISCOVER(RandomCollectible()).then(
            SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_ENT_2: Discover.CARD}),
            COINFLIP
            & (
                Give(CONTROLLER, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1)),
                Give(OPPONENT, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_2)),
            )
            | (
                Give(CONTROLLER, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_2)),
                Give(OPPONENT, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1)),
            ),
            UnsetTags(
                SELF,
                (
                    GameTag.TAG_SCRIPT_DATA_ENT_1,
                    GameTag.TAG_SCRIPT_DATA_ENT_2,
                ),
            ),
        ),
    )


class TRL_537:
    """Da Undatakah / 送葬者安德提卡
    战吼：获得在本局对战中三个死亡的友方随从的亡语。"""

    # [x]<b>Battlecry:</b> Gain the <b>Deathrattle</b> effects of 3 friendly minions that
    # died this game.
    play = CopyDeathrattleBuff(
        RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 3, "TRL_537e"
    )


class TRL_541:
    """Hakkar, the Soulflayer / 夺灵者哈卡
    亡语：将一张“堕落之血”分别洗入每个玩家的牌库。"""

    # <b>Deathrattle:</b> Shuffle a Corrupted Blood into each player's deck.
    deathrattle = Shuffle(PLAYER, "TRL_541t")


class TRL_541t:
    """Corrupted Blood"""

    # <b>Casts When Drawn</b> Take 3 damage. After you draw, shuffle two copies of this
    # into your deck.
    play = Hit(FRIENDLY_HERO, 3), Shuffle(CONTROLLER, "TRL_541t") * 2
    draw = CAST_WHEN_DRAWN


class TRL_542:
    """Oondasta / 乌达斯塔
    突袭 超杀：从你的手牌中召唤一个野兽。"""

    # <b>Rush</b> <b>Overkill:</b> Summon a Beast from your hand.
    overkill = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + BEAST))


class TRL_564:
    """Mojomaster Zihi / 魔精大师兹伊希
    战吼： 将每个玩家的法力水晶重置为五个。"""

    # <b>Battlecry:</b> Set each player to 5 Mana Crystals.
    play = SetMana(PLAYER, 5)
