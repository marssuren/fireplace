from ..utils import *


##
# Minions


class UNG_020:
    """Arcanologist / 秘法学家
    战吼：抽一张奥秘牌。"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + SECRET))


class UNG_021:
    """Steam Surger / 蒸汽涌动者
    战吼：如果你在上个回合使用过元素牌，将一张“烈焰喷涌”置入你的手牌。"""

    play = ELEMENTAL_PLAYED_LAST_TURN & Give(CONTROLLER, "UNG_018")


class UNG_027:
    """Pyros / 派烙斯
    亡语：将本随从移回你的手牌，并变为法力值消耗为（4）点的6/6随从牌。"""

    deathrattle = Give(CONTROLLER, SELF).then(Morph(SELF, "UNG_027t2"))


class UNG_027t2:
    deathrattle = Give(CONTROLLER, SELF).then(Morph(SELF, "UNG_027t4"))


class UNG_846:
    """Shimmering Tempest / 活体风暴
    战吼：随机将一张法师法术牌置入你的 手牌。"""

    deathrattle = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))


##
# Spells


class UNG_018:
    """Flame Geyser / 烈焰喷涌
    造成$2点伤害。 将一张1/2的元素牌置入你的手牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), Give(CONTROLLER, "UNG_809t1")


class UNG_024:
    """Mana Bind / 法术共鸣
    奥秘：当你的对手施放一个法术时，将该法术的一张复制置入你的手牌，其法力值消耗变为（0）点。"""

    secret = Play(OPPONENT, SPELL).after(
        Reveal(SELF),
        Give(CONTROLLER, Copy(Play.CARD)).then(Buff(Give.CARD, "UNG_024e")),
    )


@custom_card
class UNG_024e:
    tags = {
        GameTag.CARDNAME: "Mana Bind Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    cost = SET(0)
    events = REMOVED_IN_PLAY


class UNG_028:
    """Open the Waygate / 打开时空之门
    任务：施放8个你的套牌之外的 法术。 奖励：时空扭曲。"""

    progress_total = 8
    quest = Play(CONTROLLER, SPELL - STARTING_DECK).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_028t")


class UNG_028t:
    def play(self):
        self.game.next_players.insert(0, self.controller)


class UNG_941:
    """Primordial Glyph / 远古雕文
    发现一张法术牌，使其法力值消耗减少（2）点。"""

    play = Discover(CONTROLLER, RandomSpell()).then(
        Give(CONTROLLER, Discover.CARD), Buff(Discover.CARD, "UNG_941e")
    )


class UNG_941e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -2}


class UNG_948:
    """Molten Reflection / 熔岩镜像
    选择一个友方随从，召唤一个该随从的复制。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


class UNG_955:
    """Meteor / 陨石术
    对一个随从造成$15点伤害，并对其相邻的随从造成 $4点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 15), Hit(TARGET_ADJACENT, 3)
