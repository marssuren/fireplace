from ..utils import *


##
# Minions


class TRL_131:
    """Sand Drudge / 沙地苦工
    每当你施放一个法术，召唤一个1/1并具有嘲讽的僵尸。"""

    # Whenever you cast a spell, summon a 1/1 Zombie with <b>Taunt</b>.
    events = Play(CONTROLLER, SPELL).on(Summon(CONTROLLER, "TRL_131t"))


class TRL_259:
    """Princess Talanji / 塔兰吉公主
    战吼： 召唤你的手牌中所有你的套牌之外的 随从。"""

    # <b>Battlecry:</b> Summon all minions from your hand that_didn't start in your_deck.
    play = Summon(CONTROLLER, FRIENDLY_HAND + MINION - STARTING_DECK)


class TRL_260:
    """Bwonsamdi, the Dead / 邦桑迪，死亡之神
    战吼：从你的牌库中抽取法力值消耗为（1）的随从，直到达到你的手牌上限。"""

    # [x]<b>Battlecry:</b> Draw 1-Cost minions from your deck until your hand is full.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 1))) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class TRL_408:
    """Grave Horror / 墓园恐魔
    嘲讽 在本局对战中，你每施放一个法术，本牌的法力值消耗便减少（1）点。"""

    # [x]<b>Taunt</b> Costs (1) less for each spell you've cast this game.
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + SPELL)


class TRL_501:
    """Auchenai Phantasm / 奥金尼幻象
    战吼：在本回合中，你的治疗效果转而造成等量的伤害。"""

    # <b>Battlecry:</b> This turn, your healing effects deal damage instead.
    play = Buff(CONTROLLER, "TRL_501e")


TRL_501e = buff(embrace_the_shadow=True)


class TRL_502:
    """Spirit of the Dead / 亡者之灵
    潜行一回合。在一个友方随从死亡后，将它的一张复制洗入你的牌库，其法力值消耗为（1）。"""

    # [x]<b>Stealth</b> for 1 turn. After a friendly minion dies, shuffle a 1-Cost copy of
    # it into your deck.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Death(FRIENDLY_MINIONS).on(
            Shuffle(CONTROLLER, Buff(Copy(Death.ENTITY), "TRL_502e"))
        ),
    )


class TRL_502e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


##
# Spells


class TRL_097:
    """Seance / 灵媒术
    选择一个随从，将一张它的复制置入你的手牌。"""

    # Choose a minion. Add_a copy of it to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Give(CONTROLLER, Copy(TARGET))


class TRL_128:
    """Regenerate / 再生
    恢复#3点生命值。"""

    # Restore #3 Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Heal(TARGET, 3)


class TRL_258:
    """Mass Hysteria / 群体狂乱
    使每个随从随机攻击其他随从。"""

    # Force each minion to_attack another random minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        board = ALL_MINIONS.eval(self.game, self)
        self.game.random.shuffle(board)
        for attacker in board:
            if attacker.dead:
                continue
            defenders = RANDOM(ALL_MINIONS - DEAD - SELF).eval(self.game, attacker)
            if defenders:
                defender = self.game.random.choice(defenders)
                yield Attack(attacker, defender)


class TRL_500:
    """Surrender to Madness / 疯入膏肓
    摧毁你的三个法力水晶。使你牌库中的所有随从牌获得+2/+2。"""

    # [x]Destroy 3 of your Mana Crystals. Give all minions in your deck +2/+2.
    play = (GainEmptyMana(CONTROLLER, -3), Buff(FRIENDLY_DECK + MINION, "TRL_500e"))


TRL_500e = buff(+2, +2)
