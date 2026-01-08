from ..utils import *


##
# Minions


class OG_109:
    """Darkshire Librarian / 夜色镇图书管理员
    战吼： 随机弃一张牌。 亡语： 抽一张牌。"""

    play = Discard(RANDOM(FRIENDLY_HAND))
    deathrattle = Draw(CONTROLLER)


class OG_113:
    """Darkshire Councilman / 夜色镇议员
    在你召唤一个随从后，获得+1攻击力。"""

    events = Summon(CONTROLLER, MINION).on(Buff(SELF, "OG_113e"))


OG_113e = buff(atk=1)


class OG_121:
    """Cho'gall / 古加尔
    战吼：将你在本局对战中弃掉的所有牌移回你的手牌，这些牌会消耗生命值而非法力值。"""

    play = Buff(CONTROLLER, "OG_121e")


class OG_121e:
    events = OWN_SPELL_PLAY.on(Destroy(SELF))
    update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class OG_241:
    """Possessed Villager / 着魔村民
    亡语：召唤一个1/1的暗影兽。"""

    deathrattle = Summon(CONTROLLER, "OG_241a")


class OG_302:
    """Usher of Souls / 渡魂者
    每当一个随从死亡，使你的克苏恩获得+1/+1（无论它在哪里）。"""

    events = Death(FRIENDLY_MINIONS).on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


##
# Spells


class OG_116:
    """Spreading Madness / 狂乱传染
    造成$13点伤害，随机分配到所有角色身上。"""

    play = Hit(RANDOM_CHARACTER, 1) * 13


class OG_118:
    """Renounce Darkness / 弃暗投明
    将你的英雄技能和术士卡牌替换成另一职业的。这些牌的法力值消耗减少（1）点。"""

    def play(self):
        classes = [
            (CardClass.DEMONHUNTER, "HERO_10bp"),
            (CardClass.DRUID, "HERO_06bp"),
            (CardClass.HUNTER, "HERO_05bp"),
            (CardClass.MAGE, "HERO_08bp"),
            (CardClass.PALADIN, "HERO_04bp"),
            (CardClass.PRIEST, "HERO_09bp"),
            (CardClass.ROGUE, "HERO_03bp"),
            (CardClass.SHAMAN, "HERO_02bp"),
            (CardClass.WARRIOR, "HERO_01bp"),
        ]
        hero_class, hero_power = self.game.random.choice(classes)
        yield Summon(CONTROLLER, hero_power)
        yield Morph(
            FRIENDLY + WARLOCK + (IN_HAND | IN_DECK),
            RandomCollectible(card_class=hero_class),
        ).then(Buff(Morph.CARD, "OG_118f"))


class OG_118f:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class OG_239:
    """DOOM! / 末日降临
    消灭所有随从。每消灭一个随从，便抽一张牌。"""

    def play(self):
        minion_count = Count(ALL_MINIONS).evaluate(self)
        yield Destroy(ALL_MINIONS)
        yield Draw(CONTROLLER) * minion_count


class OG_114:
    """Forbidden Ritual / 禁忌仪式
    消耗你所有的法力值，召唤相同数量的1/1的触须。"""

    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
        Summon(CONTROLLER, "OG_114a") * SpendMana.AMOUNT
    )
