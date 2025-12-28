from ..utils import *


##
# Minions


class BOT_243:
    """Myra Rotspring / 迈拉·腐泉
    战吼： 发现一张亡语随从牌，并获得其亡语。"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a <b>Deathrattle</b> minion. Also gain its
    # <b>Deathrattle</b>.
    play = Discover(CONTROLLER, RandomMinion(deathrattle=True)).then(
        Retarget(SELF, Discover.CARD),
        Give(CONTROLLER, TARGET),
        CopyDeathrattleBuff(TARGET, "BOT_243e"),
    )


class BOT_283:
    """Pogo-Hopper / 蹦蹦兔
    战吼：在本局对战中，你每使用过一张其他蹦蹦兔，便获得+2/+2。"""

    # [x]<b>Battlecry:</b> Gain +2/+2 for each other Pogo-Hopper you played this game.
    play = Buff(SELF, "BOT_283e") * Count(CARDS_PLAYED_THIS_GAME + ID("BOT_283"))


BOT_283e = buff(+2, +2)


class BOT_288:
    """Lab Recruiter / 实验室招募员
    战吼：将一个友方随从的三张复制洗入你的牌库。"""

    # <b>Battlecry:</b> Shuffle 3 copies of a friendly minion into your deck.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Shuffle(CONTROLLER, Copy(TARGET)) * 3


class BOT_565:
    """Blightnozzle Crawler / 荒疫爬行者
    亡语：召唤一个1/1并具有剧毒和突袭的软泥怪。"""

    # <b>Deathrattle:</b> Summon a 1/1 Ooze with <b>Poisonous</b> and <b>Rush</b>.
    deathrattle = Summon(CONTROLLER, "BOT_565t")


class BOT_576:
    """Crazed Chemist / 疯狂的药剂师
    连击：使一个友方随从获得+4攻击力。"""

    # <b>Combo:</b> Give a friendly minion +4 Attack.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    combo = Buff(TARGET, "BOT_576e")


BOT_576e = buff(atk=4)


##
# Spells


class BOT_084:
    """Violet Haze / 紫色烟雾
    随机将两张亡语牌置入你的 手牌。"""

    # Add 2 random <b>Deathrattle</b> cards to_your hand.
    play = Give(CONTROLLER, RandomMinion(deathrattle=True)) * 2


class BOT_087:
    """Academic Espionage / 学术剽窃
    将十张你对手职业的卡牌洗入你的牌库，其法力值消耗为（1）点。"""

    # Shuffle 10 cards from your opponent's class into your deck. They_cost (1).
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Shuffle(CONTROLLER, Buff(RandomCollectible(card_class=ENEMY_CLASS), "BOT_087e"))
        * 10
    )


class BOT_087e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class BOT_242:
    """Myra's Unstable Element / 迈拉的不稳定元素
    抽取你牌库剩下的牌。"""

    # Draw the rest of your deck.
    play = ForceDraw(FRIENDLY_DECK)


class BOT_508:
    """Necrium Vial / 死金药剂
    触发一个友方随从的亡语两次。"""

    # Trigger a friendly minion's <b>Deathrattle</b> twice.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = Deathrattle(TARGET) * 2


##
# Weapons


class BOT_286:
    """Necrium Blade / 死金匕首
    亡语： 随机触发一个友方随从的亡语。"""

    # <b>Deathrattle:</b> Trigger the <b>Deathrattle</b> of a random friendly minion.
    deathrattle = Deathrattle(RANDOM(FRIENDLY_MINIONS + DEATHRATTLE))
