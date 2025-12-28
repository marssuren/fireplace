from ..utils import *


##
# Minions


class TRL_071:
    """Bloodsail Howler / 血帆啸猴
    突袭，战吼：你每控制一个其他海盗，便获得+1/+1。"""

    # [x]<b>Rush</b> <b>Battlecry:</b> Gain +1/+1 for each other Pirate you control.
    play = Buff(SELF, "TRL_071e") * Count(FRIENDLY_MINIONS + PIRATE)


TRL_071e = buff(+1, +1)


class TRL_077:
    """Gurubashi Hypemon / 古拉巴什宣传员
    战吼： 发现一张具有战吼的随从牌的1/1复制，其法力值消耗为（1）点。"""

    # <b>Battlecry:</b> <b>Discover</b> a 1/1 copy of a <b>Battlecry</b> minion. It costs
    # (1).
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Discover(CONTROLLER, RandomMinion(battlecry=True)).then(
        Give(CONTROLLER, MultiBuff(Discover.CARD, ["TRL_077e", "GBL_001e"]))
    )


class TRL_077e:
    atk = SET(1)
    max_health = SET(1)


class TRL_092:
    """Spirit of the Shark / 鲨鱼之灵
    潜行一回合。你的随从的战吼和连击触发两次。"""

    # [x]<b>Stealth</b> for 1 turn. Your minions' <b>Battlecries</b> __and <b>Combos</b>
    # trigger twice._
    events = (OWN_TURN_BEGIN.on(Unstealth(SELF)),)
    update = (
        Refresh(CONTROLLER, {enums.MINION_EXTRA_BATTLECRIES: True}),
        Refresh(CONTROLLER, {enums.MINION_EXTRA_COMBOS: True}),
    )


class TRL_126:
    """Captain Hooktusk / 钩牙船长
    战吼：从你的牌库中召唤三个海盗，并使其获得突袭。"""

    # <b>Battlecry:</b> Summon 3 Pirates from your deck. Give them <b>Rush</b>.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + PIRATE) * 3).then(
        GiveRush(Summon.CARD)
    )


class TRL_409:
    """Gral, the Shark / 格罗尔，鲨鱼之神
    战吼：吞食一个你的牌库中的随从，并获得其属性值。亡语：将被吞食的随从置入手牌。"""

    # [x]<b>Battlecry:</b> Eat a minion in your deck and gain its stats.
    # <b>Deathrattle:</b> Add it to your hand.
    play = Find(FRIENDLY_DECK + MINION) & (
        Retarget(SELF, RANDOM(FRIENDLY_DECK + MINION)),
        Reveal(TARGET),
        Destroy(TARGET),
        Buff(SELF, "TRL_409e", atk=ATK(TARGET), max_health=CURRENT_HEALTH(TARGET)),
    )
    deathrattle = HAS_TARGET & Give(CONTROLLER, Copy(TARGET))


##
# Spells


class TRL_124:
    """Raiding Party / 团伙劫掠
    从你的牌库中抽两张海盗牌。 连击：并抽一张 武器牌。"""

    # Draw 2 Pirates from_your deck. <b>Combo:</b> And a weapon.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE) * 2)
    combo = (
        ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE) * 2),
        ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON)),
    )


class TRL_127:
    """Cannon Barrage / 火炮弹幕
    随机对一个敌人造成$3点伤害。你每有一个海盗，就重复 一次。"""

    # [x]Deal $3 damage to a random enemy. Repeat for each of your Pirates.
    play = Hit(RANDOM_ENEMY_CHARACTER, 3) * (Count(FRIENDLY_MINIONS + PIRATE) + 1)


class TRL_156:
    """Stolen Steel / 盗取武器
    发现一张（另一职业的） 武器牌。"""

    # <b>Discover</b> a weapon <i>(from another class)</i>.
    play = GenericChoice(CONTROLLER, RandomWeapon(card_class=ANOTHER_CLASS) * 3)


class TRL_157:
    """Walk the Plank / 走跳板
    消灭一个未受伤的随从。"""

    # Destroy an undamaged minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET)


##
# Weapons


class TRL_074:
    """Serrated Tooth / 锯刃齿
    亡语：使你的所有随从获得突袭。"""

    # <b>Deathrattle:</b> Give your minions <b>Rush</b>.
    deathrattle = Buff(FRIENDLY_MINIONS, "TRL_074e")


TRL_074e = buff(rush=True)
