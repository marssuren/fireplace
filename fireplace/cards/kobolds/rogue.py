from ..utils import *


##
# Minions


class LOOT_026:
    """Fal'dorei Strider / 法多雷突袭者
    战吼： 将三张伏击牌洗入你的牌库。 当抽到伏击牌时，召唤一只4/4的蜘蛛。"""

    # [x]<b>Battlecry:</b> Shuffle 3 Ambushes into your deck. When drawn, summon a 4/4
    # Spider.
    play = Shuffle(CONTROLLER, "LOOT_026e") * 3


class LOOT_026e:
    """Spider Ambush!"""

    # Summon a 4/4 Spider. Draw a card. Cast this when drawn.
    play = Summon(CONTROLLER, "LOOT_026t")
    draw = CAST_WHEN_DRAWN


class LOOT_033:
    """Cavern Shinyfinder / 洞穴探宝者
    战吼：从你的牌库中抽一张武器牌。"""

    # <b>Battlecry:</b> Draw a weapon from your deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON))


class LOOT_165:
    """Sonya Shadowdancer / 影舞者索尼娅
    在一个友方随从死亡后，将它的1/1复制置入你的手牌，其法力值消耗变为（1）点。"""

    # After a friendly minion dies, add a 1/1 copy of it to your hand. It costs (1).
    events = Death(FRIENDLY + MINION).on(
        Give(CONTROLLER, MultiBuff(Copy(Death.ENTITY), ["LOOT_165e", "GBL_001e"]))
    )


class LOOT_165e:
    atk = SET(1)
    max_health = SET(1)


class LOOT_211:
    """Elven Minstrel / 精灵咏唱者
    连击：从你的牌库中抽两张随从牌。"""

    # <b>Combo:</b> Draw 2 minions from your deck.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    combo = ForceDraw(RANDOM(FRIENDLY_DECK + MINION))


class LOOT_412:
    """Kobold Illusionist / 狗头人幻术师
    亡语：从你的手牌中召唤一个随从的 1/1复制。"""

    # <b>Deathrattle:</b> Summon a 1/1 copy of a minion from your hand.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION)).then(
        Buff(Summon.CARD, "LOOT_412e")
    )


class LOOT_412e:
    atk = SET(1)
    max_health = SET(1)


##
# Spells


class LOOT_204:
    """Cheat Death / 诈死
    奥秘：当一个友方随从死亡时，将其移回你的手牌，它的法力值消耗减少（2）点。"""

    # <b>Secret:</b> When a friendly minion dies, return it to your hand. It costs (2)
    # less.
    secret = Death(FRIENDLY + MINION).on(
        Reveal(SELF), Bounce(Buff(Death.ENTITY, "LOOT_204e"))
    )


class LOOT_204e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class LOOT_210:
    """Sudden Betrayal / 叛变
    奥秘：当一个随从攻击你的英雄时，改为该随从攻击与其相邻的一个随从。"""

    # <b>Secret:</b> When a minion attacks your hero, instead it attacks one of_its
    # neighbors.
    secret = Attack(MINION, FRIENDLY_HERO).on(
        Find(ADJACENT(Attack.ATTACKER))
        & (Reveal(SELF), Retarget(Attack.ATTACKER, RANDOM(ADJACENT(Attack.ATTACKER))))
    )


class LOOT_214:
    """Evasion / 闪避
    奥秘：你的英雄在受到伤害后，在本回合中免疫。"""

    # <b>Secret:</b> After your hero takes damage, become <b>Immune</b> this turn.
    secret = Damage(FRIENDLY_HERO).on(Buff(FRIENDLY_HERO, "LOOT_214e"))


LOOT_214e = buff(immune=True)


class LOOT_503:
    """Lesser Onyx Spellstone / 小型法术黑曜石
    随机消灭一个敌方随从。@（使用三张亡语牌后升级。）"""

    # Destroy 1 random enemy minion. @<i>(Play 3 <b>Deathrattle</b> cards to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1,
    }
    play = Destroy(RANDOM_ENEMY_MINION)
    progress_total = 3
    reward = Morph(SELF, "LOOT_503t")

    class Hand:
        events = Play(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Play.CARD))


class LOOT_503t:
    """Onyx Spellstone"""

    # Destroy up to 2 random enemy minions. @
    requirements = {
        PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1,
    }
    play = Destroy(RANDOM_ENEMY_MINION * 2)
    progress_total = 3
    reward = Morph(SELF, "LOOT_503t")

    class Hand:
        events = Play(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Play.CARD))


class LOOT_503t2:
    """Greater Onyx Spellstone"""

    # Destroy up to 3 random enemy minions.
    requirements = {
        PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1,
    }
    play = Destroy(RANDOM_ENEMY_MINION * 3)


##
# Weapons


class LOOT_542:
    """Kingsbane / 弑君
    始终保留所有附加效果。亡语：将这把武器洗入你的牌库。"""

    # [x]<b>Deathrattle:</b> Shuffle this into your deck. It keeps any enchantments.
    tags = {enums.KEEP_BUFF: True}
    deathrattle = Shuffle(CONTROLLER, SELF)
