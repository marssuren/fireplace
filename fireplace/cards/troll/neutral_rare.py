from ..utils import *


##
# Minions


class TRL_057:
    """Serpent Ward / 毒蛇守卫
    在你的回合结束时，对敌方英雄造成2点 伤害。"""

    # At the end of your turn, deal 2 damage to the enemy hero.
    events = OWN_TURN_END.on(Hit(ENEMY_HERO, 2))


class TRL_407:
    """Waterboy / 茶水小弟
    战吼： 在本回合中，你的下一个英雄技能的法力值消耗为（0）点。"""

    # <b>Battlecry:</b> Your next Hero Power this turn costs (0).
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(CONTROLLER, "TRL_407e")


class TRL_407e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))


class TRL_504:
    """Booty Bay Bookie / 藏宝海湾荷官
    战吼：使你的对手获得一张幸运币。"""

    # <b>Battlecry:</b> Give your opponent a Coin.
    play = Give(OPPONENT, THE_COIN)


class TRL_514:
    """Belligerent Gnome / 好斗的侏儒
    嘲讽 战吼：如果你的对手拥有2个或者更多随从，便获得+1攻击力。"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If your opponent has 2 or more minions, gain +1
    # Attack.
    play = (Count(ENEMY_MINIONS) >= 2) & Buff(SELF, "TRL_514e")


TRL_514e = buff(atk=1)


class TRL_520:
    """Murloc Tastyfin / 鱼人大厨
    亡语：从你的牌库中抽两张鱼人牌。"""

    # [x]<b>Deathrattle:</b> Draw 2 Murlocs from your deck.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC)) * 2


class TRL_521:
    """Arena Patron / 竞技场奴隶主
    超杀：召唤另一个竞技场奴隶主。"""

    # <b>Overkill:</b> Summon another Arena Patron.
    overkill = Summon(CONTROLLER, "TRL_521")


class TRL_523:
    """Firetree Witchdoctor / 火树巫医
    战吼：如果你的手牌中有龙牌，便发现 一张法术牌。"""

    # [x]<b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b> a spell.
    powered_up = HOLDING_DRAGON
    play = powered_up & DISCOVER(RandomSpell())


class TRL_524:
    """Shieldbreaker / 破盾者
    战吼：沉默一个具有嘲讽的敌方随从。"""

    # <b>Battlecry:</b> <b>Silence</b> an enemy minion with <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_MUST_TARGET_TAUNTER: 0,
    }
    play = Silence(TARGET)


class TRL_570:
    """Soup Vendor / 汤水商贩
    每当你为你的英雄恢复3点及以上生命值时，抽一张牌。"""

    # Whenever you restore 3 or more Health to your hero, draw a card.
    events = Heal(FRIENDLY_HERO).on((Heal.AMOUNT >= 3) & Draw(CONTROLLER))
