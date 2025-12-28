from ..utils import *


##
# Minions


class DRG_201:
    """Crazed Netherwing / 疯狂的灵翼龙
    战吼： 如果你的手牌中有龙牌，则对所有其他角色造成3点伤害。"""

    # <b>Battlecry:</b> If you're holding a Dragon, deal 3 damage to all other characters.
    powered_up = HOLDING_DRAGON
    play = powered_up & Hit(ALL_CHARACTERS - SELF, 3)


class DRG_202:
    """Dragonblight Cultist / 龙骨荒野异教徒
    战吼：祈求迦拉克隆。每有一个其他友方随从，便获得+1攻击力。"""

    # [x]<b>Battlecry:</b> <b>Invoke</b> Galakrond. Gain +1 Attack for each other friendly
    # minion.
    play = INVOKE, Buff(SELF, "DRG_202e") * Count(FRIENDLY_MINIONS - SELF)


DRG_202e = buff(atk=1)


class DRG_203:
    """Veiled Worshipper / 暗藏的信徒
    战吼： 如果你已经祈求过两次，则抽三张牌。"""

    # [x]<b>Battlecry:</b> If you've <b>Invoked</b> twice, draw 3 cards.
    play = INVOKED_TWICE & Draw(CONTROLLER) * 3


class DRG_207:
    """Abyssal Summoner / 深渊召唤者
    战吼：召唤一个属性值等同于你的手牌数量并具有嘲讽的恶魔。"""

    # [x]<b>Battlecry:</b> Summon a Demon with <b>Taunt</b> and stats equal to your hand
    # size.
    def play(self):
        count = len(self.controller.hand)
        if count <= 0:
            return

        demon = self.controller.card("DRG_207t", source=self)
        demon.custom_card = True

        def create_custom_card(demon):
            demon.atk = count
            demon.max_health = count
            demon.cost = min(count, 10)

        demon.create_custom_card = create_custom_card
        demon.create_custom_card(demon)

        yield Summon(self.controller, demon)


class DRG_208:
    """Valdris Felgorge / 瓦迪瑞斯·邪噬
    战吼：将你的手牌上限提高至12张。抽四张牌。"""

    # <b>Battlecry:</b> Increase your maximum hand size to 12. Draw 4 cards.
    play = SetTags(CONTROLLER, {GameTag.MAXHANDSIZE: 12}), Draw(CONTROLLER) * 4


class DRG_209:
    """Zzeraku the Warped / 扭曲巨龙泽拉库
    每当你的英雄受到伤害，召唤一条6/6的虚空幼龙。"""

    # [x]Whenever your hero takes damage, summon a 6/6 Nether Drake.
    events = Damage(FRIENDLY_HERO).on(Summon(CONTROLLER, "DRG_209t"))


##
# Spells


class DRG_204:
    """Dark Skies / 黑暗天际
    随机对一个随从造成$1点伤害。你每有一张手牌，就重复 一次。"""

    # [x]Deal $1 damage to a random minion. Repeat for each card in your hand.
    play = Hit(RANDOM_MINION, 1), Hit(RANDOM_MINION, 1) * Count(FRIENDLY_HAND)


class DRG_205:
    """Nether Breath / 虚空吐息
    造成$2点伤害。如果你的手牌中有龙牌，则改为造成$4点伤害并具有吸血。"""

    # Deal $2 damage. If you're holding a Dragon, deal $4 damage with <b>Lifesteal</b>
    # instead.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    powered_up = HOLDING_DRAGON
    play = powered_up & (GiveLifesteal(SELF), Hit(TARGET, 4)) | Hit(TARGET, 2)


class DRG_206:
    """Rain of Fire / 火焰之雨
    对所有角色造成$1点伤害。"""

    # Deal $1 damage to all_characters.
    play = Hit(ALL_CHARACTERS, 1)


class DRG_250:
    """Fiendish Rites / 邪鬼仪式
    祈求迦拉克隆。使你的所有随从获得+1攻击力。"""

    # <b>Invoke</b> Galakrond. Give your minions +1_Attack.
    play = INVOKE, Buff(FRIENDLY_MINIONS, "DRG_250e")


DRG_250e = buff(atk=1)


##
# Heros


class DRG_600(GalakrondUtils):
    """Galakrond, the Wretched"""

    # [x]<b>Battlecry:</b> Summon 1 random Demon. <i>(@)</i>
    progress_total = 2
    play = Summon(CONTROLLER, RandomDemon())
    reward = Find(SELF + FRIENDLY_HERO) | Morph(SELF, "DRG_600t2")


class DRG_600t2(GalakrondUtils):
    """Galakrond, the Apocalypse"""

    # [x]<b>Battlecry:</b> Summon 2 random Demons. <i>(@)</i>
    progress_total = 2
    play = Summon(CONTROLLER, RandomDemon()) * 2
    reward = Find(SELF + FRIENDLY_HERO) | Morph(SELF, "DRG_600t3")


class DRG_600t3:
    """Galakrond, Azeroth's End"""

    # [x]<b>Battlecry:</b> Summon 4 random Demons. Equip a 5/2 Claw.
    play = (Summon(CONTROLLER, RandomDemon()) * 4, Summon(CONTROLLER, "DRG_238ht"))


class DRG_238p3:
    """Galakrond's Malice"""

    # [x]<b>Hero Power</b> Summon two 1/1 Imps.
    activate = Summon(CONTROLLER, "DRG_238t12t2") * 2
