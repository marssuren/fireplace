from ..utils import *


##
# Minions


class DAL_060:
    """Clockwork Goblin / 发条地精
    战吼：将一张“炸弹” 牌洗入你对手的牌库。当抽到“炸弹”时，便会受到5点伤害。"""

    # [x]<b>Battlecry:</b> Shuffle a Bomb into your opponent's deck. When drawn, it
    # explodes for 5 damage.
    play = Shuffle(OPPONENT, "BOT_511t")


class DAL_064:
    """Blastmaster Boom / 爆破之王砰砰
    战吼：你对手的牌库中每有一张“炸弹”牌，便召唤两个1/1的砰砰机器人。"""

    # [x]<b>Battlecry:</b> Summon two 1/1 Boom Bots for each Bomb in your opponent's deck.
    play = Summon(CONTROLLER, "GVG_110t") * (Count(ENEMY_DECK + ID("BOT_511t")) * 2)


class DAL_070:
    """The Boom Reaver / 砰砰机甲
    战吼： 召唤一个你牌库中的随从的复制，并使其获得突袭。"""

    # <b>Battlecry:</b> Summon a copy of a minion in your deck. Give it <b>Rush</b>.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY_DECK + MINION))).then(
        Buff(Summon.CARD, "DAL_070e")
    )


DAL_070e = buff(rush=True)


class DAL_759:
    """Vicious Scraphound / 凶恶的废钢猎犬
    每当本随从造成伤害时，获得等量的 护甲值。"""

    # Whenever this minion deals damage, gain that much Armor.
    events = Damage(CHARACTER, None, SELF).on(GainArmor(FRIENDLY_HERO, Damage.AMOUNT))


class DAL_770:
    """Omega Devastator / 欧米茄毁灭者
    战吼：如果你有十个法力水晶，对一个随从造成10点伤害。"""

    # [x]<b>Battlecry:</b> If you have 10 Mana Crystals, deal 10 damage to a minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MIN_MANA_CRYSTAL: 10,
    }
    play = Hit(TARGET, 10)


##
# Spells


class DAL_008(SchemeUtils):
    """Dr. Boom's Scheme"""

    # Gain @ Armor. <i>(Upgrades each turn!)</i>
    play = GainArmor(FRIENDLY_HERO, Attr(SELF, GameTag.QUEST_PROGRESS) + 1)


class DAL_059:
    """Dimensional Ripper / 空间撕裂器
    召唤你的牌库中一个随从的两个复制。"""

    # Summon 2 copies of a minion in your deck.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }

    def play(self):
        minion = self.game.random.choice(
            self.controller.deck.filter(type=CardType.MINION)
        )
        if minion:
            yield Summon(CONTROLLER, minion.id) * 2


class DAL_062:
    """Sweeping Strikes / 横扫攻击
    使一个随从获得 “同时对其攻击目标相邻的随从造成伤害。”"""

    # Give a minion "Also damages minions next to whomever this attacks."
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "DAL_062e")


class DAL_062e:
    events = Attack(OWNER).on(Hit(ADJACENT(Attack.DEFENDER), ATK(OWNER)))


class DAL_769:
    """Improve Morale / 提振士气
    对一个随从造成$1点伤害。如果它依然存活，则将一张跟班牌置入你的手牌。"""

    # [x]Deal $1 damage to a minion. If it survives, add a <b>Lackey</b> to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Dead(TARGET) | Give(CONTROLLER, RandomLackey())


##
# Weapons


class DAL_063:
    """Wrenchcalibur / 圣剑扳手
    在你的英雄攻击后，将一张“炸弹”牌洗入你对手的牌库。"""

    # After your hero attacks, shuffle a Bomb into your [x]opponent's deck.
    events = Attack(FRIENDLY_HERO).after(Shuffle(OPPONENT, "BOT_511t"))
