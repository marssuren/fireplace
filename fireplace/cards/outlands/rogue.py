from ..utils import *


##
# Minions


class BT_188:
    """Shadowjeweler Hanar / 暗影珠宝师汉纳尔
    在你使用一张奥秘牌后，发现一张不同职业的奥秘牌。"""

    # [x]After you play a <b>Secret</b>, <b>Discover</b> a <b>Secret</b> from a
    # different class.
    events = Play(CONTROLLER, SECRET).after(
        DISCOVER(RandomSpell(card_class=ANOTHER_CLASS, secret=True))
    )


class BT_702:
    """Ashtongue Slayer / 灰舌杀手
    战吼：在本回合中，使一个潜行的随从获得+3攻击力和免疫。"""

    # <b>Battlecry:</b> Give a <b><b>Stealth</b>ed</b> minion +3 Attack and
    # <b>Immune</b> this turn.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_STEALTHED_TARGET: 0,
    }
    play = Buff(TARGET, "BT_702e")


BT_702e = buff(atk=3, immune=True)


class BT_703:
    """Cursed Vagrant / 被诅咒的流浪者
    亡语：召唤一个7/5并具有潜行的阴影。"""

    # <b>Deathrattle:</b> Summon a 7/5 Shadow with <b>Stealth</b>.
    deathrattle = Summon(CONTROLLER, "BT_703t")


class BT_710:
    """Greyheart Sage / 暗心贤者
    战吼：如果你控制一个潜行的随从，抽两张牌。"""

    # [x]<b>Battlecry:</b> If you control a <b><b>Stealth</b>ed</b> minion,
    # draw 2 cards.
    powered_up = Find(FRIENDLY_MINIONS + STEALTH)
    play = powered_up & Draw(CONTROLLER) * 2


class BT_711:
    """Blackjack Stunner / 钉棍终结者
    战吼：如果你控制一个奥秘，将一个随从移回其拥有者的手牌，并且法力值消耗增加（2）点。"""

    # [x]<b>Battlecry:</b> If you control a <b>Secret</b>, return a minion to
    # its owner's hand. It costs (1) more.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS: 1,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & (Bounce(TARGET), Buff(TARGET, "BT_711e"))


class BT_711e:
    tags = {GameTag.COST: +1}
    events = REMOVED_IN_PLAY


class BT_713:
    """Akama / 阿卡玛
    潜行 亡语：将“终极阿卡玛”洗入你的牌库。"""

    # [x]<b>Stealth</b> <b>Deathrattle:</b> Shuffle 'Akama Prime' into your
    # deck.
    deathrattle = Shuffle(CONTROLLER, "BT_713t")


class BT_713t:
    """Akama Prime"""

    # Permanently <b><b>Stealth</b>ed</b>.
    update = Refresh(SELF, {GameTag.STEALTH: True})


##
# Spells


class BT_042:
    """Bamboozle / 偷天换日
    奥秘：当你的随从受到攻击时，随机将其变形成为一个法力值消耗增加（3）点的随从。"""

    # [x]<b>Secret:</b> When one of your minions is attacked, transform it into
    # a random one that costs (3) more.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        Reveal(SELF), Retarget(Attack.ATTACKER, Evolve(Attack.DEFENDER, 3))
    )


class BT_707:
    """Ambush / 伏击
    奥秘：在你的对手使用一张随从牌后，召唤一个2/3并具有剧毒的伏击者。"""

    # [x]<b>Secret:</b> After your opponent plays a minion, summon a 2/3
    # Ambusher with <b>Poisonous</b>.
    secret = Play(OPPONENT, MINION).after(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "BT_707t"))
    )


class BT_709:
    """Dirty Tricks / 邪恶计谋
    奥秘：在你的对手施放一个法术后，抽两张牌。"""

    # [x]<b>Secret:</b> After your opponent casts a spell, draw 2 cards.
    secret = Play(OPPONENT, SPELL).after(
        FULL_HAND | (Reveal(SELF), Draw(CONTROLLER) * 2)
    )
