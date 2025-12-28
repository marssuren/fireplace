from ..utils import *


##
# Minions


class ULD_236:
    """Tortollan Pilgrim / 始祖龟朝圣者
    战吼：从你的牌库中 发现一张法术牌，并对随机目标施放。"""

    # [x]<b>Battlecry</b>: <b>Discover</b> a copy of a spell in your deck and cast it with
    # random targets.
    play = Choice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL)) * 3)
    ).then(CastSpell(Choice.CARD), Remove(Choice.CARDS))


class ULD_238:
    """Reno the Relicologist / 考古专家雷诺
    战吼：如果你的牌库里没有相同的牌，则造成10点伤害，随机分配到所有敌方随从身上。"""

    # <b>Battlecry:</b> If your deck has no duplicates, deal 10 damage randomly split among
    # all enemy minions.
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & Hit(RANDOM_ENEMY_CHARACTER, 1) * 10


class ULD_240:
    """Arcane Flakmage / 对空奥术法师
    在你使用一张奥秘牌后，对所有敌方随从造成2点伤害。"""

    # After you play a <b>Secret</b>, deal 2 damage to all enemy minions.
    events = Play(CONTROLLER, SECRET).after(Hit(ENEMY_MINIONS, 2))


class ULD_293:
    """Cloud Prince / 云雾王子
    战吼： 如果你控制一个奥秘，则造成6点伤害。"""

    # <b>Battlecry:</b> If you control a <b>Secret</b>, deal 6 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS: 1,
    }
    play = Hit(TARGET, 6)


class ULD_329:
    """Dune Sculptor / 沙丘塑形师
    在你施放一个法术后，随机将一张法师随从牌置入你的手牌。"""

    # [x]After you cast a spell, add a random Mage minion to your hand.
    events = OWN_SPELL_PLAY.after(
        Give(CONTROLLER, RandomMinion(card_class=CardClass.MAGE))
    )


class ULD_435:
    """Naga Sand Witch / 纳迦沙漠女巫
    战吼：使你手牌中的法术牌法力值消耗变为（5）点。"""

    # [x]<b>Battlecry:</b> Change the Cost of spells in your hand to (5).
    play = Buff(FRIENDLY_HAND + SPELL, "ULD_435e")


class ULD_435e:
    cost = SET(5)
    events = REMOVED_IN_PLAY


##
# Spells


class ULD_216:
    """Puzzle Box of Yogg-Saron / 尤格-萨隆的谜之匣
    随机施放10个法术（目标随机而定）。"""

    # Cast 10 random spells <i>(targets chosen randomly).</i>
    play = CastSpell(RandomSpell()) * 10


class ULD_239:
    """Flame Ward / 火焰结界
    奥秘：在一个随从攻击你的英雄后，对所有敌方随从造成$3点伤害。"""

    # <b>Secret:</b> After a minion attacks your hero, deal $3 damage to all enemy minions.
    secret = Attack(MINION, FRIENDLY_HERO).after(Hit(ENEMY_MINIONS, 3))


class ULD_433:
    """Raid the Sky Temple / 洗劫天空殿
    任务：施放10个法术。 奖励：升格卷轴。"""

    # <b>Quest:</b> Cast 10 spells. <b>Reward: </b>Ascendant Scroll.
    progress_total = 10
    quest = Play(CONTROLLER, SPELL).on(AddProgress(SELF, Play.CARD))
    reward = Summon(CONTROLLER, "ULD_433p")


class ULD_433p:
    """Ascendant Scroll"""

    # <b>Hero Power</b> Add a random Mage spell to your hand. It costs (2) less.
    requirements = {
        PlayReq.REQ_HAND_NOT_FULL: 0,
    }
    activate = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)).then(
        Buff(Give.CARD, "ULD_433e")
    )


class ULD_433e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class ULD_726:
    """Ancient Mysteries / 远古谜团
    从你的牌库中抽一张奥秘牌。其法力值消耗为（0）点。"""

    # Draw a <b>Secret</b> from your deck. It costs (0).
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SECRET)).then(
        Buff(ForceDraw.TARGET, "ULD_726e")
    )


class ULD_726e:
    cost = SET(0)
    events = REMOVED_IN_PLAY
