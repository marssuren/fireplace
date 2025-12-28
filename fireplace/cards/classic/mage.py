from ..utils import *


##
# Minions


class CS2_033:
    """Water Elemental / 水元素
    冻结任何受到本随从伤害的角色。"""

    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class EX1_274:
    """Ethereal Arcanist / 虚灵奥术师
    在你的回合结束时，如果你控制着奥秘，获得+2/+2。"""

    events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Buff(SELF, "EX1_274e"))


EX1_274e = buff(+2, +2)


class EX1_559:
    """Archmage Antonidas / 大法师安东尼达斯
    每当你施放一个法术，将一张“火球术”法术牌置入你的手牌。"""

    events = OWN_SPELL_PLAY.on(Give(CONTROLLER, "CS2_029"))


class EX1_608:
    """Sorcerer's Apprentice / 巫师学徒
    你的法术的法力值消耗减少（1）点（但不能少于1点）。"""

    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


class EX1_612:
    """Kirin Tor Mage / 肯瑞托法师
    战吼： 在本回合中，你使用的下一个奥秘的法力值消耗为（0）点。"""

    play = Buff(CONTROLLER, "EX1_612o")


class EX1_612o:
    update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(0)})
    events = Play(CONTROLLER, SECRET).on(Destroy(SELF))


class NEW1_012:
    """Mana Wyrm / 法力浮龙
    每当你施放一个法术，便获得 +1攻击力。"""

    events = OWN_SPELL_PLAY.on(Buff(SELF, "NEW1_012o"))


NEW1_012o = buff(atk=1)


##
# Spells


class CS2_022:
    """Polymorph / 变形术
    使一个随从变形成为1/1的绵羊。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Morph(TARGET, "CS2_tk1")


class CS2_023:
    """Arcane Intellect / 奥术智慧
    抽两张牌。"""

    play = Draw(CONTROLLER) * 2


class CS2_024:
    """Frostbolt / 寒冰箭
    对一个角色造成$3点伤害，并使其冻结。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Freeze(TARGET)


class CS2_025:
    """Arcane Explosion / 魔爆术
    对所有敌方随从造成$1点伤害。"""

    play = Hit(ENEMY_MINIONS, 1)


class CS2_026:
    """Frost Nova / 冰霜新星
    冻结所有敌方随从。"""

    play = Freeze(ENEMY_MINIONS)


class CS2_027:
    """Mirror Image / 镜像
    召唤两个0/2，并具有嘲讽的随从。"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "CS2_mirror") * 2


class CS2_028:
    """Blizzard / 暴风雪
    对所有敌方随从造成$2点伤害，并使其冻结。"""

    play = Hit(ENEMY_MINIONS, 2), Freeze(ENEMY_MINIONS)


class CS2_029:
    """Fireball / 火球术
    造成$6点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 6)


class CS2_031:
    """Ice Lance / 冰枪术
    冻结一个角色，如果该角色已被冻结，则改为对其造成$4点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Find(TARGET + FROZEN) & Hit(TARGET, 4) | Freeze(TARGET)


class CS2_032:
    """Flamestrike / 烈焰风暴
    对所有敌方随从造成$5点伤害。"""

    play = Hit(ENEMY_MINIONS, 4)


class EX1_275:
    """Cone of Cold / 冰锥术
    冻结一个随从和其相邻的随从，并对它们造成$1点伤害。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET | TARGET_ADJACENT, 1), Freeze(TARGET | TARGET_ADJACENT)


class EX1_277:
    """Arcane Missiles / 奥术飞弹
    造成$3点伤害，随机分配到所有敌人身上。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(3)


class EX1_279:
    """Pyroblast / 炎爆术
    造成$10点伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 10)


##
# Secrets


class tt_010:
    """Spellbender"""

    secret = Play(OPPONENT, SPELL, MINION).on(
        FULL_BOARD | (Reveal(SELF), Retarget(Play.CARD, Summon(CONTROLLER, "tt_010a")))
    )


class EX1_287:
    """Counterspell / 法术反制
    奥秘：当你的对手施放一个法术时，反制该法术。"""

    secret = Play(OPPONENT, SPELL).on(Reveal(SELF), Counter(Play.CARD))


class EX1_289:
    """Ice Barrier / 寒冰护体
    奥秘：当你的英雄受到攻击时，获得8点护甲值。"""

    secret = Attack(CHARACTER, FRIENDLY_HERO).on(
        Reveal(SELF), GainArmor(FRIENDLY_HERO, 8)
    )


class EX1_294:
    """Mirror Entity / 镜像实体
    奥秘：在你的对手使用一张随从牌后，召唤一个该随从的复制。"""

    secret = [
        Play(OPPONENT, MINION).after(
            Reveal(SELF), Summon(CONTROLLER, ExactCopy(Play.CARD))
        ),
        Play(OPPONENT, ID("EX1_323h")).after(
            Reveal(SELF), Summon(CONTROLLER, "EX1_323")
        ),  # :-)
    ]


class EX1_295:
    """Ice Block / 寒冰屏障
    奥秘：当你的英雄将要承受致命伤害时，防止这些伤害，并使其在本回合中免疫。"""

    secret = Predamage(FRIENDLY_HERO).on(
        Lethal(FRIENDLY_HERO, Predamage.AMOUNT)
        & (Reveal(SELF), Buff(FRIENDLY_HERO, "EX1_295o"), Predamage(FRIENDLY_HERO, 0))
    )


EX1_295o = buff(immune=True)


class EX1_594:
    """Vaporize / 蒸发
    奥秘：当一个随从攻击你的英雄，将其消灭。"""

    secret = Attack(MINION, FRIENDLY_HERO).on(Reveal(SELF), Destroy(Attack.ATTACKER))


class EX1_179:
    """Icicle / 冰刺
    对一个随从造成$2点伤害。如果它已被冻结，抽一张牌。"""

    # Deal $2 damage to a minion. If it's <b>Frozen</b>, draw a card.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), Find(TARGET + FROZEN) & Draw(CONTROLLER)


class EX1_180:
    """Tome of Intellect / 智慧秘典
    随机将一张法师法术牌置入你的手牌。"""

    # Add a random Mage spell to your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))
