from ..utils import *


##
# Minions


class BOT_034:
    """Boommaster Flark / 爆破大师弗拉克
    战吼：召唤四个0/2的地精炸弹。"""

    # <b>Battlecry:</b> Summon four 0/2 Goblin Bombs.
    play = SummonBothSides(CONTROLLER, "BOT_031") * 4


class BOT_035:
    """Venomizer / 毒箭机器人
    磁力 剧毒"""

    # <b>Magnetic</b> <b>Poisonous</b>
    magnetic = MAGNETIC("BOT_035e")


BOT_035e = buff(poisonous=True)


class BOT_038:
    """Fireworks Tech / 焰火技师
    战吼：使一个友方机械获得+1/+1。如果它拥有亡语，则将其 触发。"""

    # [x]<b>Battlecry:</b> Give a friendly Mech +1/+1. If it has <b>Deathrattle</b>,
    # trigger it.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
    }
    play = (Buff(TARGET, "BOT_038e"), Find(TARGET + DEATHRATTLE) & Deathrattle(TARGET))


BOT_038e = buff(+1, +1)


class BOT_039:
    """Necromechanic / 死灵机械师
    你的亡语会触发 两次。"""

    # Your <b>Deathrattles</b> trigger twice.
    update = Refresh(CONTROLLER, {GameTag.EXTRA_DEATHRATTLES: True})


class BOT_251:
    """Spider Bomb / 蜘蛛炸弹
    磁力 亡语：随机消灭一个敌方随从。"""

    # <b>Magnetic</b> <b>Deathrattle:</b> Destroy a random_enemy_minion.
    magnetic = MAGNETIC("BOT_251e")
    deathrattle = Destroy(RANDOM(ENEMY_MINIONS))


class BOT_251e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Destroy(RANDOM(ENEMY_MINIONS))


##
# Spells


class BOT_033:
    """Bomb Toss / 投掷炸弹
    造成$2点伤害。召唤一个0/2的地精炸弹。"""

    # Deal $2 damage. Summon a 0/2 Goblin_Bomb.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), Summon(CONTROLLER, "BOT_031")


class BOT_402:
    """Secret Plan / 奥秘图纸
    发现一张奥秘牌。"""

    # <b>Discover</b> a <b>Secret</b>.
    play = WITH_SECRECTS & (DISCOVER(RandomSpell(secret=True))) | (
        DISCOVER(RandomSpell(secret=True, card_class=CardClass.HUNTER))
    )


class BOT_429:
    """Flark's Boom-Zooka / 弗拉克的火箭炮
    从你的牌库中召唤三个随从。他们会攻击敌方随从，然后死亡。"""

    # [x]Summon 3 minions from your deck. They attack enemy minions, then die.
    # 如果场上没有敌方随从，召唤的随从会直接死亡而不攻击
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
            Find(ENEMY_MINIONS) & Attack(Summon.CARD, RANDOM_ENEMY_MINION),
            Destroy(Summon.CARD)
        )
        * 3
    )


class BOT_437:
    """Goblin Prank / 地精的把戏
    使一个友方随从获得+3/+3和突袭，该随从会在回合结束时死亡。"""

    # Give a friendly minion +3/+3 and <b>Rush</b>. It_dies at end of turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_437e")


class BOT_437e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
        GameTag.RUSH: True,
    }
    events = OWN_TURN_END.on(Destroy(OWNER))


class BOT_438:
    """Cybertech Chip / 机核芯片
    使你的所有随从获得 “亡语：随机将一张机械牌置入你的手牌”。"""

    # Give your minions "<b>Deathrattle:</b> Add a random Mech to your_hand."
    play = Buff(FRIENDLY_MINIONS, "BOT_438e")


class BOT_438e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, RandomMech())
