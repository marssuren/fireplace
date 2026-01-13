"""贫瘠之地的锤炼（Forged in the Barrens）卡牌实现"""
from ..utils import *


class BAR_307:
    """Void Flayer - 剥灵者
    Battlecry: For each spell in your hand, deal 1 damage to a random enemy minion.
    战吼：你手牌中每有一张法术牌，便对一个随机敌方随从造成1点伤害。
    """
    play = Hit(RANDOM_ENEMY_MINION, 1) * Count(FRIENDLY_HAND + SPELL)


class BAR_308:
    """Power Word: Fortitude - 真言术：韧
    Give a minion +3/+5. Costs (1) less for each spell in your hand.
    使一个随从获得+3/+5。你手牌中每有一张法术牌，本牌的法力值消耗便减少（1）点。
    """
    cost_mod = -Count(FRIENDLY_HAND + SPELL)
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BAR_308e")


class BAR_308e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 5,
    }


class BAR_309:
    """Desperate Prayer - 绝望祷言
    Restore #5 Health to each hero.
    为每个英雄恢复#5点生命值。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Heal(ALL_HEROES, 5)


class BAR_310:
    """Lightshower Elemental - 光沐元素
    Taunt. Deathrattle: Restore #8 Health to all friendly characters.
    嘲讽。亡语：为所有友方角色恢复#8点生命值。
    """
    deathrattle = Heal(FRIENDLY_CHARACTERS, 8)


class BAR_311:
    """Devouring Plague - 噬灵疫病
    Lifesteal. Deal $4 damage randomly split among all enemy minions.
    吸血。造成$4点伤害，随机分配到所有敌方随从身上。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(RANDOM_ENEMY_MINION, 1) * 4


class BAR_312:
    """Soothsayer's Caravan - 占卜者车队
    At the start of your turn, copy a spell from your opponent's deck to your hand.
    在你的回合开始时，从你对手的牌库中复制一张法术牌到你的手牌。
    """
    events = OWN_TURN_BEGIN.on(
        Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK + SPELL)))
    )


class BAR_313:
    """Priest of An'she - 安瑟祭司
    Taunt. Battlecry: If you've restored Health this turn, gain +3/+3.
    嘲讽。战吼：如果你在本回合中恢复过生命值，获得+3/+3。
    """
    powered_up = HEALED_THIS_TURN(CONTROLLER) > 0
    play = powered_up & Buff(SELF, "BAR_313e")


class BAR_313e:
    tags = {
        GameTag.ATK: 3,
        GameTag.HEALTH: 3,
    }


class BAR_314:
    """Condemn (Rank 1) - 罪罚（等级1）
    Deal $1 damage to all enemy minions. (Upgrades when you have 5 Mana.)
    对所有敌方随从造成$1点伤害。（在你有5点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_314t",
        enums.RANKED_SPELL_THRESHOLD: 5,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(ENEMY_MINIONS, 1)


class BAR_314t:
    """Condemn (Rank 2) - 罪罚（等级2）
    Deal $2 damage to all enemy minions. (Upgrades when you have 10 Mana.)
    对所有敌方随从造成$2点伤害。（在你有10点法力值时升级。）
    """
    tags = {
        enums.RANKED_SPELL_NEXT_RANK: "BAR_314t2",
        enums.RANKED_SPELL_THRESHOLD: 10,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(ENEMY_MINIONS, 2)


class BAR_314t2:
    """Condemn (Rank 3) - 罪罚（等级3）
    Deal $3 damage to all enemy minions.
    对所有敌方随从造成$3点伤害。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(ENEMY_MINIONS, 3)


class BAR_315:
    """Serena Bloodfeather - 塞瑞娜·血羽
    Battlecry: Choose an enemy minion. Steal Attack and Health from it until this has more.
    战吼：选择一个敌方随从。从其身上窃取攻击力和生命值，直到该随从的属性值更高。
    """
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = (
        # 窃取攻击力直到自己更高
        ((ATK(TARGET) >= ATK(SELF)) & (
            Buff(SELF, "BAR_315e", atk=ATK(TARGET) - ATK(SELF) + 1),
            Buff(TARGET, "BAR_315e2", atk=-(ATK(TARGET) - ATK(SELF) + 1)),
        )),
        # 窃取生命值直到自己更高
        ((HEALTH(TARGET) >= HEALTH(SELF)) & (
            Buff(SELF, "BAR_315e3", max_health=HEALTH(TARGET) - HEALTH(SELF) + 1),
            Buff(TARGET, "BAR_315e4", max_health=-(HEALTH(TARGET) - HEALTH(SELF) + 1)),
        )),
    )


class BAR_315e:
    """Stolen Attack"""
    pass


class BAR_315e2:
    """Lost Attack"""
    pass


class BAR_315e3:
    """Stolen Health"""
    pass


class BAR_315e4:
    """Lost Health"""
    pass


class BAR_735:
    """Xyrella - 泽瑞拉
    Battlecry: If you've restored Health this turn, deal that much damage to all enemy minions.
    战吼：如果你在本回合中恢复过生命值，对所有敌方随从造成等同于恢复量的伤害。
    """
    play = (HEALED_THIS_TURN(CONTROLLER) > 0) & Hit(ENEMY_MINIONS, HEALED_THIS_TURN(CONTROLLER))


class WC_013:
    """虚诚地下城历险家 - Devout Dungeoneer
    Battlecry: Draw a spell. If it's a Holy spell, reduce its Cost by (2).
    战吼：抽一张法术牌。如果是神圣法术，使其法力值消耗减少（2）点。
    """
    def play(self):
        cards = yield ForceDraw(CONTROLLER, FRIENDLY_DECK + SPELL)
        if cards:
            for card in cards:
                if card and card.spell_school == SpellSchool.HOLY:
                    yield Buff(card, "WC_013e")


class WC_013e:
    tags = {
        GameTag.COST: -2,
    }


class WC_014:
    """除奇致胜 - Against All Odds
    Destroy ALL odd-Attack minions.
    摧毁所有攻击力为奇数的随从。
    """
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(FuncSelector(lambda entities, src: [e for e in entities if hasattr(e, 'atk') and e.atk % 2 == 1]) + ALL_MINIONS)


class WC_803:
    """Cleric of An'she - 安瑟教士
    Battlecry: If you've restored Health this turn, Discover a spell from your deck.
    战吼：如果你在本回合中恢复过生命值，从你的牌库中发现一张法术牌。
    """
    play = (HEALED_THIS_TURN(CONTROLLER) > 0) & DISCOVER(FRIENDLY_DECK + SPELL)


