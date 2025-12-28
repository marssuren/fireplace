from ..utils import *


##
# Minions


class CS2_088:
    """Guardian of Kings / 列王守卫
    嘲讽，战吼：为你的英雄恢复#6点生命值。"""

    play = Heal(FRIENDLY_HERO, 6)


class EX1_362:
    """Argent Protector / 银色保卫者
    战吼：使一个其他友方随从获得圣盾。"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = GiveDivineShield(TARGET)


class EX1_382:
    """Aldor Peacekeeper / 奥尔多卫士
    战吼：使一个敌方随从的攻击力变为1。"""

    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "EX1_382e")


class EX1_382e:
    atk = SET(1)


class EX1_383:
    """Tirion Fordring / 提里奥·弗丁
    圣盾，嘲讽，亡语：装备一把5/3的 灰烬使者。"""

    deathrattle = Summon(CONTROLLER, "EX1_383t")


##
# Spells


class CS2_087:
    """Blessing of Might / 力量祝福
    使一个随从获得+3攻击力。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_087e")


CS2_087e = buff(atk=3)


class CS2_089:
    """Holy Light / 圣光术
    为你的英雄恢复#8点生命值。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 6)


class CS2_092:
    """Blessing of Kings / 王者祝福
    使一个随从获得+4/+4。（+4攻击力/+4生命值）"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_092e")


CS2_092e = buff(+4, +4)


class CS2_093:
    """Consecration / 奉献
    对所有敌人造成$2点伤害。"""

    play = Hit(ENEMY_CHARACTERS, 2)


class CS2_094:
    """Hammer of Wrath / 愤怒之锤
    造成$3点伤害。抽一张牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Draw(CONTROLLER)


class EX1_349:
    """Divine Favor / 神恩术
    抽若干数量的牌，直到你的手牌数量等同于你对手的手牌数量。"""

    play = DrawUntil(CONTROLLER, Count(ENEMY_HAND))


class EX1_354:
    """Lay on Hands / 圣疗术
    恢复#8点生命值，抽三张牌。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 8), Draw(CONTROLLER) * 3


class EX1_355:
    """Blessed Champion / 受祝福的勇士
    使一个随从的攻击力翻倍。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "EX1_355e")


class EX1_355e:
    atk = lambda self, i: i * 2


class EX1_360:
    """Humility / 谦逊
    使一个随从的攻击力变为1。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "EX1_360e")


class EX1_360e:
    atk = SET(1)


class EX1_363:
    """Blessing of Wisdom / 智慧祝福
    选择一个随从，每当其进行攻击，便抽一张牌。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "EX1_363e")


class EX1_363e:
    events = Attack(OWNER).on(Draw(CONTROLLER))


class EX1_363e2:
    """Blessing of Wisdom (Unused)"""

    events = Attack(OWNER).on(Draw(OWNER_OPPONENT))


class EX1_365:
    """Holy Wrath / 神圣愤怒
    抽一张牌， 并对一个随从造成等同于该牌法力值消耗的伤害。"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Draw(CONTROLLER).then(Hit(TARGET, COST(Draw.CARD)))


class EX1_371:
    """Hand of Protection / 保护之手
    使一个随从获得圣盾。"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = GiveDivineShield(TARGET)


class EX1_384:
    """Avenging Wrath / 复仇之怒
    造成$8点伤害，随机分配到所有敌人身上。"""

    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(8)


class EX1_619:
    """Equality / 生而平等
    将所有随从的生命值变为1。"""

    play = Buff(ALL_MINIONS, "EX1_619e")


class EX1_619e:
    max_health = SET(1)


##
# Secrets


class EX1_130:
    """Noble Sacrifice / 崇高牺牲
    奥秘：当一个敌人攻击时，召唤一个2/1的防御者，并使其成为攻击的目标。"""

    secret = Attack(ENEMY_MINIONS).on(
        FULL_BOARD
        | (Reveal(SELF), Retarget(Attack.ATTACKER, Summon(CONTROLLER, "EX1_130a")))
    )


class EX1_132:
    """Eye for an Eye / 以眼还眼
    奥秘： 当你的英雄受到伤害时，对敌方英雄造成等量伤害。"""

    secret = Damage(FRIENDLY_HERO).on(Reveal(SELF), Hit(ENEMY_HERO, Damage.AMOUNT))


class EX1_136:
    """Redemption / 救赎
    奥秘：当一个友方随从死亡时，使其回到战场，并具有1点生命值。"""

    secret = Death(FRIENDLY + MINION).after(
        FULL_BOARD
        | (
            Reveal(SELF),
            Summon(CONTROLLER, Copy(Death.ENTITY)).then(
                SetCurrentHealth(Summon.CARD, 1)
            ),
        )
    )


class EX1_379:
    """Repentance / 忏悔
    奥秘： 在你的对手使用一张随从牌后，使该随从的生命值降为1。"""

    secret = Play(OPPONENT, MINION | HERO).after(
        Reveal(SELF), Buff(Play.CARD, "EX1_379e")
    )


class EX1_379e:
    max_health = SET(1)


##
# Weapons


class CS2_097:
    """Truesilver Champion / 真银圣剑
    每当你的英雄进攻，便为其恢复#3点生命值。"""

    events = Attack(FRIENDLY_HERO).on(Heal(FRIENDLY_HERO, 2))


class EX1_366:
    """Sword of Justice / 公正之剑
    在你召唤一个随从后，使其获得+1/+1，这把武器失去1点耐久度。"""

    events = Summon(CONTROLLER, MINION).after(
        Buff(Summon.CARD, "EX1_366e"), Hit(SELF, 1)
    )


EX1_366e = buff(+1, +1)


class EX1_184:
    """Righteousness / 正义
    使你的所有随从获得圣盾。"""

    # Give your minions <b>Divine Shield</b>.
    play = GiveDivineShield(FRIENDLY_MINIONS)
