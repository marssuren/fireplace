from ..utils import *


##
# Minions


class BT_187:
    """Kayn Sunfury / 凯恩·日怒
    冲锋 所有友方攻击无视 嘲讽。"""

    # <b>Charge</b> All friendly attacks ignore_<b>Taunt</b>.
    update = Refresh(FRIENDLY_MINIONS, {GameTag.IGNORE_TAUNT: True})


class BT_321:
    """Netherwalker / 虚无行者
    战吼： 发现一张恶魔牌。"""

    # <b>Battlecry:</b> <b>Discover</b> a Demon.
    play = DISCOVER(RandomDemon())


class BT_480:
    """Crimson Sigil Runner / 火色魔印奔行者
    流放：抽一张牌。"""

    # <b>Outcast:</b> Draw a card.
    outcast = Draw(CONTROLLER)


class BT_486:
    """Pit Commander / 深渊指挥官
    嘲讽 在你的回合结束时，从你的牌库中召唤一个恶魔。"""

    # <b>Taunt</b> At the end of your turn, summon a Demon from your deck.
    events = OWN_TURN_END.on(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + DEMON)))


class BT_493:
    """Priestess of Fury / 愤怒的女祭司
    在你的回合结束时，造成6点伤害，随机分配到所有敌人身上。"""

    # At the end of your turn, deal 6 damage randomly split among all enemies.
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 1) * 6)


class BT_496:
    """Furious Felfin / 暴怒的邪鳍
    战吼：在本回合中，如果你的英雄进行过攻击，则获得+1攻击力和突袭。"""

    # [x]<b>Battlecry:</b> If your hero attacked this turn, gain +1 Attack and
    # <b>Rush</b>.
    powered_up = NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) > 0
    play = powered_up & Buff(SELF, "BT_496e")


BT_496e = buff(atk=1, rush=True)


class BT_509:
    """Fel Summoner / 邪能召唤师
    亡语：随机从你的手牌中召唤一个恶魔。"""

    # <b>Deathrattle:</b> Summon a random Demon from your_hand.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON))


class BT_761:
    """Coilfang Warlord / 盘牙督军
    突袭，亡语：召唤一个5/9并具有嘲讽 的督军。"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Summon a 5/9 Warlord with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "BT_761t")


class BT_934:
    """Imprisoned Antaen / 被禁锢的安塔恩
    休眠2回合。 唤醒时，造成10点伤害，随机分配到所有敌人身上。"""

    # [x]<b>Dormant</b> for 2 turns. When this awakens, deal 10 damage randomly
    # split among all enemies.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Hit(RANDOM_ENEMY_CHARACTER, 1) * 10


##
# Spells


class BT_429:
    """Metamorphosis / 恶魔变形
    将你的英雄技能替换为“造成5点伤害。”使用两次后，换回原技能。"""

    # Swap your Hero Power to "Deal 4 damage." After 2 uses, swap it back.
    play = Switch(
        FRIENDLY_HERO_POWER,
        {
            "BT_429p": (),
            "BT_429p2": (
                SetTags(
                    SELF,
                    {
                        GameTag.TAG_SCRIPT_DATA_ENT_1: GetTag(
                            FRIENDLY_HERO_POWER, GameTag.TAG_SCRIPT_DATA_ENT_1
                        )
                    },
                ),
                Summon(CONTROLLER, "BT_429p").then(
                    SetTags(
                        Summon.CARD,
                        {
                            GameTag.TAG_SCRIPT_DATA_ENT_1: GetTag(
                                SELF, GameTag.TAG_SCRIPT_DATA_ENT_1
                            )
                        },
                    )
                ),
                UnsetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1),
            ),
            None: (
                SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_ENT_1: FRIENDLY_HERO_POWER}),
                Summon(CONTROLLER, "BT_429p").then(
                    SetTags(
                        Summon.CARD,
                        {
                            GameTag.TAG_SCRIPT_DATA_ENT_1: GetTag(
                                SELF, GameTag.TAG_SCRIPT_DATA_ENT_1
                            )
                        },
                    )
                ),
                UnsetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1),
            ),
        },
    )


class BT_429p:
    """Demonic Blast"""

    # [x]<b>Hero Power</b> Deal $4 damage. <i>(Two uses left!)</i>
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = (
        Hit(TARGET, 4),
        Summon(CONTROLLER, "BT_429p2").then(
            SetTags(
                Summon.CARD,
                {
                    GameTag.TAG_SCRIPT_DATA_ENT_1: GetTag(
                        SELF, GameTag.TAG_SCRIPT_DATA_ENT_1
                    ),
                    enums.ACTIVATIONS_THIS_TURN: Attr(SELF, enums.ACTIVATIONS_THIS_TURN)
                    + 1,
                },
            ),
        ),
    )


class BT_429p2:
    """Demonic Blast"""

    # [x]<b>Hero Power</b> Deal $4 damage. <i>(Last use!)</i>
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = (
        Hit(TARGET, 4),
        Summon(CONTROLLER, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1)),
        RefreshHeroPower(FRIENDLY_HERO_POWER),
    )


class BT_491:
    """Spectral Sight / 幽灵视觉
    抽一张牌。流放：再抽一张。"""

    # [x]Draw a card. <b>Outcast:</b> Draw another.
    play = Draw(CONTROLLER)
    outcast = Draw(CONTROLLER) * 2


class BT_514:
    """Immolation Aura / 献祭光环
    对所有随从造成$1点伤害两次。"""

    # Deal $1 damage to all minions twice.
    play = Hit(ALL_MINIONS, 1) * 2


class BT_601:
    """Skull of Gul'dan / 古尔丹之颅
    抽三张牌。流放：这些牌的法力值消耗减少（3）点。"""

    # Draw 3 cards. <b>Outcast:</b> Reduce their Cost by (3).
    play = Draw(CONTROLLER) * 3
    outcast = Draw(CONTROLLER).then(Buff(Draw.CARD, "BT_601e")) * 3


class BT_601e:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY


##
# Weapons


class BT_430:
    """Warglaives of Azzinoth / 埃辛诺斯战刃
    在攻击一个随从后，你的英雄可以再次攻击。"""

    # After attacking a minion, your hero may attack again.
    events = Attack(FRIENDLY_HERO, MINION).after(ExtraAttack(FRIENDLY_HERO))
