from ..utils import *


##
# Minions


class BT_197:
    """Reliquary of Souls / 灵魂之匣
    吸血 亡语：将“终极魂匣”洗入你的牌库。"""

    # [x]<b>Lifesteal</b> <b>Deathrattle:</b> Shuffle 'Reliquary Prime' into
    # your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_197t")


class BT_197t:
    """Reliquary Prime"""

    # [x]<b><b>Taunt</b>, Lifesteal</b> Only you can target this with spells
    # and Hero Powers.
    update = CurrentPlayer(OPPONENT) & Refresh(
        SELF,
        {
            GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
            GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
        },
    )


class BT_254:
    """Sethekk Veilweaver / 塞泰克织巢者
    在你对一个随从施放法术后，随机将一张牧师法术牌置入你的 手牌。"""

    # [x]After you cast a spell on a minion, add a Priest spell to your hand.
    events = Play(CONTROLLER, SPELL, MINION).after(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.PRIEST))
    )


class BT_256:
    """Dragonmaw Overseer / 龙喉监工
    在你的回合结束时，使另一个友方随从获得+2/+2。"""

    # At the end of your turn, give another friendly minion +2/+2.
    events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "BT_256e"))


BT_256e = buff(+2, +2)


class BT_258:
    """Imprisoned Homunculus / 被禁锢的矮劣魔
    休眠2回合。嘲讽"""

    # <b>Dormant</b> for 2 turns. <b>Taunt</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2


class BT_262:
    """Dragonmaw Sentinel / 龙喉哨兵
    战吼：如果你的手牌中有龙牌，便获得+1攻击力和吸血。"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain +1 Attack and
    # <b>Lifesteal</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "BT_262e")


BT_262e = buff(atk=1, lifesteal=True)


class BT_341:
    """Skeletal Dragon / 骸骨巨龙
    嘲讽 在你的回合结束时，将一张龙牌置入你的手牌。"""

    # [x]<b>Taunt</b> At the end of your turn, add a Dragon to your hand.
    events = OWN_TURN_END.on(Give(CONTROLLER, RandomDragon()))


##
# Spells


class BT_198:
    """Soul Mirror / 灵魂之镜
    召唤所有敌方随从的复制，并使敌方随从攻击其复制。"""

    # Summon copies of enemy minions. They attack their copies.
    def play(self):
        for entity in ENEMY_MINIONS.eval(self.game, self):
            yield Summon(CONTROLLER, ExactCopy(SELF).evaluate(entity)).then(
                Attack(Summon.CARD, entity)
            )


class BT_252:
    """Renew / 复苏
    恢复#3点 生命值。发现一张法术牌。"""

    # Restore #3 Health. <b>Discover</b> a spell.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 3), DISCOVER(RandomSpell())


class BT_253:
    """Psyche Split / 心灵分裂
    使一个随从获得+1/+2，并召唤一个它的复制。"""

    # Give a minion +1/+2. Summon a copy of it.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "BT_253e"), Summon(CONTROLLER, ExactCopy(TARGET))


class BT_257:
    """Apotheosis / 神圣化身
    使一个随从获得+2/+3和吸血。"""

    # Give a minion +2/+3 and <b>Lifesteal</b>.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "BT_257e")


BT_257e = buff(+2, +3, lifesteal=True)
