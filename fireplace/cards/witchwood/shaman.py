from ..utils import *


##
# Minions


class GIL_530:
    """Murkspark Eel / 阴燃电鳗
    战吼： 如果你的牌库中只有法力值消耗为偶数的牌，造成2点伤害。"""

    # <b>Battlecry:</b> If your deck has only even-Cost cards, deal_2 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_ONLY_EVEN_COST_CARD_IN_DECK: 0,
    }
    powered_up = EvenCost(FRIENDLY_DECK)
    play = powered_up & Hit(TARGET, 2)


class GIL_531:
    """Witch's Apprentice / 女巫的学徒
    嘲讽，战吼：随机将一张萨满祭司法术牌置入你的手牌。"""

    # <b>Taunt</b> <b>Battlecry:</b> Add a random Shaman spell to your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))


class GIL_583:
    """Totem Cruncher / 图腾啃食者
    嘲讽，战吼：消灭你的所有图腾。每消灭一个图腾，便获得+2/+2。"""

    # <b>Taunt</b> <b>Battlecry:</b> Destroy your Totems. Gain +2/+2 for each destroyed.
    play = Destroy(FRIENDLY_MINIONS + TOTEM).then(Buff(SELF, "GIL_583e"))


GIL_583e = buff(+2, +2)


class GIL_807:
    """Bogshaper / 塑沼者
    每当你施放一个法术，从你的牌库中抽一张随从牌。"""

    # Whenever you cast a spell, draw a minion from your_deck.
    events = Play(CONTROLLER, SPELL).after(ForceDraw(FRIENDLY_DECK + MINION))


class GIL_820:
    """Shudderwock / 沙德沃克
    战吼：重复在本局对战中你所使用过的所有其他卡牌的战吼效果（目标随机而定）。"""

    # [x]<b>Battlecry:</b> Repeat all other <b>Battlecries</b> from cards you played this
    # game <i>(targets chosen randomly)</i>.
    def play(self):
        sel = RANDOM(CARDS_PLAYED_THIS_GAME + BATTLECRY - ID("GIL_820")) * 30
        entities = sel.eval(self.game, self)
        for entity in entities:
            yield ExtraBattlecry(entity, None)
            while self.controller.choice:
                choice = self.game.random.choice(self.controller.choice.cards)
                log.info("Choosing card %r" % (choice))
                self.controller.choice.choose(choice)
            yield Deaths()
            if self.dead or self.silenced or self.zone != Zone.PLAY:
                break


##
# Spells


class GIL_586:
    """Earthen Might / 大地之力
    使一个随从获得+2/+2。如果该随从是元素，则随机将一张元素牌置入你的手牌。"""

    # [x]Give a minion +2/+2. If it's an Elemental, add a random Elemental to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(TARGET, "GIL_586e"),
        Find(TARGET + ELEMENTAL) & Give(CONTROLLER, RandomElemental()),
    )


GIL_586e = buff(+2, +2)


class GIL_600:
    """Zap! / 电击
    对一个随从造成$2点伤害。过载：（1）"""

    # Deal $2 damage to a minion. <b>Overload:</b> (1)
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class GIL_836:
    """Blazing Invocation / 炽焰祈咒
    发现一张战吼随从牌，其法力值消耗减少（1）点。"""

    # <b>Discover</b> a <b>Battlecry</b> minion.
    play = DISCOVER(RandomMinion(battlecry=True))


##
# Heros


class GIL_504:
    """Hagatha the Witch / 女巫哈加莎
    战吼：对所有随从造成3点伤害。"""

    # <b>Battlecry:</b> Deal 3 damage to all minions.
    play = Hit(ALL_MINIONS, 3)


class GIL_504h:
    """Bewitch"""

    # [x]<b>Passive Hero Power</b> After you play a minion, add a random Shaman spell to
    # your hand.
    tags = {enums.PASSIVE_HERO_POWER: True}
    events = Play(CONTROLLER, MINION).on(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))
    )
