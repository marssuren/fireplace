from ..utils import *


##
# Minions


class TRL_223:
    """Spirit of the Raptor / 迅猛龙之灵
    潜行一回合。在你的英雄攻击并消灭一个随从后，抽一张牌。"""

    # [x]<b>Stealth</b> for 1 turn. After your hero attacks and __kills a minion, draw a
    # card.__
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Attack(FRIENDLY_HERO, ALL_MINIONS).after(
            Dead(ALL_MINIONS + Attack.DEFENDER) & Draw(CONTROLLER)
        ),
    )


class TRL_232:
    """Ironhide Direhorn / 铁皮恐角龙
    超杀：召唤一个5/5的铁皮小恐龙。"""

    # <b>Overkill:</b> Summon a 5/5_Ironhide Runt.
    overkill = Summon(CONTROLLER, "TRL_232t")


class TRL_240:
    """Savage Striker / 野蛮先锋
    战吼：对一个敌方随从造成等同于你的英雄攻击力的伤害。"""

    # <b>Battlecry:</b> Deal damage to an enemy minion equal to your hero's Attack.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_HERO_HAS_ATTACK: 0,
    }
    play = Hit(TARGET, ATK(FRIENDLY_HERO))


class TRL_241:
    """Gonk, the Raptor / 贡克，迅猛龙之神
    在你的英雄攻击并消灭一个随从后，便可再次攻击。"""

    # After your hero attacks and_kills a minion, it may_attack again.
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & ExtraAttack(SELF)
    )


class TRL_341:
    """Treespeaker / 树语者
    战吼： 将你的所有树人变形成为5/5的古树。"""

    # <b>Battlecry:</b> Transform your Treants into 5/5 Ancients.
    play = Morph(FRIENDLY_MINIONS + TREANT, "TRL_341t")


class TRL_343:
    """Wardruid Loti / 战争德鲁伊罗缇
    抉择：变形成为罗缇的四种恐龙形态之一。"""

    # <b>Choose One - </b>Transform into one of Loti's four dinosaur forms.
    choose = ("TRL_343at2", "TRL_343bt2", "TRL_343ct2", "TRL_343dt2")
    play = (ChooseBoth(CONTROLLER), Morph(SELF, "TRL_343et1"))


class TRL_343at2:
    play = Morph(SELF, "TRL_343at1")


class TRL_343bt2:
    play = Morph(SELF, "TRL_343bt1")


class TRL_343ct2:
    play = Morph(SELF, "TRL_343ct1")


class TRL_343dt2:
    play = Morph(SELF, "TRL_343dt1")


##
# Spells


class TRL_243:
    """Pounce / 飞扑
    在本回合中，使你的英雄获得+2攻击力。"""

    # Give your hero +2_Attack this turn.
    play = Buff(FRIENDLY_HERO, "TRL_243e")


TRL_243e = buff(atk=2)


class TRL_244:
    """Predatory Instincts / 掠食本能
    从你的牌库中抽一张野兽牌。将其生命值翻倍。"""

    # [x]Draw a Beast from your deck. Double its Health.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "TRL_244e", max_health=CURRENT_HEALTH(ForceDraw.TARGET))
    )


class TRL_254:
    """Mark of the Loa / 神灵印记
    抉择： 使一个随从获得+2/+4和嘲讽；或者召唤两个3/2的迅猛龙。"""

    # <b>Choose One</b> - Give a minion +2/+4 and <b>Taunt</b>; or Summon two 3/2 Raptors.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    choose = ("TRL_254a", "TRL_254b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(TARGET, "TRL_254ae"),
        Summon(CONTROLLER, "TRL_254t") * 2,
    )


class TRL_254a:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "TRL_254ae")


TRL_254ae = buff(+2, +4, taunt=True)


class TRL_254b:
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "TRL_254t") * 2


class TRL_255:
    """Stampeding Roar / 狂奔怒吼
    随机从你的手牌中召唤一个野兽，并使其获得突袭。"""

    # Summon a random Beast from your hand and give it <b>Rush</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_FRIENDLY_MINION_OF_RACE_IN_HAND: 20,
    }
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + BEAST)).then(
        Buff(Summon.CARD, "TRL_255e")
    )


TRL_255e = buff(rush=True)
