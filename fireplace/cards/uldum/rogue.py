from ..utils import *


##
# Minions


class ULD_186:
    """Pharaoh Cat / 法老御猫
    战吼： 随机将一张复生随从牌置入你的手牌。"""

    # <b>Battlecry:</b> Add a random <b>Reborn</b> minion to your_hand.
    play = Give(CONTROLLER, RandomMinion(reborn=True))


class ULD_231:
    """Whirlkick Master / 连环腿大师
    每当你使用一张连击牌时，随机将一张连击牌置入你的手牌。"""

    # Whenever you play a <b>Combo</b> card, add a random <b>Combo</b> card to your hand.
    events = Play(CONTROLLER, COMBO).on(Give(CONTROLLER, RandomCollectible(combo=True)))


class ULD_280:
    """Sahket Sapper / 沙赫柯特工兵
    亡语：随机将一个敌方随从移回对手的 手牌。"""

    # <b>Deathrattle:</b> Return a _random enemy minion to_ your_opponent's_hand.
    deathrattle = Bounce(RANDOM_ENEMY_MINION)


class ULD_288:
    """Anka, the Buried / 被埋葬的安卡
    战吼：使你手牌中所有具有亡语的随从牌变为1/1，且法力值消耗为（1）点。"""

    # <b>Battlecry:</b> Change each <b>Deathrattle</b> minion in your hand into a 1/1 that
    # costs (1).
    play = MultiBuff(FRIENDLY_HAND + MINION + DEATHRATTLE, ["ULD_288e", "GBL_001e"])


class ULD_288e:
    atk = SET(1)
    max_health = SET(1)


class ULD_327:
    """Bazaar Mugger / 集市恶痞
    突袭 战吼：随机将一张另一职业的随从牌置入你的手牌。"""

    # <b>Rush</b> <b>Battlecry:</b> Add a random minion from another class to your hand.
    play = Give(CONTROLLER, RandomMinion(card_class=ANOTHER_CLASS))


##
# Spells


class ULD_286:
    """Shadow of Death / 死亡之影
    选择一个随从。将三张“阴影”牌洗入你的牌库，当抽到“阴影”时，召唤该随从的一个复制。"""

    # Choose a minion. Shuffle 3 'Shadows' into your deck that summon a copy when drawn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Shuffle(CONTROLLER, "ULD_286t") * 3


class ULD_286t:
    play = Summon(CONTROLLER, Copy(CREATOR_TARGET))
    draw = CAST_WHEN_DRAWN


class ULD_326:
    """Bazaar Burglary / 劫掠集市
    任务：将4张其他职业的卡牌置入你的手牌。 奖励：远古刀锋。"""

    # [x]<b>Quest:</b> Add 4 cards from other classes to your hand. <b>Reward: </b>Ancient
    # Blades.
    progress_total = 4
    quest = Give(CONTROLLER, ANOTHER_CLASS).after(AddProgress(SELF, Give.CARD))
    reward = Summon(CONTROLLER, "ULD_326p")


class ULD_326p:
    """Ancient Blades"""

    # [x]<b>Hero Power</b> Equip a 3/2 Blade with <b>Immune</b> while attacking.
    activate = Summon(CONTROLLER, "ULD_326t")


class ULD_326t:
    update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class ULD_328:
    """Clever Disguise / 聪明的伪装
    随机将另一职业的两张法术牌置入你的手牌。"""

    # Add 2 random spells from another class to_your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=ANOTHER_CLASS)) * 2


class ULD_715:
    """Plague of Madness / 疯狂之灾祸
    每个玩家装备一把2/2并具有剧毒的刀。"""

    # Each player equips a 2/2 Knife with <b>Poisonous</b>.
    play = Summon(ALL_PLAYERS, "ULD_715t")


##
# Weapons


class ULD_285:
    """Hooked Scimitar / 钩镰弯刀
    连击：获得+2攻击力。"""

    # [x]<b>Combo:</b> Gain +2 Attack.
    combo = Buff(SELF, "ULD_285e")


ULD_285e = buff(atk=2)
