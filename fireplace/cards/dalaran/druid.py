from ..utils import *


##
# Minions


class DAL_354:
    """Acornbearer / 橡果人
    亡语：将两张1/1的“松鼠”置入你的手牌。"""

    # <b>Deathrattle:</b> Add two 1/1 Squirrels to your hand.
    deathrattle = Give(CONTROLLER, "DAL_354t") * 2


class DAL_355:
    """Lifeweaver / 织命者
    每当有角色获得你的治疗时，随机将一张德鲁伊法术牌置入你的手牌。"""

    # Whenever you restore Health, add a random Druid spell to your hand.
    events = Heal(source=FRIENDLY).on(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.DRUID))
    )


class DAL_357:
    """Lucentbark / 卢森巴克
    嘲讽。亡语：进入休眠状态。累计恢复5点生命值可唤醒本随从。"""

    # <b>Taunt</b> <b>Deathrattle:</b> Go dormant. Restore 5 Health to awaken this minion.
    deathrattle = Find(FRIENDLY_MINIONS + SELF) & (Morph(SELF, "DAL_357t")) | (
        Summon(CONTROLLER, "DAL_357t")
    )


class DAL_357t:
    tags = {GameTag.DORMANT: True}
    progress_total = 5
    dormant_events = Heal().on(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))
    reward = Morph(SELF, "DAL_357")


class DAL_732:
    """Keeper Stalladris / 守护者斯塔拉蒂斯
    在你施放了一个抉择法术后，将每个选项的复制置入你的手牌。"""

    # After you cast a <b>Choose One</b> spell, add copies of both choices_to_your_hand.
    events = Play(CONTROLLER, CHOOSE_ONE + SPELL).after(
        Give(CONTROLLER, Copy(CHOOSE_CARDS(Play.CARD)))
    )


class DAL_799(ThresholdUtils):
    """Crystal Stag"""

    # <b>Rush</b>. <b>Battlecry:</b> If you've restored 5 Health this game, summon a copy
    # of this.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = ThresholdUtils.powered_up & Summon(CONTROLLER, ExactCopy(SELF))


##
# Spells


class DAL_256:
    """The Forest's Aid / 森林的援助
    双生法术 召唤五个2/2的 树人。"""

    # <b>Twinspell</b> Summon five 2/2 Treants.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "DAL_256t2") * 5


class DAL_256ts(DAL_256):
    pass


class DAL_350:
    """Crystal Power / 水晶之力
    抉择：对一个随从造成$2点伤害；或者恢复#5点生命值。"""

    # <b>Choose One -</b> Deal $2 damage to a minion; or_Restore #5 Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    choose = ("DAL_350a", "DAL_350b")
    play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Heal(TARGET, 5))


class DAL_350a:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class DAL_350b:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Heal(TARGET, 5)


class DAL_351:
    """Blessing of the Ancients / 远古祝福
    双生法术 使你的所有随从获得+1/+1。"""

    # <b>Twinspell</b> Give your minions +1/+1.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(FRIENDLY_MINIONS, "DAL_351e")


class DAL_351ts(DAL_351):
    pass


DAL_351e = buff(+1, +1)


class DAL_352:
    """Crystalsong Portal / 晶歌传送门
    发现一张德鲁伊随从牌。如果你的手牌中没有随从牌，改为保留全部三张牌。"""

    # <b>Discover</b> a Druid minion. If your hand has no minions, keep all 3.
    powered_up = -Find(FRIENDLY_HAND + MINION)
    play = powered_up & (
        Give(CONTROLLER, RandomMinion(card_class=CardClass.DRUID)) * 3
    ) | (DISCOVER(RandomMinion(card_class=CardClass.DRUID)))


class DAL_733:
    """Dreamway Guardians / 守卫梦境之路
    召唤两个1/2并具有吸血的 树妖。"""

    # Summon two 1/2 Dryads with <b>Lifesteal</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "DAL_733t") * 2
