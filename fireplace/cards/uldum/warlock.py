from ..utils import *


##
# Minions


class ULD_161:
    """Neferset Thrasher / 尼斐塞特鞭笞者
    每当本随从攻击时，对你的英雄造成3点伤害。"""

    # Whenever this attacks, deal 3 damage to your_hero.
    events = Attack(SELF).on(Hit(FRIENDLY_HERO, 3))


class ULD_162:
    """EVIL Recruiter / 怪盗征募官
    战吼：消灭一个友方跟班，召唤一个5/5的恶魔。"""

    # <b>Battlecry:</b> Destroy a friendly <b>Lackey</b> to summon a 5/5 Demon.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_LACKEY: 0,
    }
    play = Destroy(TARGET), Summon(CONTROLLER, "ULD_162t")


class ULD_163:
    """Expired Merchant / 过期货物专卖商
    战吼：弃掉你手牌中法力值消耗最高的牌。亡语：将弃掉的牌的两张复制置入你的手牌。"""

    # [x]<b>Battlecry:</b> Discard your highest Cost card. <b>Deathrattle:</b> Add 2 copies
    # of it to your hand.
    play = Discard(HIGHEST_COST(FRIENDLY_HAND)).then(
        StoringBuff(SELF, "ULD_163e", Discard.TARGET)
    )


class ULD_163e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, Copy(STORE_CARD)) * 2


class ULD_165:
    """Riftcleaver / 裂隙屠夫
    战吼：消灭一个随从。你的英雄受到等同于该随从生命值的 伤害。"""

    # <b>Battlecry:</b> Destroy a minion. Your hero takes damage equal to its Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(FRIENDLY_HERO, CURRENT_HEALTH(TARGET)), Destroy(TARGET)


class ULD_167:
    """Diseased Vulture / 染病的兀鹫
    每当你的英雄在自己的回合受到伤害，随机召唤一个法力值消耗为（3）的随从。"""

    # After your hero takes damage on your turn, summon a random 3-Cost minion.
    events = Hit(FRIENDLY_HERO).on(
        Find(CURRENT_PLAYER + CONTROLLER) & Summon(CONTROLLER, RandomMinion(cost=3))
    )


class ULD_168:
    """Dark Pharaoh Tekahn / 黑暗法老塔卡恒
    战吼：在本局对战的剩余时间内，你的跟班变为4/4。"""

    # <b>Battlecry:</b> For the rest of the game, your <b>Lackeys</b> are 4/4.
    play = Buff(CONTROLLER, "ULD_168e")


class ULD_168e:
    update = Refresh(
        (IN_DECK | IN_HAND | IN_PLAY) + FRIENDLY + LACKEY, buff="ULD_168e3"
    )


class ULD_168e3:
    atk = SET(4)
    max_health = SET(4)


##
# Spells


class ULD_140:
    """Supreme Archaeology / 最最伟大的考古学
    任务：抽20张牌。 奖励：源生魔典。"""

    # <b>Quest:</b> Draw 20 cards. <b>Reward:</b> Tome of Origination.
    progress_total = 20
    quest = Draw(CONTROLLER).after(AddProgress(SELF, Draw.CARD))
    reward = Summon(CONTROLLER, "ULD_140p")


class ULD_140p:
    """Tome of Origination"""

    # <b>Hero Power</b> Draw a card. It costs (0).
    activate = Draw(CONTROLLER).then(Buff(Draw.CARD, "ULD_140e"))


class ULD_140e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


class ULD_160:
    """Sinister Deal / 邪恶交易
    发现一张跟班牌。"""

    # <b>Discover</b> a <b>Lackey</b>.
    play = DISCOVER(RandomLackey())


class ULD_324:
    """Impbalming / 小鬼油膏
    消灭一个随从。将三张“游荡小鬼”洗入你的牌库。"""

    # Destroy a minion. Shuffle 3 Worthless Imps into your deck.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Shuffle(CONTROLLER, "ULD_324t") * 3


class ULD_717:
    """Plague of Flames / 火焰之灾祸
    消灭你的所有随从。每消灭一个随从，便随机消灭一个敌方随从。"""

    # [x]Destroy all your minions. For each one, destroy a random enemy minion.
    def play(self):
        count = Count(FRIENDLY_MINIONS).evaluate(self)
        yield Destroy(FRIENDLY_MINIONS)
        yield Destroy(RANDOM_ENEMY_MINION * count)
