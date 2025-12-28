from ..utils import *


##
# Minions


class BT_351:
    """Battlefiend / 战斗邪犬
    在你的英雄攻击后，获得+1攻击力。"""

    # After your hero attacks, gain +1 Attack.
    events = Attack(FRIENDLY_HERO).after(Buff(CONTROLLER, "BT_351e"))


BT_351e = buff(atk=1)


class BT_355:
    """Wrathscale Naga / 怒鳞纳迦
    在一个友方随从死亡后，随机对一个敌人造成3点伤害。"""

    # After a friendly minion dies, deal 3 damage to a_random enemy.
    events = Death(FRIENDLY + MINION).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class BT_407:
    """Ur'zul Horror / 乌祖尔恐魔
    亡语：将一张2/1的“迷失之魂”置入你的 手牌。"""

    # <b>Deathrattle:</b> Add a 2/1 Lost Soul to your hand.
    deathrattle = Give(CONTROLLER, "BT_407t")


class BT_416:
    """Raging Felscreamer / 暴怒邪吼者
    战吼：你的下一张恶魔牌的法力值消耗减少（2）点。"""

    # <b>Battlecry:</b> The next Demon you play costs (2) less.
    play = Buff(CONTROLLER, "BT_416e")


class BT_416e:
    update = Refresh(FRIENDLY_HAND + DEMON, {GameTag.COST: -2})
    events = Play(CONTROLLER, DEMON).on(Destroy(SELF))


class BT_481:
    """Nethrandamus / 奈瑟兰达姆斯
    战吼：随机召唤两个法力值消耗为（@）的随从。 （每有一个友方随从死亡都会升级！）"""

    # [x]<b>Battlecry:</b> Summon two random @-Cost minions. <i>(Upgrades each
    # time a friendly minion dies!)</i>
    class Hand:
        events = Death(FRIENDLY + MINION).on(AddProgress(SELF, Death.ENTITY))

    play = SummonBothSides(
        CONTROLLER, RandomMinion(cost=Min(Attr(SELF, GameTag.QUEST_PROGRESS), 10))
    )


class BT_487:
    """Hulking Overfiend / 巨型大恶魔
    突袭 在本随从攻击并消灭一个随从后，可再次攻击。"""

    # <b>Rush</b>. After this attacks and kills a minion, it may_attack again.
    events = Attack(SELF, ALL_MINIONS).after(Dead(Attack.DEFENDER) & ExtraAttack(SELF))


class BT_510:
    """Wrathspike Brute / 怒刺蛮兵
    嘲讽 在本随从被攻击后，对所有敌人造成1点伤害。"""

    # [x]<b>Taunt</b> After this is attacked, deal 1 damage to all enemies.
    events = Attack(SELF).after(Hit(ENEMY_CHARACTERS, 1))


class BT_814:
    """Illidari Felblade / 伊利达雷邪刃武士
    突袭 流放：在本回合中获得免疫。"""

    # <b>Rush</b> <b>Outcast:</b> Gain <b>Immune</b> this_turn.
    outcast = Buff(SELF, "BT_814e")


BT_814e = buff(immune=True)


class BT_937:
    """Altruis the Outcast / 流放者奥图里斯
    在你使用最左或最右边的一张手牌后，对所有敌人造成1点 伤害。"""

    # [x]After you play the left- or right-most card in your hand, deal 1
    # damage to all enemies.
    events = Play(CONTROLLER, PLAY_OUTCAST).after(Hit(ENEMY_CHARACTERS, 1))


##
# Spells


class BT_173:
    """Command the Illidari / 统率伊利达雷
    召唤六个1/1并具有突袭的伊利达雷。"""

    # Summon six 1/1_Illidari with <b>Rush</b>.
    play = Summon(CONTROLLER, "BT_036t") * 6


class BT_175:
    """Twin Slice / 双刃斩击
    在本回合中，使你的英雄获得+2攻击力。将“二次斩击”置入你的手牌。"""

    # Give your hero +2 Attack this turn. Add 'Second Slice' to your hand.
    play = Buff(FRIENDLY_HERO, "BT_175e"), Give(CONTROLLER, "BT_175t")


class BT_175t:
    """Second Slice"""

    # Give your hero +2_Attack this turn.
    play = Buff(FRIENDLY_HERO, "BT_175e")


BT_175e = buff(atk=2)


class BT_354:
    """Blade Dance / 刃舞
    随机对三个敌方随从造成等同于你的英雄攻击力的伤害。"""

    # Deal damage equal to your hero's Attack to 3 random enemy minions.
    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION * 3, ATK(FRIENDLY_HERO))


class BT_427:
    """Feast of Souls / 灵魂盛宴
    在本回合中每有一个友方随从死亡，抽一张牌。@（抽@张牌）"""

    # Draw a card for each friendly minion that died this turn.
    play = Draw(CONTROLLER) * Attr(CONTROLLER, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BT_488:
    """Soul Split / 灵魂分裂
    选择一个友方恶魔，召唤一个它的复制。"""

    # Choose a friendly Demon. Summon a copy of it.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


class BT_490:
    """Consume Magic / 吞噬魔法
    沉默一个敌方随从。流放：抽一张牌。"""

    # <b>Silence</b> an enemy_minion. <b>Outcast:</b> Draw a card.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Silence(TARGET)
    outcast = Silence(TARGET), Draw(CONTROLLER)


class BT_752:
    """Blur / 疾影
    在本回合中，你的英雄无法受到伤害。"""

    # Your hero can't take damage this turn.
    play = Buff(FRIENDLY_HERO, "BT_752e")


BT_752e = buff(immune=True)


class BT_753:
    """Mana Burn / 法力燃烧
    下个回合，你的对手减少两个法力水晶。"""

    # Your opponent has 2 fewer Mana Crystals next turn.
    play = Buff(OPPONENT, "BT_753e")


class BT_753e:
    events = BeginTurn(OPPONENT).on(ManaThisTurn(OWNER, -2)), Destroy(SELF)


class BT_801:
    """Eye Beam / 眼棱
    吸血。 对一个随从造成$3点伤害。流放：法力值消耗为（1）点。"""

    # <b>Lifesteal</b>. Deal $3 damage to a minion. <b>Outcast:</b> This costs
    # (1).
    class Hand:
        update = Find(SELF + OUTERMOST_HAND) & Refresh(SELF, {GameTag.COST: SET(1)})

    play = Hit(TARGET, 3)


##
# Weapons


class BT_271:
    """Flamereaper / 斩炎
    同时对其攻击目标相邻的随从 造成伤害。"""

    # Also damages the minions next to whomever your hero_attacks.
    events = Attack(FRIENDLY_HERO).on(
        Hit(ADJACENT(Attack.DEFENDER), ATK(FRIENDLY_HERO))
    )


class BT_922:
    """Umberwing / 棕红之翼
    战吼：召唤两只1/1的邪翼蝠。"""

    # <b>Battlecry:</b> Summon two 1/1 Felwings.
    play = Summon(CONTROLLER, "BT_922t") * 2
