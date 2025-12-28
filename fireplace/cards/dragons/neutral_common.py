from ..utils import *


##
# Minions


class DRG_049:
    """Tasty Flyfish / 美味飞鱼
    亡语：使你手牌中的一张龙牌获得+2/+2。"""

    # <b>Deathrattle:</b> Give a Dragon in your hand +2/+2.
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + DRAGON), "DRG_049e")


DRG_049e = buff(+2, +2)


class DRG_050:
    """Devoted Maniac / 虔信狂徒
    突袭，战吼： 祈求迦拉克隆。"""

    # <b>Rush</b> <b>Battlecry:</b> <b>Invoke</b> Galakrond.
    play = INVOKE


class DRG_054:
    """Big Ol' Whelp / 雏龙巨婴
    战吼：抽一张牌。"""

    # <b>Battlecry:</b> Draw a card.
    play = Draw(CONTROLLER)


class DRG_056:
    """Parachute Brigand / 空降歹徒
    在你使用一张海盗牌后，从你的手牌中召唤本随从。"""

    # [x]After you play a Pirate, summon this minion from your hand.
    class Hand:
        events = Play(CONTROLLER, PIRATE).after(Summon(CONTROLLER, SELF))


class DRG_057:
    """Hot Air Balloon / 热气球
    在你的回合开始时，获得+1生命值。"""

    # At the start of your turn, gain +1 Health.
    events = OWN_TURN_BEGIN.on(Buff(SELF, "DRG_057e"))


DRG_057e = buff(health=1)


class DRG_058:
    """Wing Commander / 空军指挥官
    你手牌中每有一张龙牌，便拥有+2 攻击力。"""

    # Has +2 Attack for each Dragon in your hand.
    play = Buff(SELF, "DRG_058e") * Count(FRIENDLY_HAND + DRAGON)


DRG_058e = buff(atk=2)


class DRG_059:
    """Goboglide Tech / 地精滑翔技师
    战吼：如果你控制一个机械，便获得+1/+1和突袭。"""

    # <b>Battlecry:</b> If you control a_Mech, gain +1/+1 and_<b>Rush</b>.
    powered_up = Find(FRIENDLY_MINIONS + MECH)
    play = powered_up & Buff(SELF, "DRG_059e")


DRG_059e = buff(+1, +1, rush=True)


class DRG_060:
    """Fire Hawk / 火鹰
    战吼：你的对手每有一张手牌，本随从便获得+1攻击力。"""

    # <b>Battlecry:</b> Gain +1 Attack for each card in your opponent's hand.
    play = Buff(SELF, "DRG_060e") * Count(ENEMY_HAND)


DRG_060e = buff(atk=1)


class DRG_067:
    """Troll Batrider / 巨魔蝙蝠骑士
    战吼：随机对一个敌方随从造成3点伤害。"""

    # <b>Battlecry:</b> Deal 3 damage to a random enemy minion.
    play = Hit(RANDOM_ENEMY_CHARACTER, 3)


class DRG_068:
    """Living Dragonbreath / 活化龙息
    你的随从无法被 冻结。"""

    # Your minions can't be_<b>Frozen</b>.
    update = Refresh(FRIENDLY_MINIONS, {GameTag.CANT_BE_FROZEN: True})


class DRG_069:
    """Platebreaker / 破甲骑士
    战吼： 摧毁你对手的护甲。"""

    # <b>Battlecry:</b> Destroy your opponent's Armor.
    def play(self):
        self.controller.opponent.hero.armor = 0


class DRG_074:
    """Camouflaged Dirigible / 迷彩飞艇
    战吼：直到你的下个回合，使你的其他机械获得潜行。"""

    # <b>Battlecry:</b> Give your other Mechs <b>Stealth</b> until your_next turn.
    play = (
        Buff(FRIENDLY_MINIONS + MECH - SELF, "DRG_074e"),
        Stealth(FRIENDLY_MINIONS + MECH - SELF),
    )


class DRG_074e:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class DRG_081:
    """Scalerider / 锐鳞骑士
    战吼：如果你的手牌中有龙牌，则造成2点伤害。"""

    # <b>Battlecry:</b> If you're holding a Dragon, deal 2 damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0}
    powered_up = HOLDING_DRAGON
    play = powered_up & Hit(TARGET, 2)


class DRG_213:
    """Twin Tyrant / 双头暴虐龙
    战吼：随机对两个敌方随从造成4点伤害。"""

    # <b>Battlecry:</b> Deal 4 damage to two random enemy minions.
    play = Hit(RANDOM_ENEMY_MINION * 2, 4)


class DRG_242:
    """Shield of Galakrond / 迦拉克隆之盾
    嘲讽，战吼： 祈求迦拉克隆。"""

    # <b>Taunt</b> <b>Battlecry:</b> <b>Invoke</b> Galakrond.
    play = INVOKE
