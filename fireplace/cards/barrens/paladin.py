"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_550:
    """Galloping Savior - 迅疾救兵
    Secret: After your opponent plays three cards in a turn, summon a 3/4 Steed with Taunt.
    奥秘：在你的对手于一个回合中打出三张牌后，召唤一个3/4并具有嘲讽的战马。
    """
    secret = Play(OPPONENT).on(
        AddProgress(SELF, SELF, 1),
        (Count(SELF) >= 3) & (
            Reveal(SELF),
            Summon(CONTROLLER, "BAR_550t"),
        )
    )


class BAR_871:
    """Soldier's Caravan - 士兵车队
    At the start of your turn, summon two 1/1 Silver Hand Recruits.
    在你的回合开始时，召唤两个1/1的白银之手新兵。
    """
    events = OWN_TURN_BEGIN.on(Summon(CONTROLLER, "CS2_101t") * 2)


class BAR_873:
    """Knight of Anointment - 圣礼骑士
    Battlecry: Draw a Holy spell.
    战吼：抽一张神圣法术牌。
    """
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + HOLY))


class BAR_875:
    """Sword of the Fallen - 逝者之剑
    After your hero attacks, cast a Secret from your deck.
    在你的英雄攻击后，从你的牌库中施放一张奥秘牌。
    """
    events = Attack(FRIENDLY_HERO).after(
        CastSpell(RANDOM(FRIENDLY_DECK + SECRET))
    )


class BAR_876:
    """Northwatch Commander - 北卫军指挥官
    Battlecry: If you control a Secret, draw a minion.
    战吼：如果你控制一个奥秘，抽一张随从牌。
    """
    play = Find(FRIENDLY_SECRETS) & ForceDraw(RANDOM(FRIENDLY_DECK + MINION))


class BAR_878:
    """Veteran Warmedic - 战地医师老兵
    After you cast a Holy spell, summon a 2/2 Medic with Lifesteal.
    在你施放一个神圣法术后，召唤一个2/2并具有吸血的医师。
    """
    events = Play(CONTROLLER, SPELL + HOLY).after(
        Summon(CONTROLLER, "BAR_878t")
    )


class BAR_879:
    """Cannonmaster Smythe - 火炮长斯密瑟
    Battlecry: Transform your Secrets into 3/3 Soldiers. They transform back when they die.
    战吼：将你的奥秘变形成为3/3的士兵。它们死亡时会变回奥秘。
    """
    play = Morph(FRIENDLY_SECRETS, "BAR_879t")


class BAR_879t:
    """Soldier (from Secret)"""
    deathrattle = Summon(CONTROLLER, PARENT_CARD)


class BAR_880:
    """Conviction (Rank 1) - 定罪（等级1）
    Give a random friendly minion +3 Attack. (Upgrades when you have 5 Mana.)
    随机使一个友方随从获得+3攻击力。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_880t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(RANDOM_FRIENDLY_MINION, "BAR_880e")


class BAR_880e:
    tags = {
        GameTag.ATK: 3,
    }


class BAR_880t:
    """Conviction (Rank 2) - 定罪（等级2）
    Give 2 random friendly minions +3 Attack. (Upgrades when you have 10 Mana.)
    随机使两个友方随从获得+3攻击力。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_880t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(RANDOM_FRIENDLY_MINION * 2, "BAR_880t_e")


class BAR_880t_e:
    tags = {
        GameTag.ATK: 3,
    }


class BAR_880t2:
    """Conviction (Rank 3) - 定罪（等级3）
    Give 3 random friendly minions +3 Attack.
    随机使三个友方随从获得+3攻击力。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(RANDOM_FRIENDLY_MINION * 3, "BAR_880t2_e")


class BAR_880t2_e:
    tags = {
        GameTag.ATK: 3,
    }


class BAR_881:
    """Invigorating Sermon - 动员布道
    Give +1/+1 to all minions in your hand, deck, and battlefield.
    使你手牌、牌库和战场上的所有随从牌获得+1/+1。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(FRIENDLY_HAND + MINION, "BAR_881e"),
        Buff(FRIENDLY_DECK + MINION, "BAR_881e"),
        Buff(FRIENDLY_MINIONS, "BAR_881e"),
    )


class BAR_881e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
    }


class BAR_902:
    """Cariel Roame - 凯瑞尔·罗姆
    Rush, Divine Shield. Whenever this attacks, reduce the Cost of Holy spells in your hand by (1).
    突袭，圣盾。每当该随从攻击时，使你手牌中的神圣法术牌的法力值消耗减少（1）点。
    """
    events = Attack(SELF).on(
        Buff(FRIENDLY_HAND + SPELL + HOLY, "BAR_902e")
    )


class BAR_902e:
    tags = {
        GameTag.COST: -1,
    }


class WC_032:
    """Seedcloud Buckler - 淡云圆盾
    Deathrattle: Give your minions Divine Shield.
    亡语：使你的随从获得圣盾。
    """
    deathrattle = GiveDivineShield(FRIENDLY_MINIONS)


class WC_033:
    """Judgment of Justice - 公正审判
    Secret: When an enemy minion attacks, set its Attack and Health to 1.
    奥秘：当一个敌方随从攻击时，将其攻击力和生命值设置为1。
    """
    secret = Attack(ENEMY + MINION).on(
        Reveal(SELF),
        SetTag(Attack.ATTACKER, GameTag.ATK, 1),
        SetCurrentHealth(Attack.ATTACKER, 1),
    )


class WC_034:
    """Party Up! - 小队集合
    Summon five 2/2 Adventurers with random bonus effects.
    召唤五个2/2并具有随机奖励效果的冒险者。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RandomID("WC_034t", "WC_034t2", "WC_034t3", "WC_034t4")) * 5


